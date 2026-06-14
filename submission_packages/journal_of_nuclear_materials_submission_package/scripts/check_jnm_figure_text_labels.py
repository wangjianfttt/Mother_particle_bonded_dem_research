#!/usr/bin/env python3
"""Check active JNM display figures for reader-facing internal labels."""

from __future__ import annotations

import csv
import importlib
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv"
DISPLAY_ITEMS = {"Fig1", "Fig2", "Fig3", "Fig4", "Fig5", "Fig6", "GraphicalAbstract"}
TEXT_SUFFIXES = {".svg"}
PDF_SUFFIXES = {".pdf"}
RASTER_SUFFIXES = {".png", ".tif", ".tiff", ".jpg", ".jpeg"}
INTERNAL_LABEL_PATTERN = re.compile(r"\b(?:PB-006|PB-007|SP-002|CAL1|seed\d+)\b", re.IGNORECASE)


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def extract_pdf_text(path: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if pdftotext is not None:
        result = subprocess.run(
            [pdftotext, str(path), "-"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or f"pdftotext failed for {path}")
        return result.stdout

    try:
        pypdf = importlib.import_module("pypdf")
    except ModuleNotFoundError as exc:
        raise RuntimeError("neither pdftotext nor pypdf is available; cannot audit figure PDF text") from exc
    reader = pypdf.PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_text(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return path.read_text(errors="replace")
    if suffix in PDF_SUFFIXES:
        return extract_pdf_text(path)
    if suffix in RASTER_SUFFIXES:
        return None
    return None


def main() -> int:
    if not MATRIX.exists():
        print(f"FAIL figure text labels: missing {MATRIX}")
        return 1
    rows = list(csv.DictReader(MATRIX.open()))
    errors: list[str] = []
    skipped_raster = 0
    audited = 0

    for row in rows:
        item = (row.get("item") or "").strip()
        if item not in DISPLAY_ITEMS:
            continue
        for rel in split_paths(row.get("output_files", "")):
            path = ROOT / rel
            if not path.exists() or not path.is_file():
                errors.append(f"{item}: missing output file {rel}")
                continue
            try:
                text = extract_text(path)
            except RuntimeError as exc:
                errors.append(f"{item}: {exc}")
                continue
            if text is None:
                skipped_raster += 1
                continue
            audited += 1
            hits = sorted(set(match.group(0) for match in INTERNAL_LABEL_PATTERN.finditer(text)))
            if hits:
                errors.append(f"{item}: internal label(s) in {rel}: {', '.join(hits)}")

    if errors:
        print("FAIL figure text labels")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "PASS figure text labels: "
        f"{audited} text-bearing display files audited; {skipped_raster} raster exports skipped"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
