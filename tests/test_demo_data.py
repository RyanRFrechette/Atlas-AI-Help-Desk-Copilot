from src.atlas.demo_data import load_sample_tickets, load_knowledge_base

REQUIRED_TICKET_FIELDS = {"id", "subject", "description", "category", "priority", "status", "submitter"}
VALID_PRIORITIES = {"urgent", "high", "medium", "low"}
VALID_STATUSES = {"open", "closed", "in_progress"}


def test_sample_tickets_count():
    tickets = load_sample_tickets()
    assert len(tickets) == 8


def test_sample_tickets_have_required_fields():
    for ticket in load_sample_tickets():
        missing = REQUIRED_TICKET_FIELDS - ticket.keys()
        assert not missing, f"{ticket['id']} missing fields: {missing}"


def test_sample_tickets_valid_priority():
    for ticket in load_sample_tickets():
        assert ticket["priority"] in VALID_PRIORITIES, f"{ticket['id']} bad priority: {ticket['priority']}"


def test_sample_tickets_valid_status():
    for ticket in load_sample_tickets():
        assert ticket["status"] in VALID_STATUSES, f"{ticket['id']} bad status: {ticket['status']}"


def test_sample_tickets_unique_ids():
    tickets = load_sample_tickets()
    ids = [t["id"] for t in tickets]
    assert len(ids) == len(set(ids)), "Duplicate ticket IDs found"


def test_knowledge_base_loads():
    kb = load_knowledge_base()
    assert len(kb) >= 1
    for entry in kb:
        assert "id" in entry
        assert "steps" in entry
        assert isinstance(entry["steps"], list)
        assert len(entry["steps"]) >= 1
