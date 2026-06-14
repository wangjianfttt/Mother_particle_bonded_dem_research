#!/usr/bin/env python3
"""Check the JNM transfer-positioning audit and manuscript-facing scope."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/jnm_transfer_positioning_audit_20260613.md"
RESUBMISSION_PLAN = ROOT / "manuscript/journal_of_nuclear_materials_resubmission_plan.md"
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
COVER = ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md"
PREBUTTAL = ROOT / "manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md"

REQUIRED_AUDIT_PHRASES = [
    "scope-fit signal",
    "not as evidence that the calculation, figures or manuscript argument are invalid",
    "nuclear ceramic breeder-material degradation",
    "diagnostic instrument for ceramic breeder-material degradation",
    "Intact insertion of 500-subparticle bonded mother-pebble templates",
    "Acceptance gates",
    "Mother-pebble-resolved fracture-event extraction",
    "Nuclear Fusion identified the topic as too specialised",
]

REQUIRED_MANUSCRIPT_PHRASES = [
    "functional ceramic breeder materials",
    "mechanical degradation",
    "force network acts as a mesoscale shielding-and-activation field",
    "not as a converged fracture probability",
    "not a final Li4SiO4 material law",
    "no coupled thermal-flow prediction",
]

REQUIRED_COVER_PHRASES = [
    "functional ceramic breeder materials",
    "material-degradation processes",
    "Journal of Nuclear Materials",
    "distinct from a generic DEM-method paper",
    "reactor-design calculation",
    "thermal-hydraulic study",
    "calibration candidate rather than a final Li4SiO4 material law",
    "pilot event-sequence evidence rather than a converged failure probability",
]

RISK_PATTERNS = [
    r"\bblanket design margin predicted\b",
    r"\bconverged failure probability\b",
    r"\bfinal Li4SiO4 material law\b",
    r"\bthermal-hydraulic model\b",
    r"\breactor design calculation\b",
    r"\bgeneric DEM study\b",
]


def fail(errors: list[str]) -> int:
    print("FAIL JNM transfer-positioning audit")
    for error in errors:
        print(f"- {error}")
    return 1


def require_file(path: Path, errors: list[str]) -> str:
    if not path.exists() or path.stat().st_size == 0:
        errors.append(f"missing or empty: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def missing_phrases(text: str, phrases: list[str]) -> list[str]:
    return [phrase for phrase in phrases if phrase not in text]


def risky_positive_hits(path: Path, text: str) -> list[str]:
    hits: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        negated = any(token in lowered for token in ["not ", "rather than", "avoid", "without", "no "])
        for pattern in RISK_PATTERNS:
            if re.search(pattern, line, flags=re.IGNORECASE) and not negated:
                hits.append(f"{path.relative_to(ROOT)}:{line_no}:{pattern}")
    return hits


def main() -> int:
    errors: list[str] = []
    audit = require_file(AUDIT, errors)
    resubmission = require_file(RESUBMISSION_PLAN, errors)
    manuscript = require_file(MANUSCRIPT, errors)
    cover = require_file(COVER, errors)
    prebuttal = require_file(PREBUTTAL, errors)
    if errors:
        return fail(errors)

    missing = missing_phrases(audit, REQUIRED_AUDIT_PHRASES)
    if missing:
        errors.append("audit missing phrases: " + "; ".join(missing))

    missing = missing_phrases(manuscript, REQUIRED_MANUSCRIPT_PHRASES)
    if missing:
        errors.append("manuscript missing transfer-positioning phrases: " + "; ".join(missing))

    missing = missing_phrases(cover, REQUIRED_COVER_PHRASES)
    if missing:
        errors.append("cover letter missing positioning phrases: " + "; ".join(missing))

    if "too specialised for its audience" not in resubmission:
        errors.append("resubmission plan no longer records the Nuclear Fusion scope-fit reason")
    if "scope-fit rejection rather than a technical rejection" not in resubmission:
        errors.append("resubmission plan no longer distinguishes scope fit from technical rejection")
    if "Data availability may be considered insufficient before DOI insertion" not in prebuttal:
        errors.append("reviewer prebuttal no longer contains DOI/data-availability risk")

    for path, text in [(MANUSCRIPT, manuscript), (COVER, cover)]:
        hits = risky_positive_hits(path, text)
        if hits:
            errors.append("positive over-scope phrases found: " + "; ".join(hits))

    if errors:
        return fail(errors)

    print("PASS JNM transfer-positioning audit: NF transfer reason, JNM materials framing and scope boundaries verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
