#!/usr/bin/env python3
"""Summarize subparticle-resolution and loading-rate validation."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data/processed"

RESOLUTION_CASES = [
    (250, "SP-RES-250"),
    (500, "SP-RES-500"),
    (1000, "SP-RES-1000"),
]
RATE_CASES = [
    (0.10, "SP-RES-500"),
    (0.05, "SP-RATE-500-0p05-FULL"),
    (0.03, "SP-RATE-500-0p03-FULL"),
]


def read_rows(path: Path) -> list[dict[str, float]]:
    with path.open(newline="") as handle:
        return [
            {key: float(value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def read_summary(path: Path) -> dict[str, str]:
    with path.open(newline="") as handle:
        return {row["metric"]: row["value"] for row in csv.DictReader(handle)}


def final_fragments(path: Path, particle_count: int) -> tuple[float, float, int]:
    rows = read_rows(path)
    final = max(rows, key=lambda row: row["timestep"])
    return (
        final["largest_fragment_particles"] / particle_count,
        final["second_fragment_particles"] / particle_count,
        int(final["fragment_count"]),
    )


def curve(case_id: str) -> tuple[list[float], list[float]]:
    rows = read_rows(PROCESSED / f"{case_id}_thermo.csv")
    return (
        [row["top_disp"] * 1.0e3 for row in rows],
        [abs(row["top_forc"]) for row in rows],
    )


def metrics(case_id: str, particle_count: int) -> dict[str, float | int | str]:
    summary = read_summary(PROCESSED / f"{case_id}_summary.csv")
    largest, second, fragment_count = final_fragments(
        PROCESSED / f"{case_id}_fragments.csv", particle_count
    )
    initial_bonds = max(
        row["bond_int"] for row in read_rows(PROCESSED / f"{case_id}_thermo.csv")
    )
    return {
        "case": case_id,
        "subparticles": particle_count,
        "initial_bonds": int(initial_bonds),
        "peak_top_force_N": float(summary["peak_top_force_N"]),
        "peak_displacement_mm": float(summary["peak_top_force_displacement_mm"]),
        "first_break_displacement_mm": float(summary["first_break_displacement_mm"]),
        "final_broken_bonds": int(float(summary["final_broken_bonds"])),
        "final_fragment_count": fragment_count,
        "largest_fragment_fraction": largest,
        "second_fragment_fraction": second,
    }


def main() -> None:
    required = [
        PROCESSED / f"{case_id}_{suffix}.csv"
        for _, case_id in RESOLUTION_CASES
        for suffix in ("thermo", "summary", "fragments")
    ]
    required += [
        PROCESSED / f"{case_id}_{suffix}.csv"
        for _, case_id in RATE_CASES
        for suffix in ("thermo", "summary", "fragments")
    ]
    missing = [path for path in required if not path.exists()]
    if missing:
        raise SystemExit("Missing validation outputs:\n" + "\n".join(map(str, missing)))

    resolution = [metrics(case_id, count) for count, case_id in RESOLUTION_CASES]
    rate = []
    for velocity, case_id in RATE_CASES:
        row = metrics(case_id, 500)
        row["loading_velocity_m_per_s"] = velocity
        rate.append(row)

    table_dir = ROOT / "tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in (
        ("jnm_single_pebble_resolution_summary.csv", resolution),
        ("jnm_single_pebble_rate_summary.csv", rate),
    ):
        with (table_dir / name).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.labelsize": 8,
            "legend.fontsize": 7,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "axes.linewidth": 0.8,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    colors = ["#0072B2", "#D55E00", "#009E73"]
    linestyles = ["-", "--", "-."]
    markers = ["o", "s", "^"]

    fig, axes = plt.subplots(2, 2, figsize=(7.15, 5.25))
    for index, (count, case_id) in enumerate(RESOLUTION_CASES):
        x, y = curve(case_id)
        axes[0, 0].plot(
            x,
            y,
            color=colors[index],
            linestyle=linestyles[index],
            linewidth=1.1,
            label=f"{count} subparticles",
        )

    counts = [int(row["subparticles"]) for row in resolution]
    reference = resolution[1]
    peak_ratio = [
        float(row["peak_top_force_N"]) / float(reference["peak_top_force_N"])
        for row in resolution
    ]
    break_ratio = [
        float(row["first_break_displacement_mm"])
        / float(reference["first_break_displacement_mm"])
        for row in resolution
    ]
    axes[0, 1].plot(
        counts,
        peak_ratio,
        color=colors[0],
        marker="o",
        linewidth=1.1,
        label="Peak load / 500-case value",
    )
    axes[0, 1].plot(
        counts,
        break_ratio,
        color=colors[1],
        marker="s",
        linestyle="--",
        linewidth=1.1,
        label="First-break displacement / 500-case value",
    )
    axes[0, 1].axhline(1.0, color="#777777", linewidth=0.7, linestyle=":")

    for index, (velocity, case_id) in enumerate(RATE_CASES):
        x, y = curve(case_id)
        axes[1, 0].plot(
            x,
            y,
            color=colors[index],
            linestyle=linestyles[index],
            linewidth=1.1,
            label=f"{velocity:.2f} m s$^{{-1}}$",
        )

    rate_sorted = sorted(rate, key=lambda row: float(row["loading_velocity_m_per_s"]))
    velocities = [float(row["loading_velocity_m_per_s"]) for row in rate_sorted]
    largest = [float(row["largest_fragment_fraction"]) for row in rate_sorted]
    second = [float(row["second_fragment_fraction"]) for row in rate_sorted]
    axes[1, 1].plot(
        velocities,
        largest,
        color=colors[0],
        marker="o",
        linewidth=1.1,
        label="Largest fragment",
    )
    axes[1, 1].plot(
        velocities,
        second,
        color=colors[1],
        marker="s",
        linestyle="--",
        linewidth=1.1,
        label="Second-largest fragment",
    )

    axes[0, 0].set_xlabel("Top-plate displacement (mm)")
    axes[0, 0].set_ylabel("Top-plate force (N)")
    axes[0, 1].set_xlabel("Subparticles per mother pebble")
    axes[0, 1].set_ylabel("Metric normalized by 500-case value")
    axes[1, 0].set_xlabel("Top-plate displacement (mm)")
    axes[1, 0].set_ylabel("Top-plate force (N)")
    axes[1, 1].set_xlabel("Loading velocity (m s$^{-1}$)")
    axes[1, 1].set_ylabel("Final fragment fraction")
    axes[1, 1].set_xlim(0.02, 0.11)
    axes[1, 1].set_ylim(0, 0.55)

    for label, axis in zip("abcd", axes.flat):
        axis.text(0.02, 0.96, label, transform=axis.transAxes, weight="bold", va="top")
        axis.grid(False)
    for axis in axes.flat:
        axis.legend(frameon=False, loc="best")

    fig.subplots_adjust(
        left=0.085, right=0.985, bottom=0.10, top=0.98, wspace=0.30, hspace=0.30
    )
    figure_base = ROOT / "figures/sp002/jnm_single_pebble_validation"
    for suffix in ("pdf", "svg", "png", "tiff"):
        kwargs = {"dpi": 600} if suffix in {"png", "tiff"} else {}
        fig.savefig(figure_base.with_suffix(f".{suffix}"), bbox_inches="tight", **kwargs)
    plt.close(fig)

    print(table_dir / "jnm_single_pebble_resolution_summary.csv")
    print(table_dir / "jnm_single_pebble_rate_summary.csv")
    print(figure_base.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
