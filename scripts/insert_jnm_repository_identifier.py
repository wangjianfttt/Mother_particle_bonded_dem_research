#!/usr/bin/env python3
"""Insert the final repository DOI or stable URL into JNM submission files."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FILES_TO_UPDATE = [
    ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md",
    ROOT / "manuscript/journal_of_nuclear_materials_author_declaration_checklist.md",
    ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md",
    ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md",
    ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md",
    ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md",
    ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md",
    ROOT / "manuscript/journal_of_nuclear_materials_repro_package_readme.md",
    ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md",
    ROOT / "manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_resubmission_plan.md",
    ROOT / "docs/jnm_author_final_upload_readme_zh.md",
    ROOT / "docs/jnm_coauthor_final_approval_packet.md",
    ROOT / "docs/jnm_final_submission_action_summary.md",
    ROOT / "docs/jnm_final_submission_gate_report.md",
    ROOT / "docs/jnm_objective_completion_audit_20260613.md",
    ROOT / "docs/jnm_submission_readiness_audit_20260612.md",
    ROOT / "docs/next_stage_optimization_plan.md",
]

JSON_METADATA = ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json"


def validate_identifier(identifier: str) -> str:
    identifier = identifier.strip()
    if not identifier:
        raise ValueError("Identifier is empty")
    allowed = (
        identifier.startswith("https://doi.org/10.")
        or identifier.startswith("http://doi.org/10.")
        or identifier.startswith("doi:10.")
        or identifier.startswith("10.")
        or identifier.startswith("https://zenodo.org/")
        or identifier.startswith("https://figshare.com/")
        or identifier.startswith("https://")
    )
    if not allowed:
        raise ValueError(
            "Identifier should be a DOI, DOI URL or stable repository URL, for example "
            "https://doi.org/10.5281/zenodo.xxxxxxx"
        )
    return identifier


def data_availability_sentence(identifier: str) -> str:
    return (
        "The package has been deposited in a persistent repository and is available at "
        f"{identifier}."
    )


def replace_text(text: str, identifier: str) -> str:
    data_sentence = data_availability_sentence(identifier)
    text = re.sub(
        r"For submission, this package should be deposited in a persistent repository such as Zenodo, "
        r"Figshare or an institutional repository, and the final DOI or stable URL should be inserted "
        r"here before upload: \[repository DOI/URL to be added\]\.",
        data_sentence,
        text,
    )
    text = text.replace("[repository DOI/URL to be added]", identifier)
    text = text.replace("locally_ready_external_doi_pending", "repository_identifier_inserted")
    text = text.replace(
        "a repository DOI or stable URL will be inserted before final upload",
        f"the repository DOI or stable URL is {identifier}",
    )
    text = text.replace(
        "The package will be deposited in a persistent repository before final submission, and the generated DOI or stable URL should be inserted in the manuscript and submission system.",
        f"The package has been deposited in a persistent repository and is available at {identifier}.",
    )
    text = text.replace(
        "Repository DOI or stable URL inserted after deposit.",
        f"Repository DOI or stable URL inserted after deposit: {identifier}.",
    )
    text = text.replace(
        "Repository DOI/stable URL is inserted after deposit.",
        f"Repository DOI/stable URL inserted after deposit: {identifier}.",
    )
    text = text.replace(
        "the real DOI or stable URL must replace the current placeholder before submission.",
        f"the real DOI or stable URL has been inserted before submission: {identifier}.",
    )
    text = text.replace(
        "the real DOI or stable URL must replace the current placeholder before final submission.",
        f"the real DOI or stable URL has been inserted before final submission: {identifier}.",
    )
    text = text.replace("<真实DOI或URL>", identifier)
    text = text.replace("<doi-or-stable-url>", identifier)
    text = text.replace("<doi-or-url>", identifier)
    text = text.replace("<DOI-or-URL>", identifier)
    text = text.replace("doi_pending", "ready_after_repository_identifier_insert")
    text = text.replace("Deposit externally and insert DOI/stable URL", f"Deposited at {identifier}")
    text = text.replace("Repository DOI is missing", f"Repository identifier inserted: {identifier}")
    text = text.replace("Repository DOI/stable URL is missing", f"Repository identifier inserted: {identifier}")
    text = text.replace("Repository DOI/stable URL insertion still needed", f"Repository identifier inserted: {identifier}")
    text = text.replace("External DOI/stable URL required", f"Repository identifier inserted: {identifier}")
    text = text.replace("Deposit the reduced reproducibility package and insert the DOI or stable URL.", f"Reduced reproducibility package deposited at {identifier}.")
    text = text.replace(
        "Do not submit as fully complete until the repository DOI or stable URL is inserted.",
        f"Repository identifier inserted: {identifier}. Do not remove the repository availability statement.",
    )
    text = text.replace(
        "Repository DOI or stable URL is still pending.",
        f"Repository DOI or stable URL: {identifier}.",
    )
    text = text.replace(
        "A real repository DOI or stable URL must still be inserted before final submission.",
        f"Repository identifier inserted before final submission: {identifier}.",
    )
    text = text.replace("deposit DOI still needed", f"repository identifier inserted: {identifier}")
    text = text.replace("DOI still must be generated externally", f"repository identifier inserted: {identifier}")
    text = text.replace(
        "Local manuscript/package gate: `BLOCKED_EXTERNAL`",
        "Local manuscript/package gate: `PASS after repository identifier insertion`",
    )
    text = text.replace(
        "Expected blocker: repository DOI or stable URL has not yet been inserted",
        f"Repository identifier inserted: {identifier}",
    )
    text = text.replace(
        "the main workspace remains honestly pre-deposit at `BLOCKED_EXTERNAL` until a real repository identifier is available",
        f"the repository identifier has been inserted and the DOI-closure gate should pass for {identifier}",
    )
    return text


def update_json_metadata(identifier: str, apply: bool) -> str:
    data = json.loads(JSON_METADATA.read_text())
    data["related_identifiers"] = [
        {
            "identifier": identifier,
            "relation": "isSupplementTo",
            "scheme": "url" if identifier.startswith("http") else "doi",
        }
    ]
    data["notes"] = (
        data.get("notes", "")
        .replace(
            "After deposit, insert the generated DOI or stable URL into the manuscript Data availability statement, cover letter and submission system.",
            f"Repository identifier inserted for manuscript submission: {identifier}.",
        )
        .replace(
            "Before final deposit, confirm author names, affiliations, license choice, repository community and whether ORCID identifiers should be added.",
            "Before final upload, confirm author names, affiliations, license choice, repository community and whether ORCID identifiers should be added.",
        )
    )
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if apply:
        JSON_METADATA.write_text(rendered)
    return rendered


def update_files(identifier: str, apply: bool) -> list[str]:
    changed: list[str] = []
    for path in FILES_TO_UPDATE:
        original = path.read_text()
        updated = replace_text(original, identifier)
        if updated != original:
            changed.append(str(path.relative_to(ROOT)))
            if apply:
                path.write_text(updated)
    metadata = update_json_metadata(identifier, apply)
    if "related_identifiers" in metadata:
        changed.append(str(JSON_METADATA.relative_to(ROOT)))
    return changed


def run_rebuild() -> None:
    root_commands = [
        ["python3", "scripts/build_journal_of_nuclear_materials_latex.py"],
        ["python3", "scripts/render_jnm_pdf_visual_qa.py"],
        ["python3", "scripts/build_jnm_elsevier_flat_source_bundle.py"],
        ["python3", "scripts/build_jnm_upload_docx.py"],
        ["python3", "scripts/build_jnm_editorial_manager_upload_ready.py"],
        ["bash", "scripts/build_journal_of_nuclear_materials_submission_package.sh"],
        ["python3", "scripts/build_jnm_public_repro_package.py"],
        ["python3", "scripts/build_jnm_repository_deposit_staging.py"],
        ["python3", "scripts/build_jnm_repository_deposit_handoff.py"],
        ["python3", "scripts/build_jnm_repository_deposit_staging.py"],
        ["python3", "scripts/build_jnm_final_upload_manifest.py"],
        ["python3", "scripts/check_jnm_submission_gate.py"],
        ["bash", "scripts/build_journal_of_nuclear_materials_submission_package.sh"],
        ["python3", "scripts/build_jnm_public_repro_package.py"],
        ["python3", "scripts/build_jnm_repository_deposit_staging.py"],
        ["python3", "scripts/build_jnm_repository_deposit_handoff.py"],
        ["python3", "scripts/build_jnm_repository_deposit_staging.py"],
        ["python3", "scripts/build_jnm_final_upload_manifest.py"],
        ["python3", "scripts/check_jnm_submission_gate.py"],
    ]
    manuscript_command = [
        "latexmk",
        "-g",
        "-xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "journal_of_nuclear_materials_submission.tex",
    ]

    subprocess.run(root_commands[0], cwd=ROOT, check=True)
    subprocess.run(manuscript_command, cwd=ROOT / "manuscript", check=True)
    subprocess.run(root_commands[1], cwd=ROOT, check=True)
    subprocess.run(root_commands[2], cwd=ROOT, check=True)
    subprocess.run(
        manuscript_command,
        cwd=ROOT / "submission_packages/journal_of_nuclear_materials_flat_source",
        check=True,
    )
    for command in root_commands[3:]:
        subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("identifier", help="Repository DOI, DOI URL or stable URL")
    parser.add_argument("--apply", action="store_true", help="Write changes. Without this, perform a dry run.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument("--rebuild", action="store_true", help="After applying, rebuild manuscript/source/package and run gate.")
    args = parser.parse_args()

    if args.apply and args.dry_run:
        raise SystemExit("Use either --apply or --dry-run, not both.")
    identifier = validate_identifier(args.identifier)
    changed = update_files(identifier, apply=args.apply)
    mode = "APPLY" if args.apply else "DRY_RUN"
    print(f"mode={mode}")
    print(f"identifier={identifier}")
    print("changed_files:")
    for path in changed:
        print(f"- {path}")
    if args.rebuild:
        if not args.apply:
            raise SystemExit("--rebuild requires --apply")
        run_rebuild()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
