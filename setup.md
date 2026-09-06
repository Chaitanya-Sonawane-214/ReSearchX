# Setup Guide

Everything needed to get **AI Research Review** running on a fresh machine — from
zero to both servers up. If something breaks, jump straight to
[Troubleshooting](#troubleshooting) — the two issues listed there are the ones
people actually hit on Windows.

## 1. Prerequisites

| Tool | Version | Check with |
|---|---|---|
| Python | 3.10 or newer | `python --version` |
| Node.js | 18 or newer | `node --version` |
| npm | comes with Node | `npm --version` |
| Git | any recent | `git --version` |

All commands below assume you're at the **repo root** (the folder containing
`backend/` and `frontend/`) unless a `cd` says otherwise.

## 2. Get the code

```bash
git clone https://github.com/<owner>/ai-research-paper-review.git
cd ai-research-paper-review
```

(Or unzip it, if you received it as a folder instead of a GitHub link.)

## 3. Backend setup (Python / FastAPI)

```bash
cd backend
python -m venv venv
```

Activate the virtual environment — **the command differs by shell**, so match
yours exactly:

| Your shell | Activate with |
|---|---|
| PowerShell | `venv\Scripts\Activate.ps1` |
| Git Bash / WSL / macOS / Linux | `source venv/Scripts/activate` (Windows) or `source venv/bin/activate` (macOS/Linux) |
| cmd.exe | `venv\Scripts\activate.bat` |

You'll know it worked when your prompt gets a `(venv)` prefix. If you don't see
that prefix, the next steps will silently use the wrong Python — see
[Troubleshooting](#troubleshooting).

Then install dependencies:

```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, Pydantic, PyMuPDF (`fitz`), pdfplumber, fpdf2,
and the `anthropic` SDK (only used if you later enable live AI mode).

**Verify it worked:**

```bash
python -c "import fitz, fastapi, pdfplumber, fpdf; print('backend deps OK')"
```

You should see `backend deps OK`. If you get `ModuleNotFoundError`, your venv
isn't actually active — see below.

## 4. Frontend setup (React / Vite)

In a **new terminal window** (leave the backend one alone):

```bash
cd frontend
npm install
```

This pulls in React, TypeScript, Vite, Tailwind v4, React Router, Recharts,
Lucide icons, and TanStack Query. Takes a minute or two on first run.

## 5. Running it

See **[running.md](running.md)** for how to start both servers and a full
checklist of what to click to verify every feature works. Short version:

```bash
# Terminal 1 — backend
cd backend
# (activate venv as above)
python -m uvicorn main:app --reload --port 8000 --workers 1

# Terminal 2 — frontend
cd frontend
npm run dev
```

Then open **http://localhost:5173**.

## 6. Optional: live AI mode

By default the app runs fully offline (no API key, no cost, can't fail during a
demo). To make the 7 agents call the real Claude API instead:

```bash
# before starting uvicorn, in the backend terminal:
export ANTHROPIC_API_KEY="sk-ant-..."       # Git Bash / macOS / Linux
$env:ANTHROPIC_API_KEY = "sk-ant-..."       # PowerShell
```

Then start the backend as usual. The Settings page and the header pill will
show "Live AI" instead of "Demo Mode" once it's picked up. Not required —
skip this section entirely for a normal run.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'fitz'` (or fastapi, pydantic, etc.)

Your venv isn't active, so `python`/`uvicorn` are resolving to some *other*
Python already on your machine's PATH instead of `backend/venv`. Fix:

1. Make sure you `cd`'d into `backend` first (`ls` should show `main.py`).
2. Re-run the activation command **that matches your actual shell** (table
   above) — a PowerShell script (`.ps1`) silently fails as "command not found"
   if typed into Git Bash, and vice versa.
3. Confirm it worked: your prompt should show `(venv)`. Then run
   `python -c "import sys; print(sys.executable)"` — the path it prints should
   be inside `backend\venv\`. If it isn't, activation didn't take.
4. Run the server with `python -m uvicorn ...` (not bare `uvicorn`) — this
   guarantees it uses the same Python you just checked in step 3.

### `[WinError 10013]` or `[WinError 10048]` when starting uvicorn

Something is already bound to port 8000 — usually a previous `uvicorn` process
you forgot to stop (check for a lingering terminal), or another app using that
port. Either close the other process, or run on a different port:

```bash
python -m uvicorn main:app --reload --port 8001 --workers 1
```

(then also set `VITE_API_BASE=http://127.0.0.1:8001/api` for the frontend, or
edit the fallback in `frontend/src/services/api.ts`).

### Frontend loads but shows no data / network errors in the console

The backend isn't running, isn't on port 8000, or CORS is blocked. Check the
backend terminal is still up and visit `http://127.0.0.1:8000/docs` directly —
if that doesn't load, the backend is the problem, not the frontend.

### `npm install` fails or hangs

Delete `frontend/node_modules` and `frontend/package-lock.json` and retry. Make
sure you're on Node 18+ (`node --version`).
