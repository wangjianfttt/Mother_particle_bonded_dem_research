#!/usr/bin/env python3
"""Build a mechanism-focused PB-007 comparison figure.

The figure intentionally avoids using top-wall displacement as the dominant
coordinate.  It re-expresses the corrected bed calculations as force-network,
localization and endpoint mechanism variables.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_STEM = ROOT / "figures" / "pb007" / "pb007_replicate_comparison"
SOURCE_DATA = ROOT / "data" / "processed" / "pb007_replicate_comparison_source_data.csv"
MECHANISM_INDEX_TABLE = ROOT / "tables" / "pb007_mechanism_indices.csv"
MACRO_DATA = ROOT / "tables" / "pb007_macro_topology_event_metrics.csv"
EVENT_TOPOLOGY = ROOT / "tables" / "pb007_event_aligned_topology.csv"
STRONG_FORCE_TAIL = ROOT / "tables" / "pb007_strong_force_tail_state_metrics.csv"


CASE_STYLE = {
    "pilot_localized_microcracking": {
        "label": "Pilot",
        "color": "#335C81",
        "marker": "o",
        "kind": "cracked",
    },
    "seed02_intact_to_60um": {
        "label": "Independent",
        "color": "#B85C38",
        "marker": "s",
        "kind": "intact",
    },
    "seed03_delayed_microcracking_to_60um": {
        "label": "Delayed",
        "color": "#168A74",
        "marker": "^",
        "kind": "cracked",
    },
    "seed04_early_microcracking_to_60um": {
        "label": "Early",
        "color": "#8B3A62",
        "marker": "P",
        "kind": "cracked",
    },
    "seed06_synchronous_microcracking_to_60um": {
        "label": "Synchronous",
        "color": "#D08A24",
        "marker": "X",
        "kind": "cracked",
    },
    "seed02_strength0p5_intact_to_60um": {
        "label": "0.5x intact",
        "color": "#4F7F52",
        "marker": "D",
        "kind": "strength_control",
    },
    "seed02_strength0p25_intact_to_60um": {
        "label": "0.25x intact",
        "color": "#7C6A9D",
        "marker": "v",
        "kind": "strength_control",
    },
    "seed09_200bed_intact_to_60um": {
        "label": "200-bed",
        "color": "#5E7CE2",
        "marker": "h",
        "kind": "scale",
    },
    "seed09_200bed_strength0p25_to_60um": {
        "label": "200-bed 0.25x",
        "color": "#2E6F40",
        "marker": "*",
        "kind": "scale",
    },
}


def _style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.8,
            "axes.labelsize": 7.8,
            "axes.linewidth": 0.75,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def _prepare_macro() -> pd.DataFrame:
    macro = pd.read_csv(MACRO_DATA)
    macro["display_case"] = macro["case_label"].map(lambda key: CASE_STYLE[key]["label"])
    macro["color"] = macro["case_label"].map(lambda key: CASE_STYLE[key]["color"])
    macro["marker"] = macro["case_label"].map(lambda key: CASE_STYLE[key]["marker"])
    macro["case_kind"] = macro["case_label"].map(lambda key: CASE_STYLE[key]["kind"])
    macro["broken_bond_fraction"] = macro["broken_bonds_at_endpoint"] / macro["initial_internal_bonds"].replace(0, np.nan)
    macro["damaged_fraction"] = macro["damaged_mother_pebbles"] / macro["mother_pebble_count"].replace(0, np.nan)
    macro["network_reorganization_fraction"] = (
        (macro["max_inter_mother_edges"] - macro["final_inter_mother_edges"])
        / macro["max_inter_mother_edges"].replace(0, np.nan)
    )
    macro["force_relaxation_fraction"] = (
        (macro["peak_top_force_N"] - macro["final_top_force_N"])
        / macro["peak_top_force_N"].replace(0, np.nan)
    )
    macro["load_path_reach_fraction"] = macro["final_top_reachable_mothers"] / macro["mother_pebble_count"].replace(0, np.nan)
    macro["bottom_reach_fraction"] = macro["final_bottom_reachable_from_top"] / macro["mother_pebble_count"].replace(0, np.nan)
    macro["force_path_intensity_norm"] = (
        macro["final_inter_pebble_force_sum_N"]
        / macro["final_inter_pebble_force_sum_N"].max()
    )
    macro["broken_bond_fraction_x1e5"] = macro["broken_bond_fraction"] * 1.0e5
    macro["damage_localization_index_bonds_per_damaged_mother"] = np.where(
        macro["damaged_mother_pebbles"] > 0,
        macro["broken_bonds_at_endpoint"] / macro["damaged_mother_pebbles"],
        0.0,
    )
    macro["endpoint_damage_state"] = np.where(
        macro["broken_bonds_at_endpoint"] > 0,
        "localized microcracking",
        "intact to endpoint",
    )
    macro["posthoc_mechanism_index"] = (
        macro["force_path_intensity_norm"]
        * (1.0 + macro["network_reorganization_fraction"].clip(lower=0.0))
        * (1.0 + macro["force_relaxation_fraction"].clip(lower=0.0))
    )
    if STRONG_FORCE_TAIL.exists():
        tail = pd.read_csv(STRONG_FORCE_TAIL)
        tail = tail[tail["state_kind"] == "final"].copy()
        tail = tail.rename(
            columns={
                "case_label": "display_case",
                "inter_parent_force_sum_N": "tail_inter_parent_force_sum_N",
                "F95_edge_force_N": "tail_F95_edge_force_N",
                "F99_edge_force_N": "tail_F99_edge_force_N",
                "top5_force_share": "tail_top5_force_share",
                "top1_force_share": "tail_top1_force_share",
            }
        )
        tail["display_case"] = tail["display_case"].replace(
            {
                "Intact": "Independent",
                "Intact 0.5x": "0.5x intact",
                "Intact 0.25x": "0.25x intact",
            }
        )
        keep = [
            "display_case",
            "tail_inter_parent_force_sum_N",
            "tail_F95_edge_force_N",
            "tail_F99_edge_force_N",
            "tail_top5_force_share",
            "tail_top1_force_share",
        ]
        macro = macro.merge(tail[keep], on="display_case", how="left")
    else:
        macro["tail_F95_edge_force_N"] = np.nan
        macro["tail_F99_edge_force_N"] = np.nan
        macro["tail_top5_force_share"] = np.nan
        macro["tail_top1_force_share"] = np.nan
    return macro


def _write_mechanism_index_table(macro: pd.DataFrame) -> None:
    columns = [
        "display_case",
        "endpoint_damage_state",
        "final_inter_pebble_force_sum_N",
        "force_path_intensity_norm",
        "network_reorganization_fraction",
        "force_relaxation_fraction",
        "broken_bonds_at_endpoint",
        "broken_bond_fraction_x1e5",
        "tail_F95_edge_force_N",
        "tail_F99_edge_force_N",
        "tail_top5_force_share",
        "damaged_mother_pebbles",
        "damage_localization_index_bonds_per_damaged_mother",
        "final_top_reachable_mothers",
        "final_bottom_reachable_from_top",
        "posthoc_mechanism_index",
    ]
    out = macro[columns].copy()
    out = out.sort_values(
        ["broken_bonds_at_endpoint", "posthoc_mechanism_index"],
        ascending=[False, False],
    )
    MECHANISM_INDEX_TABLE.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(MECHANISM_INDEX_TABLE, index=False)


def _source_data(macro: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    macro_source = macro.copy()
    macro_source["source_panel"] = "a_c_d_endpoint_mechanism"
    event_source = events.copy()
    event_source["source_panel"] = "b_event_aligned_topology"
    return pd.concat([macro_source, event_source], ignore_index=True, sort=False)


def _scatter_cases(ax: plt.Axes, macro: pd.DataFrame) -> None:
    for _, row in macro.iterrows():
        size = 58 + 220 * float(row["damaged_fraction"])
        edge = "#222222" if row["case_kind"] == "cracked" else "white"
        alpha = 0.98 if row["case_kind"] != "strength_control" else 0.62
        if row["case_kind"] == "scale":
            alpha = 0.88
        ax.scatter(
            row["final_inter_pebble_force_sum_N"],
            row["broken_bonds_at_endpoint"],
            s=size,
            marker=row["marker"],
            color=row["color"],
            edgecolor=edge,
            linewidth=0.65,
            alpha=alpha,
            zorder=3,
            label=row["display_case"],
        )
    intact = macro[macro["case_kind"].isin(["intact", "strength_control", "scale"])]
    if not intact.empty:
        ax.text(
            max(float(intact["final_inter_pebble_force_sum_N"].min()) + 0.03, 0.08),
            0.75,
            "intact/control\nbeds",
            fontsize=6.0,
            color="0.28",
            ha="left",
            va="bottom",
        )
    ax.set_xlabel("Endpoint inter-particle force sum (N)")
    ax.set_ylabel("Endpoint broken internal bonds")
    xmin = max(0.0, float(macro["final_inter_pebble_force_sum_N"].min()) - 0.05)
    xmax = float(macro["final_inter_pebble_force_sum_N"].max()) + 0.10
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(-0.8, 11.8)


def _plot_event_topology(ax: plt.Axes, events: pd.DataFrame) -> None:
    if events.empty:
        ax.text(0.5, 0.5, "No event-aligned topology rows", transform=ax.transAxes, ha="center", va="center")
        return

    grouped = (
        events.groupby(
            [
                "case_label",
                "event_timestep",
                "event_displacement_um",
                "force_sum_ratio_next_to_previous",
                "delta_inter_mother_edges",
            ],
            as_index=False,
        )
        .agg(
            new_broken_bonds=("new_broken_bonds", "sum"),
            damaged_pebbles=("pebble_id", "nunique"),
            cumulative_broken_bonds=("cumulative_broken_bonds", "max"),
        )
        .sort_values(["case_label", "event_timestep"])
    )

    x = grouped["force_sum_ratio_next_to_previous"].astype(float)
    y = grouped["delta_inter_mother_edges"].astype(float)
    for _, row in grouped.iterrows():
        style = next(
            item for item in CASE_STYLE.values() if item["label"] == row["case_label"]
        )
        size = 64 + 18 * float(row["new_broken_bonds"])
        ax.scatter(
            row["force_sum_ratio_next_to_previous"],
            row["delta_inter_mother_edges"],
            s=size,
            marker=style["marker"],
            color=style["color"],
            edgecolor="#222222",
            linewidth=0.55,
            zorder=4,
        )
    ax.axvline(1.0, color="0.72", lw=0.75, ls=(0, (2, 2)), zorder=0)
    ax.axhline(0.0, color="0.72", lw=0.75, ls=(0, (2, 2)), zorder=0)
    ax.set_xlabel("Next / previous inter-particle force sum")
    ax.set_ylabel("Change in force-network edges")
    ax.set_xlim(max(0.0, float(x.min()) - 0.18), max(3.0, float(x.max()) + 0.35))
    y_pad = max(4.0, 0.12 * (float(y.max()) - float(y.min()) or 1.0))
    ax.set_ylim(float(y.min()) - y_pad, float(y.max()) + y_pad)


def _plot_reachability(ax: plt.Axes, macro: pd.DataFrame) -> None:
    for _, row in macro.iterrows():
        alpha = 0.95 if row["case_kind"] != "strength_control" else 0.55
        if row["case_kind"] == "scale":
            alpha = 0.82
        ax.scatter(
            row["final_bottom_reachable_from_top"],
            row["final_top_reachable_mothers"],
            s=70 + 9 * row["broken_bonds_at_endpoint"],
            marker=row["marker"],
            color=row["color"],
            edgecolor="#222222" if row["case_kind"] in {"cracked", "scale"} else "white",
            linewidth=0.55,
            alpha=alpha,
        )
        if row["case_kind"] == "cracked":
            dx = 0.35 if row["display_case"] == "Pilot" else 0.55
            dy = 0.45 if row["display_case"] == "Pilot" else 0.25
            ax.text(
                row["final_bottom_reachable_from_top"] + dx,
                row["final_top_reachable_mothers"] + dy,
                f"{int(row['broken_bonds_at_endpoint'])} bonds",
                fontsize=6.2,
                color=row["color"],
            )
    intact = macro[macro["case_kind"].isin(["intact", "strength_control", "scale"])]
    if not intact.empty:
        ax.text(
            0.98,
            0.92,
            "intact/control beds:\n0 bonds",
            transform=ax.transAxes,
            fontsize=6.2,
            color="0.34",
            ha="right",
            va="top",
        )
    ax.set_xlabel("Bottom-contacting parent particles reachable from top")
    ax.set_ylabel("Top-reachable parent particles")
    xmin = max(0.0, float(macro["final_bottom_reachable_from_top"].min()) - 1.2)
    xmax = float(macro["final_bottom_reachable_from_top"].max()) + 1.8
    ymin = max(0.0, float(macro["final_top_reachable_mothers"].min()) - 3.0)
    ymax = float(macro["final_top_reachable_mothers"].max()) + 3.0
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)


def _plot_fingerprint(ax: plt.Axes, macro: pd.DataFrame) -> None:
    metrics = [
        ("final_inter_pebble_force_sum_N", "Force-path\nintensity", "N", "{:.2f}"),
        ("tail_F95_edge_force_N", "F95 edge\nforce", "N", "{:.3f}"),
        ("network_reorganization_fraction", "Network\nreorganization", "fraction", "{:.2f}"),
        ("force_relaxation_fraction", "Force\nrelaxation", "fraction", "{:.2f}"),
        ("broken_bond_fraction", "Broken-bond\nfraction", "x1e-5", "{:.2f}"),
    ]
    y_positions = np.arange(len(metrics))[::-1]
    ordered_names = list(macro["display_case"])
    offsets = {
        name: offset
        for name, offset in zip(
            ordered_names,
            np.linspace(0.24, -0.30, len(ordered_names)),
        )
    }
    for metric_index, (column, label, unit, fmt) in enumerate(metrics):
        values = macro.set_index("display_case")[column].astype(float)
        denom = float(values.max()) if float(values.max()) > 0 else 1.0
        base = y_positions[metric_index]
        for _, row in macro.iterrows():
            name = row["display_case"]
            raw = float(row[column])
            value = raw / denom
            y = base + offsets[name]
            ax.plot([0, value], [y, y], color=row["color"], lw=1.65, alpha=0.30)
            ax.scatter(value, y, s=24, marker=row["marker"], color=row["color"], edgecolor="white", linewidth=0.45)
            if name in {"Pilot", "Independent", "Delayed", "Early", "Synchronous", "200-bed", "200-bed 0.25x"}:
                display = raw * 1.0e5 if column == "broken_bond_fraction" else raw
                ax.text(min(value + 0.035, 1.05), y, fmt.format(display), ha="left", va="center", fontsize=5.9, color=row["color"])
        ax.text(-0.03, base, f"{label}\n({unit})", ha="right", va="center", fontsize=6.1, color="0.20")
    ax.axvline(1.0, color="0.82", lw=0.65, zorder=0)
    ax.set_xlim(-0.02, 1.23)
    ax.set_ylim(-0.62, len(metrics) - 0.35)
    ax.set_yticks([])
    ax.set_xlabel("Normalized within each variable")


def main() -> None:
    _style()
    macro = _prepare_macro()
    events = pd.read_csv(EVENT_TOPOLOGY)
    SOURCE_DATA.parent.mkdir(parents=True, exist_ok=True)
    _source_data(macro, events).to_csv(SOURCE_DATA, index=False)
    _write_mechanism_index_table(macro)

    fig = plt.figure(figsize=(7.35, 4.55))
    gs = fig.add_gridspec(
        2,
        3,
        left=0.075,
        right=0.985,
        bottom=0.105,
        top=0.855,
        width_ratios=[1.08, 1.12, 1.18],
        height_ratios=[1.0, 1.0],
        wspace=0.52,
        hspace=0.55,
    )
    ax_map = fig.add_subplot(gs[0, 0])
    ax_event = fig.add_subplot(gs[0, 1])
    ax_reach = fig.add_subplot(gs[1, 0:2])
    ax_fingerprint = fig.add_subplot(gs[:, 2])
    axes = [ax_map, ax_event, ax_reach, ax_fingerprint]
    for ax in axes:
        ax.set_facecolor("#FBFAF7")

    _scatter_cases(ax_map, macro)
    _plot_event_topology(ax_event, events)
    _plot_reachability(ax_reach, macro)
    _plot_fingerprint(ax_fingerprint, macro)

    for label, ax in zip("abcd", axes):
        ax.text(
            0.02,
            0.98,
            label,
            transform=ax.transAxes,
            fontsize=9.2,
            fontweight="bold",
            ha="left",
            va="top",
            clip_on=True,
        )

    handles = []
    labels = []
    plotted_case_labels = set(macro["case_label"])
    for key, style in CASE_STYLE.items():
        if key not in plotted_case_labels:
            continue
        handles.append(
            mpl.lines.Line2D(
                [],
                [],
                marker=style["marker"],
                linestyle="None",
                markerfacecolor=style["color"],
                markeredgecolor="#222222" if style["kind"] == "cracked" else "white",
                markersize=5.2,
            )
        )
        labels.append(style["label"])
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.54, 0.985),
        ncol=5,
        fontsize=6.4,
        columnspacing=0.85,
        handletextpad=0.35,
    )

    OUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    for suffix, kwargs in {
        ".svg": {},
        ".pdf": {},
        ".png": {"dpi": 600},
        ".tiff": {"dpi": 600},
    }.items():
        fig.savefig(OUT_STEM.with_suffix(suffix), bbox_inches="tight", **kwargs)
    print(OUT_STEM.with_suffix(".png"))
    print(SOURCE_DATA)
    print(MECHANISM_INDEX_TABLE)


if __name__ == "__main__":
    main()
