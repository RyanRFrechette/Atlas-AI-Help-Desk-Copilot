"""Deterministic placeholder triage — keyword matching, no AI."""

PRIORITY_KEYWORDS = {
    "urgent": ["locked out", "password reset", "cannot login", "urgent", "asap", "presentation"],
    "high": ["vpn", "crash", "crashes", "cannot connect", "not working", "down"],
    "medium": ["access", "printer", "offline", "overheating", "laggy", "slow"],
    "low": ["notification", "request", "upgrade", "question"],
}

CATEGORY_KEYWORDS = {
    "network": ["vpn", "network", "internet", "wifi", "wi-fi", "ethernet", "teams video"],
    "email": ["outlook", "email", "mail", "exchange"],
    "access": ["password", "locked", "access", "drive", "permission", "login"],
    "hardware": ["printer", "laptop", "computer", "monitor", "keyboard", "overheating"],
    "software": ["slack", "teams", "app", "application", "install", "crash"],
}


def _match(text: str, keyword_map: dict[str, list[str]]) -> str:
    lowered = text.lower()
    for label, keywords in keyword_map.items():
        if any(kw in lowered for kw in keywords):
            return label
    return list(keyword_map.keys())[-1]


def triage_ticket(ticket: dict) -> dict:
    """Return triage result with suggested priority and category."""
    combined = f"{ticket.get('subject', '')} {ticket.get('description', '')}"
    return {
        "ticket_id": ticket.get("id"),
        "suggested_priority": _match(combined, PRIORITY_KEYWORDS),
        "suggested_category": _match(combined, CATEGORY_KEYWORDS),
    }
