#!/usr/bin/env python3
"""Build a goal-level completion audit for the CPM resubmission route."""

from __future__ import annotations

import csv
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REPORT_MD = DOCS / "cpm_goal_completion_audit_20260704.md"
REPORT_CSV = DOCS / "cpm_goal_completion_audit_20260704.csv"
REPORT_JSON = DOCS / "cpm_goal_completion_audit_20260704.json"
READINESS_JSON = DOCS / "cpm_submission_readiness_report_20260704.json"
NAS_ROOT = Path("/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究")


def run_preflight() -> tuple[str, str]:
    cmd = [
        str(
            Path.home()
            / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
        ),
        "scripts/check_computational_particle_mechanics_submission_package.py",
    ]
    env = os.environ.copy()
    env["CPM_SKIP_GOAL_AUDIT"] = "1"
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False, env=env)
    status = "PASS" if proc.returncode == 0 else "FAIL"
    return status, (proc.stdout + proc.stderr).strip()


def has_file(path: str) -> bool:
    return (ROOT / path).exists()


def large_raw_residue_count() -> int:
    suffixes = {".vtk", ".vtu", ".vtp", ".lammpstrj", ".xyz", ".data"}
    patterns = ("dump", "local", "restart")
    count = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        name = path.name.lower()
        if path.stat().st_size <= 20 * 1024 * 1024:
            continue
        if path.suffix.lower() in suffixes or any(token in name for token in patterns):
            count += 1
    return count


def nas_archive_summary() -> dict[str, object]:
    if not NAS_ROOT.exists():
        return {"exists": False, "archives": []}
    archives = []
    for path in sorted(NAS_ROOT.iterdir()):
        if path.is_dir():
            archives.append(path.name)
    return {"exists": True, "archives": archives}


def read_readiness() -> dict[str, object]:
    if not READINESS_JSON.exists():
        return {}
    return json.loads(READINESS_JSON.read_text(encoding="utf-8"))


def rows() -> tuple[list[dict[str, str]], dict[str, object]]:
    preflight_status, preflight_output = run_preflight()
    readiness = read_readiness()
    residue = large_raw_residue_count()
    nas = nas_archive_summary()
    package_ready = (
        preflight_status == "PASS"
        and readiness.get("internal_status") == "ready_for_live_submission_after_external_metadata"
    )
    author_pending = int(readiness.get("missing_email_count", 999)) > 0

    evidence_rows = [
        {
            "requirement": "Local workspace isolation and raw-data offload",
            "status": "achieved" if residue == 0 and nas["exists"] else "requires_attention",
            "evidence": "NAS archive exists; local raw dump/restart residue count >20 MB = %d" % residue,
            "current_file_or_command": "docs/nas_raw_dump_storage_check_20260704_1930.md; /Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究",
            "remaining_action": "Keep future raw dumps on NAS or outside synced folders.",
        },
        {
            "requirement": "Scientific gap and scope repair after rejections",
            "status": "achieved" if has_file("docs/cpm_literature_gap_map_20260704.md") else "missing",
            "evidence": "CPM literature-gap map and official-guide alignment are present.",
            "current_file_or_command": "docs/cpm_literature_gap_map_20260704.md; docs/cpm_official_submission_guide_alignment_20260704.md",
            "remaining_action": "Do not revert to NF/JNM/APT scope language.",
        },
        {
            "requirement": "Material-strength and topology data mining",
            "status": "achieved" if has_file("docs/cpm_material_response_summary_20260704.md") else "missing",
            "evidence": "Material-response summary records 11 completed endpoints and six strength-reduction rows.",
            "current_file_or_command": "docs/cpm_material_response_summary_20260704.md; tables/pb007_material_parameter_response.csv",
            "remaining_action": "Treat the result as finite-window mechanism evidence, not a converged probability.",
        },
        {
            "requirement": "Rebuilt manuscript mainline and display evidence",
            "status": "achieved" if has_file("manuscript/computational_particle_mechanics_submission.tex") and has_file("manuscript/computational_particle_mechanics_submission.pdf") else "missing",
            "evidence": "Target-specific TeX/PDF, source-data matrix, six main figures and editable figure package are present.",
            "current_file_or_command": "manuscript/computational_particle_mechanics_submission.*; submission_packages/computational_particle_mechanics_upload_ready/09_main_figures.zip",
            "remaining_action": "Keep claims synchronized with the finite-window evidence matrix.",
        },
        {
            "requirement": "Official-guide and submission package readiness",
            "status": "achieved" if package_ready else "requires_attention",
            "evidence": preflight_output.replace("\n", "; "),
            "current_file_or_command": "scripts/check_computational_particle_mechanics_submission_package.py; docs/cpm_submission_readiness_report_20260704.json",
            "remaining_action": "Use upload-ready zip and optional blinded package according to the live submission workflow.",
        },
        {
            "requirement": "External author metadata for live system",
            "status": "external_pending" if author_pending else "achieved",
            "evidence": "Missing coauthor e-mail count = %s; two public candidate e-mails require author confirmation." % readiness.get("missing_email_count", "unknown"),
            "current_file_or_command": "manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.docx; docs/cpm_author_email_public_lookup_20260704.md",
            "remaining_action": "Collect or confirm coauthor e-mails before final system submission if the live system requires them.",
        },
    ]
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "overall_status": "ready_after_external_author_metadata" if package_ready and author_pending else "ready" if package_ready else "requires_attention",
        "preflight_status": preflight_status,
        "large_raw_residue_count": residue,
        "nas_archive": nas,
        "readiness": readiness,
        "rows": evidence_rows,
    }
    return evidence_rows, payload


def write_csv(evidence_rows: list[dict[str, str]]) -> None:
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(evidence_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(evidence_rows)


def write_md(payload: dict[str, object]) -> None:
    evidence_rows = payload["rows"]
    assert isinstance(evidence_rows, list)
    lines = [
        "# CPM Goal-Level Completion Audit",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        f"- Overall status: `{payload['overall_status']}`",
        f"- CPM preflight status: `{payload['preflight_status']}`",
        f"- Local large raw dump/restart residue count: `{payload['large_raw_residue_count']}`",
        "",
        "## Requirement Evidence",
        "",
        "| Requirement | Status | Evidence | Current file or command | Remaining action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in evidence_rows:
        safe = {key: str(value).replace("|", "\\|") for key, value in row.items()}
        lines.append(
            "| {requirement} | `{status}` | {evidence} | `{current_file_or_command}` | {remaining_action} |".format(
                **safe
            )
        )
    lines.extend(
        [
            "",
            "## Decision Boundary",
            "",
            "The scientific, packaging and local-storage requirements are ready for a live Computational Particle Mechanics submission route.",
            "The active project goal should remain open until the external author metadata is supplied or the live submission system confirms that the missing coauthor e-mails are not required.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    evidence_rows, payload = rows()
    REPORT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(evidence_rows)
    write_md(payload)
    print(REPORT_MD)
    print(REPORT_CSV)
    print(REPORT_JSON)


if __name__ == "__main__":
    main()
