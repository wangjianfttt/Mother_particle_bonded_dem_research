#!/usr/bin/env python3
"""Extract simple thermo tables from LIGGGHTS log files.

This is intentionally small and robust for the SP-001 workflow. It looks for
the thermo header beginning with Step and captures numeric rows until the run
summary starts.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path, help="LIGGGHTS log or captured stdout file.")
    parser.add_argument("--output", type=Path, required=True, help="Output CSV path.")
    return parser.parse_args()


def is_numeric_row(parts: list[str]) -> bool:
    if not parts:
        return False
    try:
        for value in parts:
            float(value)
    except ValueError:
        return False
    return True


def extract_rows(log_path: Path) -> tuple[list[str], list[list[str]]]:
    header: list[str] = []
    rows: list[list[str]] = []
    active = False

    for raw_line in log_path.read_text(errors="replace").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        if parts[0] == "Step":
            header = parts
            active = True
            continue
        if active and line.startswith("Loop time"):
            active = False
            continue
        if active and is_numeric_row(parts):
            if len(parts) == len(header):
                rows.append(parts)

    if not header:
        raise RuntimeError(f"No thermo header found in {log_path}")
    return normalize_header(header), rows


def normalize_header(header: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: dict[str, int] = {}
    bond_status_names = ["bond_created", "bond_broken", "bond_intact"]
    bond_status_index = 0

    for name in header:
        if name == "bond_sta" and bond_status_index < len(bond_status_names):
            normalized.append(bond_status_names[bond_status_index])
            bond_status_index += 1
            continue

        count = seen.get(name, 0) + 1
        seen[name] = count
        normalized.append(name if count == 1 else f"{name}_{count}")

    return normalized


def main() -> None:
    args = parse_args()
    header, rows = extract_rows(args.log)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    main()
