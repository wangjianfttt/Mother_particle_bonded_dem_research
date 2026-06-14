#!/usr/bin/env python3
"""Verify the repository-deposit copy-paste fields document."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/jnm_repository_deposit_copy_paste_fields.md"
EXPECTED_SHA = "b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30"


def fail(message: str) -> int:
    print("FAIL repository copy-paste fields: " + message)
    return 1


def main() -> int:
    if not DOC.exists() or DOC.stat().st_size == 0:
        return fail("missing or empty docs/jnm_repository_deposit_copy_paste_fields.md")
    text = DOC.read_text(encoding="utf-8")
    required = [
        "journal_of_nuclear_materials_reproducibility_package.zip",
        EXPECTED_SHA,
        "Dataset",
        "Reduced reproducibility package for acceptance-gated bonded-template DEM of Li4SiO4 breeder-bed fracture sequences",
        "CC BY 4.0",
        "Li4SiO4; ceramic breeder; fusion blanket",
        "Wang, Jian",
        "Lei, Ming-Zhun",
        "Institute of Plasma Physics, Chinese Academy of Sciences",
        "insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild",
        "85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
    ]
    missing = [phrase for phrase in required if phrase not in text]
    if missing:
        return fail("missing phrases: " + "; ".join(missing))
    forbidden = [
        "71 PASS",
        "72 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "73 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "79 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "80 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "81 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "84 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "[repository DOI/URL to be added]",
    ]
    hits = [phrase for phrase in forbidden if phrase in text]
    if hits:
        return fail("stale or placeholder phrases present: " + "; ".join(hits))
    print("PASS repository copy-paste fields: upload file, metadata and DOI commands verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
