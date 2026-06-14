#!/usr/bin/env python3
"""Audit whether a PB-007 rigid surface pack is ready for bonded compression."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def read_final_spheres(path: Path) -> tuple[int, int, float, float, float, float]:
    lines = path.read_text().splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith("ITEM: ATOMS"))
    columns = lines[header].split()[2:]
    idx = {name: columns.index(name) for name in columns}
    rows = [line.split() for line in lines[header + 1 :] if line.strip()]
    if not rows:
        raise RuntimeError(f"No atom rows in {path}")
    mols = {int(row[idx["mol"]]) for row in rows}
    z_low = min(float(row[idx["z"]]) - float(row[idx["radius"]]) for row in rows)
    z_high = max(float(row[idx["z"]]) + float(row[idx["radius"]]) for row in rows)
    x_low = min(float(row[idx["x"]]) - float(row[idx["radius"]]) for row in rows)
    x_high = max(float(row[idx["x"]]) + float(row[idx["radius"]]) for row in rows)
    return len(rows), len(mols), x_high - x_low, z_low, z_high, z_high - z_low


def read_log_tail_metrics(path: Path) -> tuple[float | None, int | None]:
    final_ke = None
    total_neighbors = None
    thermo_re = re.compile(r"^\s*\d+\s+\d+\s+([-+0-9.eE]+)\s+[-+0-9.eE]+\s+[-+0-9.eE]+\s+[-+0-9.eE]+")
    neigh_re = re.compile(r"Total # of neighbors =\s+(\d+)")
    for line in path.read_text(errors="replace").splitlines():
        thermo_match = thermo_re.match(line)
        if thermo_match:
            final_ke = float(thermo_match.group(1))
        neigh_match = neigh_re.search(line)
        if neigh_match:
            total_neighbors = int(neigh_match.group(1))
    return final_ke, total_neighbors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--final-step", type=int, default=300000)
    parser.add_argument("--target-pebbles", type=int, default=100)
    parser.add_argument("--max-height-mm", type=float, default=6.0)
    parser.add_argument("--min-neighbors", type=int, default=5000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    final_dump = args.case_dir / "post" / f"spheres_{args.final_step:08d}.dump"
    log_file = args.case_dir / "log.liggghts"
    atoms, pebbles, x_span, zlo, zhi, height = read_final_spheres(final_dump)
    final_ke, total_neighbors = read_log_tail_metrics(log_file)
    height_mm = height * 1.0e3
    status = "pass"
    if pebbles != args.target_pebbles:
        status = "fail_incomplete_insertion"
    elif height_mm > args.max_height_mm:
        status = "fail_unsettled_tall_bed"
    elif total_neighbors is None or total_neighbors < args.min_neighbors:
        status = "fail_sparse_contact_network"

    row = {
        "case_id": args.case_dir.name,
        "final_step": args.final_step,
        "atoms": atoms,
        "mother_pebbles": pebbles,
        "x_span_mm": x_span * 1.0e3,
        "zlo_mm": zlo * 1.0e3,
        "zhi_mm": zhi * 1.0e3,
        "bed_height_mm": height_mm,
        "final_ke_multisphere_J": final_ke,
        "total_neighbors": total_neighbors,
        "max_height_gate_mm": args.max_height_mm,
        "min_neighbors_gate": args.min_neighbors,
        "rigid_pack_gate_status": status,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_header = not args.output.exists()
    with args.output.open("a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    print(args.output)
    print(status)


if __name__ == "__main__":
    main()
