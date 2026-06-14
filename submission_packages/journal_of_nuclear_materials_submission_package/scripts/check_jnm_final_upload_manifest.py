#!/usr/bin/env python3
"""Verify the author-facing final upload manifest for the JNM submission."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "docs/jnm_final_upload_manifest.csv"
MD_PATH = ROOT / "docs/jnm_final_upload_manifest.md"

REQUIRED_ROLES = {
    "public_reproducibility_zip": {
        "path": "submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip",
        "destination": "repository",
        "action": "UPLOAD_TO_REPOSITORY",
    },
    "public_reproducibility_checksum": {
        "path": "submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip.sha256",
        "destination": "repository",
        "action": "UPLOAD_OR_RECORD_WITH_REPOSITORY",
    },
    "editorial_manager_upload_ready_zip": {
        "path": "submission_packages/jnm_editorial_manager_upload_ready.zip",
        "destination": "editorial_manager",
        "action": "UPLOAD_OR_UNZIP_FOR_EDITORIAL_MANAGER",
    },
    "manuscript_pdf": {
        "path": "manuscript/journal_of_nuclear_materials_submission.pdf",
        "destination": "editorial_manager",
        "action": "UPLOAD_TO_EDITORIAL_MANAGER_AFTER_DOI_INSERTION",
    },
    "flat_latex_source_zip": {
        "path": "submission_packages/journal_of_nuclear_materials_flat_source.zip",
        "destination": "editorial_manager",
        "action": "UPLOAD_IF_SOURCE_FILES_REQUESTED",
    },
    "paste_ready_fields": {
        "path": "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md",
        "destination": "editorial_manager",
        "action": "PASTE_INTO_EDITORIAL_MANAGER_AFTER_DOI_INSERTION",
    },
    "local_submission_support_package": {
        "path": "submission_packages/journal_of_nuclear_materials_submission_package.zip",
        "destination": "local_support_only",
        "action": "DO_NOT_UPLOAD_AS_PUBLIC_REPOSITORY_RECORD",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL final upload manifest: " + message)


def read_rows() -> list[dict[str, str]]:
    require(CSV_PATH.exists(), f"missing {CSV_PATH}")
    require(MD_PATH.exists(), f"missing {MD_PATH}")
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    require(bool(rows), "CSV has no data rows")
    required_columns = {"role", "destination", "path", "size_bytes", "sha256", "action", "note"}
    require(required_columns.issubset(rows[0]), "CSV columns are incomplete")
    return rows


def check_rows(rows: list[dict[str, str]]) -> None:
    by_role = {row["role"]: row for row in rows}
    missing_roles = sorted(set(REQUIRED_ROLES) - set(by_role))
    require(not missing_roles, "missing required roles " + ", ".join(missing_roles))

    public_rows = [row for row in rows if row["action"] == "UPLOAD_TO_REPOSITORY"]
    require(len(public_rows) == 1, "exactly one public repository upload zip must be marked UPLOAD_TO_REPOSITORY")
    require(public_rows[0]["role"] == "public_reproducibility_zip", "wrong public repository upload role")

    for role, expected in REQUIRED_ROLES.items():
        row = by_role[role]
        for field, value in expected.items():
            require(row[field] == value, f"{role} has {field}={row[field]!r}, expected {value!r}")

    for row in rows:
        path = ROOT / row["path"]
        require(path.exists(), f"missing referenced file {row['path']}")
        require(path.is_file(), f"referenced path is not a file {row['path']}")
        size = path.stat().st_size
        require(size > 0, f"empty referenced file {row['path']}")
        require(str(size) == row["size_bytes"], f"size mismatch for {row['path']}")
        digest = sha256(path)
        require(digest == row["sha256"], f"sha256 mismatch for {row['path']}")

    support = by_role["local_submission_support_package"]
    public = by_role["public_reproducibility_zip"]
    require(
        support["sha256"] != public["sha256"],
        "local support package and public reproducibility zip unexpectedly share a checksum",
    )


def check_markdown(rows: list[dict[str, str]]) -> None:
    text = MD_PATH.read_text(encoding="utf-8")
    by_role = {row["role"]: row for row in rows}
    public = by_role["public_reproducibility_zip"]
    support = by_role["local_submission_support_package"]
    required_phrases = [
        "JNM final upload manifest",
        public["path"],
        public["sha256"],
        "UPLOAD_TO_REPOSITORY",
        support["path"],
        "Do not upload",
        "DO_NOT_UPLOAD_AS_PUBLIC_REPOSITORY_RECORD",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    require(not missing, "Markdown manifest missing " + ", ".join(missing))


def main() -> int:
    rows = read_rows()
    check_rows(rows)
    check_markdown(rows)
    print(f"PASS final upload manifest: {len(rows)} entries, hashes and upload roles verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
