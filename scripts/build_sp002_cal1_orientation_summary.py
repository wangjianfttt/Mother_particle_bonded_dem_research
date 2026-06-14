#!/usr/bin/env python3
"""Summarize SP-002-CAL1 weak-plane orientation cases."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CASES = [
    ("SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm", "x", "1,0,0"),
    ("SP-002-CAL1-orient-xy30", "xy30", "0.866,0.5,0"),
    ("SP-002-CAL1-orient-y", "y", "0,1,0"),
    ("SP-002-CAL1-orient-xy45", "xy45", "1,1,0"),
    ("SP-002-CAL1-orient-tilt", "tilt_xz", "1,0,0.5"),
]


def metrics(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        return {row["metric"]: row["value"] for row in csv.DictReader(f)}


def final_row(path: Path) -> dict[str, str]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-1]


def main() -> None:
    out = ROOT / "tables/sp002_cal1_orientation_summary.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "case_id",
        "orientation_label",
        "normal_vector",
        "peak_top_force_N",
        "peak_bottom_force_N",
        "first_break_displacement_mm",
        "final_broken_bonds",
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
        for case_id, label, normal in CASES:
            summary = metrics(ROOT / f"data/processed/{case_id}_summary.csv")
            fragments = final_row(ROOT / f"data/processed/{case_id}_fragments.csv")
            failure = final_row(ROOT / f"data/processed/{case_id}_failure_metrics.csv")
            writer.writerow(
                {
                    "case_id": case_id,
                    "orientation_label": label,
                    "normal_vector": normal,
                    "peak_top_force_N": summary["peak_top_force_N"],
                    "peak_bottom_force_N": summary["peak_bottom_force_N"],
                    "first_break_displacement_mm": summary["first_break_displacement_mm"],
                    "final_broken_bonds": summary["final_broken_bonds"],
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
