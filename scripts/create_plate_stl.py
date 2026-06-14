#!/usr/bin/env python3
"""Create simple square STL plates for single-pebble compression tests."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", type=float, default=0.002, help="Plate side length in m.")
    parser.add_argument("--z", type=float, required=True, help="Plate z position in m.")
    parser.add_argument("--normal-z", type=float, required=True, choices=[-1.0, 1.0], help="Facet normal z.")
    parser.add_argument("--divisions", type=int, default=8, help="Number of square divisions per side.")
    parser.add_argument("--output", type=Path, required=True, help="Output ASCII STL path.")
    return parser.parse_args()


def write_plate(path: Path, side: float, z: float, normal_z: float, divisions: int) -> None:
    half = side / 2.0
    step = side / divisions

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        handle.write("solid plate\n")
        for ix in range(divisions):
            for iy in range(divisions):
                x0 = -half + ix * step
                x1 = x0 + step
                y0 = -half + iy * step
                y1 = y0 + step
                vertices = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]
                triangles = [(0, 1, 2), (0, 2, 3)] if normal_z > 0 else [(0, 2, 1), (0, 3, 2)]
                for tri in triangles:
                    handle.write(f"  facet normal 0 0 {normal_z:.1f}\n")
                    handle.write("    outer loop\n")
                    for idx in tri:
                        x, y, zz = vertices[idx]
                        handle.write(f"      vertex {x:.12e} {y:.12e} {zz:.12e}\n")
                    handle.write("    endloop\n")
                    handle.write("  endfacet\n")
        handle.write("endsolid plate\n")


def main() -> None:
    args = parse_args()
    write_plate(args.output, args.side, args.z, args.normal_z, args.divisions)


if __name__ == "__main__":
    main()
