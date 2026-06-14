#!/usr/bin/env python3
"""Check the accepted PB-007 run-to-figure provenance capsule."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_ID = "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot"
CASE_DIR = ROOT / "simulations/pebble_bed/PB-007/cases" / CASE_ID
DOC = ROOT / "docs/jnm_active_run_provenance_capsule_20260613.md"
SOURCE_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv"
WRAPPER = ROOT / "scripts/run_pb007_bonded_step_relaxed_validation.sh"
POSTPROCESS = ROOT / "scripts/postprocess_pb007_corrected_fracture_pilot.sh"
SCREEN = CASE_DIR / f"screen_{CASE_ID}.log"
INPUT = CASE_DIR / "in.pb007_bonded_step_relaxed_validation.lmp"
METADATA = CASE_DIR / "data/bonded_template_metadata.csv"
THERMO = ROOT / f"data/processed/{CASE_ID}_thermo.csv"
EVENTS = ROOT / f"data/processed/{CASE_ID}_breakage_events.csv"
BOND_SERIES = ROOT / f"data/processed/{CASE_ID}_bond_series.csv"
NATIVE_SERIES = ROOT / f"data/processed/{CASE_ID}_native_force_network_series.csv"
ACCEPTANCE = ROOT / f"tables/pb007_{CASE_ID}_acceptance_summary.csv"
NATIVE_SUMMARY = ROOT / f"tables/pb007_{CASE_ID}_native_summary.csv"


REQUIRED_PATHS = [
    DOC,
    SOURCE_MATRIX,
    WRAPPER,
    POSTPROCESS,
    SCREEN,
    INPUT,
    CASE_DIR / "log.liggghts",
    METADATA,
    CASE_DIR / "post/bonds_final.local",
    CASE_DIR / "post/pairs_final.local",
    CASE_DIR / "post/walls_final.local",
    THERMO,
    EVENTS,
    BOND_SERIES,
    NATIVE_SERIES,
    ACCEPTANCE,
    NATIVE_SUMMARY,
    ROOT / "figures/pb007/pb007_acceptance_gate_validation.pdf",
    ROOT / "figures/pb007/pb007_corrected_fracture_sequence.pdf",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []

    for path in REQUIRED_PATHS:
        require(path.exists(), f"missing {path.relative_to(ROOT)}", failures)
        if path.exists() and path.is_file():
            require(path.stat().st_size > 0, f"empty {path.relative_to(ROOT)}", failures)
    if failures:
        print("FAIL active-run provenance")
        for failure in failures:
            print(f"- {failure}")
        return 1

    doc = DOC.read_text(encoding="utf-8")
    screen = SCREEN.read_text(errors="replace")
    wrapper = WRAPPER.read_text(encoding="utf-8")
    postprocess = POSTPROCESS.read_text(encoding="utf-8")
    matrix_rows = {row["item"]: row for row in read_rows(SOURCE_MATRIX)}
    metadata = read_rows(METADATA)
    events = read_rows(EVENTS)
    acceptance = read_rows(ACCEPTANCE)[0]
    native = read_rows(NATIVE_SUMMARY)[0]

    for phrase in [
        CASE_ID,
        "wrapper and screen log are the runtime authority",
        "not a final Li4SiO4 material law",
        "59.6%",
        "final `run 0`",
    ]:
        require(phrase in doc, f"capsule missing phrase {phrase!r}", failures)
    require(
        "not treated" in doc and "quasi-static force-balance" in doc,
        "capsule missing 60 um quasi-static force-balance boundary",
        failures,
    )

    for phrase in [
        "-var young",
        "-var n_increments",
        "-var hold_steps",
        "-var bond_dump_every",
        "-var native_dump_every",
        "extract_liggghts_thermo.py",
    ]:
        require(phrase in wrapper, f"wrapper missing {phrase}", failures)

    for phrase in [
        "analyze_pb007_native_force_network.py",
        "analyze_pb007_native_force_network_series.py",
        "summarize_pb007_loadpath_validation.py",
        "analyze_pb007_bond_event_sequence.py",
    ]:
        require(phrase in postprocess, f"postprocess driver missing {phrase}", failures)

    for pattern, label in [
        (r"youngsModulus peratomtype 1\.5e10 1\.5e10 1\.5e10", "expanded restored modulus"),
        (r"timestep\s+5\.0e-9", "expanded timestep"),
        (r"variable\s+top_disp equal 60\*0\.2\*5\.0e-9\*1000", "final displacement expression"),
        (r"run\s+1000", "hold-step expansion"),
        (r"130001\s+50000\s+4\.2398608e-08\s+6e-05\s+0\.1577665.*493495", "final physical thermo row"),
    ]:
        require(re.search(pattern, screen) is not None, f"screen log missing {label}", failures)

    require(len(metadata) == 100, f"metadata has {len(metadata)} rows, expected 100", failures)
    rms_max = max(float(row["coordinate_fit_rms_m"]) for row in metadata)
    require(rms_max < 1.0e-8, f"metadata RMS max {rms_max:.3e} m is not <1e-8 m", failures)

    displacements_um = [round(float(row["top_displacement_mm"]) * 1000.0) for row in events]
    broken = [int(row["new_broken_bonds"]) for row in events]
    require(displacements_um == [25, 35, 60], f"event displacements {displacements_um} != [25, 35, 60]", failures)
    require(broken == [2, 2, 1], f"event increments {broken} != [2, 2, 1]", failures)
    require({int(row["pebble_id"]) for row in events} == {78}, "events are not localized to mother pebble 78", failures)
    require({int(row["rank_from_top"]) for row in events} == {2}, "events are not rank-from-top 2", failures)

    require(int(acceptance["initial_intact_bonds"]) == 493500, "initial intact bonds are not 493500", failures)
    require(int(acceptance["minimum_intact_bonds"]) == 493495, "minimum intact bonds are not 493495", failures)
    require(float(acceptance["final_top_displacement_um"]) == 60.0, "final displacement is not 60 um", failures)
    require(float(acceptance["incremental_wall_balance_residual_percent"]) > 50.0, "60 um residual boundary is not recorded", failures)
    require(int(native["inter_pebble_edges"]) == 74, "final native inter-pebble edges are not 74", failures)
    require(int(native["top_reachable_mother_pebbles"]) == 57, "final top-reachable count is not 57", failures)
    require(int(native["bottom_mothers_reachable_from_top"]) == 11, "final bottom-reachable count is not 11", failures)

    parameter_table = matrix_rows.get("Table3", {})
    for rel in [
        "docs/jnm_model_parameter_consistency_audit_20260613.md",
        "docs/jnm_active_run_provenance_capsule_20260613.md",
    ]:
        require(rel in parameter_table.get("source_data_files", ""), f"Table3 source-data matrix missing {rel}", failures)
    require(
        "scripts/check_jnm_active_run_provenance.py" in parameter_table.get("generation_or_audit_scripts", ""),
        "Table3 source-data matrix missing active-run provenance checker",
        failures,
    )

    if failures:
        print("FAIL active-run provenance")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "PASS active-run provenance: accepted PB-007 case, runtime parameters, raw dumps, processed outputs and Table 3 source mapping are traceable"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
