import time
from src.atlas.triage import triage_ticket
from src.atlas.demo_data import load_sample_tickets

REQUIRED_FIELDS = {
    "ticket_id", "issue_category", "priority", "confidence", "risk_level",
    "escalation_recommended", "escalation_reason", "matching_kb_articles",
    "troubleshooting_checklist", "customer_response_draft", "technician_notes",
    "resolution_documentation_template",
}
VALID_PRIORITIES = {"urgent", "high", "medium", "low"}
VALID_CONFIDENCES = {"high", "medium", "low"}
VALID_RISK_LEVELS = {"critical", "high", "medium", "low"}
VALID_CATEGORIES = {"access", "hardware", "network", "email", "security"}


def _t(id="T0", subject="", description="", **kwargs):
    return {"id": id, "subject": subject, "description": description, **kwargs}


def test_triage_returns_all_required_fields():
    result = triage_ticket(_t("T0", "VPN not working", "Cannot connect to VPN"))
    missing = REQUIRED_FIELDS - result.keys()
    assert not missing, f"Missing fields: {missing}"


def test_password_reset_no_escalation():
    ticket = _t("T1", "Password reset request", "Forgot my password, please reset it.",
                category="access", priority="medium")
    result = triage_ticket(ticket)
    assert result["escalation_recommended"] is False
    assert result["escalation_reason"] is None


def test_unknown_lockouts_require_escalation():
    ticket = _t(
        "T2",
        "Account locked — multiple failed logins from unknown location",
        "My account has been locked three times today. I did not attempt those logins.",
        category="access", priority="high",
    )
    result = triage_ticket(ticket)
    assert result["escalation_recommended"] is True
    assert result["escalation_reason"] is not None


def test_phishing_requires_escalation_and_security_category():
    ticket = _t(
        "T3",
        "Suspicious phishing email received",
        "Got email with fake portal link asking for credentials. Did not click.",
        category="security", priority="urgent",
    )
    result = triage_ticket(ticket)
    assert result["escalation_recommended"] is True
    assert result["issue_category"] == "security"
    assert result["risk_level"] == "critical"


def test_vpn_matches_network_kb():
    ticket = _t("T4", "VPN keeps dropping", "VPN disconnects every 30 minutes.",
                category="network", priority="high")
    result = triage_ticket(ticket)
    assert result["issue_category"] == "network"
    assert any(a["category"] == "network" for a in result["matching_kb_articles"])


def test_outlook_matches_email_kb():
    ticket = _t("T5", "Outlook not syncing", "Outlook inbox stopped syncing. OWA works fine.",
                category="email", priority="medium")
    result = triage_ticket(ticket)
    assert result["issue_category"] == "email"
    assert any(a["category"] == "email" for a in result["matching_kb_articles"])


def test_shared_drive_matches_access_kb():
    ticket = _t("T6", "No access to shared drive", "Cannot access the Legal shared drive after transfer.",
                category="access", priority="medium")
    result = triage_ticket(ticket)
    assert result["issue_category"] == "access"
    assert any(a["category"] == "access" for a in result["matching_kb_articles"])


def test_confidence_is_valid():
    result = triage_ticket(_t("T7", "VPN issue", "Cannot connect", category="network", priority="high"))
    assert result["confidence"] in VALID_CONFIDENCES


def test_risk_level_is_valid():
    result = triage_ticket(_t("T8", "Printer offline", "HP printer shows offline",
                              category="hardware", priority="medium"))
    assert result["risk_level"] in VALID_RISK_LEVELS


def test_priority_is_valid():
    result = triage_ticket(_t("T9", "Slow laptop", "Very slow after update"))
    assert result["priority"] in VALID_PRIORITIES


def test_missing_fields_handled_gracefully():
    result = triage_ticket({})
    assert result["ticket_id"] == "TKT-UNKNOWN"
    assert result["priority"] in VALID_PRIORITIES
    assert result["escalation_recommended"] in (True, False)
    assert isinstance(result["matching_kb_articles"], list)
    assert isinstance(result["troubleshooting_checklist"], list)


def test_no_external_api_behavior():
    start = time.perf_counter()
    triage_ticket(_t("T10", "Test ticket", "Test description"))
    assert time.perf_counter() - start < 1.0, "Triage too slow — possible external I/O"


def test_security_keyword_overrides_category():
    ticket = _t("T11", "Fake login page link in email",
                "Got email with phishing link to fake portal.", category="access", priority="medium")
    result = triage_ticket(ticket)
    assert result["issue_category"] == "security"


def test_resolution_template_contains_ticket_id():
    result = triage_ticket(_t("TKT-XYZ", "Test", "Test description"))
    assert "TKT-XYZ" in result["resolution_documentation_template"]


def test_customer_response_draft_contains_ticket_id():
    result = triage_ticket(_t("TKT-ABC", "VPN issue", "Cannot connect",
                              category="network", priority="high"))
    assert "TKT-ABC" in result["customer_response_draft"]


def test_checklist_is_list_of_strings():
    result = triage_ticket(_t("T12", "VPN drops", "VPN disconnects", category="network", priority="high"))
    assert isinstance(result["troubleshooting_checklist"], list)
    assert all(isinstance(s, str) for s in result["troubleshooting_checklist"])


def test_all_sample_tickets_triage_successfully():
    for ticket in load_sample_tickets():
        result = triage_ticket(ticket)
        missing = REQUIRED_FIELDS - result.keys()
        assert not missing, f"{ticket['id']} missing fields: {missing}"
