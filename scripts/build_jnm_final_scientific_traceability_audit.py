#!/usr/bin/env python3
"""Build the final JNM scientific traceability audit.

This audit is reviewer-facing scaffolding for the author package. It does not
introduce new claims; it joins the existing claim/evidence and source-data
matrices into one compact chain from manuscript claim to data, figure, script
and overclaim boundary.
"""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIM_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv"
SOURCE_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv"
OUTPUT = ROOT / "docs/jnm_final_scientific_traceability_audit_20260613.md"


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def compact_paths(paths: list[str], limit: int = 3) -> str:
    if not paths:
        return "none"
    visible = paths[:limit]
    extra = len(paths) - len(visible)
    text = "<br>".join(f"`{path}`" for path in visible)
    if extra:
        text += f"<br>+{extra} more"
    return text


def main() -> int:
    claim_rows = read_csv(CLAIM_MATRIX)
    source_rows = read_csv(SOURCE_MATRIX)
    source_by_item = {row["item"].strip(): row for row in source_rows}

    lines: list[str] = []
    lines.append("# JNM final scientific traceability audit")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()}")
    lines.append("")
    lines.append(
        "Purpose: provide a compact, auditable chain from each active manuscript "
        "claim to its display item, source data, generation or audit scripts and "
        "explicit wording boundary. This file is a submission-support audit; it "
        "does not add evidence beyond the checked manuscript matrices."
    )
    lines.append("")
    lines.append("## Reviewer-risk closure")
    lines.append("")
    lines.append(
        "- Numerical evidence only: every active scientific claim below is tied to "
        "processed data, figures, tables, audits or manuscript text already checked "
        "by the final gate."
    )
    lines.append(
        "- No hidden probability claim: event-sequence results are treated as "
        "mechanistic evidence, not as converged failure probabilities or design "
        "margins."
    )
    lines.append(
        "- No hidden material-law claim: the bonded 1 mm pebble is described as a "
        "current calibration candidate over the tested load and morphology window, "
        "not as a final Li4SiO4 constitutive law."
    )
    lines.append(
        "- No hidden thermal-flow claim: force-network and fracture chronology are "
        "framed as state variables relevant to breeder-bed contact networks and "
        "future coupled heat/flow models, not as a coupled thermal-hydraulic result."
    )
    lines.append("")
    lines.append("## Claim-to-evidence closure")
    lines.append("")
    lines.append(
        "| Claim | Display item(s) | Evidence status | Primary evidence | Generation/audit scripts | Boundary enforced |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- |")

    for row in claim_rows:
        claim_id = row["claim_id"].strip()
        displays = split_values(row["primary_display_items"])
        evidence_paths = split_values(row["primary_source_data_or_docs"])
        script_paths: list[str] = []
        for display in displays:
            source = source_by_item.get(display)
            if not source:
                continue
            script_paths.extend(split_values(source.get("generation_or_audit_scripts", "")))
        # Keep order while dropping duplicates.
        script_paths = list(dict.fromkeys(script_paths))
        display_text = "<br>".join(f"`{item}`" for item in displays)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{claim_id}: {row['manuscript_claim']}",
                    display_text,
                    row["claim_status"],
                    compact_paths(evidence_paths),
                    compact_paths(script_paths),
                    row["wording_boundary"],
                ]
            )
            + " |"
        )

    lines.append("")
    lines.append("## Figure/table provenance closure")
    lines.append("")
    lines.append("| Item | Evidence role | Output file(s) | Source data/doc(s) | Script(s) |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in source_rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    row["item"],
                    row["evidence_role"],
                    compact_paths(split_values(row["output_files"]), limit=2),
                    compact_paths(split_values(row["source_data_files"]), limit=2),
                    compact_paths(split_values(row["generation_or_audit_scripts"]), limit=2),
                ]
            )
            + " |"
        )

    lines.append("")
    lines.append("## Submission boundary")
    lines.append("")
    lines.append(
        "The current local package remains pre-DOI: the only expected external blocker "
        "is insertion of the repository DOI or stable URL after depositing the frozen "
        "reduced reproducibility package. This audit should remain valid before and "
        "after DOI insertion because it relies on file-level evidence paths rather "
        "than repository-specific identifiers."
    )
    lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
