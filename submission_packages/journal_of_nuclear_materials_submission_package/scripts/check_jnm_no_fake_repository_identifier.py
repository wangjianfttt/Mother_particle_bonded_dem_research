#!/usr/bin/env python3
"""Reject fake or rehearsal repository identifiers in JNM-facing files."""

from __future__ import annotations

import re
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCAN_DIRS = [
    ROOT / "manuscript",
    ROOT / "docs",
    ROOT / "tables",
    ROOT / "scripts",
    ROOT / "submission_packages/jnm_repository_deposit_staging",
]

TEXT_SUFFIXES = {
    ".bib",
    ".csv",
    ".json",
    ".lmp",
    ".md",
    ".py",
    ".sh",
    ".tex",
    ".txt",
}

FORBIDDEN_PATTERNS = [
    re.compile(r"10\.5281/zenodo\.99999999", re.IGNORECASE),
    re.compile(r"zenodo\.99999999", re.IGNORECASE),
    re.compile(r"doi\.org/10\.5281/zenodo\.99999999", re.IGNORECASE),
    re.compile(r"10\.0000/[A-Za-z0-9_.-]+", re.IGNORECASE),
    re.compile(r"10\.1234/[A-Za-z0-9_.-]+", re.IGNORECASE),
    re.compile(r"example\.com", re.IGNORECASE),
]


def iter_text_files() -> list[Path]:
    paths: list[Path] = []
    for root in SCAN_DIRS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            paths.append(path)
    return sorted(paths)


def main() -> int:
    if os.environ.get("JNM_ALLOW_FAKE_REPOSITORY_IDENTIFIER") == "1":
        print("PASS fake repository identifier check: explicitly allowed for isolated DOI rehearsal")
        return 0

    hits: list[str] = []
    for path in iter_text_files():
        text = path.read_text(errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(pattern.search(line) for pattern in FORBIDDEN_PATTERNS):
                hits.append(f"{path.relative_to(ROOT)}:{line_no}")
    if hits:
        print("FAIL fake repository identifier check: " + ", ".join(hits[:30]))
        return 1
    print("PASS fake repository identifier check: no concrete rehearsal DOI or example URL leaked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
