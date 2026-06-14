#!/usr/bin/env python3
"""Summarize reduced-strength validation cases for SP-002-CAL1."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("SP-002-CAL1-orient-y", "y", 1.0, 90.0, 22.5),
    ("SP-002-CAL1-y-bulk80-weak20", "y", 80.0 / 90.0, 80.0, 20.0),
    ("SP-002-CAL1-y-bulk74-weak18p5", "y", 74.0 / 90.0, 74.0, 18.5),
    ("SP-002-CAL1-y-bulk70-weak17p5", "y", 70.0 / 90.0, 70.0, 17.5),
    ("SP-002-CWB-13-y-bulk55p07-weak13p767", "y", 55.069760 / 90.0, 55.069760, 13.767440),
]


def metrics(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        return {row["metric"]: row["value"] for row in csv.DictReader(f)}


def final_row(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-1]


def main() -> None:
    out = ROOT / "tables/sp002_strength_multiplier_validation.csv"
    fieldnames = [
        "case_id",
        "orientation_label",
        "strength_multiplier",
        "bulk_strength_MPa",
        "weak_strength_MPa",
        "peak_top_force_N",
        "peak_bottom_force_N",
        "first_break_displacement_mm",
        "fragment_count",
        "largest_fragment_particles",
        "second_fragment_particles",
        "single_particle_fragments",
        "largest_fragment_fraction",
        "second_fragment_fraction",
        "failure_mode_draft",
    ]
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for case_id, orientation, multiplier, bulk, weak in CASES:
            summary = metrics(ROOT / f"data/processed/{case_id}_summary.csv")
            fragments = final_row(ROOT / f"data/processed/{case_id}_fragments.csv")
            failure = final_row(ROOT / f"data/processed/{case_id}_failure_metrics.csv")
            writer.writerow(
                {
                    "case_id": case_id,
                    "orientation_label": orientation,
                    "strength_multiplier": f"{multiplier:.6f}",
                    "bulk_strength_MPa": f"{bulk:.6f}",
                    "weak_strength_MPa": f"{weak:.6f}",
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
    print(out)


if __name__ == "__main__":
    main()
