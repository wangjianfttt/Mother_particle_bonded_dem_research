#!/usr/bin/env python3
"""Check JNM author metadata against the active manuscript draft."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHOR_CSV = ROOT / "manuscript/journal_of_nuclear_materials_author_metadata.csv"
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"


def normalize_author(name: str) -> str:
    return name.replace("*", "").strip()


def normalize_affiliations(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"[;,]", value) if part.strip()]


def main() -> int:
    rows = list(csv.DictReader(AUTHOR_CSV.open()))
    text = MANUSCRIPT.read_text()
    authors_match = re.search(r"^Authors:\s*(.+)$", text, re.MULTILINE)
    if not authors_match:
        print("FAIL missing Authors line")
        return 1
    manuscript_authors = [normalize_author(part) for part in authors_match.group(1).split(",")]
    csv_authors = [row["display_name"] for row in rows]
    failures: list[str] = []
    if manuscript_authors != csv_authors:
        failures.append(f"author order mismatch: manuscript={manuscript_authors}; csv={csv_authors}")

    email_match = re.search(r"^\*Corresponding author:\s*(\S+)$", text, re.MULTILINE)
    manuscript_email = email_match.group(1) if email_match else ""
    csv_corresponding = [row for row in rows if row["corresponding_author"].lower() == "yes"]
    if len(csv_corresponding) != 1:
        failures.append(f"expected one corresponding author, found {len(csv_corresponding)}")
    elif csv_corresponding[0]["email"] != manuscript_email:
        failures.append(f"corresponding email mismatch: manuscript={manuscript_email}; csv={csv_corresponding[0]['email']}")

    for row in rows:
        pattern = rf"^- {re.escape(row['display_name'])}:\s*(.+)$"
        match = re.search(pattern, text, re.MULTILINE)
        if not match or normalize_affiliations(match.group(1)) != normalize_affiliations(row["affiliation_ids"]):
            failures.append(f"affiliation mapping mismatch for {row['display_name']}")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"PASS author metadata matches manuscript ({len(rows)} authors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
