#!/usr/bin/env python3
"""Build the CPM reviewer-risk preflight matrix from current evidence paths."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CSV_OUT = DOCS / "cpm_reviewer_risk_preflight_20260704.csv"
MD_OUT = DOCS / "cpm_reviewer_risk_preflight_20260704.md"


ROWS = [
    {
        "risk": "Novelty and literature rationale",
        "likely_concern": "The work may look like a routine DEM compression calculation.",
        "current_response": (
            "The Introduction and cover letter now separate single-particle crush, "
            "packed-bed compression, force-network DEM, particle-replacement "
            "breakage and bonded-particle fracture studies, then identify the "
            "missing chronological link between contact-network state and first "
            "internal bond loss."
        ),
        "evidence": (
            "docs/cpm_literature_gap_map_20260704.md; "
            "manuscript/repaired_full_submission_draft.md; "
            "manuscript/computational_particle_mechanics_cover_letter.md"
        ),
        "boundary": "Keep the claim as a particle-mechanics event-sequence contribution.",
        "status": "reduced",
    },
    {
        "risk": "Material-property dependence",
        "likely_concern": "Previous rejections questioned whether material properties affect the calculated fracture events.",
        "current_response": (
            "The completed strength matrix adds six rows across two cracking "
            "geometries and reports first localized bond-loss displacement, "
            "endpoint broken bonds and force-network descriptors."
        ),
        "evidence": (
            "figures/pb007/pb007_material_strength_response.pdf; "
            "tables/pb007_material_parameter_response.csv; "
            "tables/pb007_material_strength_matrix_summary.csv; "
            "data/figure_source/pb007_material_strength_response.csv; "
            "docs/cpm_material_response_summary_20260704.md"
        ),
        "boundary": "Finite-window material-strength response, not a universal strength law.",
        "status": "reduced",
    },
    {
        "risk": "Statistical scope",
        "likely_concern": "The finite number of beds may not support stochastic failure probabilities.",
        "current_response": (
            "The manuscript states finite 100-particle windows, reports four "
            "localized cracking sequences and three zero-loss controls, and avoids "
            "probability or ensemble-convergence claims."
        ),
        "evidence": (
            "docs/repaired_manuscript_evidence_status_20260704.md; "
            "tables/pb007_macro_topology_event_metrics.csv; "
            "tables/pb007_material_parameter_response.csv"
        ),
        "boundary": "Event chronology and mechanism variables only; no converged probability.",
        "status": "bounded",
    },
    {
        "risk": "Single-particle template credibility",
        "likely_concern": "The 500-subparticle template may not be a credible parent-particle representation.",
        "current_response": (
            "The selected weak-plane template is tied to published crush-load and "
            "split-fragment constraints, with resolution and loading-rate "
            "sensitivity checks."
        ),
        "evidence": (
            "figures/apt_redesign/fig2_single_pebble_template_validation.pdf; "
            "tables/single_pebble_model_calibration_matrix.csv; "
            "tables/sp002_strength_multiplier_validation.csv"
        ),
        "boundary": "Sensitivity-bounded template candidate, not a final Li4SiO4 material law.",
        "status": "bounded",
    },
    {
        "risk": "Artificial pre-loading damage",
        "likely_concern": "The transfer procedure may create damage before compression.",
        "current_response": (
            "The entry-state validation retains 493,500 initial internal bonds, "
            "measurable load transfer and a connected native force graph before "
            "fracture loading."
        ),
        "evidence": (
            "figures/apt_redesign/fig3_entry_state_validation.pdf; "
            "tables/pb007_*_acceptance_summary.csv; "
            "tables/pb007_*_native_summary.csv"
        ),
        "boundary": "Accepted 100-particle windows only.",
        "status": "reduced",
    },
    {
        "risk": "Reproducibility and raw-data handling",
        "likely_concern": "The workflow may be difficult to verify or too large to archive.",
        "current_response": (
            "The upload package has a manifest and checksum, a reduced "
            "reproducibility package is archived with DOI, and large raw files are "
            "kept in NAS storage outside the compact repository."
        ),
        "evidence": (
            "docs/cpm_submission_readiness_report_20260704.md; "
            "README_CPM_SUBMISSION_20260704.md; "
            "START_HERE_CPM_SUBMISSION.md; "
            "submission_packages/computational_particle_mechanics_upload_ready.zip.sha256"
        ),
        "boundary": "Processed manuscript evidence is archived; full raw trajectories are on request.",
        "status": "reduced",
    },
    {
        "risk": "Journal scope",
        "likely_concern": "The manuscript could be read as a nuclear-materials or blanket-design paper instead of particle mechanics.",
        "current_response": (
            "The title, abstract, cover letter and keywords frame Li4SiO4 as a "
            "representative brittle ceramic pebble and present the contribution as "
            "packed brittle-particle mechanics."
        ),
        "evidence": (
            "manuscript/repaired_full_submission_draft.md; "
            "manuscript/computational_particle_mechanics_cover_letter.md; "
            "manuscript/computational_particle_mechanics_editorial_fields.md"
        ),
        "boundary": "Particle-mechanics scope with Li4SiO4 as the application material.",
        "status": "reduced",
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
        "# CPM Reviewer-Risk Preflight Matrix",
        "",
        "Date: 2026-07-04",
        "",
        "Purpose: record the main editor/reviewer risks after the previous rejections "
        "and the evidence currently used to reduce each risk. This is an internal "
        "author-facing preflight file.",
        "",
        "| Risk | Likely concern | Current response | Evidence | Boundary | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in ROWS:
        lines.append(
            "| {risk} | {likely_concern} | {current_response} | {evidence} | "
            "{boundary} | {status} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Current judgement",
            "",
            "The current CPM package is internally ready for live submission after "
            "external author metadata are completed. The remaining scientific risk is "
            "not a known missing calculation in the present finite-window claim; it is "
            "the boundary that the current data support event chronology and "
            "mechanism variables, not converged stochastic failure probability.",
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
