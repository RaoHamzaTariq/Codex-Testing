from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from base_watcher import ensure_directories


def generate_briefing(vault_path: Path) -> Path:
    briefings_path = vault_path / "Briefings"
    done_path = vault_path / "Done"
    accounting_path = vault_path / "Accounting"
    goals_path = vault_path / "Business_Goals.md"

    ensure_directories([briefings_path, done_path, accounting_path])

    period_end = datetime.now(timezone.utc).date()
    period_start = period_end - timedelta(days=7)

    completed_tasks = [p.stem for p in done_path.glob("*.md")]
    revenue_summary = "Pending accounting aggregation"

    content = f"""---
generated: {datetime.now(timezone.utc).isoformat()}
period: {period_start} to {period_end}
---
# Monday Morning CEO Briefing

## Executive Summary
Weekly audit generated. Review goals in {goals_path.name}.

## Revenue
- **Summary**: {revenue_summary}

## Completed Tasks
"""

    if completed_tasks:
        content += "\n".join(f"- [x] {task}" for task in completed_tasks)
    else:
        content += "- _No completed tasks logged._"

    content += """

## Bottlenecks
| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| _None detected_ | - | - | - |

## Proactive Suggestions
- Review subscriptions over $600/month.
- Confirm upcoming deadlines.
"""

    briefing_path = briefings_path / f"{period_end}_Monday_Briefing.md"
    briefing_path.write_text(content)
    return briefing_path


def main() -> None:
    vault_path = Path(os.getenv("VAULT_PATH", "AI_Employee_Vault"))
    path = generate_briefing(vault_path)
    print(f"Briefing generated: {path}")


if __name__ == "__main__":
    main()
