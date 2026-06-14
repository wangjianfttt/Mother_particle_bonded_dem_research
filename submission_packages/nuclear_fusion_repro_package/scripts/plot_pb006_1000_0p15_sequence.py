#!/usr/bin/env python3
"""Plot the completed 1000-pebble 0.15 mm restartable event sequence."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
CASE = "PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in ("", None) else 0.0


def cumulative(values: list[float]) -> list[float]:
    total = 0.0
    out = []
    for value in values:
        total += value
        out.append(total)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--events",
        type=Path,
        default=ROOT / f"data/processed/{CASE}_breakage_events.csv",
    )
    parser.add_argument(
        "--thermo",
        type=Path,
        default=ROOT / f"data/processed/{CASE}_thermo.csv",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=ROOT / "tables/pb006_1000_0p15_restartable_summary.csv",
    )
    parser.add_argument(
        "--height",
        type=Path,
        default=ROOT / f"data/processed/{CASE}_height_summary.csv",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=ROOT / "figures/pb006/pb006_1000_0p15_three_stage_sequence",
    )
    args = parser.parse_args()

    events = read_rows(args.events)
    thermo = [
        row
        for row in read_rows(args.thermo)
        if row.get("top_disp", "") not in ("", None) and row.get("top_forc", "") not in ("", None)
    ]
    summary = read_rows(args.summary)[0]
    height_rows = read_rows(args.height)

    if not events:
        raise SystemExit("No restartable 0.15 mm events found")

    event_disp = [f(row, "top_displacement_mm") for row in events]
    event_size = [f(row, "new_broken_bonds") for row in events]
    event_cum = cumulative(event_size)
    pebble_ids = [int(float(row["pebble_id"])) for row in events]
    ranks = [1000 - pid + 1 for pid in pebble_ids]

    disp_to_broken = defaultdict(float)
    for row in events:
        disp_to_broken[f(row, "top_displacement_mm")] += f(row, "new_broken_bonds")
    burst_x = sorted(disp_to_broken)
    burst_y = [disp_to_broken[x] for x in burst_x]
    burst_cum = cumulative(burst_y)

    thermo_disp = [f(row, "top_disp") * 1e3 for row in thermo]
    thermo_force = [f(row, "top_forc") for row in thermo]
    top_bin_broken = int(float(summary["top_bin_broken_bonds"]))
    second_bin_broken = int(float(summary["second_bin_broken_bonds"]))
    damaged_pebbles = int(float(summary["broken_pebbles"]))
    top_bin_count = int(float(summary["top_bin_count"]))
    bed_height = float(summary["bed_height_mm"])

    colors = {
        1000: "#2F6F73",
        980: "#C46A30",
        961: "#6B5EA8",
    }

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

    mosaic = [["a", "a", "b"], ["c", "d", "e"], ["c", "f", "f"]]
    fig, axes = plt.subplot_mosaic(
        mosaic,
        figsize=(7.2, 5.8),
        constrained_layout=True,
        gridspec_kw={"height_ratios": [1.05, 1.0, 0.82]},
    )

    ax = axes["a"]
    ax.plot(thermo_disp, thermo_force, color="#30343F", linewidth=1.2)
    ax.scatter(event_disp, [f(row, "top_force_z_N") for row in events], s=12, color="#9A2F43", zorder=3)
    ax.axvspan(0.0675, 0.0950, color="#2F6F73", alpha=0.12, linewidth=0)
    ax.axvspan(0.0950, 0.1300, color="#8A8F98", alpha=0.10, linewidth=0)
    ax.axvspan(0.1325, 0.1500, color="#C46A30", alpha=0.12, linewidth=0)
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Top force (N)")
    ax.set_title("a  Load response and event windows", loc="left", fontweight="bold")
    ax.text(0.071, max(thermo_force) * 0.18, "onset", color="#2F6F73", fontsize=7)
    ax.text(0.104, max(thermo_force) * 0.18, "quiet plateau", color="#5D6470", fontsize=7)
    ax.text(0.134, max(thermo_force) * 0.18, "late burst", color="#C46A30", fontsize=7)

    ax = axes["b"]
    ax.bar(burst_x, burst_y, width=0.0012, color="#9A2F43", alpha=0.85)
    ax.step(burst_x, burst_cum, where="post", color="#30343F", linewidth=1.2)
    ax.scatter(burst_x, burst_cum, s=14, color="#30343F", zorder=3)
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Broken bonds")
    ax.set_title("b  Burst size and cumulative damage", loc="left", fontweight="bold")
    ax.text(0.096, max(burst_cum) * 0.58, "no new bond loss\n0.095-0.130 mm", fontsize=7, color="#5D6470")

    ax = axes["c"]
    for pid in sorted(set(pebble_ids), reverse=True):
        rows = [i for i, value in enumerate(pebble_ids) if value == pid]
        ax.scatter(
            [event_disp[i] for i in rows],
            [ranks[i] for i in rows],
            s=[18 + 1.8 * event_size[i] for i in rows],
            color=colors.get(pid, "#555555"),
            alpha=0.85,
            label=f"pebble {pid}",
        )
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Rank from highest id")
    ax.set_title("c  Mother-pebble event sequence", loc="left", fontweight="bold")
    ax.set_ylim(45, 0)
    ax.legend(frameon=False, fontsize=7, loc="lower left")

    ax = axes["d"]
    per_pebble = defaultdict(float)
    for pid, size in zip(pebble_ids, event_size):
        per_pebble[pid] += size
    ordered = sorted(per_pebble, key=lambda pid: (-per_pebble[pid], pid))
    bars = ax.bar(
        [str(pid) for pid in ordered],
        [per_pebble[pid] for pid in ordered],
        color=[colors.get(pid, "#555555") for pid in ordered],
    )
    for bar, pid in zip(bars, ordered):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.2,
            f"{int(per_pebble[pid])}",
            ha="center",
            va="bottom",
            fontsize=7,
        )
    ax.set_xlabel("Mother pebble")
    ax.set_ylabel("Broken bonds")
    ax.set_title("d  Final damaged pebbles at 0.15 mm", loc="left", fontweight="bold")
    ax.text(
        0.02,
        0.94,
        f"{int(float(summary['localized_events']))} events, "
        f"{int(float(summary['localized_broken_bonds']))} broken bonds, "
        f"{int(float(summary['broken_pebbles']))} pebbles",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=7,
    )
    ax.set_ylim(0, max(per_pebble.values()) * 1.24)

    ax = axes["e"]
    stage_labels = ["Onset", "Quiet", "Late\nburst"]
    stage_bonds = [53, 0, 45]
    stage_events = [6, 0, 9]
    x_stage = range(len(stage_labels))
    ax.bar(x_stage, stage_bonds, color=["#2F6F73", "#8A8F98", "#C46A30"], width=0.58, label="broken bonds")
    ax2 = ax.twinx()
    ax2.plot(list(x_stage), stage_events, color="#30343F", marker="o", linewidth=1.2, label="events")
    for idx, value in enumerate(stage_bonds):
        ax.text(idx, value + 3, str(value), ha="center", va="bottom", fontsize=7)
    for idx, value in enumerate(stage_events):
        ax2.text(idx, value + 0.55, str(value), ha="center", va="bottom", fontsize=7, color="#30343F")
    ax.set_xticks(list(x_stage), stage_labels)
    ax.set_ylabel("Broken bonds")
    ax2.set_ylabel("Events")
    ax.set_title("e  Stage-window damage", loc="left", fontweight="bold")
    ax.set_ylim(0, 62)
    ax2.set_ylim(0, 11)
    ax2.spines["top"].set_visible(False)
    ax2.tick_params(direction="out", length=3)

    ax = axes["f"]
    labels = ["Top bin\nbroken bonds", "Second bin\nbroken bonds", "Damaged\npebbles", "Top-bin\npebbles"]
    values = [top_bin_broken, second_bin_broken, damaged_pebbles, top_bin_count]
    bar_colors = ["#2F6F73", "#8A8F98", "#C46A30", "#6B5EA8"]
    bars = ax.bar(labels, values, color=bar_colors, width=0.58)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.03, str(value), ha="center", va="bottom", fontsize=7)
    ax.set_ylabel("Count")
    ax.set_title("f  Top-layer localization", loc="left", fontweight="bold")
    ax.text(
        0.98,
        0.90,
        f"bed height {bed_height:.3f} mm",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=7,
        color="#30343F",
    )
    ax.set_ylim(0, max(values) * 1.30)

    for ax in axes.values():
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=3)

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in [".svg", ".pdf", ".png", ".tiff"]:
        dpi = 600 if suffix in [".png", ".tiff"] else None
        fig.savefig(args.out_prefix.with_suffix(suffix), dpi=dpi)

    print(args.out_prefix)


if __name__ == "__main__":
    main()
