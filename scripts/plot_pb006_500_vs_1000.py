#!/usr/bin/env python3
"""Plot PB-006 500-peed three-seed results against the 1000-pebble short scan."""

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
    parser.add_argument(
        "--seed-summary",
        type=Path,
        default=ROOT / "tables/pb006_seed01_seed02_seed03_summary.csv",
    )
    parser.add_argument(
        "--summary1000",
        type=Path,
        default=ROOT / "tables/pb006_1000_targeted_window_summary.csv",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=ROOT / "figures/pb006/pb006_500_vs_1000_short_comparison",
    )
    args = parser.parse_args()

    rows = []
    for row in read_rows(args.seed_summary):
        rows.append(
            {
                "label": row["seed"],
                "npebbles": 500,
                "first_break_displacement_mm": f(row, "first_break_displacement_mm"),
                "broken_bonds": f(row, "localized_broken_bonds"),
                "broken_pebbles": f(row, "broken_pebbles"),
                "final_top_force_N": f(row, "final_top_force_N"),
                "top_bin_broken_bonds": f(row, "top_bin_broken_bonds"),
                "second_bin_broken_bonds": f(row, "second_bin_broken_bonds"),
                "final_displacement_mm": 0.20,
            }
        )
    row1000 = read_rows(args.summary1000)[0]
    rows.append(
        {
            "label": "1000 target",
            "npebbles": 1000,
            "first_break_displacement_mm": f(row1000, "first_break_displacement_mm"),
            "broken_bonds": f(row1000, "localized_broken_bonds"),
            "broken_pebbles": f(row1000, "broken_pebbles"),
            "final_top_force_N": f(row1000, "final_top_force_N"),
            "top_bin_broken_bonds": f(row1000, "top_bin_broken_bonds"),
            "second_bin_broken_bonds": f(row1000, "second_bin_broken_bonds"),
            "final_displacement_mm": 0.10,
        }
    )

    colors = ["#2F6F73", "#C46A30", "#6B5EA8", "#3D5A80"]
    x = list(range(len(rows)))
    labels = [row["label"] for row in rows]

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
    vals = [row["first_break_displacement_mm"] for row in rows]
    ax.bar(x, vals, color=colors, width=0.62)
    ax.set_xticks(x, labels, rotation=15, ha="right")
    ax.set_ylabel("First break displacement (mm)")
    ax.set_title("a  Onset displacement", loc="left", fontweight="bold")
    ax.set_ylim(0, max(vals) * 1.22)
    for i, val in enumerate(vals):
        ax.text(i, val + 0.002, f"{val:.4f}", ha="center", va="bottom", fontsize=7)

    ax = axes[0, 1]
    vals = [row["broken_bonds"] for row in rows]
    ax.bar(x, vals, color=colors, width=0.62)
    ax.set_xticks(x, labels, rotation=15, ha="right")
    ax.set_ylabel("Broken internal bonds")
    ax.set_title("b  Final bond loss", loc="left", fontweight="bold")
    ax.set_ylim(0, max(vals) * 1.18)
    for i, val in enumerate(vals):
        ax.text(i, val + 10, f"{int(val)}", ha="center", va="bottom", fontsize=7)

    ax = axes[1, 0]
    top_vals = [row["top_bin_broken_bonds"] for row in rows]
    second_vals = [row["second_bin_broken_bonds"] for row in rows]
    ax.bar(x, top_vals, color="#5B8E7D", width=0.62, label="Top bin")
    ax.bar(x, second_vals, bottom=top_vals, color="#D08C60", width=0.62, label="Second bin")
    ax.set_xticks(x, labels, rotation=15, ha="right")
    ax.set_ylabel("Broken bonds by height bin")
    ax.set_title("c  Height localization", loc="left", fontweight="bold")
    ax.legend(frameon=False)

    ax = axes[1, 1]
    vals = [row["final_top_force_N"] for row in rows]
    ax.bar(x, vals, color=colors, width=0.62)
    ax.set_xticks(x, labels, rotation=15, ha="right")
    ax.set_ylabel("Final top force (N)")
    ax.set_title("d  Force at sampled endpoint", loc="left", fontweight="bold")
    ax.set_ylim(0, max(vals) * 1.18)
    for i, row in enumerate(rows):
        ax.text(
            i,
            vals[i] + 1.0,
            f"{vals[i]:.1f} N\n{row['final_displacement_mm']:.2f} mm",
            ha="center",
            va="bottom",
            fontsize=7,
        )

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
