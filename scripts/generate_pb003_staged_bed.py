#!/usr/bin/env python3
"""Generate staged pebble-bed creation and relocation commands.

Pebbles are first created far enough apart that the initial bond-creation
step cannot form cohesive bonds between different pebbles. After one
timestep, each 500-subparticle pebble is translated as a group into the
target packed-bed geometry; subsequent contacts between pebbles are therefore
ordinary Hertz contacts, not cohesive bonds.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def grid_centres(nx: int, ny: int, nz: int, spacing: float, z0: float) -> list[tuple[float, float, float]]:
    xs = [(i - (nx - 1) / 2) * spacing for i in range(nx)]
    ys = [(j - (ny - 1) / 2) * spacing for j in range(ny)]
    zs = [z0 + k * spacing for k in range(nz)]
    return [(x, y, z) for z in zs for y in ys for x in xs]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-output", type=Path, required=True)
    parser.add_argument("--move-output", type=Path, required=True)
    parser.add_argument("--nx", type=int, default=2)
    parser.add_argument("--ny", type=int, default=2)
    parser.add_argument("--nz", type=int, default=3)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--far-spacing", type=float, default=0.00135)
    parser.add_argument("--target-spacing", type=float, default=0.00098)
    parser.add_argument("--far-z0", type=float, default=-0.00135)
    parser.add_argument("--target-z0", type=float, default=-0.00098)
    args = parser.parse_args()

    far = grid_centres(args.nx, args.ny, args.nz, args.far_spacing, args.far_z0)
    target = grid_centres(args.nx, args.ny, args.nz, args.target_spacing, args.target_z0)
    if len(far) != len(target):
        raise SystemExit("far and target centre counts differ")

    args.create_output.parent.mkdir(parents=True, exist_ok=True)
    with args.create_output.open("w") as f:
        f.write("# Auto-generated PB-003 staged pebble bed\n")
        f.write("# Stage A: create separated pebbles and define atom-id groups\n")
        for i, (x, y, z) in enumerate(far, start=1):
            first = (i - 1) * args.nspheres + 1
            last = i * args.nspheres
            f.write(f"create_particles clump single {x:.12e} {y:.12e} {z:.12e} velocity 0.0 0.0 0.0\n")
            f.write(f"group pebble{i:02d} id {first}:{last}\n")
        f.write(f"# total_pebbles {len(far)}\n")

    args.move_output.parent.mkdir(parents=True, exist_ok=True)
    with args.move_output.open("w") as f:
        f.write("# Auto-generated PB-003 staged pebble bed\n")
        f.write("# Stage B: translate intact bonded pebbles into the target bed\n")
        for i, (src, dst) in enumerate(zip(far, target), start=1):
            dx, dy, dz = (dst[j] - src[j] for j in range(3))
            f.write(f"displace_atoms pebble{i:02d} move {dx:.12e} {dy:.12e} {dz:.12e} units box\n")


if __name__ == "__main__":
    main()
