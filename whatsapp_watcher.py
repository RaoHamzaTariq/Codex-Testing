from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from base_watcher import BaseWatcher, ensure_directories

KEYWORDS = {"urgent", "asap", "invoice", "payment", "help"}


class WhatsAppWatcher(BaseWatcher):
    def __init__(self, vault_path: Path, check_interval: int = 30) -> None:
        super().__init__(vault_path, check_interval)
        self.session_path = Path(os.getenv("WHATSAPP_SESSION_PATH", "./whatsapp_session.json"))
        ensure_directories([self.needs_action_path, self.session_path.parent])
        self.logger = logging.getLogger("WhatsAppWatcher")

    def check_for_updates(self) -> list[dict[str, Any]]:
        """Placeholder for Playwright-based WhatsApp Web polling."""
        self.logger.info("Polling WhatsApp Web for unread messages")
        # TODO: Implement Playwright automation with session persistence.
        return []

    def create_action_file(self, item: dict[str, Any]) -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        detected = [kw for kw in KEYWORDS if kw in item["message"].lower()]
        path = self.needs_action_path / f"WHATSAPP_{timestamp}.md"
        content = """---
type: whatsapp
chat: "{chat}"
received: {received}
keywords: {keywords}
status: pending
---
## Message
{message}
""".format(
            chat=item["chat"],
            received=item.get("received", datetime.now(timezone.utc).isoformat()),
            keywords=detected,
            message=item["message"],
        )
        path.write_text(content)
        return path


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    vault_path = Path(os.getenv("VAULT_PATH", "AI_Employee_Vault"))
    watcher = WhatsAppWatcher(vault_path=vault_path)
    watcher.run()


if __name__ == "__main__":
    main()
