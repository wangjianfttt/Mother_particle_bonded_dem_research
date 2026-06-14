#!/usr/bin/env python3
"""Generate bonded-template creation and relocation includes from proxy centres."""

from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path


def random_quaternion(rng: random.Random) -> tuple[float, float, float, float]:
    u1 = rng.random()
    u2 = rng.random()
    u3 = rng.random()
    qx = math.sqrt(1.0 - u1) * math.sin(2.0 * math.pi * u2)
    qy = math.sqrt(1.0 - u1) * math.cos(2.0 * math.pi * u2)
    qz = math.sqrt(u1) * math.sin(2.0 * math.pi * u3)
    qw = math.sqrt(u1) * math.cos(2.0 * math.pi * u3)
    return qw, qx, qy, qz


def far_centres(n: int, spacing: float) -> list[tuple[float, float, float]]:
    nx = math.ceil(n ** (1.0 / 3.0))
    ny = nx
    nz = math.ceil(n / (nx * ny))
    xs = [(i - (nx - 1) / 2.0) * spacing for i in range(nx)]
    ys = [(j - (ny - 1) / 2.0) * spacing for j in range(ny)]
    zs = [-(k + 1) * spacing for k in range(nz)]
    centres = [(x, y, z) for z in zs for y in ys for x in xs]
    return centres[:n]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--centers", type=Path, required=True)
    parser.add_argument("--create-output", type=Path, required=True)
    parser.add_argument("--move-output", type=Path, required=True)
    parser.add_argument("--metadata-output", type=Path, required=True)
    parser.add_argument("--bounds-output", type=Path, required=True)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--far-spacing", type=float, default=0.00135)
    parser.add_argument("--orientation-seed", type=int, default=20260524)
    parser.add_argument("--side-margin", type=float, default=0.00065)
    parser.add_argument("--vertical-margin", type=float, default=0.00005)
    args = parser.parse_args()

    with args.centers.open(newline="") as f:
        targets = list(csv.DictReader(f))
    if not targets:
        raise SystemExit("No proxy centres supplied")

    far = far_centres(len(targets), args.far_spacing)
    rng = random.Random(args.orientation_seed)

    args.create_output.parent.mkdir(parents=True, exist_ok=True)
    args.move_output.parent.mkdir(parents=True, exist_ok=True)
    args.metadata_output.parent.mkdir(parents=True, exist_ok=True)
    args.bounds_output.parent.mkdir(parents=True, exist_ok=True)

    metadata_rows = []
    with args.create_output.open("w") as create_file, args.move_output.open("w") as move_file:
        create_file.write("# Auto-generated far-field bonded template creation from proxy packing centres\n")
        move_file.write("# Auto-generated relocation to proxy packing centres using one reusable temporary group\n")
        for i, (src, target) in enumerate(zip(far, targets), start=1):
            q1, q2, q3, q4 = random_quaternion(rng)
            create_file.write(
                "create_particles clump single "
                f"{src[0]:.12e} {src[1]:.12e} {src[2]:.12e} "
                "velocity 0.0 0.0 0.0 "
                f"orientation {q1:.12e} {q2:.12e} {q3:.12e} {q4:.12e}\n"
            )
            x, y, z = float(target["x"]), float(target["y"]), float(target["z"])
            first = (i - 1) * args.nspheres + 1
            last = i * args.nspheres
            move_file.write(f"group pebble_tmp id {first}:{last}\n")
            move_file.write(
                "displace_atoms pebble_tmp move "
                f"{x - src[0]:.12e} {y - src[1]:.12e} {z - src[2]:.12e} units box\n"
            )
            move_file.write("group pebble_tmp delete\n")
            metadata_rows.append(
                {
                    "pebble_id": i,
                    "proxy_atom_id": target["proxy_atom_id"],
                    "target_x": x,
                    "target_y": y,
                    "target_z": z,
                    "far_x": src[0],
                    "far_y": src[1],
                    "far_z": src[2],
                    "q1": q1,
                    "q2": q2,
                    "q3": q3,
                    "q4": q4,
                }
            )

    with args.metadata_output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(metadata_rows[0]))
        writer.writeheader()
        writer.writerows(metadata_rows)

    xs = [float(r["x"]) for r in targets]
    ys = [float(r["y"]) for r in targets]
    zs = [float(r["z"]) for r in targets]
    radii = [float(r["radius"]) for r in targets]
    radius = max(radii)
    bounds = {
        "xlo": min(xs) - radius - args.side_margin,
        "xhi": max(xs) + radius + args.side_margin,
        "ylo": min(ys) - radius - args.side_margin,
        "yhi": max(ys) + radius + args.side_margin,
        "zlo": min(zs) - radius - args.vertical_margin,
        "zhi": max(zs) + radius + args.vertical_margin,
        "npebbles": len(targets),
        "nspheres": args.nspheres,
    }
    with args.bounds_output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(bounds))
        writer.writeheader()
        writer.writerow(bounds)

    print(args.create_output)
    print(args.move_output)
    print(args.metadata_output)
    print(args.bounds_output)


if __name__ == "__main__":
    main()
