import py_compile
from pathlib import Path


def test_app_compiles():
    py_compile.compile("app.py", doraise=True)


def test_atlas_modules_compile():
    for path in Path("src/atlas").glob("*.py"):
        py_compile.compile(str(path), doraise=True)


def test_demo_data_module_importable():
    from src.atlas.demo_data import load_sample_tickets, load_knowledge_base
    assert callable(load_sample_tickets)
    assert callable(load_knowledge_base)


def test_triage_module_importable():
    from src.atlas.triage import triage_ticket
    assert callable(triage_ticket)
