#!/usr/bin/env python3
"""Relate PB-006 packing geometry to localized breakage outcomes."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def load_pebbles(path: Path) -> list[dict[str, float]]:
    rows = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            rows.append(
                {
                    "pebble_id": int(row["pebble_id"]),
                    "x": float(row["initial_x"]),
                    "y": float(row["initial_y"]),
                    "z": float(row["initial_z"]),
                    "height_bin": int(row["height_bin"]),
                    "event_count": int(row["event_count"]),
                    "broken": int(row["total_new_broken_bonds"]),
                    "first_disp": row["first_event_top_displacement_mm"],
                }
            )
    return rows


def load_events(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def median(values: list[float]) -> float:
    if not values:
        return 0.0
    vals = sorted(values)
    n = len(vals)
    mid = n // 2
    if n % 2:
        return vals[mid]
    return 0.5 * (vals[mid - 1] + vals[mid])


def compute_degrees(pebbles: list[dict[str, float]], cutoff_m: float) -> dict[int, int]:
    degrees = {int(p["pebble_id"]): 0 for p in pebbles}
    for i, a in enumerate(pebbles):
        for b in pebbles[i + 1 :]:
            dx = a["x"] - b["x"]
            dy = a["y"] - b["y"]
            dz = a["z"] - b["z"]
            if dx * dx + dy * dy + dz * dz <= cutoff_m * cutoff_m:
                degrees[int(a["pebble_id"])] += 1
                degrees[int(b["pebble_id"])] += 1
    return degrees


def summarize_seed(label: str, pebbles: list[dict[str, float]], events: list[dict[str, str]], cutoff_m: float) -> tuple[dict[str, object], list[dict[str, object]]]:
    degrees = compute_degrees(pebbles, cutoff_m)
    z_sorted = sorted(pebbles, key=lambda p: p["z"], reverse=True)
    z_rank = {int(p["pebble_id"]): rank for rank, p in enumerate(z_sorted, start=1)}
    zmin = min(p["z"] for p in pebbles)
    zmax = max(p["z"] for p in pebbles)
    top_bin = max(int(p["height_bin"]) for p in pebbles)
    top_pebbles = [p for p in pebbles if int(p["height_bin"]) == top_bin]
    active = [p for p in pebbles if int(p["broken"]) > 0]
    top10 = z_sorted[: max(1, int(0.10 * len(z_sorted)))]
    top5 = z_sorted[:5]

    first = events[0] if events else {}
    first_pid = int(first.get("pebble_id", 0) or 0)
    first_row = next((p for p in pebbles if int(p["pebble_id"]) == first_pid), None)

    contact_count = sum(degrees.values()) // 2
    row = {
        "seed": label,
        "npebbles": len(pebbles),
        "cutoff_mm": cutoff_m * 1000.0,
        "bed_height_mm": (zmax - zmin) * 1000.0,
        "zmax_mm": zmax * 1000.0,
        "top_bin_count": len(top_pebbles),
        "geometric_contact_count": contact_count,
        "global_mean_degree": mean(list(degrees.values())),
        "global_median_degree": median(list(degrees.values())),
        "top_bin_mean_degree": mean([degrees[int(p["pebble_id"])] for p in top_pebbles]),
        "top_bin_median_degree": median([degrees[int(p["pebble_id"])] for p in top_pebbles]),
        "top10pct_mean_degree": mean([degrees[int(p["pebble_id"])] for p in top10]),
        "top5_ids": ";".join(str(int(p["pebble_id"])) for p in top5),
        "top5_mean_degree": mean([degrees[int(p["pebble_id"])] for p in top5]),
        "active_pebbles": len(active),
        "active_mean_degree": mean([degrees[int(p["pebble_id"])] for p in active]),
        "active_median_zrank": median([z_rank[int(p["pebble_id"])] for p in active]),
        "localized_broken_bonds": sum(int(p["broken"]) for p in pebbles),
        "first_break_pebble": first_pid,
        "first_break_zrank": z_rank.get(first_pid, ""),
        "first_break_degree": degrees.get(first_pid, ""),
        "first_break_height_bin": int(first_row["height_bin"]) if first_row else "",
        "first_break_displacement_mm": first.get("top_displacement_mm", ""),
        "first_event_new_broken_bonds": first.get("new_broken_bonds", ""),
    }

    active_rows = []
    for p in sorted(active, key=lambda item: (-int(item["broken"]), int(item["pebble_id"]))):
        pid = int(p["pebble_id"])
        active_rows.append(
            {
                "seed": label,
                "pebble_id": pid,
                "broken_bonds": int(p["broken"]),
                "event_count": int(p["event_count"]),
                "height_bin": int(p["height_bin"]),
                "zrank": z_rank[pid],
                "z_mm": p["z"] * 1000.0,
                "degree": degrees[pid],
                "first_event_top_displacement_mm": p["first_disp"],
            }
        )
    return row, active_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        action="append",
        required=True,
        help="label:pebble_summary.csv:breakage_events.csv",
    )
    parser.add_argument("--cutoff-mm", type=float, default=1.02)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--active-output", type=Path, required=True)
    args = parser.parse_args()

    summary_rows = []
    active_rows = []
    cutoff_m = args.cutoff_mm / 1000.0
    for spec in args.seed:
        label, pebble_path, event_path = spec.split(":", 2)
        row, active = summarize_seed(label, load_pebbles(Path(pebble_path)), load_events(Path(event_path)), cutoff_m)
        summary_rows.append(row)
        active_rows.extend(active)

    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)

    with args.active_output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(active_rows[0]))
        writer.writeheader()
        writer.writerows(active_rows)

    print(args.summary_output)
    print(args.active_output)


if __name__ == "__main__":
    main()
