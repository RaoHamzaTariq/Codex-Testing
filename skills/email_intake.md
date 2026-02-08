# Skill: Email Intake (Gmail)

## Purpose
Poll Gmail for unread + important emails and convert them into actionable Markdown files in the Obsidian vault.

## Entry Point
- `gmail_watcher.py`

## Inputs
- OAuth2 credentials via environment variables
- Gmail API scope: read-only

## Outputs
- `AI_Employee_Vault/Needs_Action/EMAIL_{message_id}.md`
