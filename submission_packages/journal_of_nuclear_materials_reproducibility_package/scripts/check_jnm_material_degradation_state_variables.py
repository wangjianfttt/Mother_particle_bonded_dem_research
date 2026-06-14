#!/usr/bin/env python3
"""Verify material-degradation state-variable framing for the JNM paper."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
COVER_LETTER = ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md"
PREBUTTAL = ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md"
AUDIT = ROOT / "docs/jnm_material_degradation_state_variables_audit_20260613.md"
MECHANISM_INDICES = ROOT / "tables/jnm_material_degradation_mechanism_indices.csv"
EVENT_TOPOLOGY = ROOT / "tables/pb007_event_aligned_topology.csv"

STATE_VARIABLES = [
    "event time",
    "damaged mother-pebble identity",
    "bond-loss increment",
    "native force connectivity",
    "macroscopic force relaxation",
]

MANUSCRIPT_PHRASES = [
    "material-degradation state variables",
    "event time",
    "damaged mother-pebble identity",
    "bond-loss increment",
    "native force connectivity",
    "macroscopic force relaxation",
    "time-stamped, location-resolved and load-path-aware",
    "ceramic breeder-bed degradation",
    "1.0e-5",
    "1.44x",
    "1.35x",
    "46.4%",
    "mesoscale shielding-and-activation field",
]

COVER_PHRASES = [
    "material-degradation state variables",
    "event time",
    "damaged mother-pebble identity",
    "bond-loss increment",
    "native force connectivity",
    "macroscopic force relaxation",
]

PREBUTTAL_PHRASES = [
    "reusable materials information",
    "state-variable structure",
    "event time",
    "damaged mother-pebble identity",
    "bond-loss increment",
    "native force connectivity",
    "macroscopic force relaxation",
    "local contact-network degradation pathway",
    "later coupled heat-transfer and purge-flow studies",
]

REQUIRED_MECHANISM_INDICES = {
    "endpoint_broken_bond_fraction": "1.0132e-05",
    "damaged_mother_pebble_fraction": "0.01",
    "damaged_pebble_rank_from_top": "2",
    "inter_mother_edge_densification": "1.436",
    "top_reachability_densification": "1.354",
    "peak_to_endpoint_force_relaxation": "0.4643",
    "pilot_to_independent_final_force_sum_contrast": "3.418",
    "spanning_graph_with_local_damage": "yes",
    "strength_audit_endpoint_broken_bonds": "0",
}

REQUIRED_EVENT_TOPOLOGY = {
    "25.0": ("2", "55", "67", "48", "58"),
    "35.0": ("2", "67", "79", "58", "65"),
    "60.0": ("1", "67", "74", "56", "57"),
}


def read_required(path: Path) -> str:
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(path.relative_to(ROOT).as_posix())
    return path.read_text(encoding="utf-8", errors="replace")


def missing_phrases(text: str, phrases: list[str]) -> list[str]:
    text_lower = text.lower()
    return [phrase for phrase in phrases if phrase.lower() not in text_lower]


def write_audit() -> None:
    metrics = list(csv.DictReader(MECHANISM_INDICES.open(encoding="utf-8")))
    event_rows = list(csv.DictReader(EVENT_TOPOLOGY.open(encoding="utf-8")))
    lines = [
        "# JNM material-degradation state-variable audit",
        "",
        "Purpose: protect the Journal of Nuclear Materials framing introduced after the NF scope rejection. "
        "The paper should not read as a generic DEM movie; it should expose computed state variables for Li4SiO4 ceramic breeder-bed degradation.",
        "",
        "## Required state variables",
        "",
    ]
    lines.extend(f"- {item}" for item in STATE_VARIABLES)
    lines.extend(
        [
            "",
            "## Cross-scale mechanism chain",
            "",
            "The state variables are useful because they connect four scales that a materials-journal reviewer can audit:",
            "",
            "1. Internal fracture chronology: event time, damaged mother-pebble identity and bond-loss increment.",
            "2. Mesoscale load-path environment: native force connectivity, top reachability and inter-mother force edges.",
            "3. Macroscopic bed response: top-wall force history, peak-to-endpoint relaxation and final force-sum contrast.",
            "4. Fusion-breeder service interpretation: contact-stiffness, heat-transfer constriction and helium purge-path implications, without solving coupled transport.",
            "",
            "This chain is the bridge from a numerical bond graph to ceramic breeder-material degradation; it keeps the manuscript from reading as a generic granular DEM visualization.",
            "",
            "## Mechanism indices locked by the gate",
            "",
            "| Metric | Value | Interpretation | Boundary |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for row in metrics:
        lines.append(
            f"| {row['metric']} | {row['value']} {row['unit']} | "
            f"{row['interpretation']} | {row['boundary']} |"
        )
    lines.extend(
        [
            "",
            "## Event-aligned topology bridge",
            "",
            "| Event displacement (micrometres) | New broken bonds | Inter-mother edges | Top-reachable mothers | Force-network status |",
            "| ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in event_rows:
        lines.append(
            f"| {row['event_displacement_um']} | {row['new_broken_bonds']} | "
            f"{row['previous_inter_mother_edges']} -> {row['next_inter_mother_edges']} | "
            f"{row['previous_top_reachable_mothers']} -> {row['next_top_reachable_mothers']} | "
            f"spanning before={row['spanning_graph_before']}, after={row['spanning_graph_after']} |"
        )
    lines.extend(
        [
            "",
            "## Evidence",
            "",
            "- The manuscript abstract, introduction and discussion define the output as material-degradation state variables.",
            "- The cover letter presents the same state-variable framing to the editor.",
            "- The reviewer-risk prebuttal explains why these variables are reusable beyond a single pilot calculation.",
            "- `tables/jnm_material_degradation_mechanism_indices.csv` fixes the quantitative bridge from localized bond loss to force-network reorganization and macroscopic relaxation.",
            "- `tables/pb007_event_aligned_topology.csv` confirms that each event increment occurs inside a measured spanning native force graph.",
            "",
            "## Boundary",
            "",
            "These state variables support event-sequence and mechanism interpretation only. They are not a calibrated lifetime model, a converged fracture probability, a final Li4SiO4 constitutive law or a coupled thermal-flow prediction. The heat-transfer and purge-path language is therefore a service-relevance interpretation of contact-network degradation, not a reported transport simulation.",
            "",
        ]
    )
    AUDIT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    try:
        manuscript = read_required(MANUSCRIPT)
    except FileNotFoundError as exc:
        print(f"FAIL material-degradation state variables: missing {exc}")
        return 1
    try:
        mechanism_rows = list(csv.DictReader(MECHANISM_INDICES.open(encoding="utf-8")))
        event_rows = list(csv.DictReader(EVENT_TOPOLOGY.open(encoding="utf-8")))
    except FileNotFoundError as exc:
        print(f"FAIL material-degradation state variables: missing {exc}")
        return 1
    cover = COVER_LETTER.read_text(encoding="utf-8", errors="replace") if COVER_LETTER.exists() else ""
    prebuttal = PREBUTTAL.read_text(encoding="utf-8", errors="replace") if PREBUTTAL.exists() else ""

    checks = [("manuscript", manuscript, MANUSCRIPT_PHRASES)]
    # The public reproducibility package deliberately excludes cover-letter and
    # reviewer-preparation files. Check them when present in the full workspace,
    # while keeping the deposited package self-auditable from manuscript text.
    if cover:
        checks.append(("cover letter", cover, COVER_PHRASES))
    if prebuttal:
        checks.append(("reviewer-risk prebuttal", prebuttal, PREBUTTAL_PHRASES))
    for label, text, phrases in checks:
        missing = missing_phrases(text, phrases)
        if missing:
            failures.append(f"{label} missing: " + "; ".join(missing))

    metric_values = {row.get("metric", ""): row.get("value", "") for row in mechanism_rows}
    for metric, expected in REQUIRED_MECHANISM_INDICES.items():
        if metric_values.get(metric) != expected:
            failures.append(
                f"mechanism index {metric} expected {expected}, found {metric_values.get(metric, '<missing>')}"
            )

    event_by_disp = {row.get("event_displacement_um", ""): row for row in event_rows}
    for displacement, expected_values in REQUIRED_EVENT_TOPOLOGY.items():
        row = event_by_disp.get(displacement)
        if not row:
            failures.append(f"missing event-aligned topology row at {displacement} micrometres")
            continue
        observed = (
            row.get("new_broken_bonds", ""),
            row.get("previous_inter_mother_edges", ""),
            row.get("next_inter_mother_edges", ""),
            row.get("previous_top_reachable_mothers", ""),
            row.get("next_top_reachable_mothers", ""),
        )
        if observed != expected_values:
            failures.append(
                f"event topology at {displacement} micrometres expected {expected_values}, found {observed}"
            )
        if row.get("spanning_graph_before") != "1" or row.get("spanning_graph_after") != "1":
            failures.append(f"event topology at {displacement} micrometres is not spanning before and after")

    overclaim_phrases = [
        "calibrated lifetime model",
        "converged fracture probability model",
        "final Li4SiO4 constitutive law",
        "coupled thermal-flow prediction",
    ]
    manuscript_lower = manuscript.lower()
    for phrase in overclaim_phrases:
        phrase_lower = phrase.lower()
        is_negated = (
            f"not {phrase_lower}" in manuscript_lower
            or f"no {phrase_lower}" in manuscript_lower
            or f"not a {phrase_lower}" in manuscript_lower
        )
        if phrase_lower in manuscript_lower and not is_negated:
            failures.append(f"possible unbounded overclaim in manuscript: {phrase}")

    if failures:
        print("FAIL material-degradation state variables")
        for failure in failures:
            print(f"- {failure}")
        return 1

    write_audit()
    print(
        "PASS material-degradation state variables: manuscript, cover letter and prebuttal preserve "
        "event-time, damaged-pebble, bond-loss, force-connectivity, force-relaxation and cross-scale mechanism framing"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
