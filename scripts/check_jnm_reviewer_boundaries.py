#!/usr/bin/env python3
"""Check reviewer-risk boundaries for the active JNM manuscript."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
PREBUTTAL = ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md"
RISK_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv"
CLAIM_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv"
AUDIT = ROOT / "docs/jnm_reviewer_boundary_audit_20260613.md"
PROVENANCE = ROOT / "docs/jnm_active_run_provenance_capsule_20260613.md"
MODEL_AUDIT = ROOT / "docs/jnm_model_parameter_consistency_audit_20260613.md"

REQUIRED_MANUSCRIPT_PHRASES = [
    "current calibration candidate",
    "not a final Li4SiO4 material law",
    "event-sequence evidence",
    "not as a converged fracture probability",
    "larger stochastic ensembles",
    "no coupled thermal-flow prediction",
    "not as a measured material stiffness",
    "not to report a bulk elastic modulus",
]

REPOSITORY_AVAILABILITY_PHRASES = [
    "repository DOI/URL to be added",
    "package has been deposited in a persistent repository and is available at",
]

REQUIRED_AUDIT_PHRASES = [
    "JNM reviewer-boundary audit",
    "Boundary map",
    "Prohibited unqualified claims",
    "generic DEM workflow",
    "measured Li4SiO4 stiffness",
    "Do not submit as locally complete",
]

REQUIRED_PREBUTTAL_PHRASES = [
    "not presented as a converged fracture-probability model",
    "final Li4SiO4 constitutive law",
    "blanket design-margin calculation",
    "not a completed transport prediction",
    "Do not call the bed compression fully quasi-static",
]

EXPECTED_RISKS = {f"R{idx}" for idx in range(1, 11)}
EXPECTED_CLAIMS = {f"C{idx}" for idx in range(1, 10)}

RISKY_PATTERNS = {
    "converged failure probability": r"\bconverged failure probability\b",
    "universal onset displacement": r"\buniversal onset displacement\b",
    "lifetime prediction": r"\blifetime prediction\b",
    "design margin": r"\bdesign[- ]margin\b|\bdesign margin\b",
    "final Li4SiO4 material law": r"\bfinal Li4SiO4 material law\b|\bfinal Li4SiO4 constitutive law\b",
    "fully quasi-static": r"\bfully quasi-static\b",
    "coupled thermal-flow prediction": r"\bcoupled thermal-flow prediction\b|\bcompleted transport prediction\b",
    "measured material stiffness": r"\bmeasured material stiffness\b|\bmeasured Li4SiO4 stiffness\b",
}

NEGATION_TERMS = [
    "not ",
    "no ",
    "do not",
    "cannot",
    "without",
    "rather than",
    "avoid",
    "must not",
    "should not",
    "require",
    "requires",
    "before",
    "boundary",
    "limitation",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def risky_hits(text: str, rel: str) -> list[str]:
    hits: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        negated = any(term in lowered for term in NEGATION_TERMS)
        for label, pattern in RISKY_PATTERNS.items():
            if re.search(pattern, line, flags=re.IGNORECASE) and not negated:
                hits.append(f"{rel}:{line_no}:{label}")
    return hits


def main() -> int:
    failures: list[str] = []
    for path in [MANUSCRIPT, PREBUTTAL, RISK_MATRIX, CLAIM_MATRIX, AUDIT, PROVENANCE, MODEL_AUDIT]:
        require(path.exists() and path.stat().st_size > 0, f"missing or empty {path.relative_to(ROOT)}", failures)
    if failures:
        print("FAIL reviewer boundaries")
        for failure in failures:
            print(f"- {failure}")
        return 1

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    prebuttal = PREBUTTAL.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    provenance = PROVENANCE.read_text(encoding="utf-8")
    model_audit = MODEL_AUDIT.read_text(encoding="utf-8")

    for phrase in REQUIRED_MANUSCRIPT_PHRASES:
        require(phrase in manuscript, f"manuscript missing boundary phrase {phrase!r}", failures)
    require(
        any(phrase in manuscript for phrase in REPOSITORY_AVAILABILITY_PHRASES),
        "manuscript missing repository availability placeholder or inserted persistent-repository statement",
        failures,
    )
    for phrase in REQUIRED_AUDIT_PHRASES:
        require(phrase in audit, f"reviewer-boundary audit missing phrase {phrase!r}", failures)
    for phrase in REQUIRED_PREBUTTAL_PHRASES:
        require(phrase in prebuttal, f"prebuttal missing phrase {phrase!r}", failures)

    risk_rows = read_rows(RISK_MATRIX)
    risk_ids = {row.get("risk_id", "").strip() for row in risk_rows}
    require(risk_ids == EXPECTED_RISKS, f"risk matrix ids {sorted(risk_ids)} != {sorted(EXPECTED_RISKS)}", failures)
    for row in risk_rows:
        for column in ["current_evidence", "prebuttal_position", "wording_boundary", "action_before_submission"]:
            require(bool(row.get(column, "").strip()), f"{row.get('risk_id')} has empty {column}", failures)

    claim_rows = read_rows(CLAIM_MATRIX)
    claim_ids = {row.get("claim_id", "").strip() for row in claim_rows}
    require(claim_ids == EXPECTED_CLAIMS, f"claim matrix ids {sorted(claim_ids)} != {sorted(EXPECTED_CLAIMS)}", failures)
    for row in claim_rows:
        require(row.get("reviewer_risk_link", "").strip() in EXPECTED_RISKS, f"{row.get('claim_id')} has invalid risk link", failures)
        require(bool(row.get("wording_boundary", "").strip()), f"{row.get('claim_id')} has empty wording boundary", failures)

    for rel, text in [
        (MANUSCRIPT.relative_to(ROOT).as_posix(), manuscript),
        (PREBUTTAL.relative_to(ROOT).as_posix(), prebuttal),
    ]:
        hits = risky_hits(text, rel)
        if hits:
            failures.append("unqualified risky claims: " + "; ".join(hits))

    require("1.5e10 Pa" in manuscript, "manuscript missing 1.5e10 Pa protocol value", failures)
    require("1.5e10 Pa" in provenance and "not a final Li4SiO4 material law" in provenance, "provenance missing 1.5e10 Pa protocol boundary", failures)
    require("1.5e10 Pa" in model_audit and "not a final Li4SiO4 material law" in model_audit, "model audit missing 1.5e10 Pa protocol boundary", failures)
    require("60 micrometre endpoint is not treated" in provenance, "provenance missing 60 um endpoint force-balance boundary", failures)
    require("The 60 micrometre endpoint is not treated" in audit, "reviewer-boundary audit missing 60 um endpoint boundary", failures)

    result = subprocess.run(
        ["python3", "scripts/check_jnm_active_run_provenance.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        failures.append("active-run provenance subcheck failed: " + (result.stdout + result.stderr).strip())

    if failures:
        print("FAIL reviewer boundaries")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "PASS reviewer boundaries: JNM scope, calibration, ensemble-size, contact-modulus, topology, rate and DOI boundaries are consistent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
