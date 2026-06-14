#!/usr/bin/env python3
"""Validate the JNM claim-evidence-boundary matrix."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv"
EXPECTED_CLAIMS = {f"C{i}" for i in range(1, 10)}
PUBLIC_PACKAGE_ROOT_NAME = "journal_of_nuclear_materials_reproducibility_package"
PUBLIC_PACKAGE_DEFERRED_EVIDENCE = {
    "docs/jnm_final_submission_gate_report.md",
    "docs/jnm_final_submission_gate_report.json",
    "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip",
    "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip.sha256",
}
REQUIRED_COLUMNS = [
    "claim_id",
    "manuscript_claim",
    "primary_display_items",
    "primary_source_data_or_docs",
    "claim_status",
    "wording_boundary",
    "reviewer_risk_link",
]


def is_public_package_root() -> bool:
    return ROOT.name == PUBLIC_PACKAGE_ROOT_NAME


def split_values(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def main() -> int:
    errors: list[str] = []
    deferred_evidence: list[str] = []
    public_package_mode = is_public_package_root()
    if not MATRIX.exists():
        print(f"FAIL claim-evidence matrix: missing {MATRIX}")
        return 1
    rows = list(csv.DictReader(MATRIX.open()))
    if not rows:
        print("FAIL claim-evidence matrix: no data rows")
        return 1
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in rows[0]]
    if missing_columns:
        errors.append("missing columns: " + ", ".join(missing_columns))

    claim_ids = {row.get("claim_id", "").strip() for row in rows}
    missing_claims = sorted(EXPECTED_CLAIMS - claim_ids)
    extra_claims = sorted(claim_ids - EXPECTED_CLAIMS)
    if missing_claims:
        errors.append("missing expected claims: " + ", ".join(missing_claims))
    if extra_claims:
        errors.append("unexpected claims: " + ", ".join(extra_claims))

    for row_index, row in enumerate(rows, start=2):
        claim_id = row.get("claim_id", "").strip() or f"row {row_index}"
        for column in REQUIRED_COLUMNS:
            if not (row.get(column) or "").strip():
                errors.append(f"{claim_id}: empty {column}")
        for rel in split_values(row.get("primary_source_data_or_docs", "")):
            path = ROOT / rel
            if not path.exists():
                if public_package_mode and rel in PUBLIC_PACKAGE_DEFERRED_EVIDENCE:
                    deferred_evidence.append(rel)
                    continue
                errors.append(f"{claim_id}: missing evidence path {rel}")
            elif path.is_file() and path.stat().st_size == 0:
                errors.append(f"{claim_id}: empty evidence path {rel}")
        if "Do not" not in row.get("wording_boundary", ""):
            errors.append(f"{claim_id}: wording_boundary should include an explicit Do not boundary")

    if errors:
        print("FAIL claim-evidence matrix")
        for error in errors:
            print(f"- {error}")
        return 1
    if deferred_evidence:
        deferred_count = len(set(deferred_evidence))
        print(
            f"PASS claim-evidence matrix: {len(rows)} claims, "
            f"public package deferred {deferred_count} self-referential/final-gate evidence paths"
        )
    else:
        print(f"PASS claim-evidence matrix: {len(rows)} claims, all evidence paths exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
