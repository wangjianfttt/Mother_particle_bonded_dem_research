#!/usr/bin/env python3
"""Check that JNM manuscript model parameters match representative inputs/logs."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
AUDIT = ROOT / "docs/jnm_model_parameter_consistency_audit_20260613.md"
PB007_INPUT = ROOT / "simulations/pebble_bed/PB-007/in.pb007_bonded_step_relaxed_validation.lmp"
PB007_CASE_INPUT = (
    ROOT
    / "simulations/pebble_bed/PB-007/cases/"
    / "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/"
    / "in.pb007_bonded_step_relaxed_validation.lmp"
)
PB007_SCREEN = (
    ROOT
    / "simulations/pebble_bed/PB-007/cases/"
    / "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/"
    / "screen_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot.log"
)
PB007_ACCEPTANCE = ROOT / (
    "tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot"
    "_acceptance_summary.csv"
)
PB007_WRAPPER = ROOT / "scripts/run_pb007_bonded_step_relaxed_validation.sh"
SP_INPUT = ROOT / "simulations/single_pebble/SP-SURFACE/cases/SP-SURFACE-500-S260/in.resolution_compression.lmp"
TEMPLATE_METADATA = (
    ROOT
    / "simulations/pebble_bed/PB-007/cases/"
    / "PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot/"
    / "data/bonded_template_metadata.csv"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def contains(text: str, phrase: str) -> bool:
    return phrase.lower() in text.lower()


def csv_first(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return next(csv.DictReader(handle))


def main() -> int:
    failures: list[str] = []
    paths = [
        MANUSCRIPT,
        AUDIT,
        PB007_INPUT,
        PB007_CASE_INPUT,
        PB007_SCREEN,
        PB007_ACCEPTANCE,
        PB007_WRAPPER,
        SP_INPUT,
        TEMPLATE_METADATA,
    ]
    for path in paths:
        require(path.exists() and path.stat().st_size > 0, f"missing or empty {path.relative_to(ROOT)}", failures)
    if failures:
        print("FAIL model parameter consistency: " + "; ".join(failures))
        return 1

    manuscript = read_text(MANUSCRIPT)
    audit = read_text(AUDIT)
    pb007_input = read_text(PB007_INPUT)
    pb007_case_input = read_text(PB007_CASE_INPUT)
    pb007_screen = read_text(PB007_SCREEN)
    wrapper = read_text(PB007_WRAPPER)
    sp_input = read_text(SP_INPUT)
    acceptance = csv_first(PB007_ACCEPTANCE)

    manuscript_phrases = [
        "density 2400 kg m-3",
        "Young's modulus 90 GPa",
        "Poisson ratio 0.25",
        "restitution coefficient 0.3",
        "friction coefficient 0.5",
        "1.0e14 and 5.0e13 N m-3",
        "90 MPa",
        "22.5 MPa",
        "0.20 mm",
        "0.09 mm",
        "5.0 ns timestep",
        "restored contact modulus 1.5e10 Pa",
        "10,000 pre-compression relaxation steps",
        "4935 internal bonds per mother pebble",
        "493,500 bonds for the 100-mother-pebble bed",
    ]
    for phrase in manuscript_phrases:
        require(contains(manuscript, phrase), f"manuscript missing parameter phrase {phrase!r}", failures)
        require(contains(audit, phrase), f"audit missing parameter phrase {phrase!r}", failures)

    input_pairs = [
        (pb007_input, "variable        nspheres       index 500", "PB-007 nspheres"),
        (pb007_input, "variable        dt             index 5.0e-9", "PB-007 dt"),
        (pb007_input, "variable        rho            equal 2400.0", "PB-007 density"),
        (pb007_input, "variable        poisson        equal 0.25", "PB-007 Poisson"),
        (pb007_input, "variable        cor            equal 0.3", "PB-007 restitution"),
        (pb007_input, "variable        mu             equal 0.5", "PB-007 friction"),
        (pb007_input, "variable        kn_bond        index 1.0e14", "PB-007 normal bond stiffness"),
        (pb007_input, "variable        kt_bond        index 5.0e13", "PB-007 tangential bond stiffness"),
        (pb007_input, "variable        sigma_bulk     index 9.0e7", "PB-007 bulk normal strength"),
        (pb007_input, "variable        tau_bulk       index 9.0e7", "PB-007 bulk tangential strength"),
        (pb007_input, "variable        sigma_weak     index 2.25e7", "PB-007 weak normal strength"),
        (pb007_input, "variable        tau_weak       index 2.25e7", "PB-007 weak tangential strength"),
        (pb007_input, "variable        create_dist    equal 2.00e-4", "PB-007 bulk creation distance"),
        (pb007_input, "variable        create_weak    equal 9.00e-5", "PB-007 weak creation distance"),
        (pb007_case_input, "variable        young          index 5.0e6", "case input default Young value documented as overrideable"),
        (wrapper, 'young="${10:-5.0e6}"', "wrapper Young argument"),
        (wrapper, '-var young "$young"', "wrapper Young override"),
        (sp_input, "variable        young            equal 9.0e10", "single-pebble Young modulus"),
        (sp_input, "variable        top_vz           index -0.1", "single-pebble loading rate"),
    ]
    for text, phrase, label in input_pairs:
        require(phrase in text, f"missing {label}: {phrase!r}", failures)

    runtime_patterns = [
        (r"youngsModulus peratomtype 1\.5e10 1\.5e10 1\.5e10", "runtime restored contact modulus"),
        (r"timestep\s+5\.0e-9", "runtime timestep"),
        (r"normalBondStiffnessPerUnitArea.*1\.0e14 1\.0e14 1\.0e14", "runtime normal bond stiffness"),
        (r"tangentialBondStiffnessPerUnitArea.*5\.0e13 5\.0e13 5\.0e13", "runtime tangential bond stiffness"),
        (r"maxSigmaBond.*9\.0e7 2\.25e7 9\.0e7", "runtime normal/weak strength matrix"),
        (r"maxTauBond.*9\.0e7 2\.25e7 9\.0e7", "runtime tangential/weak strength matrix"),
        (r"createDistanceBond.*0\.0002 9e-05 0\.0002", "runtime creation-distance matrix"),
        (r"variable\s+top_disp equal 60\*0\.2\*5\.0e-9\*1000", "runtime 60 micrometre displacement expression"),
        (r"\s130001\s+50000\s+.*\s6e-05\s+", "runtime final accepted displacement row"),
    ]
    for pattern, label in runtime_patterns:
        require(re.search(pattern, pb007_screen) is not None, f"missing {label} in PB-007 screen log", failures)

    initial = int(acceptance["initial_intact_bonds"])
    final_min = int(acceptance["minimum_intact_bonds"])
    final_um = float(acceptance["final_top_displacement_um"])
    baseline = int(acceptance["baseline_step"])
    require(initial == 493500, f"acceptance initial bonds {initial} != 493500", failures)
    require(final_min == 493495, f"acceptance final minimum intact bonds {final_min} != 493495", failures)
    require(abs(final_um - 60.0) < 1e-9, f"acceptance displacement {final_um} um != 60.0", failures)
    require(baseline == 10001, f"acceptance baseline step {baseline} != 10001", failures)

    with TEMPLATE_METADATA.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 100, f"template metadata rows {len(rows)} != 100 mother pebbles", failures)
    rms_values = [float(row["coordinate_fit_rms_m"]) for row in rows]
    require(max(rms_values) < 1.0e-8, f"template coordinate-fit RMS max {max(rms_values):.3e} m >= 1e-8 m", failures)

    require(
        contains(audit, "not the template default") and contains(audit, "run 0"),
        "audit missing wrapper/default and run-0 caveat",
        failures,
    )

    if failures:
        print("FAIL model parameter consistency")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "PASS model parameter consistency: manuscript Methods/Table 2 parameters match active PB-007 logs, wrapper overrides and single-pebble inputs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
