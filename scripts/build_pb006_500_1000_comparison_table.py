#!/usr/bin/env python3
"""Build a conservative PB-006 500-vs-1000 onset comparison table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed500",
        type=Path,
        default=ROOT / "tables/pb006_seed01_seed02_seed03_summary.csv",
    )
    parser.add_argument(
        "--summary1000",
        type=Path,
        default=ROOT / "tables/pb006_1000_targeted_window_summary.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tables/pb006_500_vs_1000_onset_comparison.csv",
    )
    args = parser.parse_args()

    rows: list[dict[str, str | int | float]] = []
    for row in read_rows(args.seed500):
        rows.append(
            {
                "case": row["seed"],
                "mother_pebbles": 500,
                "endpoint_displacement_mm": 0.20,
                "output_mode": "full local-dump sequence",
                "localized_events": row["localized_events"],
                "localized_broken_bonds": row["localized_broken_bonds"],
                "broken_pebbles": row["broken_pebbles"],
                "first_break_displacement_mm": row["first_break_displacement_mm"],
                "first_break_pebble_id": row["first_break_pebble_id"],
                "final_top_force_N": row["final_top_force_N"],
                "top_bin_broken_bonds": row["top_bin_broken_bonds"],
                "second_bin_broken_bonds": row["second_bin_broken_bonds"],
                "interpretation": "500-pebble production statistic at 0.20 mm",
            }
        )

    row = read_rows(args.summary1000)[0]
    rows.append(
        {
            "case": "seed01-1000 targeted window",
            "mother_pebbles": 1000,
            "endpoint_displacement_mm": 0.10,
            "output_mode": "thermo scan plus targeted local-dump window",
            "localized_events": row["localized_events"],
            "localized_broken_bonds": row["localized_broken_bonds"],
            "broken_pebbles": row["broken_pebbles"],
            "first_break_displacement_mm": row["first_break_displacement_mm"],
            "first_break_pebble_id": row["first_break_pebble_id"],
            "final_top_force_N": row["final_top_force_N"],
            "top_bin_broken_bonds": row["top_bin_broken_bonds"],
            "second_bin_broken_bonds": row["second_bin_broken_bonds"],
            "interpretation": "1000-pebble short-displacement onset check",
        }
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(args.output)


if __name__ == "__main__":
    main()
