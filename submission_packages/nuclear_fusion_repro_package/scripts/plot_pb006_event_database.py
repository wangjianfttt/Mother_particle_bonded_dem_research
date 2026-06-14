#!/usr/bin/env python3
"""Plot the combined breakage-event database."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", type=Path, default=ROOT / "tables/pb006_breakage_event_database.csv")
    parser.add_argument("--summary", type=Path, default=ROOT / "tables/pb006_breakage_event_database_summary.csv")
    parser.add_argument("--out-prefix", type=Path, default=ROOT / "figures/pb006/pb006_breakage_event_database")
    args = parser.parse_args()

    events = read_rows(args.events)
    summary = read_rows(args.summary)
    cases = [row["case"] for row in summary]
    colors = {
        "seed01-500": "#2F6F73",
        "seed02-500": "#C46A30",
        "seed03-500": "#6B5EA8",
        "seed01-1000-0p10": "#3D5A80",
        "seed01-1000-0p15-restartable": "#9A2F43",
        "seed01-1000-orient02-0p15": "#7A8C37",
        "seed02-1000-0p15-restartable": "#4F7CAC",
    }
    display_names = {
        "seed01-500": "500-bed A",
        "seed02-500": "500-bed B",
        "seed03-500": "500-bed C",
        "seed01-1000-0p10": "1000 onset",
        "seed01-1000-0p15-restartable": "1000-bed A",
        "seed01-1000-orient02-0p15": "orientation replicate",
        "seed02-1000-0p15-restartable": "1000-bed B",
    }

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
    fig, axes = plt.subplots(2, 2, figsize=(7.1, 5.0), constrained_layout=True)

    ax = axes[0, 0]
    for case in cases:
        case_events = sorted([row for row in events if row["case"] == case], key=lambda r: f(r, "top_displacement_mm"))
        xs = [f(row, "top_displacement_mm") for row in case_events]
        cumulative = []
        total = 0
        for row in case_events:
            total += int(float(row["new_broken_bonds"]))
            cumulative.append(total)
        ax.step(xs, cumulative, where="post", color=colors.get(case, "#333333"), linewidth=1.5, label=display_names.get(case, case))
        ax.scatter(xs, cumulative, s=12, color=colors.get(case, "#333333"))
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Cumulative broken bonds")
    ax.set_title("a  Event accumulation", loc="left", fontweight="bold")
    ax.legend(frameon=False, fontsize=6)

    ax = axes[0, 1]
    x = range(len(summary))
    ax.bar(x, [f(row, "first_break_displacement_mm") for row in summary], color=[colors.get(row["case"], "#333333") for row in summary])
    ax.set_xticks(list(x), [display_names.get(case, case) for case in cases], rotation=20, ha="right")
    ax.set_ylabel("First break displacement (mm)")
    ax.set_title("b  First-break reproducibility", loc="left", fontweight="bold")

    ax = axes[1, 0]
    ax.bar(x, [f(row, "damaged_pebbles") for row in summary], color=[colors.get(row["case"], "#333333") for row in summary])
    ax.set_xticks(list(x), [display_names.get(case, case) for case in cases], rotation=20, ha="right")
    ax.set_ylabel("Damaged mother pebbles")
    ax.set_title("c  Event spread", loc="left", fontweight="bold")

    ax = axes[1, 1]
    for case in cases:
        case_events = [row for row in events if row["case"] == case]
        ax.scatter(
            [f(row, "top_displacement_mm") for row in case_events],
            [f(row, "relative_pebble_rank_from_top_id") for row in case_events],
            s=[12 + 1.2 * f(row, "new_broken_bonds") for row in case_events],
            color=colors.get(case, "#333333"),
            alpha=0.78,
            label=display_names.get(case, case),
        )
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Mother-pebble rank from top id")
    ax.set_title("d  Damaged-pebble sequence", loc="left", fontweight="bold")
    max_rank = max(f(row, "relative_pebble_rank_from_top_id") for row in events)
    ax.set_ylim(0.5, max(80, max_rank * 1.08))

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=3)

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in [".svg", ".pdf", ".png", ".tiff"]:
        dpi = 600 if suffix in [".png", ".tiff"] else None
        fig.savefig(args.out_prefix.with_suffix(suffix), dpi=dpi)


if __name__ == "__main__":
    main()
