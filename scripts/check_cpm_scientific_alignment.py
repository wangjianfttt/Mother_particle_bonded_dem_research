#!/usr/bin/env python3
"""Check CPM manuscript, cover letter and fields share the same scientific spine."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
DOCS = ROOT / "docs"

FILES = {
    "draft": MANUSCRIPT / "repaired_full_submission_draft.md",
    "tex": MANUSCRIPT / "computational_particle_mechanics_submission.tex",
    "cover": MANUSCRIPT / "computational_particle_mechanics_cover_letter.md",
    "fields": MANUSCRIPT / "computational_particle_mechanics_editorial_fields.md",
    "gap_map": DOCS / "cpm_literature_gap_map_20260704.md",
}

REQUIRED = {
    "draft": [
        "The missing particle-mechanics layer is the chronological link",
        "placing many bonded parent particles into a random load-bearing bed",
        "force-path topology and bonded-particle strength jointly control",
    ],
    "cover": [
        "Single-particle crush tests",
        "bed-compression studies",
        "force-chain DEM",
        "particle-replacement breakage models",
        "bonded-particle fracture models",
        "chronological link between a load-bearing contact network",
        "damaged-particle identity",
        "bond-loss increments",
        "native force-network state",
        "eleven-row material-response table",
        "six-case bond-strength matrix",
    ],
    "fields": [
        "eleven-row material-response table",
        "six-case strength matrix",
        "local force-path topology",
        "bonded-particle strength",
        "source-data-backed event sequence",
    ],
    "gap_map": [
        "Single-particle crush and fragment-mode evidence",
        "Packed-bed compression and crushed-bed consequences",
        "DEM force-chain and load-path studies",
        "Particle-replacement and crushable-bed DEM",
        "Bonded-particle fracture modelling",
        "chronological link between a load-bearing contact network",
    ],
}

FORBIDDEN = re.compile(
    r"\b(repaired version|audit|diagnostic|gate|CAL|SP-00|PB-00|"
    r"Advanced Powder|Journal of Nuclear Materials|Nuclear Fusion)\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    texts = {}
    for key, path in FILES.items():
        if not path.exists():
            fail(f"missing {key} file: {path}")
        texts[key] = path.read_text(encoding="utf-8", errors="ignore")

    for key, required_terms in REQUIRED.items():
        text = texts[key]
        missing = [term for term in required_terms if term not in text]
        if missing:
            fail(f"{key} missing required scientific-alignment terms: {missing}")

    for key in ["draft", "tex", "cover", "fields"]:
        match = FORBIDDEN.search(texts[key])
        if match:
            fail(f"{key} contains reader-facing residue: {match.group(0)!r}")

    print("PASS CPM scientific alignment: manuscript, cover letter, fields and gap map match")


if __name__ == "__main__":
    main()
