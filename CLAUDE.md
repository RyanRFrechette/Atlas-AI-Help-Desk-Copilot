# Atlas AI Help Desk Copilot — Project Rules

## Output
- Short responses. No summaries after completing work.
- No multi-paragraph explanations. Code blocks unchanged.

## Shell
- PowerShell-first. Use `pwsh` syntax.
- No bash unless explicitly requested.

## Scope
- One phase at a time. Do not implement future phases.
- No broad directory scans (`Get-ChildItem -Recurse` across full repo is banned).
- No private data. No real credentials, PII, or production connection strings.

## System Safety
- No risky system changes: no global pip installs, no registry edits, no firewall rules.
- No destructive git commands without explicit user confirmation.
- No `git push` without explicit user request.

## Workflow
- Screenshot-proof each feature before marking done.
- Commit only after proof steps pass.
- Commit message: conventional format, subject ≤50 chars.

## Stack Constraints
- UI: Streamlit only (no Flask, FastAPI, or other servers).
- Data: JSON files in `data/`. No live databases, no external APIs.
- Tests: pytest only. No mocks unless integration testing demands it.
- No AI/LLM calls inside the app. All logic is deterministic.

## Agents
- Agents are review gates, not builders.
- Agents do not edit code unless explicitly asked.
- Agents output ≤10 lines per review.
- No broad scans inside agent prompts.

## Phase Gates
- Phase 0: scaffold + CLAUDE.md + agents only.
- Phase 1: demo data, triage logic, Streamlit UI.
- Phase 2: KB search, response drafting, dashboard.
- Phase 3: screenshots, docs, portfolio polish.
- Do not skip gates. Do not merge phases.
