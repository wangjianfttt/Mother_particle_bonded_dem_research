#!/usr/bin/env python3
"""Check the author-facing JNM figure-caption companion file."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPTIONS = ROOT / "manuscript/figure_captions.md"

EXPECTED_SECTIONS = [
    "## Graphical abstract",
    "## Fig. 1 | Locked-template workflow for fracture-resolved Li4SiO4 breeder-bed compression.",
    "## Fig. 2 | Single-pebble calibration evidence for the current 500-subparticle template.",
    "## Fig. 3 | Subparticle-resolution and loading-rate sensitivity of the single-pebble template.",
    "## Fig. 4 | Corrected pre-damage force-transmission validation.",
    "## Fig. 5 | Corrected fracture-event sequence and native force-network evolution.",
    "## Fig. 6 | Corrected-case comparison separates force connectivity from fracture onset.",
    "## Supplementary Fig. S1 | Single-pebble fragment morphology.",
    "## Supplementary Fig. S2 | Force-displacement overlay for the selected weak-plane template.",
]

REQUIRED_PATHS = [
    "figures/main/journal_of_nuclear_materials_graphical_abstract.png",
    "figures/main/fig1_workflow.png",
    "figures/sp002/single_pebble_calibration_evidence.svg",
    "figures/sp002/jnm_single_pebble_validation.svg",
    "figures/pb007/pb007_acceptance_gate_validation.svg",
    "figures/pb007/pb007_corrected_fracture_sequence.svg",
    "figures/pb007/pb007_replicate_comparison.svg",
    "figures/sp002/single_pebble_fragment_morphology_paraview.png",
    "figures/sp002/sp002_force_displacement_overlay.svg",
    "tables/single_pebble_calibration_target_evidence_summary.csv",
    "tables/jnm_single_pebble_resolution_summary.csv",
    "tables/pb007_event_aligned_topology.csv",
    "tables/pb007_macro_topology_event_metrics.csv",
    "tables/jnm_material_degradation_mechanism_indices.csv",
]

FORBIDDEN_CAPTION_TERMS = [
    re.compile(r"\bSP-002\b", re.IGNORECASE),
    re.compile(r"\bCAL1\b", re.IGNORECASE),
    re.compile(r"\bPB-006\b", re.IGNORECASE),
    re.compile(r"\bPB-007\b", re.IGNORECASE),
    re.compile(r"\bseed\d+\b", re.IGNORECASE),
    re.compile(r"Local bond dumps", re.IGNORECASE),
]


def fail(errors: list[str]) -> int:
    print("FAIL JNM figure captions companion")
    for error in errors:
        print(f"- {error}")
    return 1


def caption_text_only(text: str) -> str:
    lines: list[str] = []
    in_file_list = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.endswith("files:") or stripped.endswith("file:") or stripped.startswith("Traceable source"):
            in_file_list = True
            continue
        if stripped.startswith("## "):
            in_file_list = False
        if in_file_list and stripped.startswith("- `"):
            continue
        lines.append(line)
    return "\n".join(lines)


def main() -> int:
    errors: list[str] = []
    if not CAPTIONS.exists() or CAPTIONS.stat().st_size == 0:
        return fail(["missing or empty manuscript/figure_captions.md"])

    text = CAPTIONS.read_text(encoding="utf-8", errors="replace")
    missing_sections = [section for section in EXPECTED_SECTIONS if section not in text]
    if missing_sections:
        errors.append("missing sections: " + "; ".join(missing_sections))

    missing_paths = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing_paths:
        errors.append("missing display/source paths: " + "; ".join(missing_paths))

    caption_text = caption_text_only(text)
    term_hits: list[str] = []
    for line_no, line in enumerate(caption_text.splitlines(), start=1):
        for pattern in FORBIDDEN_CAPTION_TERMS:
            if pattern.search(line):
                term_hits.append(f"line {line_no}: {pattern.pattern}")
    if term_hits:
        errors.append("reader-facing caption terms found: " + "; ".join(term_hits[:20]))

    required_phrases = [
        "current calibration candidate rather than a final Li4SiO4 material law",
        "not a converged blanket design-margin prediction",
        "not an ensemble statistic",
        "local force-path sensitivity rather than a deterministic displacement-only",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]
    if missing_phrases:
        errors.append("missing conservative caption phrases: " + "; ".join(missing_phrases))

    if errors:
        return fail(errors)

    print(
        "PASS JNM figure captions companion: graphical abstract, 6 main figures, "
        "2 supplementary figures, source paths and reader-facing terminology verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
