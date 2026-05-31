# Atlas Use Cases — All 8 Demo Scenarios

Each scenario demonstrates a different triage path through Atlas. Together they cover the most common Tier 1 IT support request types for a remote/hybrid workforce.

---

## TKT-001 — Password Reset

**Submitter:** Marcus Webb, Human Resources
**Scenario:** Forgot Windows password over the weekend, account locked after three failed attempts, needs access before a 9 AM meeting.

**How Atlas helps:**
- Classifies as `access / medium`
- Matches KB-001 (Password Reset — Self-Service and Assisted)
- Checklist leads with self-service portal (password.example.com) — no technician involvement needed if MFA is enrolled
- Response draft includes the helpline number for urgent cases
- No escalation — standard lockout with known resolution path

**What this demonstrates:** Atlas correctly handles the most common access ticket without over-escalating a routine request.

---

## TKT-002 — Account Locked from Unknown Location

**Submitter:** Diana Souza, Finance
**Scenario:** Account locked three times in one day; user only logged in once and was in a meeting when the other lockouts occurred.

**How Atlas helps:**
- Classifies as `access / high`
- Detects phrase "locked three times" + "did not attempt" → escalation flag fires
- Matches KB-001 (Password Reset) and KB-002 (Account Lockout Security Investigation)
- Technician notes reference Event ID 4740 (lockout source) and Entra ID sign-in log review
- Escalation reason: "Possible credential compromise or unauthorised account activity"

**What this demonstrates:** Atlas distinguishes a routine lockout from a potential security incident using phrase-level detection, not just a single keyword.

---

## TKT-003 — Slow Computer After Windows Update

**Submitter:** Kevin Park, Engineering
**Scenario:** Dell Latitude 5540 takes 12+ minutes to boot since Tuesday's Windows Update; 100% disk usage visible in Task Manager.

**How Atlas helps:**
- Classifies as `hardware / low`
- Matches KB-003 (Slow Startup — High Disk Usage After Windows Update)
- Checklist: disable startup programs, identify disk-hogging process (TiWorker.exe, MsMpEng.exe), check drive health with CrystalDiskInfo, run `sfc /scannow`
- Technician notes flag KB5034441 (Jan 2024 WinRE update) as a known issue to rule out
- No escalation — performance issue, not a complete outage

**What this demonstrates:** Atlas surfaces a specific known Windows Update issue in the technician notes, saving the tech from guessing.

---

## TKT-004 — Shared Network Printer Offline

**Submitter:** Linda Osei, Marketing
**Scenario:** HP LaserJet Pro M404dn on floor 2 offline since 8 AM; 5 users blocked; client proposal due at noon.

**How Atlas helps:**
- Classifies as `hardware / high` (multiple users + business deadline)
- Matches KB-004 (Network Printer Offline — Diagnosis and Resolution)
- Checklist: check LCD for errors, power-cycle, confirm IP via Network Configuration Page, update print server port if IP changed, ping test
- Technician notes explain HP LaserJet DHCP lease behaviour after power cycle
- Escalation trigger listed: no ping response after power cycle = possible NIC failure

**What this demonstrates:** Atlas correctly classifies a shared-resource outage as high priority and provides the IP/print-server workflow specific to HP network printers.

---

## TKT-005 — VPN Drops Every 20–30 Minutes

**Submitter:** Carlos Rivera, Sales
**Scenario:** Remote worker using GlobalProtect 6.2 on Windows 11; VPN drops every 20–30 minutes, disrupting CRM and SharePoint access; home internet is stable.

**How Atlas helps:**
- Classifies as `network / high`; status is `in_progress`
- Matches KB-005 (VPN Drops Repeatedly — GlobalProtect Stability Issues)
- Checklist: verify client version, ISP ping test, MTU mismatch test, power management fix for Wi-Fi adapter, review PanGPS.log
- Technician notes explain home router session timeout as common root cause, and GlobalProtect keep-alive interval
- No escalation at Tier 1; escalation trigger listed if MTU fix fails or multiple users affected

**What this demonstrates:** Atlas provides vendor-specific (Palo Alto GlobalProtect) troubleshooting steps including the MTU fix — a non-obvious but common remote VPN issue.

---

## TKT-006 — Outlook Inbox Not Syncing

**Submitter:** Sandra Kim, Operations
**Scenario:** Outlook desktop client stopped syncing 18 hours ago; OWA and mobile app work fine; safe mode and restart did not help.

**How Atlas helps:**
- Classifies as `email / medium`
- Matches KB-006 (Outlook Desktop Not Syncing — M365 Exchange Issues)
- Checklist: check M365 service health first (rules out tenant-wide outage), remove/re-add Exchange account, rename OST file to force rebuild, create new Outlook profile, test AutoDiscover
- Technician notes: warn that OST rebuild can take 30–60 minutes on large mailboxes; if tenant-wide, open P2 with Microsoft Support
- No escalation — single-user desktop client issue with known resolution path

**What this demonstrates:** Atlas leads with the M365 service health check — the correct first step before touching the client — and provides the OST rebuild path that resolves most single-user sync failures.

---

## TKT-007 — Suspicious Phishing Email

**Submitter:** Jerome Whitfield, IT Department
**Scenario:** Received email from spoofed IT Support address with a link to `corp-portal-login.net`. User recognised the fake domain, did not click, forwarded headers to security@example.com, and filed this ticket.

**How Atlas helps:**
- Detects "phishing" keyword → security category override (ignores submitted category)
- Classifies as `security / urgent / critical risk`
- Escalation fires immediately: "Security/phishing ticket — requires immediate Tier 2 security team response"
- Matches KB-007 (Phishing Email Response — Reporting and Containment)
- Checklist step 1: **confirm whether user clicked or entered credentials** — if yes, stop Tier 1 and escalate
- Response draft acknowledges the report, praises the user for not clicking, and includes the hotline number
- Technician notes: log in security queue, check VirusTotal/URLhaus for sender domain, initiate Credential Compromise playbook if credentials were entered (`Revoke-MgUserSignInSession`, incident report within 1 hour)

**What this demonstrates:** Atlas models correct security-incident behaviour — the category override ensures phishing is never silently routed as a routine access ticket, and the KB step ordering (credential check first) reflects real Tier 1 containment procedure.

---

## TKT-008 — Shared Drive Missing After Department Transfer

**Submitter:** Priya Anand, Legal
**Scenario:** Transferred from Compliance to Legal three days ago; old P: drive removed (expected), but L: drive not appearing despite manager submitting access request (REQ-2891) on Monday.

**How Atlas helps:**
- Classifies as `access / medium`
- Matches KB-008 (Shared Drive Access Missing After Department Transfer)
- Checklist: verify manager approval in IT portal, check AD group membership (`Get-ADUser` with `-Properties MemberOf`), run `gpupdate /force` if group is correct, manually add AD group if missing, verify DFS namespace reachability
- Technician notes explain the provisioning workflow runs overnight — manual AD group add is acceptable for urgent cases
- No escalation — standard provisioning delay with known workaround

**What this demonstrates:** Atlas surfaces the AD group membership check and provisioning delay explanation that Tier 1 agents often miss, reducing unnecessary escalation to Tier 2.
