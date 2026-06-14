#!/usr/bin/env python3
"""Stage the files needed for repository deposition of the JNM package."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission_packages/jnm_repository_deposit_staging"

FILES = [
    ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip",
    ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip.sha256",
    ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json",
    ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md",
    ROOT / "docs/jnm_repository_deposit_action_checklist.md",
    ROOT / "docs/jnm_repository_deposit_action_checklist_zh.md",
    ROOT / "docs/jnm_repository_deposit_final_handoff_zh.md",
    ROOT / "docs/jnm_final_submission_action_summary.md",
    ROOT / "docs/jnm_final_submission_gate_report.md",
    ROOT / "docs/jnm_final_submission_gate_report.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_readme() -> None:
    metadata = json.loads((ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json").read_text())
    lines = [
        "# JNM repository deposit staging",
        "",
        "This folder contains the files needed to deposit the reduced reproducibility package for the Journal of Nuclear Materials submission.",
        "The manuscript source package inside the zip is Elsevier-native (`elsarticle`/`frontmatter`) and uses the bundled `elsarticle-num.bst` numeric bibliography style.",
        "",
        "## Upload this file to the repository",
        "",
        "- `journal_of_nuclear_materials_reproducibility_package.zip`",
        "",
        "Keep the checksum file with your records and, if the repository allows multiple files, upload it as supporting metadata:",
        "",
        "- `journal_of_nuclear_materials_reproducibility_package.zip.sha256`",
        "",
        "From this staging folder, verify the package checksum before upload:",
        "",
        "```bash",
        "shasum -a 256 -c journal_of_nuclear_materials_reproducibility_package.zip.sha256",
        "```",
        "",
        "## Suggested repository metadata",
        "",
        f"- Title: {metadata.get('title', '')}",
        f"- Upload type: {metadata.get('upload_type', '')}",
        f"- License: {metadata.get('license', '')}",
        f"- Access: {metadata.get('access_right', '')}",
        f"- Version: {metadata.get('version', '')}",
        f"- Language: {metadata.get('language', '')}",
        f"- Keywords: {', '.join(metadata.get('keywords', []))}",
        "",
        "Use `journal_of_nuclear_materials_repository_metadata_zenodo.json` as the structured metadata source.",
        "Use `jnm_repository_deposit_action_checklist.md` as the step-by-step author-side upload checklist.",
        "Use `jnm_repository_deposit_action_checklist_zh.md` as the Chinese author-side upload checklist.",
        "Use `jnm_repository_deposit_final_handoff_zh.md` as the concise Chinese final handoff for the corresponding author.",
        "Use `jnm_final_submission_action_summary.md` as the compact final upload sequence.",
        "",
        "From the project root, this read-only command prints the upload file, checksum and current gate status:",
        "",
        "```bash",
        "python3 scripts/print_jnm_repository_deposit_packet.py",
        "```",
        "",
        "## After the repository reserves or publishes a DOI/stable URL",
        "",
        "From the project root, run:",
        "",
        "```bash",
        "python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild",
        "```",
        "",
        "Before applying, preview with:",
        "",
        "```bash",
        "python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run",
        "```",
        "",
        "The current final-gate report is included here for audit context. Before DOI insertion, its expected status is `BLOCKED_EXTERNAL` with no local `FAIL` entries.",
        "",
    ]
    (OUT / "README_deposit_staging.md").write_text("\n".join(lines))


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    rows: list[dict[str, str]] = []
    for source in FILES:
        if not source.exists():
            raise FileNotFoundError(source)
        target = OUT / source.name
        shutil.copy2(source, target)
        rows.append(
            {
                "file": target.name,
                "source": str(source.relative_to(ROOT)),
                "size_bytes": str(target.stat().st_size),
                "sha256": sha256(target),
            }
        )
    write_readme()
    readme = OUT / "README_deposit_staging.md"
    rows.append(
        {
            "file": readme.name,
            "source": "generated",
            "size_bytes": str(readme.stat().st_size),
            "sha256": sha256(readme),
        }
    )
    with (OUT / "STAGING_MANIFEST.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "source", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    print(OUT)


if __name__ == "__main__":
    main()
