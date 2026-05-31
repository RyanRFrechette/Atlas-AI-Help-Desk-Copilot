"""Deterministic placeholder triage — keyword matching, no AI."""
from __future__ import annotations
import json
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent.parent / "data"

PRIORITY_KEYWORDS: dict[str, list[str]] = {
    "urgent": [
        "locked out", "password reset", "cannot login", "urgent", "asap", "presentation",
        "breach", "malware", "virus", "phishing", "ransomware", "hacked",
    ],
    "high": [
        "vpn", "crash", "crashes", "cannot connect", "not working", "email down",
        "cannot access", "completely down",
    ],
    "medium": [
        "access", "printer", "offline", "overheating", "laggy", "slow",
        "no access", "not receiving", "delayed", "pixelated",
    ],
    "low": ["notification", "request", "upgrade", "question", "inquiry"],
}

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "network": [
        "vpn", "network", "internet", "wifi", "wi-fi", "ethernet",
        "bandwidth", "connection", "latency", "teams video", "pixelated", "choppy",
    ],
    "email": ["outlook", "email", "mail", "exchange", "calendar", "mailbox"],
    "access": [
        "password", "locked", "access", "drive", "permission", "login",
        "account", "reset", "credentials", "authentication",
    ],
    "hardware": [
        "printer", "laptop", "computer", "monitor", "keyboard", "overheating",
        "mouse", "screen", "battery", "hardware", "device", "fan",
    ],
    "software": [
        "slack", "teams", "app", "application", "install", "crash",
        "update", "notification", "software", "plugin",
    ],
}

SECURITY_KEYWORDS = [
    "breach", "malware", "virus", "phishing", "ransomware",
    "unauthorized", "hacked", "suspicious", "data leak", "credentials stolen",
]

_RESPONSE_TEMPLATES: dict[str, str] = {
    "network": (
        "Thank you for contacting IT Support. I've reviewed your network connectivity issue.\n\n"
        "Our team will investigate shortly. In the meantime, please try:\n"
        "  • Restarting your network adapter (Device Manager > Network Adapters > Disable/Enable)\n"
        "  • Connecting via wired Ethernet if currently on Wi-Fi\n"
        "  • Running a speed test at fast.com and noting the result\n\n"
        "We'll follow up within 2 business hours.\n\nReference: {ticket_id}"
    ),
    "email": (
        "Thank you for reporting this email issue. I've opened a support case for you.\n\n"
        "While we investigate, please try launching Outlook in safe mode:\n"
        "Hold Ctrl while clicking the Outlook icon, then select 'Yes' when prompted.\n\n"
        "If the issue persists in safe mode, please let us know and we'll escalate.\n"
        "Expected response time: 4 business hours.\n\nReference: {ticket_id}"
    ),
    "access": (
        "Thank you for your access request. I've logged this as a priority ticket.\n\n"
        "For urgent lockouts, call the IT helpline immediately at ext. 4357 (HELP).\n"
        "For access requests, your manager will receive an approval request within 30 minutes.\n\n"
        "Reference: {ticket_id}"
    ),
    "hardware": (
        "Thank you for reporting your hardware issue. A support ticket has been created.\n\n"
        "Our hardware team will assess the situation. If the device is unusable, you may request\n"
        "a loaner unit through the IT portal. An engineer will contact you to schedule an on-site\n"
        "visit within 1 business day.\n\nReference: {ticket_id}"
    ),
    "software": (
        "Thank you for contacting IT Support about your software issue.\n\n"
        "Please try the following steps first:\n"
        "  • Sign out of the application completely and sign back in\n"
        "  • Check for pending application updates\n"
        "  • Clear the application cache (steps vary by application)\n\n"
        "If the issue continues, reply to this message and we'll escalate.\n\nReference: {ticket_id}"
    ),
}

_TECHNICIAN_NOTES: dict[str, str] = {
    "network": (
        "- Verify DHCP lease and DNS resolution on affected machine\n"
        "- Check switch port status and VLAN assignment in network management\n"
        "- Review firewall logs for blocked connections to target IP\n"
        "- Confirm VPN client version matches current policy (check IT portal)\n"
        "- Ping trace: gateway → internal DNS → external. Identify failure point"
    ),
    "email": (
        "- Check Exchange / M365 service health dashboard first (admin.microsoft.com)\n"
        "- Review Outlook add-ins: File > Options > Add-ins — disable all, re-enable one by one\n"
        "- Run scanpst.exe against user .pst/.ost if profile corruption suspected\n"
        "- Verify mailbox size quota and auto-archive settings in EAC\n"
        "- Confirm account license assignment in M365 admin center"
    ),
    "access": (
        "- Verify user AD account: enabled, not expired, not locked (ADUC or Get-ADUser)\n"
        "- Check group membership — confirm target resource/share groups assigned\n"
        "- Review AD event logs: Event ID 4740 (lockout), 4625 (failed login)\n"
        "- For shared drives: confirm DFS namespace reachable, share + NTFS permissions\n"
        "- Repeated lockouts: check all devices for stale saved credentials"
    ),
    "hardware": (
        "- Log device serial number and pull warranty status from vendor portal\n"
        "- Overheating: clean vents with compressed air; check thermal paste age (replace if 3+ yrs)\n"
        "- Printers: verify IP via LCD > Network Settings; update IP in print server if changed\n"
        "- Run built-in diagnostics (Dell SupportAssist / HP PC Hardware Diagnostics)\n"
        "- Document findings in asset management system before any hardware swap"
    ),
    "software": (
        "- Check application event log (Event Viewer > Windows Logs > Application) for crash codes\n"
        "- Verify software version is on approved/supported versions list\n"
        "- Test in fresh Windows user profile to rule out profile corruption\n"
        "- Review recent Windows Updates — check if rollback to previous resolves issue\n"
        "- For mobile: check OS version against application compatibility matrix"
    ),
}

_RESOLUTION_TEMPLATE = """\
## Resolution Record — {ticket_id}

**Category:** {category}
**Suggested Priority:** {priority}
**Resolved by:** [Technician Name]
**Resolution Date:** [YYYY-MM-DD]
**Time to Resolution:** [HH:MM]

### Root Cause
[Describe the root cause identified]

### Steps Taken
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Resolution
[Describe how the issue was resolved and confirmed fixed]

### Preventive Action
[Any changes made to prevent recurrence — or "None required"]

### Time Spent
[HH:MM]
"""


def _count_matches(text: str, keyword_map: dict[str, list[str]]) -> dict[str, int]:
    lowered = text.lower()
    return {label: sum(1 for kw in kws if kw in lowered) for label, kws in keyword_map.items()}


def _best_match(counts: dict[str, int], fallback: str) -> tuple[str, int]:
    best = max(counts, key=lambda k: counts[k])
    return (best, counts[best]) if counts[best] > 0 else (fallback, 0)


def _confidence(match_count: int) -> str:
    if match_count >= 3:
        return "high"
    if match_count >= 1:
        return "medium"
    return "low"


def _load_kb() -> list[dict]:
    with open(_DATA_DIR / "knowledge_base.json", encoding="utf-8") as f:
        return json.load(f)


def find_kb_matches(category: str) -> list[dict]:
    return [entry for entry in _load_kb() if entry.get("category") == category]


def triage_ticket(ticket: dict) -> dict:
    combined = f"{ticket.get('subject', '')} {ticket.get('description', '')}"
    lowered = combined.lower()

    priority_counts = _count_matches(combined, PRIORITY_KEYWORDS)
    category_counts = _count_matches(combined, CATEGORY_KEYWORDS)

    priority, p_hits = _best_match(priority_counts, "low")
    category, c_hits = _best_match(category_counts, "software")

    is_security = any(kw in lowered for kw in SECURITY_KEYWORDS)
    escalate = priority == "urgent" or is_security

    ticket_id = ticket.get("id", "TKT-???")

    return {
        "ticket_id": ticket_id,
        "suggested_priority": priority,
        "suggested_category": category,
        "confidence": _confidence(p_hits + c_hits),
        "escalation_recommended": escalate,
        "escalation_reason": (
            "Security-related keywords detected." if is_security
            else "Ticket classified as urgent priority." if priority == "urgent"
            else None
        ),
        "kb_matches": find_kb_matches(category),
        "response_draft": _RESPONSE_TEMPLATES.get(category, "").format(ticket_id=ticket_id),
        "technician_notes": _TECHNICIAN_NOTES.get(category, ""),
        "resolution_template": _RESOLUTION_TEMPLATE.format(
            ticket_id=ticket_id,
            category=category,
            priority=priority,
        ),
    }
