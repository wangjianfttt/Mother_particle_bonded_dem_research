#!/usr/bin/env python3
"""Build paste-ready Editorial Manager fields for the JNM submission."""

from __future__ import annotations

import csv
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
HIGHLIGHTS = ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"
DECLARATIONS = ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md"
AUTHOR_CSV = ROOT / "manuscript/journal_of_nuclear_materials_author_metadata.csv"
OUTPUT = ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_line_value(text: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}:\s*(.+)$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"Missing line: {label}:")
    return match.group(1).strip()


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=\n## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"Missing section: ## {heading}")
    return match.group("body").strip()


def declaration_section(text: str, heading: str) -> str:
    return section(text, heading)


def plain_paragraph(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("![") or stripped.startswith("**Fig."):
            continue
        lines.append(stripped)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def highlight_bullets(text: str) -> list[str]:
    bullets = [line.removeprefix("-").strip() for line in text.splitlines() if line.strip().startswith("-")]
    if not bullets:
        raise ValueError("No highlights found")
    return bullets


def author_rows() -> list[dict[str, str]]:
    with AUTHOR_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def affiliations_from_manuscript(text: str) -> list[str]:
    body = section(text, "Introduction")
    del body
    affiliations_match = re.search(r"^Affiliations:\s*\n\n(?P<body>.*?)(?=\nAuthor affiliations:)", text, re.S | re.M)
    if not affiliations_match:
        raise ValueError("Missing Affiliations block")
    return [line.strip() for line in affiliations_match.group("body").splitlines() if line.strip()]


def author_affiliation_lines(rows: list[dict[str, str]]) -> list[str]:
    lines = []
    for row in rows:
        suffix = " (corresponding author)" if row["corresponding_author"].lower() == "yes" else ""
        email = f"; email: {row['email']}" if row.get("email") else ""
        lines.append(
            f"- {row['display_name']}: affiliation ids {row['affiliation_ids']}; "
            f"{row['affiliations']}{email}{suffix}"
        )
    return lines


def credit_lines(rows: list[dict[str, str]]) -> list[str]:
    return [f"{row['display_name']}: {row['credit_roles']}." for row in rows]


def wrap_field(text: str) -> str:
    return textwrap.fill(text.strip(), width=100, break_long_words=False, break_on_hyphens=False)


def main() -> int:
    manuscript_text = read_text(MANUSCRIPT)
    highlights_text = read_text(HIGHLIGHTS)
    declarations_text = read_text(DECLARATIONS)
    rows = author_rows()

    title = manuscript_text.splitlines()[0].removeprefix("#").strip()
    article_type = first_line_value(manuscript_text, "Article type")
    keywords = first_line_value(manuscript_text, "Keywords")
    authors = first_line_value(manuscript_text, "Authors")
    corresponding = first_line_value(manuscript_text, "*Corresponding author")
    abstract = plain_paragraph(section(manuscript_text, "Abstract"))
    data_statement = plain_paragraph(section(manuscript_text, "Data availability statement"))
    code_statement = plain_paragraph(section(manuscript_text, "Code availability statement"))
    funding = declaration_section(declarations_text, "Funding declaration")
    role_of_funder = declaration_section(declarations_text, "Role of the funding source")
    ai_declaration = declaration_section(
        declarations_text,
        "Declaration of generative AI and AI-assisted technologies in the writing process",
    )
    competing_interest = declaration_section(declarations_text, "Declaration of competing interest")
    highlights = highlight_bullets(highlights_text)
    affiliations = affiliations_from_manuscript(manuscript_text)

    lines = [
        "# Journal of Nuclear Materials Editorial Manager paste fields",
        "",
        "Generated from the active manuscript, highlights, declaration and author-metadata files.",
        "The corresponding author should paste these fields into Editorial Manager after final repository deposit.",
        "",
        "## Title",
        "",
        title,
        "",
        "## Article type",
        "",
        article_type,
        "",
        "## Authors",
        "",
        authors,
        "",
        "## Corresponding author",
        "",
        corresponding,
        "",
        "## Affiliations",
        "",
        *affiliations,
        "",
        "## Author-affiliation metadata",
        "",
        *author_affiliation_lines(rows),
        "",
        "## Abstract",
        "",
        wrap_field(abstract),
        "",
        "## Keywords",
        "",
        keywords,
        "",
        "## Highlights",
        "",
        *[f"- {bullet}" for bullet in highlights],
        "",
        "## Data availability statement",
        "",
        wrap_field(data_statement),
        "",
        "## Code availability statement",
        "",
        wrap_field(code_statement),
        "",
        "## Declaration of competing interest",
        "",
        wrap_field(competing_interest),
        "",
        "## Funding declaration",
        "",
        wrap_field(funding),
        "",
        "## Role of the funding source",
        "",
        wrap_field(role_of_funder),
        "",
        "## Declaration of generative AI and AI-assisted technologies in the writing process",
        "",
        wrap_field(ai_declaration),
        "",
        "## CRediT authorship contribution statement",
        "",
        " ".join(credit_lines(rows)),
        "",
        "## Repository DOI action",
        "",
        "Repository DOI or stable URL is still pending. Deposit the reduced reproducibility package first, "
        "then run `python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> "
        "--apply --rebuild` before final upload.",
        "",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
