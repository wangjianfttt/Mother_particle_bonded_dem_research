#!/usr/bin/env python3
"""Create a manuscript figure summarizing single-pebble calibration evidence."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def f(row: dict[str, str], key: str) -> float | None:
    value = row.get(key, "")
    return float(value) if value not in ("", None) else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--targets",
        type=Path,
        default=ROOT / "tables/single_pebble_calibration_target_evidence_summary.csv",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=ROOT / "tables/single_pebble_model_calibration_matrix.csv",
    )
    parser.add_argument(
        "--orientation",
        type=Path,
        default=ROOT / "tables/sp002_cal1_orientation_summary.csv",
    )
    parser.add_argument(
        "--multiplier",
        type=Path,
        default=ROOT / "tables/sp002_strength_multiplier_validation.csv",
    )
    parser.add_argument(
        "--weibull",
        type=Path,
        default=ROOT / "tables/sp002_weibull_ensemble_completed_summary.csv",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=ROOT / "figures/sp002/single_pebble_calibration_evidence",
    )
    args = parser.parse_args()

    target_rows = rows(args.targets)
    model_rows = rows(args.model)
    orient_rows = rows(args.orientation)
    mult_rows = rows(args.multiplier)
    wb_rows = rows(args.weibull)
    slow_summary_path = ROOT / "data/processed/SP-002-CAL1-slow0p05ms-0p3mm_summary.csv"
    slow_fragments_path = ROOT / "data/processed/SP-002-CAL1-slow0p05ms-0p3mm_fragments.csv"
    matched_summary_path = ROOT / "data/processed/SP-002-CAL1-matched0p10ms-0p3mm_summary.csv"
    matched_fragments_path = ROOT / "data/processed/SP-002-CAL1-matched0p10ms-0p3mm_fragments.csv"
    x_slow_summary_path = ROOT / "data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_summary.csv"
    x_slow_fragments_path = ROOT / "data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_fragments.csv"
    slow_summary = {row["metric"]: row["value"] for row in rows(slow_summary_path)} if slow_summary_path.exists() else None
    slow_fragments = rows(slow_fragments_path)[-1] if slow_fragments_path.exists() else None
    matched_summary = {row["metric"]: row["value"] for row in rows(matched_summary_path)} if matched_summary_path.exists() else None
    matched_fragments = rows(matched_fragments_path)[-1] if matched_fragments_path.exists() else None
    x_slow_summary = {row["metric"]: row["value"] for row in rows(x_slow_summary_path)} if x_slow_summary_path.exists() else None
    x_slow_fragments = rows(x_slow_fragments_path)[-1] if x_slow_fragments_path.exists() else None

    cal1 = next(row for row in model_rows if row["case_id"] == "SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm")
    homogeneous = next(row for row in model_rows if row["case_id"] == "SP-002-calib-kn1e14-120MPa-0p1ms")

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
    fig, axes = plt.subplots(1, 3, figsize=(7.1, 3.45), constrained_layout=True)

    ax = axes[0]
    for row in target_rows:
        force = f(row, "mean_crush_load_N")
        dia = f(row, "diameter_mm")
        if force is None or dia is None:
            continue
        err = f(row, "std_crush_load_N")
        cls = row["evidence_class"]
        if cls == "verified tabulated anchor":
            color, marker, label = "#2F6F73", "o", "Zhao verified"
        elif cls == "digitized size-effect anchor":
            color, marker, label = "#C46A30", "s", "Annabattula digitized"
        else:
            color, marker, label = "#6B5EA8", "^", "near-size/context"
        ax.errorbar(
            dia,
            force,
            yerr=err,
            fmt=marker,
            markersize=4.5,
            color=color,
            ecolor=color,
            capsize=2 if err else 0,
            label=label,
            alpha=0.92,
        )
    ax.scatter([1.0], [f(cal1, "peak_top_force_N")], marker="*", s=90, color="#111111", label="selected template")
    ax.axhspan(15, 22, color="#E7E1CF", alpha=0.55, zorder=-1)
    ax.set_xlabel("Pebble diameter (mm)")
    ax.set_ylabel("Crush load / peak force (N)")
    ax.set_title("a  Literature target window", loc="left", fontweight="bold")
    ax.set_xlim(0.18, 1.62)
    ax.set_ylim(0, 32)
    handles, labels = ax.get_legend_handles_labels()
    seen = {}
    for h, label in zip(handles, labels):
        seen.setdefault(label, h)
    ax.legend(seen.values(), seen.keys(), frameon=False, fontsize=6.5, loc="upper left")

    ax = axes[1]
    names = ["homogeneous", "selected template"]
    if x_slow_summary:
        names.append("x-normal 0.05 m/s")
    if matched_summary:
        names.append("orthogonal 0.10 m/s")
    if slow_summary:
        names.append("orthogonal 0.05 m/s")
    names += ["orientation pilot", "strength multiplier", "Weibull trial"]
    values = [
        [f(homogeneous, "peak_top_force_N")],
        [f(cal1, "peak_top_force_N")],
    ]
    colors = ["#8093A5", "#111111"]
    if x_slow_summary:
        values.append([float(x_slow_summary["peak_top_force_N"])])
        colors.append("#2F6F73")
    if matched_summary:
        values.append([float(matched_summary["peak_top_force_N"])])
        colors.append("#4C78A8")
    if slow_summary:
        values.append([float(slow_summary["peak_top_force_N"])])
        colors.append("#9A2F43")
    values += [
        [f(row, "peak_top_force_N") for row in orient_rows],
        [f(row, "peak_top_force_N") for row in mult_rows],
        [f(row, "peak_top_force_N") for row in wb_rows],
    ]
    colors += ["#6B5EA8", "#C46A30", "#5B8E7D"]
    y = list(range(len(names)))
    for i, vals in enumerate(values):
        ax.scatter(vals, [i] * len(vals), color=colors[i], s=24, alpha=0.9)
        if len(vals) > 1:
            ax.hlines(i, min(vals), max(vals), color=colors[i], linewidth=1.2, alpha=0.7)
    ax.axvspan(15, 22, color="#E7E1CF", alpha=0.55, zorder=-1)
    ax.set_yticks(y, names)
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=6.5)
    ax.set_xlabel("Peak top force (N)")
    ax.set_title("b  Model load evidence", loc="left", fontweight="bold")
    ax.set_xlim(8, 31)

    ax = axes[2]
    labels = ["homogeneous", "selected template"]
    if x_slow_fragments:
        labels.append("x-normal 0.05 m/s")
    if matched_fragments:
        labels.append("orthogonal 0.10 m/s")
    if slow_fragments:
        labels.append("orthogonal 0.05 m/s")
    labels += ["orientation pilot", "strength multiplier", "Weibull trial"]
    largest = [
        f(homogeneous, "largest_fragment_particles"),
        f(cal1, "largest_fragment_particles"),
    ]
    second = [
        f(homogeneous, "second_fragment_particles"),
        f(cal1, "second_fragment_particles"),
    ]
    if x_slow_fragments:
        largest.append(float(x_slow_fragments["largest_fragment_particles"]))
        second.append(float(x_slow_fragments["second_fragment_particles"]))
    if matched_fragments:
        largest.append(float(matched_fragments["largest_fragment_particles"]))
        second.append(float(matched_fragments["second_fragment_particles"]))
    if slow_fragments:
        largest.append(float(slow_fragments["largest_fragment_particles"]))
        second.append(float(slow_fragments["second_fragment_particles"]))
    largest += [
        max(f(row, "largest_fragment_particles") for row in orient_rows),
        max(f(row, "largest_fragment_particles") for row in mult_rows),
        max(f(row, "largest_fragment_particles") for row in wb_rows),
    ]
    second += [
        max(f(row, "second_fragment_particles") for row in orient_rows),
        max(f(row, "second_fragment_particles") for row in mult_rows),
        max(f(row, "second_fragment_particles") for row in wb_rows),
    ]
    y = list(range(len(labels)))
    ax.barh(y, largest, color="#2F6F73", height=0.62, label="Largest")
    ax.barh(y, second, left=largest, color="#D08C60", height=0.62, label="Second")
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=6.5)
    ax.set_xlabel("Particles in two largest fragments")
    ax.set_title("c  Fragment-mode filter", loc="left", fontweight="bold")
    ax.axvline(500, color="#333333", linewidth=0.8, linestyle=":")
    ax.set_xlim(0, 540)
    ax.legend(frameon=False, fontsize=7, loc="lower right")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=3)

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in [".svg", ".pdf", ".png", ".tiff"]:
        dpi = 600 if suffix in [".png", ".tiff"] else None
        fig.savefig(args.out_prefix.with_suffix(suffix), dpi=dpi)


if __name__ == "__main__":
    main()
