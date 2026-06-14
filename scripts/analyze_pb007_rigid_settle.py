#!/usr/bin/env python3
"""Summarize the mother-pebble contact graph in a rigid-clump settling dump."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict, deque
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree


def read_dump(path: Path) -> dict[str, np.ndarray]:
    lines = path.read_text().splitlines()
    atoms_header = next(i for i, line in enumerate(lines) if line.startswith("ITEM: ATOMS"))
    columns = lines[atoms_header].split()[2:]
    data = np.loadtxt(lines[atoms_header + 1 :])
    if data.ndim == 1:
        data = data[None, :]
    return {name: data[:, index] for index, name in enumerate(columns)}


def largest_component(nodes: set[int], adjacency: dict[int, set[int]]) -> set[int]:
    largest: set[int] = set()
    unseen = set(nodes)
    while unseen:
        start = unseen.pop()
        component = {start}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in adjacency.get(node, set()):
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        if len(component) > len(largest):
            largest = component
    return largest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dump", type=Path)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--bottom-z", type=float, default=0.0)
    parser.add_argument("--contact-tolerance", type=float, default=1.0e-10)
    args = parser.parse_args()

    atoms = read_dump(args.dump)
    positions = np.column_stack((atoms["x"], atoms["y"], atoms["z"]))
    radii = atoms["radius"]
    mother_ids = atoms["mol"].astype(int)
    unique_mothers = set(np.unique(mother_ids).tolist())

    search_radius = float(2.0 * radii.max() + args.contact_tolerance)
    pairs = cKDTree(positions).query_pairs(search_radius, output_type="ndarray")
    edge_accumulator: dict[tuple[int, int], dict[str, float]] = {}
    adjacency: dict[int, set[int]] = defaultdict(set)
    for first, second in pairs:
        mother_first = int(mother_ids[first])
        mother_second = int(mother_ids[second])
        if mother_first == mother_second:
            continue
        distance = float(np.linalg.norm(positions[first] - positions[second]))
        overlap = float(radii[first] + radii[second] - distance)
        if overlap < -args.contact_tolerance:
            continue
        edge = tuple(sorted((mother_first, mother_second)))
        record = edge_accumulator.setdefault(edge, {"contacts": 0.0, "max_overlap_m": 0.0, "sum_overlap_m": 0.0})
        record["contacts"] += 1.0
        record["max_overlap_m"] = max(record["max_overlap_m"], max(0.0, overlap))
        record["sum_overlap_m"] += max(0.0, overlap)
        adjacency[mother_first].add(mother_second)
        adjacency[mother_second].add(mother_first)

    bottom_mask = positions[:, 2] - radii <= args.bottom_z + args.contact_tolerance
    bottom_mothers = set(mother_ids[bottom_mask].tolist())
    component = largest_component(unique_mothers, adjacency)
    component_bottom = component & bottom_mothers

    args.edges.parent.mkdir(parents=True, exist_ok=True)
    with args.edges.open("w", newline="") as handle:
        fieldnames = ["mother_i", "mother_j", "subcontacts", "max_overlap_m", "sum_overlap_m"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for (mother_i, mother_j), values in sorted(edge_accumulator.items()):
            writer.writerow(
                {
                    "mother_i": mother_i,
                    "mother_j": mother_j,
                    "subcontacts": int(values["contacts"]),
                    "max_overlap_m": values["max_overlap_m"],
                    "sum_overlap_m": values["sum_overlap_m"],
                }
            )

    summary = {
        "dump": str(args.dump),
        "subparticles": len(positions),
        "mother_pebbles": len(unique_mothers),
        "inter_pebble_edges": len(edge_accumulator),
        "inter_pebble_subcontacts": int(sum(record["contacts"] for record in edge_accumulator.values())),
        "active_mother_pebbles": len(adjacency),
        "largest_component_pebbles": len(component),
        "largest_component_fraction": len(component) / len(unique_mothers) if unique_mothers else 0.0,
        "bottom_contacting_pebbles": len(bottom_mothers),
        "largest_component_bottom_pebbles": len(component_bottom),
        "minimum_surface_z_m": float(np.min(positions[:, 2] - radii)),
        "maximum_surface_z_m": float(np.max(positions[:, 2] + radii)),
        "maximum_inter_pebble_overlap_m": max(
            (record["max_overlap_m"] for record in edge_accumulator.values()), default=0.0
        ),
    }
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.summary.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)
    print(args.summary)


if __name__ == "__main__":
    main()
