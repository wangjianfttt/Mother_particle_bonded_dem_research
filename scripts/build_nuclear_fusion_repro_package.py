#!/usr/bin/env python3
"""Build a reduced Nuclear Fusion reproducibility package.

The package contains manuscript-facing figures, processed CSV tables, selected
simulation inputs and scripts needed to regenerate the reported event database
and plots. It intentionally excludes raw restart files and large local-bond dump
histories.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


EXACT_FILES = [
    "manuscript/nuclear_fusion_submission_draft.md",
    "manuscript/nuclear_fusion_iop_submission.tex",
    "manuscript/nuclear_fusion_iop_submission.pdf",
    "manuscript/nuclear_fusion_cover_letter_draft.md",
    "manuscript/nuclear_fusion_targeting_plan.md",
    "manuscript/nuclear_fusion_submission_asset_manifest.csv",
    "manuscript/nuclear_fusion_data_code_package_plan.md",
    "manuscript/nuclear_fusion_repro_package_readme.md",
    "manuscript/nuclear_fusion_final_upload_checklist.md",
    "manuscript/nuclear_fusion_author_info_template.md",
    "manuscript/nuclear_fusion_submission_cover_sheet.md",
    "manuscript/nuclear_fusion_submission_integrity_audit_20260601.md",
    "manuscript/nuclear_fusion_reviewer_response_prebuttal.md",
    "docs/nuclear_fusion_enhancement_execution_plan.md",
    "tables/pb006_seed_manifest.csv",
    "manuscript/figure_captions.md",
    "manuscript/references.bib",
    "tables/reference_crossref_audit_20260531.csv",
    "tables/single_pebble_calibration_target_evidence_summary.csv",
    "tables/single_pebble_model_ensemble_evidence_summary.csv",
    "tables/sp002_force_displacement_overlay_metrics.csv",
    "tables/sp002_single_pebble_fragment_visualization_summary.csv",
    "data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_thermo.csv",
    "data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_summary.csv",
    "data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_initial_stiffness.csv",
    "data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_fragments.csv",
    "data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_failure_metrics.csv",
    "tables/pb006_breakage_event_database.csv",
    "tables/pb006_breakage_event_database_summary.csv",
    "tables/pb006_1000_bed_a_stage_summary.csv",
    "tables/pb006_1000_orientation_sensitivity_metrics.csv",
    "tables/pb006_three_seed_packing_descriptors_cutoff1p02mm.csv",
    "tables/pb006_1000_seed02_packing_descriptors_cutoff1p02mm.csv",
    "simulations/pebble_bed/PB-006/in.pb006_proxy_settle.lmp",
    "simulations/pebble_bed/PB-006/in.pb006_bonded_initcheck.lmp",
    "simulations/pebble_bed/PB-006/in.pb006_bonded_compression_targeted_window_restartable.lmp",
    "simulations/pebble_bed/PB-006/data/bonded_template_metadata_500.csv",
    "simulations/pebble_bed/PB-006/data/bonded_template_metadata_1000.csv",
]


GLOBS = [
    "figures/main/fig1_workflow.pdf",
    "figures/sp002/single_pebble_calibration_evidence.pdf",
    "figures/sp002/sp002_force_displacement_overlay.pdf",
    "figures/sp002/single_pebble_fragment_morphology_paraview.png",
    "figures/sp002/single_pebble_fragment_particles.vtp",
    "figures/sp002/single_pebble_fragment_bonds.vtp",
    "figures/pb006/pb006_breakage_event_database.pdf",
    "figures/pb006/pb006_force_path_proxy.pdf",
    "figures/pb006/pb006_1000_0p15_three_stage_sequence.pdf",
    "figures/pb006/pb006_1000_orientation_sensitivity.pdf",
    "tables/pb006_seed02_overlap_force_proxy_*.csv",
    "tables/pb006_seed03_overlap_force_proxy_*.csv",
    "data/processed/PB-006-bonded-randompack-500-prod-0p20mm-primitivewall_breakage_events.csv",
    "data/processed/PB-006-bonded-randompack-500-prod-0p20mm-primitivewall_height_summary.csv",
    "data/processed/PB-006-bonded-randompack-500-prod-0p20mm-primitivewall_pebble_summary.csv",
    "data/processed/PB-006-bonded-randompack-500-prod-0p20mm-primitivewall_per_pebble_series.csv",
    "data/processed/PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall_breakage_events.csv",
    "data/processed/PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall_height_summary.csv",
    "data/processed/PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall_pebble_summary.csv",
    "data/processed/PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall_per_pebble_series.csv",
    "data/processed/PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall_breakage_events.csv",
    "data/processed/PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall_height_summary.csv",
    "data/processed/PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall_pebble_summary.csv",
    "data/processed/PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall_per_pebble_series.csv",
    "data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable_*.csv",
    "data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_*.csv",
    "data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_breakage_events.csv",
    "data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_height_summary.csv",
    "data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_pebble_summary.csv",
    "data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_per_pebble_series.csv",
    "data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_thermo.csv",
    "simulations/pebble_bed/PB-006/data/proxy_centers_500*.csv",
    "simulations/pebble_bed/PB-006/data/proxy_centers_1000*.csv",
]


SCRIPTS = [
    "scripts/generate_bonded_sphere.py",
    "scripts/generate_weak_plane_template.py",
    "scripts/export_liggghts_multiplespheres.py",
    "scripts/generate_bonded_bed_from_centers.py",
    "scripts/run_sp002_weakplane_case.sh",
    "scripts/run_sp002_weakplane_orientation_case.sh",
    "scripts/run_pb006_proxy_settle.sh",
    "scripts/run_pb006_bonded_initcheck.sh",
    "scripts/run_pb006_bonded_compression_targeted_window_restartable.sh",
    "scripts/extract_liggghts_thermo.py",
    "scripts/analyze_bed_breakage_events.py",
    "scripts/summarize_random_pack_breakage.py",
    "scripts/build_pb006_event_database.py",
    "scripts/analyze_pb006_packing_descriptors.py",
    "scripts/analyze_pb006_overlap_force_network.py",
    "scripts/plot_main_workflow_figure.py",
    "scripts/plot_single_pebble_calibration_evidence.py",
    "scripts/plot_sp002_force_displacement_overlay.py",
    "scripts/export_sp002_fragment_vtp.py",
    "scripts/render_sp002_fragment_paraview.py",
    "scripts/plot_pb006_event_database.py",
    "scripts/plot_pb006_1000_0p15_sequence.py",
    "scripts/plot_pb006_1000_orientation_sensitivity.py",
    "scripts/plot_pb006_overlap_force_proxy.py",
    "scripts/build_nuclear_fusion_latex.py",
    "scripts/build_nuclear_fusion_repro_package.py",
]


def collect_files() -> list[Path]:
    paths: set[Path] = set()
    for rel in EXACT_FILES + SCRIPTS:
        p = ROOT / rel
        if p.exists():
            paths.add(p)
    for pattern in GLOBS:
        for p in ROOT.glob(pattern):
            if p.is_file():
                paths.add(p)
    return sorted(paths)


def copy_package(paths: list[Path], outdir: Path) -> None:
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    for src in paths:
        rel = src.relative_to(ROOT)
        dst = outdir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(paths: list[Path], outdir: Path, checksums: bool = False) -> Path:
    manifest = outdir / "MANIFEST.csv"
    with manifest.open("w", newline="") as f:
        writer = csv.writer(f)
        header = ["relative_path", "bytes"]
        if checksums:
            header.append("sha256")
        writer.writerow(header)
        for src in paths:
            rel = src.relative_to(ROOT)
            row = [rel.as_posix(), src.stat().st_size]
            if checksums:
                row.append(sha256(src))
            writer.writerow(row)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        default="submission_packages/nuclear_fusion_repro_package",
        help="Package output directory relative to the project root.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--checksums", action="store_true", help="Add SHA-256 checksums to MANIFEST.csv.")
    args = parser.parse_args()

    paths = collect_files()
    missing = [rel for rel in EXACT_FILES + SCRIPTS if not (ROOT / rel).exists()]
    if missing:
        print("Missing exact files:")
        for rel in missing:
            print(f"  {rel}")
    print(f"Collected {len(paths)} files")
    print(f"Total bytes: {sum(p.stat().st_size for p in paths)}")

    if args.dry_run:
        for p in paths:
            print(p.relative_to(ROOT).as_posix())
        return

    outdir = ROOT / args.outdir
    copy_package(paths, outdir)
    manifest = write_manifest(paths, outdir, checksums=args.checksums)
    print(f"Wrote package: {outdir}")
    print(f"Wrote manifest: {manifest}")


if __name__ == "__main__":
    main()
