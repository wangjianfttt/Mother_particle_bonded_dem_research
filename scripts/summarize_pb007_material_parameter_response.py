#!/usr/bin/env python3
"""Summarize PB-007 material-parameter response cases.

The table produced here is a source-data bridge between the simulation matrix
and future manuscript figures. It records status for planned/running cases and
extracts fracture and force-network metrics only from postprocessed outputs.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT / "simulations" / "pebble_bed" / "PB-007" / "cases"
MATRIX = ROOT / "tables" / "pb007_material_parameter_matrix_20260704.csv"
OUT = ROOT / "tables" / "pb007_material_parameter_response.csv"
SUMMARY_OUT = ROOT / "tables" / "pb007_material_strength_matrix_summary.csv"
INITIAL_BONDS = 493_500


@dataclass(frozen=True)
class ResponseCase:
    case_label: str
    geometry_class: str
    strength_multiplier: float
    case_id: str
    manuscript_role: str


BASELINE_CASES = [
    ResponseCase(
        "seed02_nominal",
        "intact_geometry",
        1.0,
        "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02",
        "intact geometry baseline",
    ),
    ResponseCase(
        "seed02_strength0p5",
        "intact_geometry",
        0.5,
        "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02",
        "existing weakened-bond intact control",
    ),
    ResponseCase(
        "seed02_strength0p25",
        "intact_geometry",
        0.25,
        "PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02",
        "existing weakened-bond intact control",
    ),
    ResponseCase(
        "seed04_nominal",
        "early_cracking",
        1.0,
        "PB-007-bonded-steprelaxed-100-seed04-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed04",
        "nominal early-cracking baseline",
    ),
    ResponseCase(
        "seed06_nominal",
        "synchronous_cracking",
        1.0,
        "PB-007-bonded-steprelaxed-100-seed06-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed06",
        "nominal synchronous-cracking baseline",
    ),
]


def _matrix_cases() -> list[ResponseCase]:
    if not MATRIX.exists():
        return []
    rows: list[ResponseCase] = []
    with MATRIX.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                ResponseCase(
                    case_label=row["case_label"],
                    geometry_class=row["geometry_class"],
                    strength_multiplier=float(row["strength_multiplier"]),
                    case_id=row["case_id"],
                    manuscript_role=row["manuscript_role"],
                )
            )
    return rows


def _case_status(case_id: str) -> str:
    case_dir = CASES_DIR / case_id
    acceptance_path = ROOT / "tables" / f"pb007_{case_id}_acceptance_summary.csv"
    final_restart = case_dir / "post" / "seated_final.restart"
    log_path = case_dir / "log.liggghts"
    if acceptance_path.exists():
        return "completed_postprocessed"
    if final_restart.exists():
        return "completed_needs_postprocess"
    if log_path.exists():
        return "running_or_incomplete"
    if case_dir.exists():
        return "created_no_solver_log"
    return "not_started"


def _read_first_row(path: Path) -> pd.Series | None:
    if not path.exists() or path.stat().st_size == 0:
        return None
    df = pd.read_csv(path)
    if df.empty:
        return None
    return df.iloc[0]


def _acceptance_metrics(case_id: str) -> dict[str, object]:
    row = _read_first_row(ROOT / "tables" / f"pb007_{case_id}_acceptance_summary.csv")
    if row is None:
        return {}
    initial = int(float(row.get("initial_intact_bonds", INITIAL_BONDS)))
    minimum = int(float(row.get("minimum_intact_bonds", initial)))
    return {
        "final_displacement_um": float(row.get("final_top_displacement_um", float("nan"))),
        "final_top_force_N": float(row.get("final_top_force_N", float("nan"))),
        "final_kinetic_energy_J": float(row.get("final_kinetic_energy_J", float("nan"))),
        "initial_intact_bonds": initial,
        "minimum_intact_bonds": minimum,
        "broken_bonds_at_endpoint": initial - minimum,
        "no_bond_loss_over_run": int(minimum == initial),
        "last_valid_bond_step": int(float(row.get("last_valid_bond_step", 0))),
    }


def _native_metrics(case_id: str) -> dict[str, object]:
    row = _read_first_row(ROOT / "tables" / f"pb007_{case_id}_native_summary.csv")
    if row is None:
        return {}
    return {
        "final_inter_mother_edges": int(float(row.get("inter_pebble_edges", 0))),
        "final_inter_pebble_subcontacts": int(float(row.get("inter_pebble_subcontacts", 0))),
        "final_inter_pebble_force_sum_N": float(row.get("inter_pebble_force_sum_N", float("nan"))),
        "final_top_reachable_mothers": int(float(row.get("top_reachable_mother_pebbles", 0))),
        "final_bottom_reachable_from_top": int(float(row.get("bottom_mothers_reachable_from_top", 0))),
        "final_spanning_force_graph": int(float(row.get("spanning_force_graph", 0))),
    }


def _event_metrics(case_id: str) -> dict[str, object]:
    path = ROOT / "data" / "processed" / f"{case_id}_breakage_events.csv"
    if not path.exists() or path.stat().st_size == 0:
        return {
            "event_rows": 0,
            "first_event_displacement_um": pd.NA,
            "damaged_mother_pebbles": 0,
            "localized_broken_bonds": 0,
        }
    df = pd.read_csv(path)
    if df.empty:
        return {
            "event_rows": 0,
            "first_event_displacement_um": pd.NA,
            "damaged_mother_pebbles": 0,
            "localized_broken_bonds": 0,
        }
    for col in ["top_displacement_mm", "new_broken_bonds", "cumulative_broken_bonds", "pebble_id"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return {
        "event_rows": int(len(df)),
        "first_event_displacement_um": float(df["top_displacement_mm"].min() * 1000.0),
        "damaged_mother_pebbles": int(df["pebble_id"].nunique()),
        "localized_broken_bonds": int(df["cumulative_broken_bonds"].max()),
    }


def _thermo_metrics(case_id: str) -> dict[str, object]:
    path = ROOT / "data" / "processed" / f"{case_id}_thermo.csv"
    if not path.exists() or path.stat().st_size == 0:
        return {}
    df = pd.read_csv(path)
    for col in ["top_disp", "top_forc", "bond_int"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    valid = df[df["bond_int"] > 0].copy()
    if valid.empty:
        return {}
    valid["disp_um"] = valid["top_disp"] * 1.0e6
    valid["abs_top_force_N"] = valid["top_forc"].abs()
    damaged = valid[valid["bond_int"] < INITIAL_BONDS]
    return {
        "peak_top_force_N": float(valid["abs_top_force_N"].max()),
        "first_thermo_break_displacement_um": (
            float(damaged["disp_um"].iloc[0]) if not damaged.empty else pd.NA
        ),
    }


def main() -> int:
    rows = []
    for case in [*BASELINE_CASES, *_matrix_cases()]:
        row: dict[str, object] = {
            "case_label": case.case_label,
            "geometry_class": case.geometry_class,
            "strength_multiplier": case.strength_multiplier,
            "case_id": case.case_id,
            "case_status": _case_status(case.case_id),
            "manuscript_role": case.manuscript_role,
        }
        row.update(_acceptance_metrics(case.case_id))
        row.update(_native_metrics(case.case_id))
        row.update(_event_metrics(case.case_id))
        row.update(_thermo_metrics(case.case_id))
        rows.append(row)

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    summary_cols = [
        "case_label",
        "geometry_class",
        "strength_multiplier",
        "case_status",
        "final_displacement_um",
        "broken_bonds_at_endpoint",
        "first_event_displacement_um",
        "damaged_mother_pebbles",
        "final_inter_pebble_force_sum_N",
        "final_top_reachable_mothers",
        "final_bottom_reachable_from_top",
        "final_spanning_force_graph",
    ]
    summary = out[summary_cols].copy()
    summary = summary.sort_values(["geometry_class", "strength_multiplier"], ascending=[True, True])
    summary.to_csv(SUMMARY_OUT, index=False)
    print(OUT)
    print(SUMMARY_OUT)
    print(out[["case_label", "geometry_class", "strength_multiplier", "case_status"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
