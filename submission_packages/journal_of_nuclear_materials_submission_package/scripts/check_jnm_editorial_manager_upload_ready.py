#!/usr/bin/env python3
"""Check the minimal JNM Editorial Manager upload-ready folder."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission_packages/jnm_editorial_manager_upload_ready"
ZIP_PATH = ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip"
SHA_PATH = ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip.sha256"
MANIFEST = OUT / "MANIFEST.csv"
ROLE_SOURCE_CHECKS = {
    "03_highlights": ROOT / "manuscript/journal_of_nuclear_materials_highlights.md",
    "05_graphical_abstract_png": ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.png",
    "05_graphical_abstract_tiff": ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.tiff",
    "08_paste_ready_fields": ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md",
}

REQUIRED_ROLES = {
    "00_readme",
    "01_manuscript_pdf",
    "02_flat_latex_source",
    "02_flat_latex_source_sha256",
    "03_highlights",
    "04_cover_letter",
    "04_cover_letter_docx",
    "05_graphical_abstract_png",
    "05_graphical_abstract_tiff",
    "06_supplementary_pdf",
    "07_declarations",
    "07_declarations_docx",
    "08_paste_ready_fields",
    "09_author_metadata",
    "10_author_final_upload_readme_zh",
    "11_coauthor_final_approval_packet",
    "12_final_submission_action_summary",
}

FORBIDDEN_FRAGMENTS = [
    "reviewer_risk",
    "claim_evidence",
    "local-bond",
    "restart",
]

README_PHRASES = [
    "Editorial Manager",
    "minimal local files",
    "insert_jnm_repository_identifier.py",
    "reviewer-risk prebuttal",
    "claim-evidence matrices",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> int:
    print(f"FAIL editorial-manager-upload-ready: {message}")
    return 1


def main() -> int:
    if not OUT.exists() or not ZIP_PATH.exists() or not SHA_PATH.exists() or not MANIFEST.exists():
        return fail("missing upload-ready folder, zip, checksum or manifest")
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
    if not rows:
        return fail("manifest has no rows")
    roles = {row["role"] for row in rows}
    missing = sorted(REQUIRED_ROLES - roles)
    extra = sorted(roles - REQUIRED_ROLES)
    if missing:
        return fail("missing role(s): " + ", ".join(missing))
    if extra:
        return fail("unexpected role(s): " + ", ".join(extra))

    for row in rows:
        path = OUT / row["file"]
        if not path.exists() or path.stat().st_size == 0:
            return fail(f"missing or empty file for role {row['role']}: {row['file']}")
        if int(row["size_bytes"]) != path.stat().st_size:
            return fail(f"size mismatch for {row['file']}")
        if row["sha256"] != sha256(path):
            return fail(f"sha256 mismatch for {row['file']}")
        source = ROLE_SOURCE_CHECKS.get(row["role"])
        if source is not None and sha256(path) != sha256(source):
            return fail(f"staged file for role {row['role']} differs from source {source.relative_to(ROOT)}")

    readme = (OUT / "README.md").read_text(encoding="utf-8")
    missing_readme = [phrase for phrase in README_PHRASES if phrase not in readme]
    if missing_readme:
        return fail("README missing phrase(s): " + ", ".join(missing_readme))

    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = set(archive.namelist())
    expected_members = {f"jnm_editorial_manager_upload_ready/{row['file']}" for row in rows}
    expected_members.add("jnm_editorial_manager_upload_ready/MANIFEST.csv")
    missing_members = sorted(expected_members - names)
    if missing_members:
        return fail("zip missing member(s): " + ", ".join(missing_members[:10]))
    forbidden = [name for name in names if any(fragment in name.lower() for fragment in FORBIDDEN_FRAGMENTS)]
    if forbidden:
        return fail("zip contains internal/raw file(s): " + ", ".join(forbidden[:10]))

    expected_hash = SHA_PATH.read_text(encoding="utf-8").split()[0]
    if expected_hash != sha256(ZIP_PATH):
        return fail("upload-ready zip checksum mismatch")

    print(
        "PASS editorial-manager-upload-ready: "
        f"{len(rows)} files, zip, checksum, source-sync and upload-only hygiene verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
