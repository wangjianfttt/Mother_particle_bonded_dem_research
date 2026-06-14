#!/usr/bin/env python3
"""Validate the JNM figure/table source-data coverage matrix."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv"
EXPECTED_ITEMS = {
    "Fig1",
    "Fig2",
    "Fig3",
    "Fig4",
    "Fig5",
    "Fig6",
    "Table1",
    "Table2",
    "Table3",
    "GraphicalAbstract",
    "PDFVisualQA",
    "JNMScopeAudit",
    "ScientificStorylineAudit",
}
PATH_COLUMNS = ["output_files", "source_data_files", "generation_or_audit_scripts"]


def split_paths(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def main() -> int:
    errors: list[str] = []
    if not MATRIX.exists():
        print(f"FAIL source-data matrix: missing {MATRIX}")
        return 1

    rows = list(csv.DictReader(MATRIX.open()))
    if not rows:
        print("FAIL source-data matrix: no data rows")
        return 1

    item_ids = {row.get("item", "").strip() for row in rows}
    missing_items = sorted(EXPECTED_ITEMS - item_ids)
    extra_items = sorted(item_ids - EXPECTED_ITEMS)
    if missing_items:
        errors.append("missing expected items: " + ", ".join(missing_items))
    if extra_items:
        errors.append("unexpected items: " + ", ".join(extra_items))

    for row_index, row in enumerate(rows, start=2):
        item = row.get("item", "").strip() or f"row {row_index}"
        for column in PATH_COLUMNS:
            paths = split_paths(row.get(column, ""))
            if not paths:
                errors.append(f"{item}: empty {column}")
                continue
            for rel in paths:
                path = ROOT / rel
                if not path.exists():
                    errors.append(f"{item}: missing {column} path {rel}")
                elif path.is_file() and path.stat().st_size == 0:
                    errors.append(f"{item}: empty {column} path {rel}")

    if errors:
        print("FAIL source-data matrix")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS source-data matrix: {len(rows)} items, all referenced files exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
