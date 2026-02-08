# Setup Guide

## Prerequisites
- Python 3.13+
- Claude Code CLI available as `claude`
- Node.js 24+ (for MCP servers)
- Obsidian installed (optional for GUI access)

## Installation
1. Clone the repository.
2. Create a `.env` file for secrets (see `SECURITY.md`).
3. Install Python dependencies you add for watchers (Gmail, Playwright, etc.).
4. Copy `mcp.json.example` to `~/.config/claude-code/mcp.json` and edit paths.

## Run the Core Processes
```bash
python orchestrator.py
python gmail_watcher.py
python whatsapp_watcher.py
python finance_watcher.py
```

## PM2 (Optional)
```bash
pm2 start orchestrator.py --interpreter python3 --name "orchestrator"
pm2 start gmail_watcher.py --interpreter python3 --name "gmail-watcher"
pm2 start whatsapp_watcher.py --interpreter python3 --name "whatsapp-watcher"
pm2 start finance_watcher.py --interpreter python3 --name "finance-watcher"
pm2 save
pm2 startup
```

## End-to-End Invoice Flow Test
1. Simulate a WhatsApp message with keyword `invoice`.
2. Confirm the watcher creates `Needs_Action/WHATSAPP_*.md`.
3. Orchestrator triggers Claude to create a plan in `Plans/`.
4. Claude writes an approval request to `Pending_Approval/`.
5. Move the approval file to `Approved/`.
6. Orchestrator detects approval and logs the action.
7. Verify `Dashboard.md` updates and files move to `Done/`.
