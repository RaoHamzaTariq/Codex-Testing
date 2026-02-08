from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from base_watcher import BaseWatcher, ensure_directories


class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: Path, check_interval: int = 120) -> None:
        super().__init__(vault_path, check_interval)
        self.state_path = self.vault_path / "Logs" / "gmail_state.json"
        ensure_directories([self.needs_action_path, self.state_path.parent])
        self.logger = logging.getLogger("GmailWatcher")

    def _load_state(self) -> set[str]:
        if not self.state_path.exists():
            return set()
        return set(json.loads(self.state_path.read_text()))

    def _save_state(self, message_ids: set[str]) -> None:
        self.state_path.write_text(json.dumps(sorted(message_ids), indent=2))

    def check_for_updates(self) -> list[dict[str, Any]]:
        """Placeholder for Gmail API polling."""
        self.logger.info("Polling Gmail for unread + important emails")
        # TODO: Implement Gmail API polling with OAuth2 credentials
        # For now, return empty list.
        return []

    def create_action_file(self, item: dict[str, Any]) -> Path:
        message_id = item["message_id"]
        path = self.needs_action_path / f"EMAIL_{message_id}.md"
        content = """---
type: email
from: {sender}
subject: "{subject}"
received: {received}
priority: {priority}
status: pending
---
## Email Content
{snippet}

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
""".format(
            sender=item["from"],
            subject=item["subject"],
            received=item["received"],
            priority=item.get("priority", "high"),
            snippet=item.get("snippet", ""),
        )
        path.write_text(content)
        processed_ids = self._load_state()
        processed_ids.add(message_id)
        self._save_state(processed_ids)
        return path


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    vault_path = Path(os.getenv("VAULT_PATH", "AI_Employee_Vault"))
    watcher = GmailWatcher(vault_path=vault_path)
    watcher.run()


if __name__ == "__main__":
    main()
