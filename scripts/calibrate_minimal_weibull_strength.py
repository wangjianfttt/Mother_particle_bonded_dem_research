#!/usr/bin/env python3
"""Minimal Weibull/strength-multiplier calibration for SP-002.

This script is intentionally statistical only: it reads existing calibration
tables and writes derived CSV recommendations without touching any LIGGGHTS
input deck or simulation template.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def as_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def mean_sd(values: list[float]) -> tuple[float | None, float | None]:
    if not values:
        return None, None
    if len(values) == 1:
        return values[0], 0.0
    return statistics.mean(values), statistics.stdev(values)


def loglog_power_fit(points: list[tuple[float, float]]) -> tuple[float, float, float]:
    """Return intercept, slope and RMSE for log(force) = intercept + slope log(d)."""
    xs = [math.log(d) for d, _ in points]
    ys = [math.log(f) for _, f in points]
    xbar = statistics.mean(xs)
    ybar = statistics.mean(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denom
    intercept = ybar - slope * xbar
    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    rmse = math.sqrt(sum(r * r for r in residuals) / max(len(residuals) - 2, 1))
    return intercept, slope, rmse


def weibull_cv(shape_m: float) -> float:
    g1 = math.gamma(1.0 + 1.0 / shape_m)
    g2 = math.gamma(1.0 + 2.0 / shape_m)
    return math.sqrt(g2 / (g1 * g1) - 1.0)


def percentile_weibull_multiplier(p: float, shape_m: float) -> float:
    """Unit-mean two-parameter Weibull quantile multiplier."""
    scale_for_unit_mean = 1.0 / math.gamma(1.0 + 1.0 / shape_m)
    return scale_for_unit_mean * (-math.log(1.0 - p)) ** (1.0 / shape_m)


def weibull_cdf_for_multiplier(multiplier: float, shape_m: float) -> float:
    """CDF for a unit-mean two-parameter Weibull multiplier."""
    scale_for_unit_mean = 1.0 / math.gamma(1.0 + 1.0 / shape_m)
    return 1.0 - math.exp(-((multiplier / scale_for_unit_mean) ** shape_m))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_calibration(args: argparse.Namespace) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    experimental_rows = read_rows(ROOT / args.experimental_targets)
    orientation_rows = read_rows(ROOT / args.orientation_summary)
    model_rows = read_rows(ROOT / args.model_summary)

    size_points = [
        (diameter, force)
        for row in experimental_rows
        if row.get("calibration_use") == "size_effect_reference"
        for diameter in [as_float(row.get("diameter_mm"))]
        for force in [as_float(row.get("mean_crush_load_N"))]
        if diameter is not None and force is not None and diameter > 0 and force > 0
    ]
    if len(size_points) < 2:
        raise ValueError("Need at least two size-effect reference points.")

    intercept, slope, log_rmse = loglog_power_fit(size_points)
    target_mean = math.exp(intercept + slope * math.log(args.target_diameter_mm))

    probability_rows = [
        row
        for row in experimental_rows
        if row.get("calibration_use") == "probability_strength_reference"
    ]
    reported_cvs = [
        std / mean
        for row in probability_rows
        for mean in [as_float(row.get("mean_crush_load_N"))]
        for std in [as_float(row.get("std_crush_load_N"))]
        if mean is not None and std is not None and mean > 0
    ]
    weibull_ms = [
        m
        for row in probability_rows
        for m in [as_float(row.get("weibull_m"))]
        if m is not None and m > 0
    ]
    cv_prior = statistics.mean(reported_cvs) if reported_cvs else 0.20
    weibull_m_prior = statistics.mean(weibull_ms) if weibull_ms else 3.0
    target_sd = target_mean * cv_prior
    target_low = args.target_low_N if args.target_low_N is not None else target_mean * 0.85
    target_high = args.target_high_N if args.target_high_N is not None else target_mean * 1.15

    orientation_peak_forces = [
        force
        for row in orientation_rows
        for force in [as_float(row.get("peak_top_force_N"))]
        if force is not None
    ]
    orientation_mean, orientation_sd = mean_sd(orientation_peak_forces)

    candidate_rows = [
        row
        for row in model_rows
        if row.get("calibration_status") == "candidate_calibrated"
        or "weak-plane" in row.get("case_id", "")
    ]
    candidate_forces = [
        force
        for row in candidate_rows
        for force in [as_float(row.get("peak_top_force_N"))]
        if force is not None
    ]
    candidate_mean, candidate_sd = mean_sd(candidate_forces)

    baseline_force = orientation_mean or candidate_mean
    if baseline_force is None or baseline_force <= 0:
        raise ValueError("No usable model peak force in orientation summary or model summary.")

    mean_multiplier = target_mean / baseline_force
    low_multiplier = target_low / baseline_force
    high_multiplier = target_high / baseline_force
    p10_multiplier = mean_multiplier * percentile_weibull_multiplier(0.10, weibull_m_prior)
    p90_multiplier = mean_multiplier * percentile_weibull_multiplier(0.90, weibull_m_prior)
    truncated_p_low = weibull_cdf_for_multiplier(low_multiplier / mean_multiplier, weibull_m_prior)
    truncated_p_high = weibull_cdf_for_multiplier(high_multiplier / mean_multiplier, weibull_m_prior)

    summary_rows: list[dict[str, object]] = [
        {
            "block": "literature_target",
            "metric": "target_diameter_mm",
            "value": args.target_diameter_mm,
            "units": "mm",
            "method": "script input",
            "notes": "Default is the current 1.0 mm SP-002 mother particle.",
        },
        {
            "block": "literature_target",
            "metric": "mean_crush_load_N",
            "value": round(target_mean, 6),
            "units": "N",
            "method": "log-log power fit to size_effect_reference rows",
            "notes": f"Fit slope={slope:.3f}; log-space RMSE={log_rmse:.3f}.",
        },
        {
            "block": "literature_target",
            "metric": "std_crush_load_N",
            "value": round(target_sd, 6),
            "units": "N",
            "method": "target mean times Zhao probability-reference reported CV",
            "notes": f"Mean reported CV={cv_prior:.3f}; Weibull-m prior={weibull_m_prior:.3f}.",
        },
        {
            "block": "literature_target",
            "metric": "target_window_N",
            "value": f"{target_low:.6g}-{target_high:.6g}",
            "units": "N",
            "method": "explicit input or +/-15% default",
            "notes": "Use as the first acceptance window for mean force before morphology checks.",
        },
        {
            "block": "model_orientation_pilot",
            "metric": "peak_top_force_mean_N",
            "value": round(orientation_mean, 6) if orientation_mean is not None else "",
            "units": "N",
            "method": "mean of sp002_cal1_orientation_summary.csv peak_top_force_N",
            "notes": f"n={len(orientation_peak_forces)} orientation pilots.",
        },
        {
            "block": "model_orientation_pilot",
            "metric": "peak_top_force_std_N",
            "value": round(orientation_sd, 6) if orientation_sd is not None else "",
            "units": "N",
            "method": "sample standard deviation",
            "notes": "Captures orientation/weak-plane scatter only.",
        },
        {
            "block": "model_weakplane_candidates",
            "metric": "peak_top_force_mean_N",
            "value": round(candidate_mean, 6) if candidate_mean is not None else "",
            "units": "N",
            "method": "mean of candidate/weak-plane rows in model summary",
            "notes": f"n={len(candidate_forces)} current weak-plane candidates.",
        },
        {
            "block": "model_weakplane_candidates",
            "metric": "peak_top_force_std_N",
            "value": round(candidate_sd, 6) if candidate_sd is not None else "",
            "units": "N",
            "method": "sample standard deviation",
            "notes": "Useful for comparing the tuned weak-plane row with the orientation pilot.",
        },
        {
            "block": "strength_multiplier",
            "metric": "suggested_mean_multiplier",
            "value": round(mean_multiplier, 6),
            "units": "relative_to_orientation_pilot_mean",
            "method": "literature target mean / orientation pilot mean",
            "notes": "Apply as a sample-level multiplier to both bulk and weak-plane strengths.",
        },
        {
            "block": "strength_multiplier",
            "metric": "suggested_range_multiplier",
            "value": f"{low_multiplier:.6g}-{high_multiplier:.6g}",
            "units": "relative_to_orientation_pilot_mean",
            "method": "target force window / orientation pilot mean",
            "notes": "Do not overwrite the current CAL1 input; use this for future ensemble case generation.",
        },
        {
            "block": "strength_multiplier",
            "metric": "weibull_p10_p90_multiplier",
            "value": f"{p10_multiplier:.6g}-{p90_multiplier:.6g}",
            "units": "relative_to_current_strengths",
            "method": "unit-mean Weibull quantiles using the Zhao m prior",
            "notes": "Use as the untruncated stochastic spread estimate before the first acceptance window is imposed.",
        },
        {
            "block": "strength_multiplier",
            "metric": "truncated_weibull_probability_window",
            "value": f"{truncated_p_low:.6g}-{truncated_p_high:.6g}",
            "units": "cdf_probability",
            "method": "CDF values of suggested multiplier range under the unit-mean Weibull prior",
            "notes": "The sampling plan uses Latin quantiles inside this probability window to avoid duplicate clipped samples.",
        },
    ]

    orientation_labels = [row.get("orientation_label", "") for row in orientation_rows]
    if not orientation_labels:
        orientation_labels = ["x", "xy30", "y", "xy45", "tilt_xz"]

    sample_count = args.ensemble_samples
    sampling_rows: list[dict[str, object]] = []
    for sample_id in range(1, sample_count + 1):
        full_p = (sample_id - 0.5) / sample_count
        truncated_p = truncated_p_low + full_p * (truncated_p_high - truncated_p_low)
        full_distribution_multiplier = mean_multiplier * percentile_weibull_multiplier(full_p, weibull_m_prior)
        recommended_multiplier = mean_multiplier * percentile_weibull_multiplier(truncated_p, weibull_m_prior)
        orientation = orientation_labels[(sample_id - 1) % len(orientation_labels)]
        sampling_rows.append(
            {
                "sample_id": sample_id,
                "orientation_label": orientation,
                "full_weibull_probability_midpoint": round(full_p, 6),
                "truncated_weibull_probability_midpoint": round(truncated_p, 6),
                "full_distribution_strength_multiplier": round(full_distribution_multiplier, 6),
                "recommended_strength_multiplier": round(recommended_multiplier, 6),
                "bulk_strength_MPa_if_CAL1_bulk90": round(90.0 * recommended_multiplier, 6),
                "weakplane_strength_MPa_if_CAL1_weak22p5": round(22.5 * recommended_multiplier, 6),
                "strategy_note": "Truncated Latin-quantile Weibull strength multiplier crossed with rotating weak-plane orientations.",
            }
        )

    return summary_rows, sampling_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--experimental-targets",
        default="tables/single_pebble_experimental_calibration_targets.csv",
    )
    parser.add_argument(
        "--orientation-summary",
        default="tables/sp002_cal1_orientation_summary.csv",
    )
    parser.add_argument(
        "--model-summary",
        default="tables/single_pebble_model_calibration_matrix.csv",
    )
    parser.add_argument("--target-diameter-mm", type=float, default=1.0)
    parser.add_argument("--target-low-N", type=float, default=15.0)
    parser.add_argument("--target-high-N", type=float, default=22.0)
    parser.add_argument("--ensemble-samples", type=int, default=25)
    parser.add_argument(
        "--summary-out",
        default="tables/minimal_weibull_strength_calibration_summary.csv",
    )
    parser.add_argument(
        "--sampling-out",
        default="tables/minimal_weibull_strength_sampling_plan.csv",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not 20 <= args.ensemble_samples <= 30:
        raise ValueError("--ensemble-samples should be between 20 and 30 for this pilot plan.")
    summary_rows, sampling_rows = build_calibration(args)
    summary_out = ROOT / args.summary_out
    sampling_out = ROOT / args.sampling_out
    write_csv(summary_out, summary_rows)
    write_csv(sampling_out, sampling_rows)
    print(summary_out)
    print(sampling_out)


if __name__ == "__main__":
    main()
