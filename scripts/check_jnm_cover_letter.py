#!/usr/bin/env python3
"""Check the JNM cover letter and Highlights support files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COVER = ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md"
HIGHLIGHTS = ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"
TITLE = "Acceptance-gated bonded-template DEM reveals localized fracture sequences in Li4SiO4 ceramic breeder beds"


def main() -> int:
    errors: list[str] = []
    if not COVER.exists():
        print(f"FAIL cover letter: missing {COVER}")
        return 1
    if not HIGHLIGHTS.exists():
        print(f"FAIL cover letter: missing {HIGHLIGHTS}")
        return 1

    cover = COVER.read_text()
    highlights = HIGHLIGHTS.read_text()
    required_cover_phrases = [
        TITLE,
        "Journal of Nuclear Materials",
        "mechanical degradation",
        "ceramic breeder",
        "material-degradation",
        "not incremental",
        "fusion-blanket ceramic material",
        "mother-pebble-resolved fracture-event extraction",
        "mechanism-index audit",
        "event-topology mechanism audit",
        "25, 35 and 60 micrometres",
        "rather than a converged failure probability",
    ]
    for phrase in required_cover_phrases:
        if phrase not in cover:
            errors.append(f"cover letter missing phrase: {phrase}")
    required_style_phrases = [
        "Dear Editors of the Journal of Nuclear Materials",
        "for consideration as a Research Article in the Journal of Nuclear Materials",
    ]
    for phrase in required_style_phrases:
        if phrase not in cover:
            errors.append(f"cover letter missing journal-style phrase: {phrase}")
    awkward_phrases = [
        "Dear Editors of Journal of Nuclear Materials",
        "for consideration as a Research Article in Journal of Nuclear Materials",
    ]
    for phrase in awkward_phrases:
        if phrase in cover:
            errors.append(f"cover letter contains awkward journal phrase: {phrase}")
    if (
        "repository DOI or stable URL will be inserted before final upload" not in cover
        and "the repository DOI or stable URL is " not in cover
    ):
        errors.append("cover letter missing repository DOI/stable URL status phrase")

    forbidden_patterns = [
        r"\bPB-006\b",
        r"\bPB-007\b",
        r"\bSP-002\b",
        r"\bCAL1\b",
        r"\bseed\d+\b",
        r"\bTable 3\b",
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, cover, flags=re.IGNORECASE):
            errors.append(f"cover letter contains reader-facing/internal label: {pattern}")

    bullets = [line.removeprefix("-").strip() for line in highlights.splitlines() if line.strip().startswith("-")]
    if not (3 <= len(bullets) <= 5):
        errors.append(f"highlights has {len(bullets)} bullets; expected 3-5")
    too_long = [bullet for bullet in bullets if len(bullet) > 85]
    if too_long:
        errors.append("highlights over 85 characters: " + "; ".join(too_long))

    if errors:
        print("FAIL cover letter")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS cover letter: title/material framing and {len(bullets)} highlights verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
