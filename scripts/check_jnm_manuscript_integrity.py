#!/usr/bin/env python3
"""Check figure/table integrity in the JNM manuscript draft."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"


def resolve_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def ordered_unique(values: list[int]) -> list[int]:
    seen: set[int] = set()
    out: list[int] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def expected_sequence(values: list[int], label: str) -> list[str]:
    errors: list[str] = []
    if not values:
        errors.append(f"No {label} captions found")
        return errors
    expected = list(range(1, max(values) + 1))
    if values != expected:
        errors.append(f"{label} captions are {values}, expected {expected}")
    return errors


def main() -> int:
    text = MANUSCRIPT.read_text()
    errors: list[str] = []

    image_matches = list(
        re.finditer(r"^!\[Fig\. (\d+) \| ([^\]]+)\]\(([^)]+)\)", text, flags=re.MULTILINE)
    )
    image_numbers = [int(match.group(1)) for match in image_matches]
    caption_numbers = [
        int(match.group(1))
        for match in re.finditer(r"^\*\*Fig\. (\d+) \| ([^*]+)\.\*\*", text, flags=re.MULTILINE)
    ]
    table_numbers = [
        int(match.group(1))
        for match in re.finditer(r"^\*\*Table (\d+) \| ([^*]+)\.\*\*", text, flags=re.MULTILINE)
    ]

    errors.extend(expected_sequence(image_numbers, "figure image"))
    errors.extend(expected_sequence(caption_numbers, "figure"))
    errors.extend(expected_sequence(table_numbers, "table"))

    if image_numbers != caption_numbers:
        errors.append(f"Figure image numbers {image_numbers} do not match caption numbers {caption_numbers}")

    for match in image_matches:
        fig_no = int(match.group(1))
        path = resolve_path(match.group(3))
        if not path.exists():
            errors.append(f"Fig. {fig_no} image path does not exist: {path}")
        if path.suffix.lower() not in {".png", ".pdf", ".tif", ".tiff", ".svg"}:
            errors.append(f"Fig. {fig_no} has unexpected image suffix: {path.suffix}")

    body_without_captions = "\n".join(
        line
        for line in text.splitlines()
        if not line.startswith("![Fig.") and not line.startswith("**Fig.") and not line.startswith("**Table")
    )
    figure_refs = ordered_unique([int(value) for value in re.findall(r"\bFig\. (\d+)\b", body_without_captions)])
    table_refs = ordered_unique([int(value) for value in re.findall(r"\bTable (\d+)\b", body_without_captions)])
    missing_fig_refs = sorted(set(image_numbers) - set(figure_refs))
    missing_table_refs = sorted(set(table_numbers) - set(table_refs))
    if missing_fig_refs:
        errors.append("Figures not referenced in manuscript body: " + ", ".join(map(str, missing_fig_refs)))
    if missing_table_refs:
        errors.append("Tables not referenced in manuscript body: " + ", ".join(map(str, missing_table_refs)))

    duplicate_caption = re.search(r"\b(?:Fig\.|Figure|Table)\s+(?:Fig\.|Figure|Table)\b", text)
    if duplicate_caption:
        errors.append(f"Possible duplicated figure/table label near: {duplicate_caption.group(0)}")

    if errors:
        print("FAIL manuscript integrity")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "PASS manuscript integrity: "
        f"{len(image_numbers)} figures, {len(table_numbers)} tables, "
        f"{len(figure_refs)} figure refs, {len(table_refs)} table refs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
