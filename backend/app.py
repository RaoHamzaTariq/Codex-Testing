from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI(title="AI Employee Control Center API")

VAULT_PATH = Path(os.getenv("VAULT_PATH", "AI_Employee_Vault"))


def _read_latest_file(directory: Path, pattern: str) -> str | None:
    files = sorted(directory.glob(pattern))
    if not files:
        return None
    return files[-1].read_text()


def _list_markdown(directory: Path) -> list[dict[str, str]]:
    items = []
    for path in sorted(directory.glob("*.md")):
        items.append({"id": path.stem, "path": str(path), "content": path.read_text()})
    return items


def _move_file(source: Path, destination_dir: Path) -> None:
    destination_dir.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        raise HTTPException(status_code=404, detail="File not found")
    source.rename(destination_dir / source.name)


@app.get("/api/status")
def get_status() -> dict[str, str]:
    return {
        "status": "healthy",
        "last_update": datetime.now(timezone.utc).isoformat(),
        "watchers": "3 watchers configured",
    }


@app.get("/api/inbox")
def get_inbox() -> JSONResponse:
    inbox_path = VAULT_PATH / "Needs_Action"
    inbox_path.mkdir(parents=True, exist_ok=True)
    return JSONResponse(_list_markdown(inbox_path))


@app.post("/api/inbox/{item_id}/ai")
def handle_ai(item_id: str) -> dict[str, str]:
    return {
        "status": "queued",
        "message": f"Claude processing requested for {item_id}",
    }


@app.get("/api/pending")
def get_pending() -> JSONResponse:
    pending_path = VAULT_PATH / "Pending_Approval"
    pending_path.mkdir(parents=True, exist_ok=True)
    return JSONResponse(_list_markdown(pending_path))


@app.post("/api/approve/{item_id}")
def approve_item(item_id: str) -> dict[str, str]:
    source = VAULT_PATH / "Pending_Approval" / f"{item_id}.md"
    _move_file(source, VAULT_PATH / "Approved")
    return {"status": "approved", "id": item_id}


@app.post("/api/reject/{item_id}")
def reject_item(item_id: str) -> dict[str, str]:
    source = VAULT_PATH / "Pending_Approval" / f"{item_id}.md"
    _move_file(source, VAULT_PATH / "Rejected")
    return {"status": "rejected", "id": item_id}


@app.get("/api/logs")
def get_logs() -> dict[str, str | None]:
    logs_path = VAULT_PATH / "Logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    latest = _read_latest_file(logs_path, "*.json")
    return {"latest": latest}


@app.get("/api/briefing")
def get_briefing() -> dict[str, str | None]:
    briefings_path = VAULT_PATH / "Briefings"
    briefings_path.mkdir(parents=True, exist_ok=True)
    latest = _read_latest_file(briefings_path, "*_Monday_Briefing.md")
    return {"latest": latest}


@app.post("/api/command")
def post_command(payload: dict[str, str]) -> dict[str, str]:
    return {
        "status": "received",
        "command": payload.get("command", ""),
    }


@app.get("/ws/events")
def stream_events() -> StreamingResponse:
    def event_generator() -> Iterable[str]:
        while True:
            data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": "heartbeat",
            }
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
