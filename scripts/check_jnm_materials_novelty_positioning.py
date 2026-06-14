#!/usr/bin/env python3
"""Check the JNM materials-novelty positioning audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/jnm_materials_novelty_positioning_matrix_20260613.md"
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
COVER_LETTER = ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md"
PREBUTTAL = ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md"


def require(text: str, needles: list[str], label: str, failures: list[str]) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        failures.append(f"{label}: missing {missing}")


def main() -> int:
    failures: list[str] = []
    for path in [AUDIT, MANUSCRIPT, COVER_LETTER, PREBUTTAL]:
        if not path.exists() or path.stat().st_size == 0:
            failures.append(f"missing or empty file: {path.relative_to(ROOT)}")

    if failures:
        print("FAIL materials-novelty positioning: " + "; ".join(failures))
        return 1

    audit = AUDIT.read_text()
    manuscript = MANUSCRIPT.read_text()
    cover = COVER_LETTER.read_text()
    prebuttal = PREBUTTAL.read_text()
    combined = "\n".join([manuscript, cover, prebuttal])

    require(
        audit,
        [
            "Core editorial thesis",
            "Positioning matrix",
            "Reviewer-facing one-paragraph argument",
            "Do-not-cross boundaries",
            "Li4SiO4 ceramic breeder-material degradation",
            "mother-pebble-resolved fracture-event sequences",
            "local force-path sensitivity evidence",
        ],
        "audit structure",
        failures,
    )
    require(
        combined,
        [
            "functional ceramic breeder materials",
            "native force",
            "mother-pebble",
            "calibration candidate",
            "converged failure probability",
            "coupled thermal-flow",
        ],
        "manuscript/support positioning",
        failures,
    )
    require(
        cover,
        [
            "distinct from a generic DEM-method paper",
            "nuclear-application materials research",
            "methodological and mechanistic",
        ],
        "cover letter positioning",
        failures,
    )
    require(
        prebuttal,
        [
            "not presented as a converged fracture-probability model",
            "final Li4SiO4 constitutive law",
            "blanket design-margin calculation",
        ],
        "reviewer-risk boundaries",
        failures,
    )

    if failures:
        print("FAIL materials-novelty positioning: " + "; ".join(failures))
        return 1

    rows = audit.count("| Editorial question |")
    evidence_mentions = sum(
        token in audit
        for token in [
            "Fig. 1",
            "Fig. 4",
            "Fig. 5",
            "Fig. 6",
            "claim_evidence",
            "final_scientific_traceability",
            "event_aligned_topology",
            "material_degradation_mechanism_indices",
        ]
    )
    if rows != 1 or evidence_mentions < 6:
        print(
            "FAIL materials-novelty positioning: matrix header or evidence links are incomplete "
            f"(header_count={rows}, evidence_mentions={evidence_mentions})"
        )
        return 1

    print(
        "PASS materials-novelty positioning: JNM material object, novelty, mechanism evidence and claim boundaries verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
