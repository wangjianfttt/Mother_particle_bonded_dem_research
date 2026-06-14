#!/usr/bin/env python3
"""Generate a bonded-sphere template for Li4SiO4 pebble BPM studies.

The script creates subparticle centers inside a spherical mother particle,
assigns a uniform subparticle radius, and connects near neighbors with bonds.
It writes simple CSV files first so the geometry can be inspected before being
translated into a LIGGGHTS-INL data file.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=500, help="Number of subparticles.")
    parser.add_argument("--diameter-mm", type=float, default=1.0, help="Mother pebble diameter in mm.")
    parser.add_argument("--seed", type=int, default=20260523, help="Random seed.")
    parser.add_argument(
        "--packing-fraction",
        type=float,
        default=0.30,
        help=(
            "Approximate subparticle solid fraction inside the mother sphere. "
            "Sequential random insertion becomes very slow near dense packing."
        ),
    )
    parser.add_argument(
        "--bond-factor",
        type=float,
        default=2.25,
        help="Create bonds when center distance is below bond_factor * 2r.",
    )
    parser.add_argument(
        "--min-distance-factor",
        type=float,
        default=1.65,
        help="Minimum center distance as min_distance_factor * subparticle radius.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("simulations/single_pebble/templates/sp_500_d1mm"),
        help="Output directory.",
    )
    return parser.parse_args()


def subparticle_radius(mother_radius: float, count: int, packing_fraction: float) -> float:
    mother_volume = 4.0 / 3.0 * math.pi * mother_radius**3
    sub_volume = packing_fraction * mother_volume / count
    return (3.0 * sub_volume / (4.0 * math.pi)) ** (1.0 / 3.0)


def random_point_in_sphere(radius: float) -> tuple[float, float, float]:
    while True:
        x = random.uniform(-radius, radius)
        y = random.uniform(-radius, radius)
        z = random.uniform(-radius, radius)
        if x * x + y * y + z * z <= radius * radius:
            return x, y, z


def generate_centers(
    count: int, mother_radius: float, particle_radius: float, min_distance_factor: float
) -> list[tuple[float, float, float]]:
    usable_radius = mother_radius - particle_radius
    min_distance = min_distance_factor * particle_radius
    centers: list[tuple[float, float, float]] = []
    attempts = 0
    max_attempts = count * 20000

    while len(centers) < count and attempts < max_attempts:
        attempts += 1
        candidate = random_point_in_sphere(usable_radius)
        ok = True
        for center in centers:
            dx = candidate[0] - center[0]
            dy = candidate[1] - center[1]
            dz = candidate[2] - center[2]
            if dx * dx + dy * dy + dz * dz < min_distance * min_distance:
                ok = False
                break
        if ok:
            centers.append(candidate)

    if len(centers) < count:
        raise RuntimeError(
            f"Only generated {len(centers)} centers after {attempts} attempts. "
            "Try reducing packing fraction, reducing min-distance-factor, or reducing count."
        )

    return centers


def build_bonds(
    centers: list[tuple[float, float, float]], particle_radius: float, bond_factor: float
) -> list[tuple[int, int, float]]:
    cutoff = bond_factor * 2.0 * particle_radius
    cutoff2 = cutoff * cutoff
    bonds: list[tuple[int, int, float]] = []

    for i, ci in enumerate(centers):
        for j in range(i + 1, len(centers)):
            cj = centers[j]
            dx = ci[0] - cj[0]
            dy = ci[1] - cj[1]
            dz = ci[2] - cj[2]
            distance2 = dx * dx + dy * dy + dz * dz
            if distance2 <= cutoff2:
                bonds.append((i + 1, j + 1, math.sqrt(distance2)))

    return bonds


def write_particles(path: Path, centers: list[tuple[float, float, float]], radius: float) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "x_mm", "y_mm", "z_mm", "radius_mm"])
        for idx, center in enumerate(centers, start=1):
            writer.writerow([idx, *center, radius])


def write_bonds(path: Path, bonds: list[tuple[int, int, float]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "atom1", "atom2", "length_mm"])
        for idx, bond in enumerate(bonds, start=1):
            writer.writerow([idx, *bond])


def write_summary(
    path: Path,
    count: int,
    mother_diameter: float,
    particle_radius: float,
    bond_count: int,
    bond_factor: float,
) -> None:
    average_coordination = 2.0 * bond_count / count
    text = "\n".join(
        [
            "# Bonded Sphere Template Summary",
            "",
            f"- subparticle_count: {count}",
            f"- mother_diameter_mm: {mother_diameter:.8g}",
            f"- subparticle_radius_mm: {particle_radius:.8g}",
            f"- bond_factor: {bond_factor:.8g}",
            f"- bond_count: {bond_count}",
            f"- average_bond_coordination: {average_coordination:.4f}",
            "",
            "CSV files use millimetres. Convert to SI units before final LIGGGHTS-INL runs if needed.",
        ]
    )
    path.write_text(text + "\n")


def main() -> None:
    args = parse_args()
    random.seed(args.seed)

    mother_radius = args.diameter_mm / 2.0
    radius = subparticle_radius(mother_radius, args.count, args.packing_fraction)
    centers = generate_centers(args.count, mother_radius, radius, args.min_distance_factor)
    bonds = build_bonds(centers, radius, args.bond_factor)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_particles(args.out_dir / "particles.csv", centers, radius)
    write_bonds(args.out_dir / "bonds.csv", bonds)
    write_summary(args.out_dir / "summary.md", args.count, args.diameter_mm, radius, len(bonds), args.bond_factor)


if __name__ == "__main__":
    main()
