from src.atlas.triage import triage_ticket, find_kb_matches

REQUIRED_FIELDS = {
    "ticket_id", "suggested_priority", "suggested_category", "confidence",
    "escalation_recommended", "escalation_reason", "kb_matches",
    "response_draft", "technician_notes", "resolution_template",
}
VALID_PRIORITIES = {"urgent", "high", "medium", "low"}
VALID_CONFIDENCES = {"high", "medium", "low"}


def test_triage_returns_all_fields():
    result = triage_ticket({"id": "T0", "subject": "VPN down", "description": "Cannot connect"})
    missing = REQUIRED_FIELDS - result.keys()
    assert not missing, f"Missing fields: {missing}"


def test_triage_priority_values_valid():
    result = triage_ticket({"id": "T1", "subject": "Outlook crash", "description": "App crashes"})
    assert result["suggested_priority"] in VALID_PRIORITIES


def test_triage_confidence_values_valid():
    result = triage_ticket({"id": "T2", "subject": "VPN crash urgent", "description": "Cannot connect vpn not working"})
    assert result["confidence"] in VALID_CONFIDENCES


def test_escalation_on_security_keyword():
    ticket = {"id": "T3", "subject": "Suspicious link", "description": "I clicked a phishing email link"}
    result = triage_ticket(ticket)
    assert result["escalation_recommended"] is True
    assert result["escalation_reason"] is not None


def test_escalation_on_urgent_priority():
    ticket = {"id": "T4", "subject": "Locked out urgent ASAP", "description": "Cannot login presentation in 30 min"}
    result = triage_ticket(ticket)
    assert result["escalation_recommended"] is True


def test_no_escalation_low_priority():
    ticket = {"id": "T5", "subject": "Notification question", "description": "How do I change notification settings?"}
    result = triage_ticket(ticket)
    assert result["escalation_recommended"] is False


def test_kb_matches_returns_correct_category():
    matches = find_kb_matches("network")
    assert len(matches) >= 1
    assert all(m["category"] == "network" for m in matches)


def test_kb_matches_empty_for_unknown_category():
    assert find_kb_matches("unknown_xyz") == []


def test_response_draft_contains_ticket_id():
    result = triage_ticket({"id": "TKT-999", "subject": "printer offline", "description": "floor 3 printer down"})
    assert "TKT-999" in result["response_draft"]


def test_resolution_template_contains_ticket_id():
    result = triage_ticket({"id": "TKT-888", "subject": "vpn not working", "description": "cannot connect to vpn"})
    assert "TKT-888" in result["resolution_template"]


def test_triage_handles_missing_fields_gracefully():
    result = triage_ticket({})
    assert result["ticket_id"] == "TKT-???"
    assert result["suggested_priority"] in VALID_PRIORITIES
