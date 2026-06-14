#!/usr/bin/env python3
"""Check JNM/Elsevier declaration support files."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECLARATIONS = ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md"
AUTHOR_CHECKLIST = ROOT / "manuscript/journal_of_nuclear_materials_author_declaration_checklist.md"

REQUIRED_DECLARATION_SECTIONS = [
    "Declaration of competing interest",
    "Funding declaration",
    "Role of the funding source",
    "Declaration of generative AI and AI-assisted technologies in the writing process",
    "Data availability statement for Editorial Manager",
    "Code availability statement for Editorial Manager",
    "Final author approval checklist",
]
REQUIRED_PHRASES = [
    "no known competing financial interests",
    "had no role in the design of the computational study",
    "reviewed, edited and verified",
    "take full responsibility for the content",
    "repository DOI or stable URL",
    "included in the reduced reproducibility package",
]
REQUIRED_CHECKLIST_ITEMS = [
    "Author order confirmed.",
    "Author affiliations confirmed.",
    "Corresponding author email confirmed.",
    "CRediT contribution statement confirmed by all authors.",
    "Funding text and grant numbers confirmed.",
    "Repository DOI or stable URL inserted after deposit.",
    "Generative-AI declaration confirmed or edited before upload.",
    "Journal submission system metadata matches the manuscript title page.",
]


def checkbox_count(text: str) -> int:
    return len(re.findall(r"^- \[[ xX]\] ", text, flags=re.MULTILINE))


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []
    if not DECLARATIONS.exists():
        print(f"FAIL declarations: missing {DECLARATIONS}")
        return 1
    if not AUTHOR_CHECKLIST.exists():
        print(f"FAIL declarations: missing {AUTHOR_CHECKLIST}")
        return 1
    declarations = DECLARATIONS.read_text()
    checklist = AUTHOR_CHECKLIST.read_text()

    for section in REQUIRED_DECLARATION_SECTIONS:
        if f"## {section}" not in declarations:
            errors.append(f"missing declarations section: {section}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in declarations:
            errors.append(f"missing declarations phrase: {phrase}")
    for item in REQUIRED_CHECKLIST_ITEMS:
        if item not in declarations and item.removesuffix(".") + ":" not in declarations:
            errors.append(f"missing final author approval checklist item: {item}")

    if "Corresponding author: Jian Wang" not in checklist or "wjfttt@mail.ustc.edu.cn" not in checklist:
        errors.append("author declaration checklist does not confirm corresponding author metadata")
    if "Jian Wang" not in checklist or "Haishun Deng" not in checklist:
        errors.append("author declaration checklist does not include the expected author range")

    unchecked = len(re.findall(r"^- \[ \] ", declarations + "\n" + checklist, flags=re.MULTILINE))
    total_boxes = checkbox_count(declarations + "\n" + checklist)
    if unchecked:
        notes.append(f"{unchecked} unchecked author-side confirmation item(s) remain")
    if total_boxes < 16:
        errors.append(f"expected at least 16 declaration checklist boxes; found {total_boxes}")

    if errors:
        print("FAIL declarations")
        for error in errors:
            print(f"- {error}")
        return 1
    suffix = f"; {'; '.join(notes)}" if notes else ""
    print(f"PASS declarations: required Elsevier/JNM declarations present{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
