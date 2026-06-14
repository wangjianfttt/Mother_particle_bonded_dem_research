#!/usr/bin/env python3
"""Build a minimal Editorial Manager upload-ready folder for JNM."""

from __future__ import annotations

import csv
import hashlib
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission_packages/jnm_editorial_manager_upload_ready"
ZIP_PATH = ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip"
SHA_PATH = ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip.sha256"

FILES = [
    ("01_manuscript_pdf", ROOT / "manuscript/journal_of_nuclear_materials_submission.pdf"),
    ("02_flat_latex_source", ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip"),
    ("02_flat_latex_source_sha256", ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip.sha256"),
    ("03_highlights", ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"),
    ("04_cover_letter", ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md"),
    ("04_cover_letter_docx", ROOT / "manuscript/journal_of_nuclear_materials_cover_letter.docx"),
    ("05_graphical_abstract_png", ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.png"),
    ("05_graphical_abstract_tiff", ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.tiff"),
    ("06_supplementary_pdf", ROOT / "manuscript/journal_of_nuclear_materials_supplementary.pdf"),
    ("07_declarations", ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md"),
    ("07_declarations_docx", ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.docx"),
    ("08_paste_ready_fields", ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md"),
    ("09_author_metadata", ROOT / "manuscript/journal_of_nuclear_materials_author_metadata.csv"),
    ("10_author_final_upload_readme_zh", ROOT / "docs/jnm_author_final_upload_readme_zh.md"),
    ("11_coauthor_final_approval_packet", ROOT / "docs/jnm_coauthor_final_approval_packet.md"),
    ("12_final_submission_action_summary", ROOT / "docs/jnm_final_submission_action_summary.md"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def staged_name(label: str, source: Path) -> str:
    suffix = "".join(source.suffixes)
    return f"{label}{suffix}"


def write_readme(rows: list[dict[str, str]]) -> None:
    lines = [
        "# JNM Editorial Manager upload-ready folder",
        "",
        "This folder contains the minimal local files that the corresponding author is likely to upload or paste into Elsevier Editorial Manager.",
        "It deliberately excludes internal reviewer-risk prebuttal files, claim-evidence matrices and raw simulation archives.",
        "",
        "Important: before final submission, deposit the reduced reproducibility package in a persistent repository and run:",
        "",
        "```bash",
        "python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild",
        "```",
        "",
        "After that command, rebuild this folder and use the refreshed files below.",
        "",
        "## File roles",
        "",
        "| Role | File | Source |",
        "| --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row['role']} | `{row['file']}` | `{row['source']}` |")
    lines.extend(
        [
            "",
            "Do not upload `reviewer_risk_prebuttal`, `claim_evidence_boundary_matrix` or large raw restart/local-bond dump files unless the editor explicitly requests them.",
            "",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def build_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(OUT.parent))
    SHA_PATH.write_text(f"{sha256(ZIP_PATH)}  {ZIP_PATH.name}\n", encoding="utf-8")


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    rows: list[dict[str, str]] = []
    for role, source in FILES:
        if not source.exists():
            raise FileNotFoundError(source)
        target = OUT / staged_name(role, source)
        shutil.copy2(source, target)
        rows.append(
            {
                "role": role,
                "file": target.name,
                "source": str(source.relative_to(ROOT)),
                "size_bytes": str(target.stat().st_size),
                "sha256": sha256(target),
            }
        )

    write_readme(rows)
    readme = OUT / "README.md"
    rows.append(
        {
            "role": "00_readme",
            "file": readme.name,
            "source": "generated",
            "size_bytes": str(readme.stat().st_size),
            "sha256": sha256(readme),
        }
    )
    with (OUT / "MANIFEST.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["role", "file", "source", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    build_zip()
    print(ZIP_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
