#!/usr/bin/env python3
"""Summarize bed breakage events by pebble layer for regular beds."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def layer_index_for_pebble(pebble_id: int, nx: int, ny: int, nz: int) -> int | None:
    pebbles_per_layer = nx * ny
    max_pebbles = pebbles_per_layer * nz
    if not (1 <= pebble_id <= max_pebbles):
        return None
    return (pebble_id - 1) // pebbles_per_layer + 1


def layer_name(layer_index: int, nz: int) -> str:
    if layer_index == 1:
        return "bottom"
    if layer_index == nz:
        return "top"
    return f"middle_{layer_index}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("events_csv", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--nx", type=int, default=2)
    parser.add_argument("--ny", type=int, default=2)
    parser.add_argument("--nz", type=int, default=3)
    args = parser.parse_args()

    rows = list(csv.DictReader(args.events_csv.open()))
    by_layer: dict[str, dict[str, object]] = {}
    broken_by_layer = defaultdict(int)
    event_count_by_layer = defaultdict(int)
    first_by_layer: dict[str, dict[str, str]] = {}
    for row in rows:
        layer_index = layer_index_for_pebble(int(row["pebble_id"]), args.nx, args.ny, args.nz)
        layer = "unknown" if layer_index is None else layer_name(layer_index, args.nz)
        broken_by_layer[layer] += int(row["new_broken_bonds"])
        event_count_by_layer[layer] += 1
        first_by_layer.setdefault(layer, row)

    out_rows = []
    layer_order = [layer_name(i, args.nz) for i in range(args.nz, 0, -1)]
    if "unknown" in event_count_by_layer:
        layer_order.append("unknown")
    for layer in layer_order:
        first = first_by_layer.get(layer, {})
        out_rows.append(
            {
                "layer": layer,
                "nx": args.nx,
                "ny": args.ny,
                "nz": args.nz,
                "event_count": event_count_by_layer[layer],
                "total_new_broken_bonds": broken_by_layer[layer],
                "first_event_timestep": first.get("timestep", ""),
                "first_event_top_displacement_mm": first.get("top_displacement_mm", ""),
                "first_event_pebble_id": first.get("pebble_id", ""),
                "first_event_new_broken_bonds": first.get("new_broken_bonds", ""),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        writer.writeheader()
        writer.writerows(out_rows)
    print(args.output)


if __name__ == "__main__":
    main()
