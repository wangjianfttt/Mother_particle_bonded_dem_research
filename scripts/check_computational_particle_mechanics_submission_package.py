#!/usr/bin/env python3
"""Check the Computational Particle Mechanics upload package."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    from docx import Document
except ImportError as exc:  # pragma: no cover - environment message
    raise SystemExit(
        "python-docx is required. Use the bundled Codex Python runtime for this check."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
UPLOAD_DIR = ROOT / "submission_packages" / "computational_particle_mechanics_upload_ready"
UPLOAD_ZIP = ROOT / "submission_packages" / "computational_particle_mechanics_upload_ready.zip"
UPLOAD_SHA = Path(str(UPLOAD_ZIP) + ".sha256")
REPRO_ZIP = ROOT / "submission_packages" / "repaired_submission_package.zip"
REPRO_SHA = ROOT / "submission_packages" / "repaired_submission_package.zip.sha256"
CPM_TEX = ROOT / "manuscript" / "computational_particle_mechanics_submission.tex"
COVER_LETTER = ROOT / "manuscript" / "computational_particle_mechanics_cover_letter.md"
CPM_FIELDS = ROOT / "manuscript" / "computational_particle_mechanics_editorial_fields.md"
CPM_HIGHLIGHTS = ROOT / "manuscript" / "computational_particle_mechanics_highlights.md"
README = ROOT / "README_CPM_SUBMISSION_20260704.md"
START_HERE = ROOT / "START_HERE_CPM_SUBMISSION.md"
SUPPORT_DOCX = [
    ROOT / "manuscript" / "computational_particle_mechanics_coauthor_email_request_zh_en.docx",
    ROOT / "manuscript" / "computational_particle_mechanics_live_submission_checklist.docx",
]
SUPPORT_TEXT = [
    ROOT / "manuscript" / "computational_particle_mechanics_coauthor_email_request_zh_en.txt",
    ROOT / "manuscript" / "computational_particle_mechanics_live_submission_checklist.md",
]

EXPECTED_UPLOAD_FILES = {
    "01_manuscript.pdf",
    "02_highlights.docx",
    "03_graphical_abstract.pdf",
    "03_graphical_abstract.png",
    "03_graphical_abstract.svg",
    "03_graphical_abstract.tiff",
    "04_declaration_of_competing_interest.docx",
    "05_cover_letter.docx",
    "06_author_emails_and_contributions.docx",
    "07_latex_source.zip",
    "08_editorial_submission_fields.docx",
    "09_main_figures.zip",
    "10_author_email_completion_sheet.docx",
    "10_author_email_completion_sheet.csv",
    "MANIFEST.csv",
    "README_upload_roles.txt",
}

DOCX_FILES = [
    "02_highlights.docx",
    "04_declaration_of_competing_interest.docx",
    "05_cover_letter.docx",
    "06_author_emails_and_contributions.docx",
    "08_editorial_submission_fields.docx",
    "10_author_email_completion_sheet.docx",
]

FORBIDDEN_READER_TERMS = re.compile(
    r"\b(audit|diagnostic|gate|however|therefore|rather than|not only|CAL|SP-00|PB-00|"
    r"Advanced Powder|Journal of Nuclear Materials|Nuclear Fusion)\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_sha_file(zip_path: Path, sha_path: Path) -> None:
    if not zip_path.exists():
        fail(f"missing zip: {zip_path}")
    if not sha_path.exists():
        fail(f"missing checksum: {sha_path}")
    expected = sha_path.read_text(encoding="utf-8").split()[0]
    actual = sha256(zip_path)
    if actual != expected:
        fail(f"checksum mismatch for {zip_path.name}")


def check_zip(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad is not None:
            fail(f"bad zip member in {path.name}: {bad}")
        return zf.namelist()


def check_manifest() -> list[dict[str, str]]:
    manifest = UPLOAD_DIR / "MANIFEST.csv"
    if not manifest.exists():
        fail("missing upload manifest")
    rows = list(csv.DictReader(manifest.open(encoding="utf-8")))
    if len(rows) != 15:
        fail(f"expected 15 upload manifest rows, found {len(rows)}")
    paths = {row["path"] for row in rows}
    required = EXPECTED_UPLOAD_FILES - {"MANIFEST.csv"}
    missing = sorted(required - paths)
    if missing:
        fail(f"manifest missing files: {missing}")
    for row in rows:
        path = UPLOAD_DIR / row["path"]
        if not path.exists():
            fail(f"manifest path missing on disk: {row['path']}")
        if str(path.stat().st_size) != row["bytes"]:
            fail(f"manifest byte count mismatch: {row['path']}")
        if sha256(path) != row["sha256"]:
            fail(f"manifest checksum mismatch: {row['path']}")
    return rows


def check_docx_files() -> None:
    for name in DOCX_FILES:
        Document(UPLOAD_DIR / name)


def check_nested_zips() -> None:
    latex_members = check_zip(UPLOAD_DIR / "07_latex_source.zip")
    if len(latex_members) != 9:
        fail(f"expected 9 LaTeX-source members, found {len(latex_members)}")
    if "manuscript/computational_particle_mechanics_submission.tex" not in latex_members:
        fail("LaTeX source zip missing target-specific TeX")

    figure_members = check_zip(UPLOAD_DIR / "09_main_figures.zip")
    if len(figure_members) != 19:
        fail(f"expected 19 main-figure members, found {len(figure_members)}")
    for stem in [
        "figures/main/fig1_workflow",
        "figures/apt_redesign/fig2_single_pebble_template_validation",
        "figures/apt_redesign/fig3_entry_state_validation",
        "figures/apt_redesign/fig4_pilot_fracture_event_sequence",
        "figures/apt_redesign/fig5_mechanism_state_space",
        "figures/pb007/pb007_material_strength_response",
    ]:
        for ext in [".pdf", ".png", ".svg"]:
            if stem + ext not in figure_members:
                fail(f"main figure zip missing {stem + ext}")


def check_author_email_sheet() -> None:
    sheet = UPLOAD_DIR / "10_author_email_completion_sheet.csv"
    rows = list(csv.DictReader(sheet.open(encoding="utf-8")))
    if len(rows) != 8:
        fail(f"expected 8 author rows, found {len(rows)}")
    missing = [row for row in rows if row["Status"] == "Missing"]
    if len(missing) != 7:
        fail(f"expected 7 missing coauthor e-mails, found {len(missing)}")
    if not any(row["Author"] == "Jian Wang" and row["Status"] == "Available" for row in rows):
        fail("corresponding author e-mail is not marked available")


def check_highlights() -> None:
    lines = [
        line.strip("- ").strip()
        for line in CPM_HIGHLIGHTS.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("-")
    ]
    if len(lines) != 5:
        fail(f"expected 5 highlights, found {len(lines)}")
    too_long = [(idx, len(text), text) for idx, text in enumerate(lines, 1) if len(text) > 85]
    if too_long:
        fail(f"highlight length exceeds 85 characters: {too_long}")


def check_reader_text() -> None:
    for path in [
        CPM_TEX,
        COVER_LETTER,
        CPM_FIELDS,
        CPM_HIGHLIGHTS,
        UPLOAD_DIR / "README_upload_roles.txt",
        README,
    ]:
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = FORBIDDEN_READER_TERMS.search(text)
        if match:
            fail(f"reader-facing residue {match.group(0)!r} in {path}")


def check_doi_and_target() -> None:
    text = CPM_TEX.read_text(encoding="utf-8")
    if "10.5281/zenodo.20687351" not in text:
        fail("manuscript TeX missing Zenodo DOI")
    if r"\journal{Computational Particle Mechanics}" not in text:
        fail("manuscript TeX missing target journal")
    fields = CPM_FIELDS.read_text(encoding="utf-8")
    if fields.count("10.5281/zenodo.20687351") < 2:
        fail("editorial fields missing DOI statements")


def check_support_docs() -> None:
    if not START_HERE.exists():
        fail("missing START_HERE_CPM_SUBMISSION.md")
    for path in SUPPORT_DOCX:
        if not path.exists():
            fail(f"missing support DOCX: {path.name}")
        Document(path)
    for path in SUPPORT_TEXT:
        if not path.exists() or path.stat().st_size == 0:
            fail(f"missing or empty support text file: {path.name}")
    start = START_HERE.read_text(encoding="utf-8")
    for required in [
        "computational_particle_mechanics_upload_ready.zip",
        "10_author_email_completion_sheet.docx",
        "scripts/check_computational_particle_mechanics_submission_package.py",
        "10.5281/zenodo.20687351",
    ]:
        if required not in start:
            fail(f"START_HERE missing {required}")


def check_scientific_alignment() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_cpm_scientific_alignment.py")],
        cwd=ROOT,
        check=True,
    )


def check_reviewer_risk_preflight() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_cpm_reviewer_risk_preflight.py")],
        cwd=ROOT,
        check=True,
    )


def main() -> None:
    check_sha_file(UPLOAD_ZIP, UPLOAD_SHA)
    check_sha_file(REPRO_ZIP, REPRO_SHA)
    check_zip(UPLOAD_ZIP)
    check_manifest()
    check_docx_files()
    check_nested_zips()
    check_author_email_sheet()
    check_highlights()
    check_reader_text()
    check_doi_and_target()
    check_support_docs()
    check_scientific_alignment()
    check_reviewer_risk_preflight()
    print("PASS CPM submission package: manifest=15, figures=19, docx=8, DOI and support docs verified")


if __name__ == "__main__":
    main()
