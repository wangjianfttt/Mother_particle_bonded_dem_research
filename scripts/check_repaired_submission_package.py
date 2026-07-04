#!/usr/bin/env python3
"""Check the repaired target-neutral submission and upload packages."""

from __future__ import annotations

import csv
import hashlib
import zipfile
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission_packages"
UPLOAD_DIR = OUT / "repaired_editorial_upload_ready"
SUPPORT_DIR = OUT / "repaired_submission_package"
UPLOAD_ZIP = OUT / "repaired_editorial_upload_ready.zip"
SUPPORT_ZIP = OUT / "repaired_submission_package.zip"

REQUIRED_UPLOAD = {
    "01_manuscript.pdf",
    "02_highlights.docx",
    "03_graphical_abstract.png",
    "03_graphical_abstract.tiff",
    "03_graphical_abstract.pdf",
    "03_graphical_abstract.svg",
    "04_declaration_of_competing_interest.docx",
    "05_cover_letter.docx",
    "06_author_emails_and_contributions.docx",
    "README_upload_roles.txt",
    "MANIFEST.csv",
}

REQUIRED_SUPPORT = {
    "README.md",
    "MANIFEST.csv",
    "docs/cpm_literature_gap_map_20260704.csv",
    "docs/cpm_literature_gap_map_20260704.md",
    "docs/cpm_official_submission_guide_alignment_20260704.csv",
    "docs/cpm_official_submission_guide_alignment_20260704.md",
    "docs/cpm_material_response_summary_20260704.csv",
    "docs/cpm_material_response_summary_20260704.md",
    "docs/cpm_reviewer_risk_preflight_20260704.csv",
    "docs/cpm_reviewer_risk_preflight_20260704.md",
    "docs/cpm_live_submission_packet_20260704.csv",
    "docs/cpm_live_submission_packet_20260704.json",
    "docs/cpm_live_submission_packet_20260704.md",
    "docs/cpm_live_submission_packet_docx_qa_20260704.md",
    "manuscript/repaired_full_submission.pdf",
    "manuscript/repaired_full_submission.tex",
    "manuscript/repaired_full_submission_draft.md",
    "manuscript/repaired_full_manuscript_source_data_matrix.csv",
    "manuscript/repaired_cover_letter_draft.md",
    "manuscript/repaired_highlights.md",
    "manuscript/repaired_declaration_of_competing_interest.md",
    "manuscript/computational_particle_mechanics_live_submission_packet.docx",
    "figures/apt_redesign/fig5_mechanism_state_space.svg",
    "figures/pb007/pb007_material_strength_response.svg",
    "data/figure_source/pb007_material_strength_response.csv",
    "scripts/build_cpm_literature_gap_map.py",
    "scripts/build_cpm_official_submission_guide_alignment.py",
    "scripts/build_cpm_blinded_review_package.py",
    "scripts/build_cpm_material_response_summary.py",
    "scripts/build_cpm_reviewer_risk_preflight.py",
    "scripts/build_cpm_submission_readiness_report.py",
    "scripts/build_cpm_live_submission_packet.py",
    "scripts/check_cpm_reviewer_risk_preflight.py",
    "scripts/check_cpm_scientific_alignment.py",
    "scripts/build_repaired_full_latex.py",
    "scripts/build_repaired_submission_package.py",
    "scripts/check_repaired_submission_package.py",
}

FORBIDDEN_VISIBLE = [
    "Journal of Nuclear Materials",
    "Nuclear Fusion",
    "Advanced Powder Technology",
    "ADVPT-D",
    "JNUMA-D",
    "scientific weakness",
    "do not provide",
    "No converged",
    "diagnostic",
    "audit",
    "gate",
    "CAL",
    "SP-002",
    "PB-007",
    "seed",
]

FORBIDDEN_SOURCE_TEXT = [
    "Journal of Nuclear Materials",
    "Nuclear Fusion",
    "Advanced Powder Technology",
    "ADVPT-D",
    "JNUMA-D",
    "scientific weakness",
    "do not provide",
    "No converged",
    "diagnostic",
    "audit",
    "gate",
]

TEXT_SUFFIXES = {".md", ".txt", ".csv", ".svg", ".tex"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_manifest(directory: Path, failures: list[str]) -> None:
    manifest = directory / "MANIFEST.csv"
    if not manifest.exists():
        failures.append(f"missing manifest: {manifest}")
        return
    with manifest.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        path = directory / row["path"]
        if not path.exists():
            failures.append(f"manifest path missing: {row['path']}")
            continue
        if str(path.stat().st_size) != row["bytes"]:
            failures.append(f"manifest byte mismatch: {row['path']}")
        if sha256(path) != row["sha256"]:
            failures.append(f"manifest sha256 mismatch: {row['path']}")


def check_zip(zip_path: Path, failures: list[str]) -> None:
    if not zip_path.exists():
        failures.append(f"missing zip: {zip_path}")
        return
    sha_path = zip_path.with_suffix(zip_path.suffix + ".sha256")
    if not sha_path.exists():
        failures.append(f"missing sha256 file: {sha_path}")
    else:
        recorded = sha_path.read_text(encoding="utf-8").split()[0]
        actual = sha256(zip_path)
        if recorded != actual:
            failures.append(f"zip sha256 mismatch: {zip_path.name}")
    with zipfile.ZipFile(zip_path) as zf:
        bad = zf.testzip()
        if bad:
            failures.append(f"zip corrupt member: {bad}")


def check_required(directory: Path, required: set[str], failures: list[str]) -> None:
    for rel in sorted(required):
        if not (directory / rel).exists():
            failures.append(f"required file missing in {directory.name}: {rel}")


def check_pdf(failures: list[str]) -> None:
    pdf = UPLOAD_DIR / "01_manuscript.pdf"
    if not pdf.exists():
        failures.append("upload manuscript PDF missing")
        return
    reader = PdfReader(str(pdf))
    if len(reader.pages) != 18:
        failures.append(f"unexpected upload PDF page count: {len(reader.pages)}")


def check_visible_text(directory: Path, failures: list[str], forbidden: list[str] = FORBIDDEN_VISIBLE) -> None:
    for path in directory.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(directory)
        for term in forbidden:
            if term in text:
                failures.append(f"forbidden term {term!r} in {rel}")


def check_cpm_support_summary(failures: list[str]) -> None:
    summary = SUPPORT_DIR / "docs" / "cpm_material_response_summary_20260704.md"
    if not summary.exists():
        failures.append("missing CPM material-response summary")
        return
    text = summary.read_text(encoding="utf-8")
    required_phrases = [
        "11 completed endpoints",
        "6 strength-reduction rows",
        "first localized bond loss advances from 39 to 19 micrometres",
        "minimum cracking force sum 0.575 N / maximum zero-loss force sum 0.253 N = 2.28",
        "all 11 material-response endpoints retain a spanning final native force graph",
    ]
    for phrase in required_phrases:
        if phrase not in text:
            failures.append(f"CPM support summary missing phrase: {phrase}")


def main() -> None:
    failures: list[str] = []
    check_required(UPLOAD_DIR, REQUIRED_UPLOAD, failures)
    check_required(SUPPORT_DIR, REQUIRED_SUPPORT, failures)
    check_manifest(UPLOAD_DIR, failures)
    check_manifest(SUPPORT_DIR, failures)
    check_zip(UPLOAD_ZIP, failures)
    check_zip(SUPPORT_ZIP, failures)
    check_pdf(failures)
    check_cpm_support_summary(failures)
    # Upload files are reader-facing. Support package is checked only for current
    # repaired materials and source-data exports, not historical scripts.
    check_visible_text(UPLOAD_DIR, failures)
    check_visible_text(SUPPORT_DIR / "manuscript", failures)
    check_visible_text(SUPPORT_DIR / "figures", failures)
    check_visible_text(SUPPORT_DIR / "data" / "figure_source", failures, FORBIDDEN_SOURCE_TEXT)
    if failures:
        raise SystemExit("FAIL repaired submission package check:\n- " + "\n- ".join(failures))
    print("PASS repaired submission package check")
    print(f"upload_files={len(list(UPLOAD_DIR.rglob('*')))} support_files={len(list(SUPPORT_DIR.rglob('*')))}")
    print(f"upload_zip={UPLOAD_ZIP} support_zip={SUPPORT_ZIP}")


if __name__ == "__main__":
    main()
