#!/usr/bin/env python3
"""Build event-aligned topology descriptors for the corrected PB-007 pilot.

The output is a compact, auditable table that links each mother-pebble
fracture-event window to the nearest measured native force-network states.
It only uses existing processed DEM outputs; it does not infer new breakage
events or synthesize missing simulation data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot"
EVENTS = ROOT / "data" / "processed" / f"{CASE_ID}_breakage_events.csv"
NATIVE_SERIES = ROOT / "data" / "processed" / f"{CASE_ID}_native_force_network_series.csv"
NATIVE_SUMMARY = ROOT / "tables" / f"pb007_{CASE_ID}_native_summary.csv"
THERMO = ROOT / "data" / "processed" / f"{CASE_ID}_thermo.csv"
OUT = ROOT / "tables" / "pb007_event_aligned_topology.csv"


def _load_native_states() -> pd.DataFrame:
    series = pd.read_csv(NATIVE_SERIES)
    summary = pd.read_csv(NATIVE_SUMMARY)

    # The final native summary does not carry a timestep column; it is the
    # compression endpoint for this 60 micrometre pilot.
    summary = summary.copy()
    summary["timestep"] = 130001
    summary["native_state"] = "final"
    series = series.copy()
    series["native_state"] = "periodic"

    keep = [
        "timestep",
        "native_state",
        "inter_pebble_edges",
        "inter_pebble_subcontacts",
        "inter_pebble_force_sum_N",
        "top_reachable_mother_pebbles",
        "bottom_mothers_reachable_from_top",
        "spanning_force_graph",
    ]
    for col in keep:
        if col not in summary:
            summary[col] = pd.NA
    native = pd.concat([series[keep], summary[keep]], ignore_index=True)
    for col in keep:
        if col not in {"native_state"}:
            native[col] = pd.to_numeric(native[col], errors="coerce")
    return native.sort_values("timestep").drop_duplicates("timestep", keep="last")


def _load_event_forces() -> pd.DataFrame:
    thermo = pd.read_csv(THERMO)
    for col in ["Step", "top_forc", "bond_int"]:
        thermo[col] = pd.to_numeric(thermo[col], errors="coerce")
    thermo = thermo.dropna(subset=["Step", "top_forc"])
    # Remove duplicated post-run rows with zero bond_int fields when possible.
    valid = thermo[(thermo["bond_int"].isna()) | (thermo["bond_int"] > 0)]
    if not valid.empty:
        thermo = valid
    return thermo.drop_duplicates("Step", keep="last").set_index("Step")


def _nearest_rows(native: pd.DataFrame, timestep: float) -> tuple[pd.Series, pd.Series]:
    before = native[native["timestep"] < timestep]
    after = native[native["timestep"] >= timestep]
    if before.empty:
        before_row = native.iloc[0]
    else:
        before_row = before.iloc[-1]
    if after.empty:
        after_row = native.iloc[-1]
    else:
        after_row = after.iloc[0]
    return before_row, after_row


def main() -> int:
    events = pd.read_csv(EVENTS)
    native = _load_native_states()
    thermo = _load_event_forces()

    for col in ["timestep", "top_displacement_mm", "new_broken_bonds", "cumulative_broken_bonds"]:
        events[col] = pd.to_numeric(events[col], errors="coerce")

    rows: list[dict[str, object]] = []
    for _, event in events.sort_values("timestep").iterrows():
        before, after = _nearest_rows(native, float(event["timestep"]))
        event_force = float(event["top_force_z_N"])
        if float(event["timestep"]) in thermo.index:
            event_force = float(thermo.loc[float(event["timestep"]), "top_forc"])
        rows.append(
            {
                "event_index": int(event["event_index"]),
                "event_timestep": int(event["timestep"]),
                "event_displacement_um": round(float(event["top_displacement_mm"]) * 1000.0, 6),
                "pebble_id": int(event["pebble_id"]),
                "rank_from_top": int(event["rank_from_top"]),
                "new_broken_bonds": int(event["new_broken_bonds"]),
                "cumulative_broken_bonds": int(event["cumulative_broken_bonds"]),
                "event_top_force_N": event_force,
                "previous_native_timestep": int(before["timestep"]),
                "next_native_timestep": int(after["timestep"]),
                "previous_inter_mother_edges": int(before["inter_pebble_edges"]),
                "next_inter_mother_edges": int(after["inter_pebble_edges"]),
                "delta_inter_mother_edges": int(after["inter_pebble_edges"] - before["inter_pebble_edges"]),
                "previous_top_reachable_mothers": int(before["top_reachable_mother_pebbles"]),
                "next_top_reachable_mothers": int(after["top_reachable_mother_pebbles"]),
                "delta_top_reachable_mothers": int(
                    after["top_reachable_mother_pebbles"] - before["top_reachable_mother_pebbles"]
                ),
                "previous_inter_pebble_force_sum_N": float(before["inter_pebble_force_sum_N"]),
                "next_inter_pebble_force_sum_N": float(after["inter_pebble_force_sum_N"]),
                "force_sum_ratio_next_to_previous": float(after["inter_pebble_force_sum_N"])
                / float(before["inter_pebble_force_sum_N"]),
                "spanning_graph_before": int(before["spanning_force_graph"]),
                "spanning_graph_after": int(after["spanning_force_graph"]),
                "mechanism_note": "localized bond loss embedded in a spanning native force graph",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
