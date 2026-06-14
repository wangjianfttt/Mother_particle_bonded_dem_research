#!/usr/bin/env python3
"""Create a LIGGGHTS multisphere template with two particle types separated by a plane."""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True, help="Input x y z radius multisphere file.")
    parser.add_argument("--output", type=Path, required=True, help="Output x y z radius type file.")
    parser.add_argument("--normal", nargs=3, type=float, default=(1.0, 0.0, 0.0))
    parser.add_argument("--offset", type=float, default=0.0, help="Plane offset in m: n dot x = offset.")
    parser.add_argument("--type-negative", type=int, default=1)
    parser.add_argument("--type-positive", type=int, default=2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    nx, ny, nz = args.normal
    norm = math.sqrt(nx * nx + ny * ny + nz * nz)
    if norm == 0.0:
        raise SystemExit("--normal must be non-zero")
    nx, ny, nz = nx / norm, ny / norm, nz / norm

    args.output.parent.mkdir(parents=True, exist_ok=True)
    negative = 0
    positive = 0
    with args.input.open() as src, args.output.open("w") as dst:
        for line in src:
            parts = line.split()
            if len(parts) < 4:
                continue
            x, y, z, r = map(float, parts[:4])
            side = nx * x + ny * y + nz * z - args.offset
            atom_type = args.type_positive if side >= 0.0 else args.type_negative
            positive += atom_type == args.type_positive
            negative += atom_type == args.type_negative
            dst.write(f"{x:.12e} {y:.12e} {z:.12e} {r:.12e} {atom_type}\n")

    print(
        f"wrote {args.output} with type {args.type_negative}: {negative}, "
        f"type {args.type_positive}: {positive}"
    )


if __name__ == "__main__":
    main()
