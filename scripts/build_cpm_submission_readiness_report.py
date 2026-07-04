#!/usr/bin/env python3
"""Build a concise readiness report for the CPM resubmission package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
UPLOAD_DIR = ROOT / "submission_packages" / "computational_particle_mechanics_upload_ready"
UPLOAD_ZIP = ROOT / "submission_packages" / "computational_particle_mechanics_upload_ready.zip"
REPRO_ZIP = ROOT / "submission_packages" / "repaired_submission_package.zip"
EMAIL_SHEET = UPLOAD_DIR / "10_author_email_completion_sheet.csv"
REPORT_MD = DOCS / "cpm_submission_readiness_report_20260704.md"
REPORT_JSON = DOCS / "cpm_submission_readiness_report_20260704.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_check() -> tuple[str, str]:
    cmd = [
        str(
            Path.home()
            / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
        ),
        "scripts/check_computational_particle_mechanics_submission_package.py",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    return ("PASS" if proc.returncode == 0 else "FAIL", (proc.stdout + proc.stderr).strip())


def zip_member_count(path: Path) -> int:
    with zipfile.ZipFile(path) as zf:
        return len(zf.namelist())


def read_manifest() -> list[dict[str, str]]:
    return list(csv.DictReader((UPLOAD_DIR / "MANIFEST.csv").open(encoding="utf-8")))


def read_email_sheet() -> tuple[int, int, list[str]]:
    rows = list(csv.DictReader(EMAIL_SHEET.open(encoding="utf-8")))
    missing = [row["Author"] for row in rows if row["Status"] == "Missing"]
    return len(rows), len(missing), missing


def build_payload() -> dict[str, object]:
    DOCS.mkdir(exist_ok=True)
    check_status, check_output = run_check()
    manifest = read_manifest()
    author_count, missing_email_count, missing_email_authors = read_email_sheet()
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "target_journal": "Computational Particle Mechanics",
        "manuscript_title": (
            "Bonded-template DEM reveals strength- and topology-dependent "
            "fracture-event sequences in packed brittle ceramic pebbles"
        ),
        "doi": "https://doi.org/10.5281/zenodo.20687351",
        "github_repository": "wangjianfttt/Mother_particle_bonded_dem_research",
        "preflight_status": check_status,
        "preflight_output": check_output,
        "upload_package": str(UPLOAD_ZIP.relative_to(ROOT)),
        "upload_package_bytes": UPLOAD_ZIP.stat().st_size,
        "upload_package_sha256": sha256(UPLOAD_ZIP),
        "reproducibility_package": str(REPRO_ZIP.relative_to(ROOT)),
        "reproducibility_package_bytes": REPRO_ZIP.stat().st_size,
        "reproducibility_package_sha256": sha256(REPRO_ZIP),
        "manifest_rows": len(manifest),
        "upload_zip_members": zip_member_count(UPLOAD_ZIP),
        "latex_source_members": zip_member_count(UPLOAD_DIR / "07_latex_source.zip"),
        "main_figure_members": zip_member_count(UPLOAD_DIR / "09_main_figures.zip"),
        "author_rows": author_count,
        "missing_email_count": missing_email_count,
        "missing_email_authors": missing_email_authors,
        "internal_status": "ready_for_live_submission_after_external_metadata",
        "external_items": [
            "Complete seven missing coauthor e-mail addresses if required by the live submission system.",
            "Confirm the article type and upload categories in the live Elsevier/ScienceDirect submission system.",
            "Preview the system-generated submission PDF before final submit.",
        ],
    }
    return payload


def write_markdown(payload: dict[str, object]) -> None:
    missing = payload["missing_email_authors"]
    assert isinstance(missing, list)
    lines = [
        "# CPM Submission Readiness Report",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Status",
        "",
        f"- Internal package status: `{payload['internal_status']}`",
        f"- Preflight status: `{payload['preflight_status']}`",
        f"- Preflight output: `{payload['preflight_output']}`",
        "",
        "## Target",
        "",
        f"- Journal: {payload['target_journal']}",
        f"- Manuscript title: {payload['manuscript_title']}",
        f"- DOI: {payload['doi']}",
        f"- GitHub repository: `{payload['github_repository']}`",
        "",
        "## Package Evidence",
        "",
        f"- Upload package: `{payload['upload_package']}`",
        f"- Upload package bytes: `{payload['upload_package_bytes']}`",
        f"- Upload package SHA256: `{payload['upload_package_sha256']}`",
        f"- Reduced reproducibility package: `{payload['reproducibility_package']}`",
        f"- Reduced reproducibility package bytes: `{payload['reproducibility_package_bytes']}`",
        f"- Reduced reproducibility package SHA256: `{payload['reproducibility_package_sha256']}`",
        f"- Manifest rows: `{payload['manifest_rows']}`",
        f"- Upload zip members: `{payload['upload_zip_members']}`",
        f"- LaTeX source zip members: `{payload['latex_source_members']}`",
        f"- Main figure zip members: `{payload['main_figure_members']}`",
        "",
        "## Author Metadata",
        "",
        f"- Author rows: `{payload['author_rows']}`",
        f"- Missing coauthor e-mail addresses: `{payload['missing_email_count']}`",
        "",
        "Missing e-mail authors:",
        "",
    ]
    lines.extend([f"- {name}" for name in missing])
    lines.extend(
        [
            "",
            "## External Items Before Final Submit",
            "",
        ]
    )
    external = payload["external_items"]
    assert isinstance(external, list)
    lines.extend([f"- [ ] {item}" for item in external])
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    payload = build_payload()
    REPORT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(payload)
    print(REPORT_MD)
    print(REPORT_JSON)


if __name__ == "__main__":
    main()

