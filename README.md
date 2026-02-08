# Digital FTE (Local-First AI Employee)

This repository contains a local-first, agentic system that uses Claude Code for reasoning and an Obsidian vault for memory, tasks, and audit trails.

## Architecture Overview
- **Brain**: Claude Code orchestrated via `orchestrator.py`, with a Ralph Wiggum stop hook loop for autonomous iteration.
- **Memory/GUI**: Obsidian vault at `AI_Employee_Vault/` with task flow and dashboards.
- **Perception**: Python watchers for Gmail, WhatsApp, and finance sources.
- **Action Layer**: MCP servers for email, browser, WhatsApp, calendar, and accounting integrations.
- **Human-in-the-loop**: Approval workflow using file moves between `Pending_Approval/`, `Approved/`, and `Rejected/`.

## Tier Achieved
**Bronze foundation (with scaffolding for Silver/Gold)**: Vault structure, Claude orchestration loop, three watcher skeletons, HITL folder flow, audit logging, and weekly briefing generation. MCP servers and external APIs are stubbed for local-first development.

## Repository Layout
```
AI_Employee_Vault/    # Obsidian vault
base_watcher.py       # Abstract watcher class
orchestrator.py       # Claude Code orchestrator + stop hook loop
retry_handler.py      # Retry utilities
weekly_audit.py       # Weekly CEO briefing generator
```

## Next Steps
- Wire Gmail API OAuth2 in `gmail_watcher.py`.
- Implement Playwright automation in `whatsapp_watcher.py`.
- Connect bank APIs/CSV parsing in `finance_watcher.py`.
- Integrate MCP servers and fill action execution logic.

## Demo Scenario
See `SETUP.md` for the end-to-end invoice flow test scenario.
