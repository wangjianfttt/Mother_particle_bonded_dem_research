#!/usr/bin/env python3
"""Create six ASCII STL mesh walls for a rectangular pebble-bed box."""

from __future__ import annotations

import argparse
from pathlib import Path


def write_rect(
    path: Path,
    plane: str,
    value: float,
    a_min: float,
    a_max: float,
    b_min: float,
    b_max: float,
    normal: tuple[float, float, float],
    divisions_a: int,
    divisions_b: int,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    da = (a_max - a_min) / divisions_a
    db = (b_max - b_min) / divisions_b

    def vertex(a: float, b: float) -> tuple[float, float, float]:
        if plane == "z":
            return (a, b, value)
        if plane == "x":
            return (value, a, b)
        if plane == "y":
            return (a, value, b)
        raise ValueError(plane)

    nx, ny, nz = normal
    normal_positive = nx + ny + nz > 0
    with path.open("w") as handle:
        handle.write("solid wall\n")
        for ia in range(divisions_a):
            for ib in range(divisions_b):
                a0 = a_min + ia * da
                a1 = a0 + da
                b0 = b_min + ib * db
                b1 = b0 + db
                vertices = [vertex(a0, b0), vertex(a1, b0), vertex(a1, b1), vertex(a0, b1)]
                triangles = [(0, 1, 2), (0, 2, 3)] if normal_positive else [(0, 2, 1), (0, 3, 2)]
                for tri in triangles:
                    handle.write(f"  facet normal {nx:.1f} {ny:.1f} {nz:.1f}\n")
                    handle.write("    outer loop\n")
                    for idx in tri:
                        x, y, z = vertices[idx]
                        handle.write(f"      vertex {x:.12e} {y:.12e} {z:.12e}\n")
                    handle.write("    endloop\n")
                    handle.write("  endfacet\n")
        handle.write("endsolid wall\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--xlo", type=float, required=True)
    parser.add_argument("--xhi", type=float, required=True)
    parser.add_argument("--ylo", type=float, required=True)
    parser.add_argument("--yhi", type=float, required=True)
    parser.add_argument("--zlo", type=float, required=True)
    parser.add_argument("--zhi", type=float, required=True)
    parser.add_argument("--divisions", type=int, default=12)
    args = parser.parse_args()

    d = args.divisions
    out = args.output_dir
    write_rect(out / "bottom_plate.stl", "z", args.zlo, args.xlo, args.xhi, args.ylo, args.yhi, (0, 0, 1), d, d)
    write_rect(out / "top_plate.stl", "z", args.zhi, args.xlo, args.xhi, args.ylo, args.yhi, (0, 0, -1), d, d)
    write_rect(out / "xlo_wall.stl", "x", args.xlo, args.ylo, args.yhi, args.zlo, args.zhi, (1, 0, 0), d, d)
    write_rect(out / "xhi_wall.stl", "x", args.xhi, args.ylo, args.yhi, args.zlo, args.zhi, (-1, 0, 0), d, d)
    write_rect(out / "ylo_wall.stl", "y", args.ylo, args.xlo, args.xhi, args.zlo, args.zhi, (0, 1, 0), d, d)
    write_rect(out / "yhi_wall.stl", "y", args.yhi, args.xlo, args.xhi, args.zlo, args.zhi, (0, -1, 0), d, d)


if __name__ == "__main__":
    main()
