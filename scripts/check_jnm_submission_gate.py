#!/usr/bin/env python3
"""Check the Journal of Nuclear Materials submission package gate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import struct
import subprocess
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = ROOT / "docs/jnm_final_submission_gate_report.md"
REPORT_JSON = ROOT / "docs/jnm_final_submission_gate_report.json"


@dataclass
class Check:
    name: str
    status: str
    detail: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_sha_file(path: Path) -> tuple[str, str]:
    text = path.read_text().strip()
    digest, file_name = text.split(maxsplit=1)
    return digest, file_name


def check_file_exists(path: Path, label: str) -> Check:
    if not path.exists():
        return Check(label, "FAIL", f"Missing file: {path}")
    if path.is_file() and path.stat().st_size == 0:
        return Check(label, "FAIL", f"Empty file: {path}")
    return Check(label, "PASS", f"{path} ({path.stat().st_size} bytes)")


def check_csv_paths(path: Path, label: str) -> list[Check]:
    checks: list[Check] = [check_file_exists(path, label)]
    if checks[-1].status != "PASS":
        return checks
    rows = list(csv.DictReader(path.open()))
    if not rows:
        checks.append(Check(label, "FAIL", "CSV has no data rows"))
        return checks
    file_cols = [
        col
        for col in rows[0]
        if col in {"primary_file", "alternate_file", "alternate_or_source_file"}
    ]
    missing: list[str] = []
    for row in rows:
        for col in file_cols:
            value = (row.get(col) or "").strip()
            if value and not (ROOT / value).exists():
                missing.append(f"{row.get('item', '<item>')}:{col}={value}")
    if missing:
        checks.append(Check(label, "FAIL", "; ".join(missing)))
    else:
        checks.append(Check(label, "PASS", f"{len(rows)} rows; all referenced paths exist"))
    return checks


def check_log_clean(path: Path) -> Check:
    if not path.exists():
        return Check(f"log clean: {path.name}", "FAIL", f"Missing log: {path}")
    pattern = re.compile(
        r"undefined|Citation.*undefined|LaTeX Error|Emergency stop|Fatal error|There were undefined citations",
        re.IGNORECASE,
    )
    hits = [line.strip() for line in path.read_text(errors="replace").splitlines() if pattern.search(line)]
    if hits:
        return Check(f"log clean: {path.name}", "FAIL", " | ".join(hits[:8]))
    return Check(f"log clean: {path.name}", "PASS", "No unresolved citations or fatal LaTeX errors")


def check_checksum(zip_path: Path, sha_path: Path, label: str) -> Check:
    if not zip_path.exists() or not sha_path.exists():
        return Check(label, "FAIL", f"Missing zip or checksum: {zip_path}, {sha_path}")
    expected, _ = read_sha_file(sha_path)
    actual = sha256(zip_path)
    if expected != actual:
        return Check(label, "FAIL", f"Expected {expected}; actual {actual}")
    return Check(label, "PASS", f"{zip_path.name} checksum OK")


def check_zip_members(zip_path: Path, required: list[str]) -> Check:
    if not zip_path.exists():
        return Check("submission zip members", "FAIL", f"Missing zip: {zip_path}")
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    missing = [name for name in required if name not in names]
    if missing:
        return Check("submission zip members", "FAIL", "; ".join(missing))
    return Check("submission zip members", "PASS", f"{len(required)} required members present")


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Not a PNG file: {path}")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_graphical_abstract(path: Path) -> Check:
    if not path.exists():
        return Check("graphical abstract dimensions", "FAIL", f"Missing file: {path}")
    try:
        width, height = png_size(path)
    except Exception as exc:  # noqa: BLE001
        return Check("graphical abstract dimensions", "FAIL", str(exc))
    if width < 1328 or height < 531:
        return Check("graphical abstract dimensions", "FAIL", f"{width} x {height} px")
    return Check("graphical abstract dimensions", "PASS", f"{width} x {height} px")


def check_highlights(path: Path) -> Check:
    if not path.exists():
        return Check("highlights", "FAIL", f"Missing file: {path}")
    bullets = [line.removeprefix("-").strip() for line in path.read_text().splitlines() if line.strip().startswith("-")]
    too_long = [bullet for bullet in bullets if len(bullet) > 85]
    if not (3 <= len(bullets) <= 5):
        return Check("highlights", "FAIL", f"{len(bullets)} bullets; expected 3-5")
    if too_long:
        return Check("highlights", "FAIL", "Bullets over 85 characters: " + "; ".join(too_long))
    return Check("highlights", "PASS", f"{len(bullets)} bullets; all <=85 characters")


def check_manuscript_integrity() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_manuscript_integrity.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "manuscript figure/table integrity",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_source_data_matrix() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_source_data_matrix.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "figure/table source-data matrix",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_claim_evidence_matrix() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_claim_evidence_matrix.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "claim-evidence boundary matrix",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_figure_text_labels() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_figure_text_labels.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "figure reader-facing text labels",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_figure_captions_companion() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_figure_captions_companion.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "figure captions companion",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_cover_letter() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_cover_letter.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "cover letter and highlights support",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_abstract_scope() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_abstract_scope.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "abstract scope and conservative wording",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_declarations() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_declarations.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "declarations and author-confirmation support",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_coauthor_approval_packet() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_coauthor_approval_packet.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "coauthor final approval packet",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_editorial_manager_paste_fields() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_editorial_manager_paste_fields.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "Editorial Manager paste-field consistency",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_references() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_references.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "reference metadata and citation coverage",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_repro_package_coverage() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_repro_package_coverage.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "repro package evidence coverage",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_public_repro_package() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_public_repro_package.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "public reproducibility package",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_elsevier_upload_compliance() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_elsevier_upload_compliance.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "Elsevier upload compliance",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_editorial_manager_upload_ready() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_editorial_manager_upload_ready.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "Editorial Manager upload-ready bundle",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_upload_docx() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_upload_docx.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "cover letter and declarations DOCX",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_official_scope_alignment() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_official_scope_alignment.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "JNM official scope alignment",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_transfer_positioning_audit() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_transfer_positioning_audit.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "JNM transfer-positioning audit",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_materials_novelty_positioning() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_materials_novelty_positioning.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "JNM materials-novelty positioning",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_key_numeric_consistency() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_key_numeric_consistency.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "JNM key numeric and parameter consistency",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_scientific_storyline() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_scientific_storyline.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "scientific storyline consistency",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_objective_completion_audit() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_objective_completion_audit.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "objective completion and evidence-boundary audit",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_final_scientific_traceability_audit() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_final_scientific_traceability_audit.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "final scientific traceability audit",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_pdf_frontmatter() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_pdf_frontmatter.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "PDF frontmatter extraction",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_pdf_visual_qa() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_pdf_visual_qa.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "PDF visual QA and metadata warnings",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_repository_deposit_staging() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_repository_deposit_staging.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "repository-deposit staging package",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_frozen_deposit_packet() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_frozen_deposit_packet.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "frozen repository-deposit packet",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_start_here() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_start_here.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "JNM start-here guide",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_repository_copy_paste_fields() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_repository_copy_paste_fields.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "repository deposit copy-paste fields",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_final_upload_manifest() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_final_upload_manifest.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "final upload manifest",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_public_artifact_hygiene() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_public_artifact_hygiene.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "public upload text hygiene",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_reader_facing_hygiene() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_reader_facing_hygiene.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "reader-facing terminology hygiene",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_no_fake_repository_identifier() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_no_fake_repository_identifier.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "fake repository identifier leakage",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_title_consistency() -> Check:
    result = subprocess.run(
        ["python3", "scripts/check_jnm_title_consistency.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return Check(
        "title consistency",
        "PASS" if result.returncode == 0 else "FAIL",
        (result.stdout + result.stderr).strip(),
    )


def check_reader_facing_codes(paths: list[Path]) -> Check:
    pattern = re.compile(r"\b(?:PB-006|PB-007|SP-002|CAL1|seed\d+)\b", re.IGNORECASE)
    hits: list[str] = []
    for path in paths:
        for line_no, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            if pattern.search(line):
                hits.append(f"{path.relative_to(ROOT)}:{line_no}")
    if hits:
        return Check("reader-facing internal case labels", "FAIL", "; ".join(hits[:20]))
    return Check("reader-facing internal case labels", "PASS", "No PB/SP/CAL/seed labels in active manuscript text")


def check_repository_doi(paths: list[Path]) -> Check:
    placeholders: list[str] = []
    patterns = [
        "[repository DOI/URL to be added]",
        "doi_pending",
        "External DOI/stable URL required",
        "Repository DOI is missing",
        "Repository DOI/stable URL insertion still needed",
        "Expected blocker: repository DOI or stable URL has not yet been inserted",
        "Local manuscript/package gate: `BLOCKED_EXTERNAL`",
        "locally_ready_external_doi_pending",
    ]
    for path in paths:
        text = path.read_text(errors="replace")
        if any(pattern in text for pattern in patterns):
            placeholders.append(str(path.relative_to(ROOT)))
    if placeholders:
        return Check(
            "repository DOI/stable URL",
            "BLOCKED_EXTERNAL",
            "Repository deposit and DOI/stable URL insertion still needed: " + ", ".join(placeholders),
        )
    return Check("repository DOI/stable URL", "PASS", "No repository DOI placeholder found")


def check_no_running_dem() -> Check:
    result = subprocess.run(
        ["ps", "ax", "-o", "pid=,comm=,args="],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    workspace_candidates: list[str] = []
    external_candidates: list[str] = []

    def is_dem_process(command_name: str, command: str) -> bool:
        comm_base = Path(command_name).name.lower()
        argv_base = Path(command.split(maxsplit=1)[0]).name.lower() if command else comm_base
        bases = {comm_base, argv_base}
        if any(base == "liggghts" or base.startswith("liggghts-") for base in bases):
            return True
        if any(base == "lmp" or base.startswith("lmp_") or base.startswith("lmp-") for base in bases):
            return True
        if comm_base == "prterun" and ("lmp_" in command.lower() or "liggghts" in command.lower()):
            return True
        return False

    def process_cwd(pid: str) -> Path | None:
        cwd_result = subprocess.run(
            ["lsof", "-a", "-p", pid, "-d", "cwd", "-Fn"],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
        )
        for line in cwd_result.stdout.splitlines():
            if line.startswith("n/"):
                return Path(line[1:])
        return None

    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        parts = stripped.split(maxsplit=2)
        if len(parts) < 2:
            continue
        pid = parts[0]
        command_name = parts[1]
        command = parts[2] if len(parts) > 2 else command_name
        if not is_dem_process(command_name, command):
            continue
        cwd = process_cwd(pid)
        detail = f"{pid} cwd={cwd if cwd else '<unknown>'} cmd={command}"
        if cwd and ROOT in [cwd, *cwd.parents]:
            workspace_candidates.append(detail)
        else:
            external_candidates.append(detail)
    if workspace_candidates:
        return Check(
            "running DEM processes",
            "WARN",
            "Possible active current-workspace DEM processes: " + " | ".join(workspace_candidates[:5]),
        )
    if external_candidates:
        return Check(
            "running DEM processes",
            "PASS",
            "No active current-workspace DEM process detected; external DEM process(es) outside this submission workspace observed: "
            + " | ".join(external_candidates[:3]),
        )
    return Check("running DEM processes", "PASS", "No active current-workspace LIGGGHTS/lmp process detected")


def build_checks() -> list[Check]:
    checks: list[Check] = []
    required_files = [
        ROOT / "manuscript/journal_of_nuclear_materials_submission.pdf",
        ROOT / "manuscript/journal_of_nuclear_materials_submission.tex",
        ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md",
        ROOT / "manuscript/journal_of_nuclear_materials_author_metadata.csv",
        ROOT / "manuscript/journal_of_nuclear_materials_author_declaration_checklist.md",
        ROOT / "manuscript/journal_of_nuclear_materials_supplementary.pdf",
        ROOT / "manuscript/journal_of_nuclear_materials_highlights.md",
        ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md",
        ROOT / "manuscript/journal_of_nuclear_materials_cover_letter.docx",
        ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md",
        ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.docx",
        ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md",
        ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv",
        ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md",
        ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json",
        ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md",
        ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv",
        ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv",
        ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
        ROOT / "docs/jnm_author_final_upload_readme_zh.md",
        ROOT / "docs/jnm_final_submission_action_summary.md",
        ROOT / "docs/jnm_coauthor_final_approval_packet.md",
        ROOT / "docs/jnm_final_scientific_traceability_audit_20260613.md",
        ROOT / "docs/jnm_transfer_positioning_audit_20260613.md",
        ROOT / "docs/jnm_materials_novelty_positioning_matrix_20260613.md",
        ROOT / "docs/jnm_key_numeric_consistency_audit_20260613.md",
        ROOT / "docs/jnm_model_parameter_consistency_audit_20260613.md",
        ROOT / "docs/jnm_final_upload_manifest.csv",
        ROOT / "docs/jnm_final_upload_manifest.md",
        ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.png",
        ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip",
        ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip",
        ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip",
        ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip",
    ]
    checks.extend(check_file_exists(path, f"required file: {path.relative_to(ROOT)}") for path in required_files)
    checks.extend(check_csv_paths(ROOT / "manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv", "asset manifest"))
    checks.extend(check_csv_paths(ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv", "upload matrix"))
    checks.append(check_log_clean(ROOT / "manuscript/journal_of_nuclear_materials_submission.log"))
    checks.append(
        check_log_clean(
            ROOT
            / "submission_packages/journal_of_nuclear_materials_flat_source/journal_of_nuclear_materials_submission.log"
        )
    )
    checks.append(
        check_checksum(
            ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip",
            ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip.sha256",
            "main submission package checksum",
        )
    )
    checks.append(
        check_checksum(
            ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip",
            ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip.sha256",
            "public reproducibility package checksum",
        )
    )
    checks.append(
        check_checksum(
            ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip",
            ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip.sha256",
            "flat source package checksum",
        )
    )
    checks.append(
        check_checksum(
            ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip",
            ROOT / "submission_packages/jnm_editorial_manager_upload_ready.zip.sha256",
            "Editorial Manager upload-ready package checksum",
        )
    )
    checks.append(
        check_zip_members(
            ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip",
            [
                "journal_of_nuclear_materials_submission_package/START_HERE_JNM_SUBMISSION.md",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_submission.pdf",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_author_final_upload_readme_zh.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_final_submission_action_summary.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_coauthor_final_approval_packet.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_final_scientific_traceability_audit_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_transfer_positioning_audit_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_materials_novelty_positioning_matrix_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_reviewer_boundary_audit_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_material_degradation_state_variables_audit_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_key_numeric_consistency_audit_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_model_parameter_consistency_audit_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_active_run_provenance_capsule_20260613.md",
                "journal_of_nuclear_materials_submission_package/docs/jnm_repository_deposit_copy_paste_fields.md",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv",
                "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
                "journal_of_nuclear_materials_submission_package/manuscript/figure_captions.md",
                "journal_of_nuclear_materials_submission_package/figures/main/journal_of_nuclear_materials_graphical_abstract.png",
                "journal_of_nuclear_materials_submission_package/scripts/build_jnm_final_scientific_traceability_audit.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_final_scientific_traceability_audit.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_transfer_positioning_audit.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_materials_novelty_positioning.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_reviewer_boundaries.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_material_degradation_state_variables.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_key_numeric_consistency.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_model_parameter_consistency.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_active_run_provenance.py",
                "journal_of_nuclear_materials_submission_package/scripts/build_jnm_final_upload_manifest.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_final_upload_manifest.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_figure_captions_companion.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_frozen_deposit_packet.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_start_here.py",
                "journal_of_nuclear_materials_submission_package/scripts/check_jnm_repository_copy_paste_fields.py",
                "journal_of_nuclear_materials_submission_package/MANIFEST.csv",
            ],
        )
    )
    checks.append(check_graphical_abstract(ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.png"))
    checks.append(check_highlights(ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"))
    checks.append(check_abstract_scope())
    checks.append(check_references())
    checks.append(check_manuscript_integrity())
    checks.append(check_source_data_matrix())
    checks.append(check_claim_evidence_matrix())
    checks.append(check_figure_text_labels())
    checks.append(check_figure_captions_companion())
    checks.append(check_cover_letter())
    checks.append(check_declarations())
    checks.append(check_upload_docx())
    checks.append(check_coauthor_approval_packet())
    checks.append(check_editorial_manager_paste_fields())
    checks.append(check_public_repro_package())
    checks.append(check_repro_package_coverage())
    checks.append(check_elsevier_upload_compliance())
    checks.append(check_editorial_manager_upload_ready())
    checks.append(check_official_scope_alignment())
    checks.append(check_transfer_positioning_audit())
    checks.append(check_materials_novelty_positioning())
    checks.append(check_key_numeric_consistency())
    checks.append(check_scientific_storyline())
    checks.append(check_objective_completion_audit())
    checks.append(check_final_scientific_traceability_audit())
    checks.append(check_pdf_frontmatter())
    checks.append(check_pdf_visual_qa())
    checks.append(check_repository_deposit_staging())
    checks.append(check_frozen_deposit_packet())
    checks.append(check_start_here())
    checks.append(check_repository_copy_paste_fields())
    checks.append(check_final_upload_manifest())
    checks.append(check_public_artifact_hygiene())
    checks.append(check_reader_facing_hygiene())
    checks.append(check_no_fake_repository_identifier())
    checks.append(check_title_consistency())
    author_check = subprocess.run(
        ["python3", "scripts/check_jnm_author_metadata.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.append(
        Check(
            "author metadata consistency",
            "PASS" if author_check.returncode == 0 else "FAIL",
            (author_check.stdout + author_check.stderr).strip(),
        )
    )
    checks.append(
        check_reader_facing_codes(
            [
                ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md",
                ROOT / "manuscript/journal_of_nuclear_materials_submission.tex",
            ]
        )
    )
    checks.append(
        check_repository_doi(
            [
                ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md",
                ROOT / "manuscript/journal_of_nuclear_materials_submission.tex",
                ROOT / "manuscript/journal_of_nuclear_materials_author_declaration_checklist.md",
                ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
                ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv",
                ROOT / "manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv",
                ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv",
                ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md",
                ROOT / "docs/jnm_author_final_upload_readme_zh.md",
                ROOT / "docs/jnm_coauthor_final_approval_packet.md",
                ROOT / "docs/jnm_final_submission_action_summary.md",
                ROOT / "docs/next_stage_optimization_plan.md",
            ]
        )
    )
    checks.append(check_no_running_dem())
    return checks


def overall_status(checks: list[Check]) -> str:
    statuses = {check.status for check in checks}
    if "FAIL" in statuses:
        return "FAIL"
    if "BLOCKED_EXTERNAL" in statuses:
        return "BLOCKED_EXTERNAL"
    if "WARN" in statuses:
        return "WARN"
    return "PASS"


def write_reports(checks: list[Check]) -> None:
    status = overall_status(checks)
    counts = {state: sum(1 for check in checks if check.status == state) for state in ["PASS", "WARN", "BLOCKED_EXTERNAL", "FAIL"]}
    lines = [
        "# JNM final submission gate report",
        "",
        f"Overall status: **{status}**",
        "",
        f"Summary: {counts['PASS']} PASS, {counts['WARN']} WARN, {counts['BLOCKED_EXTERNAL']} BLOCKED_EXTERNAL, {counts['FAIL']} FAIL.",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in checks:
        detail = check.detail.replace("|", "\\|")
        lines.append(f"| {check.name} | {check.status} | {detail} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `FAIL` means a local package or manuscript issue must be fixed before upload.",
            "- `BLOCKED_EXTERNAL` means the local package is prepared but an author-side or repository-side action is still required.",
            "- The current expected external blocker is repository DOI/stable URL insertion after depositing the reduced reproducibility package.",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n")
    REPORT_JSON.write_text(
        json.dumps(
            {
                "overall_status": status,
                "counts": counts,
                "checks": [asdict(check) for check in checks],
            },
            indent=2,
        )
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Return non-zero for FAIL or BLOCKED_EXTERNAL.")
    args = parser.parse_args()
    checks = build_checks()
    write_reports(checks)
    status = overall_status(checks)
    print(f"overall_status={status}")
    print(f"report={REPORT_MD}")
    if args.strict and status != "PASS":
        return 1
    if status == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
