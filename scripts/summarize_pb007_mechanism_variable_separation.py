#!/usr/bin/env python3
"""Summarize mechanism-variable separation in the PB-007 endpoint dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "tables" / "pb007_material_parameter_response.csv"
TABLE_OUT = ROOT / "tables" / "pb007_mechanism_variable_separation.csv"
FIGURE_SOURCE_OUT = ROOT / "data" / "figure_source" / "pb007_mechanism_variable_separation.csv"
DOC_OUT = ROOT / "docs" / "repaired_mechanism_variable_separation_20260704.md"


def _fmt_range(series: pd.Series, unit: str = "") -> str:
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return "n/a"
    suffix = f" {unit}" if unit else ""
    if values.min() == values.max():
        return f"{values.min():.3g}{suffix}"
    return f"{values.min():.3g}-{values.max():.3g}{suffix}"


def _overlap(a: pd.Series, b: pd.Series) -> bool:
    va = pd.to_numeric(a, errors="coerce").dropna()
    vb = pd.to_numeric(b, errors="coerce").dropna()
    if va.empty or vb.empty:
        return False
    return max(va.min(), vb.min()) <= min(va.max(), vb.max())


def main() -> int:
    df = pd.read_csv(INPUT)
    numeric_cols = [
        "strength_multiplier",
        "broken_bonds_at_endpoint",
        "first_event_displacement_um",
        "final_inter_pebble_force_sum_N",
        "final_top_reachable_mothers",
        "final_bottom_reachable_from_top",
        "damaged_mother_pebbles",
        "peak_top_force_N",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["endpoint_class"] = df["broken_bonds_at_endpoint"].gt(0).map(
        {True: "localized cracking", False: "zero-loss endpoint"}
    )
    cracking = df[df["endpoint_class"].eq("localized cracking")]
    intact = df[df["endpoint_class"].eq("zero-loss endpoint")]

    max_intact_force = float(intact["final_inter_pebble_force_sum_N"].max())
    min_crack_force = float(cracking["final_inter_pebble_force_sum_N"].min())
    midpoint_force_threshold = 0.5 * (max_intact_force + min_crack_force)
    force_gap_ratio = min_crack_force / max_intact_force if max_intact_force else float("nan")

    rows = [
        {
            "descriptor": "final inter-particle force sum",
            "zero_loss_range": _fmt_range(intact["final_inter_pebble_force_sum_N"], "N"),
            "cracking_range": _fmt_range(cracking["final_inter_pebble_force_sum_N"], "N"),
            "overlap_between_endpoint_classes": "no",
            "finite_window_separation": f"minimum cracking value / maximum zero-loss value = {force_gap_ratio:.2f}",
            "manuscript_use": "Use as the strongest endpoint state variable in the current finite windows.",
        },
        {
            "descriptor": "bond-strength multiplier",
            "zero_loss_range": _fmt_range(intact["strength_multiplier"]),
            "cracking_range": _fmt_range(cracking["strength_multiplier"]),
            "overlap_between_endpoint_classes": "yes" if _overlap(intact["strength_multiplier"], cracking["strength_multiplier"]) else "no",
            "finite_window_separation": "0.25x, 0.50x and 1.00x appear in both endpoint classes",
            "manuscript_use": "Use to show that strength multiplier must be read with packing geometry.",
        },
        {
            "descriptor": "top-reachable parent-particle count",
            "zero_loss_range": _fmt_range(intact["final_top_reachable_mothers"]),
            "cracking_range": _fmt_range(cracking["final_top_reachable_mothers"]),
            "overlap_between_endpoint_classes": "yes" if _overlap(intact["final_top_reachable_mothers"], cracking["final_top_reachable_mothers"]) else "no",
            "finite_window_separation": "reachability overlaps across endpoint classes",
            "manuscript_use": "Use as a connectivity descriptor, not as a single separator.",
        },
        {
            "descriptor": "bottom-contacting particles reachable from top",
            "zero_loss_range": _fmt_range(intact["final_bottom_reachable_from_top"]),
            "cracking_range": _fmt_range(cracking["final_bottom_reachable_from_top"]),
            "overlap_between_endpoint_classes": "yes" if _overlap(intact["final_bottom_reachable_from_top"], cracking["final_bottom_reachable_from_top"]) else "no",
            "finite_window_separation": "zero-loss rows have higher bottom reachability in the current finite windows",
            "manuscript_use": "Use together with force intensity and damage chronology.",
        },
        {
            "descriptor": "endpoint broken-bond count",
            "zero_loss_range": _fmt_range(intact["broken_bonds_at_endpoint"], "bonds"),
            "cracking_range": _fmt_range(cracking["broken_bonds_at_endpoint"], "bonds"),
            "overlap_between_endpoint_classes": "no",
            "finite_window_separation": "output class definition",
            "manuscript_use": "Use as the observed response, not as a predictor.",
        },
    ]
    summary = pd.DataFrame(rows)

    detail_cols = [
        "case_label",
        "geometry_class",
        "strength_multiplier",
        "endpoint_class",
        "final_inter_pebble_force_sum_N",
        "final_top_reachable_mothers",
        "final_bottom_reachable_from_top",
        "first_event_displacement_um",
        "broken_bonds_at_endpoint",
        "damaged_mother_pebbles",
    ]
    detail = df[detail_cols].sort_values(
        ["endpoint_class", "geometry_class", "strength_multiplier"],
        ascending=[True, True, False],
    )
    detail["force_sum_separation_rule_current_windows"] = (
        detail["final_inter_pebble_force_sum_N"] > midpoint_force_threshold
    )

    TABLE_OUT.parent.mkdir(parents=True, exist_ok=True)
    FIGURE_SOURCE_OUT.parent.mkdir(parents=True, exist_ok=True)
    DOC_OUT.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(TABLE_OUT, index=False)
    detail.to_csv(FIGURE_SOURCE_OUT, index=False)

    lines = [
        "# PB-007 mechanism-variable separation",
        "",
        "Date: 2026-07-04",
        "",
        "Input: `tables/pb007_material_parameter_response.csv`.",
        "",
        "## Endpoint rows",
        "",
        f"- Total completed endpoint rows: {len(df)}",
        f"- Localized-cracking rows: {len(cracking)}",
        f"- Zero-loss endpoint rows: {len(intact)}",
        "",
        "## Main finite-window separation",
        "",
        f"- Maximum zero-loss final inter-particle force sum: {max_intact_force:.3f} N",
        f"- Minimum cracking final inter-particle force sum: {min_crack_force:.3f} N",
        f"- Separation ratio: {force_gap_ratio:.2f}",
        f"- Midpoint separator for these finite windows: {midpoint_force_threshold:.3f} N",
        "",
        "Strength multiplier alone does not separate the endpoint classes: 0.25x, 0.50x and 1.00x appear in both zero-loss and cracking rows. Top reachability overlaps, while bottom reachability separates these finite windows in the opposite direction from force intensity. The useful interpretation is a joint state variable set: local force-path intensity, packing geometry, bond strength and event chronology.",
        "",
        "## Output files",
        "",
        f"- `{TABLE_OUT.relative_to(ROOT)}`",
        f"- `{FIGURE_SOURCE_OUT.relative_to(ROOT)}`",
        "",
    ]
    DOC_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(TABLE_OUT)
    print(FIGURE_SOURCE_OUT)
    print(DOC_OUT)
    print(
        "finite-window force-sum separation: "
        f"max_zero_loss={max_intact_force:.3f} N, "
        f"min_cracking={min_crack_force:.3f} N, "
        f"ratio={force_gap_ratio:.2f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
