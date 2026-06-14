#!/usr/bin/env python3
"""Check active JNM citation coverage and BibTeX metadata."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "manuscript/journal_of_nuclear_materials_submission.tex"
BIB = ROOT / "manuscript/references.bib"
REQUIRED_ARTICLE_FIELDS = ["author", "title", "journal", "year", "doi"]
PLACEHOLDER_PATTERN = re.compile(r"\b(?:todo|tbd|placeholder|unverified|missing)\b", re.IGNORECASE)


def citation_keys(tex: str) -> set[str]:
    keys: set[str] = set()
    for match in re.finditer(r"\\cite[a-zA-Z*]*\{([^}]*)\}", tex):
        keys.update(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys


def parse_bib_entries(text: str) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    starts = list(re.finditer(r"@(\w+)\s*\{\s*([^,]+)\s*,", text))
    for index, start in enumerate(starts):
        end_pos = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        entry_text = text[start.end() : end_pos]
        entry_type = start.group(1).lower()
        key = start.group(2).strip()
        fields = {"ENTRYTYPE": entry_type}
        for field, value in re.findall(r"(?m)^\s*([A-Za-z][A-Za-z0-9_-]*)\s*=\s*[\{\"](.+?)[\}\"]\s*,?\s*$", entry_text):
            fields[field.lower()] = value.strip()
        entries[key] = fields
    return entries


def main() -> int:
    errors: list[str] = []
    if not TEX.exists():
        print(f"FAIL references: missing {TEX}")
        return 1
    if not BIB.exists():
        print(f"FAIL references: missing {BIB}")
        return 1
    tex = TEX.read_text(errors="replace")
    bib = BIB.read_text(errors="replace")
    cites = citation_keys(tex)
    entries = parse_bib_entries(bib)
    bib_keys = set(entries)

    missing = sorted(cites - bib_keys)
    uncited = sorted(bib_keys - cites)
    if missing:
        errors.append("missing BibTeX entries for citations: " + ", ".join(missing))
    if uncited:
        errors.append("uncited BibTeX entries in active JNM bibliography: " + ", ".join(uncited))

    for key, fields in sorted(entries.items()):
        entry_type = fields.get("ENTRYTYPE", "")
        if PLACEHOLDER_PATTERN.search(str(fields)):
            errors.append(f"{key}: placeholder/unverified marker present")
        if entry_type == "article":
            for field in REQUIRED_ARTICLE_FIELDS:
                if not fields.get(field):
                    errors.append(f"{key}: missing required article field {field}")
        elif entry_type in {"misc", "software"}:
            if not (fields.get("url") or fields.get("doi")):
                errors.append(f"{key}: misc/software entry needs url or doi")

    if errors:
        print("FAIL references")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS references: {len(cites)} active citations, {len(entries)} BibTeX entries, metadata complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
