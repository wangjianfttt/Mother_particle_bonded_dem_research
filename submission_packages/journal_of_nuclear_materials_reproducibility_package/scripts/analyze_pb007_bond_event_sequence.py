#!/usr/bin/env python3
"""Extract PB-007 mother-pebble bond-breakage event sequences from local dumps."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def pebble_id(atom_id: int, nspheres: int, npebbles: int) -> int | None:
    idx = (atom_id - 1) // nspheres + 1
    return idx if 1 <= idx <= npebbles else None


def read_dump_edges(path: Path, nspheres: int, npebbles: int) -> tuple[int, dict[int, set[tuple[int, int]]]]:
    timestep: int | None = None
    edges_by_pebble = {i: set() for i in range(1, npebbles + 1)}
    in_entries = False
    with path.open() as handle:
        for line in handle:
            stripped = line.strip()
            if stripped == "ITEM: TIMESTEP":
                timestep = int(next(handle).strip())
                continue
            if stripped.startswith("ITEM: ENTRIES"):
                in_entries = True
                continue
            if not in_entries:
                continue
            parts = stripped.split()
            if len(parts) < 2:
                continue
            atom_a, atom_b = int(float(parts[0])), int(float(parts[1]))
            pebble_a = pebble_id(atom_a, nspheres, npebbles)
            pebble_b = pebble_id(atom_b, nspheres, npebbles)
            if pebble_a is not None and pebble_a == pebble_b:
                edges_by_pebble[pebble_a].add((atom_a, atom_b) if atom_a < atom_b else (atom_b, atom_a))
    if timestep is None:
        raise ValueError(f"No timestep found in {path}")
    return timestep, edges_by_pebble


def read_thermo(path: Path | None) -> dict[int, dict[str, str]]:
    if path is None or not path.exists():
        return {}
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {int(float(row.get("Step", row.get("step", 0)))): row for row in rows}


def nearest_thermo(step: int, thermo: dict[int, dict[str, str]]) -> dict[str, str]:
    if not thermo:
        return {}
    nearest_step = min(thermo, key=lambda item: abs(item - step))
    return thermo[nearest_step]


def read_metadata(path: Path | None, npebbles: int) -> dict[int, dict[str, str]]:
    meta = {i: {"pebble_z_mm": "", "rank_from_top": ""} for i in range(1, npebbles + 1)}
    if path is None or not path.exists():
        return meta
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    z_values: list[tuple[int, float]] = []
    for row in rows:
        pid = int(row["pebble_id"])
        z_m = float(row.get("rigid_zcm", row.get("insertion_origin_z", 0.0)))
        meta[pid]["pebble_z_mm"] = f"{z_m * 1e3:.9g}"
        z_values.append((pid, z_m))
    for rank, (pid, _) in enumerate(sorted(z_values, key=lambda item: item[1], reverse=True), start=1):
        meta[pid]["rank_from_top"] = str(rank)
    return meta


def value(row: dict[str, str], *names: str) -> str:
    for name in names:
        if name in row and row[name] not in ("", None):
            return row[name]
    return ""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bond_dumps", nargs="+", type=Path)
    parser.add_argument("--npebbles", type=int, default=100)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--thermo", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--series-output", type=Path, required=True)
    parser.add_argument("--events-output", type=Path, required=True)
    args = parser.parse_args()

    dump_series = [read_dump_edges(path, args.nspheres, args.npebbles) for path in args.bond_dumps]
    dump_series.sort(key=lambda item: item[0])
    if not dump_series:
        raise SystemExit("No PB-007 bond dumps supplied.")

    reference_step, reference_edges = max(
        dump_series,
        key=lambda item: sum(len(edges) for edges in item[1].values()),
    )
    initial_counts = {pid: len(reference_edges[pid]) for pid in range(1, args.npebbles + 1)}
    thermo = read_thermo(args.thermo)
    metadata = read_metadata(args.metadata, args.npebbles)

    previous_broken = {pid: 0 for pid in range(1, args.npebbles + 1)}
    series_rows: list[dict[str, str | int | float]] = []
    event_rows: list[dict[str, str | int | float]] = []
    event_index = 1

    for step, edges_by_pebble in dump_series:
        thermo_row = nearest_thermo(step, thermo)
        top_disp_m = value(thermo_row, "top_disp", "v_top_disp")
        top_disp_mm = float(top_disp_m) * 1e3 if top_disp_m else ""
        top_force = value(thermo_row, "top_forc", "top_force", "v_top_force")
        bottom_force = value(thermo_row, "bottom_f", "bottom_force", "v_bottom_force")
        side_force = value(thermo_row, "side_for", "side_force", "v_side_force")
        all_wall_force = value(thermo_row, "all_wall", "all_wall_force", "v_all_wall_force")

        for pid in range(1, args.npebbles + 1):
            intact = len(edges_by_pebble[pid])
            broken = max(0, initial_counts[pid] - intact)
            delta = broken - previous_broken[pid]
            base = {
                "timestep": step,
                "pebble_id": pid,
                "pebble_z_mm": metadata[pid]["pebble_z_mm"],
                "rank_from_top": metadata[pid]["rank_from_top"],
                "reference_step": reference_step,
                "initial_internal_bonds": initial_counts[pid],
                "intact_internal_bonds": intact,
                "broken_internal_bonds": broken,
                "delta_broken_since_previous_dump": delta,
                "top_displacement_m": top_disp_m,
                "top_displacement_mm": top_disp_mm,
                "top_force_z_N": top_force,
                "bottom_force_z_N": bottom_force,
                "side_force_z_N": side_force,
                "all_wall_force_z_N": all_wall_force,
            }
            series_rows.append(base)
            if delta > 0:
                event_row = dict(base)
                event_row["event_index"] = event_index
                event_row["new_broken_bonds"] = delta
                event_row["cumulative_broken_bonds"] = broken
                event_rows.append(event_row)
                event_index += 1
            previous_broken[pid] = broken

    args.series_output.parent.mkdir(parents=True, exist_ok=True)
    with args.series_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(series_rows[0]))
        writer.writeheader()
        writer.writerows(series_rows)

    event_fieldnames = [
        "event_index",
        "timestep",
        "pebble_id",
        "pebble_z_mm",
        "rank_from_top",
        "reference_step",
        "initial_internal_bonds",
        "intact_internal_bonds",
        "broken_internal_bonds",
        "delta_broken_since_previous_dump",
        "new_broken_bonds",
        "cumulative_broken_bonds",
        "top_displacement_m",
        "top_displacement_mm",
        "top_force_z_N",
        "bottom_force_z_N",
        "side_force_z_N",
        "all_wall_force_z_N",
    ]
    with args.events_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=event_fieldnames)
        writer.writeheader()
        writer.writerows(event_rows)

    print(args.series_output)
    print(args.events_output)


if __name__ == "__main__":
    main()
