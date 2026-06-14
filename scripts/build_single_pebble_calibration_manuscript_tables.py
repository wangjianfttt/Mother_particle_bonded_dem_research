#!/usr/bin/env python3
"""Build compact manuscript tables for single-pebble calibration evidence."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean, pstdev


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def fmt_range(values: list[float], digits: int = 2) -> str:
    return f"{min(values):.{digits}f}-{max(values):.{digits}f}"


def fmt_mean_sd(values: list[float], digits: int = 2) -> str:
    return f"{mean(values):.{digits}f} +/- {pstdev(values):.{digits}f}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--experimental",
        type=Path,
        default=ROOT / "tables/single_pebble_experimental_calibration_targets.csv",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=ROOT / "tables/single_pebble_model_calibration_matrix.csv",
    )
    parser.add_argument(
        "--orientation",
        type=Path,
        default=ROOT / "tables/sp002_cal1_orientation_summary.csv",
    )
    parser.add_argument(
        "--multiplier",
        type=Path,
        default=ROOT / "tables/sp002_strength_multiplier_validation.csv",
    )
    parser.add_argument(
        "--weibull",
        type=Path,
        default=ROOT / "tables/sp002_weibull_ensemble_completed_summary.csv",
    )
    parser.add_argument(
        "--target-output",
        type=Path,
        default=ROOT / "tables/single_pebble_calibration_target_evidence_summary.csv",
    )
    parser.add_argument(
        "--ensemble-output",
        type=Path,
        default=ROOT / "tables/single_pebble_model_ensemble_evidence_summary.csv",
    )
    args = parser.parse_args()

    target_rows = []
    for row in read_rows(args.experimental):
        if "Zhao" in row["source"]:
            evidence_class = "verified tabulated anchor"
            manuscript_role = "0.5 mm plate/environment sensitivity and Weibull-scale scatter"
        elif "Annabattula" in row["source"]:
            evidence_class = "digitized size-effect anchor"
            manuscript_role = "diameter trend; supports extrapolated 1.0 mm load window"
        elif "Lo Frano" in row["source"]:
            evidence_class = "near-size approximate anchor"
            manuscript_role = "near-size load/displacement and fragment-mode check"
        else:
            evidence_class = "near-neighbour numerical literature"
            manuscript_role = "failure-pattern context, not direct force calibration"
        target_rows.append(
            {
                "source": row["source"],
                "doi": row["doi"],
                "diameter_mm": row["diameter_mm"],
                "plate_environment": f"{row['plate_material']} / {row['environment']}",
                "mean_crush_load_N": row["mean_crush_load_N"],
                "std_crush_load_N": row["std_crush_load_N"],
                "weibull_m": row["weibull_m"],
                "sample_count": row["sample_count"],
                "fracture_displacement_mm": row["fracture_displacement_mm"],
                "fracture_mode": row["fracture_mode"],
                "evidence_class": evidence_class,
                "manuscript_role": manuscript_role,
            }
        )

    args.target_output.parent.mkdir(parents=True, exist_ok=True)
    with args.target_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(target_rows[0]))
        writer.writeheader()
        writer.writerows(target_rows)

    model_rows = read_rows(args.model)
    cal1 = next(row for row in model_rows if row["case_id"] == "SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm")
    homogeneous = next(row for row in model_rows if row["case_id"] == "SP-002-calib-kn1e14-120MPa-0p1ms")
    slow_summary_path = ROOT / "data/processed/SP-002-CAL1-slow0p05ms-0p3mm_summary.csv"
    slow_fragments_path = ROOT / "data/processed/SP-002-CAL1-slow0p05ms-0p3mm_fragments.csv"
    matched_summary_path = ROOT / "data/processed/SP-002-CAL1-matched0p10ms-0p3mm_summary.csv"
    matched_fragments_path = ROOT / "data/processed/SP-002-CAL1-matched0p10ms-0p3mm_fragments.csv"
    x_slow_summary_path = ROOT / "data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_summary.csv"
    x_slow_fragments_path = ROOT / "data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_fragments.csv"
    orient = read_rows(args.orientation)
    mult = read_rows(args.multiplier)
    weibull = read_rows(args.weibull)

    ensemble_rows = [
        {
            "case_set": "homogeneous load-matched candidate",
            "n_cases": 1,
            "peak_top_force_N": f"{f(homogeneous, 'peak_top_force_N'):.2f}",
            "first_break_displacement_mm": f"{f(homogeneous, 'first_break_displacement_mm'):.4f}",
            "fragment_signature": f"{homogeneous['largest_fragment_particles']} + {homogeneous['second_fragment_particles']} particles; {homogeneous['single_particle_fragments']} single-particle chips",
            "manuscript_status": "reject as final template because morphology is surface chipping",
        },
        {
            "case_set": "SP-002-CAL1 deterministic weak-plane candidate",
            "n_cases": 1,
            "peak_top_force_N": f"{f(cal1, 'peak_top_force_N'):.2f}",
            "first_break_displacement_mm": f"{f(cal1, 'first_break_displacement_mm'):.4f}",
            "fragment_signature": f"{cal1['largest_fragment_particles']} + {cal1['second_fragment_particles']} particles; {cal1['single_particle_fragments']} single-particle chips",
            "manuscript_status": "current calibration candidate for bed insertion",
        },
    ]

    if x_slow_summary_path.exists() and x_slow_fragments_path.exists():
        x_slow_summary = {row["metric"]: row["value"] for row in read_rows(x_slow_summary_path)}
        x_slow_fragments = read_rows(x_slow_fragments_path)[-1]
        ensemble_rows.append(
            {
                "case_set": "SP-002-CAL1 x-normal 0.05 m/s rate check",
                "n_cases": 1,
                "peak_top_force_N": f"{float(x_slow_summary['peak_top_force_N']):.2f}",
                "first_break_displacement_mm": f"{float(x_slow_summary['first_break_displacement_mm']):.4f}",
                "fragment_signature": (
                    f"{x_slow_fragments['largest_fragment_particles']} + "
                    f"{x_slow_fragments['second_fragment_particles']} particles; "
                    f"{x_slow_fragments['single_particle_fragments']} single-particle chips"
                ),
                "manuscript_status": "true CAL1 rate check; peak rises but remains in target window and split morphology persists",
            }
        )

    if matched_summary_path.exists() and matched_fragments_path.exists():
        matched_summary = {row["metric"]: row["value"] for row in read_rows(matched_summary_path)}
        matched_fragments = read_rows(matched_fragments_path)[-1]
        ensemble_rows.append(
            {
                "case_set": "SP-002 y-normal 0.10 m/s rerun",
                "n_cases": 1,
                "peak_top_force_N": f"{float(matched_summary['peak_top_force_N']):.2f}",
                "first_break_displacement_mm": f"{float(matched_summary['first_break_displacement_mm']):.4f}",
                "fragment_signature": (
                    f"{matched_fragments['largest_fragment_particles']} + "
                    f"{matched_fragments['second_fragment_particles']} particles; "
                    f"{matched_fragments['single_particle_fragments']} single-particle chips"
                ),
                "manuscript_status": "orientation-specific rate check; do not cite as x-normal CAL1 reproduction",
            }
        )

    if slow_summary_path.exists() and slow_fragments_path.exists():
        slow_summary = {row["metric"]: row["value"] for row in read_rows(slow_summary_path)}
        slow_fragments = read_rows(slow_fragments_path)[-1]
        ensemble_rows.append(
            {
                "case_set": "SP-002 y-normal 0.05 m/s rerun",
                "n_cases": 1,
                "peak_top_force_N": f"{float(slow_summary['peak_top_force_N']):.2f}",
                "first_break_displacement_mm": f"{float(slow_summary['first_break_displacement_mm']):.4f}",
                "fragment_signature": (
                    f"{slow_fragments['largest_fragment_particles']} + "
                    f"{slow_fragments['second_fragment_particles']} particles; "
                    f"{slow_fragments['single_particle_fragments']} single-particle chips"
                ),
                "manuscript_status": "orientation-specific rate check; matches y-normal 0.10 m/s branch",
            }
        )

    ensemble_rows.extend(
        [
            {
            "case_set": "CAL1 weak-plane orientation pilot",
            "n_cases": len(orient),
            "peak_top_force_N": fmt_range([f(row, "peak_top_force_N") for row in orient]),
            "first_break_displacement_mm": fmt_range([f(row, "first_break_displacement_mm") for row in orient], digits=4),
            "fragment_signature": "two major fragments in all cases; largest-pair sizes "
            + fmt_range([f(row, "largest_fragment_particles") for row in orient], digits=0)
            + " and "
            + fmt_range([f(row, "second_fragment_particles") for row in orient], digits=0),
            "manuscript_status": "pilot scatter evidence; not yet Weibull-calibrated",
        },
        {
            "case_set": "y-normal strength multiplier validation",
            "n_cases": len(mult),
            "peak_top_force_N": fmt_range([f(row, "peak_top_force_N") for row in mult]),
            "first_break_displacement_mm": fmt_range([f(row, "first_break_displacement_mm") for row in mult], digits=4),
            "fragment_signature": "two major fragments retained while strength scale changes",
            "manuscript_status": "validates sample-level strength scaling over one orientation",
        },
        {
            "case_set": "initial five-sample Weibull-conditioned trial",
            "n_cases": len(weibull),
            "peak_top_force_N": fmt_mean_sd([f(row, "peak_top_force_N") for row in weibull]),
            "first_break_displacement_mm": fmt_range([f(row, "first_break_displacement_mm") for row in weibull], digits=4),
            "fragment_signature": "two major fragments retained; one low-strength tilted case is more progressive",
            "manuscript_status": "early trial only; requires orientation-specific interpolation and more samples",
            },
        ]
    )

    with args.ensemble_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ensemble_rows[0]))
        writer.writeheader()
        writer.writerows(ensemble_rows)

    print(args.target_output)
    print(args.ensemble_output)


if __name__ == "__main__":
    main()
