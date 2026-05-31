# Atlas Demo Script — 60–90 Seconds

Use this script for a live demo, screen share, or recorded walkthrough. The phishing ticket (TKT-007) is the primary example — it shows the most distinctive behaviour: security override, critical risk, and escalation logic.

---

## Before You Start

1. `streamlit run app.py` — app running at `http://localhost:8501`
2. Browser window open, full screen or maximised
3. Scroll to top of page

---

## Script

### Opening (5–10 seconds)

> "This is Atlas, a triage assistant I built for IT help desk teams.
> It classifies incoming tickets, surfaces KB articles, and generates response drafts
> — so agents spend less time on intake."

*Point to the dashboard metrics row.*

> "The dashboard gives you an immediate queue snapshot — total tickets, how many are high or urgent,
> how many are escalation candidates, and how many are security-related."

---

### Phishing Ticket — Main Demo (30–40 seconds)

*Select **TKT-007** from the dropdown.*

> "I'll use the phishing ticket — this is the most important scenario for any help desk.
> A user received a credential-harvesting email, recognised it as fake, and filed the ticket."

*Click **Analyze Ticket**.*

> "Atlas detects the phishing keywords, overrides the category to Security, and flags it as Critical.
> The escalation banner fires immediately with a specific reason."

*Scroll to the KB Articles section.*

> "The first KB checklist step is: confirm whether the user clicked or entered credentials.
> If yes — stop Tier 1 and escalate. That ordering is intentional."

*Scroll to the Response Draft.*

> "The customer-facing draft confirms the report, praises the user for not clicking,
> and includes the IT hotline. It includes a review warning — Atlas never sends anything on its own."

*Scroll to Technician Notes.*

> "The internal notes reference the Credential Compromise playbook, the specific PowerShell cmdlet
> to revoke active sessions, and the one-hour incident report deadline."

---

### Custom Ticket — Optional (15–20 seconds)

*Clear the custom ticket fields or type a new subject.*

> "You can also type any ticket subject and description to see how Atlas classifies it.
> I'll try a VPN issue..."

*Type: Subject: "VPN keeps dropping", Description: "Disconnects every 30 minutes, home internet is fine."*

*Click **Analyze Ticket**.*

> "It classifies as Network, High priority, matches the GlobalProtect KB article,
> and generates a checklist starting with the client version check."

---

### Closing (5–10 seconds)

> "The triage is fully deterministic — no API calls, no AI, completely explainable.
> All outputs are suggestions that a technician reviews before acting.
> The project has 32 passing tests and runs locally with no external dependencies."

---

## Key Points to Emphasise

- **Security override is automatic** — phishing keywords override submitted category
- **Escalation is specific** — reason text, not just a flag
- **KB step ordering matters** — credential check is step 1 in the phishing playbook
- **Review warning appears everywhere** — Atlas does not act, it assists
- **No live systems** — safe to demo anywhere, no credentials or real data

---

## Automated Recording Mode

**URL:** `http://localhost:8501?demo=video`

**Launch (PowerShell from repo root):**
```powershell
.\scripts\Start-AtlasDemoRecording.ps1
```

Or manually: `streamlit run app.py` then open `http://localhost:8501?demo=video`

### What it shows (no clicks required)

Pre-analyzed TKT-007 phishing ticket, full page top to bottom:

1. Demo banner + project purpose
2. Dashboard metrics
3. Phishing ticket summary
4. Triage result cards (Category · Priority · Confidence · Risk)
5. Escalation banner
6. Matching KB article (expanded)
7. Troubleshooting checklist
8. Customer response draft
9. Technician notes
10. Resolution documentation template
11. Disclaimer footer

### 60–90 second narration outline

| Time | Section | Narration focus |
|---|---|---|
| 0–10s | Banner + dashboard | Introduce Atlas, queue metrics |
| 10–20s | Ticket summary | Describe phishing scenario |
| 20–35s | Triage cards + escalation | Security override, Critical risk, why escalation fires |
| 35–50s | KB article + checklist | Step ordering — credential check is step 1 |
| 50–65s | Response draft | Review-before-send warning, customer tone |
| 65–80s | Tech notes + resolution template | Cmdlets, playbook reference, documentation discipline |
| 80–90s | Footer | Deterministic, no AI, technician review required |

---

## Anticipated Questions

**"Is this using ChatGPT or an AI model?"**
No. All triage is deterministic keyword matching. This is intentional — it keeps outputs explainable and the tool fast and testable.

**"How would this connect to a real ticket system?"**
The demo uses JSON files, but the loader functions (`load_sample_tickets`, `load_knowledge_base`) could be swapped for API calls to ServiceNow, Jira Service Management, or Freshdesk with minimal changes to the rest of the application.

**"What would you add to make this production-ready?"**
Live AD/Entra ID lookup for account status, a feedback loop where technicians confirm or correct triage outputs to improve keyword weights, and role-based views separating Tier 1 from security team outputs.
