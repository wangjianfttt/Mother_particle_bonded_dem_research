#!/usr/bin/env python3
"""Summarize completed orientation-conditioned SP-002 ensemble samples."""

from __future__ import annotations

import csv
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def metrics(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        return {row["metric"]: row["value"] for row in csv.DictReader(f)}


def final_row(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-1]


def read_plan() -> dict[str, dict[str, str]]:
    with (ROOT / "tables/orientation_conditioned_strength_sampling_plan.csv").open(newline="") as f:
        return {row["sample_id"]: row for row in csv.DictReader(f)}


def sample_id_from_case(case_id: str) -> str:
    return str(int(case_id.split("-")[3]))


def main() -> None:
    plan = read_plan()
    rows: list[dict[str, str]] = []
    for summary_path in sorted((ROOT / "data/processed").glob("SP-002-CWB-*_summary.csv")):
        case_id = summary_path.name.removesuffix("_summary.csv")
        sample_id = sample_id_from_case(case_id)
        if sample_id not in plan:
            continue
        fragment_path = ROOT / f"data/processed/{case_id}_fragments.csv"
        failure_path = ROOT / f"data/processed/{case_id}_failure_metrics.csv"
        if not fragment_path.exists() or not failure_path.exists():
            continue
        summary = metrics(summary_path)
        fragments = final_row(fragment_path)
        failure = final_row(failure_path)
        plan_row = plan[sample_id]
        rows.append(
            {
                "sample_id": sample_id,
                "case_id": case_id,
                "orientation_label": plan_row["orientation_label"],
                "recommended_strength_multiplier": plan_row["recommended_strength_multiplier"],
                "bulk_strength_MPa": plan_row["bulk_strength_MPa_if_CAL1_bulk90"],
                "weak_strength_MPa": plan_row["weakplane_strength_MPa_if_CAL1_weak22p5"],
                "expected_force_if_linear_N": plan_row["expected_force_if_linear_N"],
                "peak_top_force_N": summary["peak_top_force_N"],
                "peak_bottom_force_N": summary["peak_bottom_force_N"],
                "first_break_displacement_mm": summary["first_break_displacement_mm"],
                "fragment_count": fragments["fragment_count"],
                "largest_fragment_particles": fragments["largest_fragment_particles"],
                "second_fragment_particles": fragments["second_fragment_particles"],
                "single_particle_fragments": fragments["single_particle_fragments"],
                "largest_fragment_fraction": failure["largest_fragment_fraction"],
                "second_fragment_fraction": failure["second_fragment_fraction"],
                "failure_mode_draft": failure["failure_mode_draft"],
            }
        )

    out = ROOT / "tables/sp002_conditioned_ensemble_completed_summary.csv"
    if rows:
        with out.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    forces = [float(row["peak_top_force_N"]) for row in rows]
    stats_out = ROOT / "tables/sp002_conditioned_ensemble_completed_stats.csv"
    if forces:
        with stats_out.open("w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "completed_samples",
                    "peak_top_mean_N",
                    "peak_top_std_N",
                    "peak_top_min_N",
                    "peak_top_max_N",
                    "samples_in_15_22_N",
                ],
            )
            writer.writeheader()
            writer.writerow(
                {
                    "completed_samples": len(forces),
                    "peak_top_mean_N": statistics.mean(forces),
                    "peak_top_std_N": statistics.stdev(forces) if len(forces) > 1 else 0.0,
                    "peak_top_min_N": min(forces),
                    "peak_top_max_N": max(forces),
                    "samples_in_15_22_N": sum(15.0 <= f <= 22.0 for f in forces),
                }
            )

    print(out)
    print(stats_out)


if __name__ == "__main__":
    main()
