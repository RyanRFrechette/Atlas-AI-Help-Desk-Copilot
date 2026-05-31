import json
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_sample_tickets() -> list[dict]:
    with open(_DATA_DIR / "sample_tickets.json", encoding="utf-8") as f:
        return json.load(f)


def load_knowledge_base() -> list[dict]:
    with open(_DATA_DIR / "knowledge_base.json", encoding="utf-8") as f:
        return json.load(f)
