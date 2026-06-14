#!/usr/bin/env python3
"""Compare completed 1000-pebble 0.15 mm event sequences."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]

CASES = [
    {
        "label": "1000-bed A",
        "case": "PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable",
        "summary": ROOT / "tables/pb006_1000_0p15_restartable_summary.csv",
        "color": "#2F6F73",
    },
    {
        "label": "orientation replicate",
        "case": "PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable",
        "summary": ROOT / "tables/pb006_1000_seed01_orient02_0p15_summary.csv",
        "color": "#C46A30",
    },
    {
        "label": "1000-bed B",
        "case": "PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable",
        "summary": ROOT / "tables/pb006_1000_seed02_0p15_summary.csv",
        "color": "#4F7CAC",
    },
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in ("", None) else 0.0


def cumulative(values: list[float]) -> list[float]:
    total = 0.0
    out = []
    for value in values:
        total += value
        out.append(total)
    return out


def load_case(spec: dict[str, str | Path]) -> dict[str, object]:
    case = str(spec["case"])
    events = read_rows(ROOT / f"data/processed/{case}_breakage_events.csv")
    thermo = [
        row
        for row in read_rows(ROOT / f"data/processed/{case}_thermo.csv")
        if row.get("top_disp", "") not in ("", None) and row.get("top_forc", "") not in ("", None)
    ]
    summary = read_rows(Path(spec["summary"]))[0]

    event_disp = [as_float(row, "top_displacement_mm") for row in events]
    event_size = [as_float(row, "new_broken_bonds") for row in events]
    event_force = [as_float(row, "top_force_z_N") for row in events]
    pebble_ids = [int(float(row["pebble_id"])) for row in events]

    by_disp = defaultdict(float)
    for disp, size in zip(event_disp, event_size):
        by_disp[disp] += size
    burst_x = sorted(by_disp)
    burst_y = [by_disp[x] for x in burst_x]

    per_pebble = defaultdict(float)
    for pid, size in zip(pebble_ids, event_size):
        per_pebble[pid] += size

    unique_pebbles = sorted(per_pebble)
    waiting = [b - a for a, b in zip(event_disp, event_disp[1:])]
    final_disp = max([as_float(row, "top_disp") * 1e3 for row in thermo], default=0.0)
    last_event_disp = event_disp[-1] if event_disp else 0.0

    return {
        "label": spec["label"],
        "case": case,
        "color": spec["color"],
        "events": events,
        "thermo": thermo,
        "summary": summary,
        "event_disp": event_disp,
        "event_size": event_size,
        "event_force": event_force,
        "pebble_ids": pebble_ids,
        "burst_x": burst_x,
        "burst_y": burst_y,
        "burst_cum": cumulative(burst_y),
        "per_pebble": dict(per_pebble),
        "unique_pebbles": unique_pebbles,
        "waiting": waiting,
        "final_disp": final_disp,
        "last_event_disp": last_event_disp,
    }


def metrics_row(case_data: dict[str, object]) -> dict[str, object]:
    event_disp = case_data["event_disp"]
    event_size = case_data["event_size"]
    unique_pebbles = case_data["unique_pebbles"]
    waiting = case_data["waiting"]
    per_pebble = case_data["per_pebble"]
    summary = case_data["summary"]
    final_disp = float(case_data["final_disp"])
    last_event_disp = float(case_data["last_event_disp"])
    top_pid = max(unique_pebbles) if unique_pebbles else ""
    top_pid_damage = per_pebble.get(top_pid, 0.0) if top_pid != "" else 0.0
    total_damage = sum(event_size)

    return {
        "label": case_data["label"],
        "case": case_data["case"],
        "event_count": len(event_size),
        "total_broken_bonds": int(total_damage),
        "damaged_pebbles": len(unique_pebbles),
        "damaged_pebble_ids": ";".join(str(pid) for pid in unique_pebbles),
        "first_break_displacement_mm": event_disp[0] if event_disp else "",
        "last_event_displacement_mm": last_event_disp if event_disp else "",
        "post_last_event_quiet_window_mm": final_disp - last_event_disp if event_disp else "",
        "max_burst_bonds": int(max(event_size)) if event_size else 0,
        "mean_waiting_displacement_mm": sum(waiting) / len(waiting) if waiting else 0.0,
        "top_pebble_damage_fraction": top_pid_damage / total_damage if total_damage else 0.0,
        "top_bin_broken_bonds": summary.get("top_bin_broken_bonds", ""),
        "second_bin_broken_bonds": summary.get("second_bin_broken_bonds", ""),
    }


def write_metrics(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = [
        "label",
        "case",
        "event_count",
        "total_broken_bonds",
        "damaged_pebbles",
        "damaged_pebble_ids",
        "first_break_displacement_mm",
        "last_event_displacement_mm",
        "post_last_event_quiet_window_mm",
        "max_burst_bonds",
        "mean_waiting_displacement_mm",
        "top_pebble_damage_fraction",
        "top_bin_broken_bonds",
        "second_bin_broken_bonds",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--metrics-output",
        type=Path,
        default=ROOT / "tables/pb006_1000_orientation_sensitivity_metrics.csv",
    )
    parser.add_argument(
        "--out-prefix",
        type=Path,
        default=ROOT / "figures/pb006/pb006_1000_orientation_sensitivity",
    )
    args = parser.parse_args()

    data = [load_case(spec) for spec in CASES]
    metric_rows = [metrics_row(row) for row in data]
    write_metrics(args.metrics_output, metric_rows)

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

    fig, axes = plt.subplot_mosaic(
        [["a", "a"], ["b", "c"], ["d", "d"]],
        figsize=(7.2, 6.0),
        constrained_layout=True,
        gridspec_kw={"height_ratios": [1.05, 1.0, 0.95]},
    )

    ax = axes["a"]
    for row in data:
        thermo_disp = [as_float(item, "top_disp") * 1e3 for item in row["thermo"]]
        thermo_force = [as_float(item, "top_forc") for item in row["thermo"]]
        ax.plot(thermo_disp, thermo_force, color=row["color"], linewidth=1.35, label=row["label"])
        ax.scatter(row["event_disp"], row["event_force"], s=13, color=row["color"], edgecolor="white", linewidth=0.3)
    ax.axvspan(0.0675, 0.0950, color="#2F6F73", alpha=0.08, linewidth=0)
    ax.axvspan(0.0950, 0.1300, color="#8A8F98", alpha=0.08, linewidth=0)
    ax.axvspan(0.1300, 0.1500, color="#C46A30", alpha=0.08, linewidth=0)
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Top force (N)")
    ax.set_title("a  Load response and breakage times", loc="left", fontweight="bold")
    ax.legend(frameon=False, ncol=2, loc="upper left")

    ax = axes["b"]
    for row in data:
        ax.step(row["burst_x"], row["burst_cum"], where="post", color=row["color"], linewidth=1.4, label=row["label"])
        ax.scatter(row["burst_x"], row["burst_cum"], s=14, color=row["color"], zorder=3)
    ax.set_xlabel("Top displacement (mm)")
    ax.set_ylabel("Cumulative broken bonds")
    ax.set_title("b  Cumulative damage sequence", loc="left", fontweight="bold")
    ax.legend(frameon=False, loc="upper left")

    ax = axes["c"]
    labels = [row["label"] for row in data]
    damaged_pebbles = [len(row["unique_pebbles"]) for row in data]
    total_bonds = [sum(row["event_size"]) for row in data]
    x = range(len(labels))
    ax.bar([value - 0.18 for value in x], total_bonds, width=0.34, color="#30343F", label="broken bonds")
    ax2 = ax.twinx()
    ax2.bar([value + 0.18 for value in x], damaged_pebbles, width=0.34, color="#9A2F43", label="damaged pebbles")
    ax.set_xticks(list(x), labels)
    ax.set_ylabel("Broken bonds")
    ax2.set_ylabel("Damaged pebbles")
    ax.set_title("c  Final damage concentration", loc="left", fontweight="bold")
    ax.set_ylim(0, max(total_bonds) * 1.30)
    ax2.set_ylim(0, max(damaged_pebbles) * 1.80)
    for idx, value in enumerate(total_bonds):
        ax.text(idx - 0.18, value + max(total_bonds) * 0.04, str(int(value)), ha="center", va="bottom", fontsize=7)
    for idx, value in enumerate(damaged_pebbles):
        ax2.text(idx + 0.18, value + max(damaged_pebbles) * 0.08, str(int(value)), ha="center", va="bottom", fontsize=7)

    ax = axes["d"]
    for case_data, metrics in zip(data, metric_rows):
        first_break = float(metrics["first_break_displacement_mm"])
        total_bonds = float(metrics["total_broken_bonds"])
        damaged = float(metrics["damaged_pebbles"])
        ax.scatter(
            first_break,
            total_bonds,
            s=45 + 26 * damaged,
            color=case_data["color"],
            alpha=0.82,
            edgecolor="white",
            linewidth=0.5,
            label=case_data["label"],
        )
        ax.text(first_break + 0.0008, total_bonds + 6, case_data["label"], fontsize=7, color=case_data["color"])
    ax.set_xlabel("First-break displacement (mm)")
    ax.set_ylabel("Total broken bonds")
    ax.set_title("d  Damage severity versus onset", loc="left", fontweight="bold")
    ax.set_xlim(0.057, 0.077)
    ax.set_ylim(0, max(float(row["total_broken_bonds"]) for row in metric_rows) * 1.18)
    ax.text(0.058, ax.get_ylim()[1] * 0.88, "marker area scales with\ndamaged-pebble count", fontsize=7, color="#4E4A45")

    for ax in axes.values():
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.tick_params(direction="out", length=3)
    ax2.spines["top"].set_visible(False)
    ax2.tick_params(direction="out", length=3)

    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    for suffix in [".svg", ".pdf", ".png", ".tiff"]:
        dpi = 600 if suffix in [".png", ".tiff"] else None
        fig.savefig(args.out_prefix.with_suffix(suffix), dpi=dpi)

    print(args.metrics_output)
    print(args.out_prefix)


if __name__ == "__main__":
    main()
