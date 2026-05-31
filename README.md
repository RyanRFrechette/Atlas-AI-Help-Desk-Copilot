# Atlas AI Help Desk Copilot

AI-powered triage and knowledge assistant for IT help desk teams.

## Purpose

Atlas reduces ticket resolution time by automatically categorizing incoming support tickets, surfacing relevant knowledge base articles, and suggesting next steps — giving agents a head start on every case.

## Planned Features

- Ticket triage: classify by category, urgency, and suggested owner
- Knowledge base search: surface relevant troubleshooting guides per ticket
- Response drafting: generate first-draft replies for common issues
- Dashboard: live queue overview with priority scoring
- Feedback loop: agents confirm/correct suggestions to improve accuracy

## Local Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Running Tests

```bash
pytest
```
