#!/usr/bin/env python3
"""Compute fragment statistics from LIGGGHTS local bond dumps."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


class UnionFind:
    def __init__(self, nodes: range):
        self.parent = {i: i for i in nodes}
        self.size = {i: 1 for i in nodes}

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

    def component_sizes(self) -> list[int]:
        counts: dict[int, int] = {}
        for node in self.parent:
            root = self.find(node)
            counts[root] = counts.get(root, 0) + 1
        return sorted(counts.values(), reverse=True)


def parse_timestep(path: Path) -> int:
    stem = path.stem
    return int(stem.split("_")[-1])


def read_edges(path: Path) -> list[tuple[int, int]]:
    lines = path.read_text().splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("ITEM: ENTRIES"):
            start = i + 1
            break
    if start is None:
        return []
    edges = []
    for line in lines[start:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        edges.append((int(float(parts[0])), int(float(parts[1]))))
    return edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bond_dumps", nargs="+", type=Path)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = []
    for path in sorted(args.bond_dumps, key=parse_timestep):
        uf = UnionFind(range(1, args.atoms + 1))
        edges = read_edges(path)
        for a, b in edges:
            if 1 <= a <= args.atoms and 1 <= b <= args.atoms:
                uf.union(a, b)
        sizes = uf.component_sizes()
        rows.append({
            "timestep": parse_timestep(path),
            "intact_bonds": len(edges),
            "fragment_count": len(sizes),
            "largest_fragment_particles": sizes[0] if sizes else 0,
            "second_fragment_particles": sizes[1] if len(sizes) > 1 else 0,
            "single_particle_fragments": sum(1 for s in sizes if s == 1),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
