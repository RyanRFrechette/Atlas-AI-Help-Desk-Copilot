# Atlas — Limitations

This document is intentionally direct about what Atlas does not do. These limitations are by design for a portfolio project; they are documented here so evaluators can assess the scope honestly.

---

## Demo Data Only

Atlas uses 8 hand-written tickets and 8 KB articles stored in JSON files.

- There is no connection to any live ticket system (ServiceNow, Jira, Freshdesk, etc.)
- There are no real users, real accounts, or real organizational data
- All names, departments, email addresses, ticket IDs, and timestamps are fictional
- The dataset is not representative of a real queue's distribution, volume, or edge-case diversity

---

## No Live System Integration

Atlas does not connect to:

- Active Directory or Microsoft Entra ID (no live account lookup)
- Microsoft 365 or Exchange Online (no live mailbox or tenant status)
- Any VPN management console
- Any printer or device management system
- Any external threat intelligence feed

Commands shown in KB articles and technician notes (e.g., `Get-ADUser`, `Revoke-MgUserSignInSession`) are informational — Atlas does not execute them.

---

## Deterministic, Keyword-Based Triage

The triage engine uses keyword matching and hard-coded rules. This means:

- Classification accuracy depends on keywords appearing in the subject or description
- Ambiguous tickets (e.g., "I can't log in" with no other context) may be mis-classified
- The same ticket phrased differently can produce a different category
- Confidence scores are a rough heuristic (3-point scale), not a calibrated model
- There is no learning or feedback loop — the rules do not improve over time

All triage outputs are **suggestions**, not decisions. A technician must review every output before taking action.

---

## No Authentication or Access Control

- Any user who can reach the app can view all demo tickets and triage output
- There are no user roles, no audit logging, and no session management
- This is appropriate for a local demo tool; it is not appropriate for production use

---

## Not a Replacement for Policy or Judgment

Atlas does not know:

- Your organization's SLAs, escalation thresholds, or staffing policies
- Whether a specific user is a VIP, contractor, or high-risk account
- The current threat landscape or active incidents
- Whether a KB article applies to a specific system version or configuration

The security escalation logic catches common patterns (phishing keywords, repeated unknown lockouts), but it will miss novel attacks and context that only a trained analyst would recognize.

---

## Scope Intentionally Excluded

The following were deliberately excluded to keep the MVP focused:

- Email or chat integration (no ticket ingest from Outlook, Teams, or email)
- Ticket history or recurrence detection
- Attachment parsing or screenshot analysis
- Multi-language support
- Mobile-responsive layout
- Accessibility compliance (WCAG)

---

## Summary

| Claim | Accurate? |
|---|---|
| Demonstrates IT help desk triage workflow | ✓ Yes |
| Uses real ticket system data | ✗ No — demo data only |
| Triage is always correct | ✗ No — keyword-based, review required |
| Connects to live systems | ✗ No — fully offline |
| Ready for production deployment | ✗ No — portfolio proof-of-concept |
| Shows understanding of IT support domain | ✓ Yes |
| Shows Python/Streamlit development skills | ✓ Yes |
| Tests cover triage and data logic | ✓ Yes — 32 tests passing |
