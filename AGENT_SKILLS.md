# Agent Skills Catalog

All AI functionality is implemented as reusable skills. Each skill has a short description and the entry point script.

## Skills
- **Email Intake (Gmail)**: Poll Gmail for unread + important messages and create actionable Markdown files. (`gmail_watcher.py`)
- **WhatsApp Intake**: Poll WhatsApp Web, detect keywords, and create action files. (`whatsapp_watcher.py`)
- **Finance Intake**: Poll banking sources or CSV, log transactions, and flag anomalies. (`finance_watcher.py`)
- **Claude Orchestration**: Process `/Needs_Action` items with the Ralph Wiggum loop and move tasks through the vault. (`orchestrator.py`)
- **Weekly Briefing**: Generate Monday Morning CEO briefing summaries. (`weekly_audit.py`)
- **Retry Handling**: Shared retry/backoff utilities for API calls. (`retry_handler.py`)

## Usage Example
1. Add a new action file in `AI_Employee_Vault/Needs_Action/`.
2. Run `python orchestrator.py` to trigger Claude processing.
3. Review approval files in `AI_Employee_Vault/Pending_Approval/`.
