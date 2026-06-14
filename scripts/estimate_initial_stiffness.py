#!/usr/bin/env python3
"""Estimate initial post-contact stiffness from SP-002 thermo CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force-threshold", type=float, default=0.05)
    parser.add_argument("--points", type=int, default=6)
    args = parser.parse_args()

    rows = []
    with args.csv_path.open(newline="") as f:
        for row in csv.DictReader(f):
            force = abs(float(row["top_forc"]))
            disp_mm = float(row["top_disp"]) * 1e3
            if force >= args.force_threshold:
                rows.append((disp_mm, force))

    fit = rows[: args.points]
    if len(fit) < 2:
        stiffness = ""
        intercept = ""
    else:
        n = len(fit)
        sx = sum(x for x, _ in fit)
        sy = sum(y for _, y in fit)
        sxx = sum(x * x for x, _ in fit)
        sxy = sum(x * y for x, y in fit)
        denom = n * sxx - sx * sx
        stiffness = (n * sxy - sx * sy) / denom if denom else ""
        intercept = (sy - stiffness * sx) / n if stiffness != "" else ""

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["source_csv", str(args.csv_path)])
        writer.writerow(["force_threshold_N", args.force_threshold])
        writer.writerow(["fit_points", len(fit)])
        writer.writerow(["initial_stiffness_N_per_mm", stiffness])
        writer.writerow(["intercept_N", intercept])


if __name__ == "__main__":
    main()
