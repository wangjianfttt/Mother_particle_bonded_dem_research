#!/usr/bin/env python3
"""Extract the last-frame proxy sphere centres from a LIGGGHTS dump."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def read_last_frame(path: Path) -> tuple[int, list[str], list[dict[str, str]]]:
    lines = path.read_text().splitlines()
    i = 0
    last_step = 0
    last_fields: list[str] = []
    last_rows: list[dict[str, str]] = []
    while i < len(lines):
        if lines[i] != "ITEM: TIMESTEP":
            i += 1
            continue
        step = int(lines[i + 1])
        if lines[i + 2] != "ITEM: NUMBER OF ATOMS":
            raise ValueError(f"Unexpected dump format near line {i + 3}")
        n_atoms = int(lines[i + 3])
        atoms_header = i + 8
        if not lines[atoms_header].startswith("ITEM: ATOMS"):
            raise ValueError(f"Could not find ITEM: ATOMS near timestep {step}")
        fields = lines[atoms_header].split()[2:]
        rows = []
        for line in lines[atoms_header + 1 : atoms_header + 1 + n_atoms]:
            values = line.split()
            rows.append(dict(zip(fields, values)))
        last_step, last_fields, last_rows = step, fields, rows
        i = atoms_header + 1 + n_atoms
    if not last_rows:
        raise SystemExit(f"No frames found in {path}")
    return last_step, last_fields, last_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dump", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--sort", choices=["id", "zyx"], default="zyx")
    args = parser.parse_args()

    step, fields, rows = read_last_frame(args.dump)
    required = {"id", "x", "y", "z", "radius"}
    missing = required - set(fields)
    if missing:
        raise SystemExit(f"Dump is missing required fields: {sorted(missing)}")

    if args.sort == "zyx":
        rows.sort(key=lambda r: (float(r["z"]), float(r["y"]), float(r["x"]), int(r["id"])))
    else:
        rows.sort(key=lambda r: int(r["id"]))
    if args.limit is not None:
        rows = rows[: args.limit]

    out_rows = []
    for pebble_id, row in enumerate(rows, start=1):
        out_rows.append(
            {
                "pebble_id": pebble_id,
                "proxy_atom_id": int(row["id"]),
                "x": float(row["x"]),
                "y": float(row["y"]),
                "z": float(row["z"]),
                "radius": float(row["radius"]),
                "source_timestep": step,
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
