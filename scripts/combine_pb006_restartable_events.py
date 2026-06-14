#!/usr/bin/env python3
"""Combine early 1000-pebble onset events with restartable late-window events."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing event file: {path}")
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--early-events", type=Path, required=True)
    parser.add_argument("--late-events", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    fieldnames = [
        "event_index",
        "timestep",
        "pebble_id",
        "new_broken_bonds",
        "cumulative_broken_bonds",
        "top_displacement_m",
        "top_displacement_mm",
        "top_force_z_N",
        "bottom_force_z_N",
    ]

    early = read_rows(args.early_events)
    late = read_rows(args.late_events)
    max_early_displacement = max((float(row["top_displacement_mm"]) for row in early), default=-1.0)

    base_by_pebble: dict[int, int] = {}
    combined: list[dict[str, object]] = []
    for row in early:
        pebble = int(float(row["pebble_id"]))
        cumulative = int(float(row["cumulative_broken_bonds"]))
        base_by_pebble[pebble] = max(base_by_pebble.get(pebble, 0), cumulative)
        combined.append({key: row.get(key, "") for key in fieldnames})

    for row in late:
        if float(row["top_displacement_mm"]) <= max_early_displacement:
            continue
        pebble = int(float(row["pebble_id"]))
        base = base_by_pebble.get(pebble, 0)
        adjusted = {key: row.get(key, "") for key in fieldnames}
        adjusted["cumulative_broken_bonds"] = base + int(float(row["cumulative_broken_bonds"]))
        combined.append(adjusted)

    combined.sort(key=lambda row: (float(row["top_displacement_mm"]), int(float(row["timestep"])), int(float(row["pebble_id"]))))
    for index, row in enumerate(combined, start=1):
        row["event_index"] = index

    write_rows(args.output, combined, fieldnames)
    print(args.output)


if __name__ == "__main__":
    main()
