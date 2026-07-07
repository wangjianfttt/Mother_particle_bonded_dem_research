#!/usr/bin/env python3
"""Build a source-backed progress figure for the PB-007 strength matrix.

This plot can serve as a progress figure while matrix cases are still running
and as the final strength-response figure once all material-matrix rows are
postprocessed. Filled markers use completed postprocessed outputs. Open
markers are shown only when a row is still a live preview.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "tables"
FIG_DIR = ROOT / "figures" / "pb007"
SRC_DIR = ROOT / "data" / "figure_source"

RESPONSE = TABLES / "pb007_material_parameter_response.csv"
PROGRESS = TABLES / "pb007_material_parameter_run_progress.csv"

OUT_STEM = FIG_DIR / "pb007_material_strength_response_progress"
SRC_OUT = SRC_DIR / "pb007_material_strength_response_progress.csv"
FINAL_STEM = FIG_DIR / "pb007_material_strength_response"
FINAL_SRC_OUT = SRC_DIR / "pb007_material_strength_response.csv"

COLORS = {
    "intact_geometry": "#D55E00",
    "early_cracking": "#0072B2",
    "synchronous_cracking": "#009E73",
    "grid": "#E7E9EC",
    "text": "#222222",
    "muted": "#7B8790",
    "running": "#FFFFFF",
}

GEOMETRY_LABELS = {
    "intact_geometry": "Intact geometry",
    "early_cracking": "Early-cracking geometry",
    "synchronous_cracking": "Synchronous-cracking geometry",
}


def style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.5,
            "axes.labelsize": 7.5,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 6.6,
            "axes.linewidth": 0.65,
            "axes.edgecolor": COLORS["text"],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "xtick.major.width": 0.65,
            "ytick.major.width": 0.65,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def panel(ax: plt.Axes, label: str, x: float = 0.02, y: float = 0.98) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.2,
        fontweight="bold",
        color=COLORS["text"],
    )


def clean(ax: plt.Axes, axis: str = "y") -> None:
    ax.grid(True, axis=axis, color=COLORS["grid"], lw=0.45, alpha=0.85)
    ax.set_axisbelow(True)


def export(fig: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=450, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def load_source() -> pd.DataFrame:
    response = pd.read_csv(RESPONSE)
    progress = pd.read_csv(PROGRESS) if PROGRESS.exists() else pd.DataFrame()

    keep = [
        "case_label",
        "geometry_class",
        "strength_multiplier",
        "case_status",
        "manuscript_role",
        "final_displacement_um",
        "broken_bonds_at_endpoint",
        "first_event_displacement_um",
        "damaged_mother_pebbles",
        "peak_top_force_N",
        "final_inter_pebble_force_sum_N",
        "final_top_reachable_mothers",
        "final_bottom_reachable_from_top",
        "final_spanning_force_graph",
    ]
    out = response[keep].copy()
    out["evidence_state"] = np.where(
        out["case_status"].eq("completed_postprocessed"),
        "completed",
        "running preview",
    )
    out["plot_broken_bonds"] = pd.to_numeric(out["broken_bonds_at_endpoint"], errors="coerce")
    out["plot_first_break_um"] = pd.to_numeric(out["first_event_displacement_um"], errors="coerce")

    if not progress.empty:
        progress_keep = progress[
            [
                "case_label",
                "latest_top_displacement_um",
                "latest_broken_bonds_estimate",
                "first_log_break_displacement_um",
                "final_restart_exists",
            ]
        ].copy()
        out = out.merge(progress_keep, how="left", on="case_label")
        running = out["case_status"].ne("completed_postprocessed")
        out.loc[running, "plot_broken_bonds"] = pd.to_numeric(
            out.loc[running, "latest_broken_bonds_estimate"], errors="coerce"
        )
        out.loc[running, "plot_first_break_um"] = pd.to_numeric(
            out.loc[running, "first_log_break_displacement_um"], errors="coerce"
        )
    else:
        out["latest_top_displacement_um"] = np.nan
        out["latest_broken_bonds_estimate"] = np.nan
        out["first_log_break_displacement_um"] = np.nan
        out["final_restart_exists"] = np.nan

    out["geometry_label"] = out["geometry_class"].map(GEOMETRY_LABELS).fillna(out["geometry_class"])
    out["plot_broken_bonds"] = pd.to_numeric(out["plot_broken_bonds"], errors="coerce").fillna(0)
    out["plot_first_break_um"] = pd.to_numeric(out["plot_first_break_um"], errors="coerce")
    out["plot_force_sum_N"] = pd.to_numeric(out["final_inter_pebble_force_sum_N"], errors="coerce")
    out["plot_top_reachable"] = pd.to_numeric(out["final_top_reachable_mothers"], errors="coerce")
    out["plot_bottom_reachable"] = pd.to_numeric(out["final_bottom_reachable_from_top"], errors="coerce")
    out["marker_size"] = 36 + 10 * np.sqrt(out["plot_broken_bonds"].clip(lower=0))

    SRC_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(SRC_OUT, index=False)
    matrix = out[
        out["case_label"].str.contains("strength0p", na=False)
        & out["geometry_class"].isin(["early_cracking", "synchronous_cracking"])
    ]
    if len(matrix) == 6 and matrix["case_status"].eq("completed_postprocessed").all():
        out.to_csv(FINAL_SRC_OUT, index=False)
    return out


def scatter_by_state(
    ax: plt.Axes,
    data: pd.DataFrame,
    x: str,
    y: str,
    size_col: str = "marker_size",
    annotate_bonds: bool = False,
) -> None:
    for geometry, group in data.groupby("geometry_class", sort=False):
        color = COLORS.get(geometry, COLORS["muted"])
        completed = group["case_status"].eq("completed_postprocessed")
        if completed.any():
            ax.scatter(
                group.loc[completed, x],
                group.loc[completed, y],
                s=group.loc[completed, size_col],
                color=color,
                edgecolor=COLORS["text"],
                linewidth=0.45,
                alpha=0.92,
                zorder=3,
            )
        running = ~completed
        if running.any():
            ax.scatter(
                group.loc[running, x],
                group.loc[running, y],
                s=group.loc[running, size_col],
                facecolor="white",
                edgecolor=color,
                linewidth=1.1,
                alpha=0.95,
                zorder=3,
            )
        if annotate_bonds:
            for _, row in group.iterrows():
                bonds = int(round(row["plot_broken_bonds"]))
                if bonds > 0:
                    ax.text(
                        row[x] + 0.012,
                        row[y],
                        f"{bonds}",
                        color=color,
                        fontsize=6.2,
                        va="center",
                    )


def build_figure() -> None:
    style()
    data = load_source()
    fig = plt.figure(figsize=(7.25, 4.45), constrained_layout=True)
    gs = fig.add_gridspec(2, 3, width_ratios=[1.12, 1.05, 1.10], height_ratios=[1.0, 1.0])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])
    ax_e = fig.add_subplot(gs[:, 2])

    panel(ax_a, "a")
    scatter_by_state(ax_a, data, "strength_multiplier", "plot_broken_bonds", annotate_bonds=False)
    clean(ax_a)
    ax_a.set_xlabel("Bond-strength multiplier")
    ax_a.set_ylabel("Broken internal bonds")
    ax_a.set_xlim(0.18, 1.07)
    ax_a.set_ylim(-0.7, max(12, data["plot_broken_bonds"].max() + 2))
    ax_a.set_xticks([0.25, 0.50, 0.75, 1.00])

    panel(ax_b, "b")
    onset = data.dropna(subset=["plot_first_break_um"]).copy()
    scatter_by_state(ax_b, onset, "strength_multiplier", "plot_first_break_um", annotate_bonds=False)
    clean(ax_b)
    ax_b.set_xlabel("Bond-strength multiplier")
    ax_b.set_ylabel("First bond loss (micrometre)")
    ax_b.set_xlim(0.18, 1.07)
    ax_b.set_xticks([0.25, 0.50, 0.75, 1.00])
    if not onset.empty:
        ax_b.set_ylim(0, max(65, onset["plot_first_break_um"].max() + 8))

    panel(ax_c, "c")
    completed = data[data["case_status"].eq("completed_postprocessed")].copy()
    scatter_by_state(ax_c, completed, "strength_multiplier", "plot_force_sum_N", annotate_bonds=False)
    clean(ax_c)
    ax_c.set_xlabel("Bond-strength multiplier")
    ax_c.set_ylabel("Final inter-particle force sum (N)")
    ax_c.set_xlim(0.18, 1.07)
    ax_c.set_xticks([0.25, 0.50, 0.75, 1.00])
    if not completed["plot_force_sum_N"].dropna().empty:
        ax_c.set_ylim(0, completed["plot_force_sum_N"].max() * 1.18)

    panel(ax_d, "d")
    reach = completed.dropna(subset=["plot_bottom_reachable", "plot_top_reachable"])
    scatter_by_state(ax_d, reach, "plot_bottom_reachable", "plot_top_reachable", annotate_bonds=False)
    clean(ax_d)
    ax_d.set_xlabel("Bottom-reaching particles")
    ax_d.set_ylabel("Top-reachable particles")
    if not reach.empty:
        ax_d.set_xlim(0, max(20, reach["plot_bottom_reachable"].max() + 3))
        ax_d.set_ylim(0, max(80, reach["plot_top_reachable"].max() + 6))

    panel(ax_e, "e")
    y_order = ["intact_geometry", "early_cracking", "synchronous_cracking"]
    y_map = {name: idx for idx, name in enumerate(y_order)}
    heat = data[data["geometry_class"].isin(y_order)].copy()
    heat["y"] = heat["geometry_class"].map(y_map)
    for _, row in heat.iterrows():
        color = COLORS.get(row["geometry_class"], COLORS["muted"])
        completed_case = row["case_status"] == "completed_postprocessed"
        ax_e.scatter(
            row["strength_multiplier"],
            row["y"],
            s=85 + 17 * np.sqrt(max(float(row["plot_broken_bonds"]), 0.0)),
            facecolor=color if completed_case else "white",
            edgecolor=COLORS["text"] if completed_case else color,
            linewidth=0.55 if completed_case else 1.15,
            alpha=0.92,
            zorder=3,
        )
        label = int(round(float(row["plot_broken_bonds"])))
        if label > 0:
            ax_e.text(
                row["strength_multiplier"],
                row["y"] - 0.21,
                str(label),
                ha="center",
                va="top",
                fontsize=6.2,
                color=color,
            )
    clean(ax_e, axis="x")
    ax_e.set_xlabel("Bond-strength multiplier")
    ax_e.set_yticks([y_map[name] for name in y_order])
    ax_e.set_yticklabels([GEOMETRY_LABELS[name] for name in y_order])
    ax_e.set_xlim(0.18, 1.07)
    ax_e.set_xticks([0.25, 0.50, 0.75, 1.00])
    ax_e.set_ylim(-0.6, len(y_order) - 0.4)
    ax_e.invert_yaxis()

    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS[key], markeredgecolor=COLORS["text"], markersize=5.2, label=label)
        for key, label in [
            ("intact_geometry", "Intact geometry"),
            ("early_cracking", "Early-cracking geometry"),
            ("synchronous_cracking", "Synchronous-cracking geometry"),
        ]
    ]
    if data["case_status"].ne("completed_postprocessed").any():
        handles.extend(
            [
                Line2D([0], [0], marker="o", color="none", markerfacecolor=COLORS["muted"], markeredgecolor=COLORS["text"], markersize=5.2, label="completed"),
                Line2D([0], [0], marker="o", color="none", markerfacecolor="white", markeredgecolor=COLORS["muted"], markeredgewidth=1.1, markersize=5.2, label="running preview"),
            ]
        )
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.52, 1.03), columnspacing=1.0, handletextpad=0.35)
    matrix = data[
        data["case_label"].str.contains("strength0p", na=False)
        & data["geometry_class"].isin(["early_cracking", "synchronous_cracking"])
    ]
    stems = [OUT_STEM]
    if len(matrix) == 6 and matrix["case_status"].eq("completed_postprocessed").all():
        stems.append(FINAL_STEM)
    for stem in stems:
        stem.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
        fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
        fig.savefig(stem.with_suffix(".png"), dpi=450, bbox_inches="tight")
        fig.savefig(stem.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    build_figure()
    print(SRC_OUT)
    if FINAL_SRC_OUT.exists():
        print(FINAL_SRC_OUT)
    for suffix in [".pdf", ".svg", ".png", ".tiff"]:
        print(OUT_STEM.with_suffix(suffix))
    if FINAL_STEM.with_suffix(".pdf").exists():
        for suffix in [".pdf", ".svg", ".png", ".tiff"]:
            print(FINAL_STEM.with_suffix(suffix))


if __name__ == "__main__":
    main()
