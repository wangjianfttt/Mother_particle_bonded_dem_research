#!/usr/bin/env python3
"""Plot PB-006 random-pack compression and localized breakage statistics."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def set_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 7,
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.linewidth": 0.75,
            "axes.labelsize": 7,
            "axes.titlesize": 7,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "legend.fontsize": 6.2,
            "legend.frameon": False,
            "figure.dpi": 160,
        }
    )


def save_pub(fig: mpl.figure.Figure, output_base: Path) -> None:
    output_base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_base.with_suffix(".tiff"), dpi=600, bbox_inches="tight")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, help="Case id without suffix.")
    parser.add_argument("--processed-dir", default="data/processed")
    parser.add_argument("--output", default="figures/pb006/pb006_randompack_500_breakage")
    args = parser.parse_args()

    processed = Path(args.processed_dir)
    thermo = pd.read_csv(processed / f"{args.case}_thermo.csv")
    events = pd.read_csv(processed / f"{args.case}_breakage_events.csv")
    height = pd.read_csv(processed / f"{args.case}_height_summary.csv")
    pebble = pd.read_csv(processed / f"{args.case}_pebble_summary.csv")

    thermo["top_disp_mm"] = thermo["top_disp"] * 1000.0
    thermo["cum_broken"] = thermo["bond_bro"].cumsum()
    step_events = (
        events.groupby(["timestep", "top_displacement_mm"], as_index=False)["new_broken_bonds"]
        .sum()
        .sort_values("timestep")
    )

    active_pebbles = pebble[pebble["total_new_broken_bonds"] > 0].copy()
    active_pebbles = active_pebbles.sort_values("total_new_broken_bonds", ascending=True)
    height = height.sort_values("height_bin")

    set_style()
    fig = plt.figure(figsize=(7.2, 4.8))
    gs = fig.add_gridspec(2, 2, hspace=0.55, wspace=0.42)

    neutral = "#3B4252"
    signal = "#B84A39"
    accent = "#3C7D6B"
    pale = "#D8A24A"

    ax = fig.add_subplot(gs[0, 0])
    ax.plot(thermo["top_disp_mm"], thermo["top_forc"], color=neutral, lw=1.2)
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Top force (N)")
    ax.set_title("a  Compression response")
    ax2 = ax.twinx()
    ax2.plot(thermo["top_disp_mm"], thermo["cum_broken"], color=signal, lw=1.1)
    ax2.set_ylabel("Cumulative broken bonds", color=signal)
    ax2.tick_params(axis="y", colors=signal)
    ax2.spines["top"].set_visible(False)

    ax = fig.add_subplot(gs[0, 1])
    ax.bar(
        step_events["top_displacement_mm"],
        step_events["new_broken_bonds"],
        width=0.012,
        color=signal,
        edgecolor="black",
        linewidth=0.25,
    )
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Localized new broken bonds")
    ax.set_title("b  Event bursts")
    for _, row in step_events.iterrows():
        ax.text(
            row["top_displacement_mm"],
            row["new_broken_bonds"] + 3,
            f"{int(row['new_broken_bonds'])}",
            ha="center",
            va="bottom",
            fontsize=5.8,
        )

    ax = fig.add_subplot(gs[1, 0])
    ax.barh(
        height["height_bin"],
        height["total_new_broken_bonds"],
        color=[pale if v > 0 else "#D9DEE7" for v in height["total_new_broken_bonds"]],
        edgecolor="black",
        linewidth=0.25,
    )
    ax.set_xlabel("Localized broken bonds")
    ax.set_ylabel("Height bin")
    ax.set_yticks(height["height_bin"])
    ax.set_title("c  Damage localizes near the loaded surface")

    ax = fig.add_subplot(gs[1, 1])
    colors = [accent if pid != 500 else signal for pid in active_pebbles["pebble_id"]]
    ax.barh(
        active_pebbles["pebble_id"].astype(str),
        active_pebbles["total_new_broken_bonds"],
        color=colors,
        edgecolor="black",
        linewidth=0.25,
    )
    ax.set_xlabel("Localized broken bonds")
    ax.set_ylabel("Mother pebble id")
    ax.set_title("d  Few pebbles initiate early breakage")

    fig.text(
        0.01,
        0.99,
        "PB-006 random pack, 500 mother pebbles, 250,000 bonded subparticles",
        ha="left",
        va="top",
        fontsize=8,
        weight="bold",
    )

    save_pub(fig, Path(args.output))


if __name__ == "__main__":
    main()
