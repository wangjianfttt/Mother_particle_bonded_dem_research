#!/usr/bin/env python3
"""Summarize PB-006 contact-local dumps as mother-pebble force networks."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def dump_step(path: Path) -> int:
    stem = path.stem
    tail = stem.split("_")[-1]
    if tail.isdigit():
        return int(tail)
    raise ValueError(f"Cannot infer timestep from {path}")


def read_local_rows(path: Path) -> tuple[int, list[list[float]]]:
    with path.open() as f:
        if not f.readline().startswith("ITEM: TIMESTEP"):
            raise ValueError(f"{path} is not a local dump")
        step = int(f.readline().strip())
        f.readline()
        nrows = int(f.readline().strip())
        f.readline()
        for _ in range(3):
            f.readline()
        f.readline()
        rows = [[float(x) for x in f.readline().split()] for _ in range(nrows)]
    return step, rows


def pebble_id(atom_id: int, nspheres: int) -> int:
    return (atom_id - 1) // nspheres + 1


def force_mag(row: list[float], offset: int) -> float:
    return math.sqrt(row[offset] ** 2 + row[offset + 1] ** 2 + row[offset + 2] ** 2)


def summarize_pair_dump(path: Path, nspheres: int) -> tuple[dict[str, object], list[dict[str, object]]]:
    step, rows = read_local_rows(path)
    edge_stats: dict[tuple[int, int], dict[str, float]] = {}
    internal_contacts = 0
    inter_contacts = 0
    inter_force_sum = 0.0
    inter_normal_sum = 0.0
    inter_tangential_sum = 0.0

    # Column order for `id force force_normal force_tangential`:
    # id1, id2, periodic_flag, Fx, Fy, Fz, Fn_x, Fn_y, Fn_z, Ft_x, Ft_y, Ft_z.
    for row in rows:
        if len(row) < 12:
            continue
        a_atom = int(row[0])
        b_atom = int(row[1])
        a = pebble_id(a_atom, nspheres)
        b = pebble_id(b_atom, nspheres)
        f = force_mag(row, 3)
        fn = force_mag(row, 6)
        ft = force_mag(row, 9)
        if a == b:
            internal_contacts += 1
            continue
        inter_contacts += 1
        inter_force_sum += f
        inter_normal_sum += fn
        inter_tangential_sum += ft
        key = tuple(sorted((a, b)))
        stat = edge_stats.setdefault(key, {"contact_count": 0, "force_sum": 0.0, "normal_sum": 0.0, "tangential_sum": 0.0, "force_max": 0.0})
        stat["contact_count"] += 1
        stat["force_sum"] += f
        stat["normal_sum"] += fn
        stat["tangential_sum"] += ft
        stat["force_max"] = max(stat["force_max"], f)

    summary = {
        "timestep": step,
        "inter_pebble_edges": len(edge_stats),
        "inter_subparticle_contacts": inter_contacts,
        "internal_subparticle_contacts": internal_contacts,
        "inter_force_sum_N": inter_force_sum,
        "inter_normal_force_sum_N": inter_normal_sum,
        "inter_tangential_force_sum_N": inter_tangential_sum,
    }
    edge_rows = []
    for (a, b), stat in sorted(edge_stats.items(), key=lambda item: item[1]["force_sum"], reverse=True):
        edge_rows.append(
            {
                "timestep": step,
                "pebble_i": a,
                "pebble_j": b,
                "contact_count": int(stat["contact_count"]),
                "force_sum_N": stat["force_sum"],
                "normal_force_sum_N": stat["normal_sum"],
                "tangential_force_sum_N": stat["tangential_sum"],
                "max_contact_force_N": stat["force_max"],
            }
        )
    return summary, edge_rows


def summarize_topwall_dump(path: Path, nspheres: int) -> tuple[dict[str, object], list[dict[str, object]]]:
    step, rows = read_local_rows(path)
    pebble_stats: dict[int, dict[str, float]] = {}
    force_sum = 0.0
    normal_sum = 0.0

    # Column order for wall/gran/local `id force force_normal force_tangential`:
    # mesh_id, triangle_id, atom_id, Fx, Fy, Fz, Fn_x, Fn_y, Fn_z, Ft_x, Ft_y, Ft_z.
    for row in rows:
        if len(row) < 12:
            continue
        pid = pebble_id(int(row[2]), nspheres)
        f = force_mag(row, 3)
        fn = force_mag(row, 6)
        ft = force_mag(row, 9)
        force_sum += f
        normal_sum += fn
        stat = pebble_stats.setdefault(pid, {"contact_count": 0, "force_sum": 0.0, "normal_sum": 0.0, "tangential_sum": 0.0, "force_max": 0.0})
        stat["contact_count"] += 1
        stat["force_sum"] += f
        stat["normal_sum"] += fn
        stat["tangential_sum"] += ft
        stat["force_max"] = max(stat["force_max"], f)

    summary = {
        "timestep": step,
        "topwall_pebbles": len(pebble_stats),
        "topwall_subparticle_contacts": len(rows),
        "topwall_force_sum_N": force_sum,
        "topwall_normal_force_sum_N": normal_sum,
    }
    pebble_rows = []
    for pid, stat in sorted(pebble_stats.items(), key=lambda item: item[1]["force_sum"], reverse=True):
        pebble_rows.append(
            {
                "timestep": step,
                "pebble_id": pid,
                "contact_count": int(stat["contact_count"]),
                "force_sum_N": stat["force_sum"],
                "normal_force_sum_N": stat["normal_sum"],
                "tangential_force_sum_N": stat["tangential_sum"],
                "max_contact_force_N": stat["force_max"],
            }
        )
    return summary, pebble_rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        if not rows:
            f.write("")
            return
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair-dumps", nargs="*", type=Path, default=[])
    parser.add_argument("--topwall-dumps", nargs="*", type=Path, default=[])
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--pair-summary-output", type=Path)
    parser.add_argument("--pair-edge-output", type=Path)
    parser.add_argument("--topwall-summary-output", type=Path)
    parser.add_argument("--topwall-pebble-output", type=Path)
    args = parser.parse_args()

    pair_summaries = []
    pair_edges = []
    for path in sorted(args.pair_dumps, key=dump_step):
        summary, edges = summarize_pair_dump(path, args.nspheres)
        pair_summaries.append(summary)
        pair_edges.extend(edges)

    wall_summaries = []
    wall_pebbles = []
    for path in sorted(args.topwall_dumps, key=dump_step):
        summary, pebbles = summarize_topwall_dump(path, args.nspheres)
        wall_summaries.append(summary)
        wall_pebbles.extend(pebbles)

    if args.pair_summary_output:
        write_csv(args.pair_summary_output, pair_summaries)
    if args.pair_edge_output:
        write_csv(args.pair_edge_output, pair_edges)
    if args.topwall_summary_output:
        write_csv(args.topwall_summary_output, wall_summaries)
    if args.topwall_pebble_output:
        write_csv(args.topwall_pebble_output, wall_pebbles)


if __name__ == "__main__":
    main()
