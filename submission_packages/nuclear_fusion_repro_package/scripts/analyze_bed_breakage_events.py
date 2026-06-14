#!/usr/bin/env python3
"""Extract per-mother-pebble breakage event sequences from bed bond dumps."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def timestep(path: Path) -> int:
    return int(path.stem.split("_")[-1])


def pebble_id(atom_id: int, nspheres: int, npebbles: int) -> int | None:
    idx = (atom_id - 1) // nspheres + 1
    return idx if 1 <= idx <= npebbles else None


def read_edges(path: Path, nspheres: int, npebbles: int) -> dict[int, set[tuple[int, int]]]:
    edges_by_pebble = {i: set() for i in range(1, npebbles + 1)}
    in_entries = False
    with path.open() as handle:
        for line in handle:
            if not in_entries:
                in_entries = line.startswith("ITEM: ENTRIES")
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            a, b = int(float(parts[0])), int(float(parts[1]))
            pa = pebble_id(a, nspheres, npebbles)
            pb = pebble_id(b, nspheres, npebbles)
            if pa is not None and pa == pb:
                edges_by_pebble[pa].add((a, b) if a < b else (b, a))
    return edges_by_pebble


def thermo_by_step(path: Path) -> dict[int, dict[str, str]]:
    if not path or not path.exists():
        return {}
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for row in rows:
        step = int(float(row.get("Step", row.get("step", 0))))
        out[step] = row
    return out


def nearest_thermo(step: int, thermo: dict[int, dict[str, str]]) -> dict[str, str]:
    if not thermo:
        return {}
    nearest = min(thermo, key=lambda s: abs(s - step))
    return thermo[nearest]


def fallback_top_displacement(step: int, pre_steps: int, top_speed: float, dt: float) -> str:
    if step <= pre_steps:
        return "0.0"
    return f"{top_speed * (step - pre_steps) * dt:.12g}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bond_dumps", nargs="+", type=Path)
    parser.add_argument("--npebbles", type=int, default=12)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--thermo", type=Path)
    parser.add_argument("--pre-steps", type=int, default=1001)
    parser.add_argument("--top-speed", type=float, default=0.5)
    parser.add_argument("--dt", type=float, default=5.0e-9)
    parser.add_argument("--series-output", type=Path, required=True)
    parser.add_argument("--events-output", type=Path, required=True)
    args = parser.parse_args()

    paths = sorted(args.bond_dumps, key=timestep)
    if not paths:
        raise SystemExit("No bond dumps supplied")
    thermo = thermo_by_step(args.thermo) if args.thermo else {}

    edge_series = [(timestep(path), read_edges(path, args.nspheres, args.npebbles)) for path in paths]
    reference_step, reference_edges = max(
        edge_series,
        key=lambda item: sum(len(edges) for edges in item[1].values()),
    )
    initial_counts = {pid: len(reference_edges[pid]) for pid in reference_edges}

    series_rows = []
    event_rows = []
    previous_broken = {pid: 0 for pid in range(1, args.npebbles + 1)}
    event_index = 1
    for step, edges_by_pebble in edge_series:
        thermo_row = nearest_thermo(step, thermo)
        top_disp = thermo_row.get("top_disp", thermo_row.get("v_top_disp", ""))
        if top_disp in ("", None):
            top_disp = fallback_top_displacement(step, args.pre_steps, args.top_speed, args.dt)
        top_force = thermo_row.get("top_forc", thermo_row.get("v_top_force_z", ""))
        bottom_force = thermo_row.get("bottom_f", thermo_row.get("v_bottom_force_z", ""))
        for pid in range(1, args.npebbles + 1):
            intact = len(edges_by_pebble[pid])
            broken = max(0, initial_counts[pid] - intact)
            delta = broken - previous_broken[pid]
            series_rows.append(
                {
                    "timestep": step,
                    "pebble_id": pid,
                    "reference_step": reference_step,
                    "initial_internal_bonds": initial_counts[pid],
                    "intact_internal_bonds": intact,
                    "broken_internal_bonds": broken,
                    "delta_broken_since_previous_dump": delta,
                    "top_displacement_m": top_disp,
                    "top_displacement_mm": float(top_disp) * 1e3 if top_disp not in ("", None) else "",
                    "top_force_z_N": top_force,
                    "bottom_force_z_N": bottom_force,
                }
            )
            if delta > 0:
                event_rows.append(
                    {
                        "event_index": event_index,
                        "timestep": step,
                        "pebble_id": pid,
                        "new_broken_bonds": delta,
                        "cumulative_broken_bonds": broken,
                        "top_displacement_m": top_disp,
                        "top_displacement_mm": float(top_disp) * 1e3 if top_disp not in ("", None) else "",
                        "top_force_z_N": top_force,
                        "bottom_force_z_N": bottom_force,
                    }
                )
                event_index += 1
            previous_broken[pid] = broken

    args.series_output.parent.mkdir(parents=True, exist_ok=True)
    with args.series_output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(series_rows[0]))
        writer.writeheader()
        writer.writerows(series_rows)

    with args.events_output.open("w", newline="") as f:
        fieldnames = [
            "event_index",
            "timestep",
            "pebble_id",
            "new_broken_bonds",
            "cumulative_broken_bonds",
            "top_displacement_m",
            "top_displacement_mm",
            "top_force_z_N",
            "bottom_force_z_N",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(event_rows)

    print(args.series_output)
    print(args.events_output)


if __name__ == "__main__":
    main()
