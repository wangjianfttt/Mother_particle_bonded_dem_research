#!/usr/bin/env python3
"""Build an author-facing final upload manifest for the JNM submission."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "docs/jnm_final_upload_manifest.csv"
OUT_MD = ROOT / "docs/jnm_final_upload_manifest.md"
STAGING = ROOT / "submission_packages/jnm_repository_deposit_staging"
FROZEN = ROOT / "submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def row(role: str, destination: str, path: Path, action: str, note: str) -> dict[str, str]:
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(path)
    return {
        "role": role,
        "destination": destination,
        "path": rel(path),
        "size_bytes": str(path.stat().st_size),
        "sha256": sha256(path),
        "action": action,
        "note": note,
    }


def build_rows() -> list[dict[str, str]]:
    return [
        row(
            "public_reproducibility_zip",
            "repository",
            FROZEN / "journal_of_nuclear_materials_reproducibility_package.zip",
            "UPLOAD_TO_REPOSITORY",
            "This frozen zip is the only zip that should be deposited as the public data/code reproducibility record.",
        ),
        row(
            "public_reproducibility_checksum",
            "repository",
            FROZEN / "journal_of_nuclear_materials_reproducibility_package.zip.sha256",
            "UPLOAD_OR_RECORD_WITH_REPOSITORY",
            "Use to verify the public reproducibility zip before and after upload.",
        ),
        row(
            "repository_metadata_json",
            "repository",
            FROZEN / "journal_of_nuclear_materials_repository_metadata_zenodo.json",
            "USE_AS_METADATA_SOURCE",
            "Structured title, creators, description, keywords and license metadata.",
        ),
        row(
            "repository_metadata_readme",
            "repository",
            FROZEN / "journal_of_nuclear_materials_repository_metadata_readme.md",
            "USE_AS_METADATA_GUIDE",
            "Human-readable repository-deposit guide.",
        ),
        row(
            "repository_deposit_checklist_en",
            "repository_support",
            FROZEN / "jnm_repository_deposit_action_checklist.md",
            "READ_BEFORE_DEPOSIT",
            "English author-side deposit checklist.",
        ),
        row(
            "repository_deposit_checklist_zh",
            "repository_support",
            FROZEN / "jnm_repository_deposit_action_checklist_zh.md",
            "READ_BEFORE_DEPOSIT",
            "Chinese author-side deposit checklist.",
        ),
        row(
            "repository_deposit_handoff_zh",
            "repository_support",
            FROZEN / "jnm_repository_deposit_final_handoff_zh.md",
            "READ_BEFORE_DEPOSIT",
            "Concise Chinese handoff with current package SHA256 and expected post-DOI gate.",
        ),
        row(
            "editorial_manager_upload_ready_zip",
            "editorial_manager",
            ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip",
            "UPLOAD_OR_UNZIP_FOR_EDITORIAL_MANAGER",
            "Minimal local Editorial Manager upload bundle; not the public data repository record.",
        ),
        row(
            "manuscript_pdf",
            "editorial_manager",
            ROOT / "manuscript/journal_of_nuclear_materials_submission.pdf",
            "UPLOAD_TO_EDITORIAL_MANAGER_AFTER_DOI_INSERTION",
            "Regenerate after inserting the real repository DOI or stable URL.",
        ),
        row(
            "flat_latex_source_zip",
            "editorial_manager",
            ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip",
            "UPLOAD_IF_SOURCE_FILES_REQUESTED",
            "Elsevier-ready flat LaTeX source bundle.",
        ),
        row(
            "paste_ready_fields",
            "editorial_manager",
            ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md",
            "PASTE_INTO_EDITORIAL_MANAGER_AFTER_DOI_INSERTION",
            "Title, abstract, keywords, highlights, declarations and availability statements.",
        ),
        row(
            "local_submission_support_package",
            "local_support_only",
            ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip",
            "DO_NOT_UPLOAD_AS_PUBLIC_REPOSITORY_RECORD",
            "Internal Editorial Manager/coauthor support archive; contains submission-management material.",
        ),
    ]


def write_csv(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["role", "destination", "path", "size_bytes", "sha256", "action", "note"],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, str]]) -> None:
    upload = next(row for row in rows if row["role"] == "public_reproducibility_zip")
    lines = [
        "# JNM final upload manifest",
        "",
        "This manifest distinguishes the public repository deposit files from local Editorial Manager support files.",
        "",
        "## Public repository upload",
        "",
        f"- Upload zip: `{upload['path']}`",
        f"- SHA256: `{upload['sha256']}`",
        "- Do not upload `submission_packages/journal_of_nuclear_materials_submission_package.zip` as the public data repository record.",
        "",
        "## Machine-readable manifest",
        "",
        f"- CSV: `{rel(OUT_CSV)}`",
        "",
        "## Entries",
        "",
        "| Role | Destination | Action | Path |",
        "| --- | --- | --- | --- |",
    ]
    for item in rows:
        lines.append(f"| {item['role']} | {item['destination']} | {item['action']} | `{item['path']}` |")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    rows = build_rows()
    write_csv(rows)
    write_md(rows)
    print(OUT_CSV)
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
