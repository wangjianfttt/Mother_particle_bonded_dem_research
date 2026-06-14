#!/usr/bin/env python3
"""Build mother-pebble contact networks from particle overlaps in PB-006 dumps.

This is a geometry-derived force proxy, not a replacement for native
LIGGGHTS contact-local forces. For each inter-mother subparticle overlap,
the edge weight is sum(delta**1.5), proportional to Hertzian normal force
for identical material parameters.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


def parse_wall_bounds(path: Path) -> dict[str, float]:
    bounds = {}
    with path.open() as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 4 and parts[0] == "variable":
                bounds[parts[1].replace("wall_", "")] = float(parts[3])
    return bounds


def read_dump(path: Path, nspheres: int) -> tuple[int, list[tuple[int, float, float, float, float]]]:
    with path.open() as f:
        if not f.readline().startswith("ITEM: TIMESTEP"):
            raise ValueError(f"{path} is not a particle dump")
        step = int(f.readline().strip())
        f.readline()
        natoms = int(f.readline().strip())
        f.readline()
        for _ in range(3):
            f.readline()
        header = f.readline().strip().split()[2:]
        idx = {name: i for i, name in enumerate(header)}
        required = ["id", "x", "y", "z", "radius"]
        missing = [name for name in required if name not in idx]
        if missing:
            raise ValueError(f"{path} missing columns: {missing}")
        atoms = []
        for _ in range(natoms):
            parts = f.readline().split()
            atom_id = int(parts[idx["id"]])
            pid = (atom_id - 1) // nspheres + 1
            atoms.append(
                (
                    pid,
                    float(parts[idx["x"]]),
                    float(parts[idx["y"]]),
                    float(parts[idx["z"]]),
                    float(parts[idx["radius"]]),
                )
            )
    return step, atoms


def displacement_m(step: int, pre_steps: int, top_speed: float, dt: float) -> float:
    return max(0.0, top_speed * (step - pre_steps) * dt)


def summarize_dump(
    path: Path,
    nspheres: int,
    skin: float,
    wall_zhi: float,
    pre_steps: int,
    top_speed: float,
    dt: float,
    top_n: int,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    step, atoms = read_dump(path, nspheres)
    max_r = max(a[4] for a in atoms)
    cell = 2.0 * max_r + skin
    grid: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    for i, (_, x, y, z, _) in enumerate(atoms):
        grid[(math.floor(x / cell), math.floor(y / cell), math.floor(z / cell))].append(i)

    edge = defaultdict(lambda: {"contacts": 0, "overlap_sum_m": 0.0, "hertz_proxy_sum": 0.0, "max_overlap_m": 0.0})
    for i, (pa, xa, ya, za, ra) in enumerate(atoms):
        cx, cy, cz = math.floor(xa / cell), math.floor(ya / cell), math.floor(za / cell)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in grid.get((cx + dx, cy + dy, cz + dz), []):
                        if j <= i:
                            continue
                        pb, xb, yb, zb, rb = atoms[j]
                        if pa == pb:
                            continue
                        sx = xa - xb
                        sy = ya - yb
                        sz = za - zb
                        rsum = ra + rb
                        d2 = sx * sx + sy * sy + sz * sz
                        if d2 >= rsum * rsum:
                            continue
                        dist = math.sqrt(d2) if d2 > 0 else 1.0e-30
                        overlap = rsum - dist
                        key = tuple(sorted((pa, pb)))
                        stat = edge[key]
                        stat["contacts"] += 1
                        stat["overlap_sum_m"] += overlap
                        stat["hertz_proxy_sum"] += overlap**1.5
                        stat["max_overlap_m"] = max(stat["max_overlap_m"], overlap)

    top_z = wall_zhi - displacement_m(step, pre_steps, top_speed, dt)
    top = defaultdict(lambda: {"contacts": 0, "overlap_sum_m": 0.0, "hertz_proxy_sum": 0.0, "max_overlap_m": 0.0})
    for pid, _, _, z, r in atoms:
        overlap = z + r - top_z
        if overlap <= 0:
            continue
        stat = top[pid]
        stat["contacts"] += 1
        stat["overlap_sum_m"] += overlap
        stat["hertz_proxy_sum"] += overlap**1.5
        stat["max_overlap_m"] = max(stat["max_overlap_m"], overlap)

    disp_mm = displacement_m(step, pre_steps, top_speed, dt) * 1000.0
    edge_rows = []
    for (a, b), stat in sorted(edge.items(), key=lambda item: item[1]["hertz_proxy_sum"], reverse=True):
        edge_rows.append(
            {
                "timestep": step,
                "top_displacement_mm": disp_mm,
                "pebble_i": a,
                "pebble_j": b,
                "contact_count": int(stat["contacts"]),
                "overlap_sum_um": stat["overlap_sum_m"] * 1.0e6,
                "max_overlap_um": stat["max_overlap_m"] * 1.0e6,
                "hertz_proxy_sum_m32": stat["hertz_proxy_sum"],
            }
        )
    top_rows = []
    for pid, stat in sorted(top.items(), key=lambda item: item[1]["hertz_proxy_sum"], reverse=True):
        top_rows.append(
            {
                "timestep": step,
                "top_displacement_mm": disp_mm,
                "pebble_id": pid,
                "contact_count": int(stat["contacts"]),
                "overlap_sum_um": stat["overlap_sum_m"] * 1.0e6,
                "max_overlap_um": stat["max_overlap_m"] * 1.0e6,
                "hertz_proxy_sum_m32": stat["hertz_proxy_sum"],
            }
        )

    summary = {
        "timestep": step,
        "top_displacement_mm": disp_mm,
        "inter_pebble_edges": len(edge_rows),
        "inter_subparticle_contacts": sum(r["contact_count"] for r in edge_rows),
        "inter_hertz_proxy_sum_m32": sum(r["hertz_proxy_sum_m32"] for r in edge_rows),
        "topwall_pebbles": len(top_rows),
        "topwall_subparticle_contacts": sum(r["contact_count"] for r in top_rows),
        "topwall_hertz_proxy_sum_m32": sum(r["hertz_proxy_sum_m32"] for r in top_rows),
        "top_edge_pebbles": ";".join(
            f"{r['pebble_i']}-{r['pebble_j']}" for r in edge_rows[:top_n]
        ),
        "topwall_pebble_ids": ";".join(str(r["pebble_id"]) for r in top_rows[:top_n]),
    }
    return summary, edge_rows[: max(top_n, 100)], top_rows[: max(top_n, 100)]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dumps", nargs="+", type=Path)
    parser.add_argument("--wall-bounds", type=Path, required=True)
    parser.add_argument("--wall-zhi", type=float, default=None, help="Override top-wall initial z position in metres.")
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--skin", type=float, default=0.0)
    parser.add_argument("--pre-steps", type=int, default=1001)
    parser.add_argument("--top-speed", type=float, default=0.5)
    parser.add_argument("--dt", type=float, default=5.0e-9)
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument("--edge-output", type=Path, required=True)
    parser.add_argument("--topwall-output", type=Path, required=True)
    args = parser.parse_args()

    bounds = parse_wall_bounds(args.wall_bounds)
    wall_zhi = args.wall_zhi if args.wall_zhi is not None else bounds["zhi"]
    summaries = []
    edges = []
    topwalls = []
    for dump in sorted(args.dumps, key=lambda p: int(p.stem.split("_")[-1])):
        summary, edge_rows, top_rows = summarize_dump(
            dump,
            args.nspheres,
            args.skin,
            wall_zhi,
            args.pre_steps,
            args.top_speed,
            args.dt,
            args.top_n,
        )
        summaries.append(summary)
        edges.extend(edge_rows)
        topwalls.extend(top_rows)
    write_csv(args.summary_output, summaries)
    write_csv(args.edge_output, edges)
    write_csv(args.topwall_output, topwalls)
    print(args.summary_output)
    print(args.edge_output)
    print(args.topwall_output)


if __name__ == "__main__":
    main()
