#!/usr/bin/env python3
"""Check reader-facing JNM text for implementation-detail leakage."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT_MD = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
MANUSCRIPT_TEX = ROOT / "manuscript/journal_of_nuclear_materials_submission.tex"
COVER = ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md"
HIGHLIGHTS = ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"
PUBLIC_PACKAGE_ROOT_NAME = "journal_of_nuclear_materials_reproducibility_package"

PUBLIC_TEXTS = [MANUSCRIPT_MD, MANUSCRIPT_TEX, COVER, HIGHLIGHTS]

INTERNAL_CODE = re.compile(r"\b(?:PB-006|PB-007|SP-002|CAL1|seed\d+)\b", re.IGNORECASE)
LOW_LEVEL_TERMS = re.compile(r"\b(?:raw dump|local-bond|restart file|restart files|screenlog|in\.pb|in\.plate)\b", re.IGNORECASE)
SOFTWARE_TERM = re.compile(r"LIGGGHTS(?:-INL)?", re.IGNORECASE)


def is_public_package_root() -> bool:
    return ROOT.name == PUBLIC_PACKAGE_ROOT_NAME


def reader_texts() -> list[Path]:
    if is_public_package_root():
        return [path for path in PUBLIC_TEXTS if path.exists()]
    return PUBLIC_TEXTS


def missing_files() -> list[str]:
    if is_public_package_root():
        required_public_texts = [MANUSCRIPT_MD, MANUSCRIPT_TEX, HIGHLIGHTS]
        return [str(path.relative_to(ROOT)) for path in required_public_texts if not path.exists()]
    return [str(path.relative_to(ROOT)) for path in PUBLIC_TEXTS if not path.exists()]


def scan_internal_codes() -> list[str]:
    hits: list[str] = []
    for path in reader_texts():
        for line_no, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            if INTERNAL_CODE.search(line):
                hits.append(f"{path.relative_to(ROOT)}:{line_no}")
    return hits


def scan_low_level_terms() -> list[str]:
    """Flag low-level run-file terms outside methods, data availability and code availability."""

    hits: list[str] = []
    for path in reader_texts():
        section = ""
        for line_no, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            stripped = line.strip()
            if path.suffix == ".md" and stripped.startswith("## "):
                section = stripped.lower()
            elif path.suffix == ".tex":
                match = re.match(r"\\section\*?\{(.+?)\}", stripped)
                if match:
                    section = match.group(1).lower()
            allowed = any(token in section for token in ["methods", "data availability", "code availability"])
            if LOW_LEVEL_TERMS.search(line) and not allowed:
                hits.append(f"{path.relative_to(ROOT)}:{line_no}")
    return hits


def scan_software_mentions() -> list[str]:
    """Allow the executable provenance in Methods and references, but not narrative overexposure."""

    hits: list[str] = []
    md_text = MANUSCRIPT_MD.read_text(errors="replace") if MANUSCRIPT_MD.exists() else ""
    tex_text = MANUSCRIPT_TEX.read_text(errors="replace") if MANUSCRIPT_TEX.exists() else ""
    if md_text and len(SOFTWARE_TERM.findall(md_text)) > 2:
        hits.append(f"{MANUSCRIPT_MD.relative_to(ROOT)}: more than two LIGGGHTS mentions")
    if tex_text and len(SOFTWARE_TERM.findall(tex_text)) > 2:
        hits.append(f"{MANUSCRIPT_TEX.relative_to(ROOT)}: more than two LIGGGHTS mentions")

    for path in reader_texts():
        section = ""
        for line_no, line in enumerate(path.read_text(errors="replace").splitlines(), start=1):
            stripped = line.strip()
            if path.suffix == ".md" and stripped.startswith("## "):
                section = stripped.lower()
            elif path.suffix == ".tex":
                match = re.match(r"\\section\*?\{(.+?)\}", stripped)
                if match:
                    section = match.group(1).lower()
            allowed = "methods" in section or line.lstrip().startswith("@") or "\\bibitem" in line
            if SOFTWARE_TERM.search(line) and not allowed:
                hits.append(f"{path.relative_to(ROOT)}:{line_no}")
    return hits


def main() -> int:
    errors: list[str] = []
    missing = missing_files()
    if missing:
        errors.append("missing reader-facing files: " + ", ".join(missing))
    if not errors:
        code_hits = scan_internal_codes()
        if code_hits:
            errors.append("reader-facing internal case labels in " + ", ".join(code_hits[:20]))
        low_level_hits = scan_low_level_terms()
        if low_level_hits:
            errors.append("low-level run-file terminology outside allowed sections in " + ", ".join(low_level_hits[:20]))
        software_hits = scan_software_mentions()
        if software_hits:
            errors.append("software name overexposed outside Methods/references in " + ", ".join(software_hits[:20]))

    if errors:
        print("FAIL reader-facing hygiene")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS reader-facing hygiene: internal labels, low-level run-file terms and software provenance "
        "are confined to appropriate manuscript locations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
