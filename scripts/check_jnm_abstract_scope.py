#!/usr/bin/env python3
"""Check the active JNM abstract for scope, length and conservative wording."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
MAX_WORDS = 250
REQUIRED_PHRASES = [
    "ceramic breeder",
    "mechanical degradation",
    "purge-gas pathways",
    "fracture-event sequences",
    "native force graph",
    "larger ensembles remain required",
]
FORBIDDEN_PATTERNS = [
    r"\bPB-006\b",
    r"\bPB-007\b",
    r"\bSP-002\b",
    r"\bCAL1\b",
    r"\bseed\d+\b",
    r"\bconverged failure probability\b",
    r"\bpredictive lifetime\b(?! or design-margin statements are made)",
    r"\bdesign-margin prediction\b",
]


def extract_abstract(text: str) -> str | None:
    match = re.search(r"^## Abstract\s*\n\n(.*?)\n\n^## Introduction", text, flags=re.DOTALL | re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def main() -> int:
    if not DRAFT.exists():
        print(f"FAIL abstract scope: missing {DRAFT}")
        return 1
    abstract = extract_abstract(DRAFT.read_text())
    if abstract is None:
        print("FAIL abstract scope: could not locate Abstract section")
        return 1

    errors: list[str] = []
    count = word_count(abstract)
    if count > MAX_WORDS:
        errors.append(f"abstract has {count} words; expected <= {MAX_WORDS}")
    lower = abstract.lower()
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in lower:
            errors.append(f"abstract missing scope phrase: {phrase}")
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, abstract, flags=re.IGNORECASE):
            errors.append(f"abstract contains forbidden/overclaim pattern: {pattern}")

    if errors:
        print("FAIL abstract scope")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS abstract scope: {count} words, material framing and conservative boundary verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
