#!/usr/bin/env python3
"""Check generated JNM DOCX upload companion files."""

from __future__ import annotations

import os
import sys
from pathlib import Path

BUNDLED_PYTHON = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
if BUNDLED_PYTHON.exists() and Path(sys.executable).resolve() != BUNDLED_PYTHON.resolve():
    os.execv(str(BUNDLED_PYTHON), [str(BUNDLED_PYTHON), *sys.argv])

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
COVER_MD = ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md"
DECL_MD = ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md"
COVER_DOCX = ROOT / "manuscript/journal_of_nuclear_materials_cover_letter.docx"
DECL_DOCX = ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.docx"
QA_REPORT = ROOT / "docs/jnm_upload_docx_qa.md"


def fail(message: str) -> int:
    print(f"FAIL upload-docx: {message}")
    return 1


def doc_text(path: Path) -> str:
    doc = Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def main() -> int:
    for path in [COVER_MD, DECL_MD, COVER_DOCX, DECL_DOCX, QA_REPORT]:
        if not path.exists() or path.stat().st_size == 0:
            return fail(f"missing or empty file: {path.relative_to(ROOT)}")

    cover = doc_text(COVER_DOCX)
    declarations = doc_text(DECL_DOCX)
    qa = QA_REPORT.read_text(encoding="utf-8")

    cover_required = [
        "Cover letter",
        "Journal of Nuclear Materials",
        "Acceptance-gated bonded-template DEM reveals localized fracture sequences",
        "Jian Wang",
        "wjfttt@mail.ustc.edu.cn",
    ]
    decl_required = [
        "Declarations",
        "Declaration of competing interest",
        "Data availability statement for Editorial Manager",
        "Final author approval checklist",
    ]
    missing_cover = [phrase for phrase in cover_required if phrase not in cover]
    missing_decl = [phrase for phrase in decl_required if phrase not in declarations]
    if missing_cover:
        return fail("cover DOCX missing phrase(s): " + ", ".join(missing_cover))
    if missing_decl:
        return fail("declarations DOCX missing phrase(s): " + ", ".join(missing_decl))
    if "Generated DOCX companion files" not in qa or "Render QA" not in qa:
        return fail("QA report missing expected sections")
    if "SKIPPED" in qa and "LibreOffice/soffice is not available" not in qa:
        return fail("QA report has an unexplained skipped render")

    print("PASS upload-docx: cover letter, declarations DOCX and QA report verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
