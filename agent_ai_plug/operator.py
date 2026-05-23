from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent_ai_plug.dashboard import write_dashboard

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
        "seller_lead": 70,
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

    note = lead.notes.lower()
    if "pre-approved" in note or "listing appointment" in note:
        score += 20
    if "needs follow-up" in note or "asked" in note:
        score += 10
    if "cash" in note or "relocation" in note:
        score += 8

    return score


def recommend_action(lead: Lead) -> str:
    if lead.intent == "ready_now":
        return "Call first, then send a short follow-up text if no answer."
    if lead.intent == "seller_lead":
        return "Prepare seller consult questions and offer a pricing strategy call."
    if lead.intent == "active_search":
        return "Send a helpful check-in with one clear next step."
    if lead.intent == "nurture":
        return "Send value-based follow-up, no pressure."
    return "Leave alone unless there is a clear reason to re-engage."


def draft_message(lead: Lead) -> str:
    if lead.intent == "ready_now":
        return f"Hey {lead.name}, I saw your note come through and wanted to help with the next step. Are you available for a quick call today?"
    if lead.intent == "seller_lead":
        return f"Hey {lead.name}, I can help you get a realistic pricing strategy together. Want me to take a look and give you a straight read on where the home likely sits?"
    if lead.intent == "active_search":
        return f"Hey {lead.name}, want me to narrow down a few solid options in your price range instead of you having to sort through everything?"
    if lead.intent == "nurture":
        return f"Hey {lead.name}, hope you’re doing well. No pressure, just wanted to see if your plans around buying or selling have changed at all."
    return f"Hey {lead.name}, just checking in. If real estate is back on your radar, I’m happy to help."


def rank_leads(leads: list[Lead]) -> list[dict[str, Any]]:
    return sorted(
        [
            {
                "agent": "Lead Triage Agent",
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
            for lead in leads
        ],
        key=lambda item: item["score"],
        reverse=True,
    )


def build_crm_cleanup(leads: list[Lead]) -> list[dict[str, str]]:
    cleanup: list[dict[str, str]] = []
    for lead in leads:
        if lead.last_activity_days >= 30:
            cleanup.append(
                {
                    "agent": "CRM Cleanup Agent",
                    "record": lead.name,
                    "issue": "Stale lead",
                    "recommendation": "Review before archiving or placing into a long-term nurture bucket.",
                }
            )
        if lead.price_range.lower() == "unknown":
            cleanup.append(
                {
                    "agent": "CRM Cleanup Agent",
                    "record": lead.name,
                    "issue": "Missing price range",
                    "recommendation": "Ask a simple qualifying question before sending property options.",
                }
            )
    return cleanup


def build_content_queue(content_ideas: list[dict[str, Any]]) -> list[dict[str, str]]:
    queue: list[dict[str, str]] = []
    for idea in content_ideas:
        topic = idea["topic"]
        queue.append(
            {
                "agent": "Content Repurposing Agent",
                "topic": topic,
                "facebook_post": f"A lot of buyers overcomplicate this: {topic}. Here’s the simple version agents should explain clearly.",
                "short_video_script": f"Hook: Most buyers miss this. Topic: {topic}. Close: Want the simple version? Message me and I’ll walk you through it.",
                "approval_required": "true",
            }
        )
    return queue


def build_daily_report(
    ranked_leads: list[dict[str, Any]],
    tasks: list[dict[str, Any]],
    calendar: list[dict[str, Any]],
    cleanup: list[dict[str, Any]],
    content_queue: list[dict[str, Any]],
) -> str:
    urgent_tasks = [task for task in tasks if task.get("priority") == "high"]

    lines = [
        "# Agent AI Plug Daily Operator Demo",
        "",
        "## Today: Money First",
        "",
    ]

    for lead in ranked_leads[:5]:
        lines.append(f"- **{lead['name']}** — score {lead['score']} — {lead['recommended_action']}")

    lines.extend(["", "## Drafts Awaiting Approval", ""])
    for lead in ranked_leads[:3]:
        lines.append(f"- **{lead['name']}**: {lead['draft_message']}")

    lines.extend(["", "## CRM Cleanup Flags", ""])
    if cleanup:
        for item in cleanup:
            lines.append(f"- **{item['record']}** — {item['issue']}: {item['recommendation']}")
    else:
        lines.append("- No cleanup flags found in sample data.")

    lines.extend(["", "## Content Queue", ""])
    for item in content_queue[:3]:
        lines.append(f"- **{item['topic']}** — draft post and video script ready for review.")

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
            "## Approval Rule",
            "",
            "Nothing sends automatically. The Realtor reviews, edits, approves, skips, or escalates.",
        ]
    )

    return "\n".join(lines) + "\n"


def write_outputs() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    leads = load_leads()
    tasks = load_json(DATA_DIR / "tasks.json")
    calendar = load_json(DATA_DIR / "calendar.json")
    content_ideas = load_json(DATA_DIR / "content_ideas.json")

    ranked = rank_leads(leads)
    cleanup = build_crm_cleanup(leads)
    content_queue = build_content_queue(content_ideas)
    approval_queue = ranked[:5] + cleanup + content_queue

    report = build_daily_report(ranked, tasks, calendar, cleanup, content_queue)

    (OUTPUT_DIR / "daily_report.md").write_text(report, encoding="utf-8")
    (OUTPUT_DIR / "approval_queue.json").write_text(json.dumps(approval_queue, indent=2), encoding="utf-8")
    write_dashboard()


if __name__ == "__main__":
    write_outputs()
    print("Generated output/daily_report.md")
    print("Generated output/approval_queue.json")
    print("Generated output/dashboard.html")
