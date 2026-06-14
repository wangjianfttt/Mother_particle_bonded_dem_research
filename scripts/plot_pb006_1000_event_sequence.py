#!/usr/bin/env python3
"""Plot the targeted-window 1000-pebble PB-006 breakage sequence."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in ("", None) else 0.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--events",
        type=Path,
        default=ROOT
        / "data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window_breakage_events.csv",
    )
    parser.add_argument(
        "--height",
        type=Path,
        default=ROOT
        / "data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window_height_summary.csv",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=ROOT / "tables/pb006_1000_targeted_window_summary.csv",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=ROOT / "figures/pb006/pb006_1000_targeted_window_event_sequence",
    )
    args = parser.parse_args()

    events = read_rows(args.events)
    height_rows = read_rows(args.height)
    summary = read_rows(args.summary)[0]
    if not events:
        raise SystemExit("No breakage events found")

    disp = [as_float(row, "top_displacement_mm") for row in events]
    increments = [as_float(row, "new_broken_bonds") for row in events]
    cumulative = [as_float(row, "cumulative_broken_bonds") for row in events]
    pebble_ids = [int(float(row["pebble_id"])) for row in events]
    force = [as_float(row, "top_force_z_N") for row in events]

    plt.rcParams.update(
        {
            "font.family": "Arial",
            "font.size": 8,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )

    fig, axes = plt.subplots(2, 2, figsize=(7.1, 5.2), constrained_layout=True)

    ax = axes[0, 0]
    ax.step(disp, cumulative, where="post", color="#2F6F73", linewidth=1.6)
    ax.scatter(disp, cumulative, s=22, color="#2F6F73", edgecolor="white", linewidth=0.5, zorder=3)
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Cumulative broken bonds")
    ax.set_title("a  Event accumulation", loc="left", fontweight="bold")

    ax = axes[0, 1]
    ax.bar(disp, increments, width=0.0012, color="#C46A30")
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("New broken bonds")
    ax.set_title("b  Event size", loc="left", fontweight="bold")

    ax = axes[1, 0]
    colors = ["#6B5EA8" if pid == pebble_ids[0] else "#8093A5" for pid in pebble_ids]
    ax.scatter(disp, pebble_ids, s=[18 + 2.0 * v for v in increments], color=colors, alpha=0.88)
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Mother pebble id")
    ax.set_title("c  Damaged pebble sequence", loc="left", fontweight="bold")

    ax = axes[1, 1]
    bins = [int(row["height_bin"]) for row in height_rows]
    broken = [as_float(row, "total_new_broken_bonds") for row in height_rows]
    ax.barh(bins, broken, color="#5B8E7D")
    ax.set_xlabel("Broken bonds")
    ax.set_ylabel("Initial height bin")
    ax.set_title("d  Height localization", loc="left", fontweight="bold")
    ax.set_yticks(sorted(bins))

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=3)

    fig.suptitle(
        "PB-006 1000-pebble targeted window: "
        f"first break {float(summary['first_break_displacement_mm']):.4f} mm, "
        f"{int(float(summary['localized_broken_bonds']))} broken bonds",
        fontsize=9,
    )

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in [".svg", ".pdf", ".png", ".tiff"]:
        dpi = 600 if suffix in [".png", ".tiff"] else None
        fig.savefig(args.out_prefix.with_suffix(suffix), dpi=dpi)


if __name__ == "__main__":
    main()
