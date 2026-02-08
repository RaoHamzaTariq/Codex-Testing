from __future__ import annotations

import json
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


class BaseWatcher(ABC):
    def __init__(self, vault_path: Path, check_interval: int) -> None:
        self.vault_path = vault_path
        self.check_interval = check_interval
        self.needs_action_path = self.vault_path / "Needs_Action"
        self.logs_path = self.vault_path / "Logs"
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def check_for_updates(self) -> list[dict[str, Any]]:
        """Return new actionable items."""

    @abstractmethod
    def create_action_file(self, item: dict[str, Any]) -> Path:
        """Create a markdown action file for the item."""

    def _log_action(self, action_type: str, payload: dict[str, Any]) -> None:
        self.logs_path.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_path / f"{datetime.now(timezone.utc):%Y-%m-%d}.json"
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action_type": action_type,
            "actor": self.__class__.__name__,
            "parameters": payload,
        }
        if log_file.exists():
            data: list[dict[str, Any]] = json.loads(log_file.read_text())
        else:
            data = []
        data.append(entry)
        log_file.write_text(json.dumps(data, indent=2))

    def run(self) -> None:
        self.logger.info("Starting watcher with interval %s seconds", self.check_interval)
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    action_path = self.create_action_file(item)
                    self._log_action("action_file_created", {"path": str(action_path)})
            except Exception as exc:  # noqa: BLE001
                self.logger.exception("Watcher error: %s", exc)
            time.sleep(self.check_interval)


def ensure_directories(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
