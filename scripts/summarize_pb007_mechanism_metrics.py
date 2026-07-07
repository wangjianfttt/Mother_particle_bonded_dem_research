#!/usr/bin/env python3
"""Summarize PB-007 macro-response, event and force-network metrics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tables" / "pb007_macro_topology_event_metrics.csv"


@dataclass(frozen=True)
class Case:
    label: str
    case_id: str
    optional: bool = False


CASES = [
    Case(
        "pilot_localized_microcracking",
        "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot",
    ),
    Case(
        "seed02_intact_to_60um",
        "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02",
    ),
    Case(
        "seed03_delayed_microcracking_to_60um",
        "PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03",
    ),
    Case(
        "seed04_early_microcracking_to_60um",
        "PB-007-bonded-steprelaxed-100-seed04-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed04",
    ),
    Case(
        "seed06_synchronous_microcracking_to_60um",
        "PB-007-bonded-steprelaxed-100-seed06-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed06",
    ),
    Case(
        "seed02_strength0p5_intact_to_60um",
        "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02",
    ),
    Case(
        "seed02_strength0p25_intact_to_60um",
        "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02",
    ),
    Case(
        "seed09_200bed_intact_to_60um",
        "PB-007-bonded-steprelaxed-200-seed09-midbox-fast600ksettle-y1p5e10-10kstage-hold100-60um-fracture-200bed",
    ),
    Case(
        "seed09_200bed_strength0p25_to_60um",
        "PB-007-bonded-steprelaxed-200-seed09-midbox-fast600ksettle-60um-strength0p25-200bed",
        optional=True,
    ),
]


def _macro_curve(case_id: str, acceptance: pd.Series) -> pd.DataFrame:
    """Return a conservative displacement-force curve for macro metrics.

    The extracted validation curve already filters to rows with valid internal
    bond counts, avoiding duplicate local-dump rows that can have zero bond
    fields. A final acceptance endpoint is appended because no-hold final states
    can be represented by run-0 rows outside the valid-bond thermo subset.
    """

    curve_path = ROOT / "data" / "processed" / f"{case_id}_validation_curve.csv"
    if curve_path.exists():
        df = pd.read_csv(curve_path)
        for col in ["disp_um", "top_force_mN", "KinEng"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.rename(columns={"KinEng": "kinetic_energy_J"})
        df["top_force_N"] = df["top_force_mN"].abs() * 1.0e-3
    else:
        thermo_path = ROOT / "data" / "processed" / f"{case_id}_thermo.csv"
        df = pd.read_csv(thermo_path)
        for col in ["top_disp", "top_forc", "KinEng", "bond_int"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df[df["bond_int"] > 0].copy()
        df["disp_um"] = df["top_disp"] * 1.0e6
        df["top_force_N"] = df["top_forc"].abs()
        df = df.rename(columns={"KinEng": "kinetic_energy_J"})
    endpoint = pd.DataFrame(
        [
            {
                "disp_um": float(acceptance["final_top_displacement_um"]),
                "top_force_N": float(acceptance["final_top_force_N"]),
                "kinetic_energy_J": float(acceptance["final_kinetic_energy_J"]),
            }
        ]
    )
    df = pd.concat([df[["disp_um", "top_force_N", "kinetic_energy_J"]], endpoint], ignore_index=True)
    # For repeated displacement samples, keep the final sample for endpoint-like
    # behavior and avoid duplicate final dump amplification.
    df = df.dropna(subset=["disp_um", "top_force_N"]).drop_duplicates(subset="disp_um", keep="last")
    return df.sort_values("disp_um")


def _window_stiffness(df: pd.DataFrame, lo_um: float, hi_um: float) -> float:
    mask = (df["disp_um"] >= lo_um) & (df["disp_um"] <= hi_um)
    sub = df.loc[mask, ["disp_um", "top_force_N"]].dropna()
    if len(sub) < 2:
        return float("nan")
    x = sub["disp_um"].to_numpy(dtype=float) * 1.0e-6
    y = sub["top_force_N"].to_numpy(dtype=float)
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


def _event_metrics(case_id: str) -> dict[str, float | int | str]:
    path = ROOT / "data" / "processed" / f"{case_id}_breakage_events.csv"
    if not path.exists() or path.stat().st_size == 0:
        return {
            "event_rows": 0,
            "first_event_disp_um": np.nan,
            "last_event_disp_um": np.nan,
            "damaged_mother_pebbles": 0,
            "event_localized_broken_bonds": 0,
            "event_sequence": "none",
        }
    df = pd.read_csv(path)
    if df.empty:
        return {
            "event_rows": 0,
            "first_event_disp_um": np.nan,
            "last_event_disp_um": np.nan,
            "damaged_mother_pebbles": 0,
            "event_localized_broken_bonds": 0,
            "event_sequence": "none",
        }
    df["top_displacement_mm"] = pd.to_numeric(df["top_displacement_mm"], errors="coerce")
    df["new_broken_bonds"] = pd.to_numeric(df["new_broken_bonds"], errors="coerce")
    df["cumulative_broken_bonds"] = pd.to_numeric(df["cumulative_broken_bonds"], errors="coerce")
    df["pebble_id"] = pd.to_numeric(df["pebble_id"], errors="coerce")
    disp_um = df["top_displacement_mm"] * 1000.0
    by_disp = (
        df.assign(disp_um=disp_um)
        .groupby("disp_um", as_index=False)
        .agg(new_broken_bonds=("new_broken_bonds", "sum"))
        .sort_values("disp_um")
    )
    by_disp["cumulative_broken_bonds"] = by_disp["new_broken_bonds"].cumsum()
    sequence = ";".join(
        f"{d:.1f}um:+{int(n)}"
        for d, n in zip(by_disp["disp_um"].to_numpy(dtype=float), by_disp["new_broken_bonds"].to_numpy(dtype=float))
    )
    return {
        "event_rows": int(len(df)),
        "first_event_disp_um": float(disp_um.min()),
        "last_event_disp_um": float(disp_um.max()),
        "damaged_mother_pebbles": int(df["pebble_id"].nunique()),
        "event_localized_broken_bonds": int(by_disp["cumulative_broken_bonds"].max()),
        "event_sequence": sequence,
    }


def _first_thermo_break_disp_um(case_id: str, initial_bonds: int) -> float:
    path = ROOT / "data" / "processed" / f"{case_id}_thermo.csv"
    if not path.exists():
        return float("nan")
    df = pd.read_csv(path)
    for col in ["top_disp", "bond_int"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    valid = df[df["bond_int"] > 0].copy()
    damaged = valid[valid["bond_int"] < initial_bonds]
    if damaged.empty:
        return float("nan")
    return float(damaged["top_disp"].iloc[0] * 1.0e6)


def _native_metrics(case_id: str) -> dict[str, float | int]:
    series_path = ROOT / "data" / "processed" / f"{case_id}_native_force_network_series.csv"
    summary_path = ROOT / "tables" / f"pb007_{case_id}_native_summary.csv"
    frames = []
    if series_path.exists():
        series = pd.read_csv(series_path)
        frames.append(series)
    if summary_path.exists():
        summary = pd.read_csv(summary_path)
        # Keep matching column names for final-state aggregation.
        frames.append(summary)
    if not frames:
        return {}
    df = pd.concat(frames, ignore_index=True, sort=False)
    for col in [
        "inter_pebble_edges",
        "inter_pebble_subcontacts",
        "inter_pebble_force_sum_N",
        "top_reachable_mother_pebbles",
        "bottom_mothers_reachable_from_top",
        "spanning_force_graph",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    final = pd.read_csv(summary_path).iloc[0]
    return {
        "max_inter_mother_edges": int(df["inter_pebble_edges"].max()),
        "final_inter_mother_edges": int(final["inter_pebble_edges"]),
        "max_top_reachable_mothers": int(df["top_reachable_mother_pebbles"].max()),
        "final_top_reachable_mothers": int(final["top_reachable_mother_pebbles"]),
        "max_bottom_reachable_from_top": int(df["bottom_mothers_reachable_from_top"].max()),
        "final_bottom_reachable_from_top": int(final["bottom_mothers_reachable_from_top"]),
        "final_inter_pebble_force_sum_N": float(final["inter_pebble_force_sum_N"]),
        "final_spanning_force_graph": int(final["spanning_force_graph"]),
    }


def _acceptance_summary(case_id: str) -> pd.Series:
    return pd.read_csv(ROOT / "tables" / f"pb007_{case_id}_acceptance_summary.csv").iloc[0]


def _has_postprocessed_case(case_id: str) -> bool:
    required = [
        ROOT / "tables" / f"pb007_{case_id}_acceptance_summary.csv",
        ROOT / "tables" / f"pb007_{case_id}_native_summary.csv",
        ROOT / "data" / "processed" / f"{case_id}_thermo.csv",
        ROOT / "data" / "processed" / f"{case_id}_bond_series.csv",
        ROOT / "data" / "processed" / f"{case_id}_breakage_events.csv",
        ROOT / "data" / "processed" / f"{case_id}_native_force_network_series.csv",
    ]
    return all(path.exists() and path.stat().st_size > 0 for path in required)


def _mother_pebble_count(case_id: str) -> int:
    metadata_path = (
        ROOT
        / "simulations"
        / "pebble_bed"
        / "PB-007"
        / "cases"
        / case_id
        / "data"
        / "bonded_template_metadata.csv"
    )
    if metadata_path.exists():
        return int(len(pd.read_csv(metadata_path)))
    series_path = ROOT / "data" / "processed" / f"{case_id}_bond_series.csv"
    if series_path.exists():
        series = pd.read_csv(series_path, usecols=["pebble_id"])
        return int(series["pebble_id"].nunique())
    acceptance = _acceptance_summary(case_id)
    initial_bonds = int(acceptance["initial_intact_bonds"])
    return int(round(initial_bonds / 4935.0))


def main() -> None:
    rows = []
    for case in CASES:
        if case.optional and not _has_postprocessed_case(case.case_id):
            print(f"skip optional unprocessed case: {case.case_id}")
            continue
        acceptance = _acceptance_summary(case.case_id)
        initial_bonds = int(acceptance["initial_intact_bonds"])
        mother_count = _mother_pebble_count(case.case_id)
        thermo = _macro_curve(case.case_id, acceptance)
        peak_idx = thermo["top_force_N"].idxmax()
        peak = thermo.loc[peak_idx]
        row: dict[str, float | int | str] = {
            "case_label": case.label,
            "case_id": case.case_id,
            "final_displacement_um": float(acceptance["final_top_displacement_um"]),
            "final_top_force_N": float(acceptance["final_top_force_N"]),
            "peak_top_force_N": float(peak["top_force_N"]),
            "peak_force_displacement_um": float(peak["disp_um"]),
            "mother_pebble_count": mother_count,
            "initial_internal_bonds": initial_bonds,
            "secant_stiffness_0_20um_N_per_m": _window_stiffness(thermo, 0.0, 20.0),
            "secant_stiffness_20_40um_N_per_m": _window_stiffness(thermo, 20.0, 40.0),
            "secant_stiffness_40_60um_N_per_m": _window_stiffness(thermo, 40.0, 60.0),
            "minimum_intact_bonds": int(acceptance["minimum_intact_bonds"]),
            "broken_bonds_at_endpoint": int(initial_bonds - acceptance["minimum_intact_bonds"]),
            "first_thermo_break_disp_um": _first_thermo_break_disp_um(case.case_id, initial_bonds),
        }
        row.update(_event_metrics(case.case_id))
        row.update(_native_metrics(case.case_id))
        rows.append(row)
    out = pd.DataFrame(rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUTPUT, index=False)
    print(OUTPUT)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
