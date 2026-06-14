#!/usr/bin/env python3
"""Aggregate native subparticle contact output into a mother-pebble network."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict, deque
from pathlib import Path

import numpy as np


def read_local(path: Path) -> np.ndarray:
    lines = path.read_text().splitlines()
    count_index = next((i for i, line in enumerate(lines) if line.startswith("ITEM: NUMBER OF ENTRIES")), None)
    if count_index is not None and count_index + 1 < len(lines) and int(lines[count_index + 1]) == 0:
        return np.empty((0, 10))
    header_index = next(i for i, line in enumerate(lines) if line.startswith("ITEM: ENTRIES"))
    if header_index + 1 >= len(lines):
        return np.empty((0, 10))
    data = np.loadtxt(lines[header_index + 1 :])
    if data.size == 0:
        return np.empty((0, 10))
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", type=Path, required=True)
    parser.add_argument("--walls", type=Path, required=True)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    args = parser.parse_args()

    pairs = read_local(args.pairs)
    walls = read_local(args.walls)
    edge_data: dict[tuple[int, int], dict[str, float]] = {}
    adjacency: dict[int, set[int]] = defaultdict(set)
    for row in pairs:
        atom_i = int(row[0])
        atom_j = int(row[1])
        delta = float(row[9])
        mother_i = (atom_i - 1) // args.nspheres + 1
        mother_j = (atom_j - 1) // args.nspheres + 1
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
        mesh_id = int(row[0])
        atom_id = int(row[2])
        mother_id = (atom_id - 1) // args.nspheres + 1
        wall_sets[mesh_id].add(mother_id)
        wall_force_z[mesh_id] += float(row[5])

    top_mothers = wall_sets.get(0, set())
    bottom_mothers = wall_sets.get(1, set())
    side_force_z = sum(wall_force_z.get(mesh_id, 0.0) for mesh_id in (2, 3, 4, 5))
    top_reachable = reachable(top_mothers, adjacency)
    spanning_mothers = top_reachable & bottom_mothers

    args.edges.parent.mkdir(parents=True, exist_ok=True)
    with args.edges.open("w", newline="") as handle:
        fieldnames = [
            "mother_i",
            "mother_j",
            "subcontacts",
            "force_sum_N",
            "force_max_N",
            "overlap_max_m",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for (mother_i, mother_j), record in sorted(edge_data.items()):
            writer.writerow(
                {
                    "mother_i": mother_i,
                    "mother_j": mother_j,
                    "subcontacts": int(record["subcontacts"]),
                    "force_sum_N": record["force_sum_N"],
                    "force_max_N": record["force_max_N"],
                    "overlap_max_m": record["overlap_max_m"],
                }
            )

    summary = {
        "pair_file": str(args.pairs),
        "inter_pebble_edges": len(edge_data),
        "inter_pebble_subcontacts": int(sum(record["subcontacts"] for record in edge_data.values())),
        "inter_pebble_force_sum_N": sum(record["force_sum_N"] for record in edge_data.values()),
        "top_loaded_mother_pebbles": len(top_mothers),
        "bottom_loaded_mother_pebbles": len(bottom_mothers),
        "top_wall_force_z_N": wall_force_z.get(0, 0.0),
        "bottom_wall_force_z_N": wall_force_z.get(1, 0.0),
        "side_wall_force_z_N": side_force_z,
        "all_wall_force_z_N": sum(wall_force_z.values()),
        "top_reachable_mother_pebbles": len(top_reachable),
        "bottom_mothers_reachable_from_top": len(spanning_mothers),
        "spanning_force_graph": int(bool(spanning_mothers)),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.summary.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)
    print(args.summary)


if __name__ == "__main__":
    main()
