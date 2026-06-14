#!/usr/bin/env python3
"""Check the final JNM scientific traceability audit."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/jnm_final_scientific_traceability_audit_20260613.md"
CLAIM_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv"
SOURCE_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv"
EXPECTED_CLAIMS = {f"C{i}" for i in range(1, 10)}
REQUIRED_PHRASES = [
    "Reviewer-risk closure",
    "Claim-to-evidence closure",
    "Figure/table provenance closure",
    "Submission boundary",
    "current calibration candidate",
    "not as converged failure probabilities",
    "not as a coupled thermal-hydraulic result",
    "repository DOI or stable URL",
]
FORBIDDEN_PATTERNS = [
    r"10\.5281/zenodo\.0000000",
    r"example\.com",
    r"FAKE",
]


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def run_builder() -> None:
    subprocess.run(
        ["python3", "scripts/build_jnm_final_scientific_traceability_audit.py"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )


def main() -> int:
    errors: list[str] = []
    run_builder()

    if not AUDIT.exists() or AUDIT.stat().st_size == 0:
        print(f"FAIL final scientific traceability audit: missing or empty {AUDIT}")
        return 1

    text = AUDIT.read_text(encoding="utf-8")
    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            errors.append(f"missing required phrase: {phrase}")
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(f"forbidden identifier leaked: {pattern}")

    claim_rows = read_csv(CLAIM_MATRIX)
    source_rows = read_csv(SOURCE_MATRIX)
    claim_ids = {row.get("claim_id", "").strip() for row in claim_rows}
    if claim_ids != EXPECTED_CLAIMS:
        errors.append(f"claim-id set mismatch: {sorted(claim_ids)}")
    for claim_id in EXPECTED_CLAIMS:
        if f"{claim_id}:" not in text:
            errors.append(f"audit missing claim row {claim_id}")

    source_items = {row.get("item", "").strip() for row in source_rows}
    for item in sorted(source_items):
        if f"| {item} |" not in text:
            errors.append(f"audit missing source item {item}")

    for row in claim_rows:
        claim_id = row.get("claim_id", "").strip()
        boundary = row.get("wording_boundary", "")
        if "Do not" not in boundary:
            errors.append(f"{claim_id}: claim matrix lacks explicit Do not boundary")
        for rel in split_values(row.get("primary_source_data_or_docs", "")):
            path = ROOT / rel
            if not path.exists():
                errors.append(f"{claim_id}: missing evidence path {rel}")
            elif path.is_file() and path.stat().st_size == 0:
                errors.append(f"{claim_id}: empty evidence path {rel}")

    for row in source_rows:
        item = row.get("item", "").strip()
        for column in ["output_files", "source_data_files", "generation_or_audit_scripts"]:
            values = split_values(row.get(column, ""))
            if not values:
                errors.append(f"{item}: empty {column}")
            for rel in values:
                path = ROOT / rel
                if not path.exists():
                    errors.append(f"{item}: missing {column} path {rel}")
                elif path.is_file() and path.stat().st_size == 0:
                    errors.append(f"{item}: empty {column} path {rel}")

    if errors:
        print("FAIL final scientific traceability audit")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS final scientific traceability audit: "
        f"{len(claim_rows)} claims and {len(source_rows)} provenance items verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
