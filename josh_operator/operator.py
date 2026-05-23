from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"


@dataclass(frozen=True)
class Lead:
    name: str
    source: str
    intent: str
    last_activity_days: int
    price_range: str
    notes: str


def load_leads(path: Path = DATA_DIR / "leads.csv") -> list[Lead]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = csv.DictReader(f)
        return [
            Lead(
                name=row["name"],
                source=row["source"],
                intent=row["intent"],
                last_activity_days=int(row["last_activity_days"]),
                price_range=row["price_range"],
                notes=row["notes"],
            )
            for row in rows
        ]


def load_json(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def score_lead(lead: Lead) -> int:
    score = 0

    intent_scores = {
        "ready_now": 80,
        "active_search": 60,
        "nurture": 35,
        "cold": 10,
    }
    score += intent_scores.get(lead.intent, 0)

    if lead.last_activity_days <= 1:
        score += 25
    elif lead.last_activity_days <= 3:
        score += 15
    elif lead.last_activity_days <= 7:
        score += 8

    if "pre-approved" in lead.notes.lower() or "listing appointment" in lead.notes.lower():
        score += 20

    if "needs follow-up" in lead.notes.lower() or "asked" in lead.notes.lower():
        score += 10

    return score


def rank_leads(leads: list[Lead]) -> list[dict[str, Any]]:
    ranked = []
    for lead in leads:
        ranked.append(
            {
                "name": lead.name,
                "source": lead.source,
                "intent": lead.intent,
                "score": score_lead(lead),
                "price_range": lead.price_range,
                "notes": lead.notes,
                "recommended_action": recommend_action(lead),
                "draft_message": draft_message(lead),
                "approval_required": True,
            }
        )
    return sorted(ranked, key=lambda item: item["score"], reverse=True)


def recommend_action(lead: Lead) -> str:
    if lead.intent == "ready_now":
        return "Call first, then send a short follow-up text if no answer."
    if lead.intent == "active_search":
        return "Send a helpful check-in with one clear next step."
    if lead.intent == "nurture":
        return "Send value-based follow-up, no pressure."
    return "Leave alone unless there is a clear reason to re-engage."


def draft_message(lead: Lead) -> str:
    if lead.intent == "ready_now":
        return f"Hey {lead.name}, I saw your note come through and wanted to help you with the next step. Are you available for a quick call today? Josh at RE/MAX Casa Grande"
    if lead.intent == "active_search":
        return f"Hey {lead.name}, checking in to see if you want me to narrow down a few good options in your price range instead of you having to sort through everything. Josh at RE/MAX Casa Grande"
    if lead.intent == "nurture":
        return f"Hey {lead.name}, hope you’re doing well. No pressure, just wanted to see if your plans around buying or selling have changed at all. Josh at RE/MAX Casa Grande"
    return f"Hey {lead.name}, just checking in. If real estate is back on your radar, I’m happy to help. Josh at RE/MAX Casa Grande"


def build_daily_report(
    ranked_leads: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    calendar: list[dict[str, Any]],
) -> str:
    urgent_tasks = [task for task in tasks if task.get("priority") == "high"]

    lines = [
        "# Daily Josh Operator Report",
        "",
        "## Money First",
        "",
    ]

    for lead in ranked_leads[:5]:
        lines.append(
            f"- **{lead['name']}** — score {lead['score']} — {lead['recommended_action']}"
        )

    lines.extend(["", "## Urgent Tasks", ""])
    if urgent_tasks:
        for task in urgent_tasks:
            lines.append(f"- **{task['title']}** — {task['due']} — {task['notes']}")
    else:
        lines.append("- No high-priority tasks found.")

    lines.extend(["", "## Calendar", ""])
    if calendar:
        for event in calendar:
            lines.append(f"- **{event['time']}** — {event['title']} — {event['location']}")
    else:
        lines.append("- No events found.")

    lines.extend(
        [
            "",
            "## Approval Queue",
            "",
            "Nothing sends automatically. Review each item before taking action.",
        ]
    )

    return "\n".join(lines) + "\n"


def write_outputs() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    leads = load_leads()
    tasks = load_json(DATA_DIR / "tasks.json")
    calendar = load_json(DATA_DIR / "calendar.json")

    ranked = rank_leads(leads)
    report = build_daily_report(ranked, tasks, calendar)

    (OUTPUT_DIR / "daily_report.md").write_text(report, encoding="utf-8")
    (OUTPUT_DIR / "approval_queue.json").write_text(
        json.dumps(ranked, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    write_outputs()
    print("Daily report generated in output/daily_report.md")
