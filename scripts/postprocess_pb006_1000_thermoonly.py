#!/usr/bin/env python3
"""Post-process a PB-006 1000-pebble thermo-only compression case."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def to_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def to_int(value: str | None) -> int | None:
    value_float = to_float(value)
    return int(value_float) if value_float is not None else None


def read_internal_counts(path: Path, nspheres: int, npebbles: int) -> dict[int, int]:
    counts = {pid: 0 for pid in range(1, npebbles + 1)}
    in_entries = False
    with path.open() as handle:
        for raw in handle:
            if not in_entries:
                if raw.startswith("ITEM: ENTRIES"):
                    in_entries = True
                continue
            parts = raw.split()
            if len(parts) < 2:
                continue
            atom_a = int(float(parts[0]))
            atom_b = int(float(parts[1]))
            pebble_a = (atom_a - 1) // nspheres + 1
            pebble_b = (atom_b - 1) // nspheres + 1
            if 1 <= pebble_a <= npebbles and pebble_a == pebble_b:
                counts[pebble_a] += 1
    return counts


def final_loss_rows(
    bond_dump: Path,
    metadata: Path,
    npebbles: int,
    nspheres: int,
    initial_bonds_per_pebble: int,
) -> list[dict[str, str | int]]:
    counts = read_internal_counts(bond_dump, nspheres, npebbles)
    meta_rows = {int(row["pebble_id"]): row for row in read_rows(metadata)}
    rows = []
    for pebble_id in range(1, npebbles + 1):
        meta = meta_rows.get(pebble_id, {})
        intact = counts.get(pebble_id, 0)
        rows.append(
            {
                "pebble_id": pebble_id,
                "intact_internal_bonds": intact,
                "initial_internal_bonds": initial_bonds_per_pebble,
                "final_broken_internal_bonds": max(0, initial_bonds_per_pebble - intact),
                "initial_x": meta.get("target_x", ""),
                "initial_y": meta.get("target_y", ""),
                "initial_z": meta.get("target_z", ""),
            }
        )
    return rows


def first_break_from_thermo(rows: list[dict[str, str]]) -> tuple[str, str]:
    for row in rows:
        broken = to_int(row.get("bond_bro"))
        if broken is not None and broken > 0:
            disp = to_float(row.get("top_disp"))
            if disp is not None:
                return f"{disp * 1000:.12g}", str(broken)
    return "", ""


def final_top_force(rows: list[dict[str, str]]) -> str:
    for row in reversed(rows):
        value = row.get("top_forc")
        if value not in (None, ""):
            return value
    return ""


def height_bin(z: float, zmin: float, zmax: float, nbins: int) -> int:
    if zmax <= zmin:
        return 1
    raw = int((z - zmin) / (zmax - zmin) * nbins) + 1
    return max(1, min(nbins, raw))


def summarize_height(rows: list[dict[str, str | int]], nbins: int) -> tuple[int, int]:
    zs = [float(row["initial_z"]) for row in rows if row["initial_z"] != ""]
    if not zs:
        return 0, 0
    zmin, zmax = min(zs), max(zs)
    totals = {bin_id: 0 for bin_id in range(1, nbins + 1)}
    for row in rows:
        if row["initial_z"] == "":
            continue
        bin_id = height_bin(float(row["initial_z"]), zmin, zmax, nbins)
        totals[bin_id] += int(row["final_broken_internal_bonds"])
    return totals[nbins], totals.get(nbins - 1, 0)


def write_csv(path: Path, rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True)
    parser.add_argument("--thermo", type=Path, required=True)
    parser.add_argument("--bond-dump", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--packing-summary", type=Path, default=ROOT / "tables/pb006_1000_proxy_packing_summary.csv")
    parser.add_argument("--baseline-summary", type=Path, default=ROOT / "tables/pb006_1000_targeted_window_summary.csv")
    parser.add_argument("--npebbles", type=int, default=1000)
    parser.add_argument("--nspheres", type=int, default=500)
    parser.add_argument("--initial-bonds-per-pebble", type=int, default=5876)
    parser.add_argument("--height-bins", type=int, default=8)
    parser.add_argument("--final-loss-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    args = parser.parse_args()

    thermo_rows = read_rows(args.thermo)
    loss_rows = final_loss_rows(
        args.bond_dump,
        args.metadata,
        args.npebbles,
        args.nspheres,
        args.initial_bonds_per_pebble,
    )
    write_csv(args.final_loss_output, loss_rows)

    damaged = [row for row in loss_rows if int(row["final_broken_internal_bonds"]) > 0]
    first_disp, first_increment = first_break_from_thermo(thermo_rows)
    top_bin, second_bin = summarize_height(loss_rows, args.height_bins)
    packing = read_rows(args.packing_summary)
    packing_row = packing[0] if packing else {}
    baseline = read_rows(args.baseline_summary)
    baseline_row = baseline[0] if baseline else {}
    baseline_broken = to_int(baseline_row.get("localized_broken_bonds")) or 0
    total_broken = sum(int(row["final_broken_internal_bonds"]) for row in loss_rows)

    summary = [
        {
            "case": args.case,
            "npebbles": args.npebbles,
            "endpoint_displacement_mm": "",
            "first_break_displacement_mm": first_disp,
            "first_thermo_break_increment": first_increment,
            "final_broken_internal_bonds": total_broken,
            "additional_broken_bonds_vs_0p10mm": total_broken - baseline_broken,
            "broken_pebbles": len(damaged),
            "first_damaged_pebble_id": damaged[0]["pebble_id"] if damaged else "",
            "most_damaged_pebble_id": max(damaged, key=lambda row: int(row["final_broken_internal_bonds"]))["pebble_id"] if damaged else "",
            "most_damaged_pebble_broken_bonds": max((int(row["final_broken_internal_bonds"]) for row in damaged), default=0),
            "final_top_force_N": final_top_force(thermo_rows),
            "top_bin_broken_bonds": top_bin,
            "second_bin_broken_bonds": second_bin,
            "bed_height_mm": packing_row.get("bed_height_mm", packing_row.get("settled_bed_height_mm", "")),
            "top_bin_count": packing_row.get("top_bin_count", ""),
            "global_mean_degree": packing_row.get("global_mean_degree", ""),
        }
    ]
    write_csv(args.summary_output, summary)
    print(args.final_loss_output)
    print(args.summary_output)
    print(f"damaged_pebbles={len(damaged)}")
    print(f"final_broken_internal_bonds={total_broken}")


if __name__ == "__main__":
    main()
