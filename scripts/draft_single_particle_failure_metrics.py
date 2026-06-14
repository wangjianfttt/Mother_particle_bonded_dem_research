#!/usr/bin/env python3
"""Draft metrics for single-particle failure-mode screening.

This script is intentionally standalone. It reads LIGGGHTS particle dumps and
local bond dumps from one post directory and writes a CSV of graph/spatial
metrics useful for separating core-spanning split/progressive fragmentation
from surface spall.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


class UnionFind:
    def __init__(self, nodes: list[int]):
        self.parent = {node: node for node in nodes}
        self.size = {node: 1 for node in nodes}

    def find(self, node: int) -> int:
        while self.parent[node] != node:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def union(self, a: int, b: int) -> None:
        if a not in self.parent or b not in self.parent:
            return
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

    def components(self) -> dict[int, list[int]]:
        comps: dict[int, list[int]] = {}
        for node in self.parent:
            comps.setdefault(self.find(node), []).append(node)
        return comps


def timestep(path: Path) -> int:
    return int(path.stem.split("_")[-1])


def read_particles(path: Path) -> dict[int, dict[str, float]]:
    lines = path.read_text().splitlines()
    header_idx = next(i for i, line in enumerate(lines) if line.startswith("ITEM: ATOMS"))
    fields = lines[header_idx].split()[2:]
    out: dict[int, dict[str, float]] = {}
    for line in lines[header_idx + 1:]:
        if not line.strip():
            continue
        values = line.split()
        row = dict(zip(fields, values))
        pid = int(float(row["id"]))
        out[pid] = {k: float(v) for k, v in row.items() if k != "id"}
    return out


def read_edges(path: Path) -> set[tuple[int, int]]:
    lines = path.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("ITEM: ENTRIES"):
            start = i + 1
            break
    if start is None:
        return set()
    edges: set[tuple[int, int]] = set()
    for line in lines[start:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        a, b = int(float(parts[0])), int(float(parts[1]))
        if a != b:
            edges.add((a, b) if a < b else (b, a))
    return edges


def norm(v: tuple[float, float, float]) -> float:
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


def component_stats(component: list[int], particles: dict[int, dict[str, float]]) -> dict[str, float]:
    pts = [particles[i] for i in component if i in particles]
    if not pts:
        return {"size": 0, "span_x": 0.0, "span_y": 0.0, "span_z": 0.0, "centroid_r": 0.0}
    xs = [p["x"] for p in pts]
    ys = [p["y"] for p in pts]
    zs = [p["z"] for p in pts]
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    cz = sum(zs) / len(zs)
    return {
        "size": float(len(pts)),
        "span_x": max(xs) - min(xs),
        "span_y": max(ys) - min(ys),
        "span_z": max(zs) - min(zs),
        "centroid_r": norm((cx, cy, cz)),
    }


def cloud_radius(particles: dict[int, dict[str, float]]) -> float:
    return max(
        norm((p["x"], p["y"], p["z"])) + p.get("radius", 0.0)
        for p in particles.values()
    )


def broken_bond_spatial_metrics(
    initial_edges: set[tuple[int, int]],
    edges: set[tuple[int, int]],
    reference_particles: dict[int, dict[str, float]],
    radius: float,
) -> dict[str, float]:
    broken = initial_edges - edges
    if not broken:
        return {
            "broken_edges": 0,
            "broken_core_fraction": 0.0,
            "broken_surface_fraction": 0.0,
            "broken_span_x_over_d": 0.0,
            "broken_span_y_over_d": 0.0,
            "broken_span_z_over_d": 0.0,
        }
    mids: list[tuple[float, float, float]] = []
    for a, b in broken:
        if a not in reference_particles or b not in reference_particles:
            continue
        pa, pb = reference_particles[a], reference_particles[b]
        mids.append(((pa["x"] + pb["x"]) / 2.0, (pa["y"] + pb["y"]) / 2.0, (pa["z"] + pb["z"]) / 2.0))
    if not mids:
        return {
            "broken_edges": float(len(broken)),
            "broken_core_fraction": 0.0,
            "broken_surface_fraction": 0.0,
            "broken_span_x_over_d": 0.0,
            "broken_span_y_over_d": 0.0,
            "broken_span_z_over_d": 0.0,
        }
    rs = [norm(p) / radius for p in mids]
    xs = [p[0] for p in mids]
    ys = [p[1] for p in mids]
    zs = [p[2] for p in mids]
    diameter = 2.0 * radius
    return {
        "broken_edges": float(len(broken)),
        "broken_core_fraction": sum(1 for r in rs if r <= 0.60) / len(rs),
        "broken_surface_fraction": sum(1 for r in rs if r >= 0.80) / len(rs),
        "broken_span_x_over_d": (max(xs) - min(xs)) / diameter,
        "broken_span_y_over_d": (max(ys) - min(ys)) / diameter,
        "broken_span_z_over_d": (max(zs) - min(zs)) / diameter,
    }


def classify(row: dict[str, float]) -> str:
    if row["intact_bonds"] <= 0:
        return "prebond_or_invalid"
    if row["second_fragment_fraction"] >= 0.10 and row["largest_fragment_fraction"] <= 0.90:
        if row["broken_core_fraction"] >= 0.25:
            return "through_split_or_bulk_fragmentation"
    if row["largest_fragment_fraction"] >= 0.95 and row["second_fragment_fraction"] <= 0.05:
        if row["broken_surface_fraction"] >= 0.60 or row["single_particle_fragment_fraction"] >= 0.50:
            return "surface_spall"
    if row["fragment_count"] > 1 and row["broken_core_fraction"] >= 0.15:
        return "progressive_bulk_damage"
    if row["fragment_count"] > 1:
        return "minor_spall_or_early_damage"
    return "intact_or_prebond"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_dir", type=Path, help="Directory containing particles_*.dump and bonds_*.local")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    particle_paths = {timestep(p): p for p in args.post_dir.glob("particles_*.dump")}
    bond_paths = {timestep(p): p for p in args.post_dir.glob("bonds_*.local")}
    steps = sorted(set(particle_paths) & set(bond_paths))
    if not steps:
        raise SystemExit("No matching particle/bond dump timesteps found")

    particles_by_step = {step: read_particles(particle_paths[step]) for step in steps}
    edges_by_step = {step: read_edges(bond_paths[step]) for step in steps}
    reference_step = max(steps, key=lambda step: len(edges_by_step[step]))
    initial_edges = edges_by_step[reference_step]
    reference_particles = particles_by_step[reference_step]
    radius = cloud_radius(reference_particles)
    atoms = sorted(reference_particles)

    rows: list[dict[str, float | str | int]] = []
    for step in steps:
        particles = particles_by_step[step]
        edges = edges_by_step[step]
        uf = UnionFind(atoms)
        for a, b in edges:
            uf.union(a, b)
        comps = sorted(uf.components().values(), key=len, reverse=True)
        stats = [component_stats(comp, particles) for comp in comps]
        largest = stats[0] if stats else {"size": 0.0, "span_x": 0.0, "span_y": 0.0, "span_z": 0.0, "centroid_r": 0.0}
        second = stats[1] if len(stats) > 1 else {"size": 0.0, "span_x": 0.0, "span_y": 0.0, "span_z": 0.0, "centroid_r": 0.0}
        row: dict[str, float | str | int] = {
            "timestep": step,
            "reference_step": reference_step,
            "intact_bonds": len(edges),
            "broken_bonds_from_reference": max(0, len(initial_edges) - len(edges)),
            "fragment_count": len(comps),
            "largest_fragment_fraction": largest["size"] / len(atoms),
            "second_fragment_fraction": second["size"] / len(atoms),
            "single_particle_fragment_fraction": sum(1 for comp in comps if len(comp) == 1) / max(1, len(comps)),
            "largest_span_x_over_d": largest["span_x"] / (2.0 * radius),
            "largest_span_y_over_d": largest["span_y"] / (2.0 * radius),
            "largest_span_z_over_d": largest["span_z"] / (2.0 * radius),
            "second_centroid_r_over_R": second["centroid_r"] / radius if radius else 0.0,
        }
        row.update(broken_bond_spatial_metrics(initial_edges, edges, reference_particles, radius))
        row["failure_mode_draft"] = classify(row)  # type: ignore[arg-type]
        rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
