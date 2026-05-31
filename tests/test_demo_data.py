from src.atlas.demo_data import load_sample_tickets, load_knowledge_base

REQUIRED_TICKET_FIELDS = {
    "id", "subject", "description", "category", "priority",
    "status", "submitter", "department", "created_at", "expected_escalation",
}
VALID_PRIORITIES = {"urgent", "high", "medium", "low"}
VALID_STATUSES = {"open", "in_progress", "closed"}
VALID_CATEGORIES = {"access", "hardware", "network", "email", "security"}

REQUIRED_KB_FIELDS = {
    "id", "title", "category", "symptoms",
    "troubleshooting_steps", "escalation_triggers", "technician_notes",
}


def test_loaders_return_lists():
    assert isinstance(load_sample_tickets(), list)
    assert isinstance(load_knowledge_base(), list)


def test_exactly_8_tickets():
    assert len(load_sample_tickets()) == 8


def test_required_ticket_fields():
    for t in load_sample_tickets():
        missing = REQUIRED_TICKET_FIELDS - t.keys()
        assert not missing, f"{t.get('id')} missing fields: {missing}"


def test_unique_ticket_ids():
    ids = [t["id"] for t in load_sample_tickets()]
    assert len(ids) == len(set(ids)), "Duplicate ticket IDs"


def test_valid_priorities():
    for t in load_sample_tickets():
        assert t["priority"] in VALID_PRIORITIES, f"{t['id']} bad priority: {t['priority']}"


def test_valid_statuses():
    for t in load_sample_tickets():
        assert t["status"] in VALID_STATUSES, f"{t['id']} bad status: {t['status']}"


def test_valid_categories():
    for t in load_sample_tickets():
        assert t["category"] in VALID_CATEGORIES, f"{t['id']} bad category: {t['category']}"


def test_at_least_one_escalation():
    escalations = [t for t in load_sample_tickets() if t["expected_escalation"] is True]
    assert len(escalations) >= 1, "No tickets flagged for escalation"


def test_at_least_one_security_ticket():
    security = [t for t in load_sample_tickets() if t["category"] == "security"]
    assert len(security) >= 1, "No security/phishing ticket found"


def test_kb_required_fields():
    for entry in load_knowledge_base():
        missing = REQUIRED_KB_FIELDS - entry.keys()
        assert not missing, f"{entry.get('id')} missing KB fields: {missing}"


def test_kb_steps_are_lists():
    for entry in load_knowledge_base():
        assert isinstance(entry["troubleshooting_steps"], list), f"{entry['id']} steps not a list"
        assert len(entry["troubleshooting_steps"]) >= 1, f"{entry['id']} has no steps"
