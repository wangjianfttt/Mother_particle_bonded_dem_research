#!/usr/bin/env python3
"""Build a traceable literature-gap map for the CPM manuscript."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CSV_OUT = DOCS / "cpm_literature_gap_map_20260704.csv"
MD_OUT = DOCS / "cpm_literature_gap_map_20260704.md"


ROWS = [
    {
        "literature_class": "Single-particle crush and fragment-mode evidence",
        "current_references": (
            "PlateMaterialLi4SiO4; Zhao2013FailureInitiationLi4SiO4; "
            "Annabattula2014SizeDependentCrush; Bhartia2020ElasticResponse; "
            "Tavares2022SingleParticleBreakageReview"
        ),
        "what_the_literature_provides": (
            "Load scale, size dependence, failure-initiation context and "
            "single-particle fragment-mode targets."
        ),
        "remaining_gap": (
            "Single-particle tests do not identify the first damaged parent "
            "particle inside a load-bearing random bed."
        ),
        "present_evidence": (
            "Fig. 2; Table 1; tables/single_pebble_model_calibration_matrix.csv; "
            "data/figure_source/fig2_single_pebble_*.csv"
        ),
        "manuscript_role": "Calibrates the bonded template before bed insertion.",
        "claim_boundary": (
            "Sensitivity-bounded template representation, not a final Li4SiO4 "
            "material law."
        ),
    },
    {
        "literature_class": "Packed-bed compression and crushed-bed consequences",
        "current_references": (
            "ZaccariLoFrano2009CeramicPebbleBeds; "
            "PreliminaryLi4SiO4StructuralPerformance; "
            "CrushedPebblePressureDrop2024; Fang2026Li4SiO4BedCrushing"
        ),
        "what_the_literature_provides": (
            "Bed stiffness, compaction, breakage-ratio and pressure-drop trends."
        ),
        "remaining_gap": (
            "Bed-level responses do not resolve the chronological source of "
            "the first localized internal damage."
        ),
        "present_evidence": (
            "Fig. 4; Table 2; tables/pb007_macro_topology_event_metrics.csv; "
            "data/figure_source/fig4_fracture_sequence_pilot_events.csv"
        ),
        "manuscript_role": (
            "Converts compression response into parent-particle event sequences."
        ),
        "claim_boundary": "Finite 100-particle windows, not converged failure probability.",
    },
    {
        "literature_class": "DEM force-chain and load-path studies",
        "current_references": (
            "An2007DEMCeramicBreederBeds; GanKamlah2010DEMPebbleBeds; "
            "Wang2024ForceChainPebbleBed"
        ),
        "what_the_literature_provides": (
            "Coordination number, contact-force distribution and load-path "
            "evolution in particulate beds."
        ),
        "remaining_gap": (
            "Force-chain descriptors are rarely linked to internal bond-loss "
            "increments of named parent particles."
        ),
        "present_evidence": (
            "Fig. 5; Table 3; tables/pb007_event_aligned_topology.csv; "
            "tables/pb007_mechanism_variable_separation.csv"
        ),
        "manuscript_role": (
            "Links localized fracture events to native force-network state variables."
        ),
        "claim_boundary": (
            "State-space separation in the current finite windows, not a universal "
            "classifier."
        ),
    },
    {
        "literature_class": "Particle-replacement and crushable-bed DEM",
        "current_references": (
            "JimenezHerrera2018BreakageModels; Barrios2020ParticleBedBreakage; "
            "Zhou2020FragmentReplacementModes; Wang2021CrushableCeramicPebbleBed; "
            "CrushableDEMPebbleBed2026"
        ),
        "what_the_literature_provides": (
            "Efficient bed-scale particle replacement, fragment insertion and "
            "crushed-fraction effects."
        ),
        "remaining_gap": (
            "Replacement routes usually begin after an overload criterion and "
            "do not preserve a pre-loaded internal bond graph for every parent particle."
        ),
        "present_evidence": (
            "Fig. 1; Fig. 3; Table 1; tables/pb007_*_acceptance_summary.csv"
        ),
        "manuscript_role": (
            "Introduces intact bonded-template insertion before fracture loading."
        ),
        "claim_boundary": (
            "Workflow evidence for accepted windows; raw large ensembles remain "
            "future work."
        ),
    },
    {
        "literature_class": "Bonded-particle fracture modelling",
        "current_references": "PotyondyCundall2004",
        "what_the_literature_provides": (
            "A subparticle-bond representation that can resolve internal crack "
            "growth and fragment topology."
        ),
        "remaining_gap": (
            "The single-object bonded-particle idea needs a bed insertion and "
            "event-extraction route for many parent particles."
        ),
        "present_evidence": (
            "Figs. 1, 4 and 6; Tables 2 and 4; "
            "tables/pb007_material_parameter_response.csv"
        ),
        "manuscript_role": (
            "Extends bonded-particle fracture resolution to packed parent-particle "
            "event chronology."
        ),
        "claim_boundary": (
            "Event chronology and material-response evidence in 100-particle "
            "windows."
        ),
    },
]


def write_csv() -> None:
    DOCS.mkdir(exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(ROWS[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(ROWS)


def write_md() -> None:
    lines = [
        "# CPM Literature Gap Map",
        "",
        "Date: 2026-07-04",
        "",
        "Purpose: record how the current Computational Particle Mechanics manuscript "
        "responds to the previous literature-context and novelty concern. This is an "
        "internal author-facing map; the manuscript text should remain concise.",
        "",
        "| Literature class | Current references | What they provide | Remaining gap | Present evidence | Boundary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in ROWS:
        lines.append(
            "| {literature_class} | `{current_references}` | {what_the_literature_provides} | "
            "{remaining_gap} | {present_evidence} | {claim_boundary} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Manuscript action",
            "",
            "- The Introduction now states the five literature classes directly.",
            "- The stated gap is the chronological link between a load-bearing contact network and the first internal bond losses inside named parent particles.",
            "- The discussion keeps the claim bounded to finite 100-particle windows and material-response evidence, not a converged stochastic failure probability.",
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
