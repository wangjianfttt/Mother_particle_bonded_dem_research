#!/usr/bin/env python3
"""Aggregate PB-006 subparticle dump forces to mother-pebble force metrics."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def parse_dump(path: Path, nspheres: int) -> tuple[int, dict[int, dict[str, float]]]:
    with path.open() as f:
        line = f.readline()
        if not line.startswith("ITEM: TIMESTEP"):
            raise ValueError(f"{path} is not a LIGGGHTS dump")
        timestep = int(f.readline().strip())
        f.readline()
        natoms = int(f.readline().strip())
        f.readline()
        for _ in range(3):
            f.readline()
        header = f.readline().strip().split()[2:]
        indices = {name: idx for idx, name in enumerate(header)}
        required = ["id", "x", "y", "z", "fx", "fy", "fz"]
        missing = [name for name in required if name not in indices]
        if missing:
            raise ValueError(f"{path} missing columns: {missing}")

        groups: dict[int, dict[str, float]] = {}
        for _ in range(natoms):
            parts = f.readline().split()
            atom_id = int(parts[indices["id"]])
            pebble_id = (atom_id - 1) // nspheres + 1
            g = groups.setdefault(
                pebble_id,
                {
                    "subparticles": 0,
                    "sum_x": 0.0,
                    "sum_y": 0.0,
                    "sum_z": 0.0,
                    "sum_fx": 0.0,
                    "sum_fy": 0.0,
                    "sum_fz": 0.0,
                    "sum_abs_fz": 0.0,
                    "max_sub_abs_fz": 0.0,
                },
            )
            fx = float(parts[indices["fx"]])
            fy = float(parts[indices["fy"]])
            fz = float(parts[indices["fz"]])
            g["subparticles"] += 1
            g["sum_x"] += float(parts[indices["x"]])
            g["sum_y"] += float(parts[indices["y"]])
            g["sum_z"] += float(parts[indices["z"]])
            g["sum_fx"] += fx
            g["sum_fy"] += fy
            g["sum_fz"] += fz
            g["sum_abs_fz"] += abs(fz)
            g["max_sub_abs_fz"] = max(g["max_sub_abs_fz"], abs(fz))
    return timestep, groups


def load_pebble_summary(path: Path) -> dict[int, dict[str, str]]:
    with path.open(newline="") as f:
        return {int(row["pebble_id"]): row for row in csv.DictReader(f)}


def load_event_steps(path: Path) -> dict[int, int]:
    counts: dict[int, int] = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            counts[int(row["timestep"])] = counts.get(int(row["timestep"]), 0) + int(row["new_broken_bonds"])
    return counts


def displacement_mm(step: int, pre_steps: int, top_speed: float, dt: float) -> float:
    return max(0.0, top_speed * (step - pre_steps) * dt * 1000.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dumps", nargs="+", type=Path)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--pebble-summary", type=Path, required=True)
    parser.add_argument("--events", type=Path, required=True)
    parser.add_argument("--pre-steps", type=int, default=1001)
    parser.add_argument("--top-speed", type=float, default=0.5)
    parser.add_argument("--dt", type=float, default=5.0e-9)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    meta = load_pebble_summary(args.pebble_summary)
    event_counts = load_event_steps(args.events)
    rows: list[dict[str, object]] = []

    for dump in sorted(args.dumps, key=lambda p: int(p.stem.split("_")[-1]) if p.stem.split("_")[-1].isdigit() else 10**12):
        step, groups = parse_dump(dump, args.nspheres)
        active_step_broken = event_counts.get(step, 0)
        enriched = []
        for pid, g in groups.items():
            n = g["subparticles"]
            fmag = math.sqrt(g["sum_fx"] ** 2 + g["sum_fy"] ** 2 + g["sum_fz"] ** 2)
            m = meta.get(pid, {})
            enriched.append(
                {
                    "seed": args.seed,
                    "timestep": step,
                    "top_displacement_mm": displacement_mm(step, args.pre_steps, args.top_speed, args.dt),
                    "pebble_id": pid,
                    "centroid_z_mm": (g["sum_z"] / n) * 1000.0,
                    "height_bin": m.get("height_bin", ""),
                    "total_broken_bonds": m.get("total_new_broken_bonds", ""),
                    "event_count": m.get("event_count", ""),
                    "step_new_broken_bonds": active_step_broken,
                    "net_fx_N": g["sum_fx"],
                    "net_fy_N": g["sum_fy"],
                    "net_fz_N": g["sum_fz"],
                    "net_force_N": fmag,
                    "sum_abs_subparticle_fz_N": g["sum_abs_fz"],
                    "max_subparticle_abs_fz_N": g["max_sub_abs_fz"],
                }
            )

        top_force = sorted(enriched, key=lambda r: (float(r["net_force_N"]), float(r["sum_abs_subparticle_fz_N"])), reverse=True)[: args.top_n]
        top_z = sorted(enriched, key=lambda r: float(r["centroid_z_mm"]), reverse=True)[: args.top_n]
        keep: dict[tuple[int, int], dict[str, object]] = {}
        for rank, row in enumerate(top_force, start=1):
            row = dict(row)
            row["selection"] = "top_force"
            row["selection_rank"] = rank
            keep[(int(row["pebble_id"]), 10_000 + rank)] = row
        for rank, row in enumerate(top_z, start=1):
            row = dict(row)
            row["selection"] = "top_z"
            row["selection_rank"] = rank
            keep[(int(row["pebble_id"]), 20_000 + rank)] = row
        rows.extend(keep.values())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(args.output)


if __name__ == "__main__":
    main()
