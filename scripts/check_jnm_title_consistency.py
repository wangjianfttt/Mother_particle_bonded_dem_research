#!/usr/bin/env python3
"""Check title consistency across JNM submission and repository files."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"

TEXT_FILES = [
    ROOT / "manuscript/journal_of_nuclear_materials_cover_letter_draft.md",
    ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md",
    ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md",
    ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md",
    ROOT / "manuscript/journal_of_nuclear_materials_repro_package_readme.md",
    ROOT / "docs/jnm_coauthor_final_approval_packet.md",
]
TEX = ROOT / "manuscript/journal_of_nuclear_materials_submission.tex"
JSON_METADATA = ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json"


def manuscript_title() -> str:
    first = MANUSCRIPT.read_text(encoding="utf-8").splitlines()[0].strip()
    if not first.startswith("# "):
        raise RuntimeError("manuscript draft first line is not an H1 title")
    return first.removeprefix("# ").strip()


def normalized_title(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tex_plain_title(tex: str) -> str:
    match = re.search(r"\\title\{\\texorpdfstring\{.*?\}\{(?P<title>.*?)\}\}", tex, re.DOTALL)
    return normalized_title(match.group("title")) if match else ""


def main() -> int:
    errors: list[str] = []
    title = manuscript_title()
    if "Li4SiO4" not in title or "fracture sequences" not in title:
        errors.append("authoritative manuscript title is missing Li4SiO4 fracture-sequence framing")

    for path in TEXT_FILES:
        text = path.read_text(encoding="utf-8")
        if title not in text:
            errors.append(f"title mismatch or missing in {path.relative_to(ROOT)}")

    tex_title = tex_plain_title(TEX.read_text(encoding="utf-8"))
    if tex_title != title:
        errors.append(f"plain-text TeX title mismatch: {tex_title!r}")

    metadata = json.loads(JSON_METADATA.read_text(encoding="utf-8"))
    description = metadata.get("description", "")
    if title not in description:
        errors.append("repository metadata description does not cite manuscript title")

    stale_fragments = [
        "Nuclear Fusion",
        "fracture propagation in ceramic breeder beds",
        "bonded-template fracture statistics",
    ]
    checked_text = "\n".join(path.read_text(encoding="utf-8") for path in TEXT_FILES)
    for fragment in stale_fragments:
        if fragment in checked_text:
            errors.append(f"stale title/scope fragment found in title-sensitive files: {fragment}")

    if errors:
        print("FAIL title consistency")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS title consistency: {len(TEXT_FILES) + 2} title-sensitive files match manuscript title")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
