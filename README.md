# Digital FTE (Local-First AI Employee)

This repository delivers a local-first, agentic system that uses Claude Code for reasoning and an Obsidian vault for memory, tasks, approvals, and audit trails.

## Architecture Overview
- **Brain**: Claude Code orchestrated via `orchestrator.py`, with a Ralph Wiggum stop-hook loop for autonomous iteration.
- **Memory/GUI**: Obsidian vault at `AI_Employee_Vault/` with task flow and dashboards.
- **Perception**: Python watchers for Gmail, WhatsApp, and finance sources.
- **Action Layer**: MCP servers for email, browser, WhatsApp, calendar, and accounting integrations.
- **Human-in-the-loop**: Approval workflow using file moves between `Pending_Approval/`, `Approved/`, and `Rejected/`.

## What’s Included
- Vault structure and seed files (`Dashboard.md`, `Company_Handbook.md`, `Business_Goals.md`).
- Watcher scaffolding for Gmail, WhatsApp, and finance intake.
- Orchestrator with the Ralph Wiggum loop.
- Weekly CEO briefing generator.
- Security, setup, and skills documentation.

## Quick Start
1. Follow the **full configuration guide** in `SETUP.md`.
2. Open `AI_Employee_Vault/` as an Obsidian vault (optional but recommended).
3. Start the orchestrator and any watchers you’ve configured.

## Repository Layout
```
AI_Employee_Vault/    # Obsidian vault
base_watcher.py       # Abstract watcher class
orchestrator.py       # Claude Code orchestrator + stop-hook loop
retry_handler.py      # Retry utilities
weekly_audit.py       # Weekly CEO briefing generator
```

## Testing Scenario
See `SETUP.md` for the end-to-end invoice flow test scenario and validation checklist.
