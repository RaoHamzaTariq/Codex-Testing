from __future__ import annotations

import json
import logging
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from base_watcher import ensure_directories


class Orchestrator:
    def __init__(self, vault_path: Path, check_interval: int = 10) -> None:
        self.vault_path = vault_path
        self.check_interval = check_interval
        self.needs_action_path = vault_path / "Needs_Action"
        self.in_progress_path = vault_path / "In_Progress" / "claude_code"
        self.done_path = vault_path / "Done"
        self.pending_approval_path = vault_path / "Pending_Approval"
        self.approved_path = vault_path / "Approved"
        self.logs_path = vault_path / "Logs"
        ensure_directories(
            [
                self.needs_action_path,
                self.in_progress_path,
                self.done_path,
                self.pending_approval_path,
                self.approved_path,
                self.logs_path,
            ]
        )
        self.logger = logging.getLogger("Orchestrator")

    def _log(self, action_type: str, payload: dict[str, str]) -> None:
        self.logs_path.mkdir(parents=True, exist_ok=True)
        log_file = self.logs_path / f"{datetime.now(timezone.utc):%Y-%m-%d}.json"
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action_type": action_type,
            "actor": "claude_code",
            "parameters": payload,
        }
        if log_file.exists():
            data = json.loads(log_file.read_text())
        else:
            data = []
        data.append(entry)
        log_file.write_text(json.dumps(data, indent=2))

    def _run_claude(self, prompt: str) -> str:
        command = ["claude", "--cwd", str(self.vault_path), prompt]
        result = subprocess.run(command, check=False, capture_output=True, text=True)
        output = (result.stdout + result.stderr).strip()
        return output

    def _ralph_wiggum_loop(self, prompt: str, task_file: Path) -> None:
        while True:
            output = self._run_claude(prompt)
            self._log("claude_output", {"output": output[:5000]})
            if "TASK_COMPLETE" in output or not task_file.exists():
                break
            prompt = f"Continue from where you left off. Previous output: {output}"

    def _process_task(self, task_file: Path) -> None:
        claimed = self.in_progress_path / task_file.name
        task_file.rename(claimed)
        prompt = f"Process {claimed}"
        self._ralph_wiggum_loop(prompt, claimed)
        if claimed.exists():
            claimed.rename(self.done_path / claimed.name)

    def _process_approved_actions(self) -> None:
        for approval_file in self.approved_path.glob("*.md"):
            self._log("approved_action_detected", {"file": str(approval_file)})
            approval_file.rename(self.done_path / approval_file.name)

    def run(self) -> None:
        self.logger.info("Starting orchestrator")
        while True:
            try:
                for task_file in self.needs_action_path.glob("*.md"):
                    self._process_task(task_file)
                self._process_approved_actions()
            except Exception as exc:  # noqa: BLE001
                self.logger.exception("Orchestrator error: %s", exc)
            time.sleep(self.check_interval)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    vault_path = Path(os.getenv("VAULT_PATH", "AI_Employee_Vault"))
    orchestrator = Orchestrator(vault_path=vault_path)
    orchestrator.run()


if __name__ == "__main__":
    main()
