#!/usr/bin/env python3
"""Build a model-side calibration matrix from existing SP-002 outputs."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CASES = [
    {
        "case_id": "SP-002-strength-25MPa",
        "thermo_csv": "data/processed/SP-002-strength-25MPa_thermo.csv",
        "summary_csv": "data/processed/SP-002-strength-25MPa_summary.csv",
        "fragment_csv": "",
        "top_speed_m_s": 1.0,
        "sigma_tau_MPa": 25.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "fast strength-screening case",
    },
    {
        "case_id": "SP-002-strength-50MPa",
        "thermo_csv": "data/processed/SP-002-strength-50MPa_thermo.csv",
        "summary_csv": "data/processed/SP-002-strength-50MPa_summary.csv",
        "fragment_csv": "",
        "top_speed_m_s": 1.0,
        "sigma_tau_MPa": 50.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "fast strength-screening case",
    },
    {
        "case_id": "SP-002-strength-100MPa",
        "thermo_csv": "data/processed/SP-002-strength-100MPa_thermo.csv",
        "summary_csv": "data/processed/SP-002-strength-100MPa_summary.csv",
        "fragment_csv": "",
        "top_speed_m_s": 1.0,
        "sigma_tau_MPa": 100.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "fast strength-screening case",
    },
    {
        "case_id": "SP-002-speed-0p1ms-50MPa-bonds",
        "thermo_csv": "data/processed/SP-002-speed-0p1ms-50MPa-bonds_thermo.csv",
        "summary_csv": "data/processed/SP-002-speed-0p1ms-50MPa-bonds_summary.csv",
        "fragment_csv": "data/processed/SP-002-speed-0p1ms-50MPa-bonds_fragments.csv",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 50.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "current fragment-reference case",
    },
    {
        "case_id": "SP-002-speed-0p25ms-50MPa",
        "thermo_csv": "data/processed/SP-002-speed-0p25ms-50MPa_thermo.csv",
        "summary_csv": "data/processed/SP-002-speed-0p25ms-50MPa_summary.csv",
        "fragment_csv": "",
        "top_speed_m_s": 0.25,
        "sigma_tau_MPa": 50.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "speed-screening case",
    },
    {
        "case_id": "SP-002-speed-0p5ms-50MPa",
        "thermo_csv": "data/processed/SP-002-speed-0p5ms-50MPa_thermo.csv",
        "summary_csv": "data/processed/SP-002-speed-0p5ms-50MPa_summary.csv",
        "fragment_csv": "",
        "top_speed_m_s": 0.5,
        "sigma_tau_MPa": 50.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "speed-screening case",
    },
    {
        "case_id": "SP-002-stiffness-kn5e13",
        "thermo_csv": "data/processed/SP-002-stiffness-kn5e13_thermo.csv",
        "summary_csv": "data/processed/SP-002-stiffness-kn5e13_summary.csv",
        "stiffness_csv": "data/processed/SP-002-stiffness-kn5e13_initial_stiffness.csv",
        "fragment_csv": "",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 50.0,
        "kn_N_m3": 5.0e13,
        "kt_N_m3": 2.5e13,
        "notes": "stiffness-screening case",
    },
    {
        "case_id": "SP-002-stiffness-kn1e14",
        "thermo_csv": "data/processed/SP-002-stiffness-kn1e14_thermo.csv",
        "summary_csv": "data/processed/SP-002-stiffness-kn1e14_summary.csv",
        "stiffness_csv": "data/processed/SP-002-stiffness-kn1e14_initial_stiffness.csv",
        "fragment_csv": "",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 50.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "stiffness-screening case",
    },
    {
        "case_id": "SP-002-calib-kn1e14-120MPa-0p1ms",
        "thermo_csv": "data/processed/SP-002-calib-kn1e14-120MPa-0p1ms_thermo.csv",
        "summary_csv": "data/processed/SP-002-calib-kn1e14-120MPa-0p1ms_summary.csv",
        "stiffness_csv": "data/processed/SP-002-calib-kn1e14-120MPa-0p1ms_initial_stiffness.csv",
        "fragment_csv": "data/processed/SP-002-calib-kn1e14-120MPa-0p1ms_fragments.csv",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 120.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "first load-calibrated candidate; peak force in target window but fragment mode is surface chipping",
    },
    {
        "case_id": "SP-002-calib-kn1e14-sig120-tau60-0p1ms",
        "thermo_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau60-0p1ms_thermo.csv",
        "summary_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau60-0p1ms_summary.csv",
        "stiffness_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau60-0p1ms_initial_stiffness.csv",
        "fragment_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau60-0p1ms_fragments.csv",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 120.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "tau/sigma=0.5 diagnostic; peak force too low and still surface chipping",
    },
    {
        "case_id": "SP-002-calib-kn1e14-sig120-tau240-0p1ms",
        "thermo_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau240-0p1ms_thermo.csv",
        "summary_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau240-0p1ms_summary.csv",
        "stiffness_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau240-0p1ms_initial_stiffness.csv",
        "fragment_csv": "data/processed/SP-002-calib-kn1e14-sig120-tau240-0p1ms_fragments.csv",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 120.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "tau/sigma=2.0 diagnostic; peak force near target but still surface chipping",
    },
    {
        "case_id": "SP-002-weakplane-bulk120-weak60-cd110-0p1ms-0p3mm",
        "thermo_csv": "data/processed/SP-002-weakplane-bulk120-weak60-cd110-0p1ms-0p3mm_thermo.csv",
        "summary_csv": "data/processed/SP-002-weakplane-bulk120-weak60-cd110-0p1ms-0p3mm_summary.csv",
        "stiffness_csv": "data/processed/SP-002-weakplane-bulk120-weak60-cd110-0p1ms-0p3mm_initial_stiffness.csv",
        "fragment_csv": "data/processed/SP-002-weakplane-bulk120-weak60-cd110-0p1ms-0p3mm_fragments.csv",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 120.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "weak-plane diagnostic; major split achieved but peak force too high",
    },
    {
        "case_id": "SP-002-weakplane-bulk100-weak25-cd90-0p1ms-0p3mm",
        "thermo_csv": "data/processed/SP-002-weakplane-bulk100-weak25-cd90-0p1ms-0p3mm_thermo.csv",
        "summary_csv": "data/processed/SP-002-weakplane-bulk100-weak25-cd90-0p1ms-0p3mm_summary.csv",
        "stiffness_csv": "data/processed/SP-002-weakplane-bulk100-weak25-cd90-0p1ms-0p3mm_initial_stiffness.csv",
        "fragment_csv": "data/processed/SP-002-weakplane-bulk100-weak25-cd90-0p1ms-0p3mm_fragments.csv",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 100.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "weak-plane near-calibrated candidate; load at upper edge and major split achieved",
    },
    {
        "case_id": "SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm",
        "thermo_csv": "data/processed/SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm_thermo.csv",
        "summary_csv": "data/processed/SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm_summary.csv",
        "stiffness_csv": "data/processed/SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm_initial_stiffness.csv",
        "fragment_csv": "data/processed/SP-002-weakplane-bulk90-weak22p5-cd90-0p1ms-0p3mm_fragments.csv",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 90.0,
        "kn_N_m3": 1.0e14,
        "kt_N_m3": 5.0e13,
        "notes": "SP-002-CAL1 weak-plane candidate; peak load in target window and major split achieved",
    },
    {
        "case_id": "SP-002-stiffness-kn2e14",
        "thermo_csv": "data/processed/SP-002-stiffness-kn2e14_thermo.csv",
        "summary_csv": "data/processed/SP-002-stiffness-kn2e14_summary.csv",
        "stiffness_csv": "data/processed/SP-002-stiffness-kn2e14_initial_stiffness.csv",
        "fragment_csv": "",
        "top_speed_m_s": 0.1,
        "sigma_tau_MPa": 50.0,
        "kn_N_m3": 2.0e14,
        "kt_N_m3": 1.0e14,
        "notes": "rejected until smaller-timestep verification",
    },
]


def metric_dict(path: str) -> dict[str, str]:
    if not path:
        return {}
    full = ROOT / path
    if not full.exists():
        return {}
    with full.open(newline="") as f:
        rows = list(csv.reader(f))
    return {row[0]: row[1] for row in rows[1:] if len(row) >= 2}


def final_fragments(path: str) -> dict[str, str]:
    if not path:
        return {}
    full = ROOT / path
    if not full.exists():
        return {}
    with full.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-1] if rows else {}


def main() -> None:
    out = ROOT / "tables/single_pebble_model_calibration_matrix.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "case_id",
        "mother_diameter_mm",
        "subparticles",
        "initial_bonds",
        "top_speed_m_s",
        "sigma_tau_MPa",
        "kn_N_m3",
        "kt_N_m3",
        "estimated_initial_stiffness_N_per_mm",
        "peak_top_force_N",
        "peak_bottom_force_N",
        "first_break_displacement_mm",
        "final_broken_bonds",
        "final_fragment_count",
        "largest_fragment_particles",
        "second_fragment_particles",
        "single_particle_fragments",
        "calibration_status",
        "notes",
        "thermo_csv",
    ]

    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for case in CASES:
            summary = metric_dict(case["summary_csv"])
            stiffness = metric_dict(case.get("stiffness_csv", ""))
            fragments = final_fragments(case.get("fragment_csv", ""))
            rejected = "rejected" in case["notes"]
            writer.writerow(
                {
                    "case_id": case["case_id"],
                    "mother_diameter_mm": 1.0,
                    "subparticles": 500,
                    "initial_bonds": 6723,
                    "top_speed_m_s": case["top_speed_m_s"],
                    "sigma_tau_MPa": case["sigma_tau_MPa"],
                    "kn_N_m3": case["kn_N_m3"],
                    "kt_N_m3": case["kt_N_m3"],
                    "estimated_initial_stiffness_N_per_mm": stiffness.get("initial_stiffness_N_per_mm", ""),
                    "peak_top_force_N": summary.get("peak_top_force_N", ""),
                    "peak_bottom_force_N": summary.get("peak_bottom_force_N", ""),
                    "first_break_displacement_mm": summary.get("first_break_displacement_mm", ""),
                    "final_broken_bonds": summary.get("final_broken_bonds", ""),
                    "final_fragment_count": fragments.get("fragment_count", ""),
                    "largest_fragment_particles": fragments.get("largest_fragment_particles", ""),
                    "second_fragment_particles": fragments.get("second_fragment_particles", ""),
                    "single_particle_fragments": fragments.get("single_particle_fragments", ""),
                    "calibration_status": "candidate_calibrated" if "SP-002-CAL1" in case["notes"] else "exclude_numerical_failure" if rejected else "model_side_metric_only",
                    "notes": case["notes"],
                    "thermo_csv": case["thermo_csv"],
                }
            )

    print(out)


if __name__ == "__main__":
    main()
