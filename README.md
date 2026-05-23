# Agent AI Plug — Realtor Agent Kit

A testable starter kit for building AI agent systems that real estate agents can actually use.

This repo is not meant to be a random AI playground. It is the product foundation for **Agent AI Plug**: plug-and-play agent workflows for working Realtors who need practical help with lead follow-up, CRM cleanup, content, listing prep, client communication, and daily execution.

## Big idea

Most agents do not need a chatbot. They need a small team of focused AI agents that can:

- read structured inputs
- identify what matters
- draft useful outputs
- queue actions for approval
- avoid compliance landmines
- create repeatable daily business leverage

## V1 goal

Build a kit of safe, reusable Realtor agents that can run against fake/sample data first.

Nothing sends automatically. Nothing touches a live CRM. Nothing uses private client data. The first job is to prove the workflow works.

## Agent kit included

Planned agents live in `/agents`:

1. **Lead Triage Agent** — ranks leads and recommends the next move.
2. **Follow-Up Drafting Agent** — drafts short human-sounding texts/emails.
3. **CRM Cleanup Agent** — flags missing tags, stale leads, duplicates, and bad records.
4. **Listing Prep Agent** — creates listing checklist, photo notes, description angles, and seller questions.
5. **Content Repurposing Agent** — turns one idea into posts, captions, email, and short video scripts.
6. **Open House Follow-Up Agent** — turns sign-in notes into segmented follow-up drafts.
7. **Compliance Review Agent** — checks outputs for obvious Fair Housing, advertising, and overclaim issues.
8. **Daily Operator Agent** — creates the daily command plan and approval queue.

## Repo structure

```text
agents/              Agent specs, prompts, inputs, outputs, safety rules
agent_ai_plug/       Python package for testable agent workflows
data/                Fake sample data only
output/              Generated demo outputs, ignored locally if desired
tests/               Automated tests
.github/workflows/   GitHub Actions test runner
sales/               Product packaging, offer, demos, install docs
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
python -m agent_ai_plug.operator
```

Generated demo outputs:

```text
output/daily_report.md
output/approval_queue.json
```

## Safety rules

This repo should stay safe by default:

- No API keys
- No passwords
- No real client names or contact info
- No MLS data
- No CRM exports
- No automatic sending
- No financial actions
- Human approval required before external actions

## Product direction

This should become a sellable install kit for Realtors:

- Starter prompts
- Agent specs
- Demo workflows
- Setup instructions
- Compliance guardrails
- CRM export templates
- Approval queue workflow
- Optional Notion/GitHub dashboard
- Optional n8n/Zapier/Make build paths

## First sellable version

The first version should be simple:

**Agent AI Plug: Realtor Daily Operator Kit**

It helps an agent answer every morning:

1. Who should I contact first?
2. What should I say?
3. What needs cleanup?
4. What content can I post today?
5. What requires my approval before sending?

That is practical, valuable, and easy to demo.
