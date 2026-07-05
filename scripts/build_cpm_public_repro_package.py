#!/usr/bin/env python3
"""Build the public CPM reproducibility package.

This package is intended for GitHub/Zenodo-style public code and data
availability. It includes manuscript-level processed data, figure source
tables, editable figures, representative DEM inputs and regeneration/check
scripts. It excludes cover letters, author-email collection files, live
submission packets and other editorial-support materials.
"""

from __future__ import annotations

import csv
import hashlib
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "computational_particle_mechanics_public_reproducibility_package"
PACKAGE_DIR = ROOT / "submission_packages" / PACKAGE_NAME
PACKAGE_ZIP = ROOT / "submission_packages" / f"{PACKAGE_NAME}.zip"
PACKAGE_SHA = ROOT / "submission_packages" / f"{PACKAGE_NAME}.zip.sha256"
SOURCE_MATRIX = ROOT / "manuscript" / "repaired_full_manuscript_source_data_matrix.csv"

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

PUBLIC_EXACT_FILES = {
    "README.md",
    "CITATION.cff",
    "START_HERE_CPM_SUBMISSION.md",
    "README_CPM_SUBMISSION_20260704.md",
    "manuscript/computational_particle_mechanics_submission.pdf",
    "manuscript/computational_particle_mechanics_submission.tex",
    "manuscript/computational_particle_mechanics_blinded_submission.pdf",
    "manuscript/computational_particle_mechanics_blinded_submission.tex",
    "manuscript/repaired_full_submission_draft.md",
    "manuscript/repaired_full_manuscript_source_data_matrix.csv",
    "manuscript/repaired_manuscript_claim_evidence_matrix.csv",
    "manuscript/references.bib",
    "docs/cpm_literature_gap_map_20260704.csv",
    "docs/cpm_literature_gap_map_20260704.md",
    "docs/cpm_material_response_summary_20260704.csv",
    "docs/cpm_material_response_summary_20260704.md",
    "docs/cpm_official_submission_guide_alignment_20260704.csv",
    "docs/cpm_official_submission_guide_alignment_20260704.md",
    "docs/cpm_submission_readiness_report_20260704.md",
    "docs/cpm_goal_completion_audit_20260704.md",
    "docs/repaired_manuscript_evidence_status_20260704.md",
    "docs/repaired_full_pdf_visual_qa_20260704.md",
    "docs/cpm_final_pdf_visual_qa_20260704.md",
    "docs/nas_raw_dump_storage_check_20260704_1736.md",
    "data/figure_source/pb007_material_strength_response.csv",
    "data/figure_source/pb007_material_strength_response_progress.csv",
    "data/figure_source/pb007_mechanism_variable_separation.csv",
    "data/processed/pb007_replicate_comparison_source_data.csv",
    "tables/pb007_event_aligned_topology.csv",
    "tables/pb007_macro_topology_event_metrics.csv",
    "tables/pb007_material_parameter_matrix_20260704.csv",
    "tables/pb007_material_parameter_response.csv",
    "tables/pb007_material_strength_matrix_summary.csv",
    "tables/pb007_mechanism_indices.csv",
    "tables/pb007_mechanism_variable_separation.csv",
    "simulations/single_pebble/SP-002/in.plate_compression_weakplane.lmp",
    "simulations/single_pebble/SP-RESOLUTION/in.resolution_compression.lmp",
    "simulations/single_pebble/SP-RESOLUTION/templates/sp_500_d1mm_nooverlap/particles.csv",
    "simulations/single_pebble/SP-RESOLUTION/templates/sp_500_d1mm_nooverlap/bonds.csv",
    "simulations/single_pebble/SP-RESOLUTION/templates/sp_500_d1mm_nooverlap/summary.md",
    "simulations/pebble_bed/PB-007/in.pb007_rigid_surface_settle.lmp",
    "simulations/pebble_bed/PB-007/in.pb007_bonded_transfer_initcheck.lmp",
    "simulations/pebble_bed/PB-007/in.pb007_bonded_step_relaxed_validation.lmp",
    "scripts/build_cpm_public_repro_package.py",
    "scripts/check_cpm_public_repro_package.py",
    "scripts/build_apt_redesigned_data_figures.py",
    "scripts/build_pb007_material_strength_response_progress.py",
    "scripts/build_pb007_replicate_comparison.py",
    "scripts/build_repaired_full_latex.py",
    "scripts/check_repaired_full_manuscript_consistency.py",
    "scripts/check_computational_particle_mechanics_submission_package.py",
    "scripts/summarize_pb007_material_parameter_response.py",
    "scripts/summarize_pb007_mechanism_metrics.py",
    "scripts/summarize_pb007_mechanism_variable_separation.py",
    "scripts/plot_main_workflow_figure.py",
}

PRIVATE_TOKENS = (
    "cover_letter",
    "declaration_of_competing_interest",
    "author_email",
    "coauthor_email",
    "individual_contact",
    "live_submission_packet",
    "live_submission_checklist",
    "editorial_upload",
    "reviewer_risk",
)


def split_semicolon_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def source_matrix_paths() -> set[str]:
    paths: set[str] = set()
    with SOURCE_MATRIX.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            for column in ["output_files", "source_data", "regeneration_or_check_script"]:
                for rel in split_semicolon_paths(row.get(column, "")):
                    if rel.startswith("manuscript/repaired_full_submission_draft.md"):
                        paths.add(rel)
                    elif not rel.startswith("submission_packages/"):
                        paths.add(rel)
    return paths


def collect_files() -> list[Path]:
    rel_paths = PUBLIC_EXACT_FILES | source_matrix_paths()
    paths: list[Path] = []
    missing: list[str] = []
    private: list[str] = []
    for rel in sorted(rel_paths):
        if any(token in rel.lower() for token in PRIVATE_TOKENS):
            private.append(rel)
            continue
        path = ROOT / rel
        if path.exists() and path.is_file():
            paths.append(path)
        else:
            missing.append(rel)
    if private:
        raise RuntimeError("private/editorial files selected: " + ", ".join(private[:12]))
    if missing:
        raise FileNotFoundError("missing public reproducibility inputs: " + ", ".join(missing[:20]))
    return paths


def sanitize_text_file(path: Path) -> None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return
    replacements = {
        str(ROOT): "<project-root>",
        "/Users/wangjian-macbook13/Documents/颗粒破碎统计研究": "<project-root>",
        "/Users/wangjian-macbook13/Documents": "<project-root-parent>",
        "/Users/wangjian-macbook13": "<user-home>",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reset_package_dir() -> None:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True)


def copy_files(paths: list[Path]) -> None:
    reset_package_dir()
    for source in paths:
        rel = source.relative_to(ROOT)
        target = PACKAGE_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        sanitize_text_file(target)

    readme = PACKAGE_DIR / "README.md"
    append = f"""

## Public Reproducibility Package

This folder is the public code/data package for the Computational Particle
Mechanics manuscript. It intentionally excludes cover letters, author e-mail
collection files, live submission packets and editorial upload work files.

Package archive: `submission_packages/{PACKAGE_NAME}.zip`
Checksum file: `submission_packages/{PACKAGE_NAME}.zip.sha256`
Repository DOI: https://doi.org/10.5281/zenodo.20687351
"""
    readme.write_text(readme.read_text(encoding="utf-8") + append, encoding="utf-8")


def write_manifest() -> None:
    rows: list[dict[str, str]] = []
    for path in sorted(PACKAGE_DIR.rglob("*")):
        if not path.is_file() or path.name == "MANIFEST.csv":
            continue
        rel = path.relative_to(PACKAGE_DIR).as_posix()
        rows.append({"sha256": sha256(path), "path": rel, "size_bytes": str(path.stat().st_size)})
    with (PACKAGE_DIR / "MANIFEST.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sha256", "path", "size_bytes"])
        writer.writeheader()
        writer.writerows(rows)


def build_zip() -> None:
    if PACKAGE_ZIP.exists():
        PACKAGE_ZIP.unlink()
    with zipfile.ZipFile(PACKAGE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if path.is_file():
                arcname = Path(PACKAGE_NAME) / path.relative_to(PACKAGE_DIR)
                archive.write(path, arcname.as_posix())
    PACKAGE_SHA.write_text(f"{sha256(PACKAGE_ZIP)}  {PACKAGE_ZIP.name}\n", encoding="utf-8")


def main() -> int:
    paths = collect_files()
    copy_files(paths)
    write_manifest()
    build_zip()
    print(PACKAGE_ZIP)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
