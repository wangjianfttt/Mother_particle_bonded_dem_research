#!/usr/bin/env python3
"""Report the latest PB-007 long-run progress from a case directory."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NUMERIC_RE = re.compile(r"^\s*\d+\s+")


def latest_thermo_rows(log_path: Path) -> tuple[list[str], list[str]]:
    latest: list[str] = []
    latest_valid: list[str] = []
    with log_path.open(errors="ignore") as handle:
        for line in handle:
            if NUMERIC_RE.match(line):
                parts = line.split()
                if len(parts) >= 11:
                    latest = parts
                    try:
                        if float(parts[10]) > 0.0:
                            latest_valid = parts
                    except ValueError:
                        pass
    if not latest:
        raise SystemExit(f"No thermo row found in {log_path}")
    return latest, latest_valid or latest


def file_count(pattern: str, post_dir: Path) -> tuple[int, str]:
    def sort_key(path: Path) -> tuple[int, str]:
        try:
            return (int(path.stem.split("_")[-1]), path.name)
        except ValueError:
            return (-1, path.name)

    paths = sorted(post_dir.glob(pattern), key=sort_key)
    latest = paths[-1].name if paths else ""
    return len(paths), latest


def directory_size(path: Path) -> int:
    total = 0
    for child in path.rglob("*"):
        if child.is_file():
            total += child.stat().st_size
    return total


def fmt_bytes(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024.0 or unit == "GiB":
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{value:.1f} GiB"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_dir", type=Path)
    args = parser.parse_args()

    log_path = args.case_dir / "log.liggghts"
    post_dir = args.case_dir / "post"
    raw_row, row = latest_thermo_rows(log_path)
    keys = [
        "Step",
        "Atoms",
        "KinEng",
        "top_disp",
        "top_force",
        "bottom_force",
        "side_force",
        "all_wall_force",
        "bond_created",
        "bond_broken",
        "bond_intact",
    ]
    data = dict(zip(keys, row[: len(keys)]))
    raw_data = dict(zip(keys, raw_row[: len(keys)]))
    for pattern in ("bonds_event_*.local", "pairs_event_*.local", "walls_event_*.local", "particles_*.dump"):
        count, latest = file_count(pattern, post_dir)
        data[f"{pattern}_count"] = str(count)
        data[f"{pattern}_latest"] = latest
    data["post_size"] = fmt_bytes(directory_size(post_dir))

    for key in keys:
        print(f"{key}: {data[key]}")
    if raw_data["Step"] != data["Step"]:
        print(f"raw_latest_step: {raw_data['Step']} raw_bond_intact: {raw_data['bond_intact']}")
    print(f"bond_event_dumps: {data['bonds_event_*.local_count']} latest={data['bonds_event_*.local_latest']}")
    print(f"pair_event_dumps: {data['pairs_event_*.local_count']} latest={data['pairs_event_*.local_latest']}")
    print(f"wall_event_dumps: {data['walls_event_*.local_count']} latest={data['walls_event_*.local_latest']}")
    print(f"particle_dumps: {data['particles_*.dump_count']} latest={data['particles_*.dump_latest']}")
    print(f"post_size: {data['post_size']}")


if __name__ == "__main__":
    main()
