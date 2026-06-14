#!/usr/bin/env python3
"""Build a publication-grade pilot/replicate comparison figure."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT_STEM = ROOT / "figures" / "pb007" / "pb007_replicate_comparison"
SOURCE_DATA = ROOT / "data" / "processed" / "pb007_replicate_comparison_source_data.csv"
SUMMARY_DATA = ROOT / "tables" / "pb007_macro_topology_event_metrics.csv"
INITIAL_BONDS = 493_500


@dataclass(frozen=True)
class Case:
    label: str
    short: str
    case_id: str
    color: str
    linestyle: str


CASES = [
    Case(
        label="Pilot: localized microcracking",
        short="Pilot",
        case_id="PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot",
        color="#335C81",
        linestyle="-",
    ),
    Case(
        label="Independent replicate: intact to 60 um",
        short="Independent",
        case_id="PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed02",
        color="#B85C38",
        linestyle="-",
    ),
    Case(
        label="Third bed: delayed microcracking",
        short="Delayed",
        case_id="PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03",
        color="#168A74",
        linestyle="-",
    ),
    Case(
        label="Independent replicate, 0.5x bond strength: intact",
        short="0.5x audit",
        case_id="PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p5-trigger-seed02",
        color="#4F7F52",
        linestyle="--",
    ),
    Case(
        label="Independent replicate, 0.25x bond strength: intact",
        short="0.25x audit",
        case_id="PB-007-bonded-steprelaxed-100-seed02-600ksettle-y1p5e10-10krelax-60um-nohold-strength0p25-trigger-seed02",
        color="#7C6A9D",
        linestyle=":",
    ),
]


def _read_thermo(case: Case) -> pd.DataFrame:
    path = ROOT / "data" / "processed" / f"{case.case_id}_thermo.csv"
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    for col in [
        "Step",
        "KinEng",
        "top_disp",
        "top_forc",
        "bottom_f",
        "side_for",
        "all_wall",
        "bond_bro",
        "bond_int",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[df["bond_int"] > 0].drop_duplicates(subset="Step", keep="last").copy()
    df = df.sort_values("Step")
    df["disp_um"] = df["top_disp"] * 1.0e6
    df["top_force_mN"] = df["top_forc"].abs() * 1.0e3
    df["broken_bonds"] = INITIAL_BONDS - df["bond_int"]
    df["broken_bonds"] = df["broken_bonds"].clip(lower=0)
    # Repeated run-0/load rows can share a displacement; keep the most damaged
    # and highest-load state at each displayed displacement.
    grouped = (
        df.groupby("disp_um", as_index=False)
        .agg(
            top_force_mN=("top_force_mN", "max"),
            broken_bonds=("broken_bonds", "max"),
            kinetic_energy_J=("KinEng", "last"),
        )
        .sort_values("disp_um")
    )
    grouped["case"] = case.short
    return grouped


def _read_native(case: Case, thermo: pd.DataFrame) -> pd.DataFrame:
    path = ROOT / "data" / "processed" / f"{case.case_id}_native_force_network_series.csv"
    native = pd.read_csv(path)
    for col in [
        "timestep",
        "inter_pebble_edges",
        "inter_pebble_subcontacts",
        "inter_pebble_force_sum_N",
        "top_reachable_mother_pebbles",
        "bottom_mothers_reachable_from_top",
        "spanning_force_graph",
    ]:
        native[col] = pd.to_numeric(native[col], errors="coerce")
    thermo_path = ROOT / "data" / "processed" / f"{case.case_id}_thermo.csv"
    raw = pd.read_csv(thermo_path)
    raw.columns = [c.strip() for c in raw.columns]
    raw["Step"] = pd.to_numeric(raw["Step"], errors="coerce")
    raw["top_disp"] = pd.to_numeric(raw["top_disp"], errors="coerce")
    raw = raw.dropna(subset=["Step", "top_disp"]).drop_duplicates(subset="Step", keep="last")
    step_to_disp = raw.set_index("Step")["top_disp"].to_dict()
    native["disp_um"] = native["timestep"].map(step_to_disp).astype(float) * 1.0e6
    if native["disp_um"].isna().any():
        # Fall back to nearest thermo displacement if an event dump step is not
        # exactly present in the compact thermo extraction.
        raw_steps = raw["Step"].to_numpy(dtype=float)
        raw_disp = raw["top_disp"].to_numpy(dtype=float)
        missing = native["disp_um"].isna()
        for idx, step in native.loc[missing, "timestep"].items():
            nearest = int(np.argmin(np.abs(raw_steps - step)))
            native.loc[idx, "disp_um"] = raw_disp[nearest] * 1.0e6
    native["case"] = case.short
    summary = _read_summary(case)
    if "last_valid_bond_step" in summary.index and pd.notna(summary["last_valid_bond_step"]):
        final_step = int(summary["last_valid_bond_step"])
    else:
        valid = raw[raw["top_disp"] <= float(summary["final_top_displacement_m"]) + 1.0e-12]
        final_step = int(valid["Step"].max()) if not valid.empty else int(raw["Step"].max())
    final_row = {
        "timestep": final_step,
        "inter_pebble_edges": float(summary["native_inter_pebble_edges"]),
        "inter_pebble_subcontacts": np.nan,
        "inter_pebble_force_sum_N": np.nan,
        "inter_pebble_force_mean_N": np.nan,
        "inter_pebble_force_max_N": np.nan,
        "top_loaded_mother_pebbles": np.nan,
        "bottom_loaded_mother_pebbles": np.nan,
        "top_wall_force_z_N": np.nan,
        "bottom_wall_force_z_N": np.nan,
        "side_wall_force_z_N": np.nan,
        "all_wall_force_z_N": np.nan,
        "top_reachable_mother_pebbles": float(summary["native_top_reachable_mother_pebbles"]),
        "bottom_mothers_reachable_from_top": float(summary["native_bottom_mothers_reachable_from_top"]),
        "spanning_force_graph": float(summary["native_spanning_force_graph"]),
        "disp_um": float(summary["final_top_displacement_um"]),
        "case": case.short,
    }
    native = pd.concat([native, pd.DataFrame([final_row])], ignore_index=True)
    native = native.drop_duplicates(subset=["disp_um"], keep="last")
    return native.sort_values("disp_um")


def _read_events(case: Case) -> pd.DataFrame:
    path = ROOT / "data" / "processed" / f"{case.case_id}_breakage_events.csv"
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    df = pd.read_csv(path)
    if df.empty:
        return df
    for col in ["top_displacement_mm", "new_broken_bonds", "cumulative_broken_bonds", "pebble_id"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["disp_um"] = df["top_displacement_mm"] * 1000.0
    df["case"] = case.short
    return df


def _read_summary(case: Case) -> pd.Series:
    path = ROOT / "tables" / f"pb007_{case.case_id}_acceptance_summary.csv"
    return pd.read_csv(path).iloc[0]


def _event_step_series(case: Case, event_df: pd.DataFrame, summary: pd.Series) -> pd.DataFrame:
    final_disp = float(summary["final_top_displacement_um"])
    rows = [{"disp_um": 0.0, "cumulative_broken_bonds": 0.0, "new_broken_bonds": 0.0, "case": case.short}]
    if not event_df.empty:
        grouped = (
            event_df.groupby("disp_um", as_index=False)
            .agg(new_broken_bonds=("new_broken_bonds", "sum"))
            .sort_values("disp_um")
        )
        cumulative = 0.0
        for _, row in grouped.iterrows():
            cumulative += float(row["new_broken_bonds"])
            rows.append(
                {
                    "disp_um": float(row["disp_um"]),
                    "cumulative_broken_bonds": cumulative,
                    "new_broken_bonds": float(row["new_broken_bonds"]),
                    "case": case.short,
                }
            )
    if rows[-1]["disp_um"] < final_disp:
        rows.append(
            {
                "disp_um": final_disp,
                "cumulative_broken_bonds": rows[-1]["cumulative_broken_bonds"],
                "new_broken_bonds": 0.0,
                "case": case.short,
            }
        )
    return pd.DataFrame(rows)


def _style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 7.2,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.7,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "legend.frameon": False,
        }
    )


def main() -> None:
    _style()
    OUT_STEM.parent.mkdir(parents=True, exist_ok=True)
    SOURCE_DATA.parent.mkdir(parents=True, exist_ok=True)

    thermo = {case.short: _read_thermo(case) for case in CASES}
    native = {case.short: _read_native(case, thermo[case.short]) for case in CASES}
    events = {case.short: _read_events(case) for case in CASES}
    summaries = {case.short: _read_summary(case) for case in CASES}
    macro = pd.read_csv(SUMMARY_DATA)
    macro_short = {
        "pilot_localized_microcracking": "Pilot",
        "seed02_intact_to_60um": "Independent",
        "seed03_delayed_microcracking_to_60um": "Delayed",
        "seed02_strength0p5_intact_to_60um": "0.5x audit",
        "seed02_strength0p25_intact_to_60um": "0.25x audit",
    }
    macro["case"] = macro["case_label"].map(macro_short)
    macro = macro.dropna(subset=["case"]).copy()
    event_steps = {
        case.short: _event_step_series(case, events[case.short], summaries[case.short])
        for case in CASES
    }

    source_frames: list[pd.DataFrame] = []
    for case in CASES:
        t = thermo[case.short].copy()
        t["source_panel"] = "a_b_thermo"
        source_frames.append(t)
        n = native[case.short].copy()
        n["source_panel"] = "c_d_native"
        source_frames.append(n)
        if not events[case.short].empty:
            e = events[case.short].copy()
            e["source_panel"] = "b_event_markers"
            source_frames.append(e)
        es = event_steps[case.short].copy()
        es["source_panel"] = "b_event_step_series"
        source_frames.append(es)
    pd.concat(source_frames, ignore_index=True, sort=False).to_csv(SOURCE_DATA, index=False)

    fig = plt.figure(figsize=(7.25, 4.85))
    gs = fig.add_gridspec(
        2,
        3,
        left=0.075,
        right=0.985,
        bottom=0.11,
        top=0.88,
        width_ratios=[1.48, 1.02, 1.18],
        height_ratios=[1.18, 1.0],
        wspace=0.52,
        hspace=0.46,
    )
    ax_force = fig.add_subplot(gs[0, :2])
    ax_bonds = fig.add_subplot(gs[1, 0])
    ax_edges = fig.add_subplot(gs[1, 1])
    ax_fingerprint = fig.add_subplot(gs[:, 2])
    wash = "#FBFAF7"
    for ax in [ax_force, ax_bonds, ax_edges, ax_fingerprint]:
        ax.set_facecolor(wash)

    for case in CASES:
        df = thermo[case.short]
        force_alpha = 1.0 if case.short in {"Pilot", "Independent", "Delayed"} else 0.45
        force_lw = 1.85 if case.short in {"Pilot", "Independent", "Delayed"} else 0.9
        ax_force.plot(
            df["disp_um"],
            df["top_force_mN"],
            color=case.color,
            lw=force_lw,
            ls=case.linestyle,
            alpha=force_alpha,
            label=case.short,
        )
        bdf = event_steps[case.short]
        ax_bonds.step(
            bdf["disp_um"],
            bdf["cumulative_broken_bonds"],
            where="post",
            color=case.color,
            lw=1.55,
            ls=case.linestyle,
            label=case.short,
        )
        nd = native[case.short]
        if case.short in {"Pilot", "Independent", "Delayed"}:
            ax_edges.plot(nd["disp_um"], nd["inter_pebble_edges"], marker="o", ms=3.4, lw=1.4, ls=case.linestyle, color=case.color)
            ax_edges.plot(nd["disp_um"], nd["top_reachable_mother_pebbles"], marker="s", ms=3.0, lw=1.15, ls="--", color=case.color, alpha=0.82)

    plotted_events = pd.concat(
        [
            event_steps[name].loc[event_steps[name]["new_broken_bonds"] > 0].copy()
            for name in ["Pilot", "Delayed"]
            if not event_steps[name].empty
        ],
        ignore_index=True,
    )
    plotted_events["event_index"] = np.arange(1, len(plotted_events) + 1)
    if not plotted_events.empty:
        ax_bonds.scatter(
            plotted_events["disp_um"],
            plotted_events["cumulative_broken_bonds"],
            s=22,
            color="#222222",
            zorder=4,
            linewidth=0.3,
            edgecolor="white",
        )
        for _, row in plotted_events.iterrows():
            ax_force.axvline(row["disp_um"], color="#A8364B", lw=0.65, ls=(0, (2, 2)), alpha=0.55, zorder=0)
        for _, row in plotted_events.iterrows():
            is_first_event = float(row["disp_um"]) < 30.0
            ax_bonds.annotate(
                f"+{int(row['new_broken_bonds'])}",
                xy=(row["disp_um"], row["cumulative_broken_bonds"]),
                xytext=(7 if is_first_event else 0, 12 if is_first_event else 8),
                textcoords="offset points",
                ha="left" if is_first_event else "center",
                va="bottom",
                fontsize=6.5,
                color="#222222",
                bbox=dict(boxstyle="round,pad=0.12", facecolor=wash, edgecolor="none", alpha=0.96),
            )

    ax_force.text(
        0.03,
        0.90,
        "pilot and third bed microcrack locally",
        transform=ax_force.transAxes,
        color=CASES[0].color,
        fontsize=7.0,
        fontweight="bold",
        ha="left",
    )
    ax_force.text(
        0.97,
        0.13,
        "one independent bed and weakened-bond audits remain intact",
        transform=ax_force.transAxes,
        color="0.30",
        fontsize=6.6,
        ha="right",
    )
    ax_force.set_xlabel("Top-wall displacement (µm)")
    ax_force.set_ylabel("Top-wall force (mN)")
    ax_force.set_xlim(0, 61.0)
    ax_force.set_title("macroscopic response separates intact and locally cracking beds", loc="left", fontweight="bold")
    ax_force.legend(
        loc="upper right",
        ncol=2,
        fontsize=5.8,
        handlelength=1.8,
        columnspacing=0.75,
    )
    ax_bonds.set_xlabel("Top-wall displacement (µm)")
    ax_bonds.set_ylabel("Event-localized broken bonds")
    ax_bonds.set_xlim(0, 61.0)
    ax_bonds.set_ylim(-0.5, 11.2)
    ax_bonds.set_yticks([0, 2, 4, 6, 8, 10])
    ax_bonds.text(
        0.05,
        0.13,
        "pilot: 5 bonds\nthird bed: 10 bonds\nintact bed/audits: 0",
        transform=ax_bonds.transAxes,
        ha="left",
        va="bottom",
        fontsize=6.1,
        fontweight="bold",
        color="0.15",
        bbox=dict(boxstyle="round,pad=0.16", facecolor=wash, edgecolor="none", alpha=0.96),
    )
    ax_bonds.set_title("fracture event boundary", loc="left", fontweight="bold")

    ax_edges.set_xlabel("Top-wall displacement (µm)")
    ax_edges.set_ylabel("Mother-pebble count / edge count")
    ax_edges.set_xlim(0, 61.0)
    ax_edges.set_ylim(0, 90)
    ax_edges.text(
        0.05,
        0.95,
        "circles: edges\nsquares: top-reachable",
        transform=ax_edges.transAxes,
        ha="left",
        va="top",
        fontsize=5.4,
        color="0.25",
        bbox=dict(boxstyle="round,pad=0.12", facecolor=wash, edgecolor="none", alpha=0.90),
    )
    ax_edges.text(
        0.04,
        0.08,
        "all corrected cases\nretain spanning graphs",
        transform=ax_edges.transAxes,
        ha="left",
        va="bottom",
        fontsize=6.3,
        color="#168A74",
        fontweight="bold",
    )
    ax_edges.set_title("native force-network topology", loc="left", fontweight="bold")

    metrics = [
        ("final_top_force_N", "Endpoint\nforce", "mN", 1000.0, "{:.0f}"),
        ("broken_bonds_at_endpoint", "Broken\nbonds", "bonds", 1.0, "{:.0f}"),
        ("final_inter_pebble_force_sum_N", "Inter-pebble\nforce sum", "N", 1.0, "{:.2f}"),
        ("final_bottom_reachable_from_top", "Bottom\nreachability", "pebbles", 1.0, "{:.0f}"),
    ]
    y_positions = np.arange(len(metrics))[::-1]
    offsets = {
        "Pilot": 0.28,
        "Independent": 0.14,
        "Delayed": 0.0,
        "0.5x audit": -0.14,
        "0.25x audit": -0.28,
    }
    case_lookup = {case.short: case for case in CASES}
    for metric_idx, (column, label, unit, scale, fmt) in enumerate(metrics):
        values = macro.set_index("case")[column].astype(float)
        max_value = values.max()
        denom = max_value if max_value > 0 else 1.0
        y_base = y_positions[metric_idx]
        for case in CASES:
            value = float(values.loc[case.short])
            normalized = value / denom
            y = y_base + offsets[case.short]
            ax_fingerprint.plot(
                [0, normalized],
                [y, y],
                color=case.color,
                lw=1.8,
                alpha=0.30,
                solid_capstyle="round",
            )
            ax_fingerprint.scatter(
                normalized,
                y,
                s=24,
                color=case.color,
                edgecolor="white",
                linewidth=0.45,
                zorder=3,
            )
            display_value = fmt.format(value * scale)
            if case.short in {"Pilot", "Independent", "Delayed"}:
                ax_fingerprint.text(
                    min(normalized + 0.035, 1.04),
                    y,
                    display_value,
                    ha="left",
                    va="center",
                    fontsize=5.7,
                    color=case.color,
                )
            if case.short in {"0.5x audit", "0.25x audit"} and column == "broken_bonds_at_endpoint":
                ax_fingerprint.text(
                    min(normalized + 0.035, 1.04),
                    y,
                    "0",
                    ha="left",
                    va="center",
                    fontsize=5.4,
                    color=case.color,
                )
        ax_fingerprint.text(
            -0.035,
            y_base,
            f"{label}\n({unit})",
            ha="right",
            va="center",
            fontsize=5.8,
            color="0.20",
        )
    ax_fingerprint.axvline(1.0, color="0.80", lw=0.6, zorder=0)
    ax_fingerprint.set_xlim(-0.02, 1.18)
    ax_fingerprint.set_ylim(-0.65, len(metrics) - 0.35)
    ax_fingerprint.set_xlabel("Normalized within each endpoint metric")
    ax_fingerprint.set_yticks([])
    ax_fingerprint.set_title("endpoint mechanism fingerprint", loc="left", fontweight="bold", fontsize=7.8)
    for label, ax in zip("abcd", [ax_force, ax_bonds, ax_edges, ax_fingerprint]):
        ax.text(-0.12, 1.07, label, transform=ax.transAxes, fontsize=9, fontweight="bold", va="top")

    fig.suptitle(
        "Corrected cases separate load-path connectivity from fracture onset",
        x=0.08,
        ha="left",
        y=0.992,
        fontsize=8.8,
        fontweight="bold",
    )
    fig.savefig(OUT_STEM.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(OUT_STEM.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(OUT_STEM.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(OUT_STEM.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    print(OUT_STEM.with_suffix(".png"))
    print(SOURCE_DATA)


if __name__ == "__main__":
    main()
