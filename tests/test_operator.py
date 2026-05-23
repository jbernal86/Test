from agent_ai_plug.agents import AGENTS
from agent_ai_plug.operator import Lead, build_crm_cleanup, rank_leads


def test_agent_library_has_core_agents():
    names = {agent.name for agent in AGENTS}
    assert "Lead Triage Agent" in names
    assert "Follow-Up Drafting Agent" in names
    assert "Compliance Review Agent" in names
    assert "Daily Operator Agent" in names
    assert len(AGENTS) >= 8


def test_ready_now_lead_scores_above_cold_lead():
    leads = [
        Lead("Hot", "Website", "ready_now", 1, "$300k-$400k", "Pre-approved and asked for help"),
        Lead("Cold", "Old CRM", "cold", 60, "Unknown", "No response"),
    ]
    ranked = rank_leads(leads)
    assert ranked[0]["name"] == "Hot"
    assert ranked[0]["score"] > ranked[1]["score"]
    assert ranked[0]["approval_required"] is True


def test_crm_cleanup_flags_stale_and_missing_price_range():
    leads = [
        Lead("Cold", "Old CRM", "cold", 45, "Unknown", "No response"),
    ]
    cleanup = build_crm_cleanup(leads)
    issues = {item["issue"] for item in cleanup}
    assert "Stale lead" in issues
    assert "Missing price range" in issues
