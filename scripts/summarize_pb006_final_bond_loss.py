#!/usr/bin/env python3
"""Summarize final internal bond loss by mother pebble from one PB-006 local dump."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


def read_internal_counts(path: Path, nspheres: int, npebbles: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    in_entries = False
    with path.open() as handle:
        for raw in handle:
            if not in_entries:
                if raw.startswith("ITEM: ENTRIES"):
                    in_entries = True
                continue
            parts = raw.split()
            if len(parts) < 2:
                continue
            atom_a = int(float(parts[0]))
            atom_b = int(float(parts[1]))
            pebble_a = (atom_a - 1) // nspheres + 1
            pebble_b = (atom_b - 1) // nspheres + 1
            if 1 <= pebble_a <= npebbles and pebble_a == pebble_b:
                counts[pebble_a] += 1
    return counts


def read_metadata(path: Path | None) -> dict[int, dict[str, str]]:
    if path is None or not path.exists():
        return {}
    with path.open(newline="") as handle:
        return {int(row["pebble_id"]): row for row in csv.DictReader(handle)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bond_dump", type=Path)
    parser.add_argument("--npebbles", type=int, required=True)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--initial-bonds-per-pebble", type=int, default=5876)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    counts = read_internal_counts(args.bond_dump, args.nspheres, args.npebbles)
    metadata = read_metadata(args.metadata)
    rows = []
    for pebble_id in range(1, args.npebbles + 1):
        intact = counts.get(pebble_id, 0)
        broken = max(0, args.initial_bonds_per_pebble - intact)
        meta = metadata.get(pebble_id, {})
        rows.append(
            {
                "pebble_id": pebble_id,
                "intact_internal_bonds": intact,
                "initial_internal_bonds": args.initial_bonds_per_pebble,
                "final_broken_internal_bonds": broken,
                "initial_x": meta.get("target_x", ""),
                "initial_y": meta.get("target_y", ""),
                "initial_z": meta.get("target_z", ""),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    damaged = [row for row in rows if row["final_broken_internal_bonds"] > 0]
    print(args.output)
    print(f"damaged_pebbles={len(damaged)}")
    print(f"final_broken_internal_bonds={sum(row['final_broken_internal_bonds'] for row in rows)}")


if __name__ == "__main__":
    main()
