#!/usr/bin/env python3
"""Check paste-ready Editorial Manager fields against source files."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASTE = ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md"
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
HIGHLIGHTS = ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"
AUTHOR_CSV = ROOT / "manuscript/journal_of_nuclear_materials_author_metadata.csv"


REQUIRED_SECTIONS = [
    "Title",
    "Article type",
    "Authors",
    "Corresponding author",
    "Affiliations",
    "Author-affiliation metadata",
    "Abstract",
    "Keywords",
    "Highlights",
    "Data availability statement",
    "Code availability statement",
    "Declaration of competing interest",
    "Funding declaration",
    "Role of the funding source",
    "Declaration of generative AI and AI-assisted technologies in the writing process",
    "CRediT authorship contribution statement",
    "Repository DOI action",
]


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body").strip() if match else ""


def manuscript_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group("body")).strip()


def bullets(text: str) -> list[str]:
    return [line.removeprefix("-").strip() for line in text.splitlines() if line.strip().startswith("-")]


def main() -> int:
    failures: list[str] = []
    if not PASTE.exists() or PASTE.stat().st_size == 0:
        print(f"FAIL missing paste-field file: {PASTE}")
        return 1

    text = PASTE.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    highlights = HIGHLIGHTS.read_text(encoding="utf-8")
    rows = list(csv.DictReader(AUTHOR_CSV.open(encoding="utf-8")))

    for heading in REQUIRED_SECTIONS:
        body = section(text, heading)
        if not body:
            failures.append(f"missing or empty section: {heading}")

    title = manuscript.splitlines()[0].removeprefix("#").strip()
    if title not in section(text, "Title"):
        failures.append("title does not match manuscript")

    manuscript_abstract = manuscript_section(manuscript, "Abstract")
    paste_abstract = re.sub(r"\s+", " ", section(text, "Abstract")).strip()
    if not manuscript_abstract or manuscript_abstract != paste_abstract:
        failures.append("abstract does not exactly match manuscript abstract")

    source_highlights = bullets(highlights)
    paste_highlights = bullets(section(text, "Highlights"))
    if paste_highlights != source_highlights:
        failures.append("highlights section does not exactly match source highlights")

    author_names = [row["display_name"] for row in rows]
    missing_authors = [name for name in author_names if name not in text]
    if missing_authors:
        failures.append("missing authors: " + ", ".join(missing_authors))
    if "wjfttt@mail.ustc.edu.cn" not in text:
        failures.append("missing corresponding-author email")
    if text.count("affiliation ids") != len(rows):
        failures.append(f"expected {len(rows)} author-affiliation metadata rows")

    internal_pattern = re.compile(r"\b(?:PB-006|PB-007|SP-002|CAL1|seed\d+)\b", re.IGNORECASE)
    internal_hits = sorted(set(internal_pattern.findall(text)))
    if internal_hits:
        failures.append("internal case labels in paste fields: " + ", ".join(internal_hits))

    fake_doi_pattern = re.compile(r"10\.0000/jnm-rehearsal-current|test-jnm-dryrun", re.IGNORECASE)
    if fake_doi_pattern.search(text):
        failures.append("fake rehearsal DOI string found")
    has_pending_repository_action = "Repository DOI or stable URL is still pending" in text
    has_inserted_repository_action = (
        "Repository DOI or stable URL:" in text
        or "Repository identifier inserted" in text
        or "https://doi.org/10." in text
        or "doi:10." in text
    )
    if not (has_pending_repository_action or has_inserted_repository_action):
        failures.append("missing pending or inserted repository DOI action")

    stale_phrases = [
        "Compiler details and build flags should be recorded",
        "template-generation, run-control and post-processing scripts are included",
    ]
    for phrase in stale_phrases:
        if phrase in text:
            failures.append(f"stale paste-field code-availability wording: {phrase}")
    required_code_phrases = [
        "figure-generation",
        "does not redistribute the local DEM executable",
        "manifest provides SHA256 checksums",
    ]
    code_body = section(text, "Code availability statement")
    for phrase in required_code_phrases:
        if phrase not in code_body:
            failures.append(f"missing updated code-availability phrase: {phrase}")

    if failures:
        print("FAIL Editorial Manager paste-field consistency")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS Editorial Manager paste fields: {len(rows)} authors, {len(bullets(highlights))} highlights")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
