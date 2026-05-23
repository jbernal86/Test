# Install Guide — Agent AI Plug Realtor OS

This guide is written for a simple demo install. It is intentionally safe and uses fake sample data.

## What this installs

The demo generates three outputs:

- `output/dashboard.html` — polished product-style command center
- `output/daily_report.md` — daily operator report
- `output/approval_queue.json` — structured approval queue

## Requirements

- Python 3.11+
- Git
- A terminal

## Step 1 — Clone the repo

```bash
git clone https://github.com/jbernal86/Test.git
cd Test
```

## Step 2 — Create a virtual environment

Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

## Step 4 — Run tests

```bash
pytest
```

## Step 5 — Generate the demo

```bash
python -m agent_ai_plug.operator
```

## Step 6 — Open the dashboard

Open this file in your browser:

```text
output/dashboard.html
```

## Important safety note

Do not put real client data into this public demo repo.

Do not add:

- API keys
- passwords
- real CRM exports
- client names/contact information
- MLS data
- private transaction details

Use fake or sanitized sample data only.
