#!/usr/bin/env python3
"""Check the Computational Particle Mechanics upload package."""

from __future__ import annotations

import csv
import hashlib
import json
import os
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
BLINDED_ZIP = ROOT / "submission_packages" / "computational_particle_mechanics_blinded_review_optional.zip"
BLINDED_SHA = ROOT / "submission_packages" / "computational_particle_mechanics_blinded_review_optional.zip.sha256"
CPM_TEX = ROOT / "manuscript" / "computational_particle_mechanics_submission.tex"
COVER_LETTER = ROOT / "manuscript" / "computational_particle_mechanics_cover_letter.md"
CPM_FIELDS = ROOT / "manuscript" / "computational_particle_mechanics_editorial_fields.md"
CPM_HIGHLIGHTS = ROOT / "manuscript" / "computational_particle_mechanics_highlights.md"
OFFICIAL_GUIDE = ROOT / "docs" / "cpm_official_submission_guide_alignment_20260704.md"
GOAL_AUDIT_JSON = ROOT / "docs" / "cpm_goal_completion_audit_20260704.json"
README = ROOT / "README_CPM_SUBMISSION_20260704.md"
START_HERE = ROOT / "START_HERE_CPM_SUBMISSION.md"
LIVE_PACKET_DOCX = ROOT / "manuscript" / "computational_particle_mechanics_live_submission_packet.docx"
LIVE_PACKET_MD = ROOT / "docs" / "cpm_live_submission_packet_20260704.md"
LIVE_PACKET_CSV = ROOT / "docs" / "cpm_live_submission_packet_20260704.csv"
LIVE_PACKET_JSON = ROOT / "docs" / "cpm_live_submission_packet_20260704.json"
EMAIL_LOOKUP_MD = ROOT / "docs" / "cpm_author_email_public_lookup_20260704.md"
EMAIL_LOOKUP_CSV = ROOT / "docs" / "cpm_author_email_public_lookup_20260704.csv"
SUPPORT_DOCX = [
    ROOT / "manuscript" / "computational_particle_mechanics_author_email_collection_packet.docx",
    ROOT / "manuscript" / "computational_particle_mechanics_coauthor_email_request_zh_en.docx",
    ROOT / "manuscript" / "computational_particle_mechanics_live_submission_checklist.docx",
    LIVE_PACKET_DOCX,
]
SUPPORT_TEXT = [
    ROOT / "manuscript" / "computational_particle_mechanics_author_email_collection_packet.csv",
    ROOT / "manuscript" / "computational_particle_mechanics_author_email_collection_packet.md",
    ROOT / "manuscript" / "computational_particle_mechanics_author_email_collection_packet.txt",
    ROOT / "manuscript" / "computational_particle_mechanics_coauthor_email_request_zh_en.txt",
    ROOT / "manuscript" / "computational_particle_mechanics_live_submission_checklist.md",
    LIVE_PACKET_MD,
    LIVE_PACKET_CSV,
    EMAIL_LOOKUP_MD,
    EMAIL_LOOKUP_CSV,
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

BLINDED_FORBIDDEN_TERMS = [
    "Jian Wang",
    "Siyu Wang",
    "Hang Zhang",
    "Ming-Zhun Lei",
    "Wei Wen",
    "Qi-Gang Wu",
    "Gang Shen",
    "Haishun Deng",
    "wjfttt@mail.ustc.edu.cn",
    "Anhui University of Science and Technology",
    "Institute of Plasma Physics",
    "Chinese Academy of Sciences",
    "10.5281/zenodo.20687351",
    "wangjianfttt",
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


def check_abstract_word_count() -> None:
    text = CPM_TEX.read_text(encoding="utf-8")
    match = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, re.S)
    if not match:
        fail("manuscript TeX missing abstract environment")
    abstract = match.group(1)
    abstract = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", lambda item: item.group(1) or "", abstract)
    abstract = re.sub(r"[{}$]", " ", abstract)
    words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", abstract)
    if len(words) > 250:
        fail(f"abstract exceeds CPM 250-word guide limit: {len(words)} words")


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
        "computational_particle_mechanics_author_email_collection_packet.docx",
        "computational_particle_mechanics_blinded_review_optional.zip",
        "computational_particle_mechanics_live_submission_packet.docx",
        "cpm_live_submission_packet_20260704.md",
        "cpm_author_email_public_lookup_20260704.md",
        "cpm_official_submission_guide_alignment_20260704.md",
        "scripts/check_computational_particle_mechanics_submission_package.py",
        "10.5281/zenodo.20687351",
        "Four public candidate e-mail records",
        "confirmation aids only",
        "Reduced reproducibility package CPM support members: `30/30` present",
    ]:
        if required not in start:
            fail(f"START_HERE missing {required}")
    if not LIVE_PACKET_JSON.exists():
        fail("missing live-submission packet JSON")
    coauthor_request = (
        ROOT / "manuscript" / "computational_particle_mechanics_coauthor_email_request_zh_en.txt"
    ).read_text(encoding="utf-8")
    for term in [
        "leimz@ipp.ac.cn",
        "wenwei@ipp.ac.cn",
        "shenganghit@163.com",
        "269469122@qq.com",
        "未确认前直接填入投稿系统",
        "before author confirmation",
    ]:
        if term not in coauthor_request:
            fail(f"coauthor e-mail request missing confirmation term: {term}")
    collection_packet = (
        ROOT / "manuscript" / "computational_particle_mechanics_author_email_collection_packet.md"
    ).read_text(encoding="utf-8")
    for term in [
        "Copy-ready short message",
        "Siyu Wang",
        "Hang Zhang",
        "Qi-Gang Wu",
        "Public candidates are confirmation aids only",
    ]:
        if term not in collection_packet:
            fail(f"author e-mail collection packet missing term: {term}")
    payload = json.loads(LIVE_PACKET_JSON.read_text(encoding="utf-8"))
    for key, value in [
        ("target_journal", "Computational Particle Mechanics"),
        ("submission_route", "ScienceDirect / Editorial Manager live submission route"),
        ("upload_package", "submission_packages/computational_particle_mechanics_upload_ready.zip"),
        ("optional_blinded_package", "submission_packages/computational_particle_mechanics_blinded_review_optional.zip"),
        ("reduced_reproducibility_package", "submission_packages/repaired_submission_package.zip"),
        ("missing_email_count", 7),
    ]:
        if payload.get(key) != value:
            fail(f"live-submission packet JSON mismatch for {key}")
    if payload.get("candidate_email_lookup") != "docs/cpm_author_email_public_lookup_20260704.md":
        fail("live-submission packet JSON missing candidate e-mail lookup")
    if payload.get("candidate_email_count") != 4:
        fail("expected four public candidate e-mails for confirmation")


def check_official_guide_alignment() -> None:
    if not OFFICIAL_GUIDE.exists():
        fail("missing official submission-guide alignment report")
    text = OFFICIAL_GUIDE.read_text(encoding="utf-8")
    required = [
        "ScienceDirect Guide for Authors",
        "Springer transition notice",
        "Double-anonymized review",
        "Abstract length",
        "not exceed 250 words",
        "ready_if_requested",
        "optional live-system support",
        "computational_particle_mechanics_blinded_review_optional.zip",
        "external_metadata_pending",
    ]
    for term in required:
        if term not in text:
            fail(f"official guide alignment report missing {term!r}")
    forbidden = [
        "highlights are required for this journal family workflow",
    ]
    for term in forbidden:
        if term in text:
            fail(f"official guide alignment retains unsupported requirement wording: {term}")


def check_goal_completion_audit() -> None:
    if not GOAL_AUDIT_JSON.exists():
        fail("missing goal-level completion audit JSON")
    payload = json.loads(GOAL_AUDIT_JSON.read_text(encoding="utf-8"))
    if payload.get("overall_status") != "ready_after_external_author_metadata":
        fail("goal-level completion audit does not record the correct external-metadata boundary")
    rows = payload.get("rows", [])
    statuses = {row.get("requirement"): row.get("status") for row in rows if isinstance(row, dict)}
    if statuses.get("External author metadata for live system") != "external_pending":
        fail("goal-level completion audit missing external author-metadata pending status")
    if payload.get("large_raw_residue_count") != 0:
        fail("goal-level completion audit reports remaining large raw dump/restart residues")


def check_blinded_review_package() -> None:
    check_sha_file(BLINDED_ZIP, BLINDED_SHA)
    names = check_zip(BLINDED_ZIP)
    required = {
        "computational_particle_mechanics_blinded_review_optional/01_blinded_manuscript.pdf",
        "computational_particle_mechanics_blinded_review_optional/01_blinded_manuscript.tex",
        "computational_particle_mechanics_blinded_review_optional/README_blinded_review_optional.txt",
        "computational_particle_mechanics_blinded_review_optional/references.bib",
    }
    missing = sorted(required - set(names))
    if missing:
        fail(f"blinded-review zip missing files: {missing}")
    with zipfile.ZipFile(BLINDED_ZIP) as zf:
        tex = zf.read("computational_particle_mechanics_blinded_review_optional/01_blinded_manuscript.tex").decode("utf-8", errors="ignore")
    found = [term for term in BLINDED_FORBIDDEN_TERMS if term in tex]
    if found:
        fail(f"blinded manuscript source still contains identifying terms: {found}")


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
    check_abstract_word_count()
    check_reader_text()
    check_doi_and_target()
    check_support_docs()
    check_official_guide_alignment()
    if os.environ.get("CPM_SKIP_GOAL_AUDIT") != "1":
        check_goal_completion_audit()
    check_blinded_review_package()
    check_scientific_alignment()
    check_reviewer_risk_preflight()
    print("PASS CPM submission package: manifest=15, figures=19, docx=9, DOI, guide alignment, live packet and optional blinded package verified")


if __name__ == "__main__":
    main()
