#!/usr/bin/env python3
"""Verify matrix-referenced evidence files are included in the public JNM package."""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package"
PACKAGE_ZIP = ROOT / "submission_packages/journal_of_nuclear_materials_reproducibility_package.zip"
MATRICES = [
    ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv",
]
PATH_COLUMNS = [
    "output_files",
    "source_data_files",
    "generation_or_audit_scripts",
    "primary_source_data_or_docs",
]
SELF_ARCHIVE_PREFIXES = (
    "submission_packages/journal_of_nuclear_materials_submission_package",
    "submission_packages/journal_of_nuclear_materials_reproducibility_package",
)
PUBLIC_EXCLUDED_FILES = {
    "docs/jnm_final_submission_gate_report.md",
    "docs/jnm_final_submission_gate_report.json",
}


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def matrix_paths() -> set[str]:
    paths: set[str] = set()
    for matrix in MATRICES:
        rows = list(csv.DictReader(matrix.open()))
        for row in rows:
            for column in PATH_COLUMNS:
                if column not in row:
                    continue
                for rel in split_paths(row.get(column, "")):
                    if rel.startswith(SELF_ARCHIVE_PREFIXES):
                        continue
                    paths.add(rel)
    return paths


def main() -> int:
    errors: list[str] = []
    required = matrix_paths() - PUBLIC_EXCLUDED_FILES
    if not PACKAGE_DIR.exists():
        print(f"FAIL package coverage: missing package directory {PACKAGE_DIR}")
        return 1
    if not PACKAGE_ZIP.exists():
        print(f"FAIL package coverage: missing package zip {PACKAGE_ZIP}")
        return 1

    for rel in sorted(required):
        path = PACKAGE_DIR / rel
        if not path.exists():
            errors.append(f"missing from package dir: {rel}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"empty in package dir: {rel}")

    with zipfile.ZipFile(PACKAGE_ZIP) as archive:
        names = set(archive.namelist())
    prefix = "journal_of_nuclear_materials_reproducibility_package/"
    for rel in sorted(required):
        member = prefix + rel
        if member not in names:
            errors.append(f"missing from package zip: {rel}")

    if errors:
        print("FAIL package coverage")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS package coverage: {len(required)} matrix-referenced files included")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
