#!/usr/bin/env python3
"""Plot selected-template force-displacement overlays against literature anchors."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


CASES = [
    (
        "reference template, 0.10 m/s",
        ROOT / "data/processed/SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm_thermo.csv",
        "#111111",
    ),
    (
        "same template, 0.05 m/s",
        ROOT / "data/processed/SP-002-CAL1-x-slow0p05ms-0p3mm_thermo.csv",
        "#2F6F73",
    ),
    (
        "same template, 0.03 m/s to 0.18 mm",
        ROOT / "data/processed/SP-002-CAL1-x-slow0p03ms-0p18mm_thermo.csv",
        "#7A4EAB",
    ),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def number(row: dict[str, str], key: str) -> float:
    return float(row[key])


def curve(rows: list[dict[str, str]]) -> tuple[list[float], list[float], list[int]]:
    displacement = [number(row, "top_disp") * 1e3 for row in rows]
    force = [abs(number(row, "top_forc")) for row in rows]
    broken = [int(float(row["bond_bro"])) for row in rows]
    return displacement, force, broken


def case_metrics(label: str, rows: list[dict[str, str]]) -> dict[str, str]:
    displacement, force, broken = curve(rows)
    peak_index = max(range(len(force)), key=force.__getitem__)
    first_break_index = next((i for i, value in enumerate(broken) if value > 0), None)
    return {
        "case": label,
        "peak_force_N": f"{force[peak_index]:.6g}",
        "peak_displacement_mm": f"{displacement[peak_index]:.6g}",
        "first_break_displacement_mm": ""
        if first_break_index is None
        else f"{displacement[first_break_index]:.6g}",
        "final_broken_bonds": str(sum(broken)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=ROOT / "figures/sp002/sp002_force_displacement_overlay",
    )
    parser.add_argument(
        "--metrics-output",
        type=Path,
        default=ROOT / "tables/sp002_force_displacement_overlay_metrics.csv",
    )
    args = parser.parse_args()

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

    fig, ax = plt.subplots(figsize=(3.55, 2.65), constrained_layout=True)
    metrics = []

    ax.axhspan(15, 22, color="#E7E1CF", alpha=0.65, zorder=-2, label="1 mm load target window")
    ax.scatter(
        [0.04],
        [14.0],
        marker="s",
        s=24,
        color="#C46A30",
        zorder=3,
        label="near-size literature anchor",
    )

    for label, path, color in CASES:
        if not path.exists():
            continue
        rows = read_rows(path)
        displacement, force, broken = curve(rows)
        linestyle = "--" if "0.03" in label else "-"
        ax.plot(displacement, force, color=color, linewidth=1.45, linestyle=linestyle, label=label)
        metrics.append(case_metrics(label, rows))
        first_break_index = next((i for i, value in enumerate(broken) if value > 0), None)
        if first_break_index is not None:
            ax.scatter(
                [displacement[first_break_index]],
                [force[first_break_index]],
                s=22,
                facecolor="white",
                edgecolor=color,
                linewidth=1.0,
                zorder=4,
            )
            ax.vlines(
                displacement[first_break_index],
                0,
                force[first_break_index],
                color=color,
                linewidth=0.8,
                alpha=0.45,
            )

    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Compressive top force (N)")
    ax.set_xlim(0, 0.30)
    ax.set_ylim(0, 32)
    ax.set_title("Single-pebble calibration check", loc="left", fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=3)
    ax.legend(frameon=False, fontsize=6.5, loc="upper right")

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in [".svg", ".pdf", ".png", ".tiff"]:
        dpi = 600 if suffix in [".png", ".tiff"] else None
        fig.savefig(args.out_prefix.with_suffix(suffix), dpi=dpi)

    args.metrics_output.parent.mkdir(parents=True, exist_ok=True)
    with args.metrics_output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(metrics[0]))
        writer.writeheader()
        writer.writerows(metrics)
    print(args.out_prefix)
    print(args.metrics_output)


if __name__ == "__main__":
    main()
