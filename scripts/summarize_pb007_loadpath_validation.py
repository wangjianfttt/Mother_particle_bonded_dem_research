#!/usr/bin/env python3
"""Create a compact acceptance summary for a PB-007 load-path pilot."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thermo", type=Path, required=True)
    parser.add_argument("--native-summary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline-step", type=int, default=None)
    args = parser.parse_args()

    thermo_raw = pd.read_csv(args.thermo)
    thermo_raw.columns = [column.strip() for column in thermo_raw.columns]
    thermo = thermo_raw.drop_duplicates(subset="Step", keep="first").sort_values("Step")
    with args.native_summary.open(newline="") as handle:
        native = next(csv.DictReader(handle))

    intact = pd.to_numeric(thermo["bond_int"], errors="coerce")
    broken = pd.to_numeric(thermo["bond_bro"], errors="coerce")
    valid = intact > 0
    thermo_valid = thermo.loc[valid].copy()
    final_bond = thermo_valid.iloc[-1]
    final = thermo_raw.iloc[-1]
    top_disp_series = pd.to_numeric(thermo_valid["top_disp"], errors="coerce")
    top_force_series = pd.to_numeric(thermo_valid["top_forc"], errors="coerce").abs()
    if args.baseline_step is not None:
        baseline_candidates = thermo_valid.loc[thermo_valid["Step"] == args.baseline_step]
    else:
        baseline_candidates = thermo_valid.loc[(top_disp_series <= 0.0) & (top_force_series <= 1.0e-12)]
        if baseline_candidates.empty:
            baseline_candidates = thermo_valid.loc[top_disp_series <= 0.0]
    baseline = baseline_candidates.iloc[-1] if not baseline_candidates.empty else thermo_valid.iloc[0]
    top_force = abs(float(final["top_forc"]))
    bottom_force = abs(float(final["bottom_f"]))
    force_ratio = min(top_force, bottom_force) / max(top_force, bottom_force) if max(top_force, bottom_force) else 0.0
    side_force = float(final["side_for"]) if "side_for" in final and pd.notna(final["side_for"]) else float("nan")
    all_wall_force = float(final["all_wall"]) if "all_wall" in final and pd.notna(final["all_wall"]) else float("nan")
    baseline_bottom_force = float(baseline["bottom_f"]) if "bottom_f" in baseline else float("nan")
    baseline_side_force = float(baseline["side_for"]) if "side_for" in baseline and pd.notna(baseline["side_for"]) else float("nan")
    baseline_all_wall_force = (
        float(baseline["all_wall"]) if "all_wall" in baseline and pd.notna(baseline["all_wall"]) else float("nan")
    )
    incremental_bottom_force = float(final["bottom_f"]) - baseline_bottom_force
    incremental_side_force = side_force - baseline_side_force if pd.notna(side_force) and pd.notna(baseline_side_force) else float("nan")
    incremental_all_wall_force = (
        all_wall_force - baseline_all_wall_force
        if pd.notna(all_wall_force) and pd.notna(baseline_all_wall_force)
        else float("nan")
    )
    final_ke = float(final["KinEng"]) if "KinEng" in final and pd.notna(final["KinEng"]) else float("nan")
    net_wall_ratio = (
        abs(all_wall_force) / max(abs(top_force), abs(bottom_force), 1.0e-30)
        if pd.notna(all_wall_force)
        else float("nan")
    )
    incremental_balance_ratio = (
        abs(incremental_all_wall_force) / max(abs(top_force), 1.0e-30)
        if pd.notna(incremental_all_wall_force)
        else float("nan")
    )
    incremental_balance_residual_percent = (
        abs(abs(incremental_all_wall_force) - top_force) / max(top_force, 1.0e-30) * 100.0
        if pd.notna(incremental_all_wall_force)
        else float("nan")
    )

    summary = {
        "thermo_file": str(args.thermo),
        "baseline_step": int(baseline["Step"]),
        "initial_intact_bonds": int(intact[valid].iloc[0]),
        "minimum_intact_bonds": int(intact[valid].min()),
        "maximum_broken_bonds_per_output": int(broken.max()),
        "final_top_displacement_m": float(final["top_disp"]),
        "final_top_displacement_um": float(final["top_disp"]) * 1.0e6,
        "final_kinetic_energy_J": final_ke,
        "final_top_force_N": top_force,
        "final_bottom_force_N": bottom_force,
        "final_side_wall_force_z_N": side_force,
        "final_all_wall_force_z_N": all_wall_force,
        "final_reaction_balance_ratio": force_ratio,
        "final_net_wall_force_ratio": net_wall_ratio,
        "baseline_bottom_force_z_N": baseline_bottom_force,
        "baseline_side_wall_force_z_N": baseline_side_force,
        "baseline_all_wall_force_z_N": baseline_all_wall_force,
        "incremental_bottom_force_z_N": incremental_bottom_force,
        "incremental_side_wall_force_z_N": incremental_side_force,
        "incremental_all_wall_force_z_N": incremental_all_wall_force,
        "incremental_wall_balance_ratio": incremental_balance_ratio,
        "incremental_wall_balance_residual_percent": incremental_balance_residual_percent,
        "native_inter_pebble_edges": int(native["inter_pebble_edges"]),
        "native_top_reachable_mother_pebbles": int(native["top_reachable_mother_pebbles"]),
        "native_bottom_mothers_reachable_from_top": int(native["bottom_mothers_reachable_from_top"]),
        "native_spanning_force_graph": int(native["spanning_force_graph"]),
        "zero_pre_damage": int(intact[valid].min() == intact[valid].iloc[0] and broken.max() == 0),
        "last_valid_bond_step": int(final_bond["Step"]),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)
    print(args.output)


if __name__ == "__main__":
    main()
