# Security & Privacy

## Credential Management
- Store secrets in a `.env` file (never commit to Git).
- Required environment variables:
  - `GMAIL_CLIENT_ID`
  - `GMAIL_CLIENT_SECRET`
  - `BANK_API_TOKEN`
  - `WHATSAPP_SESSION_PATH`
  - `CLAUDE_API_KEY`
- Use OS keychains or secret managers for production.

## HITL Safeguards
- Sensitive actions must create approval files in `Pending_Approval/`.
- Only files moved to `Approved/` are executed.
- High-risk actions (payments > $100, new contacts) require explicit approval.

## Audit Logging
- All actions log to `AI_Employee_Vault/Logs/YYYY-MM-DD.json`.
- Logs must be retained for at least 90 days.

## DEV_MODE
- Default to `DEV_MODE=true` to prevent real external actions.
- Implement `--dry-run` flags for any action scripts.
