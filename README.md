# Atlas AI Help Desk Copilot

AI-powered triage and knowledge assistant for IT help desk teams.

## Purpose

Atlas reduces ticket resolution time by classifying support tickets, surfacing relevant KB articles, and suggesting next steps — giving agents a head start on every case.

## Stack

- Streamlit (UI)
- JSON demo data (no live systems)
- pytest (tests)

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Tests

```powershell
pytest
```

## Phase Plan

- **Phase 0** — Scaffold, CLAUDE.md, agents (current)
- Phase 1 — Demo data, triage engine, Streamlit UI
- Phase 2 — KB search, response drafting, dashboard
- Phase 3 — Screenshot proof, docs, portfolio polish
