from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from base_watcher import BaseWatcher, ensure_directories


class FinanceWatcher(BaseWatcher):
    def __init__(self, vault_path: Path, check_interval: int = 300) -> None:
        super().__init__(vault_path, check_interval)
        self.accounting_path = self.vault_path / "Accounting"
        ensure_directories([self.needs_action_path, self.accounting_path])
        self.logger = logging.getLogger("FinanceWatcher")

    def check_for_updates(self) -> list[dict[str, Any]]:
        """Placeholder for bank API/CSV polling."""
        self.logger.info("Polling finance sources for transactions")
        # TODO: Implement bank API polling or CSV import.
        return []

    def _log_transaction(self, transaction: dict[str, Any]) -> None:
        month_folder = self.accounting_path / datetime.now(timezone.utc).strftime("%Y-%m")
        ensure_directories([month_folder])
        ledger = month_folder / "Current_Month.md"
        entry = "- {date} | {description} | {amount}\n".format(
            date=transaction["date"],
            description=transaction["description"],
            amount=transaction["amount"],
        )
        if ledger.exists():
            ledger.write_text(ledger.read_text() + entry)
        else:
            ledger.write_text("# Current Month Transactions\n\n" + entry)

    def create_action_file(self, item: dict[str, Any]) -> Path:
        self._log_transaction(item)
        path = self.needs_action_path / f"FINANCE_{item['id']}.md"
        content = """---
type: finance
transaction_id: {transaction_id}
amount: {amount}
priority: {priority}
status: pending
---
## Transaction Details
- Date: {date}
- Description: {description}
- Amount: {amount}
""".format(
            transaction_id=item["id"],
            amount=item["amount"],
            priority="high" if float(item["amount"]) > 500 else "normal",
            date=item["date"],
            description=item["description"],
        )
        path.write_text(content)
        return path


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    vault_path = Path(os.getenv("VAULT_PATH", "AI_Employee_Vault"))
    watcher = FinanceWatcher(vault_path=vault_path)
    watcher.run()


if __name__ == "__main__":
    main()
