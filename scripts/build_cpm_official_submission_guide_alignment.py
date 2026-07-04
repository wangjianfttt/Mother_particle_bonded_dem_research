#!/usr/bin/env python3
"""Build an official-guide alignment table for CPM submission readiness."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CSV_OUT = DOCS / "cpm_official_submission_guide_alignment_20260704.csv"
MD_OUT = DOCS / "cpm_official_submission_guide_alignment_20260704.md"

SCIENCEDIRECT_GUIDE = "https://www.sciencedirect.com/journal/computational-particle-mechanics/publish/guide-for-authors"
SPRINGER_NOTICE = "https://link.springer.com/journal/40571/submission-guidelines"


ROWS = [
    {
        "guide_item": "Current submission route",
        "official_source": "ScienceDirect Guide for Authors; Springer submission-guidelines transition notice",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready.zip; START_HERE_CPM_SUBMISSION.md",
        "status": "ready",
        "remaining_action": "Use the live ScienceDirect/Editorial Manager route, not the closed Springer portal.",
    },
    {
        "guide_item": "Article scope",
        "official_source": "ScienceDirect Guide for Authors: journal covers computational particle mechanics, DEM, modelling and fracture/fragmentation of particulate systems.",
        "current_package_evidence": "manuscript/computational_particle_mechanics_submission.tex; docs/cpm_literature_gap_map_20260704.md",
        "status": "ready",
        "remaining_action": "Select Research article or closest available article type in the live system.",
    },
    {
        "guide_item": "Double-anonymized review",
        "official_source": "ScienceDirect Guide for Authors: journal operates a double anonymized review process.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_blinded_review_optional.zip",
        "status": "ready_if_requested",
        "remaining_action": "Use the optional blinded package if the live system requests a blinded manuscript file.",
    },
    {
        "guide_item": "Abstract length",
        "official_source": "ScienceDirect Guide for Authors: abstract must be concise, factual and not exceed 250 words.",
        "current_package_evidence": "manuscript/computational_particle_mechanics_submission.tex",
        "status": "ready",
        "remaining_action": "Current manuscript abstract is checked by the package script and remains within 250 words.",
    },
    {
        "guide_item": "Title-page author details",
        "official_source": "ScienceDirect Guide for Authors: title page should include author names, affiliations, corresponding author and e-mail details where available.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready/10_author_email_completion_sheet.csv; manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.docx",
        "status": "external_metadata_pending",
        "remaining_action": "Confirm seven coauthor e-mails or leave only confirmed e-mail information if the live system does not require all author e-mails.",
    },
    {
        "guide_item": "Editable manuscript source",
        "official_source": "ScienceDirect Guide for Authors: submit editable source files where requested.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready/07_latex_source.zip",
        "status": "ready",
        "remaining_action": "Upload LaTeX source zip if the system asks for source files at initial submission.",
    },
    {
        "guide_item": "Highlights",
        "official_source": "Prepared as Elsevier-system support material; upload only if the live submission workflow requests highlights.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready/02_highlights.docx",
        "status": "ready_if_requested",
        "remaining_action": "Upload the DOCX or paste the five highlights only if the live system asks for them.",
    },
    {
        "guide_item": "Graphical abstract and artwork",
        "official_source": "ScienceDirect Guide for Authors: artwork files should be supplied separately; generative-AI artwork is not permitted. Graphical abstract is prepared only as live-system support material.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready/03_graphical_abstract.*; scripts/plot_apt_graphical_abstract.py",
        "status": "ready_if_requested",
        "remaining_action": "Use the script-generated graphical abstract only if requested; do not upload generative-AI artwork.",
    },
    {
        "guide_item": "Declaration of competing interest",
        "official_source": "ScienceDirect Guide for Authors: declaration files/statements are required.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready/04_declaration_of_competing_interest.docx",
        "status": "ready",
        "remaining_action": "Upload the declaration DOCX.",
    },
    {
        "guide_item": "Figure files",
        "official_source": "ScienceDirect Guide for Authors: figure files should be uploaded separately at suitable quality.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready/09_main_figures.zip",
        "status": "ready",
        "remaining_action": "Upload 09_main_figures.zip or individual figure files if the live system separates figure upload.",
    },
    {
        "guide_item": "Tables and source data",
        "official_source": "ScienceDirect Guide for Authors: tables should be editable and data availability should be stated.",
        "current_package_evidence": "manuscript/computational_particle_mechanics_submission.tex; submission_packages/repaired_submission_package.zip",
        "status": "ready",
        "remaining_action": "Use the manuscript tables and reduced reproducibility package for editable/source-backed evidence.",
    },
    {
        "guide_item": "Data and code availability",
        "official_source": "ScienceDirect Guide for Authors: data/code availability statements and repository links should be supplied where applicable.",
        "current_package_evidence": "manuscript/computational_particle_mechanics_submission.tex; DOI 10.5281/zenodo.20687351; GitHub repository",
        "status": "ready",
        "remaining_action": "Paste the DOI-backed data and code statements from editorial fields.",
    },
    {
        "guide_item": "Author metadata",
        "official_source": "Live submission system author-entry forms.",
        "current_package_evidence": "submission_packages/computational_particle_mechanics_upload_ready/10_author_email_completion_sheet.csv",
        "status": "external_metadata_pending",
        "remaining_action": "Fill seven coauthor e-mail addresses if the live system requires every author e-mail.",
    },
    {
        "guide_item": "Final generated PDF review",
        "official_source": "Live submission system preview step.",
        "current_package_evidence": "manuscript/computational_particle_mechanics_live_submission_checklist.md",
        "status": "external_submission_step",
        "remaining_action": "Preview the system-generated PDF before clicking final submit.",
    },
]


def write_csv() -> None:
    DOCS.mkdir(exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


def write_md() -> None:
    lines = [
        "# CPM official submission-guide alignment",
        "",
        "Date: 2026-07-04",
        "",
        "Official sources checked:",
        "",
        f"- ScienceDirect Guide for Authors: {SCIENCEDIRECT_GUIDE}",
        f"- Springer transition notice for this journal: {SPRINGER_NOTICE}",
        "",
        "Purpose: map current upload files and support files to the live journal requirements before final submission.",
        "",
        "| Guide item | Official source | Current package evidence | Status | Remaining action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in ROWS:
        lines.append(
            "| {guide_item} | {official_source} | `{current_package_evidence}` | `{status}` | {remaining_action} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "- Local upload and reproducibility files are ready for live-system entry.",
            "- An optional blinded-review package is available for the double-anonymized review workflow if requested by the live system.",
            "- Highlights and graphical-abstract files are prepared as optional live-system support, not treated as confirmed compulsory CPM guide items.",
            "- The remaining non-local items are seven coauthor e-mail addresses, live article-type/category confirmation and system-generated PDF preview.",
            "",
        ]
    )
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    write_csv()
    write_md()
    print(MD_OUT)
    print(CSV_OUT)


if __name__ == "__main__":
    main()
