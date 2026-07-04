#!/usr/bin/env python3
"""Check the CPM reviewer-risk preflight matrix against current files."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CSV_PATH = DOCS / "cpm_reviewer_risk_preflight_20260704.csv"
MD_PATH = DOCS / "cpm_reviewer_risk_preflight_20260704.md"
MANUSCRIPT = ROOT / "manuscript"

EXPECTED_RISKS = {
    "Novelty and literature rationale",
    "Material-property dependence",
    "Statistical scope",
    "Single-particle template credibility",
    "Artificial pre-loading damage",
    "Reproducibility and raw-data handling",
    "Journal scope",
}

REQUIRED_TEXT = {
    MANUSCRIPT / "repaired_full_submission_draft.md": [
        "finite 100-particle windows",
        "Quantitative fracture probability",
        "require larger random ensembles",
        "bonded-particle strength jointly control early fracture",
        "Li4SiO4 as a representative brittle ceramic pebble",
    ],
    MANUSCRIPT / "computational_particle_mechanics_cover_letter.md": [
        "packed brittle-particle fracture",
        "chronological link between a load-bearing contact network",
        "Li4SiO4 is used as a representative brittle ceramic application material",
    ],
    DOCS / "cpm_literature_gap_map_20260704.md": [
        "Particle-replacement and crushable-bed DEM",
        "Bonded-particle fracture modelling",
    ],
    DOCS / "cpm_submission_readiness_report_20260704.md": [
        "ready_for_live_submission_after_external_metadata",
        "Missing coauthor e-mail addresses: `7`",
    ],
}

FORBIDDEN_READER_TERMS = re.compile(
    r"\b(repaired version|Advanced Powder|Journal of Nuclear Materials|Nuclear Fusion|"
    r"CAL|SP-00|PB-00|converged stochastic failure probability)\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def existing_path(pattern_or_path: str) -> bool:
    if "*" in pattern_or_path:
        return bool(list(ROOT.glob(pattern_or_path)))
    return (ROOT / pattern_or_path).exists()


def main() -> None:
    if not CSV_PATH.exists() or not MD_PATH.exists():
        fail("missing reviewer-risk preflight output")

    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8")))
    risks = {row["risk"] for row in rows}
    if risks != EXPECTED_RISKS:
        fail(f"risk rows mismatch: {sorted(risks ^ EXPECTED_RISKS)}")
    if len(rows) != 7:
        fail(f"expected 7 reviewer-risk rows, found {len(rows)}")
    if {row["status"] for row in rows} - {"reduced", "bounded"}:
        fail("unexpected status in reviewer-risk matrix")

    for row in rows:
        for item in row["evidence"].split(";"):
            evidence = item.strip()
            if not evidence:
                continue
            if not existing_path(evidence):
                fail(f"missing evidence path for {row['risk']}: {evidence}")

    for path, terms in REQUIRED_TEXT.items():
        text = path.read_text(encoding="utf-8", errors="ignore")
        missing = [term for term in terms if term not in text]
        if missing:
            fail(f"{path} missing required terms: {missing}")

    for path in [
        MANUSCRIPT / "repaired_full_submission_draft.md",
        MANUSCRIPT / "computational_particle_mechanics_cover_letter.md",
        MANUSCRIPT / "computational_particle_mechanics_editorial_fields.md",
    ]:
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = FORBIDDEN_READER_TERMS.search(text)
        if match:
            fail(f"reader-facing residue in {path}: {match.group(0)!r}")

    print("PASS CPM reviewer-risk preflight: 7 risks mapped to current evidence and boundaries")


if __name__ == "__main__":
    main()
