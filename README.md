# Josh Operator v1

A safe, testable prototype for a personal/business AI operator.

This first version does **not** send emails, texts, update CRM records, touch money, or use real client data. It reads sample inputs and produces:

- a daily action report
- a ranked lead list
- draft follow-up messages
- an approval queue
- tests that prove the workflow works

## Why this exists

The goal is to build a real automation system in layers:

1. **Plan** — decide what matters today.
2. **Draft** — prepare messages and actions.
3. **Approval** — require human review before anything external happens.
4. **Execute** — later, connect approved actions to Gmail, Notion, Calendar, CRM, etc.
5. **Log** — keep a clear record of what happened.

V1 only covers steps 1-3 using fake data so it can be tested safely.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
python -m josh_operator.operator
```

After running it, check:

```text
output/daily_report.md
output/approval_queue.json
```

## Test data

Sample files live in `/data`:

- `leads.csv`
- `tasks.json`
- `calendar.json`

Replace these with fake examples only. Do not commit real client data to this public repo.

## Safety rules

This repo should stay safe by default:

- No API keys
- No passwords
- No real client names or contact info
- No MLS data
- No CRM exports
- No automatic sending
- No financial actions

## Roadmap

### V1 — Current

- Read sample business inputs
- Score leads
- Generate a daily report
- Generate an approval queue
- Run tests in GitHub Actions

### V2 — Local AI drafting

- Add LLM-generated drafts from sanitized inputs
- Keep approval required
- Add message style rules for Josh

### V3 — Real integrations

- Gmail drafts only, no auto-send
- Google Calendar read-only summary
- Notion task logging
- BoldTrail CSV export processor

### V4 — Operator dashboard

- Web UI for approve/edit/skip
- Daily command center
- End-of-day recap
