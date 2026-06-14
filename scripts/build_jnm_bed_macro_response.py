#!/usr/bin/env python3
"""Build a JNM-ready macro-response figure for the three 500-pebble beds."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


ROOT = Path(__file__).resolve().parents[1]
AREA_M2 = (11.0e-3) ** 2

CASES = [
    {
        "label": "Bed A",
        "height_mm": 3.99437,
        "thermo": ROOT
        / "data/processed/PB-006-bonded-randompack-500-prod-0p20mm-primitivewall_thermo.csv",
        "events": ROOT
        / "data/processed/PB-006-bonded-randompack-500-prod-0p20mm-primitivewall_breakage_events.csv",
    },
    {
        "label": "Bed B",
        "height_mm": 4.08026,
        "thermo": ROOT
        / "data/processed/PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall_thermo.csv",
        "events": ROOT
        / "data/processed/PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall_breakage_events.csv",
    },
    {
        "label": "Bed C",
        "height_mm": 3.81530,
        "thermo": ROOT
        / "data/processed/PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall_thermo.csv",
        "events": ROOT
        / "data/processed/PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall_breakage_events.csv",
    },
]


def read_numeric_rows(path: Path, required: tuple[str, ...]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                parsed = {name: float(row[name]) for name in required}
            except (KeyError, TypeError, ValueError):
                continue
            rows.append(parsed)
    return rows


def pressure_mpa(force_n: float) -> float:
    return abs(force_n) / AREA_M2 / 1.0e6


def main() -> None:
    out_series = ROOT / "tables/jnm_bed_macro_response_series.csv"
    out_summary = ROOT / "tables/jnm_bed_macro_response_summary.csv"
    figure_base = ROOT / "figures/pb006/jnm_bed_macro_response"
    out_series.parent.mkdir(parents=True, exist_ok=True)
    figure_base.parent.mkdir(parents=True, exist_ok=True)

    colors = ["#0072B2", "#D55E00", "#009E73"]
    linestyles = ["-", "--", "-."]
    markers = ["o", "s", "^"]

    series_rows: list[dict[str, float | str]] = []
    summary_rows: list[dict[str, float | str | int]] = []
    plot_data = []

    for case in CASES:
        thermo = read_numeric_rows(
            case["thermo"], ("Step", "top_disp", "top_forc", "KinEng")
        )
        thermo = [
            row
            for row in thermo
            if row["top_disp"] >= 0.0 and row["top_disp"] <= 2.01e-4
        ]
        by_step = {int(row["Step"]): row for row in thermo}
        thermo = [by_step[key] for key in sorted(by_step)]

        events = read_numeric_rows(
            case["events"],
            ("timestep", "top_displacement_mm", "new_broken_bonds", "pebble_id"),
        )
        increments: dict[float, int] = {}
        damaged_pebbles: set[int] = set()
        for event in events:
            displacement = event["top_displacement_mm"]
            increments[displacement] = increments.get(displacement, 0) + int(
                event["new_broken_bonds"]
            )
            damaged_pebbles.add(int(event["pebble_id"]))

        event_displacements = sorted(increments)
        cumulative = 0
        damage_curve = [(0.0, 0)]
        for displacement in event_displacements:
            cumulative += increments[displacement]
            damage_curve.append((displacement, cumulative))

        response = []
        for row in thermo:
            displacement_mm = row["top_disp"] * 1.0e3
            strain_pct = displacement_mm / float(case["height_mm"]) * 100.0
            pressure = pressure_mpa(row["top_forc"])
            localized_bonds = sum(
                increment
                for displacement, increment in increments.items()
                if displacement <= displacement_mm + 1.0e-9
            )
            response.append((displacement_mm, strain_pct, pressure, localized_bonds))
            series_rows.append(
                {
                    "case": case["label"],
                    "displacement_mm": displacement_mm,
                    "engineering_strain_percent": strain_pct,
                    "top_pressure_MPa": pressure,
                    "kinetic_energy_J": row["KinEng"],
                    "localized_cumulative_broken_bonds": localized_bonds,
                }
            )

        first_break_mm = event_displacements[0]
        first_break_strain = first_break_mm / float(case["height_mm"]) * 100.0
        nearest = min(response, key=lambda item: abs(item[0] - first_break_mm))
        summary_rows.append(
            {
                "case": case["label"],
                "settled_bed_height_mm": case["height_mm"],
                "first_break_displacement_mm": first_break_mm,
                "first_break_engineering_strain_percent": first_break_strain,
                "pressure_near_first_break_MPa": nearest[2],
                "endpoint_pressure_MPa": response[-1][2],
                "localized_broken_bonds": cumulative,
                "damaged_mother_pebbles": len(damaged_pebbles),
            }
        )
        plot_data.append((case, response, damage_curve))

    with out_series.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=series_rows[0].keys())
        writer.writeheader()
        writer.writerows(series_rows)

    with out_summary.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8,
            "axes.labelsize": 8,
            "axes.titlesize": 8,
            "legend.fontsize": 7,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "axes.linewidth": 0.8,
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.top": True,
            "ytick.right": True,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(3.54, 4.25),
        sharex=True,
        gridspec_kw={"height_ratios": [1.18, 1.0], "hspace": 0.08},
    )

    for index, (case, response, damage_curve) in enumerate(plot_data):
        strain = [item[1] for item in response]
        pressure = [item[2] for item in response]
        axes[0].plot(
            strain,
            pressure,
            color=colors[index],
            linestyle=linestyles[index],
            marker=markers[index],
            markersize=2.8,
            linewidth=1.15,
            label=case["label"],
        )

        damage_strain = [
            displacement / float(case["height_mm"]) * 100.0
            for displacement, _ in damage_curve
        ]
        damage = [value for _, value in damage_curve]
        axes[1].step(
            damage_strain,
            damage,
            where="post",
            color=colors[index],
            linestyle=linestyles[index],
            linewidth=1.2,
        )
        axes[1].scatter(
            damage_strain[1:],
            damage[1:],
            color=colors[index],
            marker=markers[index],
            s=10,
            linewidths=0.4,
            edgecolors="white",
            zorder=3,
        )

    axes[0].set_ylabel("Top-plate pressure (MPa)")
    axes[1].set_ylabel("Localized broken bonds")
    axes[1].set_xlabel("Engineering compression strain (%)")
    axes[0].legend(
        frameon=False, loc="upper left", bbox_to_anchor=(0.10, 1.0), ncol=1
    )
    axes[0].text(0.02, 0.95, "a", transform=axes[0].transAxes, weight="bold", va="top")
    axes[1].text(0.02, 0.95, "b", transform=axes[1].transAxes, weight="bold", va="top")
    axes[0].set_ylim(bottom=0)
    axes[1].set_ylim(bottom=0)
    axes[1].xaxis.set_major_locator(MaxNLocator(5))
    axes[0].yaxis.set_major_locator(MaxNLocator(5))
    axes[1].yaxis.set_major_locator(MaxNLocator(5, integer=True))
    for axis in axes:
        axis.grid(False)

    fig.subplots_adjust(left=0.19, right=0.98, bottom=0.12, top=0.98)
    for suffix in ("pdf", "svg", "png", "tiff"):
        kwargs = {"dpi": 600} if suffix in {"png", "tiff"} else {}
        fig.savefig(figure_base.with_suffix(f".{suffix}"), bbox_inches="tight", **kwargs)
    plt.close(fig)

    print(out_summary)
    print(figure_base.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
