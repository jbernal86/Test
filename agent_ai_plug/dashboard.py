from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from agent_ai_plug.agents import agent_cards

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"


def _default_profile() -> dict[str, Any]:
    return {
        "brand": {
            "product_name": "Agent AI Plug Realtor OS",
            "client_display_name": "Sample Realtor",
            "brokerage_name": "Sample Realty Group",
            "market_area": "Your Market",
            "tagline": "Plug-and-play AI systems for real estate agents",
        },
        "business_rules": {
            "crm_name": "Sample CRM",
            "primary_goal": "prioritize leads, draft follow-up, and create a daily approval queue",
        },
        "compliance": {
            "disclaimer": "Drafting and workflow support only. Human review required."
        },
    }


def render_agent_card(agent: dict[str, Any]) -> str:
    outputs = "".join(f"<li>{escape(item)}</li>" for item in agent["outputs"])
    safety = "".join(f"<li>{escape(item)}</li>" for item in agent["safety_rules"])
    return (
        '<article class="agent-card">'
        '<div class="agent-topline"><span class="pill">Agent</span>'
        '<span class="status">Approval gated</span></div>'
        f'<h3>{escape(agent["name"])}</h3>'
        f'<p class="role">{escape(agent["role"])}</p>'
        f'<p class="value">{escape(agent["customer_value"])}</p>'
        '<div class="mini-grid"><div><h4>Outputs</h4>'
        f'<ul>{outputs}</ul></div><div><h4>Guardrails</h4>'
        f'<ul>{safety}</ul></div></div></article>'
    )


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>__PRODUCT_NAME__</title>
  <style>
    :root {
      --bg: #070b14;
      --panel: rgba(18, 28, 50, .92);
      --panel-soft: rgba(255,255,255,.055);
      --line: rgba(255,255,255,.095);
      --text: #f4f7fb;
      --muted: #9aa8bd;
      --accent: #4ee0c1;
      --accent2: #74a7ff;
      --warning: #ffd166;
      --danger: #ff7a90;
      --shadow: 0 24px 80px rgba(0,0,0,.38);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background: radial-gradient(circle at 20% 0%, rgba(78,224,193,.16), transparent 30%), linear-gradient(135deg, #060913 0%, #0a1020 50%, #080b14 100%);
      line-height: 1.5;
    }
    .app-shell { display: grid; grid-template-columns: 280px minmax(0, 1fr); min-height: 100vh; }
    aside { position: sticky; top: 0; height: 100vh; padding: 28px 20px; background: rgba(7,11,20,.78); border-right: 1px solid var(--line); }
    .logo { display: flex; align-items: center; gap: 12px; margin-bottom: 34px; }
    .mark { width: 42px; height: 42px; border-radius: 14px; display: grid; place-items: center; background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #07101f; font-weight: 900; }
    .logo strong { display: block; } .logo span { color: var(--muted); font-size: 12px; }
    nav { display: grid; gap: 8px; }
    nav a { color: var(--muted); text-decoration: none; padding: 12px 13px; border-radius: 14px; font-weight: 700; font-size: 14px; }
    nav a.active, nav a:hover { background: rgba(255,255,255,.07); color: var(--text); }
    .sidebar-card { margin-top: 28px; padding: 16px; border-radius: 18px; background: rgba(78,224,193,.08); border: 1px solid rgba(78,224,193,.18); color: #dce7f7; font-size: 13px; }
    main { padding: 34px; } .container { max-width: 1280px; margin: 0 auto; }
    .hero { display: grid; grid-template-columns: 1.15fr .85fr; gap: 22px; margin-bottom: 22px; }
    .hero-panel, .panel, .agent-card { background: var(--panel); border: 1px solid var(--line); border-radius: 28px; box-shadow: var(--shadow); }
    .hero-panel { padding: 34px; }
    .eyebrow { color: var(--accent); font-size: 12px; font-weight: 900; letter-spacing: .14em; text-transform: uppercase; }
    h1 { margin: 14px 0 16px; font-size: clamp(38px, 5.8vw, 72px); line-height: .94; letter-spacing: -.065em; }
    .subtitle { color: var(--muted); font-size: 19px; max-width: 760px; }
    .cta-row { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 26px; }
    .button { display: inline-flex; padding: 13px 17px; border-radius: 14px; background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #07101f; font-weight: 850; text-decoration: none; }
    .button.secondary { background: rgba(255,255,255,.08); color: var(--text); border: 1px solid var(--line); }
    .queue-item { display: grid; grid-template-columns: 34px 1fr auto; gap: 12px; align-items: center; padding: 14px 0; border-bottom: 1px solid var(--line); }
    .queue-item:last-child { border-bottom: 0; }
    .num { width: 34px; height: 34px; border-radius: 12px; background: rgba(116,167,255,.15); color: var(--accent2); display: grid; place-items: center; font-weight: 800; }
    .queue-item b { display: block; } .queue-item span { color: var(--muted); font-size: 13px; }
    .score { color: var(--accent); font-weight: 900; background: rgba(78,224,193,.09); border: 1px solid rgba(78,224,193,.16); padding: 7px 10px; border-radius: 999px; font-size: 13px; }
    .metrics, .workflow { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 22px; }
    .metric, .step { padding: 20px; border-radius: 24px; background: var(--panel-soft); border: 1px solid var(--line); }
    .metric strong { display: block; font-size: 30px; letter-spacing: -.04em; }
    .metric span, .step span { color: var(--muted); font-weight: 650; }
    .panel { padding: 26px; margin-bottom: 22px; }
    .section-head h2 { margin: 0; font-size: 28px; letter-spacing: -.035em; } .section-head p { margin: 6px 0 18px; color: var(--muted); }
    .agent-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
    .agent-card { padding: 22px; }
    .agent-topline { display: flex; justify-content: space-between; gap: 10px; align-items: center; }
    .pill, .status { border-radius: 999px; padding: 6px 9px; font-size: 12px; font-weight: 800; }
    .pill { color: #07101f; background: var(--accent); } .status { color: var(--warning); background: rgba(255,209,102,.09); border: 1px solid rgba(255,209,102,.16); }
    .agent-card h3 { margin: 14px 0 8px; font-size: 22px; letter-spacing: -.03em; }
    .role { color: #dce7f7; font-weight: 750; } .value { color: var(--muted); }
    .mini-grid, .install-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 16px; }
    h4 { margin: 0 0 8px; color: var(--warning); } ul { margin: 0; padding-left: 18px; color: var(--muted); } li { margin-bottom: 6px; }
    pre { margin: 0; white-space: pre-wrap; background: #040711; color: #d9f9ef; border: 1px solid rgba(78,224,193,.16); padding: 18px; border-radius: 18px; overflow-x: auto; }
    .warning { color: var(--danger); font-weight: 750; } footer { color: var(--muted); padding: 26px 0 10px; }
    @media (max-width: 1100px) { .app-shell, .hero, .metrics, .workflow, .agent-grid, .install-grid { grid-template-columns: 1fr; } aside { position: relative; height: auto; } }
  </style>
</head>
<body>
  <div class="app-shell">
    <aside>
      <div class="logo"><div class="mark">AI</div><div><strong>Agent AI Plug</strong><span>Realtor OS Demo Kit</span></div></div>
      <nav><a class="active" href="#today">Today</a><a href="#workflow">Workflow</a><a href="#agents">Agent Library</a><a href="#install">Install</a><a href="#safety">Safety</a></nav>
      <div class="sidebar-card"><strong>Installed for:</strong><br />__CLIENT_NAME__<br />__BROKERAGE__<br /><br /><strong>Market:</strong><br />__MARKET_AREA__</div>
    </aside>
    <main><div class="container">
      <section id="today" class="hero">
        <div class="hero-panel"><div class="eyebrow">__TAGLINE__</div><h1>__PRODUCT_NAME__</h1><p class="subtitle">A polished command center customized for __CLIENT_NAME__. It turns __CRM_NAME__ work, follow-up drafts, content ideas, listing prep, and compliance checks into one approval-based daily workflow.</p><div class="cta-row"><a class="button" href="#install">View install flow</a><a class="button secondary" href="#agents">Browse agents</a></div></div>
        <div class="hero-panel"><h2>Today’s Command Queue</h2><div class="queue-item"><div class="num">1</div><div><b>Hot lead follow-up</b><span>Draft ready, approval required</span></div><div class="score">105</div></div><div class="queue-item"><div class="num">2</div><div><b>Seller consult prep</b><span>Pricing call checklist ready</span></div><div class="score">95</div></div><div class="queue-item"><div class="num">3</div><div><b>CRM cleanup</b><span>Stale records flagged</span></div><div class="score">Review</div></div><div class="queue-item"><div class="num">4</div><div><b>Content post</b><span>Caption + short video script ready</span></div><div class="score">Draft</div></div></div>
      </section>
      <section class="metrics"><div class="metric"><strong>8</strong><span>Focused Realtor agents</span></div><div class="metric"><strong>0</strong><span>Auto-sent messages</span></div><div class="metric"><strong>__CRM_NAME__</strong><span>Configured CRM</span></div><div class="metric"><strong>1</strong><span>Daily approval queue</span></div></section>
      <section id="workflow" class="panel"><div class="section-head"><h2>How the system works</h2><p>__PRIMARY_GOAL__</p></div><div class="workflow"><div class="step"><b>1. Import</b><br><span>Use sample data first, then sanitized CRM exports later.</span></div><div class="step"><b>2. Analyze</b><br><span>Agents rank, segment, flag, and prepare recommendations.</span></div><div class="step"><b>3. Draft</b><br><span>Texts, emails, scripts, content, and checklists are created.</span></div><div class="step"><b>4. Approve</b><br><span>The Realtor edits, approves, skips, or escalates.</span></div></div></section>
      <section id="agents" class="panel"><div class="section-head"><h2>Agent Library</h2><p>Each agent has one job, defined inputs, useful outputs, and guardrails.</p></div><div class="agent-grid">__AGENT_CARDS__</div></section>
      <section id="install" class="panel"><div class="section-head"><h2>Custom install flow</h2><p>Edit one client profile file to brand and tune the kit for each Realtor.</p></div><div class="install-grid"><pre>cp config/client_profile.example.json config/client_profile.json
python -m agent_ai_plug.operator</pre><div><h3>Generated files</h3><ul><li>output/dashboard.html</li><li>output/daily_report.md</li><li>output/approval_queue.json</li></ul><p class="warning">Do not add real CRM exports, client data, API keys, passwords, or MLS data to this demo repo.</p></div></div></section>
      <section id="safety" class="panel"><div class="section-head"><h2>Approval-first safety model</h2><p>__DISCLAIMER__</p></div></section>
      <footer>__PRODUCT_NAME__ — professional demo shell, safe sample data, and approval-gated agent workflows.</footer>
    </div></main>
  </div>
</body>
</html>
"""


def render_dashboard(profile: dict[str, Any] | None = None) -> str:
    profile = profile or _default_profile()
    brand = profile["brand"]
    rules = profile.get("business_rules", {})
    compliance = profile.get("compliance", {})

    replacements = {
        "__PRODUCT_NAME__": escape(brand.get("product_name", "Agent AI Plug Realtor OS")),
        "__CLIENT_NAME__": escape(brand.get("client_display_name", "Sample Realtor")),
        "__BROKERAGE__": escape(brand.get("brokerage_name", "Sample Realty Group")),
        "__MARKET_AREA__": escape(brand.get("market_area", "Your Market")),
        "__TAGLINE__": escape(brand.get("tagline", "Plug-and-play AI systems for real estate agents")),
        "__CRM_NAME__": escape(rules.get("crm_name", "Sample CRM")),
        "__PRIMARY_GOAL__": escape(rules.get("primary_goal", "prioritize leads, draft follow-up, and create a daily approval queue")),
        "__DISCLAIMER__": escape(compliance.get("disclaimer", "Drafting and workflow support only. Human review required.")),
        "__AGENT_CARDS__": "\n".join(render_agent_card(agent) for agent in agent_cards()),
    }

    html = HTML_TEMPLATE
    for key, value in replacements.items():
        html = html.replace(key, value)
    return html


def write_dashboard(profile: dict[str, Any] | None = None) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "dashboard.html").write_text(render_dashboard(profile), encoding="utf-8")


if __name__ == "__main__":
    write_dashboard()
    print("Dashboard generated in output/dashboard.html")
