#!/usr/bin/env python3
"""Generate a small ordered pebble-bed insertion file for PB-001."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--nx", type=int, default=2)
    parser.add_argument("--ny", type=int, default=2)
    parser.add_argument("--nz", type=int, default=3)
    parser.add_argument("--spacing", type=float, default=0.00108)
    parser.add_argument("--z0", type=float, default=-0.00108)
    args = parser.parse_args()

    xs = [(i - (args.nx - 1) / 2) * args.spacing for i in range(args.nx)]
    ys = [(j - (args.ny - 1) / 2) * args.spacing for j in range(args.ny)]
    zs = [args.z0 + k * args.spacing for k in range(args.nz)]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write("# Auto-generated PB-001 ordered pebble centres\n")
        count = 0
        for z in zs:
            for y in ys:
                for x in xs:
                    count += 1
                    f.write(f"create_particles clump single {x:.12e} {y:.12e} {z:.12e} velocity 0.0 0.0 0.0\n")
        f.write(f"# total_pebbles {count}\n")


if __name__ == "__main__":
    main()
