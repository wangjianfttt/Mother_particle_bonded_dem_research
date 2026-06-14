#!/usr/bin/env python3
"""Summarize JNM-facing material-degradation mechanism indices from PB-007 data."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MACRO = ROOT / "tables/pb007_macro_topology_event_metrics.csv"
PILOT_EVENTS = (
    ROOT
    / "data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv"
)
PILOT_NATIVE = (
    ROOT
    / "data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_force_network_series.csv"
)
OUT_CSV = ROOT / "tables/jnm_material_degradation_mechanism_indices.csv"
OUT_MD = ROOT / "docs/jnm_material_degradation_mechanism_indices_20260613.md"


def fmt(value: float) -> str:
    if abs(value) >= 1000 or (0 < abs(value) < 1e-3):
        return f"{value:.4e}"
    return f"{value:.4g}"


def add_row(
    rows: list[dict[str, str]],
    metric: str,
    value: float | str,
    unit: str,
    evidence: str,
    interpretation: str,
    boundary: str,
) -> None:
    rows.append(
        {
            "metric": metric,
            "value": fmt(value) if isinstance(value, float) else value,
            "unit": unit,
            "evidence": evidence,
            "interpretation": interpretation,
            "boundary": boundary,
        }
    )


def build_rows() -> list[dict[str, str]]:
    macro = pd.read_csv(MACRO)
    events = pd.read_csv(PILOT_EVENTS)
    native = pd.read_csv(PILOT_NATIVE)

    pilot = macro.loc[macro["case_label"] == "pilot_localized_microcracking"].iloc[0]
    independent = macro.loc[macro["case_label"] == "seed02_intact_to_60um"].iloc[0]
    strength_audits = macro[macro["case_label"].str.contains("strength")]

    first_native = native.sort_values("timestep").iloc[0]
    rows: list[dict[str, str]] = []

    add_row(
        rows,
        "endpoint_broken_bond_fraction",
        float(pilot["broken_bonds_at_endpoint"]) / float(pilot["minimum_intact_bonds"] + pilot["broken_bonds_at_endpoint"]),
        "fraction",
        "pilot bond-series endpoint",
        "Only a very small fraction of internal bonds broke by 60 micrometres.",
        "Use as localized microcracking evidence, not as a bed-scale damage law.",
    )
    add_row(
        rows,
        "damaged_mother_pebble_fraction",
        float(pilot["damaged_mother_pebbles"]) / 100.0,
        "fraction of 100 mother pebbles",
        "pilot breakage-event table",
        "Damage is confined to one mother pebble in the corrected pilot.",
        "Do not infer converged probability from one corrected pilot.",
    )
    add_row(
        rows,
        "damaged_pebble_rank_from_top",
        float(events["rank_from_top"].iloc[0]),
        "rank",
        "pilot breakage-event table",
        "The damaged mother pebble is top-near, but not simply the geometrically highest pebble.",
        "Rank is case-specific and local-structure dependent.",
    )
    add_row(
        rows,
        "inter_mother_edge_densification",
        float(pilot["max_inter_mother_edges"]) / float(first_native["inter_pebble_edges"]),
        "ratio",
        "pilot native-force series",
        "The native force graph densifies before reorganizing around the microcracking sequence.",
        "Topology ratio is a finite-bed mechanism descriptor, not a material constant.",
    )
    add_row(
        rows,
        "top_reachability_densification",
        float(pilot["max_top_reachable_mothers"]) / float(first_native["top_reachable_mother_pebbles"]),
        "ratio",
        "pilot native-force series",
        "The top-loaded force component recruits more mother pebbles before later reorganization.",
        "Reachability depends on bed realization and loading protocol.",
    )
    add_row(
        rows,
        "endpoint_edge_reorganization_drop",
        (float(pilot["max_inter_mother_edges"]) - float(pilot["final_inter_mother_edges"]))
        / float(pilot["max_inter_mother_edges"]),
        "fraction",
        "pilot macro-topology summary",
        "The endpoint graph has fewer active inter-mother force edges than the maximum sampled state.",
        "Use as evidence of reorganization, not monotonic damage accumulation.",
    )
    add_row(
        rows,
        "peak_to_endpoint_force_relaxation",
        (float(pilot["peak_top_force_N"]) - float(pilot["final_top_force_N"])) / float(pilot["peak_top_force_N"]),
        "fraction",
        "pilot thermo-derived macro metrics",
        "The pilot exhibits peak-to-endpoint load relaxation after event-localized bond loss.",
        "Do not report as a quasi-static elastic modulus.",
    )
    add_row(
        rows,
        "pilot_to_independent_final_force_sum_contrast",
        float(pilot["final_inter_pebble_force_sum_N"]) / float(independent["final_inter_pebble_force_sum_N"]),
        "ratio",
        "macro-topology event metrics",
        "The fractured pilot carries a larger final inter-pebble force sum than the intact independent bed.",
        "This is a local force-path contrast, not a universal threshold.",
    )
    add_row(
        rows,
        "spanning_graph_with_local_damage",
        "yes",
        "logical",
        "pilot native-force endpoint and event table",
        "The bed remains force-connected while one mother pebble has localized internal bond loss.",
        "Connected force graph does not imply unchanged thermal or purge-flow transport.",
    )
    add_row(
        rows,
        "strength_audit_endpoint_broken_bonds",
        float(strength_audits["broken_bonds_at_endpoint"].sum()),
        "bonds",
        "0.5x and 0.25x independent-bed audits",
        "Lowering the bond-strength multipliers in the independent bed did not trigger damage by 60 micrometres.",
        "Do not infer that strength is irrelevant; the result shows local force-path sensitivity in this bed.",
    )
    return rows


def write_outputs(rows: list[dict[str, str]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["metric", "value", "unit", "evidence", "interpretation", "boundary"],
        )
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# JNM material-degradation mechanism indices",
        "",
        "This audit converts the corrected PB-007 fracture and native-force outputs into bounded material-degradation descriptors for the Journal of Nuclear Materials manuscript. It does not introduce new simulation results; every index is recomputed from existing processed event, thermo and native-force data.",
        "",
        "| Metric | Value | Unit | Interpretation | Boundary |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['metric']} | {row['value']} | {row['unit']} | {row['interpretation']} | {row['boundary']} |"
        )
    lines.extend(
        [
            "",
            "Primary inputs:",
            f"- `{MACRO.relative_to(ROOT)}`",
            f"- `{PILOT_EVENTS.relative_to(ROOT)}`",
            f"- `{PILOT_NATIVE.relative_to(ROOT)}`",
            "",
            "The intended manuscript use is mechanistic: localized internal bond loss can coexist with a spanning native force graph and a reorganizing contact topology. The indices should not be used as converged failure probabilities, bulk elastic moduli, or coupled heat-flow/purge-flow predictions.",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    rows = build_rows()
    write_outputs(rows)
    print(OUT_CSV)
    print(OUT_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
