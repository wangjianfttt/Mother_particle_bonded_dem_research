#!/usr/bin/env python3
"""Combine PB-006 breakage-event CSVs into one analysis table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


DEFAULT_CASES = [
    (
        "seed01-500",
        500,
        0.20,
        ROOT / "data/processed/PB-006-bonded-randompack-500-prod-0p20mm-primitivewall_breakage_events.csv",
    ),
    (
        "seed02-500",
        500,
        0.20,
        ROOT / "data/processed/PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall_breakage_events.csv",
    ),
    (
        "seed03-500",
        500,
        0.20,
        ROOT / "data/processed/PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall_breakage_events.csv",
    ),
    (
        "seed01-1000-0p10",
        1000,
        0.10,
        ROOT / "data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window_breakage_events.csv",
    ),
    (
        "seed01-1000-0p15-restartable",
        1000,
        0.15,
        ROOT
        / "data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable_breakage_events.csv",
    ),
    (
        "seed01-1000-orient02-0p15",
        1000,
        0.15,
        ROOT
        / "data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_breakage_events.csv",
    ),
    (
        "seed02-1000-0p15-restartable",
        1000,
        0.15,
        ROOT
        / "data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_breakage_events.csv",
    ),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def parse_extra_case(case_spec: str) -> tuple[str, int, float, Path]:
    parts = case_spec.split(",", 3)
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            "--case must be formatted as label,npebbles,endpoint_mm,path"
        )
    label, npebbles, endpoint_mm, path = parts
    try:
        return label, int(npebbles), float(endpoint_mm), Path(path)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "--case requires integer npebbles and numeric endpoint_mm"
        ) from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "tables/pb006_breakage_event_database.csv",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=ROOT / "tables/pb006_breakage_event_database_summary.csv",
    )
    parser.add_argument(
        "--case",
        action="append",
        type=parse_extra_case,
        default=[],
        help="Additional event CSV as label,npebbles,endpoint_mm,path.",
    )
    args = parser.parse_args()

    rows = []
    cases = [*DEFAULT_CASES, *args.case]
    for case, npebbles, endpoint_mm, path in cases:
        for event in read_rows(path):
            pebble_id = int(float(event["pebble_id"]))
            rows.append(
                {
                    "case": case,
                    "npebbles": npebbles,
                    "endpoint_displacement_mm": endpoint_mm,
                    "event_index": int(float(event["event_index"])),
                    "timestep": int(float(event["timestep"])),
                    "pebble_id": pebble_id,
                    "relative_pebble_rank_from_top_id": npebbles - pebble_id + 1,
                    "new_broken_bonds": int(float(event["new_broken_bonds"])),
                    "cumulative_broken_bonds_in_pebble": int(float(event["cumulative_broken_bonds"])),
                    "top_displacement_mm": float(event["top_displacement_mm"]),
                    "top_force_z_N": event.get("top_force_z_N", ""),
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise SystemExit("No PB-006 breakage-event rows were found.")

    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summaries = []
    for case, npebbles, endpoint_mm, _ in cases:
        case_rows = [row for row in rows if row["case"] == case]
        if not case_rows:
            continue
        damaged = {row["pebble_id"] for row in case_rows}
        first = min(case_rows, key=lambda row: (row["top_displacement_mm"], row["event_index"]))
        summaries.append(
            {
                "case": case,
                "npebbles": npebbles,
                "endpoint_displacement_mm": endpoint_mm,
                "event_count": len(case_rows),
                "broken_bonds": sum(row["new_broken_bonds"] for row in case_rows),
                "damaged_pebbles": len(damaged),
                "first_break_displacement_mm": first["top_displacement_mm"],
                "first_break_pebble_id": first["pebble_id"],
                "first_break_rank_from_top_id": first["relative_pebble_rank_from_top_id"],
                "max_event_size": max(row["new_broken_bonds"] for row in case_rows),
            }
        )

    with args.summary_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        writer.writerows(summaries)

    print(args.output)
    print(args.summary_output)


if __name__ == "__main__":
    main()
