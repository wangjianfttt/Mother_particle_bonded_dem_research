#!/usr/bin/env python3
"""Build an orientation-conditioned strength sampling plan for SP-002."""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_MEAN_N = 17.364079
TARGET_WINDOW_LOW_N = 15.0
TARGET_WINDOW_HIGH_N = 22.0
SPREAD = 0.08


def read_orientation_rows() -> list[dict[str, str]]:
    with (ROOT / "tables/sp002_cal1_orientation_summary.csv").open(newline="") as f:
        return list(csv.DictReader(f))


def multiplier_for_quantile(center: float, q: float) -> float:
    # Symmetric bounded spread around the orientation-specific center.
    return center * (1.0 + SPREAD * (2.0 * q - 1.0))


def main() -> None:
    rows = read_orientation_rows()
    orientation_order = ["x", "xy30", "y", "xy45", "tilt_xz"]
    by_label = {row["orientation_label"]: row for row in rows}
    out_rows: list[dict[str, object]] = []
    sample_id = 1
    # Five orientations x five within-orientation quantiles = 25 samples.
    for q_index, q in enumerate([0.1, 0.3, 0.5, 0.7, 0.9], start=1):
        for orientation in orientation_order:
            row = by_label[orientation]
            baseline_force = float(row["peak_top_force_N"])
            center = TARGET_MEAN_N / baseline_force
            multiplier = multiplier_for_quantile(center, q)
            out_rows.append(
                {
                    "sample_id": sample_id,
                    "orientation_label": orientation,
                    "orientation_baseline_force_N": f"{baseline_force:.6f}",
                    "within_orientation_quantile": q,
                    "center_strength_multiplier": f"{center:.6f}",
                    "recommended_strength_multiplier": f"{multiplier:.6f}",
                    "bulk_strength_MPa_if_CAL1_bulk90": f"{90.0 * multiplier:.6f}",
                    "weakplane_strength_MPa_if_CAL1_weak22p5": f"{22.5 * multiplier:.6f}",
                    "expected_force_if_linear_N": f"{baseline_force * multiplier:.6f}",
                    "inside_target_window_if_linear": TARGET_WINDOW_LOW_N <= baseline_force * multiplier <= TARGET_WINDOW_HIGH_N,
                    "strategy_note": "Orientation-conditioned strength multiplier; 8% within-orientation spread around target-mean center.",
                }
            )
            sample_id += 1

    out = ROOT / "tables/orientation_conditioned_strength_sampling_plan.csv"
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        writer.writeheader()
        writer.writerows(out_rows)

    print(out)


if __name__ == "__main__":
    main()
