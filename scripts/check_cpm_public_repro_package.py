#!/usr/bin/env python3
"""Verify the public CPM reproducibility package."""

from __future__ import annotations

import csv
import hashlib
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "computational_particle_mechanics_public_reproducibility_package"
PACKAGE_ROOT_MODE = (ROOT / "MANIFEST.csv").exists()
PACKAGE_DIR = ROOT if PACKAGE_ROOT_MODE else ROOT / "submission_packages" / PACKAGE_NAME
PACKAGE_ZIP = ROOT / "submission_packages" / f"{PACKAGE_NAME}.zip"
PACKAGE_SHA = ROOT / "submission_packages" / f"{PACKAGE_NAME}.zip.sha256"
MANIFEST = PACKAGE_DIR / "MANIFEST.csv"

REQUIRED_MEMBERS = {
    "README.md",
    "CITATION.cff",
    "MANIFEST.csv",
    "manuscript/computational_particle_mechanics_submission.pdf",
    "manuscript/computational_particle_mechanics_submission.tex",
    "manuscript/computational_particle_mechanics_blinded_submission.pdf",
    "manuscript/repaired_full_manuscript_source_data_matrix.csv",
    "manuscript/repaired_manuscript_claim_evidence_matrix.csv",
    "docs/cpm_goal_completion_audit_20260704.md",
    "docs/cpm_final_readthrough_qa_20260708.md",
    "data/figure_source/pb007_material_strength_response.csv",
    "data/processed/pb007_replicate_comparison_source_data.csv",
    "tables/pb007_material_parameter_response.csv",
    "tables/pb007_macro_topology_event_metrics.csv",
    "tables/pb007_strong_force_tail_state_metrics.csv",
    "figures/main/fig1_workflow.svg",
    "figures/apt_redesign/fig2_single_pebble_template_validation.svg",
    "figures/apt_redesign/fig3_entry_state_validation.svg",
    "figures/apt_redesign/fig4_pilot_fracture_event_sequence.svg",
    "figures/pb007/pb007_replicate_comparison.svg",
    "figures/pb007/pb007_material_strength_response.svg",
    "simulations/single_pebble/SP-002/in.plate_compression_weakplane.lmp",
    "simulations/single_pebble/SP-RESOLUTION/templates/sp_500_d1mm_nooverlap/particles.csv",
    "simulations/single_pebble/SP-RESOLUTION/templates/sp_500_d1mm_nooverlap/bonds.csv",
    "simulations/pebble_bed/PB-007/in.pb007_bonded_step_relaxed_validation.lmp",
    "scripts/build_cpm_public_repro_package.py",
    "scripts/check_cpm_public_repro_package.py",
    "scripts/check_cpm_final_readthrough.py",
    "scripts/check_computational_particle_mechanics_submission_package.py",
    "scripts/summarize_pb007_strong_force_retention.py",
}

FORBIDDEN_PATH_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"cover_letter",
        r"declaration_of_competing_interest",
        r"author_email",
        r"coauthor_email",
        r"individual_contact",
        r"live_submission",
        r"editorial_upload",
        r"reviewer_risk",
        r"response_to_review",
        r"rebuttal",
    ]
]

LOCAL_PATH_PATTERNS = [
    re.compile(r"/Users/wangjian"),
    re.compile(r"Documents/颗粒破碎统计研究"),
]

TEXT_SUFFIXES = {".bib", ".csv", ".json", ".lmp", ".md", ".py", ".sh", ".tex", ".txt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> int:
    print("FAIL CPM public reproducibility package: " + message)
    return 1


def check_manifest() -> list[str]:
    if not MANIFEST.exists():
        raise RuntimeError(f"missing {MANIFEST}")
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8")))
    if not rows:
        raise RuntimeError("manifest has no data rows")
    listed = {row["path"] for row in rows}
    actual = {
        path.relative_to(PACKAGE_DIR).as_posix()
        for path in PACKAGE_DIR.rglob("*")
        if path.is_file() and path.name != "MANIFEST.csv" and ".git" not in path.relative_to(PACKAGE_DIR).parts
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


def check_required(members: list[str]) -> None:
    missing = sorted(member for member in REQUIRED_MEMBERS if member not in members)
    if missing:
        raise RuntimeError("missing required members " + ", ".join(missing))


def check_forbidden_paths(members: list[str]) -> None:
    hits = [
        member
        for member in members
        if any(pattern.search(member) for pattern in FORBIDDEN_PATH_PATTERNS)
    ]
    if hits:
        raise RuntimeError("private/editorial files present " + ", ".join(hits[:20]))


def check_local_paths() -> None:
    hits: list[str] = []
    for path in PACKAGE_DIR.rglob("*"):
        if ".git" in path.relative_to(PACKAGE_DIR).parts:
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if "re.compile" in line and "/Users/wangjian" in line:
                continue
            if "re.compile" in line and "Documents/颗粒破碎统计研究" in line:
                continue
            if any(pattern.search(line) for pattern in LOCAL_PATH_PATTERNS):
                hits.append(f"{path.relative_to(PACKAGE_DIR)}:{line_no}")
    if hits:
        raise RuntimeError("local absolute paths present " + ", ".join(hits[:20]))


def check_checksum() -> None:
    if not PACKAGE_ZIP.exists() or not PACKAGE_SHA.exists():
        raise RuntimeError("missing package zip or checksum")
    parts = PACKAGE_SHA.read_text(encoding="utf-8").strip().split()
    if len(parts) < 2:
        raise RuntimeError("malformed checksum file")
    expected_hash, expected_name = parts[0], Path(parts[1]).name
    if expected_name != PACKAGE_ZIP.name:
        raise RuntimeError(f"checksum points to {expected_name}, expected {PACKAGE_ZIP.name}")
    if expected_hash != sha256(PACKAGE_ZIP):
        raise RuntimeError("zip checksum mismatch")


def check_zip(members: list[str]) -> None:
    with zipfile.ZipFile(PACKAGE_ZIP) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"zip corrupt member: {bad}")
        zip_names = set(archive.namelist())
    expected = {f"{PACKAGE_NAME}/{member}" for member in members}
    missing = sorted(expected - zip_names)
    if missing:
        raise RuntimeError("zip missing members " + ", ".join(missing[:12]))


def main() -> int:
    if not PACKAGE_DIR.exists():
        return fail(f"missing folder {PACKAGE_DIR}")
    try:
        members = check_manifest()
        check_required(members)
        check_forbidden_paths(members)
        check_local_paths()
        if not PACKAGE_ROOT_MODE:
            check_checksum()
            check_zip(members)
    except Exception as exc:  # noqa: BLE001
        return fail(str(exc))
    checksum_note = ", checksum" if not PACKAGE_ROOT_MODE else ""
    print(
        "PASS CPM public reproducibility package: "
        f"{len(members)} files, manifest{checksum_note}, representative inputs and public-file hygiene verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
