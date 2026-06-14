#!/usr/bin/env python3
"""Verify the root-level JNM submission start-here guide."""

from __future__ import annotations

import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "START_HERE_JNM_SUBMISSION.md"
SUPPORT_ZIP = ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip"
SUPPORT_MEMBER = "journal_of_nuclear_materials_submission_package/START_HERE_JNM_SUBMISSION.md"
SUPPORT_REQUIRED_MEMBERS = [
    SUPPORT_MEMBER,
    "journal_of_nuclear_materials_submission_package/docs/jnm_repository_deposit_copy_paste_fields.md",
    "journal_of_nuclear_materials_submission_package/docs/jnm_author_final_upload_readme_zh.md",
]
EXPECTED_SHA = "b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30"


def fail(message: str) -> int:
    print("FAIL JNM start-here guide: " + message)
    return 1


def main() -> int:
    if not START.exists() or START.stat().st_size == 0:
        return fail("missing or empty START_HERE_JNM_SUBMISSION.md")

    text = START.read_text(encoding="utf-8")
    required_phrases = [
        "Upload the frozen repository package first",
        "submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/",
        "VERIFY_BEFORE_UPLOAD.sh",
        "journal_of_nuclear_materials_reproducibility_package.zip",
        EXPECTED_SHA,
        "journal_of_nuclear_materials_repository_metadata_zenodo.json",
        "docs/jnm_repository_deposit_copy_paste_fields.md",
        "Do not upload `submission_packages/journal_of_nuclear_materials_submission_package.zip`",
        "insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run",
        "insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild",
        "85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "84 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL",
        "The only blocker should be the repository DOI/stable URL",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        return fail("missing phrases: " + "; ".join(missing))

    forbidden = [
        "71 PASS",
        "75 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL",
        "76 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "77 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL",
        "78 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "78 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL",
        "79 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "79 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL",
        "80 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "80 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL",
        "81 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "83 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL",
        "84 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
        "71/0/1/0",
        "79/0/1/0",
        "80/0/0/0",
        "80/0/1/0",
        "81/0/0/0",
        "expected_after_repository_identifier=PASS 72",
    ]
    hits = [phrase for phrase in forbidden if phrase in text]
    if hits:
        return fail("stale phrases present: " + "; ".join(hits))

    if SUPPORT_ZIP.exists():
        with zipfile.ZipFile(SUPPORT_ZIP) as archive:
            names = set(archive.namelist())
            missing_support = [member for member in SUPPORT_REQUIRED_MEMBERS if member not in names]
            if missing_support:
                return fail("support package missing author-facing referenced files: " + "; ".join(missing_support))
            try:
                support_text = archive.read(SUPPORT_MEMBER).decode("utf-8")
            except KeyError:
                return fail(f"support package missing {SUPPORT_MEMBER}")
        if support_text != text:
            return fail("support package START_HERE_JNM_SUBMISSION.md is not synchronized with root copy")

    print("PASS JNM start-here guide: frozen upload path, DOI commands, gate counts and support-zip copy verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
