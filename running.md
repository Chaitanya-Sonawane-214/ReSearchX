# Running & Feature Verification Guide

This is the detailed companion to [setup.md](setup.md): how to start the app, and —
page by page, feature by feature — how to check that each part actually works.
Use it to rehearse before a demo, or to sanity-check the app after pulling new
changes.

## Starting the app

```bash
# Terminal 1 — backend (from backend/, venv activated — see setup.md)
python -m uvicorn main:app --reload --port 8000 --workers 1

# Terminal 2 — frontend (from frontend/)
npm run dev
```

- Backend: `http://127.0.0.1:8000` — interactive API docs at `http://127.0.0.1:8000/docs`
- Frontend: `http://localhost:5173`

**Every backend restart wipes state back to the seeded demo data** (7 papers at
different stages, including one untouched "hero" paper ready to run through the
full pipeline live). There's no database — this is intentional (see the main
`README.md`). If a demo run leaves things messy, just restart the backend.

`--workers 1` is required — paper state lives in memory in a single process.

---

## Quick smoke test (2 minutes, no clicking)

Before doing anything in the browser, confirm the backend itself is healthy:

```bash
curl http://127.0.0.1:8000/api/dashboard/stats
```

Expect JSON like `{"total_papers":7,"ai_reviews_completed":6,...}`. If this
fails, fix the backend first — nothing in the UI will work without it.

---

## Feature-by-feature checklist

### 1. Dashboard (`/`)

- **What it shows:** total papers, AI reviews completed, revision required,
  ready for review, similarity alerts, under human review — plus a recent
  papers table and a pipeline distribution bar.
- **How to check:** numbers should match `curl http://127.0.0.1:8000/api/dashboard/stats`.
  Recent Papers table should list 7 papers on a fresh restart. Clicking any row
  navigates to that paper's detail page.
- **AI Engine pill** (top right): should read "AI Engine: Demo Mode" unless you
  set `ANTHROPIC_API_KEY` (see setup.md §6).

### 2. Papers (`/papers`)

- Filter chips along the top (All / Ready for Analysis / Ready for Review /
  Revision Required / …) — click one and confirm the table only shows papers
  in that status.
- Search box — type part of a title or author name, confirm the table narrows.
- Every row is clickable → paper detail page.

### 3. Upload Paper (`/upload`)

- **Drag-and-drop:** drag a PDF onto the dashed box — it should highlight on
  drag-over and show the file name + size once dropped.
- **Browse button:** click "Browse PDF" → native file picker → pick a `.pdf`.
- **Invalid file:** try dragging/selecting a non-PDF (e.g. a `.txt` or `.docx`)
  — you should get an inline red error: *"Invalid File. Please upload a PDF
  research paper."* — and the upload should NOT proceed.
- **Target Venue field:** optional. Leave it blank and continue — the Scope
  Matching Agent should later fall back to a generic domain classification
  (visible in its findings) instead of blocking anything.
- Click **Upload Paper** → a confirmation card appears with the paper's title/
  size and a **Start AI Review** button.
- Click **Start AI Review** → you're taken to the Analysis Pipeline page for
  that paper.

### 4. Analysis Pipeline (`/papers/:id/pipeline`)

This is the core "wow" page — it's polling the backend live, not a canned
animation.

- **Stepper at top:** Paper Uploaded → PDF Parsed → AI Review → Report
  Generated → Editorial Screening → … — steps should light up green with a
  checkmark as each stage completes, and the current one shows a spinner.
- **PDF Parsing & Preprocessing card:** six checklist rows (Text Extraction,
  Figures Detection, Tables Detection, Equations Detection, References
  Extraction, Metadata Extraction) should tick off one by one within ~2
  seconds, each showing a real count on the right (e.g. "2 figures", "20
  references") — these are **real extracted numbers** from the uploaded PDF,
  not placeholders. Try it with two different PDFs and confirm the numbers
  differ.
- **Multi-Agent Review Layer:** all 7 agent cards go pending → running
  (spinning icon, blue ring) → completed (colored icon + score) over a few
  seconds, finishing at slightly different times (this is real async work, not
  a fixed timer).
- **Each completed agent card is clickable** → opens a dialog with that
  agent's strengths, issues (with severity badges), and recommendations.
- Once all 7 finish, a brief "Report Aggregation Agent running…" card appears,
  then a final card shows the **overall score** and **editorial headline**
  (READY FOR REVIEW / REVISION REQUIRED / NOT RECOMMENDED) with a **View Full
  Report** button.
- **To verify it's not hard-coded:** upload the same PDF twice — scores should
  be identical (deterministic per file). Upload a very short/sparse PDF vs. a
  full one — scores and flagged issues should visibly differ.

### 5. Multi-Agent Review (`/papers/:id/agents`)

- Same 7 agent cards as the pipeline page, viewable any time after analysis
  completes, without re-running anything.
- Click a card → detail dialog (see above).

### 6. Unified Review Report (`/papers/:id/report`)

- Big score ring + editorial decision headline at the top.
- **Agent Scores chart** (bar chart) — bars colored green/amber/red by score
  tier; hovering a bar shows an exact score tooltip.
- Strengths / Major Concerns / Minor Concerns lists.
- **Priority Issues table** — sorted with Critical/High first.
- **Download Review Report** button → downloads a `.txt` file summarizing the
  whole report (open it — check it has the paper title, scores, and issues).
- If the decision is **Revision Required** or **Not Recommended**:
  - **Resubmit Revised Paper** button appears → opens a dialog → you can
    optionally attach a new PDF, or leave blank to resubmit the same file.
    Confirm it creates a *new* paper entry (check the Papers list — revision
    number increments) with an **improved** score on re-analysis.
- If the decision is **Ready for Review**:
  - **Continue to Similarity Detection** button appears → takes you to the
    similarity page.

### 7. Similarity Analysis (`/papers/:id/similarity`)

- If no check has run yet: a **Run Similarity Analysis** button. Click it —
  after ~1.5s a result appears.
- **Acceptable case** (≤30% similarity): green banner, "ACCEPTABLE SIMILARITY",
  a **Continue to Reviewer Assignment** button.
- **High similarity case** (>30%): red banner, "HIGH SIMILARITY DETECTED",
  a sources table (title, matched excerpt, % similarity), and an **Editor
  Decision** panel with two real actions:
  - **Return to Author for Revision** → paper flips to Revision Required.
  - **Editor Override — Proceed to Reviewer Assignment** → paper proceeds
    despite the flag (demonstrates "editor retains control").
- To see the high-similarity path without waiting on randomness, open the
  already-seeded paper `Federated Learning for Privacy-Preserving Healthcare
  Analytics` from the Papers list (status "High Similarity Flagged").

### 8. Reviewer Assignment (`/papers/:id/reviewers`)

- A grid of AI-suggested reviewer cards: expertise tags, match %, workload
  badge, COI badge, publication count.
- **View Profile** → dialog with bio, expertise match %, recommendation score,
  full expertise list, COI status.
- **Assign Reviewer** → button shows a spinner, then a toast notification
  ("Reviewer assigned…") and the page switches to an assigned-state card with
  a **View Paper Lifecycle** link. Paper status becomes "Human Review
  Pending."

### 9. Paper Details (`/papers/:id`)

- Full vertical lifecycle stepper (Uploaded → Parsed → AI Review → Report →
  Editorial Screening → Similarity → Reviewer Assigned → Human Review).
- Score ring + metadata panel (file name/size, upload date, target venue,
  revision number).
- **Jump to Stage** buttons — disabled (grayed out) for stages not yet
  reached, enabled once available; confirm the disabled state matches reality
  (e.g. "Reviewer Assignment" stays disabled until a similarity check exists).
- If a reviewer is assigned: a **Human Peer Review** mini flow-diagram appears
  at the bottom with "Status: Review Pending" — this is deliberately the final
  stage; the prototype does not simulate an actual human reviewer's decision.

### 10. Sidebar list pages

- **AI Analysis** (`/analysis`) — papers currently mid-pipeline (uploaded /
  parsing / analyzing / aggregating / failed). Empty right after a fresh
  restart except the one seeded "Ready for Analysis" paper.
- **Review Reports** (`/reports`) — every paper that has completed AI
  analysis, regardless of what happened after.
- **Similarity** (`/similarity`) — every paper that has run a similarity
  check.
- **Reviewers** (`/reviewers`) — the full static reviewer directory (8
  reviewers), independent of any specific paper. Search box filters by name/
  expertise.

### 11. Settings (`/settings`)

- Shows current AI engine mode (Demo/Live), the similarity threshold (30%),
  and the responsible-AI notice. Should reflect `ANTHROPIC_API_KEY` state
  accurately if you toggle it and restart the backend.

### 12. Error handling

- **Invalid file on upload** — covered above (§3).
- **Analysis Failed / Retry:** hard to trigger organically (the pipeline has a
  fallback for AI failures), but the pipeline page is built to show a red
  "Analysis Failed" card with a **Retry Analysis** button if `paper.status`
  ever becomes `analysis_failed` — you can force this by stopping the backend
  mid-analysis and restarting it, then hitting the paper's pipeline page.

---

## Verifying the backend directly (optional, for the technically curious)

Every UI action maps to one REST call. You can drive the whole pipeline with
`curl` alone, without the frontend at all — useful for isolating whether a bug
is frontend or backend:

```bash
# 1. Upload
curl -s -X POST http://127.0.0.1:8000/api/papers/upload \
  -F "file=@backend/data/sample_paper.pdf" \
  -F "target_venue=International Conference on Artificial Intelligence"
# → note the returned "id", e.g. paper-0009

# 2. Start analysis
curl -s -X POST http://127.0.0.1:8000/api/papers/paper-0009/analyze

# 3. Poll status until it's no longer parsing/analyzing/aggregating
curl -s http://127.0.0.1:8000/api/papers/paper-0009 | python -m json.tool

# 4. Unified report
curl -s http://127.0.0.1:8000/api/papers/paper-0009/report

# 5. Similarity check
curl -s -X POST http://127.0.0.1:8000/api/papers/paper-0009/similarity

# 6. Recommended reviewers
curl -s http://127.0.0.1:8000/api/papers/paper-0009/reviewers

# 7. Assign one (use an id from step 6's response)
curl -s -X POST http://127.0.0.1:8000/api/papers/paper-0009/assign-reviewer \
  -H "Content-Type: application/json" -d '{"reviewer_id":"rev-ananya-sharma"}'
```

Or just open `http://127.0.0.1:8000/docs` — FastAPI's auto-generated Swagger
UI lets you fire any endpoint from the browser with a "Try it out" button.

---

## Resetting for a fresh demo

Stop the backend (Ctrl+C) and start it again — all state (including anything
you uploaded/assigned/resubmitted during rehearsal) resets to the pristine
seed data, and the hero paper goes back to "Ready for Analysis."
