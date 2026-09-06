"""
PDF parsing & preprocessing.

Real extraction is performed with PyMuPDF (fitz) for text/metadata and
pdfplumber (best-effort, wrapped in try/except) for table detection.
Everything downstream (the seven AI agents) consumes the ExtractedContent
produced here, so the "AI analysis" is grounded in the paper's real content
even while agent scoring itself runs in demo/mock mode.
"""
from __future__ import annotations

import io
import re
from typing import List

import fitz  # PyMuPDF

from schemas import ExtractedContent, ParsingChecklistItem, AgentStatus

try:
    import pdfplumber
    _HAS_PDFPLUMBER = True
except Exception:  # pragma: no cover - optional dependency
    _HAS_PDFPLUMBER = False


KNOWN_SECTIONS = [
    "abstract", "introduction", "related work", "literature review",
    "background", "methodology", "method", "materials and methods",
    "experiments", "experimental setup", "results", "evaluation",
    "discussion", "limitations", "conclusion", "conclusions",
    "acknowledgments", "acknowledgements", "references",
]

DOMAIN_KEYWORDS = {
    "Artificial Intelligence / Machine Learning": [
        "machine learning", "neural network", "deep learning", "model", "training",
        "dataset", "algorithm", "artificial intelligence", "reinforcement learning",
        "multi-agent", "prediction", "classification", "accuracy", "gradient",
    ],
    "Natural Language Processing": [
        "natural language", "nlp", "language model", "text classification",
        "sentiment", "tokeniz", "transformer", "embedding", "corpus",
    ],
    "Computer Vision": [
        "computer vision", "image classification", "object detection",
        "convolutional", "segmentation", "cnn", "image recognition",
    ],
    "Networking / Systems": [
        "network protocol", "distributed system", "latency", "throughput",
        "bandwidth", "cloud computing", "edge computing", "server",
    ],
    "Bioinformatics / Healthcare": [
        "genomic", "clinical", "patient", "biomedical", "healthcare",
        "diagnosis", "disease", "medical imaging",
    ],
    "Robotics": [
        "robot", "actuator", "manipulator", "autonomous navigation", "sensor fusion",
    ],
    "Security": [
        "security", "encryption", "vulnerability", "attack", "authentication",
        "intrusion detection", "cryptograph",
    ],
    "Environmental / Sustainability": [
        "carbon emission", "sustainability", "climate", "renewable energy",
        "environmental", "greenhouse gas",
    ],
}


def _extract_text_per_page(doc: "fitz.Document") -> List[str]:
    return [page.get_text("text") or "" for page in doc]


def _guess_title_authors(doc: "fitz.Document", full_text: str):
    meta_title = (doc.metadata or {}).get("title") or ""
    meta_author = (doc.metadata or {}).get("author") or ""

    title = meta_title.strip()
    authors: List[str] = []

    if not title:
        # Fall back to the largest font-size span on page 1.
        try:
            page = doc[0]
            spans = []
            for block in page.get_text("dict").get("blocks", []):
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text = span.get("text", "").strip()
                        if text:
                            spans.append((span.get("size", 0), text))
            if spans:
                spans.sort(key=lambda s: -s[0])
                title = spans[0][1]
        except Exception:
            pass

    if not title:
        for line in full_text.splitlines():
            if line.strip():
                title = line.strip()
                break

    if meta_author:
        authors = [a.strip() for a in re.split(r",| and ", meta_author) if a.strip()]
    else:
        # Heuristic: the first non-empty line after the title that looks like a
        # name list (short, comma separated, no terminal punctuation).
        lines = [l.strip() for l in full_text.splitlines() if l.strip()]
        try:
            idx = lines.index(title.strip())
        except ValueError:
            idx = 0
        for candidate in lines[idx + 1: idx + 4]:
            if len(candidate) < 120 and ("," in candidate or " and " in candidate) and not candidate.endswith("."):
                authors = [a.strip() for a in re.split(r",| and ", candidate) if a.strip()]
                break

    return title.strip() or "Untitled Paper", authors


def _extract_abstract(full_text: str) -> str:
    match = re.search(
        r"(?im)^\s*abstract\s*[:\-]?\s*$(.*?)(?=^\s*(1\.?\s*)?introduction\b|^\s*keywords\b)",
        full_text,
        re.DOTALL,
    )
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()[:800]
    return ""


def _find_sections(full_text: str) -> List[str]:
    found = []
    for section in KNOWN_SECTIONS:
        pattern = rf"(?im)^\s*(\d+\.?\s*)?{re.escape(section)}\s*$"
        if re.search(pattern, full_text):
            found.append(section.title())
    return found


def _count_pattern_numbers(full_text: str, keyword: str) -> int:
    numbers = set(re.findall(rf"(?i)\b{keyword}\s+(\d+)", full_text))
    return len(numbers)


def _count_equations(full_text: str) -> int:
    # Numbered equation lines, e.g. "E = mc^2         (1)"
    return len(re.findall(r"\(\s*\d{1,2}\s*\)\s*$", full_text, re.MULTILINE))


def _count_references(full_text: str) -> int:
    match = re.search(r"(?im)^\s*references?\s*$", full_text)
    tail = full_text[match.start():] if match else full_text
    numbered = re.findall(r"(?m)^\s*\[\d+\]", tail)
    if numbered:
        return len(set(numbered))
    dotted = re.findall(r"(?m)^\s*\d{1,3}\.\s+[A-Z]", tail)
    if dotted:
        return len(dotted)
    return len(re.findall(r"et al\.", full_text))


def _count_tables(full_text: str, doc: "fitz.Document") -> int:
    caption_count = _count_pattern_numbers(full_text, "table")
    plumber_count = 0
    if _HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(io.BytesIO(doc.tobytes())) as pdf:
                for page in pdf.pages:
                    plumber_count += len(page.extract_tables() or [])
        except Exception:
            plumber_count = 0
    return max(caption_count, plumber_count)


def _count_figures(full_text: str, doc: "fitz.Document") -> int:
    caption_count = _count_pattern_numbers(full_text, "fig(?:ure)?\\.?")
    image_count = 0
    try:
        for page in doc:
            image_count += len(page.get_images(full=True))
    except Exception:
        pass
    return max(caption_count, image_count)


def _guess_domain_keywords(title: str, abstract: str, full_text: str) -> List[str]:
    haystack = f"{title} {abstract} {full_text[:4000]}".lower()
    matched_domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in haystack)
        if hits > 0:
            matched_domains.append((domain, hits))
    matched_domains.sort(key=lambda d: -d[1])
    return [d for d, _ in matched_domains]


def parse_pdf(file_bytes: bytes):
    """Extract structural + content statistics from a PDF file's raw bytes.

    Returns (ExtractedContent, full_text). `full_text` is kept out of the
    public schema (it can be large) but is used internally by the Language /
    Citation / Technical agents for real regex-based analysis.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    try:
        pages_text = _extract_text_per_page(doc)
        full_text = "\n".join(pages_text)
        title, authors = _guess_title_authors(doc, full_text)
        abstract = _extract_abstract(full_text)

        content = ExtractedContent(
            page_count=doc.page_count,
            word_count=len(full_text.split()),
            figure_count=_count_figures(full_text, doc),
            table_count=_count_tables(full_text, doc),
            equation_count=_count_equations(full_text),
            reference_count=_count_references(full_text),
            title=title,
            authors=authors,
            abstract=abstract or " ".join(full_text.split())[:400],
            sections_found=_find_sections(full_text),
            domain_keywords=_guess_domain_keywords(title, abstract, full_text),
        )
        return content, full_text
    finally:
        doc.close()


def default_parsing_checklist() -> List[ParsingChecklistItem]:
    return [
        ParsingChecklistItem(key="text", label="Text Extraction", status=AgentStatus.PENDING),
        ParsingChecklistItem(key="figures", label="Figures Detection", status=AgentStatus.PENDING),
        ParsingChecklistItem(key="tables", label="Tables Detection", status=AgentStatus.PENDING),
        ParsingChecklistItem(key="equations", label="Equations Detection", status=AgentStatus.PENDING),
        ParsingChecklistItem(key="references", label="References Extraction", status=AgentStatus.PENDING),
        ParsingChecklistItem(key="metadata", label="Metadata Extraction", status=AgentStatus.PENDING),
    ]
