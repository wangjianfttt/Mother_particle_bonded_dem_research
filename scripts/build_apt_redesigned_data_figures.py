#!/usr/bin/env python3
"""Build source-data-backed repaired manuscript figures.

The figures are designed for journal review with high information density, all
raw case points visible, no mean-only bars, colorblind-safe colors plus
marker/line redundancy, and editable vector output.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "apt_redesign"
SRC = ROOT / "data" / "figure_source"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "tables"

INITIAL_BONDS = 493_500

COLORS = {
    "blue": "#0072B2",
    "orange": "#D55E00",
    "green": "#009E73",
    "purple": "#7A4FA3",
    "red": "#B2182B",
    "gold": "#E69F00",
    "grey": "#5F6B73",
    "black": "#222222",
    "wash": "#FBFAF7",
    "band": "#EFE8D8",
    "grid": "#E7E9EC",
}

CASE_STYLE = {
    "pilot_localized_microcracking": ("Pilot", COLORS["blue"], "o"),
    "seed02_intact_to_60um": ("Independent", COLORS["orange"], "s"),
    "seed03_delayed_microcracking_to_60um": ("Delayed", COLORS["green"], "^"),
    "seed04_early_microcracking_to_60um": ("Early", COLORS["red"], "P"),
    "seed06_synchronous_microcracking_to_60um": ("Synchronous", "#00A88A", "h"),
    "seed02_strength0p5_intact_to_60um": ("0.5x strength", "#4F7F52", "D"),
    "seed02_strength0p25_intact_to_60um": ("0.25x strength", COLORS["purple"], "v"),
}


def style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 7.6,
            "axes.labelsize": 7.6,
            "axes.titlesize": 7.6,
            "xtick.labelsize": 7.0,
            "ytick.labelsize": 7.0,
            "legend.fontsize": 6.6,
            "axes.linewidth": 0.65,
            "axes.edgecolor": "#2B2B2B",
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.major.size": 2.4,
            "ytick.major.size": 2.4,
            "xtick.major.width": 0.65,
            "ytick.major.width": 0.65,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def export(fig: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=450, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def panel(ax: plt.Axes, label: str, x: float = -0.16, y: float = 1.06) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.2,
        fontweight="bold",
        color=COLORS["black"],
    )


def clean_axes(ax: plt.Axes) -> None:
    ax.grid(True, axis="y", color=COLORS["grid"], lw=0.45, alpha=0.75)
    ax.set_facecolor("white")


def read_summary(case_id: str) -> dict[str, float]:
    path = PROCESSED / f"{case_id}_summary.csv"
    data = pd.read_csv(path)
    out: dict[str, float] = {}
    for _, row in data.iterrows():
        try:
            out[row["metric"]] = float(row["value"])
        except (TypeError, ValueError):
            continue
    return out


def final_fragments(case_id: str, n_particles: int) -> tuple[float, float, int]:
    data = pd.read_csv(PROCESSED / f"{case_id}_fragments.csv")
    final = data.sort_values("timestep").iloc[-1]
    return (
        float(final["largest_fragment_particles"]) / n_particles,
        float(final["second_fragment_particles"]) / n_particles,
        int(final["fragment_count"]),
    )


def thermo_curve(case_id: str) -> pd.DataFrame:
    data = pd.read_csv(PROCESSED / f"{case_id}_thermo.csv")
    data["disp_mm"] = pd.to_numeric(data["top_disp"], errors="coerce") * 1000.0
    data["top_force_N"] = pd.to_numeric(data["top_forc"], errors="coerce").abs()
    return data[["disp_mm", "top_force_N"]].dropna()


def build_single_pebble_source() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    targets = pd.read_csv(TABLES / "single_pebble_calibration_target_evidence_summary.csv")
    model = pd.read_csv(TABLES / "single_pebble_model_calibration_matrix.csv")
    orient = pd.read_csv(TABLES / "sp002_cal1_orientation_summary.csv")
    strength = pd.read_csv(TABLES / "sp002_strength_multiplier_validation.csv")
    weibull = pd.read_csv(TABLES / "sp002_weibull_ensemble_completed_summary.csv")
    resolution_cases = [(250, "SP-RES-250"), (500, "SP-RES-500"), (1000, "SP-RES-1000")]
    rate_cases = [(0.10, "SP-RES-500"), (0.05, "SP-RATE-500-0p05-FULL"), (0.03, "SP-RATE-500-0p03-FULL")]

    resolution_rows = []
    for count, case in resolution_cases:
        summary = read_summary(case)
        largest, second, fragments = final_fragments(case, count)
        resolution_rows.append(
            {
                "case": case,
                "subparticles": count,
                "peak_top_force_N": summary["peak_top_force_N"],
                "first_break_displacement_mm": summary["first_break_displacement_mm"],
                "largest_fragment_fraction": largest,
                "second_fragment_fraction": second,
                "fragment_count": fragments,
            }
        )

    rate_rows = []
    for velocity, case in rate_cases:
        summary = read_summary(case)
        largest, second, fragments = final_fragments(case, 500)
        rate_rows.append(
            {
                "case": case,
                "loading_velocity_m_s": velocity,
                "peak_top_force_N": summary["peak_top_force_N"],
                "first_break_displacement_mm": summary["first_break_displacement_mm"],
                "largest_fragment_fraction": largest,
                "second_fragment_fraction": second,
                "fragment_count": fragments,
            }
        )

    resolution = pd.DataFrame(resolution_rows)
    rates = pd.DataFrame(rate_rows)

    model_sources = []
    selected = model[model["case_id"] == "SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm"].iloc[0]
    homogeneous = model[model["case_id"] == "SP-002-calib-kn1e14-120MPa-0p1ms"].iloc[0]
    model_sources.append({"group": "homogeneous", "case": homogeneous["case_id"], "peak_top_force_N": homogeneous["peak_top_force_N"], "first_break_displacement_mm": homogeneous["first_break_displacement_mm"], "largest_fragment_fraction": homogeneous["largest_fragment_particles"] / 500.0, "second_fragment_fraction": homogeneous["second_fragment_particles"] / 500.0})
    model_sources.append({"group": "selected template", "case": selected["case_id"], "peak_top_force_N": selected["peak_top_force_N"], "first_break_displacement_mm": selected["first_break_displacement_mm"], "largest_fragment_fraction": selected["largest_fragment_particles"] / 500.0, "second_fragment_fraction": selected["second_fragment_particles"] / 500.0})
    for _, row in orient.iterrows():
        model_sources.append({"group": "orientation variants", "case": row["case_id"], "peak_top_force_N": row["peak_top_force_N"], "first_break_displacement_mm": row["first_break_displacement_mm"], "largest_fragment_fraction": row["largest_fragment_fraction"], "second_fragment_fraction": row["second_fragment_fraction"]})
    for _, row in strength.iterrows():
        model_sources.append({"group": "strength scan", "case": row["case_id"], "peak_top_force_N": row["peak_top_force_N"], "first_break_displacement_mm": row["first_break_displacement_mm"], "largest_fragment_fraction": row["largest_fragment_fraction"], "second_fragment_fraction": row["second_fragment_fraction"]})
    for _, row in weibull.iterrows():
        model_sources.append({"group": "Weibull samples", "case": row["case_id"], "peak_top_force_N": row["peak_top_force_N"], "first_break_displacement_mm": row["first_break_displacement_mm"], "largest_fragment_fraction": row["largest_fragment_fraction"], "second_fragment_fraction": row["second_fragment_fraction"]})
    model_points = pd.DataFrame(model_sources)

    SRC.mkdir(parents=True, exist_ok=True)
    targets.to_csv(SRC / "fig2_single_pebble_literature_targets.csv", index=False)
    model_points.to_csv(SRC / "fig2_single_pebble_model_points.csv", index=False)
    resolution.to_csv(SRC / "fig2_single_pebble_resolution_metrics.csv", index=False)
    rates.to_csv(SRC / "fig2_single_pebble_rate_metrics.csv", index=False)
    return targets, model_points, pd.concat([resolution.assign(series="resolution"), rates.assign(series="rate")], ignore_index=True, sort=False)


def figure_single_pebble() -> None:
    targets, model_points, robustness = build_single_pebble_source()
    fig, axes = plt.subplots(2, 2, figsize=(7.35, 5.05), constrained_layout=True)
    ax = axes[0, 0]
    ax.axhspan(15, 22, color=COLORS["band"], alpha=0.65, zorder=0)
    target_styles = {
        "verified tabulated anchor": ("Zhao tabulated", COLORS["green"], "o"),
        "digitized size-effect anchor": ("Annabattula digitized", COLORS["orange"], "s"),
        "near-size/context": ("near-size/context", COLORS["purple"], "^"),
    }
    used = set()
    for _, row in targets.dropna(subset=["diameter_mm", "mean_crush_load_N"]).iterrows():
        label, color, marker = target_styles.get(row["evidence_class"], ("literature", COLORS["grey"], "D"))
        legend_label = label if label not in used else "_nolegend_"
        used.add(label)
        yerr = row["std_crush_load_N"] if np.isfinite(row["std_crush_load_N"]) else None
        ax.errorbar(
            row["diameter_mm"],
            row["mean_crush_load_N"],
            yerr=yerr,
            fmt=marker,
            ms=4.4,
            lw=0.8,
            capsize=2.0 if yerr is not None else 0,
            color=color,
            ecolor=color,
            alpha=0.92,
            label=legend_label,
        )
    selected = model_points[model_points["group"] == "selected template"].iloc[0]
    ax.scatter(1.0, selected["peak_top_force_N"], marker="*", s=115, color=COLORS["black"], label="selected template", zorder=5)
    ax.set_xlabel("Particle diameter (mm)")
    ax.set_ylabel("Crush load / peak force (N)")
    ax.set_xlim(0.18, 1.65)
    ax.set_ylim(0, 32)
    ax.legend(loc="upper left", fontsize=5.9, handlelength=1.2)
    ax.text(1.02, 21.5, "target window", fontsize=6.2, ha="left", va="top", color="#6D6656")
    panel(ax, "a")

    ax = axes[0, 1]
    order = ["homogeneous", "selected template", "orientation variants", "strength scan", "Weibull samples"]
    y = np.arange(len(order))
    colors = [COLORS["grey"], COLORS["black"], COLORS["purple"], COLORS["orange"], COLORS["green"]]
    for i, group in enumerate(order):
        sub = model_points[model_points["group"] == group]
        ax.scatter(sub["peak_top_force_N"], np.full(len(sub), i), color=colors[i], s=23, alpha=0.9, edgecolor="white", linewidth=0.4)
        if len(sub) > 1:
            ax.hlines(i, sub["peak_top_force_N"].min(), sub["peak_top_force_N"].max(), color=colors[i], lw=1.2, alpha=0.45)
    ax.axvspan(15, 22, color=COLORS["band"], alpha=0.65, zorder=0)
    ax.set_yticks(y, ["homogeneous", "selected\ntemplate", "orientation\nvariants", "strength\nscan", "Weibull\nsamples"])
    ax.invert_yaxis()
    ax.set_xlabel("Peak top force (N)")
    ax.set_xlim(8, 31)
    panel(ax, "b")

    ax = axes[1, 0]
    res = robustness[robustness["series"] == "resolution"].sort_values("subparticles")
    rate = robustness[robustness["series"] == "rate"].sort_values("loading_velocity_m_s")
    ref = res[res["subparticles"] == 500].iloc[0]
    ax.plot(res["subparticles"], res["peak_top_force_N"] / ref["peak_top_force_N"], color=COLORS["blue"], marker="o", lw=1.3, label="peak force")
    ax.plot(res["subparticles"], res["first_break_displacement_mm"] / ref["first_break_displacement_mm"], color=COLORS["orange"], marker="s", lw=1.2, ls="--", label="first break")
    ax.axhline(1.0, color="0.6", lw=0.75, ls=(0, (2, 2)))
    ax.set_xlabel("Subparticles per particle")
    ax.set_ylabel("Normalized by 500-subparticle case")
    ax.set_xticks([250, 500, 1000])
    ax.legend(loc="upper left")
    panel(ax, "c")

    ax = axes[1, 1]
    x = np.arange(len(rate))
    labels = [f"{v:.2f}" for v in rate["loading_velocity_m_s"]]
    ax.scatter(x - 0.10, rate["largest_fragment_fraction"], s=34, color=COLORS["blue"], marker="o", label="largest")
    ax.scatter(x + 0.10, rate["second_fragment_fraction"], s=34, color=COLORS["orange"], marker="s", label="second")
    for i, row in enumerate(rate.itertuples()):
        ax.plot([i - 0.10, i + 0.10], [row.largest_fragment_fraction, row.second_fragment_fraction], color="0.78", lw=0.9, zorder=0)
    ax.set_xticks(x, labels)
    ax.set_xlabel("Loading velocity (m s$^{-1}$)")
    ax.set_ylabel("Final fragment fraction")
    ax.set_ylim(0.38, 0.52)
    ax.legend(loc="lower left", ncol=2, handletextpad=0.4)
    panel(ax, "d")
    for item in axes.flat:
        clean_axes(item)
    export(fig, OUT / "fig2_single_pebble_template_validation")


def figure_entry_validation() -> None:
    series = pd.read_csv(TABLES / "pb007_step_relaxed_validation_y1p5e10_10krelax_5um_series.csv")
    accept = pd.read_csv(TABLES / "pb007_bonded_steprelaxed_100_y1p5e10_10krelax_5um_acceptance_summary.csv").iloc[0]
    native = pd.read_csv(TABLES / "pb007_bonded_steprelaxed_100_y1p5e10_10krelax_5um_native_summary.csv").iloc[0]
    screen = pd.read_csv(TABLES / "pb007_stiffness_restore_young_screen.csv")
    endpoints = series.groupby("disp_um", as_index=False).tail(1).sort_values("disp_um")
    SRC.mkdir(parents=True, exist_ok=True)
    series.to_csv(SRC / "fig3_entry_validation_relaxation_series.csv", index=False)
    screen.to_csv(SRC / "fig3_entry_validation_stiffness_screen.csv", index=False)
    pd.DataFrame([accept]).to_csv(SRC / "fig3_entry_validation_acceptance_summary.csv", index=False)
    pd.DataFrame([native]).to_csv(SRC / "fig3_entry_validation_native_summary.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(7.35, 4.75), constrained_layout=True)
    ax = axes[0, 0]
    ax.plot(
        endpoints["disp_um"],
        endpoints["top_force_mN"],
        color=COLORS["blue"],
        lw=1.2,
        marker="o",
        ms=3.2,
        label="top wall",
    )
    ax.plot(
        endpoints["disp_um"],
        endpoints["incremental_wall_force_mN"],
        color=COLORS["orange"],
        lw=1.15,
        marker="s",
        ms=3.0,
        ls="--",
        label="baseline-corrected walls",
    )
    ax.set_xlabel("Entry displacement (µm)")
    ax.set_ylabel("Force (mN)")
    ax.set_xlim(-0.1, 5.15)
    ax.set_ylim(0, max(endpoints["top_force_mN"].max(), endpoints["incremental_wall_force_mN"].max()) * 1.12)
    ax.legend(loc="lower left", handlelength=1.8)
    ax.text(
        0.05,
        0.90,
        f"final residual {accept['incremental_wall_balance_residual_percent']:.1f}%",
        transform=ax.transAxes,
        fontsize=6.4,
        color=COLORS["blue"],
        fontweight="bold",
    )
    panel(ax, "a")

    ax = axes[0, 1]
    valid = endpoints[(endpoints["balance_residual_percent"] > 0) & np.isfinite(endpoints["balance_residual_percent"])]
    ax.plot(valid["disp_um"], valid["balance_residual_percent"], color=COLORS["green"], marker="o", lw=1.25, ms=3.0)
    ax.axhspan(0.1, 5.0, color=COLORS["green"], alpha=0.12, lw=0)
    ax.axhline(5.0, color=COLORS["green"], lw=0.8, ls=(0, (2, 2)))
    ax.set_yscale("log")
    ax.set_xlabel("Entry displacement (µm)")
    ax.set_ylabel("Force-balance residual (%)")
    ax.set_xlim(-0.05, 5.15)
    panel(ax, "b")

    ax = axes[1, 0]
    screen = screen.copy()
    x = screen["contact_young_Pa"].astype(float) / 1e9
    y = screen["spurious_bonds_lost"].astype(float)
    ok = y == 0
    ax.scatter(x[ok], y[ok], s=42, color=COLORS["green"], marker="o", label="intact")
    ax.scatter(x[~ok], y[~ok], s=42, color=COLORS["red"], marker="x", label="pre-loading bond loss")
    ax.axvline(15, color=COLORS["blue"], lw=0.9, ls=(0, (3, 2)), label="selected 15 GPa")
    ax.set_xscale("log")
    ax.set_xlabel("Restored contact modulus (GPa)")
    ax.set_ylabel("Pre-loading broken bonds")
    ax.set_ylim(-0.8, max(y.max() * 1.18, 2.0))
    ax.legend(loc="upper left")
    panel(ax, "c")

    ax = axes[1, 1]
    metrics = pd.DataFrame(
        {
            "metric": ["inter-particle edges", "top-reachable particles", "bottom reachable from top", "intact bonds (%)"],
            "value": [native["inter_pebble_edges"], native["top_reachable_mother_pebbles"], native["bottom_mothers_reachable_from_top"], accept["minimum_intact_bonds"] / accept["initial_intact_bonds"] * 100],
            "label": [
                f"{native['inter_pebble_edges']:.0f}",
                f"{native['top_reachable_mother_pebbles']:.0f}",
                f"{native['bottom_mothers_reachable_from_top']:.0f}",
                f"{accept['minimum_intact_bonds'] / accept['initial_intact_bonds'] * 100:.1f}%",
            ],
            "color": [COLORS["purple"], COLORS["blue"], COLORS["grey"], COLORS["green"]],
        }
    )
    yy = np.arange(len(metrics))
    for i, row in metrics.iterrows():
        ax.hlines(i, 0, row["value"], color=row["color"], lw=3.2, alpha=0.45)
        ax.scatter(row["value"], i, s=46, color=row["color"], edgecolor="white", linewidth=0.5)
        ax.text(row["value"] + 2.0, i, row["label"], va="center", fontsize=6.3, color=row["color"])
    ax.set_yticks(yy, metrics["metric"])
    ax.invert_yaxis()
    ax.set_xlabel("Value (counts; intact bonds, %)")
    ax.set_xlim(0, 112)
    panel(ax, "d")
    for item in axes.flat:
        clean_axes(item)
    export(fig, OUT / "fig3_entry_state_validation")


def prepare_thermo(case_id: str) -> pd.DataFrame:
    thermo = pd.read_csv(PROCESSED / f"{case_id}_thermo.csv")
    for col in ["Step", "top_disp", "top_forc", "bond_int"]:
        thermo[col] = pd.to_numeric(thermo[col], errors="coerce")
    thermo = thermo[(thermo["bond_int"] > 0) & (thermo["Step"] >= 10001)].drop_duplicates("Step").copy()
    thermo["disp_um"] = thermo["top_disp"] * 1e6
    thermo["top_force_mN"] = thermo["top_forc"].abs() * 1e3
    thermo["broken_total"] = thermo["bond_int"].iloc[0] - thermo["bond_int"]
    return thermo


def figure_fracture_sequence() -> None:
    case = "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot"
    thermo = prepare_thermo(case)
    events = pd.read_csv(PROCESSED / f"{case}_breakage_events.csv")
    native = pd.read_csv(PROCESSED / f"{case}_native_force_network_series.csv")
    native["disp_um"] = (native["timestep"].astype(float) - 10000.0) / 2000.0
    SRC.mkdir(parents=True, exist_ok=True)
    thermo.to_csv(SRC / "fig4_fracture_sequence_pilot_thermo.csv", index=False)
    events.to_csv(SRC / "fig4_fracture_sequence_pilot_events.csv", index=False)
    native.to_csv(SRC / "fig4_fracture_sequence_pilot_native_network.csv", index=False)

    fig = plt.figure(figsize=(7.35, 6.25), constrained_layout=True)
    gs = fig.add_gridspec(3, 2, height_ratios=[1.05, 0.80, 0.92])
    ax0 = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[1, :])
    ax2 = fig.add_subplot(gs[2, 0])
    ax3 = fig.add_subplot(gs[2, 1])

    macro = (
        thermo.groupby("disp_um", as_index=False)
        .agg(top_force_mN=("top_force_mN", "max"), broken_total=("broken_total", "max"))
        .sort_values("disp_um")
    )
    ax0.plot(macro["disp_um"], macro["top_force_mN"], color=COLORS["blue"], lw=1.45)
    ax0.fill_between(macro["disp_um"], 0, macro["top_force_mN"], color=COLORS["blue"], alpha=0.08, lw=0)
    event_y = events["top_force_z_N"].abs() * 1e3
    ax0.scatter(events["top_displacement_mm"] * 1000, event_y, s=38 + events["new_broken_bonds"] * 14, color=COLORS["red"], edgecolor="white", linewidth=0.55, zorder=5)
    for i, row in events.iterrows():
        x = row["top_displacement_mm"] * 1000
        ax0.axvline(x, color=COLORS["red"], lw=0.7, ls=(0, (2, 2)), alpha=0.65)
        ax0.text(x, ax0.get_ylim()[1] * 0.92, f"E{int(row['event_index'])}", ha="center", va="top", color=COLORS["red"], fontsize=6.5, fontweight="bold")
    peak = macro.loc[macro["top_force_mN"].idxmax()]
    endpoint = thermo.iloc[-1]
    relax = 100 * (peak["top_force_mN"] - endpoint["top_force_mN"]) / peak["top_force_mN"]
    ax0.scatter([peak["disp_um"]], [peak["top_force_mN"]], s=28, color=COLORS["black"], edgecolor="white", linewidth=0.45)
    ax0.text(0.76, 0.92, f"peak-to-endpoint\nrelaxation {relax:.1f}%", transform=ax0.transAxes, ha="left", va="top", fontsize=6.4)
    ax0.set_xlabel("Top-wall displacement (µm)")
    ax0.set_ylabel("Top-wall force (mN)")
    ax0.set_xlim(0, 62)
    panel(ax0, "a", x=-0.045)

    ax1.step(macro["disp_um"], macro["broken_total"], where="post", color=COLORS["black"], lw=1.35)
    ax1.scatter(events["top_displacement_mm"] * 1000, events["cumulative_broken_bonds"], color=COLORS["red"], s=35 + events["new_broken_bonds"] * 12, edgecolor="white", linewidth=0.5)
    for _, row in events.iterrows():
        ax1.text(row["top_displacement_mm"] * 1000, row["cumulative_broken_bonds"] + 0.35, f"+{int(row['new_broken_bonds'])}", ha="center", va="bottom", fontsize=6.1, color=COLORS["red"])
    ax1.set_xlabel("Top-wall displacement (µm)")
    ax1.set_ylabel("Cumulative broken bonds")
    ax1.set_ylim(-0.3, 6.2)
    panel(ax1, "b")

    ax2.plot(native["inter_pebble_force_sum_N"], native["inter_pebble_edges"], color=COLORS["green"], marker="o", lw=0.95, ms=4, alpha=0.85)
    for idx in range(len(native) - 1):
        start = native.iloc[idx]
        end = native.iloc[idx + 1]
        ax2.annotate(
            "",
            xy=(end["inter_pebble_force_sum_N"], end["inter_pebble_edges"]),
            xytext=(start["inter_pebble_force_sum_N"], start["inter_pebble_edges"]),
            arrowprops={"arrowstyle": "->", "color": COLORS["green"], "lw": 0.8, "shrinkA": 7, "shrinkB": 7, "alpha": 0.75},
        )
    for _, row in native.iterrows():
        ax2.text(row["inter_pebble_force_sum_N"] + 0.015, row["inter_pebble_edges"], f"{row['disp_um']:.0f}", fontsize=5.7, va="center", color=COLORS["green"])
    ax2.set_xlabel("Inter-particle force sum (N)")
    ax2.set_ylabel("Inter-particle force edges")
    panel(ax2, "c")

    ax3.plot(
        native["top_reachable_mother_pebbles"],
        native["bottom_mothers_reachable_from_top"],
        color=COLORS["purple"],
        lw=0.95,
        alpha=0.75,
        zorder=1,
    )
    for idx in range(len(native) - 1):
        start = native.iloc[idx]
        end = native.iloc[idx + 1]
        ax3.annotate(
            "",
            xy=(end["top_reachable_mother_pebbles"], end["bottom_mothers_reachable_from_top"]),
            xytext=(start["top_reachable_mother_pebbles"], start["bottom_mothers_reachable_from_top"]),
            arrowprops={"arrowstyle": "->", "color": COLORS["purple"], "lw": 0.8, "shrinkA": 8, "shrinkB": 8, "alpha": 0.75},
        )
    ax3.text(0.04, 0.95, "labels: displacement (µm)", transform=ax3.transAxes, ha="left", va="top", fontsize=5.8, color=COLORS["grey"])
    ax3.scatter(native["top_reachable_mother_pebbles"], native["bottom_mothers_reachable_from_top"], s=36 + native["inter_pebble_edges"] * 0.7, color=COLORS["purple"], edgecolor="white", linewidth=0.5, zorder=2)
    for _, row in native.iterrows():
        ax3.text(row["top_reachable_mother_pebbles"] + 0.35, row["bottom_mothers_reachable_from_top"], f"{row['disp_um']:.0f}", fontsize=5.7, va="center", color=COLORS["purple"])
    ax3.set_xlabel("Top-reachable particles")
    ax3.set_ylabel("Bottom particles reachable from top")
    panel(ax3, "d")
    for item in [ax0, ax1, ax2, ax3]:
        clean_axes(item)
    export(fig, OUT / "fig4_pilot_fracture_event_sequence")


def figure_mechanism_state_space() -> None:
    macro = pd.read_csv(TABLES / "pb007_macro_topology_event_metrics.csv")
    events = pd.read_csv(TABLES / "pb007_event_aligned_topology.csv")
    mechanism = pd.read_csv(TABLES / "pb007_mechanism_indices.csv")
    mechanism["display_case"] = mechanism["display_case"].replace(
        {
            "0.5x audit": "0.5x strength",
            "0.25x audit": "0.25x strength",
        }
    )
    macro["display_case"] = macro["case_label"].map(lambda key: CASE_STYLE[key][0])
    macro["color"] = macro["case_label"].map(lambda key: CASE_STYLE[key][1])
    macro["marker"] = macro["case_label"].map(lambda key: CASE_STYLE[key][2])
    macro["broken_bond_fraction_x1e5"] = macro["broken_bonds_at_endpoint"] / INITIAL_BONDS * 1e5
    macro["network_reorganization_fraction"] = (macro["max_inter_mother_edges"] - macro["final_inter_mother_edges"]) / macro["max_inter_mother_edges"]
    macro["force_relaxation_fraction"] = (macro["peak_top_force_N"] - macro["final_top_force_N"]) / macro["peak_top_force_N"].replace(0, np.nan)
    macro["force_path_intensity_norm"] = macro["final_inter_pebble_force_sum_N"] / macro["final_inter_pebble_force_sum_N"].max()
    SRC.mkdir(parents=True, exist_ok=True)
    macro.to_csv(SRC / "fig5_mechanism_state_macro_metrics.csv", index=False)
    events.to_csv(SRC / "fig5_mechanism_state_event_aligned_topology.csv", index=False)
    mechanism.to_csv(SRC / "fig5_mechanism_state_mechanism_indices.csv", index=False)

    fig = plt.figure(figsize=(7.35, 4.25), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.05, 1.08], height_ratios=[1.0, 1.0])
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    for _, row in macro.iterrows():
        size = 48 + 20 * row["broken_bonds_at_endpoint"]
        ax0.scatter(row["final_inter_pebble_force_sum_N"], row["broken_bonds_at_endpoint"], s=size, color=row["color"], marker=row["marker"], edgecolor=COLORS["black"] if row["broken_bonds_at_endpoint"] > 0 else "white", linewidth=0.55)
        if row["display_case"] in {"Pilot", "Delayed"}:
            ax0.text(
                row["final_inter_pebble_force_sum_N"] + 0.025,
                row["broken_bonds_at_endpoint"] + 0.2,
                row["display_case"],
                fontsize=6.2,
                color=row["color"],
            )
    ax0.axhspan(-0.8, 0.8, color="#F3F5F6", zorder=0)
    ax0.set_xlabel("Endpoint inter-particle force sum (N)")
    ax0.set_ylabel("Endpoint broken bonds")
    ax0.set_xlim(0.18, 1.12)
    ax0.set_ylim(-0.8, 11.5)
    panel(ax0, "a")

    sc = ax1.scatter(
        events["force_sum_ratio_next_to_previous"],
        events["delta_inter_mother_edges"],
        c=events["cumulative_broken_bonds"],
        s=58 + 35 * events["new_broken_bonds"],
        cmap="magma_r",
        edgecolor=COLORS["black"],
        linewidth=0.55,
    )
    ax1.axvline(1, color="0.72", lw=0.8, ls=(0, (2, 2)))
    for _, row in events.iterrows():
        ax1.text(row["force_sum_ratio_next_to_previous"] + 0.04, row["delta_inter_mother_edges"] + 0.12, f"+{int(row['new_broken_bonds'])}", fontsize=5.9)
    ax1.set_xlabel("Next / previous force sum")
    ax1.set_ylabel("Change in force edges")
    cbar = fig.colorbar(sc, ax=ax1, fraction=0.045, pad=0.02)
    cbar.set_label("Cumulative broken bonds", fontsize=6.0)
    cbar.ax.tick_params(labelsize=5.6)
    panel(ax1, "b")

    for _, row in macro.iterrows():
        ax2.scatter(row["final_bottom_reachable_from_top"], row["final_top_reachable_mothers"], s=54 + 12 * row["broken_bonds_at_endpoint"], color=row["color"], marker=row["marker"], edgecolor=COLORS["black"] if row["broken_bonds_at_endpoint"] > 0 else "white", linewidth=0.55)
        if row["display_case"] in {"Pilot", "Delayed"}:
            ax2.text(
                row["final_bottom_reachable_from_top"] + 0.35,
                row["final_top_reachable_mothers"] - 0.4,
                f"{int(row['broken_bonds_at_endpoint'])} bonds",
                fontsize=6.0,
                color=row["color"],
            )
    ax2.set_xlabel("Bottom particles reachable from top")
    ax2.set_ylabel("Top-reachable particles")
    ax2.set_xlim(5.5, 19.5)
    ax2.set_ylim(50, 72)
    panel(ax2, "c")

    heat_cols = ["force_path_intensity_norm", "network_reorganization_fraction", "force_relaxation_fraction", "broken_bond_fraction_x1e5"]
    heat = mechanism.set_index("display_case")[heat_cols].copy()
    display_order = ["Delayed", "Pilot", "Independent", "0.5x strength", "0.25x strength"]
    heat = heat.loc[[idx for idx in display_order if idx in heat.index]]
    heat_norm = heat / heat.max(axis=0).replace(0, np.nan)
    im = ax3.imshow(heat_norm.values, cmap="viridis", vmin=0, vmax=1, aspect="auto")
    ax3.set_xticks(np.arange(len(heat_cols)), ["force\npath", "network\nchange", "force\nrelax", "bond\nloss"])
    ax3.set_yticks(np.arange(len(heat_norm.index)), heat_norm.index)
    cmap = plt.get_cmap("viridis")
    for i in range(heat_norm.shape[0]):
        for j in range(heat_norm.shape[1]):
            val = heat_norm.iloc[i, j]
            rgb = cmap(float(val))[:3]
            luminance = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
            text_color = "black" if luminance > 0.55 else "white"
            ax3.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=5.5, color=text_color)
    cbar = fig.colorbar(im, ax=ax3, fraction=0.045, pad=0.02)
    cbar.set_label("Column-normalized value", fontsize=6.0)
    cbar.ax.tick_params(labelsize=5.6)
    panel(ax3, "d")

    legend_handles = [
        Line2D([0], [0], marker=CASE_STYLE[key][2], color="none", markerfacecolor=CASE_STYLE[key][1], markeredgecolor="white", label=CASE_STYLE[key][0], markersize=5.5)
        for key in CASE_STYLE
    ]
    fig.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(0.52, 1.02), ncol=5, handletextpad=0.45, columnspacing=0.8)
    for item in [ax0, ax1, ax2, ax3]:
        clean_axes(item)
    ax3.grid(False)
    export(fig, OUT / "fig5_mechanism_state_space")


def main() -> None:
    style()
    OUT.mkdir(parents=True, exist_ok=True)
    SRC.mkdir(parents=True, exist_ok=True)
    figure_single_pebble()
    figure_entry_validation()
    figure_fracture_sequence()
    figure_mechanism_state_space()
    print(OUT)
    print(SRC)


if __name__ == "__main__":
    main()
