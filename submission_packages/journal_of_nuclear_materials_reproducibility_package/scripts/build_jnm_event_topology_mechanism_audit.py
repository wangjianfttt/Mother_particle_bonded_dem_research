#!/usr/bin/env python3
"""Build an event-aligned topology mechanism audit for the JNM manuscript."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_TOPOLOGY = ROOT / "tables/pb007_event_aligned_topology.csv"
INDICES = ROOT / "tables/jnm_material_degradation_mechanism_indices.csv"
OUT = ROOT / "docs/jnm_event_topology_mechanism_audit_20260613.md"


def read_rows(path: Path) -> list[dict[str, str]]:
    rows = list(csv.DictReader(path.open()))
    if not rows:
        raise ValueError(f"{path} has no rows")
    return rows


def fmt(value: str, digits: int = 3) -> str:
    number = float(value)
    if abs(number) >= 10:
        return f"{number:.1f}"
    return f"{number:.{digits}g}"


def main() -> int:
    events = read_rows(EVENT_TOPOLOGY)
    indices = {row["metric"]: row for row in read_rows(INDICES)}
    lines = [
        "# Event-aligned topology mechanism audit",
        "",
        "This audit connects the localized internal-bond-loss events used in Fig. 5 and Table 1 to the nearest native force-network states. It is generated from `tables/pb007_event_aligned_topology.csv` and `tables/jnm_material_degradation_mechanism_indices.csv`; no additional data are inferred.",
        "",
        "## Event sequence and force-network state",
        "",
        "| Event | Displacement (um) | New broken bonds | Mother pebble | Rank from top | Inter-mother edges before -> after | Top-reachable mothers before -> after | Inter-pebble force sum before -> after (N) | Spanning graph |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in events:
        lines.append(
            "| "
            f"{row['event_index']} | "
            f"{fmt(row['event_displacement_um'])} | "
            f"{row['new_broken_bonds']} | "
            f"{row['pebble_id']} | "
            f"{row['rank_from_top']} | "
            f"{row['previous_inter_mother_edges']} -> {row['next_inter_mother_edges']} "
            f"(Delta {row['delta_inter_mother_edges']}) | "
            f"{row['previous_top_reachable_mothers']} -> {row['next_top_reachable_mothers']} "
            f"(Delta {row['delta_top_reachable_mothers']}) | "
            f"{fmt(row['previous_inter_pebble_force_sum_N'])} -> {fmt(row['next_inter_pebble_force_sum_N'])} | "
            f"{row['spanning_graph_before']} -> {row['spanning_graph_after']} |"
        )
    lines.extend(
        [
            "",
            "## Mechanistic interpretation",
            "",
            "- All three localized bond-loss increments occur in mother pebble 78, a top-near pebble with rank-from-top 2.",
            "- The native force graph is already spanning before every localized event and remains spanning after every localized event.",
            "- The first two event windows coincide with recruitment of additional inter-mother force edges and top-reachable mother pebbles, whereas the final event occurs after a partial network reorganization.",
            "- The endpoint broken-bond fraction remains small, but the event windows are embedded in measurable force-network densification and load redistribution.",
            "",
            "## Quantitative mechanism indices",
            "",
            "| Metric | Value | Interpretation | Boundary |",
            "| --- | ---: | --- | --- |",
        ]
    )
    selected = [
        "endpoint_broken_bond_fraction",
        "damaged_mother_pebble_fraction",
        "inter_mother_edge_densification",
        "top_reachability_densification",
        "endpoint_edge_reorganization_drop",
        "peak_to_endpoint_force_relaxation",
        "pilot_to_independent_final_force_sum_contrast",
        "spanning_graph_with_local_damage",
    ]
    for metric in selected:
        row = indices[metric]
        lines.append(
            f"| {metric} | {row['value']} | {row['interpretation']} | {row['boundary']} |"
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This audit supports a bounded materials-degradation mechanism: early breeder-pebble microcracking can be localized while the native contact-force network remains globally connected and reorganizes. It does not establish a converged fracture probability, a bulk elastic modulus, a blanket lifetime estimate or a coupled thermal-flow prediction.",
            "",
        ]
    )
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
