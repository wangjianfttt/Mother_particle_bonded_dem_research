#!/usr/bin/env python3
"""Verify the public JNM reproducibility package."""

from __future__ import annotations

import csv
import hashlib
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "journal_of_nuclear_materials_reproducibility_package"
PACKAGE_DIR = ROOT / "submission_packages" / PACKAGE_NAME
PACKAGE_ZIP = ROOT / "submission_packages" / f"{PACKAGE_NAME}.zip"
PACKAGE_SHA = ROOT / "submission_packages" / f"{PACKAGE_NAME}.zip.sha256"
MANIFEST = PACKAGE_DIR / "MANIFEST.csv"

REQUIRED_MEMBERS = {
    "README.md",
    "MANIFEST.csv",
    "manuscript/journal_of_nuclear_materials_submission.pdf",
    "manuscript/journal_of_nuclear_materials_submission_draft.md",
    "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv",
    "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
    "figures/main/journal_of_nuclear_materials_graphical_abstract.png",
    "figures/pb007/pb007_corrected_fracture_sequence.pdf",
    "figures/pb007/pb007_replicate_comparison.pdf",
    "figures/sp002/jnm_single_pebble_validation.pdf",
    "tables/pb007_macro_topology_event_metrics.csv",
    "data/processed/pb007_replicate_comparison_source_data.csv",
    "simulations/single_pebble/templates/sp_500_d1mm_nooverlap/particles.csv",
    "simulations/single_pebble/templates/sp_500_d1mm_nooverlap/bonds.csv",
    "simulations/single_pebble/SP-002/in.plate_compression_weakplane.lmp",
    "simulations/pebble_bed/PB-007/in.pb007_bonded_step_relaxed_validation.lmp",
    "scripts/build_jnm_public_repro_package.py",
    "scripts/check_jnm_public_repro_package.py",
    "scripts/check_jnm_reader_facing_hygiene.py",
    "scripts/check_jnm_no_fake_repository_identifier.py",
    "scripts/check_jnm_scientific_storyline.py",
    "scripts/check_jnm_material_degradation_state_variables.py",
    "scripts/check_jnm_objective_completion_audit.py",
    "docs/jnm_scientific_storyline_audit_20260613.md",
    "docs/jnm_material_degradation_state_variables_audit_20260613.md",
    "docs/jnm_objective_completion_audit_20260613.md",
}

FORBIDDEN_PATH_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"cover_letter",
        r"author_declaration",
        r"author_metadata",
        r"elsevier_declarations",
        r"editorial_manager",
        r"reviewer_risk",
        r"resubmission",
        r"nuclear_fusion",
        r"jnm_final_submission_gate_report",
        r"journal_of_nuclear_materials_submission_package\.zip",
        r"journal_of_nuclear_materials_flat_source\.zip",
    ]
]

LOCAL_PATH_PATTERNS = [
    re.compile(r"/Users/wangjian"),
    re.compile(r"Documents/颗粒破碎统计研究"),
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> int:
    print("FAIL public reproducibility package: " + message)
    return 1


def check_manifest() -> list[str]:
    if not MANIFEST.exists():
        raise RuntimeError(f"missing {MANIFEST}")
    rows = list(csv.DictReader(MANIFEST.open()))
    if not rows:
        raise RuntimeError("manifest has no data rows")
    listed = {row["path"] for row in rows}
    actual = {
        path.relative_to(PACKAGE_DIR).as_posix()
        for path in PACKAGE_DIR.rglob("*")
        if path.is_file() and path.name != "MANIFEST.csv"
    }
    missing = sorted(actual - listed)
    stale = sorted(listed - actual)
    if missing or stale:
        raise RuntimeError(f"manifest mismatch; missing={missing[:8]}, stale={stale[:8]}")
    for row in rows:
        path = PACKAGE_DIR / row["path"]
        if int(row["size_bytes"]) != path.stat().st_size:
            raise RuntimeError(f"size mismatch for {row['path']}")
        if row["sha256"] != sha256(path):
            raise RuntimeError(f"sha256 mismatch for {row['path']}")
    return sorted(listed | {"MANIFEST.csv"})


def check_checksum() -> None:
    if not PACKAGE_ZIP.exists() or not PACKAGE_SHA.exists():
        raise RuntimeError("missing package zip or checksum")
    parts = PACKAGE_SHA.read_text().strip().split()
    if len(parts) < 2:
        raise RuntimeError("malformed checksum file")
    expected_hash, expected_name = parts[0], Path(parts[1]).name
    if expected_name != PACKAGE_ZIP.name:
        raise RuntimeError(f"checksum points to {expected_name}, expected {PACKAGE_ZIP.name}")
    actual_hash = sha256(PACKAGE_ZIP)
    if expected_hash != actual_hash:
        raise RuntimeError("zip checksum mismatch")


def check_zip(members: list[str]) -> None:
    with zipfile.ZipFile(PACKAGE_ZIP) as archive:
        zip_names = set(archive.namelist())
    expected = {f"{PACKAGE_NAME}/{member}" for member in members}
    missing = sorted(expected - zip_names)
    if missing:
        raise RuntimeError("zip missing members " + ", ".join(missing[:12]))


def check_required(members: list[str]) -> None:
    missing = sorted(member for member in REQUIRED_MEMBERS if member not in members)
    if missing:
        raise RuntimeError("missing required members " + ", ".join(missing))


def check_forbidden(members: list[str]) -> None:
    hits = [
        member
        for member in members
        if any(pattern.search(member) for pattern in FORBIDDEN_PATH_PATTERNS)
    ]
    if hits:
        raise RuntimeError("forbidden internal files present " + ", ".join(hits[:20]))


def check_local_paths() -> None:
    hits: list[str] = []
    for path in PACKAGE_DIR.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if "re.compile" in line and "/Users/wangjian" in line:
                continue
            if any(pattern.search(line) for pattern in LOCAL_PATH_PATTERNS):
                hits.append(f"{path.relative_to(PACKAGE_DIR)}:{line_no}")
    if hits:
        raise RuntimeError("local absolute paths present " + ", ".join(hits[:20]))


def main() -> int:
    if not PACKAGE_DIR.exists():
        return fail(f"missing folder {PACKAGE_DIR}")
    try:
        members = check_manifest()
        check_required(members)
        check_forbidden(members)
        check_local_paths()
        check_checksum()
        check_zip(members)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))
    print(
        "PASS public reproducibility package: "
        f"{len(members)} files, manifest, checksum, representative inputs and public-file hygiene verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
