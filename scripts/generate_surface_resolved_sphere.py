#!/usr/bin/env python3
"""Generate a surface-resolved random bonded-sphere mother pebble.

A Fibonacci shell controls the support radius in every direction, while the
remaining subparticles are inserted randomly into the core. The random shell
rotation and random core preserve sample-to-sample variability without leaving
large directional gaps at the nominal mother-pebble surface.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation


def particle_radius(mother_radius: float, count: int, packing_fraction: float) -> float:
    return mother_radius * (packing_fraction / count) ** (1.0 / 3.0)


def fibonacci_shell(count: int, radius: float, rng: np.random.Generator) -> np.ndarray:
    indices = np.arange(count, dtype=float)
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    z = 1.0 - 2.0 * (indices + 0.5) / count
    radial = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    points = np.column_stack((radial * np.cos(golden_angle * indices), radial * np.sin(golden_angle * indices), z))
    rotation = Rotation.random(random_state=rng).as_matrix()
    return points @ rotation.T * radius


def insert_core(
    count: int,
    core_radius: float,
    particle_radius_: float,
    existing: np.ndarray,
    minimum_distance: float,
    rng: np.random.Generator,
) -> np.ndarray:
    accepted: list[np.ndarray] = []
    attempts = 0
    max_attempts = max(1_000_000, count * 100_000)
    minimum2 = minimum_distance**2
    while len(accepted) < count and attempts < max_attempts:
        attempts += 1
        direction = rng.normal(size=3)
        direction /= np.linalg.norm(direction)
        candidate = direction * core_radius * rng.random() ** (1.0 / 3.0)
        if np.any(np.sum((existing - candidate) ** 2, axis=1) < minimum2):
            continue
        if accepted:
            placed = np.vstack(accepted)
            if np.any(np.sum((placed - candidate) ** 2, axis=1) < minimum2):
                continue
        accepted.append(candidate)
    if len(accepted) != count:
        raise RuntimeError(f"placed only {len(accepted)}/{count} core particles after {attempts} attempts")
    return np.vstack(accepted)


def support_statistics(centers: np.ndarray, radius: float, rng: np.random.Generator) -> dict[str, float]:
    directions = rng.normal(size=(20_000, 3))
    directions /= np.linalg.norm(directions, axis=1)[:, None]
    support_plus = np.concatenate(
        [np.max(np.einsum("ij,kj->ik", centers, block) + radius, axis=0) for block in np.array_split(directions, 20)]
    )
    support_minus = np.concatenate(
        [np.max(np.einsum("ij,kj->ik", centers, -block) + radius, axis=0) for block in np.array_split(directions, 20)]
    )
    diameters = support_plus + support_minus
    return {
        "diameter_min_mm": float(diameters.min()),
        "diameter_q01_mm": float(np.quantile(diameters, 0.01)),
        "diameter_q05_mm": float(np.quantile(diameters, 0.05)),
        "diameter_median_mm": float(np.median(diameters)),
        "diameter_q95_mm": float(np.quantile(diameters, 0.95)),
        "diameter_max_mm": float(diameters.max()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=500)
    parser.add_argument("--shell-count", type=int, default=300)
    parser.add_argument("--diameter-mm", type=float, default=1.0)
    parser.add_argument("--packing-fraction", type=float, default=0.30)
    parser.add_argument("--minimum-distance-factor", type=float, default=2.05)
    parser.add_argument("--seed", type=int, default=20260612)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    if not 0 < args.shell_count < args.count:
        raise ValueError("shell-count must be between zero and count")

    rng = np.random.default_rng(args.seed)
    mother_radius = args.diameter_mm / 2.0
    radius = particle_radius(mother_radius, args.count, args.packing_fraction)
    shell_radius = mother_radius - radius
    minimum_distance = args.minimum_distance_factor * radius
    shell = fibonacci_shell(args.shell_count, shell_radius, rng)
    shell_distances = np.linalg.norm(shell[:, None, :] - shell[None, :, :], axis=2)
    np.fill_diagonal(shell_distances, np.inf)
    if shell_distances.min() < minimum_distance:
        raise RuntimeError(
            f"shell minimum distance {shell_distances.min():.6g} mm is below required {minimum_distance:.6g} mm"
        )
    core_radius = shell_radius - minimum_distance
    core = insert_core(
        args.count - args.shell_count,
        core_radius,
        radius,
        shell,
        minimum_distance,
        rng,
    )
    centers = np.vstack((shell, core))
    types = np.where(centers[:, 0] >= 0.0, 1, 2)
    stats = support_statistics(centers, radius, rng)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "particles.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "x_mm", "y_mm", "z_mm", "radius_mm"])
        for index, point in enumerate(centers, 1):
            writer.writerow([index, point[0], point[1], point[2], radius])
    with (args.out_dir / "template.multisphere").open("w") as handle:
        for point, particle_type in zip(centers, types):
            handle.write(
                f"{point[0] * 1.0e-3:.12e} {point[1] * 1.0e-3:.12e} "
                f"{point[2] * 1.0e-3:.12e} {radius * 1.0e-3:.12e} {particle_type}\n"
            )
    with (args.out_dir / "template_rigid.multisphere").open("w") as handle:
        for point in centers:
            handle.write(
                f"{point[0] * 1.0e-3:.12e} {point[1] * 1.0e-3:.12e} "
                f"{point[2] * 1.0e-3:.12e} {radius * 1.0e-3:.12e}\n"
            )
    with (args.out_dir / "summary.csv").open("w", newline="") as handle:
        row = {
            "count": args.count,
            "shell_count": args.shell_count,
            "core_count": args.count - args.shell_count,
            "subparticle_radius_mm": radius,
            "shell_radius_mm": shell_radius,
            "minimum_shell_spacing_mm": float(shell_distances.min()),
            **stats,
        }
        writer = csv.DictWriter(handle, fieldnames=list(row))
        writer.writeheader()
        writer.writerow(row)
    print(args.out_dir / "template.multisphere")
    print(args.out_dir / "template_rigid.multisphere")
    print(args.out_dir / "summary.csv")


if __name__ == "__main__":
    main()
