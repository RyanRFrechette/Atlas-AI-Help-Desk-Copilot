# Local Setup — Atlas AI Help Desk Copilot

PowerShell-first setup guide for Windows. All commands tested on Windows 11 with Python 3.12.

---

## Prerequisites

| Requirement | Version | Check |
|---|---|---|
| Python | 3.10 or later | `python --version` |
| pip | bundled with Python | `pip --version` |
| Git | any | `git --version` |

---

## 1. Clone the Repository

```powershell
git clone https://github.com/RyanRFrechette/Atlas-AI-Help-Desk-Copilot.git
cd Atlas-AI-Help-Desk-Copilot
```

---

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

---

## 3. Activate the Virtual Environment

```powershell
.venv\Scripts\Activate.ps1
```

If you see a script execution policy error:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then retry the activate command.

---

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `streamlit` — web UI
- `pytest` — test runner

No API keys or environment variables are required.

---

## 5. Run the App

```powershell
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

If the browser does not open, navigate there manually.

---

## 6. Run Tests

```powershell
python -m pytest --tb=short -q
```

Expected output: **32 passed**

---

## 7. Verify All Modules Compile

```powershell
python -m py_compile app.py src/atlas/demo_data.py src/atlas/triage.py src/atlas/__init__.py
```

No output = all files valid.

---

## Deactivate the Virtual Environment

When done:

```powershell
deactivate
```

---

## Troubleshooting

**`streamlit` not found after install:**
Make sure the virtual environment is activated (you should see `(.venv)` in your prompt before running commands).

**`ModuleNotFoundError: No module named 'src'`:**
Run `streamlit run app.py` and `pytest` from the project root directory, not from inside `src/` or `tests/`.

**Port 8501 already in use:**
```powershell
streamlit run app.py --server.port 8502
```

**Streamlit opens but shows an error:**
Run the compile check to confirm all source files are valid:
```powershell
python -m py_compile app.py src/atlas/demo_data.py src/atlas/triage.py
```
