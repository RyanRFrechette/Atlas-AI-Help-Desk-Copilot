"""Deterministic, rule-based ticket triage — no external AI or API calls."""
from __future__ import annotations
import json
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent.parent / "data"

# ── Keyword maps ──────────────────────────────────────────────────────────────

_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "security": [
        "phishing", "suspicious email", "malware", "virus", "breach", "ransomware",
        "unauthorized", "hacked", "fake portal", "fake login", "suspicious link",
        "credential harvest",
    ],
    "network": [
        "vpn", "network", "internet", "wifi", "wi-fi", "ethernet", "bandwidth",
        "connection", "latency", "disconnect", "drops", "globalprotect",
    ],
    "email": [
        "outlook", "email", "mail", "exchange", "calendar", "mailbox",
        "sync", "syncing", "owa", "not syncing",
    ],
    "access": [
        "password", "locked", "access", "drive", "permission", "login",
        "account", "reset", "authentication", "shared drive", "lockout", "locked out",
    ],
    "hardware": [
        "printer", "laptop", "computer", "monitor", "keyboard", "overheating",
        "mouse", "screen", "battery", "device", "fan", "slow", "boot", "startup",
        "disk", "hard drive", "laserjet",
    ],
}

# Multi-word phrases only — avoids noise from common words
_ESCALATION_PHRASES = [
    "locked multiple times",
    "locked three times",
    "did not attempt",
    "not my login",
    "unknown location",
    "possible compromise",
    "clicked phishing",
    "entered credentials",
    "credentials stolen",
    "unauthorized access",
    "active breach",
    "credential compromise",
]

_VALID_PRIORITIES = {"urgent", "high", "medium", "low"}
_VALID_CATEGORIES = {"access", "hardware", "network", "email", "security"}

_SLA_BY_PRIORITY = {
    "urgent": "30 minutes",
    "high": "2 business hours",
    "medium": "4 business hours",
    "low": "1 business day",
}

# ── Response templates ────────────────────────────────────────────────────────

_RESPONSE_TEMPLATES: dict[str, str] = {
    "access": (
        "Hello {submitter},\n\n"
        "Thank you for contacting IT Support. We have received your request and will prioritise "
        "it accordingly.\n\n"
        "For self-service password resets, visit password.example.com if your MFA is enrolled. "
        "For urgent account lockouts, call the IT helpline at ext. 4357 (HELP).\n\n"
        "We will follow up within {sla}.\n\n"
        "Reference: {ticket_id}\n\n"
        "— IT Support Team\n\n"
        "⚠ This draft requires technician review before sending. Verify all details."
    ),
    "hardware": (
        "Hello {submitter},\n\n"
        "Thank you for reporting your hardware issue. We have logged a support ticket and our "
        "team will investigate shortly.\n\n"
        "If the device is completely unusable, you may request a temporary loaner through the "
        "IT portal. An engineer will be in touch within {sla}.\n\n"
        "Reference: {ticket_id}\n\n"
        "— IT Support Team\n\n"
        "⚠ This draft requires technician review before sending. Verify all details."
    ),
    "network": (
        "Hello {submitter},\n\n"
        "Thank you for reporting your connectivity issue. We have opened a support ticket and "
        "are investigating.\n\n"
        "While we investigate, please try restarting your network adapter and, if possible, "
        "connecting via wired Ethernet. For VPN issues, ensure your client is on the latest "
        "supported version.\n\n"
        "We will follow up within {sla}.\n\n"
        "Reference: {ticket_id}\n\n"
        "— IT Support Team\n\n"
        "⚠ This draft requires technician review before sending. Verify all details."
    ),
    "email": (
        "Hello {submitter},\n\n"
        "Thank you for contacting IT Support about your email issue. We have created a support "
        "ticket and our team is investigating.\n\n"
        "In the meantime, please check if you can access email via Outlook Web App (OWA) at "
        "mail.example.com to confirm whether the issue is specific to the desktop client.\n\n"
        "We will follow up within {sla}.\n\n"
        "Reference: {ticket_id}\n\n"
        "— IT Support Team\n\n"
        "⚠ This draft requires technician review before sending. Verify all details."
    ),
    "security": (
        "Hello {submitter},\n\n"
        "Thank you for reporting this security concern. This has been escalated to the security "
        "team as an urgent priority. You did the right thing by reporting this immediately.\n\n"
        "Our security team will contact you directly within 30 minutes.\n\n"
        "IMPORTANT: Do NOT forward the suspicious email to colleagues. If you clicked any link "
        "or entered credentials, call the IT hotline immediately: ext. 4357 (HELP).\n\n"
        "Reference: {ticket_id}\n\n"
        "— IT Security Team\n\n"
        "⚠ This draft requires technician review before sending. Verify all details."
    ),
}

_RESOLUTION_TEMPLATE = """\
## Resolution Record — {ticket_id}

**Category:** {category}
**Priority:** {priority}
**Risk Level:** {risk_level}
**Escalated:** {escalated}
**Technician:** [Name]
**Resolution Date:** [YYYY-MM-DD]
**Time to Resolve:** [HH:MM]

### Root Cause
[Describe the root cause identified]

### Steps Taken
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Resolution
[Describe how the issue was resolved and confirmed fixed]

### Preventive Action
[Changes made to prevent recurrence, or "None required"]

### Time Spent
[HH:MM]
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_kb() -> list[dict]:
    with open(_DATA_DIR / "knowledge_base.json", encoding="utf-8") as f:
        return json.load(f)


def _text(ticket: dict) -> str:
    return f"{ticket.get('subject', '')} {ticket.get('description', '')}".lower()


def _detect_category(ticket: dict) -> str:
    text = _text(ticket)
    # Security always overrides — cannot miss a phishing/breach ticket
    if any(kw in text for kw in _CATEGORY_KEYWORDS["security"]):
        return "security"
    existing = ticket.get("category", "")
    if existing in _VALID_CATEGORIES:
        return existing
    # Keyword fallback
    scores = {cat: sum(1 for kw in kws if kw in text) for cat, kws in _CATEGORY_KEYWORDS.items()}
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "access"


def _detect_priority(ticket: dict, category: str) -> str:
    if category == "security":
        return "urgent"
    existing = ticket.get("priority", "")
    return existing if existing in _VALID_PRIORITIES else "medium"


def _detect_escalation(ticket: dict, category: str, priority: str) -> tuple[bool, str | None]:
    text = _text(ticket)
    if category == "security":
        return True, "Security/phishing ticket — requires immediate Tier 2 security team response."
    if priority == "urgent":
        return True, "Ticket classified as urgent priority — requires immediate attention."
    if any(phrase in text for phrase in _ESCALATION_PHRASES):
        return True, "Possible credential compromise or unauthorised account activity — escalate to security team."
    return False, None


def _risk_level(category: str, priority: str, escalate: bool) -> str:
    if category == "security":
        return "critical"
    if escalate or priority == "urgent":
        return "high"
    if priority == "high":
        return "medium"
    return "low"


def _match_kb(category: str, ticket_text: str) -> list[dict]:
    kb = _load_kb()
    scored = []
    for entry in kb:
        if entry.get("category") != category:
            continue
        hits = 0
        for symptom in entry.get("symptoms", []):
            long_words = [w for w in symptom.lower().split() if len(w) >= 4]
            if long_words and any(w in ticket_text for w in long_words):
                hits += 1
        scored.append((hits, entry))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored]


def _confidence(ticket: dict, kb_matches: list[dict]) -> str:
    score = sum([
        ticket.get("category", "") in _VALID_CATEGORIES,
        ticket.get("priority", "") in _VALID_PRIORITIES,
        len(kb_matches) > 0,
    ])
    if score == 3:
        return "high"
    if score >= 1:
        return "medium"
    return "low"


# ── Public API ────────────────────────────────────────────────────────────────

def triage_ticket(ticket: dict) -> dict:
    ticket_id = ticket.get("id", "TKT-UNKNOWN")
    submitter = ticket.get("submitter", "User")
    text = _text(ticket)

    category = _detect_category(ticket)
    priority = _detect_priority(ticket, category)
    escalate, escalation_reason = _detect_escalation(ticket, category, priority)
    risk = _risk_level(category, priority, escalate)
    kb_matches = _match_kb(category, text)
    confidence = _confidence(ticket, kb_matches)

    checklist = [
        step
        for entry in kb_matches
        for step in entry.get("troubleshooting_steps", [])
    ]

    tech_notes = "\n\n".join(
        f"[{e['id']}] {e['title']}:\n{e['technician_notes']}"
        for e in kb_matches
    )

    template = _RESPONSE_TEMPLATES.get(category, _RESPONSE_TEMPLATES["access"])
    response_draft = template.format(
        submitter=submitter,
        ticket_id=ticket_id,
        sla=_SLA_BY_PRIORITY.get(priority, "4 business hours"),
    )

    resolution_template = _RESOLUTION_TEMPLATE.format(
        ticket_id=ticket_id,
        category=category,
        priority=priority,
        risk_level=risk,
        escalated="Yes" if escalate else "No",
    )

    return {
        "ticket_id": ticket_id,
        "issue_category": category,
        "priority": priority,
        "confidence": confidence,
        "risk_level": risk,
        "escalation_recommended": escalate,
        "escalation_reason": escalation_reason,
        "matching_kb_articles": kb_matches,
        "troubleshooting_checklist": checklist,
        "customer_response_draft": response_draft,
        "technician_notes": tech_notes,
        "resolution_documentation_template": resolution_template,
    }
