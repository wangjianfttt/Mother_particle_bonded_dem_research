#!/usr/bin/env python3
"""Recommend local-dump windows from PB-006 thermo bond-break increments."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def as_int(value: str | None) -> int | None:
    val = as_float(value)
    return int(val) if val is not None else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("thermo", type=Path)
    parser.add_argument("--margin-mm", type=float, default=0.01)
    parser.add_argument("--merge-gap-mm", type=float, default=0.015)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    events = []
    cumulative = 0
    for row in rows(args.thermo):
        increment = as_int(row.get("bond_bro"))
        disp_m = as_float(row.get("top_disp"))
        step = as_int(row.get("Step"))
        force = as_float(row.get("top_forc"))
        if increment is None or increment <= 0 or disp_m is None:
            continue
        cumulative += increment
        events.append(
            {
                "step": step,
                "top_displacement_mm": disp_m * 1000.0,
                "new_broken_bonds": increment,
                "cumulative_broken_bonds_seen_in_thermo": cumulative,
                "top_force_N": force if force is not None else "",
            }
        )

    windows = []
    current = None
    for event in events:
        start = max(0.0, event["top_displacement_mm"] - args.margin_mm)
        end = event["top_displacement_mm"] + args.margin_mm
        if current is None:
            current = {
                "window_index": 1,
                "start_mm": start,
                "end_mm": end,
                "first_event_mm": event["top_displacement_mm"],
                "last_event_mm": event["top_displacement_mm"],
                "thermo_event_count": 1,
                "thermo_broken_bonds": event["new_broken_bonds"],
            }
            continue
        if start <= current["end_mm"] + args.merge_gap_mm:
            current["end_mm"] = max(current["end_mm"], end)
            current["last_event_mm"] = event["top_displacement_mm"]
            current["thermo_event_count"] += 1
            current["thermo_broken_bonds"] += event["new_broken_bonds"]
        else:
            windows.append(current)
            current = {
                "window_index": len(windows) + 1,
                "start_mm": start,
                "end_mm": end,
                "first_event_mm": event["top_displacement_mm"],
                "last_event_mm": event["top_displacement_mm"],
                "thermo_event_count": 1,
                "thermo_broken_bonds": event["new_broken_bonds"],
            }
    if current is not None:
        windows.append(current)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "window_index",
        "start_mm",
        "end_mm",
        "first_event_mm",
        "last_event_mm",
        "thermo_event_count",
        "thermo_broken_bonds",
    ]
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(windows)

    print(args.output)
    print(f"thermo_events={len(events)}")
    print(f"recommended_windows={len(windows)}")


if __name__ == "__main__":
    main()
