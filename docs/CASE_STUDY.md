# Atlas AI Help Desk Copilot — Case Study

## Problem

Help desk agents handling a high-volume ticket queue spend a disproportionate amount of time on intake: reading each ticket, determining urgency, locating relevant KB articles, and composing an initial response. For Tier 1 agents — especially new staff — this cognitive load slows first response time and increases the risk of mis-prioritised tickets slipping through.

The specific pain points this project targets:

- Password resets and account lockouts dominate queues but have known resolution paths
- Security incidents (phishing, credential compromise) require fast, specific escalation — not general intake
- Technicians lose time switching between the ticket system and the KB
- Inconsistent first-response emails reduce user confidence in the help desk

---

## Goal

Build a working Streamlit proof-of-concept that demonstrates automated triage for a remote IT help desk — classifying incoming tickets, surfacing matching KB articles, generating a response draft, and flagging escalation candidates — without requiring live infrastructure, external APIs, or AI model calls.

The project doubles as a portfolio piece demonstrating IT support domain knowledge alongside practical Python development.

---

## What Atlas Does

1. **Classifies tickets** by category (access, hardware, network, email, security) and priority using keyword matching against subject and description fields
2. **Detects security risk** — phishing keywords and credential-compromise phrases override the standard category and auto-escalate regardless of submitted priority
3. **Matches KB articles** by category and symptom keywords, ranked by relevance
4. **Generates a troubleshooting checklist** from matched KB steps — ready to follow immediately
5. **Drafts a customer response** tailored to category and priority, with a mandatory technician-review warning
6. **Produces internal technician notes** with specific commands, event log IDs, and vendor tips
7. **Creates a resolution documentation template** pre-filled with ticket metadata

---

## Workflow Demonstrated

```
Ticket submitted
      ↓
Atlas classifies (category → priority → risk → escalation check)
      ↓
KB articles matched and ranked
      ↓
Checklist, response draft, tech notes, resolution template generated
      ↓
Technician reviews, edits, and acts
```

The workflow deliberately stops short of autonomous action. Atlas assists intake; the technician owns the resolution.

---

## Build Process

The project was built in five phases following a strict phase-gate discipline:

| Phase | Deliverable |
|---|---|
| 0 | Scaffold, CLAUDE.md rules, three review-gate agents |
| 1 | Demo data (8 tickets, 8 KB articles) with loader functions and 11 data tests |
| 2 | Deterministic triage engine with 17 triage tests |
| 3 | Streamlit MVP with 4 module integrity tests |
| 4 | Realism polish — priority correction, KB accuracy fixes, UI wording |
| 5 | Portfolio documentation |

Each phase was committed separately to show a clean, intentional development history.

**Tools used:** Python 3.12, Streamlit, pytest, PowerShell, Git, Claude Code (AI-assisted development with phase-gated agents as review gates)

---

## Key Technical Decisions

**Deterministic triage over LLM calls:** Using keyword maps and multi-word phrase matching keeps the tool fast, testable, and explainable — critical properties for a tool that informs escalation decisions. An LLM could produce better classifications but would introduce cost, latency, API dependency, and non-determinism.

**Security keywords always override:** Phishing and credential-compromise terms override the submitted category field. This prevents a mis-categorised security incident from being routed as a routine access request.

**Multi-word escalation phrases:** Escalation triggers use multi-word phrases ("locked three times", "did not attempt", "unknown location") rather than single keywords. This avoids false positives from common words appearing in routine tickets.

**JSON demo data:** Portable, version-controlled, and inspectable. No database migration, no seed scripts, no connection strings.

---

## Realism Decisions

The demo data and KB content were written to pass scrutiny from a working IT professional:

- Ticket descriptions use realistic urgency framing ("client proposal due at noon", "presentation in one hour")
- KB steps reference real tools: ADUC, Entra ID sign-in logs, Event ID 4740, GlobalProtect logs, OST file paths, `gpupdate /force`
- The phishing KB article follows actual Tier 1 containment procedure (collect headers, use PAB, check message trace, escalate if clicked)
- Password reset steps include identity verification before resetting — a real security control
- The session-revocation step uses the current Microsoft Graph cmdlet (`Revoke-MgUserSignInSession`) rather than the deprecated AzureAD module

---

## Limitations

- No live ticket system integration
- Keyword matching will misclassify ambiguous tickets
- Demo data is small (8 tickets) — not representative of real queue distribution
- Triage confidence scores are a rough heuristic, not a calibrated model

See [LIMITATIONS.md](LIMITATIONS.md) for full details.

---

## What I Learned

- Writing realistic demo data is harder than writing the triage logic — it requires genuine domain knowledge to make tickets and KB articles credible
- Phase-gating a small project creates overhead upfront but makes each component independently testable and reviewable
- Security tickets need special handling at the category-detection level, not just the escalation level, to prevent silent mis-routing
- The gap between "working" and "polished" is mostly wording, priority calibration, and KB accuracy — not code

---

## Future Improvements

- **Real integrations:** ServiceNow or Jira Service Management ingest via API
- **Feedback loop:** Technicians confirm or correct triage output; corrections improve keyword weights
- **Role-based views:** Tier 1 sees checklist and response draft; Tier 2 sees tech notes and AD commands
- **Trend reporting:** Weekly category/priority distribution and escalation rate
- **Entra ID lookup:** Live account status (locked, last login, MFA enrolled) pulled at triage time
