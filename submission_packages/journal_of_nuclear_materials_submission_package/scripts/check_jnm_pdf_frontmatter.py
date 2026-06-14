#!/usr/bin/env python3
"""Verify that the compiled JNM PDF exposes the expected frontmatter text."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "manuscript/journal_of_nuclear_materials_submission.pdf"


EXPECTED_TEXT = [
    "Acceptance-gated bonded-template DEM reveals localized fracture sequences",
    "Li4SiO4 ceramic breeder beds",
    "Jian Wang",
    "Siyu Wang",
    "Hang Zhang",
    "Ming-Zhun Lei",
    "Wei Wen",
    "Qi-Gang Wu",
    "Gang Shen",
    "Haishun Deng",
    "Anhui University of Science and Technology",
    "Institute of Plasma Physics",
    "Abstract",
    "Keywords",
    "lithium orthosilicate",
    "ceramic breeder material",
    "fracture-event sequence",
]

BODY_EXPECTED_TEXT = [
    "Data availability",
    "Declaration of competing interest",
]


def normalized_pdf_text() -> str:
    reader = PdfReader(str(PDF))
    raw_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text = re.sub(r"\s+", " ", raw_text)
    text = text.replace("Li 4SiO4", "Li4SiO4")
    text = text.replace("Li4SiO 4", "Li4SiO4")
    return text


def main() -> int:
    text = normalized_pdf_text()
    missing = [item for item in EXPECTED_TEXT + BODY_EXPECTED_TEXT if item not in text]
    if missing:
        print("FAIL pdf frontmatter: missing expected PDF text: " + "; ".join(missing))
        return 1
    if not re.search(r"Jian Wang[a-z,∗*]*, Siyu Wang", text):
        print("FAIL pdf frontmatter: author order could not be verified near Jian/Siyu")
        return 1
    print(
        "PASS pdf frontmatter: title, 8 authors, affiliations, abstract, keywords "
        "and declarations/data-availability text verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
