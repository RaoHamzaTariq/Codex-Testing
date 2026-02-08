# Setup & Configuration Guide

This guide walks you through configuring the complete system, from vault setup to orchestrator + watchers + MCP servers.

## 1) Prerequisites
- Python 3.13+
- Claude Code CLI available as `claude`
- Node.js 24+ (for MCP servers)
- Obsidian installed (optional for GUI access)

## 2) Vault Setup (Obsidian)
1. Open Obsidian.
2. **Open folder as vault** and select `AI_Employee_Vault/`.
3. Confirm that `Dashboard.md`, `Company_Handbook.md`, and `Business_Goals.md` appear.

## 3) Environment Configuration
1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```
2. Populate required values:
   - `GMAIL_CLIENT_ID`
   - `GMAIL_CLIENT_SECRET`
   - `BANK_API_TOKEN`
   - `WHATSAPP_SESSION_PATH`
   - `CLAUDE_API_KEY`
   - `VAULT_PATH=AI_Employee_Vault`
   - `DEV_MODE=true`

> **Note**: Secrets must never be committed. See `SECURITY.md` for storage guidance.

## 4) MCP Server Configuration
1. Copy the example config:
   ```bash
   mkdir -p ~/.config/claude-code
   cp mcp.json.example ~/.config/claude-code/mcp.json
   ```
2. Edit `~/.config/claude-code/mcp.json` to point to your MCP server binaries.
3. Verify that each MCP server can start manually before using the orchestrator.

## 5) Watcher Configuration
### Gmail Watcher
- Implements OAuth2 polling for unread + important emails.
- Configure OAuth credentials via `.env`.
- The watcher tracks processed message IDs in `AI_Employee_Vault/Logs/gmail_state.json`.

### WhatsApp Watcher
- Uses Playwright with session persistence.
- Set `WHATSAPP_SESSION_PATH` to a secure local file path.

### Finance Watcher
- Integrate bank APIs or CSV parsing.
- Logs ledger entries to `AI_Employee_Vault/Accounting/YYYY-MM/Current_Month.md`.

## 6) Run the Core Processes
```bash
python orchestrator.py
python gmail_watcher.py
python whatsapp_watcher.py
python finance_watcher.py
```

## 7) Run the Web Dashboard (React + Tailwind)
```bash
cd frontend
npm install
npm run dev
```
Then open the URL printed by Vite (usually `http://localhost:5173`).

## 8) Run the Control Center API (FastAPI)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
The API will be available at `http://localhost:8000` and exposes `/api/*` endpoints plus an SSE stream at `/ws/events`.

## 9) Approval Workflow
1. Sensitive actions are written to `AI_Employee_Vault/Pending_Approval/`.
2. Approve by moving files to `AI_Employee_Vault/Approved/`.
3. Reject by moving files to `AI_Employee_Vault/Rejected/`.

## 10) Weekly CEO Briefing
Run the briefing generator manually:
```bash
python weekly_audit.py
```
Briefings are created under `AI_Employee_Vault/Briefings/`.

## 11) PM2 (Optional Production Supervisor)
```bash
pm2 start orchestrator.py --interpreter python3 --name "orchestrator"
pm2 start gmail_watcher.py --interpreter python3 --name "gmail-watcher"
pm2 start whatsapp_watcher.py --interpreter python3 --name "whatsapp-watcher"
pm2 start finance_watcher.py --interpreter python3 --name "finance-watcher"
pm2 save
pm2 startup
```

## 12) End-to-End Invoice Flow Test
1. Simulate a WhatsApp message with keyword `invoice`.
2. Confirm the watcher creates `Needs_Action/WHATSAPP_*.md`.
3. Orchestrator triggers Claude to create a plan in `Plans/`.
4. Claude writes an approval request to `Pending_Approval/`.
5. Move the approval file to `Approved/`.
6. Orchestrator detects approval and logs the action.
7. Verify `Dashboard.md` updates and files move to `Done/`.
