#!/usr/bin/env python3
"""Check PDF visual-QA artifacts and metadata-warning cleanliness."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QA_DOC = ROOT / "docs/jnm_pdf_visual_qa_20260612.md"
QA_DIR = ROOT / "docs/pdf_visual_qa/jnm_main_20260612"
CONTACT_SHEET = QA_DIR / "contact_sheet.png"
PDF = ROOT / "manuscript/journal_of_nuclear_materials_submission.pdf"
TEX = ROOT / "manuscript/journal_of_nuclear_materials_submission.tex"
SOURCE_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv"
LOGS = [
    ROOT / "manuscript/journal_of_nuclear_materials_submission.log",
    ROOT / "submission_packages/journal_of_nuclear_materials_flat_source/journal_of_nuclear_materials_submission.log",
]


def nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def active_main_figure_pdfs() -> list[Path]:
    figures: list[Path] = []
    with SOURCE_MATRIX.open(newline="") as handle:
        for row in csv.DictReader(handle):
            item = (row.get("item") or "").strip()
            if not re.fullmatch(r"Fig[1-6]", item):
                continue
            for raw_path in (row.get("output_files") or "").split(";"):
                path = raw_path.strip()
                if path.endswith(".pdf"):
                    figures.append(ROOT / path)
    return figures


def main() -> int:
    missing: list[str] = []
    for path in [PDF, TEX, SOURCE_MATRIX, QA_DOC, CONTACT_SHEET]:
        if not nonempty(path):
            missing.append(str(path.relative_to(ROOT)))
    figure_pdfs = active_main_figure_pdfs() if nonempty(SOURCE_MATRIX) else []
    if len(figure_pdfs) != 6:
        missing.append(f"{SOURCE_MATRIX.relative_to(ROOT)}: expected 6 active main-figure PDFs, found {len(figure_pdfs)}")
    for path in figure_pdfs:
        if not nonempty(path):
            missing.append(str(path.relative_to(ROOT)))
    pages = sorted(QA_DIR.glob("page-*.png"))
    if len(pages) < 8:
        missing.append(f"{QA_DIR.relative_to(ROOT)}: expected at least 8 page PNGs, found {len(pages)}")
    for page in pages:
        if not nonempty(page):
            missing.append(str(page.relative_to(ROOT)))
    if missing:
        print("FAIL pdf visual QA: missing or empty artifacts: " + "; ".join(missing))
        return 1

    pdf_mtime = PDF.stat().st_mtime
    stale_inputs = [
        path.relative_to(ROOT).as_posix()
        for path in [TEX, *figure_pdfs]
        if path.stat().st_mtime > pdf_mtime
    ]
    if stale_inputs:
        print("FAIL pdf visual QA: manuscript PDF older than active inputs: " + "; ".join(stale_inputs[:12]))
        return 1

    stale = [path.relative_to(ROOT).as_posix() for path in [CONTACT_SHEET, *pages] if path.stat().st_mtime < pdf_mtime]
    if stale:
        print("FAIL pdf visual QA: rendered artifacts older than manuscript PDF: " + "; ".join(stale[:12]))
        return 1

    bad_patterns = re.compile(
        r"hyperref Warning|Citation.*undefined|undefined citations|LaTeX Error|Emergency stop|Fatal error",
        re.IGNORECASE,
    )
    hits: list[str] = []
    for log in LOGS:
        if not nonempty(log):
            hits.append(f"{log.relative_to(ROOT)} missing")
            continue
        for line_no, line in enumerate(log.read_text(errors="replace").splitlines(), start=1):
            if bad_patterns.search(line):
                hits.append(f"{log.relative_to(ROOT)}:{line_no}:{line.strip()}")
                if len(hits) >= 8:
                    break
    if hits:
        print("FAIL pdf visual QA/log metadata: " + " | ".join(hits))
        return 1

    text = QA_DOC.read_text(errors="replace")
    required_phrases = [
        f"{len(pages)}-page double-column",
        "No obvious figure-caption duplication",
        "manuscript PDF must be newer than the active TeX and Fig. 1-Fig. 6 PDFs",
        "rendered artifacts must be newer than the checked PDF",
        "hyperref",
        "PDF-string warnings",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]
    if missing_phrases:
        print("FAIL pdf visual QA: QA note missing phrases: " + "; ".join(missing_phrases))
        return 1

    print(
        f"PASS pdf visual QA: {len(pages)} rendered pages, "
        f"{len(figure_pdfs)} figure-PDF freshness checks, contact sheet and metadata-warning cleanliness verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
