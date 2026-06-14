#!/usr/bin/env python3
"""Build the public JNM reproducibility package.

This package is intended for Zenodo/Figshare/institutional deposition. It is
therefore narrower than the Editorial Manager submission package: it includes
public manuscript/evidence artifacts, processed data, figure outputs, audit
scripts and representative DEM inputs, but excludes cover letters,
declarations, author checklists and reviewer-preparation notes.
"""

from __future__ import annotations

import csv
import hashlib
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package"
PACKAGE_ZIP = ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip"
PACKAGE_SHA = ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip.sha256"

MATRICES = [
    ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
]
PATH_COLUMNS = [
    "output_files",
    "source_data_files",
    "generation_or_audit_scripts",
    "primary_source_data_or_docs",
]
SELF_ARCHIVE_PREFIXES = (
    "submission_packages/journal_of_nuclear_materials_submission_package",
    "submission_packages/journal_of_nuclear_materials_reproducibility_package",
)
PUBLIC_EXCLUDED_FILES = {
    "docs/jnm_final_submission_gate_report.md",
    "docs/jnm_final_submission_gate_report.json",
}

PUBLIC_EXACT_FILES = [
    "manuscript/journal_of_nuclear_materials_submission.pdf",
    "manuscript/journal_of_nuclear_materials_submission.tex",
    "manuscript/journal_of_nuclear_materials_submission_draft.md",
    "manuscript/journal_of_nuclear_materials_supplementary.pdf",
    "manuscript/journal_of_nuclear_materials_supplementary.tex",
    "manuscript/journal_of_nuclear_materials_supplementary.md",
    "manuscript/journal_of_nuclear_materials_highlights.md",
    "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv",
    "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
    "manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json",
    "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md",
    "manuscript/journal_of_nuclear_materials_repro_package_readme.md",
    "manuscript/references.bib",
    "docs/jnm_force_transmission_validation_audit_20260612.md",
    "docs/jnm_revision_gate_after_pb006_audit_20260612.md",
    "docs/jnm_submission_readiness_audit_20260612.md",
    "docs/jnm_repository_deposit_action_checklist.md",
    "docs/jnm_repository_deposit_action_checklist_zh.md",
    "docs/jnm_final_submission_action_summary.md",
    "docs/jnm_official_scope_alignment_audit_20260613.md",
    "docs/jnm_scientific_storyline_audit_20260613.md",
    "docs/jnm_material_degradation_state_variables_audit_20260613.md",
    "docs/jnm_objective_completion_audit_20260613.md",
    "docs/single_pebble_calibration_dossier.md",
    "docs/next_stage_optimization_plan.md",
    "simulations/single_pebble/SP-002/in.plate_compression_weakplane.lmp",
    "simulations/single_pebble/SP-RESOLUTION/in.resolution_compression.lmp",
    "simulations/single_pebble/templates/sp_500_d1mm_nooverlap/particles.csv",
    "simulations/single_pebble/templates/sp_500_d1mm_nooverlap/bonds.csv",
    "simulations/single_pebble/templates/sp_500_d1mm_nooverlap/summary.md",
    "simulations/pebble_bed/PB-007/in.pb007_rigid_surface_settle.lmp",
    "simulations/pebble_bed/PB-007/in.pb007_bonded_transfer_initcheck.lmp",
    "simulations/pebble_bed/PB-007/in.pb007_bonded_step_relaxed_validation.lmp",
    "simulations/pebble_bed/PB-007/in.pb007_bonded_loadpath_validation.lmp",
]

PUBLIC_BUILD_SCRIPTS = [
    "scripts/build_jnm_public_repro_package.py",
    "scripts/check_jnm_public_repro_package.py",
    "scripts/check_jnm_repro_package_coverage.py",
    "scripts/check_jnm_source_data_matrix.py",
    "scripts/check_jnm_claim_evidence_matrix.py",
    "scripts/check_jnm_public_artifact_hygiene.py",
    "scripts/check_jnm_reader_facing_hygiene.py",
    "scripts/check_jnm_no_fake_repository_identifier.py",
    "scripts/check_jnm_repository_deposit_staging.py",
    "scripts/check_jnm_title_consistency.py",
    "scripts/print_jnm_repository_deposit_packet.py",
    "scripts/check_jnm_official_scope_alignment.py",
    "scripts/check_jnm_scientific_storyline.py",
    "scripts/check_jnm_material_degradation_state_variables.py",
    "scripts/check_jnm_objective_completion_audit.py",
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


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def matrix_paths() -> set[str]:
    paths: set[str] = set()
    for matrix in MATRICES:
        rows = list(csv.DictReader(matrix.open()))
        for row in rows:
            for column in PATH_COLUMNS:
                if column not in row:
                    continue
                for rel in split_paths(row.get(column, "")):
                    if rel.startswith(SELF_ARCHIVE_PREFIXES):
                        continue
                    paths.add(rel)
    return paths


def collect_files() -> list[Path]:
    rel_paths = (set(PUBLIC_EXACT_FILES) | set(PUBLIC_BUILD_SCRIPTS) | matrix_paths()) - PUBLIC_EXCLUDED_FILES
    paths: list[Path] = []
    missing: list[str] = []
    for rel in sorted(rel_paths):
        path = ROOT / rel
        if path.exists() and path.is_file():
            paths.append(path)
        else:
            missing.append(rel)
    if missing:
        raise FileNotFoundError("Missing public reproducibility inputs: " + ", ".join(missing))
    return paths


def sanitize_text_file(path: Path) -> None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return
    try:
        text = path.read_text(errors="strict")
    except UnicodeDecodeError:
        return
    replacements = {
        str(ROOT): "<project-root>",
        "<project-root>": "<project-root>",
        "<project-root-parent>": "<project-root-parent>",
        "<project-root>": "<project-root>",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_files(paths: list[Path]) -> None:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True)
    for source in paths:
        rel = source.relative_to(ROOT)
        target = PACKAGE_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        sanitize_text_file(target)

    readme_source = PACKAGE_DIR / "manuscript/journal_of_nuclear_materials_repro_package_readme.md"
    readme_target = PACKAGE_DIR / "README.md"
    shutil.copy2(readme_source, readme_target)
    sanitize_text_file(readme_target)


def write_manifest() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(PACKAGE_DIR.rglob("*")):
        if not path.is_file() or path.name == "MANIFEST.csv":
            continue
        rel = path.relative_to(PACKAGE_DIR).as_posix()
        rows.append(
            {
                "sha256": sha256(path),
                "path": rel,
                "size_bytes": str(path.stat().st_size),
            }
        )
    with (PACKAGE_DIR / "MANIFEST.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sha256", "path", "size_bytes"])
        writer.writeheader()
        writer.writerows(rows)


def build_zip() -> None:
    if PACKAGE_ZIP.exists():
        PACKAGE_ZIP.unlink()
    with zipfile.ZipFile(PACKAGE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if path.is_file():
                arcname = Path(PACKAGE_DIR.name) / path.relative_to(PACKAGE_DIR)
                archive.write(path, arcname.as_posix())
    PACKAGE_SHA.write_text(f"{sha256(PACKAGE_ZIP)}  {PACKAGE_ZIP.name}\n")


def main() -> int:
    paths = collect_files()
    copy_files(paths)
    write_manifest()
    build_zip()
    print(PACKAGE_ZIP)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
