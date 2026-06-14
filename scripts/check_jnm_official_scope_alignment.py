#!/usr/bin/env python3
"""Check that the JNM submission remains aligned with official scope risks."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/jnm_official_scope_alignment_audit_20260613.md"
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
GRAPHICAL_ABSTRACT = ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.png"
UPLOAD_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv"
HIGHLIGHTS = ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"
FLAT_SOURCE_ZIP = ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip"
FROZEN_DEPOSIT_ROOT = ROOT / "submission_packages"


def main() -> int:
    errors: list[str] = []
    for path in [AUDIT, MANUSCRIPT, GRAPHICAL_ABSTRACT, UPLOAD_MATRIX, HIGHLIGHTS, FLAT_SOURCE_ZIP]:
        if not path.exists() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {path.relative_to(ROOT)}")

    if errors:
        print("FAIL JNM official-scope alignment: " + "; ".join(errors))
        return 1

    audit_text = AUDIT.read_text(errors="replace")
    manuscript_text = MANUSCRIPT.read_text(errors="replace")
    required_audit_phrases = [
        "high novelty",
        "fusion reactors",
        "reactor design and technology",
        "thermal hydraulics or fluid properties",
        "general ceramic studies",
        "solid breeder blanket",
        "not as a generic granular assembly",
        "Zero-pre-damage bonded-template insertion",
        "Graphical abstract",
        "Highlights should be 3-5",
        "85 characters",
        "Elsevier LaTeX and Editorial Manager guidance",
        "elsarticle",
        "single archive",
        "official re-check matrix",
        "frozen for repository deposition",
    ]
    missing_audit = [phrase for phrase in required_audit_phrases if phrase not in audit_text]
    if missing_audit:
        errors.append("audit missing phrases: " + ", ".join(missing_audit))

    material_scope_terms = [
        "ceramic breeder",
        "Li4SiO4",
        "mechanical degradation",
        "solid breeder",
        "fracture-event",
        "native force",
        "purge",
    ]
    missing_scope = [term for term in material_scope_terms if term not in manuscript_text]
    if missing_scope:
        errors.append("manuscript missing material-scope terms: " + ", ".join(missing_scope))

    must_have_boundaries = [
        "not as a converged fracture probability",
        "not a final Li4SiO4 material law",
        "quantitative blanket design margins require larger stochastic ensembles",
    ]
    missing_boundaries = [phrase for phrase in must_have_boundaries if phrase not in manuscript_text]
    if missing_boundaries:
        errors.append("manuscript missing conservative boundaries: " + ", ".join(missing_boundaries))

    risky_phrases = [
        r"\breactor design rule\b",
        r"\bthermal-hydraulic model\b",
        r"\bgeneric ceramic DEM\b",
        r"\bconverged failure probability\b(?! or)",
        r"\bfinal design margin\b",
    ]
    risky_hits: list[str] = []
    for line_no, line in enumerate(manuscript_text.splitlines(), start=1):
        lowered = line.lower()
        negated = any(token in lowered for token in ["not ", "rather than", "avoid", "without", "require "])
        for pattern in risky_phrases:
            if re.search(pattern, line, flags=re.IGNORECASE) and not negated:
                risky_hits.append(f"{MANUSCRIPT.relative_to(ROOT)}:{line_no}:{pattern}")
    if risky_hits:
        errors.append("risky scope/overclaim phrases found: " + ", ".join(risky_hits))

    upload_text = UPLOAD_MATRIX.read_text(errors="replace")
    upload_lower = upload_text.lower()
    if "graphical abstract" not in upload_lower:
        errors.append("upload matrix does not contain graphical abstract role")
    if "latex source" not in upload_lower:
        errors.append("upload matrix does not contain LaTeX source-file role")

    highlight_lines = [
        line.strip()
        for line in HIGHLIGHTS.read_text(errors="replace").splitlines()
        if line.strip().startswith(("-", "*"))
    ]
    if not 3 <= len(highlight_lines) <= 5:
        errors.append(f"Highlights file has {len(highlight_lines)} bullets, expected 3-5")
    long_highlights = [line for line in highlight_lines if len(line.lstrip("-* ").strip()) > 85]
    if long_highlights:
        errors.append("Highlights exceed 85 characters: " + "; ".join(long_highlights[:3]))

    frozen_dirs = sorted(FROZEN_DEPOSIT_ROOT.glob("jnm_repository_deposit_FROZEN_20260614_*"))
    if not frozen_dirs:
        errors.append("missing frozen repository-deposit packet")
    else:
        latest = max(frozen_dirs, key=lambda path: path.stat().st_mtime)
        frozen_zip = latest / "journal_of_nuclear_materials_reproducibility_package.zip"
        frozen_sha = latest / "journal_of_nuclear_materials_reproducibility_package.zip.sha256"
        if not frozen_zip.exists() or not frozen_sha.exists():
            errors.append(f"latest frozen deposit packet incomplete: {latest.relative_to(ROOT)}")
        if latest.name not in audit_text:
            errors.append(f"audit does not name latest frozen deposit packet: {latest.name}")

    if errors:
        print("FAIL JNM official-scope alignment")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS JNM official-scope alignment: material scope, novelty boundaries, Elsevier format assets and frozen repository packet verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
