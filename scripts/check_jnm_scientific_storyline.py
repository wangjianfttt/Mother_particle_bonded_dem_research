#!/usr/bin/env python3
"""Validate the JNM scientific storyline against manuscript text and data."""

from __future__ import annotations

import csv
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PACKAGE_ROOT_NAME = "journal_of_nuclear_materials_reproducibility_package"
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
EVENTS = ROOT / (
    "data/processed/"
    "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv"
)
NATIVE = ROOT / (
    "data/processed/"
    "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_force_network_series.csv"
)
MACRO = ROOT / "tables/pb007_macro_topology_event_metrics.csv"
INDICES = ROOT / "tables/jnm_material_degradation_mechanism_indices.csv"
EVENT_ALIGNED_TOPOLOGY = ROOT / "tables/pb007_event_aligned_topology.csv"
EVENT_TOPOLOGY_AUDIT = ROOT / "docs/jnm_event_topology_mechanism_audit_20260613.md"


def is_public_package_root() -> bool:
    return ROOT.name == PUBLIC_PACKAGE_ROOT_NAME


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows = list(csv.DictReader(path.open()))
    if not rows:
        raise ValueError(f"{path} has no data rows")
    return rows


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    if value == "":
        raise ValueError(f"missing numeric value {key} in {row}")
    return float(value)


def as_int(row: dict[str, str], key: str) -> int:
    return int(round(as_float(row, key)))


def close(actual: float, expected: float, tol: float = 1.0e-6) -> bool:
    return math.isclose(actual, expected, rel_tol=tol, abs_tol=tol)


def main() -> int:
    errors: list[str] = []
    manuscript = MANUSCRIPT.read_text(errors="replace")
    manuscript_lower = manuscript.lower()

    required_phrases = [
        "fracture-event sequence",
        "native force graph",
        "localized upper-bed microcracking",
        "peak-to-endpoint top-wall force relaxes by 46.4%",
        "not as a converged fracture probability",
        "larger stochastic ensembles",
        "no coupled thermal-flow prediction",
        "500-subparticle mother-pebble templates",
    ]
    for phrase in required_phrases:
        if phrase.lower() not in manuscript_lower:
            errors.append(f"manuscript missing scientific-storyline phrase: {phrase}")

    events = read_rows(EVENTS)
    if len(events) != 3:
        errors.append(f"pilot event table should have 3 event rows, found {len(events)}")
    event_displacements = [as_float(row, "top_displacement_mm") * 1000.0 for row in events]
    if [round(value, 6) for value in event_displacements] != [25.0, 35.0, 60.0]:
        errors.append(f"unexpected event displacements: {event_displacements}")
    event_pebbles = {as_int(row, "pebble_id") for row in events}
    if event_pebbles != {78}:
        errors.append(f"events should localize in mother pebble 78, found {sorted(event_pebbles)}")
    if {as_int(row, "rank_from_top") for row in events} != {2}:
        errors.append("damaged mother pebble should have rank_from_top=2")
    if as_int(events[-1], "cumulative_broken_bonds") != 5:
        errors.append("pilot endpoint cumulative broken bonds should be 5")

    native = read_rows(NATIVE)
    edge_values = [as_int(row, "inter_pebble_edges") for row in native]
    reachable_values = [as_int(row, "top_reachable_mother_pebbles") for row in native]
    if edge_values[:3] != [55, 67, 79]:
        errors.append(f"unexpected early native-force edge sequence: {edge_values[:3]}")
    if reachable_values[:3] != [48, 58, 65]:
        errors.append(f"unexpected early top-reachability sequence: {reachable_values[:3]}")
    if {as_int(row, "spanning_force_graph") for row in native} != {1}:
        errors.append("all sampled pilot native-force graphs should be spanning")

    macro_rows = {row["case_label"]: row for row in read_rows(MACRO)}
    expected_cases = {
        "pilot_localized_microcracking",
        "seed02_intact_to_60um",
        "seed02_strength0p5_intact_to_60um",
        "seed02_strength0p25_intact_to_60um",
    }
    missing_cases = expected_cases - set(macro_rows)
    if missing_cases:
        errors.append("macro-topology table missing cases: " + ", ".join(sorted(missing_cases)))
    else:
        pilot = macro_rows["pilot_localized_microcracking"]
        if as_int(pilot, "event_rows") != 3:
            errors.append("pilot macro row should report 3 event rows")
        if as_int(pilot, "event_localized_broken_bonds") != 5:
            errors.append("pilot macro row should report 5 localized broken bonds")
        if not close(as_float(pilot, "first_event_disp_um"), 25.0):
            errors.append("pilot first event displacement should be 25 um")
        if not close(as_float(pilot, "last_event_disp_um"), 60.0):
            errors.append("pilot last event displacement should be 60 um")
        if as_int(pilot, "final_spanning_force_graph") != 1:
            errors.append("pilot final native force graph should be spanning")
        if as_int(pilot, "final_inter_mother_edges") != 74:
            errors.append("pilot final inter-mother edge count should be 74")
        for case in sorted(expected_cases - {"pilot_localized_microcracking"}):
            row = macro_rows[case]
            if as_int(row, "event_localized_broken_bonds") != 0:
                errors.append(f"{case} should remain intact at the endpoint")
            if as_int(row, "final_spanning_force_graph") != 1:
                errors.append(f"{case} should retain a spanning native force graph")
            if as_int(row, "final_inter_mother_edges") != 83:
                errors.append(f"{case} should finish with 83 inter-mother force edges")

    index_rows = {row["metric"]: row for row in read_rows(INDICES)}
    required_indices = {
        "endpoint_broken_bond_fraction": 1.0132e-05,
        "damaged_mother_pebble_fraction": 0.01,
        "inter_mother_edge_densification": 1.436,
        "top_reachability_densification": 1.354,
        "peak_to_endpoint_force_relaxation": 0.4643,
        "pilot_to_independent_final_force_sum_contrast": 3.418,
    }
    for metric, expected in required_indices.items():
        if metric not in index_rows:
            errors.append(f"missing mechanism index: {metric}")
            continue
        if not close(float(index_rows[metric]["value"]), expected, tol=5.0e-4):
            errors.append(f"{metric} should be {expected}, found {index_rows[metric]['value']}")
    if index_rows.get("spanning_graph_with_local_damage", {}).get("value") != "yes":
        errors.append("spanning_graph_with_local_damage should be yes")
    if index_rows.get("strength_audit_endpoint_broken_bonds", {}).get("value") != "0":
        errors.append("strength_audit_endpoint_broken_bonds should be 0")

    aligned = read_rows(EVENT_ALIGNED_TOPOLOGY)
    if len(aligned) != 3:
        errors.append(f"event-aligned topology table should have 3 rows, found {len(aligned)}")
    expected_aligned = [
        {
            "event_displacement_um": 25.0,
            "new_broken_bonds": 2,
            "previous_inter_mother_edges": 55,
            "next_inter_mother_edges": 67,
            "delta_inter_mother_edges": 12,
            "previous_top_reachable_mothers": 48,
            "next_top_reachable_mothers": 58,
            "delta_top_reachable_mothers": 10,
        },
        {
            "event_displacement_um": 35.0,
            "new_broken_bonds": 2,
            "previous_inter_mother_edges": 67,
            "next_inter_mother_edges": 79,
            "delta_inter_mother_edges": 12,
            "previous_top_reachable_mothers": 58,
            "next_top_reachable_mothers": 65,
            "delta_top_reachable_mothers": 7,
        },
        {
            "event_displacement_um": 60.0,
            "new_broken_bonds": 1,
            "previous_inter_mother_edges": 67,
            "next_inter_mother_edges": 74,
            "delta_inter_mother_edges": 7,
            "previous_top_reachable_mothers": 56,
            "next_top_reachable_mothers": 57,
            "delta_top_reachable_mothers": 1,
        },
    ]
    for row, expected in zip(aligned, expected_aligned):
        for key, value in expected.items():
            actual = as_float(row, key)
            if not close(actual, float(value), tol=1.0e-6):
                errors.append(f"event-aligned topology {key} should be {value}, found {actual}")
        if as_int(row, "pebble_id") != 78:
            errors.append("event-aligned topology should localize events in mother pebble 78")
        if as_int(row, "spanning_graph_before") != 1 or as_int(row, "spanning_graph_after") != 1:
            errors.append("event-aligned topology should remain spanning before and after each event")
        if "spanning native force graph" not in row.get("mechanism_note", ""):
            errors.append("event-aligned topology mechanism note should mention spanning native force graph")

    if not EVENT_TOPOLOGY_AUDIT.exists() or EVENT_TOPOLOGY_AUDIT.stat().st_size == 0:
        errors.append("event-aligned topology mechanism audit is missing or empty")
    else:
        audit_text = EVENT_TOPOLOGY_AUDIT.read_text(errors="replace")
        required_audit_phrases = [
            "Event-aligned topology mechanism audit",
            "25.0",
            "35.0",
            "60.0",
            "55 -> 67",
            "67 -> 79",
            "67 -> 74",
            "early breeder-pebble microcracking can be localized",
            "does not establish a converged fracture probability",
        ]
        for phrase in required_audit_phrases:
            if phrase not in audit_text:
                errors.append(f"event-topology mechanism audit missing phrase: {phrase}")

    reviewer_boundary_script = ROOT / "scripts/check_jnm_reviewer_boundaries.py"
    if reviewer_boundary_script.exists():
        boundary_check = subprocess.run(
            ["python3", str(reviewer_boundary_script.relative_to(ROOT))],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if boundary_check.returncode != 0:
            errors.append("reviewer-boundary subcheck failed: " + (boundary_check.stdout + boundary_check.stderr).strip())
    elif not is_public_package_root():
        errors.append("reviewer-boundary subcheck script is missing")

    state_variable_check = subprocess.run(
        ["python3", "scripts/check_jnm_material_degradation_state_variables.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if state_variable_check.returncode != 0:
        errors.append(
            "material-degradation state-variable subcheck failed: "
            + (state_variable_check.stdout + state_variable_check.stderr).strip()
        )

    if errors:
        print("FAIL scientific storyline")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS scientific storyline: event sequence, macro response, native-force topology, "
        "mechanism indices and conservative boundaries are consistent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
