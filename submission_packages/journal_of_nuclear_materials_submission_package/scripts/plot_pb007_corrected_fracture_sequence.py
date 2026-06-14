#!/usr/bin/env python3
"""Plot the corrected PB-007 fracture sequence and force-network evolution."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import gridspec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def load_case(case_id: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    root = Path.cwd()
    thermo = pd.read_csv(root / f"data/processed/{case_id}_thermo.csv")
    events = pd.read_csv(root / f"data/processed/{case_id}_breakage_events.csv")
    bond_series = pd.read_csv(root / f"data/processed/{case_id}_bond_series.csv")
    native = pd.read_csv(root / f"data/processed/{case_id}_native_force_network_series.csv")
    for frame in (thermo, events, bond_series, native):
        frame.columns = [column.strip() for column in frame.columns]
    return thermo, events, bond_series, native


def prepare_thermo(thermo: pd.DataFrame) -> pd.DataFrame:
    for column in ["Step", "KinEng", "top_disp", "top_forc", "bottom_f", "side_for", "all_wall", "bond_bro", "bond_int"]:
        thermo[column] = pd.to_numeric(thermo[column], errors="coerce")
    valid = thermo[(thermo["bond_int"] > 0) & (thermo["Step"] >= 10001)].drop_duplicates("Step", keep="first").copy()
    valid["disp_um"] = valid["top_disp"] * 1e6
    valid["top_force_mN"] = valid["top_forc"].abs() * 1e3
    valid["broken_total"] = valid["bond_int"].iloc[0] - valid["bond_int"]
    return valid


def main() -> None:
    args = parse_args()
    thermo, events, bond_series, native = load_case(args.case_id)
    thermo = prepare_thermo(thermo)
    thermo_summary = (
        thermo.sort_values("Step")
        .groupby("disp_um", as_index=False)
        .agg(
            top_force_mN=("top_force_mN", "max"),
            broken_total=("broken_total", "max"),
            KinEng=("KinEng", "median"),
        )
    )
    bond_series["top_displacement_um"] = pd.to_numeric(bond_series["top_displacement_mm"], errors="coerce") * 1000.0
    native["disp_um"] = (pd.to_numeric(native["timestep"], errors="coerce") - 10000.0) / 2000.0
    events["disp_um"] = pd.to_numeric(events["top_displacement_mm"], errors="coerce") * 1000.0

    damaged = (
        bond_series.groupby(["top_displacement_um", "pebble_id", "rank_from_top"], as_index=False)["broken_internal_bonds"]
        .max()
        .sort_values(["top_displacement_um", "broken_internal_bonds"], ascending=[True, False])
    )
    damaged = damaged[damaged["broken_internal_bonds"] > 0].copy()

    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.5,
            "axes.labelsize": 7.5,
            "axes.titlesize": 8.0,
            "axes.linewidth": 0.8,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    blue = "#2F6F9F"
    orange = "#D8902F"
    green = "#168A74"
    purple = "#B75383"
    black = "#222222"
    grey = "#6B747D"
    wash = "#FBFAF7"
    event_color = "#B73A4B"

    fig = plt.figure(figsize=(7.25, 4.75), constrained_layout=True)
    spec = gridspec.GridSpec(2, 3, figure=fig, height_ratios=[1.15, 1.0])
    ax = fig.add_subplot(spec[0, :])
    ax_b = fig.add_subplot(spec[1, 0], sharex=ax)
    ax_c = fig.add_subplot(spec[1, 1], sharex=ax)
    ax_d = fig.add_subplot(spec[1, 2], sharex=ax)

    for item in [ax, ax_b, ax_c, ax_d]:
        item.set_facecolor(wash)

    def panel_label(axis: plt.Axes, label: str) -> None:
        axis.text(
            -0.08,
            1.07,
            label,
            transform=axis.transAxes,
            ha="left",
            va="top",
            fontsize=9.5,
            fontweight="bold",
            color=black,
        )

    peak = thermo.loc[thermo["top_force_mN"].idxmax()]
    endpoint = thermo.iloc[-1]
    relax = 100.0 * (float(peak["top_force_mN"]) - float(endpoint["top_force_mN"])) / float(peak["top_force_mN"])

    ax.fill_between(
        thermo_summary["disp_um"],
        0,
        thermo_summary["top_force_mN"],
        color=blue,
        alpha=0.08,
        linewidth=0,
    )
    ax.plot(thermo_summary["disp_um"], thermo_summary["top_force_mN"], color=blue, lw=1.65)
    ax.scatter(
        events["disp_um"],
        events["top_force_z_N"].abs() * 1e3,
        s=42,
        color=event_color,
        edgecolor="white",
        lw=0.7,
        zorder=5,
    )
    for idx, (_, row) in enumerate(events.iterrows(), start=1):
        ax.axvline(row["disp_um"], color=event_color, lw=0.75, ls=(0, (2, 2)), alpha=0.75)
        ax.text(
            row["disp_um"],
            ax.get_ylim()[1] * 0.95 if ax.get_ylim()[1] > 1 else 305,
            f"E{idx}",
            ha="center",
            va="top",
            color=event_color,
            fontsize=7.0,
            fontweight="bold",
        )
    ax.scatter([peak["disp_um"]], [peak["top_force_mN"]], s=34, color=black, edgecolor="white", lw=0.6, zorder=6)
    ax.annotate(
        f"peak-to-endpoint\nforce relaxation {relax:.1f}%",
        xy=(float(endpoint["disp_um"]), float(endpoint["top_force_mN"])),
        xytext=(-92, 34),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "lw": 0.7, "color": grey},
        fontsize=7.2,
        ha="right",
        va="bottom",
    )
    ax.annotate(
        "peak load",
        xy=(float(peak["disp_um"]), float(peak["top_force_mN"])),
        xytext=(-22, -26),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "lw": 0.65, "color": grey},
        fontsize=7.0,
        ha="right",
        va="top",
    )
    ax.set_xlabel("Top-wall displacement (µm)")
    ax.set_ylabel("Top-wall force (mN)")
    ax.set_xlim(0, 63)
    ax.set_ylim(0, max(thermo["top_force_mN"]) * 1.12)
    ax.text(
        0.02,
        0.92,
        "localized internal damage is embedded in load-path relaxation",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color=blue,
        fontsize=7.4,
        fontweight="bold",
    )
    ax.set_title("macro-response chronology", loc="left", fontweight="bold")
    panel_label(ax, "a")

    ax = ax_b
    ax.step(
        thermo_summary["disp_um"],
        thermo_summary["broken_total"],
        where="post",
        color=black,
        lw=1.45,
        label="bed total",
    )
    ax.scatter(
        events["disp_um"],
        events["cumulative_broken_bonds"],
        s=40,
        color=event_color,
        edgecolor="white",
        lw=0.6,
        zorder=4,
        label="mother pebble 78",
    )
    for _, row in events.iterrows():
        ax.text(row["disp_um"], row["cumulative_broken_bonds"] + 0.34, f"+{int(row['new_broken_bonds'])}", ha="center", va="bottom", fontsize=6.7, color=event_color)
    ax.text(
        0.04,
        0.88,
        "all localized events\nremain in one mother pebble",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=6.9,
        color=black,
        fontweight="bold",
    )
    ax.set_xlabel("Top-wall displacement (µm)")
    ax.set_ylabel("Cumulative broken bonds")
    ax.set_ylim(-0.2, max(6, float(thermo["broken_total"].max()) + 1))
    ax.legend(loc="lower right", handlelength=1.5, fontsize=6.6)
    ax.set_title("localized bond-loss sequence", loc="left", fontweight="bold")
    panel_label(ax, "b")

    ax = ax_c
    ax.plot(native["disp_um"], native["inter_pebble_edges"], marker="o", color=green, lw=1.55)
    ax.plot(native["disp_um"], native["top_reachable_mother_pebbles"], marker="s", color=purple, lw=1.35)
    ax.plot(native["disp_um"], native["bottom_mothers_reachable_from_top"], marker="^", color=grey, lw=1.05)
    ax.scatter(native["disp_um"], native["inter_pebble_edges"], s=28, color=green, edgecolor="white", linewidth=0.5, zorder=4)
    for _, row in events.iterrows():
        before = native[native["disp_um"] <= row["disp_um"]].sort_values("disp_um").tail(1)
        after = native[native["disp_um"] >= row["disp_um"]].sort_values("disp_um").head(1)
        if not before.empty and not after.empty:
            ax.annotate(
                "",
                xy=(float(after["disp_um"].iloc[0]), float(after["inter_pebble_edges"].iloc[0])),
                xytext=(float(before["disp_um"].iloc[0]), float(before["inter_pebble_edges"].iloc[0])),
                arrowprops={"arrowstyle": "->", "lw": 0.75, "color": green, "alpha": 0.7},
            )
    ax.text(
        0.04,
        0.79,
        "spanning force graph\nbefore and after events",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=6.9,
        color=green,
        fontweight="bold",
        bbox={"facecolor": wash, "edgecolor": "none", "alpha": 0.86, "pad": 1.4},
    )
    ax.set_xlabel("Top-wall displacement (µm)")
    ax.set_ylabel("Network count")
    last_native = native.sort_values("disp_um").iloc[-1]
    ax.text(last_native["disp_um"] + 1.0, last_native["inter_pebble_edges"], "edges", va="center", fontsize=6.7, color=green)
    ax.text(last_native["disp_um"] + 1.0, last_native["top_reachable_mother_pebbles"], "top-reachable", va="center", fontsize=6.7, color=purple)
    ax.text(last_native["disp_um"] + 1.0, last_native["bottom_mothers_reachable_from_top"], "bottom", va="center", fontsize=6.7, color=grey)
    ax.set_title("native force-network topology", loc="left", fontweight="bold")
    panel_label(ax, "c")

    ax = ax_d
    if events.empty:
        ax.text(0.5, 0.5, "No damaged mother pebble", transform=ax.transAxes, ha="center", va="center")
    else:
        event_ranks = pd.to_numeric(events["rank_from_top"], errors="coerce")
        event_cumulative = pd.to_numeric(events["cumulative_broken_bonds"], errors="coerce")
        sizes = 44 + 36 * event_cumulative
        ax.axhspan(0.5, 3.0, color=event_color, alpha=0.055, linewidth=0)
        ax.scatter(
            events["disp_um"],
            event_ranks,
            s=sizes,
            color=event_color,
            edgecolor="white",
            lw=0.75,
            zorder=4,
        )
        for _, row in events.iterrows():
            ax.text(
                row["disp_um"],
                row["rank_from_top"] + 0.36,
                str(int(row["cumulative_broken_bonds"])),
                ha="center",
                va="top",
                fontsize=6.2,
                color=event_color,
            )
        ax.annotate(
            "mother pebble 78",
            xy=(float(events["disp_um"].iloc[-1]), float(event_ranks.iloc[-1])),
            xytext=(-36, 23),
            textcoords="offset points",
            arrowprops={"arrowstyle": "-", "lw": 0.7, "color": black},
            fontsize=7.2,
        )
        ax.text(
            0.05,
            0.88,
            "rank 2 from\nbed top",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=6.9,
            color=black,
            fontweight="bold",
        )
    ax.invert_yaxis()
    ax.set_xlabel("Top-wall displacement (µm)")
    ax.set_ylabel("Rank from bed top")
    ax.set_ylim(8, 0.5)
    ax.set_title("damage remains in an upper-bed mother pebble", loc="left", fontweight="bold")
    panel_label(ax, "d")

    for item in [ax_b, ax_c, ax_d]:
        for _, row in events.iterrows():
            item.axvline(row["disp_um"], color=event_color, lw=0.55, ls=(0, (2, 2)), alpha=0.45)
    for item in [ax, ax_b, ax_c, ax_d]:
        item.spines["top"].set_visible(False)
        item.spines["right"].set_visible(False)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=450, bbox_inches="tight")
    fig.savefig(args.output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(args.output.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(args.output.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    print(args.output)


if __name__ == "__main__":
    main()
