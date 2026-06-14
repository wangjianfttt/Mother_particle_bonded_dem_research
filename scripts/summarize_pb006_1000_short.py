#!/usr/bin/env python3
"""Build a compact PB-006 1000-pebble short-compression summary table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any


FIELDNAMES = [
    "case",
    "npebbles",
    "localized_events",
    "localized_broken_bonds",
    "broken_pebbles",
    "first_break_displacement_mm",
    "first_break_pebble_id",
    "final_top_force_N",
    "top_bin_broken_bonds",
    "second_bin_broken_bonds",
    "bed_height_mm",
    "top_bin_count",
    "global_mean_degree",
]


def read_csv(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists() or path.stat().st_size == 0:
        return []
    try:
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return []
            return [dict(row) for row in reader]
    except (OSError, csv.Error, UnicodeDecodeError):
        return []


def first_present(row: dict[str, Any], names: list[str]) -> str:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return str(value)
    return ""


def to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_int(value: Any) -> int | None:
    num = to_float(value)
    return int(num) if num is not None else None


def sum_int(rows: list[dict[str, str]], columns: list[str]) -> int | str:
    total = 0
    seen = False
    for row in rows:
        value = to_int(first_present(row, columns))
        if value is not None:
            total += value
            seen = True
    return total if seen else ""


def final_top_force(thermo_rows: list[dict[str, str]]) -> str:
    force_columns = ["top_forc", "v_top_force_z", "top_force_z_N", "top_force_N"]
    for row in reversed(thermo_rows):
        value = first_present(row, force_columns)
        if value:
            return value
    return ""


def first_break_from_thermo(thermo_rows: list[dict[str, str]]) -> str:
    for row in thermo_rows:
        broken = to_int(first_present(row, ["bond_bro", "bond_broken", "v_bond_broken"]))
        if broken is not None and broken > 0:
            disp_m = to_float(first_present(row, ["top_disp", "v_top_disp", "top_displacement_m"]))
            if disp_m is not None:
                return f"{disp_m * 1000.0:.12g}"
    return ""


def first_break(events: list[dict[str, str]]) -> tuple[str, str]:
    if not events:
        return "", ""
    event = events[0]
    return (
        first_present(event, ["top_displacement_mm", "first_break_displacement_mm"]),
        first_present(event, ["pebble_id", "first_break_pebble_id", "first_break_pebble"]),
    )


def damaged_pebbles_from_final_loss(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        row
        for row in rows
        if (to_int(first_present(row, ["final_broken_internal_bonds", "broken_internal_bonds"])) or 0) > 0
    ]


def broken_pebble_count(
    events: list[dict[str, str]],
    pebble_rows: list[dict[str, str]],
    final_loss_rows: list[dict[str, str]],
) -> int | str:
    if final_loss_rows:
        return len(damaged_pebbles_from_final_loss(final_loss_rows))

    if pebble_rows:
        count = 0
        seen = False
        for row in pebble_rows:
            broken = to_int(first_present(row, ["total_new_broken_bonds", "broken_bonds"]))
            if broken is not None:
                seen = True
                if broken > 0:
                    count += 1
        if seen:
            return count

    if events:
        ids = {
            first_present(row, ["pebble_id", "first_break_pebble_id", "first_break_pebble"])
            for row in events
            if to_int(first_present(row, ["new_broken_bonds", "delta_broken_since_previous_dump"])) not in (None, 0)
        }
        return len({pid for pid in ids if pid})
    return ""


def height_bin_bonds(
    height_rows: list[dict[str, str]],
    final_loss_rows: list[dict[str, str]],
) -> tuple[int | str, int | str]:
    parsed: list[tuple[int, dict[str, str]]] = []
    for row in height_rows:
        height_bin = to_int(row.get("height_bin"))
        if height_bin is not None:
            parsed.append((height_bin, row))
    if not parsed:
        return "", ""

    parsed.sort(key=lambda item: item[0], reverse=True)
    values: list[int | str] = []
    for _, row in parsed[:2]:
        values.append(sum_int([row], ["total_new_broken_bonds", "broken_bonds"]))
    while len(values) < 2:
        values.append("")
    return values[0], values[1]


def height_bin_bonds_from_final_loss(
    final_loss_rows: list[dict[str, str]], height_bins: int = 8
) -> tuple[int | str, int | str]:
    zs = [to_float(row.get("initial_z")) for row in final_loss_rows]
    zs = [value for value in zs if value is not None]
    if not zs:
        return "", ""
    zmin, zmax = min(zs), max(zs)
    totals = {height_bin: 0 for height_bin in range(1, height_bins + 1)}
    for row in final_loss_rows:
        z = to_float(row.get("initial_z"))
        broken = to_int(first_present(row, ["final_broken_internal_bonds", "broken_internal_bonds"]))
        if z is None or broken is None:
            continue
        if zmax <= zmin:
            height_bin = 1
        else:
            height_bin = int((z - zmin) / (zmax - zmin) * height_bins) + 1
            height_bin = max(1, min(height_bins, height_bin))
        totals[height_bin] += broken
    return totals[height_bins], totals.get(height_bins - 1, "")


def bed_height_mm(
    packing_rows: list[dict[str, str]], height_rows: list[dict[str, str]]
) -> str:
    if packing_rows:
        value = first_present(
            packing_rows[0],
            ["bed_height_mm", "settled_bed_height_mm", "height_mm"],
        )
        if value:
            return value

    zmins = [to_float(row.get("zmin")) for row in height_rows]
    zmaxs = [to_float(row.get("zmax")) for row in height_rows]
    zmins = [value for value in zmins if value is not None]
    zmaxs = [value for value in zmaxs if value is not None]
    if zmins and zmaxs:
        return f"{(max(zmaxs) - min(zmins)) * 1000.0:.12g}"
    return ""


def infer_case(
    explicit: str, packing_rows: list[dict[str, str]], thermo_path: Path | None
) -> str:
    if explicit:
        return explicit
    if packing_rows:
        value = first_present(packing_rows[0], ["case", "case_label", "seed"])
        if value:
            return value
    if thermo_path:
        name = thermo_path.name
        return name.removesuffix("_thermo.csv").removesuffix(".csv")
    return ""


def infer_npebbles(
    default: str,
    packing_rows: list[dict[str, str]],
    pebble_rows: list[dict[str, str]],
) -> str | int:
    if packing_rows:
        value = first_present(packing_rows[0], ["npebbles", "mother_pebbles"])
        if value:
            return value
    if pebble_rows:
        return len(pebble_rows)
    return default


def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    thermo = read_csv(args.thermo)
    events = read_csv(args.events)
    height = read_csv(args.height_summary)
    pebbles = read_csv(args.pebble_summary)
    packing = read_csv(args.packing_summary)
    final_loss = read_csv(args.final_pebble_loss)

    first_disp, first_pid = first_break(events)
    if not first_disp:
        first_disp = first_break_from_thermo(thermo)
    if not first_pid and final_loss:
        damaged = damaged_pebbles_from_final_loss(final_loss)
        if len(damaged) == 1:
            first_pid = first_present(damaged[0], ["pebble_id"])

    top_bin_bonds, second_bin_bonds = height_bin_bonds(height, final_loss)
    if top_bin_bonds == "" and final_loss:
        top_bin_bonds, second_bin_bonds = height_bin_bonds_from_final_loss(final_loss)
    packing_row = packing[0] if packing else {}
    localized_broken = sum_int(events, ["new_broken_bonds", "delta_broken_since_previous_dump"])
    if localized_broken == "" and final_loss:
        localized_broken = sum_int(final_loss, ["final_broken_internal_bonds", "broken_internal_bonds"])

    return {
        "case": infer_case(args.case, packing, args.thermo),
        "npebbles": infer_npebbles(args.npebbles, packing, pebbles),
        "localized_events": len(events) if events else "",
        "localized_broken_bonds": localized_broken,
        "broken_pebbles": broken_pebble_count(events, pebbles, final_loss),
        "first_break_displacement_mm": first_disp,
        "first_break_pebble_id": first_pid,
        "final_top_force_N": final_top_force(thermo),
        "top_bin_broken_bonds": top_bin_bonds,
        "second_bin_broken_bonds": second_bin_bonds,
        "bed_height_mm": bed_height_mm(packing, height),
        "top_bin_count": first_present(packing_row, ["top_bin_count"]),
        "global_mean_degree": first_present(packing_row, ["global_mean_degree"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize PB-006 1000-pebble short-compression post-processing CSVs."
    )
    parser.add_argument("--thermo", type=Path, help="Thermo CSV from compression run.")
    parser.add_argument("--events", type=Path, help="Breakage events CSV.")
    parser.add_argument("--height-summary", type=Path, help="Height-bin breakage summary CSV.")
    parser.add_argument("--pebble-summary", type=Path, help="Per-pebble breakage summary CSV.")
    parser.add_argument("--final-pebble-loss", type=Path, help="Final per-pebble bond-loss CSV.")
    parser.add_argument("--packing-summary", type=Path, help="Packing descriptor summary CSV.")
    parser.add_argument("--case", default="", help="Case label; inferred from inputs when omitted.")
    parser.add_argument("--npebbles", default="1000", help="Fallback pebble count when inputs are absent.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tables/pb006_1000_short_compression_summary.csv"),
        help="Output summary CSV.",
    )
    args = parser.parse_args()

    row = build_summary(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)
    print(args.output)


if __name__ == "__main__":
    main()
