#!/usr/bin/env python3
"""Build a PB-007 step-relaxed validation figure from extracted thermo data."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--thermo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--baseline-step", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.thermo)
    df.columns = [c.strip() for c in df.columns]
    for col in ["Step", "KinEng", "top_disp", "top_forc", "bottom_f", "side_for", "all_wall", "bond_bro", "bond_int"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[df["bond_int"] > 0].copy()
    df = df.drop_duplicates(subset="Step", keep="first").sort_values("Step")
    if args.baseline_step is not None:
        baseline_candidates = df[df["Step"] == args.baseline_step]
    else:
        baseline_candidates = df[(df["top_disp"] <= 0.0) & (df["top_forc"].abs() <= 1.0e-12)]
        if baseline_candidates.empty:
            baseline_candidates = df[df["top_disp"] <= 0.0]
    if baseline_candidates.empty:
        raise RuntimeError("No pre-compression baseline row found")
    baseline = baseline_candidates.iloc[-1]
    df = df[df["Step"] >= baseline["Step"]].copy()
    df["disp_um"] = df["top_disp"] * 1.0e6
    df["top_force_mN"] = df["top_forc"].abs() * 1.0e3
    df["incremental_wall_force_mN"] = (df["all_wall"] - baseline["all_wall"]).abs() * 1.0e3
    df["balance_residual_percent"] = (
        (df["incremental_wall_force_mN"] - df["top_force_mN"]).abs()
        / df["top_force_mN"].replace(0.0, np.nan)
        * 100.0
    )
    df["broken_bonds"] = df["bond_bro"]

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    df[[
        "Step",
        "disp_um",
        "KinEng",
        "top_force_mN",
        "incremental_wall_force_mN",
        "balance_residual_percent",
        "broken_bonds",
        "bond_int",
    ]].to_csv(args.csv, index=False)

    plt.rcParams.update({
        "font.family": "Arial",
        "font.size": 8,
        "axes.linewidth": 0.8,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "legend.frameon": False,
    })
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.8), constrained_layout=True)
    ax = axes[0, 0]
    ax.plot(df["disp_um"], df["top_force_mN"], color="#1f77b4", lw=1.6, label="top wall")
    ax.plot(df["disp_um"], df["incremental_wall_force_mN"], color="#d62728", lw=1.2, ls="--", label="six-wall increment")
    ax.set_xlabel(r"Top-wall displacement ($\mu$m)")
    ax.set_ylabel("Force (mN)")
    ax.legend(loc="best")

    ax = axes[0, 1]
    mask = (df["top_force_mN"] > 0.0) & np.isfinite(df["balance_residual_percent"]) & (df["balance_residual_percent"] > 0.0)
    ax.plot(df.loc[mask, "disp_um"], df.loc[mask, "balance_residual_percent"], color="#2ca02c", lw=1.4)
    ax.axhline(5.0, color="0.55", lw=0.8, ls=":")
    ax.axhline(10.0, color="0.75", lw=0.8, ls=":")
    final_row = df.iloc[-1]
    final_residual = float(final_row["balance_residual_percent"])
    final_disp = float(final_row["disp_um"])
    ax.scatter([final_disp], [final_residual], color="#111111", s=16, zorder=3)
    ax.annotate(
        f"final {final_residual:.1f}%",
        xy=(final_disp, final_residual),
        xytext=(-42, 14),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "lw": 0.6, "color": "0.25"},
        fontsize=7,
    )
    ax.set_yscale("log")
    ax.set_xlabel(r"Top-wall displacement ($\mu$m)")
    ax.set_ylabel("Incremental balance residual (%)")

    ax = axes[1, 0]
    ax.semilogy(df["disp_um"], df["KinEng"], color="#9467bd", lw=1.4)
    ax.set_xlabel(r"Top-wall displacement ($\mu$m)")
    ax.set_ylabel("Kinetic energy (J)")

    ax = axes[1, 1]
    ax.plot(df["disp_um"], df["broken_bonds"], color="#111111", lw=1.4)
    ax.set_xlabel(r"Top-wall displacement ($\mu$m)")
    ax.set_ylabel("Broken internal bonds")
    broken_max = float(df["broken_bonds"].max())
    if broken_max <= 0.0:
        ax.set_ylim(-0.05, 1.0)
        ax.set_yticks([0, 1])
    else:
        ax.set_ylim(bottom=0.0)

    for label, ax in zip("abcd", axes.flat):
        ax.text(0.02, 0.96, label, transform=ax.transAxes, va="top", ha="left", fontweight="bold")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=300)
    fig.savefig(args.output.with_suffix(".pdf"))
    print(args.output)


if __name__ == "__main__":
    main()
