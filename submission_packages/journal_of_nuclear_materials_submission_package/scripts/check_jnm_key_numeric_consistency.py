#!/usr/bin/env python3
"""Check that key manuscript numbers match the processed JNM evidence tables."""

from __future__ import annotations

import csv
import math
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
AUDIT = ROOT / "docs/jnm_key_numeric_consistency_audit_20260613.md"
EVENTS = ROOT / "data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv"
PILOT_ACCEPTANCE = ROOT / "tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_acceptance_summary.csv"
PILOT_NATIVE = ROOT / "tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_summary.csv"
MACRO = ROOT / "tables/pb007_macro_topology_event_metrics.csv"
MECHANISM = ROOT / "tables/jnm_material_degradation_mechanism_indices.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def contains(text: str, phrase: str) -> bool:
    return phrase.lower() in text.lower()


def main() -> int:
    failures: list[str] = []
    for path in [MANUSCRIPT, AUDIT, EVENTS, PILOT_ACCEPTANCE, PILOT_NATIVE, MACRO, MECHANISM]:
        require(path.exists() and path.stat().st_size > 0, f"missing or empty {path.relative_to(ROOT)}", failures)
    if failures:
        print("FAIL key numeric consistency: " + "; ".join(failures))
        return 1

    text = MANUSCRIPT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    events = read_rows(EVENTS)
    acceptance = read_rows(PILOT_ACCEPTANCE)[0]
    native = read_rows(PILOT_NATIVE)[0]
    macro = {row["case_label"]: row for row in read_rows(MACRO)}
    mechanism = {row["metric"]: row for row in read_rows(MECHANISM)}

    disps = [round(float(row["top_displacement_mm"]) * 1000.0) for row in events]
    deltas = [int(row["new_broken_bonds"]) for row in events]
    cumulative = [int(row["cumulative_broken_bonds"]) for row in events]
    pebble_ids = {int(row["pebble_id"]) for row in events}
    ranks = {int(row["rank_from_top"]) for row in events}
    final_initial = int(acceptance["initial_intact_bonds"])
    final_min = int(acceptance["minimum_intact_bonds"])
    final_broken = final_initial - final_min
    final_native_edges = int(native["inter_pebble_edges"])
    final_native_subcontacts = int(native["inter_pebble_subcontacts"])
    final_top_reachable = int(native["top_reachable_mother_pebbles"])
    final_bottom_reachable = int(native["bottom_mothers_reachable_from_top"])
    pilot = macro["pilot_localized_microcracking"]
    independent = macro["seed02_intact_to_60um"]
    force_relax = float(mechanism["peak_to_endpoint_force_relaxation"]["value"])
    edge_densification = float(mechanism["inter_mother_edge_densification"]["value"])
    reach_densification = float(mechanism["top_reachability_densification"]["value"])

    expected_pairs = [
        ("493,500", final_initial),
        ("493,495", final_min),
        ("five lost bonds", final_broken),
        ("25, 35 and 60 micrometres", disps),
        ("+2, +2 and +1", deltas),
        ("mother pebble 78", sorted(pebble_ids)),
        ("rank from top 2", sorted(ranks)),
        ("74 inter-mother edges", final_native_edges),
        ("119 inter-pebble subcontacts", final_native_subcontacts),
        ("57 mother pebbles reachable", final_top_reachable),
        ("11 bottom-contacting mother pebbles", final_bottom_reachable),
        ("46.4%", force_relax),
        ("1.44x", edge_densification),
        ("1.35x", reach_densification),
        ("83 inter-mother edges", int(independent["final_inter_mother_edges"])),
        ("18 bottom-contacting mother pebbles", int(independent["final_bottom_reachable_from_top"])),
    ]

    require(disps == [25, 35, 60], f"event displacements are {disps}, expected [25, 35, 60]", failures)
    require(deltas == [2, 2, 1], f"event increments are {deltas}, expected [2, 2, 1]", failures)
    require(cumulative[-1] == 5 and final_broken == 5, "pilot final broken-bond count is not 5", failures)
    require(pebble_ids == {78}, f"event pebble ids are {sorted(pebble_ids)}, expected [78]", failures)
    require(ranks == {2}, f"event rank set is {sorted(ranks)}, expected [2]", failures)
    require(math.isclose(force_relax, 0.4643, rel_tol=1e-4), f"force relaxation {force_relax} != 0.4643", failures)
    require(math.isclose(edge_densification, 1.436, rel_tol=1e-4), f"edge densification {edge_densification} != 1.436", failures)
    require(math.isclose(reach_densification, 1.354, rel_tol=1e-4), f"reach densification {reach_densification} != 1.354", failures)
    require(int(independent["broken_bonds_at_endpoint"]) == 0, "independent bed endpoint broken bonds are not zero", failures)
    require(int(macro["seed02_strength0p5_intact_to_60um"]["broken_bonds_at_endpoint"]) == 0, "0.5x audit endpoint broken bonds are not zero", failures)
    require(int(macro["seed02_strength0p25_intact_to_60um"]["broken_bonds_at_endpoint"]) == 0, "0.25x audit endpoint broken bonds are not zero", failures)

    for phrase, value in expected_pairs:
        require(contains(text, phrase), f"manuscript missing key phrase {phrase!r} for value {value}", failures)
        require(contains(audit, phrase), f"audit missing key phrase {phrase!r} for value {value}", failures)

    require(
        re.search(r"0\.5x and 0\.25x", text) is not None,
        "manuscript missing 0.5x/0.25x strength-audit wording",
        failures,
    )
    require(
        contains(text, "not a converged fracture probability")
        or contains(text, "should not be interpreted as a converged fracture probability"),
        "manuscript missing probability boundary",
        failures,
    )

    if failures:
        print("FAIL key numeric consistency")
        for failure in failures:
            print(f"- {failure}")
        return 1

    subchecks = [
        ("model-parameter", "scripts/check_jnm_model_parameter_consistency.py"),
        ("active-run provenance", "scripts/check_jnm_active_run_provenance.py"),
    ]
    for label, script in subchecks:
        result = subprocess.run(
            ["python3", script],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            print(f"FAIL key numeric consistency: {label} subcheck failed")
            print((result.stdout + result.stderr).strip())
            return 1

    print(
        "PASS key numeric consistency: manuscript key event, bond-count, force-network, mechanism-index, model-parameter and active-run provenance values match processed evidence"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
