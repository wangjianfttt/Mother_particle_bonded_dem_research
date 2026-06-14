#!/usr/bin/env python3
"""Create a rectangular vertical or horizontal STL wall."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--plane", choices=["x", "y", "z"], required=True)
    p.add_argument("--coord", type=float, required=True)
    p.add_argument("--a-min", type=float, required=True)
    p.add_argument("--a-max", type=float, required=True)
    p.add_argument("--b-min", type=float, required=True)
    p.add_argument("--b-max", type=float, required=True)
    p.add_argument("--normal", type=float, choices=[-1.0, 1.0], required=True)
    p.add_argument("--div-a", type=int, default=8)
    p.add_argument("--div-b", type=int, default=8)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()

    def vertex(a: float, b: float) -> tuple[float, float, float]:
        if args.plane == "x":
            return args.coord, a, b
        if args.plane == "y":
            return a, args.coord, b
        return a, b, args.coord

    normal_vec = {
        "x": (args.normal, 0.0, 0.0),
        "y": (0.0, args.normal, 0.0),
        "z": (0.0, 0.0, args.normal),
    }[args.plane]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    da = (args.a_max - args.a_min) / args.div_a
    db = (args.b_max - args.b_min) / args.div_b
    with args.output.open("w") as f:
        f.write("solid wall\n")
        for ia in range(args.div_a):
            for ib in range(args.div_b):
                a0 = args.a_min + ia * da
                a1 = a0 + da
                b0 = args.b_min + ib * db
                b1 = b0 + db
                verts = [vertex(a0, b0), vertex(a1, b0), vertex(a1, b1), vertex(a0, b1)]
                tris = [(0, 1, 2), (0, 2, 3)] if args.normal > 0 else [(0, 2, 1), (0, 3, 2)]
                for tri in tris:
                    f.write(f"  facet normal {normal_vec[0]:.1f} {normal_vec[1]:.1f} {normal_vec[2]:.1f}\n")
                    f.write("    outer loop\n")
                    for idx in tri:
                        x, y, z = verts[idx]
                        f.write(f"      vertex {x:.12e} {y:.12e} {z:.12e}\n")
                    f.write("    endloop\n")
                    f.write("  endfacet\n")
        f.write("endsolid wall\n")


if __name__ == "__main__":
    main()
