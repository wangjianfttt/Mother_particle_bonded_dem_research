#!/usr/bin/env python3
"""Check the JNM coauthor final approval packet."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs/jnm_coauthor_final_approval_packet.md"
AUTHOR_CSV = ROOT / "manuscript/journal_of_nuclear_materials_author_metadata.csv"

REQUIRED_PHRASES = [
    "Journal of Nuclear Materials",
    "Research article",
    "Acceptance-gated bonded-template DEM reveals localized fracture sequences",
    "Jian Wang",
    "wjfttt@mail.ustc.edu.cn",
    "CRediT authorship contribution statement",
    "Declaration of competing interest",
    "Data and code availability",
    "repository DOI or stable URL",
    "Evidence boundary reminder",
    "current calibration candidate",
    "event-sequence and sensitivity evidence",
]

REQUIRED_GRANTS: list[str] = []


def checkbox_count(text: str) -> int:
    return len(re.findall(r"^- \[[ xX]\] ", text, flags=re.MULTILINE))


def main() -> int:
    errors: list[str] = []
    if not PACKET.exists():
        print(f"FAIL coauthor approval packet: missing {PACKET}")
        return 1
    if not AUTHOR_CSV.exists():
        print(f"FAIL coauthor approval packet: missing {AUTHOR_CSV}")
        return 1

    text = PACKET.read_text()
    rows = list(csv.DictReader(AUTHOR_CSV.open()))
    if len(rows) != 8:
        errors.append(f"expected 8 authors in metadata, found {len(rows)}")

    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            errors.append(f"missing phrase: {phrase}")
    for grant in REQUIRED_GRANTS:
        if grant not in text:
            errors.append(f"missing grant number: {grant}")

    for row in rows:
        name = row["display_name"]
        roles = [role.strip() for role in row["credit_roles"].split(";") if role.strip()]
        if name not in text:
            errors.append(f"missing author: {name}")
        for role in roles:
            if role not in text:
                errors.append(f"missing CRediT role for {name}: {role}")

    if checkbox_count(text) < 8:
        errors.append("expected at least 8 final confirmation checkboxes")
    if "confirm before upload" not in text:
        errors.append("approval packet must preserve confirm-before-upload status")

    if errors:
        print("FAIL coauthor approval packet")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS coauthor approval packet: {len(rows)} authors, declarations and evidence boundary verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
