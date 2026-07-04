#!/usr/bin/env python3
"""Build a source-backed CPM material-response summary.

The summary converts the PB-007 material-parameter response table into a compact
set of reviewer-facing facts. It is intentionally finite-window wording: the
dataset supports material-response and force-path interaction in the completed
100-particle windows, not a converged fracture probability.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "tables" / "pb007_material_parameter_response.csv"
CSV_OUT = ROOT / "docs" / "cpm_material_response_summary_20260704.csv"
MD_OUT = ROOT / "docs" / "cpm_material_response_summary_20260704.md"


def _fmt(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def _range_text(series: pd.Series, unit: str = "") -> str:
    values = pd.to_numeric(series, errors="coerce").dropna()
    suffix = f" {unit}" if unit else ""
    if values.empty:
        return "n/a"
    if values.min() == values.max():
        return f"{_fmt(float(values.min()))}{suffix}"
    return f"{_fmt(float(values.min()))}-{_fmt(float(values.max()))}{suffix}"


def _case_label(row: pd.Series) -> str:
    return f"{row['geometry_class']} at {row['strength_multiplier']:g}x"


def main() -> int:
    df = pd.read_csv(INPUT)
    numeric_cols = [
        "strength_multiplier",
        "broken_bonds_at_endpoint",
        "first_event_displacement_um",
        "final_inter_pebble_force_sum_N",
        "final_top_reachable_mothers",
        "final_bottom_reachable_from_top",
        "final_spanning_force_graph",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if len(df) != 11:
        raise SystemExit(f"expected 11 material-response endpoint rows, found {len(df)}")
    if not df["case_status"].eq("completed_postprocessed").all():
        raise SystemExit("all material-response rows must be completed_postprocessed")
    if not df["final_spanning_force_graph"].eq(1).all():
        raise SystemExit("all material-response rows must retain a spanning final force graph")

    zero = df[df["broken_bonds_at_endpoint"].eq(0)].copy()
    crack = df[df["broken_bonds_at_endpoint"].gt(0)].copy()
    matrix = df[
        df["geometry_class"].isin(["early_cracking", "synchronous_cracking"])
        & df["strength_multiplier"].isin([0.75, 0.5, 0.25])
    ].copy()
    early = df[df["geometry_class"].eq("early_cracking")].sort_values(
        "strength_multiplier", ascending=False
    )
    sync = df[df["geometry_class"].eq("synchronous_cracking")].sort_values(
        "strength_multiplier", ascending=False
    )
    intact = df[df["geometry_class"].eq("intact_geometry")].sort_values(
        "strength_multiplier", ascending=False
    )

    max_zero_force = float(zero["final_inter_pebble_force_sum_N"].max())
    min_crack_force = float(crack["final_inter_pebble_force_sum_N"].min())
    force_ratio = min_crack_force / max_zero_force

    sync_first_nominal = float(
        sync.loc[sync["strength_multiplier"].eq(1.0), "first_event_displacement_um"].iloc[0]
    )
    sync_first_min = float(sync["first_event_displacement_um"].min())
    sync_onset_advance = sync_first_nominal - sync_first_min
    sync_onset_advance_fraction = sync_onset_advance / sync_first_nominal

    early_first_unique = sorted(early["first_event_displacement_um"].dropna().unique())

    rows = [
        {
            "finding": "completed_endpoint_rows",
            "value": f"{len(df)} completed endpoints; {len(crack)} cracking endpoints; {len(zero)} zero-loss endpoints",
            "source_columns": "case_status, broken_bonds_at_endpoint",
            "boundary": "Finite 100-particle endpoint set.",
        },
        {
            "finding": "strength_matrix_scope",
            "value": f"{len(matrix)} strength-reduction rows across early_cracking and synchronous_cracking geometries",
            "source_columns": "geometry_class, strength_multiplier",
            "boundary": "Strength multipliers 0.75x, 0.50x and 0.25x for two cracking geometries.",
        },
        {
            "finding": "intact_geometry_controls",
            "value": (
                "intact_geometry remains at 0 broken bonds for strength multipliers "
                + ", ".join(f"{v:g}x" for v in intact["strength_multiplier"])
                + f"; final force-sum range {_range_text(intact['final_inter_pebble_force_sum_N'], 'N')}"
            ),
            "source_columns": "geometry_class, strength_multiplier, broken_bonds_at_endpoint, final_inter_pebble_force_sum_N",
            "boundary": "Zero-loss controls in the 60 micrometre displacement window.",
        },
        {
            "finding": "early_cracking_response",
            "value": (
                f"first localized bond loss remains at {_fmt(float(early_first_unique[0]))} micrometres; "
                f"endpoint bond loss is {_range_text(early['broken_bonds_at_endpoint'], 'bonds')}; "
                f"force-sum range {_range_text(early['final_inter_pebble_force_sum_N'], 'N')}"
            ),
            "source_columns": "first_event_displacement_um, broken_bonds_at_endpoint, final_inter_pebble_force_sum_N",
            "boundary": "Geometry-specific response; onset does not advance in this geometry.",
        },
        {
            "finding": "synchronous_cracking_response",
            "value": (
                f"first localized bond loss advances from {_fmt(sync_first_nominal)} to {_fmt(sync_first_min)} micrometres "
                f"({sync_onset_advance:.0f} micrometres, {100.0 * sync_onset_advance_fraction:.1f}%); "
                f"endpoint bond loss is {_range_text(sync['broken_bonds_at_endpoint'], 'bonds')}; "
                f"force-sum range {_range_text(sync['final_inter_pebble_force_sum_N'], 'N')}"
            ),
            "source_columns": "first_event_displacement_um, broken_bonds_at_endpoint, final_inter_pebble_force_sum_N",
            "boundary": "Geometry-specific response; onset advances under strength reduction in this geometry.",
        },
        {
            "finding": "force_path_endpoint_separation",
            "value": (
                f"minimum cracking force sum {_fmt(min_crack_force)} N / maximum zero-loss force sum "
                f"{_fmt(max_zero_force)} N = {force_ratio:.2f}"
            ),
            "source_columns": "final_inter_pebble_force_sum_N, broken_bonds_at_endpoint",
            "boundary": "Endpoint separator for current finite windows, not a universal threshold.",
        },
        {
            "finding": "spanning_graph_retention",
            "value": "all 11 material-response endpoints retain a spanning final native force graph",
            "source_columns": "final_spanning_force_graph",
            "boundary": "Local bond loss occurs within connected load-bearing networks.",
        },
    ]

    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# CPM material-response summary",
        "",
        "Date: 2026-07-04",
        "",
        f"Input: `{INPUT.relative_to(ROOT)}`.",
        "",
        "## Source-backed findings",
        "",
    ]
    for row in rows:
        lines.append(f"- **{row['finding']}**: {row['value']}")
        lines.append(f"  Boundary: {row['boundary']}")
    lines.extend(
        [
            "",
            "## Geometry-level endpoint table",
            "",
            "| Case | Endpoint broken bonds | First localized bond loss (micrometres) | Final force sum (N) | Top reachable | Bottom reachable from top |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    display = df.sort_values(["geometry_class", "strength_multiplier"], ascending=[True, False])
    for _, row in display.iterrows():
        first = row["first_event_displacement_um"]
        first_text = "none" if pd.isna(first) else _fmt(float(first))
        lines.append(
            "| {case} | {broken:.0f} | {first} | {force:.3f} | {top:.0f} | {bottom:.0f} |".format(
                case=_case_label(row),
                broken=float(row["broken_bonds_at_endpoint"]),
                first=first_text,
                force=float(row["final_inter_pebble_force_sum_N"]),
                top=float(row["final_top_reachable_mothers"]),
                bottom=float(row["final_bottom_reachable_from_top"]),
            )
        )
    lines.extend(
        [
            "",
            "## Manuscript use",
            "",
            "Use these values to support the finite-window claim that local force-path topology and bonded-particle strength jointly control early fracture. Do not use them as a converged stochastic fracture-probability estimate or as a universal Li4SiO4 material law.",
            "",
        ]
    )
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")

    print(MD_OUT)
    print(CSV_OUT)
    print(f"force_path_gap_ratio={force_ratio:.2f}")
    print(f"sync_onset_advance_um={sync_onset_advance:.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
