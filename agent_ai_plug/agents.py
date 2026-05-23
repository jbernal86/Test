from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AgentSpec:
    name: str
    role: str
    customer_value: str
    inputs: list[str]
    outputs: list[str]
    safety_rules: list[str]


AGENTS: list[AgentSpec] = [
    AgentSpec(
        name="Lead Triage Agent",
        role="Ranks leads and explains who needs attention first.",
        customer_value="Stops agents from staring at a messy CRM and guessing who to call.",
        inputs=["lead source", "lead status", "last activity", "notes", "price range"],
        outputs=["priority score", "reason", "recommended next action", "approval item"],
        safety_rules=["Do not contact anyone automatically", "Do not infer protected class information"],
    ),
    AgentSpec(
        name="Follow-Up Drafting Agent",
        role="Drafts short, human follow-up texts, emails, and call openers.",
        customer_value="Gives agents words they can actually send without sounding robotic.",
        inputs=["lead stage", "last note", "intent", "agent tone", "market"],
        outputs=["text draft", "email draft", "call opener", "tone note"],
        safety_rules=["Human approval required", "No creepy activity-monitoring language"],
    ),
    AgentSpec(
        name="CRM Cleanup Agent",
        role="Finds stale leads, missing tags, bad stages, and duplicate records.",
        customer_value="Turns CRM chaos into cleanup tasks that can recover hidden opportunities.",
        inputs=["CRM export", "tags", "stages", "last contacted", "source"],
        outputs=["cleanup list", "duplicate flags", "missing field flags", "suggested tags"],
        safety_rules=["Do not delete records automatically", "Do not overwrite CRM data without approval"],
    ),
    AgentSpec(
        name="Listing Prep Agent",
        role="Builds listing launch checklists and marketing prep notes.",
        customer_value="Helps agents launch listings faster with fewer missed details.",
        inputs=["property facts", "seller notes", "repairs", "photos", "community info"],
        outputs=["seller questions", "photo notes", "launch checklist", "description angles"],
        safety_rules=["Do not invent property features", "Flag facts that need verification"],
    ),
    AgentSpec(
        name="Content Repurposing Agent",
        role="Turns one idea into multiple platform-ready content pieces.",
        customer_value="Helps agents stay visible without reinventing content every day.",
        inputs=["topic", "audience", "market", "platform", "CTA"],
        outputs=["Facebook post", "Instagram caption", "short video script", "email blurb"],
        safety_rules=["Avoid unverified superiority claims", "Avoid protected-class targeting"],
    ),
    AgentSpec(
        name="Open House Follow-Up Agent",
        role="Segments open house visitors and drafts follow-up.",
        customer_value="Turns open house traffic into organized follow-up instead of lost paper notes.",
        inputs=["visitor notes", "timeline", "property", "conversation summary"],
        outputs=["hot/warm/cold segments", "draft texts", "draft emails", "call list"],
        safety_rules=["Human approval required", "Do not add people to campaigns without consent review"],
    ),
    AgentSpec(
        name="Compliance Review Agent",
        role="Reviews copy for obvious risky wording and suggests safer alternatives.",
        customer_value="Gives agents a first-pass guardrail before publishing or sending.",
        inputs=["copy", "intended use", "audience", "claim type"],
        outputs=["risk flags", "safer rewrite", "reason", "approval recommendation"],
        safety_rules=["Not legal advice", "Escalate uncertain issues to broker/legal counsel"],
    ),
    AgentSpec(
        name="Daily Operator Agent",
        role="Creates a money-first daily action plan across leads, tasks, content, and listings.",
        customer_value="Shows the agent what to do today instead of letting them spin.",
        inputs=["ranked leads", "tasks", "calendar", "content goals", "active listings"],
        outputs=["daily plan", "approval queue", "drafted actions", "end-of-day review"],
        safety_rules=["No external actions without approval", "Keep plan realistic and ranked"],
    ),
]


def agent_cards() -> list[dict[str, Any]]:
    return [agent.__dict__ for agent in AGENTS]
