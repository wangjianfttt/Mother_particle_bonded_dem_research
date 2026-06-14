#!/usr/bin/env python3
"""Build a PB-007 native force-network time series from local pair/wall dumps."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict, deque
from pathlib import Path

import numpy as np


def dump_timestep(path: Path) -> int:
    with path.open(errors="ignore") as handle:
        for line in handle:
            if line.strip() == "ITEM: TIMESTEP":
                return int(next(handle).strip())
    raise ValueError(f"No timestep found in {path}")


def read_local(path: Path) -> np.ndarray:
    lines = path.read_text().splitlines()
    header_index = next(i for i, line in enumerate(lines) if line.startswith("ITEM: ENTRIES"))
    data_lines = lines[header_index + 1 :]
    if not data_lines:
        return np.empty((0, 10))
    data = np.loadtxt(data_lines)
    return np.atleast_2d(data)


def reachable(start: set[int], adjacency: dict[int, set[int]]) -> set[int]:
    visited = set(start)
    queue = deque(start)
    while queue:
        node = queue.popleft()
        for neighbor in adjacency.get(node, set()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


def summarize(pairs_path: Path, walls_path: Path, nspheres: int) -> dict[str, int | float | str]:
    pairs = read_local(pairs_path)
    walls = read_local(walls_path)
    edge_data: dict[tuple[int, int], dict[str, float]] = {}
    adjacency: dict[int, set[int]] = defaultdict(set)
    for row in pairs:
        if row.size < 10:
            continue
        atom_i = int(row[0])
        atom_j = int(row[1])
        delta = float(row[9])
        mother_i = (atom_i - 1) // nspheres + 1
        mother_j = (atom_j - 1) // nspheres + 1
        if mother_i == mother_j or delta <= 0.0:
            continue
        edge = tuple(sorted((mother_i, mother_j)))
        force = float(np.linalg.norm(row[3:6]))
        record = edge_data.setdefault(
            edge,
            {"subcontacts": 0.0, "force_sum_N": 0.0, "force_max_N": 0.0, "overlap_max_m": 0.0},
        )
        record["subcontacts"] += 1.0
        record["force_sum_N"] += force
        record["force_max_N"] = max(record["force_max_N"], force)
        record["overlap_max_m"] = max(record["overlap_max_m"], delta)
        adjacency[mother_i].add(mother_j)
        adjacency[mother_j].add(mother_i)

    wall_sets: dict[int, set[int]] = defaultdict(set)
    wall_force_z: dict[int, float] = defaultdict(float)
    for row in walls:
        if row.size < 6:
            continue
        mesh_id = int(row[0])
        atom_id = int(row[2])
        mother_id = (atom_id - 1) // nspheres + 1
        wall_sets[mesh_id].add(mother_id)
        wall_force_z[mesh_id] += float(row[5])

    top_mothers = wall_sets.get(0, set())
    bottom_mothers = wall_sets.get(1, set())
    top_reachable = reachable(top_mothers, adjacency)
    spanning_mothers = top_reachable & bottom_mothers
    force_values = [record["force_sum_N"] for record in edge_data.values()]
    max_force = max(force_values) if force_values else 0.0
    mean_force = sum(force_values) / len(force_values) if force_values else 0.0

    return {
        "timestep": dump_timestep(pairs_path),
        "pair_file": str(pairs_path),
        "wall_file": str(walls_path),
        "inter_pebble_edges": len(edge_data),
        "inter_pebble_subcontacts": int(sum(record["subcontacts"] for record in edge_data.values())),
        "inter_pebble_force_sum_N": sum(force_values),
        "inter_pebble_force_mean_N": mean_force,
        "inter_pebble_force_max_N": max_force,
        "top_loaded_mother_pebbles": len(top_mothers),
        "bottom_loaded_mother_pebbles": len(bottom_mothers),
        "top_wall_force_z_N": wall_force_z.get(0, 0.0),
        "bottom_wall_force_z_N": wall_force_z.get(1, 0.0),
        "side_wall_force_z_N": sum(wall_force_z.get(mesh_id, 0.0) for mesh_id in (2, 3, 4, 5)),
        "all_wall_force_z_N": sum(wall_force_z.values()),
        "top_reachable_mother_pebbles": len(top_reachable),
        "bottom_mothers_reachable_from_top": len(spanning_mothers),
        "spanning_force_graph": int(bool(spanning_mothers)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--nspheres", type=int, default=500)
    args = parser.parse_args()

    post_dir = args.case_dir / "post"
    pair_by_step = {dump_timestep(path): path for path in post_dir.glob("pairs_event_*.local")}
    wall_by_step = {dump_timestep(path): path for path in post_dir.glob("walls_event_*.local")}
    common_steps = sorted(set(pair_by_step) & set(wall_by_step))
    if not common_steps:
        raise SystemExit("No matched pair/wall event dumps found.")

    rows = [summarize(pair_by_step[step], wall_by_step[step], args.nspheres) for step in common_steps]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(args.output)


if __name__ == "__main__":
    main()
