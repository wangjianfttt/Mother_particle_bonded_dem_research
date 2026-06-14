#!/usr/bin/env python3
"""Summarize random-pack breakage events by initial height bins."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def load_metadata(path: Path) -> dict[int, dict[str, float]]:
    out = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            pid = int(row["pebble_id"])
            x = float(row["target_x"])
            y = float(row["target_y"])
            z = float(row["target_z"])
            out[pid] = {"x": x, "y": y, "z": z, "r": (x * x + y * y) ** 0.5}
    return out


def height_bin(z: float, zmin: float, zmax: float, nbins: int) -> int:
    if zmax <= zmin:
        return 1
    raw = int((z - zmin) / (zmax - zmin) * nbins) + 1
    return max(1, min(nbins, raw))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("events_csv", type=Path)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--height-bins", type=int, default=8)
    parser.add_argument("--pebble-output", type=Path, required=True)
    parser.add_argument("--height-output", type=Path, required=True)
    args = parser.parse_args()

    meta = load_metadata(args.metadata)
    zs = [row["z"] for row in meta.values()]
    zmin, zmax = min(zs), max(zs)

    pebble_rows = {
        pid: {
            "pebble_id": pid,
            "initial_x": vals["x"],
            "initial_y": vals["y"],
            "initial_z": vals["z"],
            "initial_radius_xy": vals["r"],
            "height_bin": height_bin(vals["z"], zmin, zmax, args.height_bins),
            "event_count": 0,
            "total_new_broken_bonds": 0,
            "first_event_timestep": "",
            "first_event_top_displacement_mm": "",
            "first_event_force_N": "",
            "last_event_top_displacement_mm": "",
        }
        for pid, vals in meta.items()
    }
    height_acc = defaultdict(lambda: {"event_count": 0, "total_new_broken_bonds": 0, "first": None})

    with args.events_csv.open(newline="") as f:
        for event in csv.DictReader(f):
            pid = int(event["pebble_id"])
            if pid not in pebble_rows:
                continue
            broken = int(event["new_broken_bonds"])
            row = pebble_rows[pid]
            row["event_count"] += 1
            row["total_new_broken_bonds"] += broken
            if row["first_event_timestep"] == "":
                row["first_event_timestep"] = event["timestep"]
                row["first_event_top_displacement_mm"] = event["top_displacement_mm"]
                row["first_event_force_N"] = event["top_force_z_N"]
            row["last_event_top_displacement_mm"] = event["top_displacement_mm"]

            hb = row["height_bin"]
            height_acc[hb]["event_count"] += 1
            height_acc[hb]["total_new_broken_bonds"] += broken
            if height_acc[hb]["first"] is None:
                height_acc[hb]["first"] = event

    pebble_out = sorted(pebble_rows.values(), key=lambda r: int(r["pebble_id"]))
    args.pebble_output.parent.mkdir(parents=True, exist_ok=True)
    with args.pebble_output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(pebble_out[0]))
        writer.writeheader()
        writer.writerows(pebble_out)

    height_rows = []
    for hb in range(args.height_bins, 0, -1):
        first = height_acc[hb]["first"] or {}
        height_rows.append(
            {
                "height_bin": hb,
                "zmin": zmin,
                "zmax": zmax,
                "event_count": height_acc[hb]["event_count"],
                "total_new_broken_bonds": height_acc[hb]["total_new_broken_bonds"],
                "first_event_timestep": first.get("timestep", ""),
                "first_event_top_displacement_mm": first.get("top_displacement_mm", ""),
                "first_event_pebble_id": first.get("pebble_id", ""),
                "first_event_new_broken_bonds": first.get("new_broken_bonds", ""),
            }
        )
    with args.height_output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(height_rows[0]))
        writer.writeheader()
        writer.writerows(height_rows)

    print(args.pebble_output)
    print(args.height_output)


if __name__ == "__main__":
    main()
