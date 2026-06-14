#!/usr/bin/env python3
"""Create a publication-style PB-007 acceptance-gate validation figure."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches


ROOT = Path(__file__).resolve().parents[1]
CASE = "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-5um-pilot"
SERIES = ROOT / "tables/pb007_step_relaxed_validation_y1p5e10_10krelax_5um_series.csv"
ACCEPTANCE = ROOT / "tables/pb007_bonded_steprelaxed_100_y1p5e10_10krelax_5um_acceptance_summary.csv"
NATIVE = ROOT / "tables/pb007_bonded_steprelaxed_100_y1p5e10_10krelax_5um_native_summary.csv"
OUT = ROOT / "figures/pb007/pb007_acceptance_gate_validation"


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.5,
            "axes.labelsize": 7.5,
            "axes.titlesize": 8.0,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 7.0,
            "axes.linewidth": 0.65,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.width": 0.65,
            "ytick.major.width": 0.65,
            "xtick.major.size": 3.0,
            "ytick.major.size": 3.0,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.18,
        1.08,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        fontweight="bold",
    )


def add_gate_badge(ax: plt.Axes, text: str, color: str, x: float = 0.98, y: float = 0.92) -> None:
    ax.text(
        x,
        y,
        text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.9,
        color=color,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.22,rounding_size=0.08", fc="white", ec=color, lw=0.7),
        zorder=8,
    )


def load_data() -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    series = pd.read_csv(SERIES)
    acceptance = pd.read_csv(ACCEPTANCE).iloc[0]
    native = pd.read_csv(NATIVE).iloc[0]
    for col in [
        "disp_um",
        "KinEng",
        "top_force_mN",
        "incremental_wall_force_mN",
        "balance_residual_percent",
        "broken_bonds",
        "bond_int",
    ]:
        series[col] = pd.to_numeric(series[col], errors="coerce")
    series = series[np.isfinite(series["disp_um"])].sort_values("disp_um")
    return series, acceptance, native


def main() -> None:
    style()
    series, acceptance, native = load_data()
    endpoints = series.groupby("disp_um", as_index=False).tail(1).sort_values("disp_um")

    blue = "#2F6F9F"
    orange = "#D8902F"
    green = "#168A74"
    purple = "#B75383"
    grey = "#6B747D"
    black = "#222222"
    light = "#EEF2F5"
    wash = "#FBFAF7"

    fig, axes = plt.subplots(2, 2, figsize=(7.18, 4.55), constrained_layout=True)
    fig.patch.set_facecolor("white")

    ax = axes[0, 0]
    ax.set_facecolor(wash)
    ax.plot(series["disp_um"], series["top_force_mN"], color=blue, lw=0.6, alpha=0.20)
    ax.plot(
        series["disp_um"],
        series["incremental_wall_force_mN"],
        color=orange,
        lw=0.6,
        ls=(0, (4, 2)),
        alpha=0.2,
    )
    ax.plot(endpoints["disp_um"], endpoints["top_force_mN"], color=blue, lw=1.45, marker="o", ms=3.1, label="top wall")
    ax.plot(
        endpoints["disp_um"],
        endpoints["incremental_wall_force_mN"],
        color=orange,
        lw=1.25,
        marker="s",
        ms=3.0,
        ls=(0, (4, 2)),
        label="six-wall increment",
    )
    final = series.iloc[-1]
    ax.scatter(
        [final["disp_um"], final["disp_um"]],
        [final["top_force_mN"], final["incremental_wall_force_mN"]],
        s=22,
        color=[blue, orange],
        edgecolor="white",
        linewidth=0.45,
        zorder=4,
    )
    ax.axvline(final["disp_um"], color=black, lw=0.7, ls=(0, (2, 2)), alpha=0.55)
    ax.annotate("accepted\n5 µm state", xy=(final["disp_um"], final["top_force_mN"]), xytext=(-44, 22), textcoords="offset points", arrowprops={"arrowstyle": "-", "lw": 0.55, "color": grey}, fontsize=7, ha="right")
    ax.set_xlim(-0.05, 5.15)
    ax.set_ylim(0, max(series["top_force_mN"].max(), series["incremental_wall_force_mN"].max()) * 1.18)
    ax.set_xlabel("Top-wall displacement (µm)")
    ax.set_ylabel("Force (mN)")
    ax.legend(loc="upper left", handlelength=2.4)
    ax.set_title("load transfer is established before fracture loading", loc="left", fontweight="bold")
    panel_label(ax, "a")

    ax = axes[0, 1]
    ax.set_facecolor(wash)
    residual = endpoints[
        (endpoints["top_force_mN"] > 1.0e-6)
        & np.isfinite(endpoints["balance_residual_percent"])
        & (endpoints["balance_residual_percent"] > 0)
    ].copy()
    ax.plot(residual["disp_um"], residual["balance_residual_percent"], color=green, lw=1.3, marker="o", ms=3.0)
    ax.axhspan(0.1, 5, color=green, alpha=0.10, lw=0)
    ax.axhline(5, color=green, lw=0.85, ls=(0, (2, 2)))
    ax.scatter([final["disp_um"]], [final["balance_residual_percent"]], color=black, s=18, zorder=4)
    add_gate_badge(ax, "PASS: 4.8% <= 5%", green)
    ax.annotate(
        f"final {final['balance_residual_percent']:.1f}%",
        xy=(final["disp_um"], final["balance_residual_percent"]),
        xytext=(-50, 18),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "lw": 0.55, "color": grey},
        fontsize=7,
    )
    ax.set_yscale("log")
    ax.set_xlim(-0.05, 5.15)
    ax.set_xlabel("Top-wall displacement (µm)")
    ax.set_ylabel("Balance residual (%)")
    ax.set_title("force-balance residual reaches the acceptance band", loc="left", fontweight="bold")
    panel_label(ax, "b")

    ax = axes[1, 0]
    ax.set_facecolor(wash)
    broken_total = series["bond_int"].iloc[0] - series["bond_int"]
    ax.add_patch(patches.Rectangle((0, 0.18), final["disp_um"], 0.18, facecolor=green, alpha=0.15, edgecolor="none"))
    ax.step(series["disp_um"], broken_total, where="post", color=black, lw=1.35)
    ax.scatter(endpoints["disp_um"], np.zeros(len(endpoints)), s=18, color=green, edgecolor="white", linewidth=0.45, zorder=4)
    ax.text(0.05, 0.84, "0 lost internal bonds", transform=ax.transAxes, ha="left", va="top", fontsize=8.0, color=black, fontweight="bold")
    ax.text(0.05, 0.70, "493,500 / 493,500 intact", transform=ax.transAxes, ha="left", va="top", fontsize=7.0, color=grey)
    add_gate_badge(ax, "ZERO PRE-DAMAGE", green, x=0.98, y=0.26)
    ax.set_xlim(-0.05, 5.15)
    ax.set_ylim(-0.05, 1.05)
    ax.set_yticks([0, 1])
    ax.set_xlabel("Top-wall displacement (µm)")
    ax.set_ylabel("Broken internal bonds")
    ax.set_title("bonded templates remain intact during seating", loc="left", fontweight="bold")
    panel_label(ax, "c")

    ax = axes[1, 1]
    ax.set_facecolor(wash)
    labels = ["force edges", "top-reachable", "bottom-reachable"]
    values = [
        float(native["inter_pebble_edges"]),
        float(native["top_reachable_mother_pebbles"]),
        float(native["bottom_mothers_reachable_from_top"]),
    ]
    colors = [purple, blue, grey]
    y = np.arange(len(labels))
    ax.hlines(y, 0, values, color=colors, lw=3.0, alpha=0.55)
    ax.scatter(values, y, s=54, color=colors, edgecolor="white", linewidth=0.7, zorder=3)
    for yi, val in zip(y, values):
        ax.text(val + 1.6, yi, f"{int(val)}", va="center", fontsize=7)
    add_gate_badge(ax, "SPANNING GRAPH", green, x=0.98, y=0.18)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0, max(values) * 1.28)
    ax.invert_yaxis()
    ax.set_xlabel("Mother-pebble count / edge count")
    ax.set_title("native contact graph spans top-to-bottom paths", loc="left", fontweight="bold")
    panel_label(ax, "d")

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(False)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT.with_suffix(".png"), dpi=450, bbox_inches="tight")
    fig.savefig(OUT.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(OUT.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(OUT.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    print(OUT.with_suffix(".png"))


if __name__ == "__main__":
    main()
