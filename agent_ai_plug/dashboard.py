from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from agent_ai_plug.agents import agent_cards

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"


def render_agent_card(agent: dict[str, Any]) -> str:
    outputs = "".join(f"<li>{escape(item)}</li>" for item in agent["outputs"])
    safety = "".join(f"<li>{escape(item)}</li>" for item in agent["safety_rules"])
    return f"""
    <section class=\"card\">
      <div class=\"eyebrow\">Agent</div>
      <h2>{escape(agent['name'])}</h2>
      <p class=\"role\">{escape(agent['role'])}</p>
      <p>{escape(agent['customer_value'])}</p>
      <div class=\"grid2\">
        <div>
          <h3>Outputs</h3>
          <ul>{outputs}</ul>
        </div>
        <div>
          <h3>Safety</h3>
          <ul>{safety}</ul>
        </div>
      </div>
    </section>
    """


def render_dashboard() -> str:
    cards = "\n".join(render_agent_card(agent) for agent in agent_cards())
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Agent AI Plug Realtor OS</title>
  <style>
    :root {{
      --bg: #0b1220;
      --panel: #111a2e;
      --card: #16213a;
      --text: #eef4ff;
      --muted: #a8b3c7;
      --accent: #55d6be;
      --warning: #ffd166;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: radial-gradient(circle at top left, #1f3159, var(--bg));
      color: var(--text);
      line-height: 1.5;
    }}
    header {{
      padding: 48px 28px 28px;
      max-width: 1180px;
      margin: 0 auto;
    }}
    .brand {{
      color: var(--accent);
      font-weight: 700;
      letter-spacing: .12em;
      text-transform: uppercase;
      font-size: 13px;
    }}
    h1 {{
      font-size: clamp(36px, 6vw, 72px);
      line-height: .95;
      margin: 12px 0 18px;
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 20px;
      max-width: 780px;
    }}
    .shell {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 0 28px 56px;
    }}
    .hero-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin: 24px 0;
    }}
    .metric, .card {{
      background: rgba(22, 33, 58, .88);
      border: 1px solid rgba(255,255,255,.09);
      border-radius: 22px;
      padding: 22px;
      box-shadow: 0 20px 60px rgba(0,0,0,.22);
    }}
    .metric strong {{ display: block; font-size: 30px; }}
    .metric span {{ color: var(--muted); }}
    .section-title {{
      margin-top: 38px;
      font-size: 28px;
    }}
    .agent-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }}
    .eyebrow {{
      color: var(--accent);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: .14em;
      font-weight: 700;
    }}
    h2 {{ margin: 8px 0; }}
    h3 {{ color: var(--warning); margin-bottom: 6px; }}
    .role {{ color: var(--muted); font-weight: 700; }}
    .grid2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}
    li {{ margin-bottom: 6px; }}
    .workflow {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-top: 18px;
    }}
    .step {{
      background: rgba(255,255,255,.06);
      border: 1px solid rgba(255,255,255,.08);
      border-radius: 18px;
      padding: 16px;
      min-height: 120px;
    }}
    .step b {{ color: var(--accent); }}
    footer {{ color: var(--muted); margin-top: 38px; }}
    @media (max-width: 900px) {{
      .hero-grid, .agent-grid, .workflow {{ grid-template-columns: 1fr; }}
      .grid2 {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class=\"brand\">Agent AI Plug</div>
    <h1>Realtor OS Agent Kit</h1>
    <p class=\"subtitle\">A practical AI command center for real estate agents: prioritize leads, draft follow-up, clean CRM chaos, prepare listings, create content, and require human approval before action.</p>
  </header>
  <main class=\"shell\">
    <section class=\"hero-grid\">
      <div class=\"metric\"><strong>8</strong><span>Focused agents</span></div>
      <div class=\"metric\"><strong>0</strong><span>Auto-sent messages in V1</span></div>
      <div class=\"metric\"><strong>5 min</strong><span>Demo goal</span></div>
      <div class=\"metric\"><strong>1</strong><span>Daily command queue</span></div>
    </section>

    <h2 class=\"section-title\">Workflow</h2>
    <section class=\"workflow\">
      <div class=\"step\"><b>1. Input</b><br>CRM export, notes, tasks, content ideas, listing facts.</div>
      <div class=\"step\"><b>2. Analyze</b><br>Agents score, flag, segment, and prepare recommendations.</div>
      <div class=\"step\"><b>3. Draft</b><br>Messages, plans, checklists, posts, and scripts are created.</div>
      <div class=\"step\"><b>4. Approve</b><br>The Realtor edits, approves, skips, or escalates.</div>
      <div class=\"step\"><b>5. Log</b><br>Actions and outcomes become tomorrow’s operating context.</div>
    </section>

    <h2 class=\"section-title\">Agent Library</h2>
    <section class=\"agent-grid\">
      {cards}
    </section>

    <footer>
      Built for safe demo mode first. Do not use real client data, MLS data, secrets, or private CRM exports in this public repo.
    </footer>
  </main>
</body>
</html>
"""


def write_dashboard() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "dashboard.html").write_text(render_dashboard(), encoding="utf-8")


if __name__ == "__main__":
    write_dashboard()
    print("Dashboard generated in output/dashboard.html")
