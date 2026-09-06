# AI-Based Research Paper Review System

A working prototype of an **AI-assisted pre-review and editorial screening platform** for
research papers. It parses an uploaded PDF for real, runs it through seven specialized
review agents, aggregates their findings into a unified report, screens for similarity,
and recommends human reviewers — while making clear throughout that **final publication
and peer-review decisions are made by qualified human reviewers/editors.**

Full product spec: [`to-do.md`](to-do.md). This file is a quick
overview — for step-by-step instructions see:

- **[setup.md](setup.md)** — installing everything from scratch, per-shell
  venv activation, troubleshooting.
- **[running.md](running.md)** — starting both servers, and a detailed,
  page-by-page checklist of how to verify every feature actually works.

## Architecture

```
proj/
├── backend/     FastAPI + PyMuPDF/pdfplumber + fpdf2 (Python)
└── frontend/    React + TypeScript + Vite + Tailwind v4 + Recharts
```

- **Backend** does real PDF text/figure/table/equation/reference/metadata extraction,
  then runs 7 agents (Layout, Structure, Formatting, Language, Citation, Technical,
  Scope Matching) whose scores/findings are computed with deterministic heuristics
  over that real extracted content — so the demo always works offline, for free, and
  every run is grounded in the actual paper rather than fully random. See
  `backend/services/ai_service.py`: if an `ANTHROPIC_API_KEY` environment variable is
  present, each agent instead calls the real Claude API for its findings, with an
  automatic fallback to the offline heuristic if a live call ever fails.
- State is in-memory (no database) and is reseeded with demo data every time the
  backend restarts — see `backend/data/seed.py`.
- **Frontend** polls the backend while a paper is mid-pipeline so you see each stage
  (PDF parsing checklist, all 7 agents, aggregation) animate in live.

## Quick start (Windows / PowerShell)

### 1. Backend

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000 --workers 1
```

Leave this running. It serves the API at `http://127.0.0.1:8000` (interactive docs at
`/docs`). **Must stay at `--workers 1`** — paper state lives in memory in a single
process, so extra workers would each see a different, incomplete copy of it.

### 2. Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL it prints (`http://localhost:5173`).

That's it — no API keys, no database setup required. The dashboard comes preloaded
with a real sample paper plus several other demo papers at different pipeline stages
so it doesn't look empty on first run.

## Demo script

1. **Dashboard** — shows the editorial overview: total papers, reviews completed,
   revision-required, ready-for-review, similarity alerts, under human review.
2. **Papers → "AI-Driven Carbon Emission Prediction..."** (status *Ready for Analysis*)
   — click in, then **Start AI Review**.
3. Watch the **Analysis Pipeline** page live: PDF parsing checklist fills in, all 7
   agent cards go pending → running → completed with real scores, then the Report
   Aggregation Agent runs, and an editorial decision (Ready for Review / Revision
   Required / Not Recommended) appears.
4. **View Full Report** — overall score, per-agent chart, strengths, major/minor
   concerns, priority issues, recommended actions. If revision is required, the
   report offers **Resubmit Revised Paper** (simulates an improved revision) and
   **Download Review Report**.
5. If ready for review, **Continue to Similarity Detection** — runs a similarity
   check; acceptable similarity continues straight to reviewer assignment, high
   similarity shows an alert with an editor override decision.
6. **Reviewer Assignment** — AI-suggested human reviewers ranked by expertise match,
   workload and conflict-of-interest, with a **View Profile** dialog. Assigning one
   moves the paper into **Human Peer Review — Review Pending**, the final stage that
   stays outside the AI's control.
7. **Paper Details** shows the complete lifecycle stepper end to end.

Other papers already seeded at different stages (Papers page) are there to make the
Dashboard, Review Reports, Similarity and Reviewer Assignment list pages feel like a
populated, real platform without you having to run the whole pipeline manually first.

## Enabling live Claude-generated findings (optional)

By default everything runs in **Demo/Mock AI mode** — no API key needed, and it's the
recommended mode for a live presentation (zero cost, no network dependency, no rate
limits). To switch every agent to real Claude-generated findings instead:

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
uvicorn main:app --reload --port 8000 --workers 1
```

The Settings page and the header pill reflect which mode is active. If a live call
ever fails mid-demo, that one agent silently falls back to its offline heuristic
rather than breaking the pipeline.

## Notes

- No authentication/database — intentional, per the prototype's scope (see spec
  section 28: this demonstrates the architecture and UX, not a production platform).
- Restarting the backend resets all state back to the seeded demo data
