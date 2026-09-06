"""FastAPI entrypoint for the AI-Based Research Paper Review System backend.

Run (from the backend/ directory, with the venv active):

    uvicorn main:app --reload --port 8000 --workers 1

NOTE: must run as a single worker/process — paper state lives in an
in-memory store (spec section 17), so multiple workers would each see a
different, incomplete copy of it.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.papers import router as papers_router
from data.seed import seed_demo_data

app = FastAPI(
    title="AI-Based Research Paper Review System",
    description=(
        "AI-assisted pre-review and editorial screening layer for research papers. "
        "This system does not replace human peer reviewers — final publication and "
        "peer-review decisions are made by qualified human reviewers/editors."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prototype only — tighten for any real deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(papers_router)


@app.on_event("startup")
async def _startup():
    seed_demo_data()


@app.get("/")
async def root():
    return {
        "name": "AI-Based Research Paper Review System API",
        "status": "ok",
        "docs": "/docs",
        "notice": "AI-assisted screening: results assist editors and reviewers and should be "
                   "independently verified by qualified human reviewers.",
    }
