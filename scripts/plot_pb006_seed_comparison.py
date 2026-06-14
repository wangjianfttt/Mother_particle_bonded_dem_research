#!/usr/bin/env python3
"""Plot three-seed PB-006 packing descriptors against breakage response."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def to_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary",
        type=Path,
        default=ROOT / "tables/pb006_seed01_seed02_seed03_summary.csv",
    )
    parser.add_argument(
        "--descriptors",
        type=Path,
        default=ROOT / "tables/pb006_three_seed_packing_descriptors_cutoff1p02mm.csv",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=ROOT / "figures/pb006/pb006_three_seed_packing_breakage",
    )
    args = parser.parse_args()

    summary = {row["seed"]: row for row in read_rows(args.summary)}
    descriptors = {row["seed"]: row for row in read_rows(args.descriptors)}
    seeds = ["seed01", "seed02", "seed03"]
    colors = {"seed01": "#2F6F73", "seed02": "#C46A30", "seed03": "#6B5EA8"}

    broken = [to_float(summary[s], "localized_broken_bonds") for s in seeds]
    force = [to_float(summary[s], "final_top_force_N") for s in seeds]
    bed_height = [to_float(descriptors[s], "bed_height_mm") for s in seeds]
    top_count = [to_float(descriptors[s], "top_bin_count") for s in seeds]
    top_degree = [to_float(descriptors[s], "top_bin_mean_degree") for s in seeds]
    first_disp = [to_float(summary[s], "first_break_displacement_mm") for s in seeds]

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

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.2), constrained_layout=True)
    ax = axes[0, 0]
    x = range(len(seeds))
    ax.bar(x, broken, color=[colors[s] for s in seeds], width=0.62)
    ax.set_xticks(list(x), seeds)
    ax.set_ylabel("Localized broken bonds")
    ax.set_ylim(0, max(broken) * 1.18)
    ax.set_title("a  Final internal bond loss", loc="left", fontweight="bold")
    for i, val in enumerate(broken):
        ax.text(i, val + 12, f"{int(val)}", ha="center", va="bottom", fontsize=8)

    ax = axes[0, 1]
    ax.bar(x, force, color=[colors[s] for s in seeds], width=0.62)
    ax.set_xticks(list(x), seeds)
    ax.set_ylabel("Final top force (N)")
    ax.set_ylim(0, max(force) * 1.18)
    ax.set_title("b  Bed-scale force response", loc="left", fontweight="bold")
    for i, val in enumerate(force):
        ax.text(i, val + 1.0, f"{val:.1f}", ha="center", va="bottom", fontsize=8)

    ax = axes[1, 0]
    width = 0.38
    ax.bar([i - width / 2 for i in x], bed_height, width=width, color="#5B8E7D", label="Bed height")
    ax.set_ylabel("Bed height (mm)")
    ax.set_xticks(list(x), seeds)
    ax.set_ylim(3.65, 4.18)
    ax2 = ax.twinx()
    ax2.bar([i + width / 2 for i in x], top_count, width=width, color="#D08C60", label="Top-bin count")
    ax2.set_ylabel("Top-bin pebble count")
    ax.set_title("c  Settled packing geometry", loc="left", fontweight="bold")
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, frameon=False, loc="upper left")

    ax = axes[1, 1]
    for seed, xd, yd, size in zip(seeds, top_degree, broken, top_count):
        ax.scatter(xd, yd, s=40 + 2.2 * size, color=colors[seed], edgecolor="black", linewidth=0.5)
        ax.text(xd + 0.015, yd + 8, seed, fontsize=8)
    ax.set_xlabel("Top-bin mean geometric degree")
    ax.set_ylabel("Localized broken bonds")
    ax.set_title("d  Upper contact network vs damage", loc="left", fontweight="bold")
    ax.set_xlim(min(top_degree) - 0.04, max(top_degree) + 0.08)
    ax.set_ylim(min(broken) - 25, max(broken) + 45)
    ax.grid(True, color="#D7D3CB", linewidth=0.6, alpha=0.7)

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=3)

    for ax in [axes[0, 0], axes[0, 1]]:
        ax.text(
            0.98,
            0.94,
            "first break: 0.0725 mm",
            ha="right",
            va="top",
            transform=ax.transAxes,
            fontsize=7,
            color="#4E4A45",
        )

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in [".svg", ".pdf", ".png", ".tiff"]:
        dpi = 600 if suffix in [".png", ".tiff"] else None
        fig.savefig(args.out_prefix.with_suffix(suffix), dpi=dpi)


if __name__ == "__main__":
    main()
