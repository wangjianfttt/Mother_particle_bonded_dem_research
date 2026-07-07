#!/usr/bin/env python3
"""Check the repaired full manuscript against its source-data map."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/repaired_full_submission_draft.md"
SOURCE_MATRIX = ROOT / "manuscript/repaired_full_manuscript_source_data_matrix.csv"


FORBIDDEN_READER_TERMS = [
    r"\bseed[0-9]+\b",
    r"\bPB-00[0-9]\b",
    r"\bSP-002\b",
    r"\bCAL1\b",
    r"\brunning\b",
    r"\bunfinished\b",
    r"progress figure",
    r"open marker",
    r"artificial intelligence",
    r"\bAI\b",
]


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def fail(message: str) -> None:
    print(f"FAIL repaired manuscript consistency: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not MANUSCRIPT.exists():
        fail(f"missing manuscript {MANUSCRIPT.relative_to(ROOT)}")
    if not SOURCE_MATRIX.exists():
        fail(f"missing source matrix {SOURCE_MATRIX.relative_to(ROOT)}")

    text = MANUSCRIPT.read_text(encoding="utf-8")

    figure_refs = set(re.findall(r"Fig\.\s*([1-6])", text))
    figure_captions = set(re.findall(r"\*\*Fig\.\s*([1-6])", text))
    table_refs = set(re.findall(r"Table\s*([1-4])", text))
    table_captions = set(re.findall(r"\*\*Table\s*([1-4])", text))
    if figure_refs != {str(i) for i in range(1, 7)}:
        fail(f"unexpected figure references {sorted(figure_refs)}")
    if figure_captions != {str(i) for i in range(1, 7)}:
        fail(f"unexpected figure captions {sorted(figure_captions)}")
    if table_refs != {str(i) for i in range(1, 5)}:
        fail(f"unexpected table references {sorted(table_refs)}")
    if table_captions != {str(i) for i in range(1, 5)}:
        fail(f"unexpected table captions {sorted(table_captions)}")

    missing_figures = []
    for rel in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
        if not (ROOT / rel).exists():
            missing_figures.append(rel)
    if missing_figures:
        fail("missing figure files: " + ", ".join(missing_figures))

    offenders = []
    for pattern in FORBIDDEN_READER_TERMS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            offenders.append(pattern)
    if offenders:
        fail("reader-facing forbidden terms: " + ", ".join(offenders))

    rows = list(csv.DictReader(SOURCE_MATRIX.open(encoding="utf-8")))
    expected_items = {f"Fig. {i}" for i in range(1, 7)} | {f"Table {i}" for i in range(1, 5)}
    found_items = {row["display_item"] for row in rows}
    if found_items != expected_items:
        fail(f"source matrix items mismatch: {sorted(found_items)}")

    missing_paths: list[str] = []
    for row in rows:
        for field in ("output_files", "source_data", "regeneration_or_check_script"):
            for rel in split_paths(row[field]):
                if not (ROOT / rel).exists():
                    missing_paths.append(f"{row['display_item']}:{field}:{rel}")
    if missing_paths:
        fail("missing source-matrix paths: " + "; ".join(missing_paths))

    if "https://doi.org/10.5281/zenodo.20687351" not in text:
        fail("missing Zenodo DOI")
    if "This work was supported by the Anhui Provincial Natural Science Foundation" not in text:
        fail("missing preserved acknowledgements")

    print(
        "PASS repaired manuscript consistency: "
        f"{len(rows)} display rows, {len(figure_refs)} figures, {len(table_refs)} tables"
    )


if __name__ == "__main__":
    main()
