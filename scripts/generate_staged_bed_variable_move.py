#!/usr/bin/env python3
"""Generate staged bed creation plus temporary-group relocation commands.

This avoids keeping one LIGGGHTS group per pebble, which hits the group-count
limit when the bed contains more than roughly 30 mother pebbles.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path


def grid_centres(nx: int, ny: int, nz: int, spacing: float, z0: float) -> list[tuple[float, float, float]]:
    xs = [(i - (nx - 1) / 2) * spacing for i in range(nx)]
    ys = [(j - (ny - 1) / 2) * spacing for j in range(ny)]
    zs = [z0 + k * spacing for k in range(nz)]
    return [(x, y, z) for z in zs for y in ys for x in xs]


def random_quaternion(rng: random.Random) -> tuple[float, float, float, float]:
    """Return a uniformly distributed unit quaternion as scalar-first."""
    u1 = rng.random()
    u2 = rng.random()
    u3 = rng.random()
    qx = math.sqrt(1.0 - u1) * math.sin(2.0 * math.pi * u2)
    qy = math.sqrt(1.0 - u1) * math.cos(2.0 * math.pi * u2)
    qz = math.sqrt(u1) * math.sin(2.0 * math.pi * u3)
    qw = math.sqrt(u1) * math.cos(2.0 * math.pi * u3)
    return qw, qx, qy, qz


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-output", type=Path, required=True)
    parser.add_argument("--move-output", type=Path, required=True)
    parser.add_argument("--nx", type=int, default=3)
    parser.add_argument("--ny", type=int, default=3)
    parser.add_argument("--nz", type=int, default=4)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--far-spacing", type=float, default=0.00135)
    parser.add_argument("--target-spacing", type=float, default=0.00102)
    parser.add_argument("--far-z0", type=float, default=-0.00135)
    parser.add_argument("--target-z0", type=float, default=-0.00102)
    parser.add_argument("--random-orientation-seed", type=int)
    args = parser.parse_args()

    far = grid_centres(args.nx, args.ny, args.nz, args.far_spacing, args.far_z0)
    target = grid_centres(args.nx, args.ny, args.nz, args.target_spacing, args.target_z0)
    if len(far) != len(target):
        raise SystemExit("far and target centre counts differ")

    args.create_output.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.random_orientation_seed) if args.random_orientation_seed is not None else None
    with args.create_output.open("w") as f:
        f.write("# Auto-generated staged pebble bed without per-pebble groups\n")
        for x, y, z in far:
            cmd = f"create_particles clump single {x:.12e} {y:.12e} {z:.12e} velocity 0.0 0.0 0.0"
            if rng is not None:
                q1, q2, q3, q4 = random_quaternion(rng)
                cmd += f" orientation {q1:.12e} {q2:.12e} {q3:.12e} {q4:.12e}"
            f.write(cmd + "\n")
        f.write(f"# total_pebbles {len(far)}\n")

    args.move_output.parent.mkdir(parents=True, exist_ok=True)
    with args.move_output.open("w") as f:
        f.write("# Auto-generated relocation by one reusable temporary group\n")
        for i, (src, dst) in enumerate(zip(far, target), start=1):
            first = (i - 1) * args.nspheres + 1
            last = i * args.nspheres
            dx = dst[0] - src[0]
            dy = dst[1] - src[1]
            dz = dst[2] - src[2]
            f.write(f"group pebble_tmp id {first}:{last}\n")
            f.write(f"displace_atoms pebble_tmp move {dx:.12e} {dy:.12e} {dz:.12e} units box\n")
            f.write("group pebble_tmp delete\n")


if __name__ == "__main__":
    main()
