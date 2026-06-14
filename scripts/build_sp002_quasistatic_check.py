#!/usr/bin/env python3
"""Build a conservative quasi-static risk table for SP-002 calibration."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def metric_map(path: Path) -> dict[str, str]:
    return {row["metric"]: row["value"] for row in read_rows(path)}


def initial_bonds_from_fragments(path: Path) -> int:
    bonded_rows = [row for row in read_rows(path) if int(row["intact_bonds"]) > 0]
    return int(bonded_rows[0]["intact_bonds"]) if bonded_rows else 0


def pct_change(a: float, b: float) -> float:
    return 100.0 * (b - a) / a if a else 0.0


def main() -> None:
    speed_rows = sorted(
        read_rows(ROOT / "tables/sp002_speed_sensitivity.csv"),
        key=lambda row: as_float(row, "top_speed_m_s"),
        reverse=True,
    )
    speed_by_value = {as_float(row, "top_speed_m_s"): row for row in speed_rows}
    v025 = speed_by_value[0.25]
    v010 = speed_by_value[0.1]
    cal1 = next(
        row
        for row in read_rows(ROOT / "tables/single_pebble_model_calibration_matrix.csv")
        if row["case_id"] == "SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm"
    )
    slow_case = "SP-002-CAL1-slow0p05ms-0p3mm"
    matched_case = "SP-002-CAL1-matched0p10ms-0p3mm"
    x_slow_case = "SP-002-CAL1-x-slow0p05ms-0p3mm"
    x_slow003_case = "SP-002-CAL1-x-slow0p03ms-0p18mm"
    slow_summary_path = ROOT / f"data/processed/{slow_case}_summary.csv"
    slow_fragments_path = ROOT / f"data/processed/{slow_case}_fragments.csv"
    matched_summary_path = ROOT / f"data/processed/{matched_case}_summary.csv"
    matched_fragments_path = ROOT / f"data/processed/{matched_case}_fragments.csv"
    x_slow_summary_path = ROOT / f"data/processed/{x_slow_case}_summary.csv"
    x_slow_fragments_path = ROOT / f"data/processed/{x_slow_case}_fragments.csv"
    x_slow003_summary_path = ROOT / f"data/processed/{x_slow003_case}_summary.csv"
    x_slow003_fragments_path = ROOT / f"data/processed/{x_slow003_case}_fragments.csv"

    force_change = pct_change(as_float(v025, "peak_top_force_N"), as_float(v010, "peak_top_force_N"))
    broken_change = pct_change(as_float(v025, "final_broken_bonds"), as_float(v010, "final_broken_bonds"))
    first_break_change = as_float(v010, "first_break_displacement_mm") - as_float(v025, "first_break_displacement_mm")

    rows = [
        {
            "check_id": "SP002-speed-50MPa-0p25-vs-0p10",
            "case_family": "homogeneous 50 MPa speed sensitivity",
            "evidence_files": "tables/sp002_speed_sensitivity.csv",
            "metric": "0.25 to 0.10 m/s convergence",
            "result": (
                f"peak force change {force_change:.1f}%; final broken-bond change "
                f"{broken_change:.1f}%; first-break displacement shift {first_break_change:.4f} mm"
            ),
            "interpretation": (
                "fragment-count convergence is encouraging, but peak force still changes by several percent"
            ),
            "claim_status": "partial support for screening-rate adequacy",
            "next_action": "treat as background only now that the true x-normal CAL1 slower check exists",
        },
        {
            "check_id": "SP002-CAL1-current-rate",
                "case_family": "SP-002-CAL1 weak-plane candidate",
                "evidence_files": (
                    "data/processed/SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm_thermo.csv; "
                    "tables/single_pebble_model_calibration_matrix.csv"
                ),
                "metric": "x-normal 0.10 m/s production loading rate",
            "result": (
                f"0.10 m/s run gives peak top force {float(cal1['peak_top_force_N']):.2f} N, "
                f"first break {float(cal1['first_break_displacement_mm']):.4f} mm, "
                f"final fragments {cal1['largest_fragment_particles']} + {cal1['second_fragment_particles']} particles"
            ),
            "interpretation": (
                "load scale and splitting morphology are acceptable for a calibration candidate, "
                "but this is not a demonstrated quasi-static material response"
            ),
            "claim_status": "candidate only",
            "next_action": "compare against the true x-normal 0.05 m/s rerun, not the y-normal residual-template run",
        },
    ]

    if x_slow_summary_path.exists() and x_slow_fragments_path.exists():
        x_slow_summary = metric_map(x_slow_summary_path)
        x_slow_fragments = read_rows(x_slow_fragments_path)
        x_initial_bonds = initial_bonds_from_fragments(x_slow_fragments_path)
        x_final_frag = x_slow_fragments[-1]
        peak_change = pct_change(
            float(cal1["peak_top_force_N"]),
            float(x_slow_summary["peak_top_force_N"]),
        )
        first_break_shift = (
            float(x_slow_summary["first_break_displacement_mm"])
            - float(cal1["first_break_displacement_mm"])
        )
        rows.append(
            {
                "check_id": "SP002-CAL1-xnormal-0p10-vs-0p05",
                "case_family": "SP-002-CAL1 x-normal weak-plane candidate",
                "evidence_files": (
                    "data/processed/SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm_summary.csv; "
                    f"data/processed/{x_slow_case}_summary.csv; "
                    f"data/processed/{x_slow_case}_fragments.csv; "
                    f"data/processed/{x_slow_case}_failure_metrics.csv"
                ),
                "metric": "true CAL1 x-normal 0.10 to 0.05 m/s comparison",
                "result": (
                    f"peak force change {peak_change:.1f}%; first-break shift {first_break_shift:.5f} mm; "
                    f"0.05 m/s peak {float(x_slow_summary['peak_top_force_N']):.2f} N; "
                    f"final fragments {x_final_frag['largest_fragment_particles']} + "
                    f"{x_final_frag['second_fragment_particles']} particles; initial intact bonds {x_initial_bonds}"
                ),
                "interpretation": (
                    "the true x-normal slow rerun preserves the 5876-bond CAL1 template, the same first-break displacement and a two-major-fragment split; "
                    "the peak force rises moderately but remains inside the current 15-22 N exploratory target window"
                ),
                "claim_status": "partial support for CAL1 rate robustness; not final quasi-static validation",
                "next_action": "add one hold-relax or slower x-normal check only if the manuscript makes strong quasi-static wording",
            }
        )

    if x_slow003_summary_path.exists() and x_slow003_fragments_path.exists():
        x_slow003_summary = metric_map(x_slow003_summary_path)
        x_slow003_fragments = read_rows(x_slow003_fragments_path)
        x_slow003_initial_bonds = initial_bonds_from_fragments(x_slow003_fragments_path)
        x_slow003_final_frag = x_slow003_fragments[-1]
        first_break_shift = (
            float(x_slow003_summary["first_break_displacement_mm"])
            - float(cal1["first_break_displacement_mm"])
        )
        rows.append(
            {
                "check_id": "SP002-CAL1-xnormal-0p03-onset-check",
                "case_family": "SP-002-CAL1 x-normal weak-plane candidate",
                "evidence_files": (
                    f"data/processed/{x_slow003_case}_summary.csv; "
                    f"data/processed/{x_slow003_case}_fragments.csv; "
                    f"data/processed/{x_slow003_case}_failure_metrics.csv"
                ),
                "metric": "true CAL1 x-normal 0.03 m/s short endpoint check",
                "result": (
                    f"first-break shift {first_break_shift:.5f} mm versus 0.10 m/s; "
                    f"first break {float(x_slow003_summary['first_break_displacement_mm']):.5f} mm; "
                    f"endpoint peak {float(x_slow003_summary['peak_top_force_N']):.2f} N at 0.18 mm endpoint; "
                    f"fragments {x_slow003_final_frag['largest_fragment_particles']} + "
                    f"{x_slow003_final_frag['second_fragment_particles']} particles; initial intact bonds {x_slow003_initial_bonds}"
                ),
                "interpretation": (
                    "the 0.03 m/s short run preserves the 5876-bond x-normal CAL1 branch and reaches the same first-break window and two-major-fragment topology; "
                    "because it stops at 0.18 mm before the known peak region, it should not be used for peak-load comparison"
                ),
                "claim_status": "supports first-break and morphology robustness only",
                "next_action": "extend to 0.30 mm only if stronger peak-load rate wording is needed",
            }
        )

    if matched_summary_path.exists() and matched_fragments_path.exists():
        matched_summary = metric_map(matched_summary_path)
        matched_fragments = read_rows(matched_fragments_path)
        matched_initial_bonds = initial_bonds_from_fragments(matched_fragments_path)
        matched_final_frag = matched_fragments[-1]
        rows.append(
            {
                "check_id": "SP002-y-normal-current-template-0p10ms",
                "case_family": "SP-002 y-normal orientation sensitivity",
                "evidence_files": (
                    f"data/processed/{matched_case}_summary.csv; "
                    f"data/processed/{matched_case}_fragments.csv; "
                    f"data/processed/{matched_case}_failure_metrics.csv"
                ),
                "metric": "residual-template y-normal 0.10 m/s rerun",
                "result": (
                    f"peak top force {float(matched_summary['peak_top_force_N']):.2f} N; "
                    f"first break {float(matched_summary['first_break_displacement_mm']):.4f} mm; "
                    f"final fragments {matched_final_frag['largest_fragment_particles']} + "
                    f"{matched_final_frag['second_fragment_particles']} particles; "
                    f"initial intact bonds {matched_initial_bonds}"
                ),
                "interpretation": (
                    "this case reproduces the y-normal orientation pilot, not the x-normal CAL1 candidate; "
                    "it is useful as an orientation-specific rate check but must not be cited as CAL1 reproduction"
                ),
                "claim_status": "orientation sensitivity evidence only",
                "next_action": (
                    "keep the case in the provenance audit and avoid using it as the CAL1 x-normal quasi-static check"
                ),
            }
        )

    if slow_summary_path.exists() and slow_fragments_path.exists():
        slow_summary = metric_map(slow_summary_path)
        slow_fragments = read_rows(slow_fragments_path)
        initial_bonds = initial_bonds_from_fragments(slow_fragments_path)
        final_frag = slow_fragments[-1]
        rows.append(
            {
                "check_id": "SP002-y-normal-current-template-0p05ms",
                "case_family": "SP-002 y-normal orientation sensitivity",
                "evidence_files": (
                    f"data/processed/{slow_case}_summary.csv; "
                    f"data/processed/{slow_case}_fragments.csv; "
                    f"data/processed/{slow_case}_failure_metrics.csv"
                ),
                "metric": "residual-template y-normal 0.05 m/s full 0.30 mm rerun",
                "result": (
                    f"peak top force {float(slow_summary['peak_top_force_N']):.2f} N; "
                    f"first break {float(slow_summary['first_break_displacement_mm']):.4f} mm; "
                    f"final fragments {final_frag['largest_fragment_particles']} + "
                    f"{final_frag['second_fragment_particles']} particles; "
                    f"initial intact bonds {initial_bonds}"
                ),
                "interpretation": (
                    "slower loading retains the y-normal two-major-fragment morphology; compared with the y-normal 0.10 m/s run, "
                    "first-break displacement, peak force and final fragment graph are nearly unchanged"
                ),
                "claim_status": "supports y-normal rate insensitivity over 0.10-0.05 m/s",
                "next_action": "use only as orientation-specific sensitivity evidence",
            }
        )

    if (
        matched_summary_path.exists()
        and matched_fragments_path.exists()
        and slow_summary_path.exists()
        and slow_fragments_path.exists()
    ):
        matched_summary = metric_map(matched_summary_path)
        slow_summary = metric_map(slow_summary_path)
        matched_final_frag = read_rows(matched_fragments_path)[-1]
        slow_final_frag = read_rows(slow_fragments_path)[-1]
        peak_change = pct_change(
            float(matched_summary["peak_top_force_N"]),
            float(slow_summary["peak_top_force_N"]),
        )
        first_break_shift = (
            float(slow_summary["first_break_displacement_mm"])
            - float(matched_summary["first_break_displacement_mm"])
        )
        rows.append(
            {
                "check_id": "SP002-y-normal-0p10-vs-0p05",
                "case_family": "SP-002 y-normal orientation sensitivity",
                "evidence_files": (
                    f"data/processed/{matched_case}_summary.csv; "
                    f"data/processed/{slow_case}_summary.csv; "
                    f"data/processed/{matched_case}_fragments.csv; "
                    f"data/processed/{slow_case}_fragments.csv"
                ),
                "metric": "y-normal same-template 0.10 to 0.05 m/s comparison",
                "result": (
                    f"peak force change {peak_change:.2f}%; first-break shift {first_break_shift:.5f} mm; "
                    f"fragments {matched_final_frag['largest_fragment_particles']}+{matched_final_frag['second_fragment_particles']} "
                    f"versus {slow_final_frag['largest_fragment_particles']}+{slow_final_frag['second_fragment_particles']}"
                ),
                "interpretation": (
                    "within the y-normal 5846-bond orientation branch, the rate reduction does not materially change "
                    "the load scale, first-break displacement or two-major-fragment topology"
                ),
                "claim_status": "orientation-specific rate-screening support",
                "next_action": "do not conflate with the x-normal CAL1 candidate",
            }
        )

    rows.append(
        {
            "check_id": "SP002-publication-boundary",
            "case_family": "single-pebble calibration claim boundary",
            "evidence_files": (
                "docs/single_pebble_calibration_protocol.md; "
                "figures/sp002/single_pebble_calibration_evidence.svg"
            ),
            "metric": "safe manuscript wording",
            "result": "use current calibration candidate, not final calibrated Li4SiO4 material law",
            "interpretation": (
                "the manuscript can defend template choice for PB-006, but should not claim predictive crush statistics"
            ),
            "claim_status": "wording rule",
            "next_action": "state that y-normal matched reruns are orientation sensitivity; use the x-normal slow rerun for CAL1 rate discussion",
        }
    )

    out = ROOT / "tables/sp002_quasistatic_check.csv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(out)


if __name__ == "__main__":
    main()
