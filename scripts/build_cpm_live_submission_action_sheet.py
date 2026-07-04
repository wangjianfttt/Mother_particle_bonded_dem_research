#!/usr/bin/env python3
"""Build a compact action sheet for live CPM submission."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
UPLOAD_DIR = ROOT / "submission_packages" / "computational_particle_mechanics_upload_ready"
READINESS_JSON = DOCS / "cpm_submission_readiness_report_20260704.json"
ACTION_CSV = DOCS / "cpm_live_submission_action_sheet_20260704.csv"
ACTION_JSON = DOCS / "cpm_live_submission_action_sheet_20260704.json"
ACTION_MD = DOCS / "cpm_live_submission_action_sheet_20260704.md"


UPLOAD_ACTIONS = [
    {
        "order": 1,
        "live_system_role": "Manuscript",
        "file": "01_manuscript.pdf",
        "requirement": "required",
        "submitter_action": "Upload as the main manuscript PDF.",
    },
    {
        "order": 2,
        "live_system_role": "Highlights",
        "file": "02_highlights.docx",
        "requirement": "required_if_highlights_field_or_file_is_requested",
        "submitter_action": "Upload or paste the five highlights from the editorial fields file.",
    },
    {
        "order": 3,
        "live_system_role": "Graphical abstract",
        "file": "03_graphical_abstract.png",
        "requirement": "if_requested",
        "submitter_action": "Prefer PNG for preview; use TIFF if the system asks for high-resolution artwork.",
    },
    {
        "order": 4,
        "live_system_role": "Graphical abstract high-resolution artwork",
        "file": "03_graphical_abstract.tiff",
        "requirement": "if_requested",
        "submitter_action": "Use if the live system requests a TIFF graphical abstract.",
    },
    {
        "order": 5,
        "live_system_role": "Graphical abstract editable backup",
        "file": "03_graphical_abstract.pdf; 03_graphical_abstract.svg",
        "requirement": "support",
        "submitter_action": "Keep as editable backup; upload only if the system asks for source artwork.",
    },
    {
        "order": 6,
        "live_system_role": "Declaration of competing interest",
        "file": "04_declaration_of_competing_interest.docx",
        "requirement": "required",
        "submitter_action": "Upload or paste the declaration text.",
    },
    {
        "order": 7,
        "live_system_role": "Cover letter",
        "file": "05_cover_letter.docx",
        "requirement": "required",
        "submitter_action": "Upload as the cover letter.",
    },
    {
        "order": 8,
        "live_system_role": "Author details and CRediT contributions",
        "file": "06_author_emails_and_contributions.docx",
        "requirement": "support",
        "submitter_action": "Use for author metadata and contribution fields.",
    },
    {
        "order": 9,
        "live_system_role": "LaTeX source",
        "file": "07_latex_source.zip",
        "requirement": "if_requested",
        "submitter_action": "Upload if the system asks for source files at initial submission.",
    },
    {
        "order": 10,
        "live_system_role": "Editorial paste fields",
        "file": "08_editorial_submission_fields.docx",
        "requirement": "support",
        "submitter_action": "Use for title, abstract, keywords and availability statements.",
    },
    {
        "order": 11,
        "live_system_role": "Main figures",
        "file": "09_main_figures.zip",
        "requirement": "if_separate_figure_files_are_requested",
        "submitter_action": "Upload if the system asks for separate figures; otherwise keep as support.",
    },
    {
        "order": 12,
        "live_system_role": "Author e-mail completion sheet",
        "file": "10_author_email_completion_sheet.docx; 10_author_email_completion_sheet.csv",
        "requirement": "external_metadata",
        "submitter_action": "Complete seven coauthor e-mails if the live system requires all author e-mails.",
    },
    {
        "order": 13,
        "live_system_role": "Optional blinded review file",
        "file": "computational_particle_mechanics_blinded_review_optional.zip",
        "requirement": "only_if_double_anonymized_review_is_requested",
        "submitter_action": "Use only if the live system requests a blinded manuscript package.",
    },
    {
        "order": 14,
        "live_system_role": "Reduced reproducibility package",
        "file": "repaired_submission_package.zip",
        "requirement": "support_or_repository_record",
        "submitter_action": "Use for data/code repository support or if supplemental data are requested.",
    },
]


FINAL_ACTIONS = [
    "Collect or confirm seven coauthor e-mail addresses if required by the live system.",
    "Confirm the article type shown by the live CPM submission workflow.",
    "Confirm whether PNG or TIFF is preferred for the graphical abstract.",
    "Preview the system-generated PDF before final submit.",
]


def read_manifest() -> dict[str, dict[str, str]]:
    rows = csv.DictReader((UPLOAD_DIR / "MANIFEST.csv").open(encoding="utf-8"))
    return {row["path"]: row for row in rows}


def file_status(file_field: str, manifest: dict[str, dict[str, str]]) -> str:
    parts = [part.strip() for part in file_field.split(";")]
    statuses = []
    for part in parts:
        if part.startswith("computational_particle_mechanics_blinded_review_optional"):
            path = ROOT / "submission_packages" / "computational_particle_mechanics_blinded_review_optional.zip"
        elif part == "repaired_submission_package.zip":
            path = ROOT / "submission_packages" / "repaired_submission_package.zip"
        else:
            path = UPLOAD_DIR / part
        statuses.append("present" if path.exists() and path.stat().st_size > 0 else "missing")
    return "present" if all(status == "present" for status in statuses) else "missing"


def build_payload() -> dict[str, object]:
    readiness = json.loads(READINESS_JSON.read_text(encoding="utf-8"))
    manifest = read_manifest()
    rows = []
    for item in UPLOAD_ACTIONS:
        row = dict(item)
        row["file_status"] = file_status(row["file"], manifest)
        row["formal_upload_package"] = "computational_particle_mechanics_upload_ready.zip"
        rows.append(row)
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "target_journal": "Computational Particle Mechanics",
        "upload_package": "submission_packages/computational_particle_mechanics_upload_ready.zip",
        "upload_package_sha256": readiness["upload_package_sha256"],
        "reduced_reproducibility_package": "submission_packages/repaired_submission_package.zip",
        "reduced_reproducibility_package_sha256": readiness[
            "reproducibility_package_sha256"
        ],
        "internal_status": readiness["internal_status"],
        "preflight_status": readiness["preflight_status"],
        "missing_email_count": readiness["missing_email_count"],
        "actions": rows,
        "final_actions": FINAL_ACTIONS,
    }


def write_csv(payload: dict[str, object]) -> None:
    rows = payload["actions"]
    assert isinstance(rows, list)
    with ACTION_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "order",
                "live_system_role",
                "file",
                "requirement",
                "file_status",
                "submitter_action",
                "formal_upload_package",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(payload: dict[str, object]) -> None:
    rows = payload["actions"]
    assert isinstance(rows, list)
    lines = [
        "# CPM Live Submission Action Sheet",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        f"- Target journal: {payload['target_journal']}",
        f"- Main upload package: `{payload['upload_package']}`",
        f"- Main upload package SHA256: `{payload['upload_package_sha256']}`",
        f"- Reduced reproducibility package: `{payload['reduced_reproducibility_package']}`",
        f"- Reduced reproducibility package SHA256: `{payload['reduced_reproducibility_package_sha256']}`",
        f"- Internal status: `{payload['internal_status']}`",
        f"- Preflight status: `{payload['preflight_status']}`",
        f"- Missing coauthor e-mail addresses: `{payload['missing_email_count']}`",
        "",
        "## Upload and Form Actions",
        "",
        "| Order | Live-system role | File or package | Requirement | File status | Submitter action |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {order} | {live_system_role} | `{file}` | `{requirement}` | `{file_status}` | {submitter_action} |".format(
                **row
            )
        )
    lines.extend(["", "## Final Live-System Actions", ""])
    final_actions = payload["final_actions"]
    assert isinstance(final_actions, list)
    lines.extend(f"- [ ] {item}" for item in final_actions)
    lines.append("")
    ACTION_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    payload = build_payload()
    ACTION_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_csv(payload)
    write_markdown(payload)
    print(ACTION_MD)
    print(ACTION_CSV)
    print(ACTION_JSON)


if __name__ == "__main__":
    main()
