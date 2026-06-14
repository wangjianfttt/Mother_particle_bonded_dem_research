#!/usr/bin/env python3
"""Check public-facing JNM upload text for avoidable local/package artefacts."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PUBLIC_TEXT_FILES = [
    ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md",
    ROOT / "manuscript/journal_of_nuclear_materials_submission.tex",
    ROOT / "manuscript/journal_of_nuclear_materials_supplementary.md",
    ROOT / "manuscript/journal_of_nuclear_materials_supplementary.tex",
    ROOT / "manuscript/journal_of_nuclear_materials_highlights.md",
    ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md",
    ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md",
    ROOT / "manuscript/journal_of_nuclear_materials_author_metadata.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json",
    ROOT / "manuscript/journal_of_nuclear_materials_repro_package_readme.md",
]

INTERNAL_SUPPORT_FILES = [
    ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md",
    ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv",
    ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md",
]

ABSOLUTE_LOCAL_PATTERNS = [
    re.compile(r"/Users/wangjian"),
    re.compile(r"Documents/颗粒破碎统计研究"),
]

READER_FACING_INTERNAL_LABEL = re.compile(r"\b(?:PB-006|PB-007|SP-002|CAL1|seed\d+)\b", re.IGNORECASE)


def scan_patterns(paths: list[Path], patterns: list[re.Pattern[str]]) -> list[str]:
    hits: list[str] = []
    for path in paths:
        text = path.read_text(errors="replace")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(pattern.search(line) for pattern in patterns):
                hits.append(f"{path.relative_to(ROOT)}:{line_no}")
    return hits


def scan_public_internal_labels() -> list[str]:
    hits: list[str] = []
    for path in PUBLIC_TEXT_FILES:
        for line_no, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            if READER_FACING_INTERNAL_LABEL.search(line):
                hits.append(f"{path.relative_to(ROOT)}:{line_no}")
    return hits


def check_repository_placeholder_scope() -> list[str]:
    allowed = {
        ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md",
        ROOT / "manuscript/journal_of_nuclear_materials_submission.tex",
        ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv",
        ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md",
    }
    scanned = PUBLIC_TEXT_FILES + INTERNAL_SUPPORT_FILES
    hits: list[str] = []
    for path in scanned:
        text = path.read_text(errors="replace")
        if "[repository DOI/URL to be added]" in text or "doi_pending" in text:
            if path not in allowed:
                hits.append(str(path.relative_to(ROOT)))
    return hits


def main() -> int:
    missing = [str(path.relative_to(ROOT)) for path in PUBLIC_TEXT_FILES + INTERNAL_SUPPORT_FILES if not path.exists()]
    if missing:
        print("FAIL public-artifact hygiene: missing files " + ", ".join(missing))
        return 1

    absolute_hits = scan_patterns(PUBLIC_TEXT_FILES + INTERNAL_SUPPORT_FILES, ABSOLUTE_LOCAL_PATTERNS)
    if absolute_hits:
        print("FAIL public-artifact hygiene: local absolute paths in " + ", ".join(absolute_hits[:20]))
        return 1

    label_hits = scan_public_internal_labels()
    if label_hits:
        print("FAIL public-artifact hygiene: reader-facing internal labels in " + ", ".join(label_hits[:20]))
        return 1

    placeholder_hits = check_repository_placeholder_scope()
    if placeholder_hits:
        print("FAIL public-artifact hygiene: DOI placeholders outside approved files " + ", ".join(placeholder_hits))
        return 1

    print(
        "PASS public-artifact hygiene: public text has no local absolute paths, "
        "no reader-facing internal case labels and DOI placeholders are scoped"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
