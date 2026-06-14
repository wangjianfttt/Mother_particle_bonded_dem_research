#!/usr/bin/env python3
"""Verify the frozen repository-deposit packet intended for upload."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e"
PACKAGE = FROZEN / "journal_of_nuclear_materials_reproducibility_package.zip"
CHECKSUM = FROZEN / "journal_of_nuclear_materials_reproducibility_package.zip.sha256"
METADATA = FROZEN / "journal_of_nuclear_materials_repository_metadata_zenodo.json"
README = FROZEN / "README_UPLOAD_THIS_FROZEN_PACKET.md"
VERIFY = FROZEN / "VERIFY_BEFORE_UPLOAD.sh"
HANDOFF_ZH = FROZEN / "jnm_repository_deposit_final_handoff_zh.md"
ACTION_SUMMARY = FROZEN / "jnm_final_submission_action_summary.md"
UPLOAD_MANIFEST_CSV = FROZEN / "jnm_final_upload_manifest.csv"
UPLOAD_MANIFEST_MD = FROZEN / "jnm_final_upload_manifest.md"
EXPECTED_SHA = "b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30"


def fail(message: str) -> int:
    print("FAIL frozen deposit packet: " + message)
    return 1


def main() -> int:
    required = [
        PACKAGE,
        CHECKSUM,
        METADATA,
        README,
        VERIFY,
        HANDOFF_ZH,
        ACTION_SUMMARY,
        UPLOAD_MANIFEST_CSV,
        UPLOAD_MANIFEST_MD,
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required if not path.exists() or path.stat().st_size == 0]
    if missing:
        return fail("missing or empty files: " + ", ".join(missing))

    checksum_text = CHECKSUM.read_text(encoding="utf-8").strip()
    if EXPECTED_SHA not in checksum_text:
        return fail("checksum file does not contain expected frozen SHA")

    result = subprocess.run(
        ["shasum", "-a", "256", "-c", CHECKSUM.name],
        cwd=FROZEN,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return fail((result.stdout + result.stderr).strip())

    json.loads(METADATA.read_text(encoding="utf-8"))

    readme = README.read_text(encoding="utf-8")
    if EXPECTED_SHA not in readme or "Do not mix hashes" not in readme:
        return fail("README does not preserve frozen hash and no-mixing warning")

    verify_text = VERIFY.read_text(encoding="utf-8")
    if EXPECTED_SHA not in verify_text or "insert_jnm_repository_identifier.py" not in verify_text:
        return fail("VERIFY script does not preserve frozen hash or DOI-insertion instructions")

    support_texts = {
        HANDOFF_ZH.relative_to(ROOT).as_posix(): HANDOFF_ZH.read_text(encoding="utf-8"),
        ACTION_SUMMARY.relative_to(ROOT).as_posix(): ACTION_SUMMARY.read_text(encoding="utf-8"),
        UPLOAD_MANIFEST_CSV.relative_to(ROOT).as_posix(): UPLOAD_MANIFEST_CSV.read_text(encoding="utf-8"),
        UPLOAD_MANIFEST_MD.relative_to(ROOT).as_posix(): UPLOAD_MANIFEST_MD.read_text(encoding="utf-8"),
    }
    required_support_phrases = {
        HANDOFF_ZH.relative_to(ROOT).as_posix(): [
            "PASS/WARN/BLOCKED_EXTERNAL/FAIL：`84/0/1/0`",
            "85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL",
            EXPECTED_SHA,
        ],
        ACTION_SUMMARY.relative_to(ROOT).as_posix(): [
            "materials-novelty positioning audit",
            "85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL and 0 FAIL",
            EXPECTED_SHA,
        ],
        UPLOAD_MANIFEST_CSV.relative_to(ROOT).as_posix(): [
            "public_reproducibility_zip",
            "DO_NOT_UPLOAD_AS_PUBLIC_REPOSITORY_RECORD",
            EXPECTED_SHA,
        ],
        UPLOAD_MANIFEST_MD.relative_to(ROOT).as_posix(): [
            "Do not upload `submission_packages/journal_of_nuclear_materials_submission_package.zip`",
            EXPECTED_SHA,
        ],
    }
    for rel, phrases in required_support_phrases.items():
        missing_phrases = [phrase for phrase in phrases if phrase not in support_texts[rel]]
        if missing_phrases:
            return fail(f"frozen support file {rel} missing current phrases: " + "; ".join(missing_phrases))

    stale_phrases = [
        "74 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "75 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "75 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "76 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "77 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "78 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "78 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "79 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "79 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "80 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "80 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "81 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "83 PASS, 0 WARN, 1 BLOCKED_EXTERNAL",
        "84 PASS, 0 WARN, 0 BLOCKED_EXTERNAL",
        "74/0/1/0",
        "75/0/0/0",
        "75/0/1/0",
        "76/0/0/0",
        "77/0/1/0",
        "78/0/0/0",
        "78/0/1/0",
        "79/0/0/0",
        "79/0/1/0",
        "80/0/0/0",
        "80/0/1/0",
        "81/0/0/0",
    ]
    stale_hits: list[str] = []
    for rel, text in support_texts.items():
        for phrase in stale_phrases:
            if phrase in text:
                stale_hits.append(f"{rel}: {phrase}")
    if stale_hits:
        return fail("stale gate-count phrases in frozen support files: " + "; ".join(stale_hits))

    print(
        "PASS frozen deposit packet: "
        f"{PACKAGE.relative_to(ROOT)} checksum OK, metadata JSON valid, upload instructions and support files current"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
