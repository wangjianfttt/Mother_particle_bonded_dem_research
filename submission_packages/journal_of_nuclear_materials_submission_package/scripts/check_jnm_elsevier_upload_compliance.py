#!/usr/bin/env python3
"""Check Elsevier/JNM upload-package compliance items.

This gate complements the scientific evidence checks. It verifies the
administrative and file-format details that commonly matter during Elsevier
Editorial Manager upload: clean LaTeX source bundle, Highlights constraints,
graphical-abstract dimensions, declarations/data-availability support and
source-file role separation.
"""

from __future__ import annotations

import csv
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FLAT_ZIP = ROOT / "submission_packages/journal_of_nuclear_materials_flat_source.zip"
MAIN_ZIP = ROOT / "submission_packages/journal_of_nuclear_materials_submission_package.zip"
TEX = ROOT / "manuscript/journal_of_nuclear_materials_submission.tex"
HIGHLIGHTS = ROOT / "manuscript/journal_of_nuclear_materials_highlights.md"
GRAPHICAL_ABSTRACT = ROOT / "figures/main/journal_of_nuclear_materials_graphical_abstract.png"
UPLOAD_MATRIX = ROOT / "manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv"
DECLARATIONS = ROOT / "manuscript/journal_of_nuclear_materials_elsevier_declarations.md"
README = ROOT / "manuscript/journal_of_nuclear_materials_repository_metadata_readme.md"
AUTHOR_UPLOAD_README_ZH = ROOT / "docs/jnm_author_final_upload_readme_zh.md"
CURRENT_FROZEN_DIR = "submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e"
CURRENT_PUBLIC_REPRO_SHA = "b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30"
CURRENT_PUBLIC_REPRO_FILE_COUNT = "125 个文件"

GRAPHICAL_ABSTRACT_MIN_WIDTH = 1328
GRAPHICAL_ABSTRACT_MIN_HEIGHT = 531


def fail(message: str) -> int:
    print(f"FAIL elsevier-upload-compliance: {message}")
    return 1


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if not header.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"{path} is not a PNG file")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def highlight_lines() -> list[str]:
    lines: list[str] = []
    for raw in HIGHLIGHTS.read_text().splitlines():
        line = raw.strip()
        if line.startswith("- "):
            lines.append(line[2:].strip())
    return lines


def check_highlights() -> list[str]:
    problems: list[str] = []
    lines = highlight_lines()
    if not 3 <= len(lines) <= 5:
        problems.append(f"Highlights should contain 3-5 bullets, found {len(lines)}")
    long_lines = [line for line in lines if len(line) > 85]
    if long_lines:
        problems.append("Highlights exceed 85 characters: " + "; ".join(long_lines))
    return problems


def check_graphical_abstract() -> list[str]:
    width, height = png_dimensions(GRAPHICAL_ABSTRACT)
    if width < GRAPHICAL_ABSTRACT_MIN_WIDTH or height < GRAPHICAL_ABSTRACT_MIN_HEIGHT:
        return [
            "Graphical abstract is "
            f"{width}x{height}px; expected at least "
            f"{GRAPHICAL_ABSTRACT_MIN_WIDTH}x{GRAPHICAL_ABSTRACT_MIN_HEIGHT}px"
        ]
    return []


def check_flat_source_zip() -> list[str]:
    problems: list[str] = []
    with zipfile.ZipFile(FLAT_ZIP) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        tex_members = [name for name in names if Path(name).name == "journal_of_nuclear_materials_submission.tex"]
        flat_tex = archive.read(tex_members[0]).decode("utf-8") if tex_members else ""
    basenames = {Path(name).name for name in names}
    required = {
        "journal_of_nuclear_materials_submission.tex",
        "journal_of_nuclear_materials_submission.bbl",
        "references.bib",
        "elsarticle-num.bst",
        "README_flat_source.txt",
        "fig1_workflow.pdf",
        "single_pebble_calibration_evidence.pdf",
        "jnm_single_pebble_validation.pdf",
        "pb007_acceptance_gate_validation.pdf",
        "pb007_corrected_fracture_sequence.pdf",
        "pb007_replicate_comparison.pdf",
    }
    missing = sorted(required - basenames)
    if missing:
        problems.append("Flat source bundle missing: " + ", ".join(missing))
    forbidden_suffixes = {".aux", ".log", ".out", ".xdv", ".fls", ".fdb_latexmk", ".synctex", ".gz"}
    forbidden = [
        name
        for name in names
        if any(name.endswith(suffix) for suffix in forbidden_suffixes)
    ]
    if forbidden:
        problems.append("Flat source bundle contains generated build artifacts: " + ", ".join(forbidden))
    nested_depth = [name for name in names if len(Path(name).parts) > 2]
    if nested_depth:
        problems.append("Flat source bundle should be single-folder flat; nested files: " + ", ".join(nested_depth))
    if "elsarticle" not in flat_tex or r"\begin{frontmatter}" not in flat_tex:
        problems.append("Flat source TeX is not in Elsevier elsarticle/frontmatter form")
    if r"\bibliographystyle{elsarticle-num}" not in flat_tex:
        problems.append("Flat source TeX is not using elsarticle-num bibliography style")
    return problems


def check_main_tex_class() -> list[str]:
    text = TEX.read_text()
    problems: list[str] = []
    if "elsarticle" not in text:
        problems.append("Main manuscript TeX is not using elsarticle")
    for marker in [r"\begin{frontmatter}", r"\end{frontmatter}", r"\begin{keyword}", r"\journal{Journal of Nuclear Materials}"]:
        if marker not in text:
            problems.append(f"Main manuscript TeX missing {marker}")
    if r"\bibliographystyle{elsarticle-num}" not in text:
        problems.append("Main manuscript TeX is not using elsarticle-num bibliography style")
    return problems


def check_main_zip_roles() -> list[str]:
    problems: list[str] = []
    with zipfile.ZipFile(MAIN_ZIP) as archive:
        names = set(archive.namelist())
    required_members = {
        "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_submission.pdf",
        "journal_of_nuclear_materials_submission_package/journal_of_nuclear_materials_flat_source.zip",
        "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_highlights.md",
        "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_cover_letter_draft.md",
        "journal_of_nuclear_materials_submission_package/manuscript/journal_of_nuclear_materials_elsevier_declarations.md",
        "journal_of_nuclear_materials_submission_package/docs/jnm_author_final_upload_readme_zh.md",
        "journal_of_nuclear_materials_submission_package/figures/main/journal_of_nuclear_materials_graphical_abstract.png",
        "journal_of_nuclear_materials_submission_package/figures/main/journal_of_nuclear_materials_graphical_abstract.tiff",
    }
    missing = sorted(required_members - names)
    if missing:
        problems.append("Main package missing upload-role artifact(s): " + ", ".join(missing))
    return problems


def check_upload_matrix() -> list[str]:
    problems: list[str] = []
    rows = list(csv.DictReader(UPLOAD_MATRIX.open()))
    roles = {
        row.get("Editorial Manager item", "")
        or row.get("item", "")
        or row.get("editorial_manager_role", "")
        for row in rows
    }
    required_roles = {
        "Manuscript",
        "Flat source bundle",
        "Highlights",
        "Cover letter",
        "Graphical abstract",
        "Supplementary material",
        "Declarations",
        "Reduced reproducibility package",
    }
    missing = sorted(required_roles - roles)
    if missing:
        problems.append("Upload matrix missing role(s): " + ", ".join(missing))
    rows_by_item = {row.get("item", ""): row for row in rows}
    repro_row = rows_by_item.get("Reduced reproducibility package")
    if repro_row is None:
        problems.append("Upload matrix missing Reduced reproducibility package row")
    else:
        expected_zip = (
            CURRENT_FROZEN_DIR
            + "/journal_of_nuclear_materials_reproducibility_package.zip"
        )
        expected_sha = expected_zip + ".sha256"
        actual_zip = repro_row.get("primary_file", "")
        actual_sha = repro_row.get("alternate_or_source_file", "")
        if actual_zip != expected_zip:
            problems.append(
                "Reduced reproducibility package should point to the frozen repository-deposit zip, "
                f"got {actual_zip}"
            )
        if actual_sha != expected_sha:
            problems.append(
                "Reduced reproducibility package checksum should point to the frozen repository-deposit checksum, "
                f"got {actual_sha}"
            )
        for rel in [actual_zip, actual_sha]:
            if rel and not (ROOT / rel).exists():
                problems.append(f"Upload matrix references missing repository-deposit file: {rel}")
    return problems


def check_text_support() -> list[str]:
    problems: list[str] = []
    declarations = DECLARATIONS.read_text()
    required_declaration_terms = [
        "competing interest",
        "Funding",
        "Role of the funding source",
        "Declaration of generative AI",
        "Data availability",
        "Code availability",
    ]
    declarations_lower = declarations.lower()
    missing_terms = [term for term in required_declaration_terms if term.lower() not in declarations_lower]
    if missing_terms:
        problems.append("Declarations file missing section(s): " + ", ".join(missing_terms))
    readme = README.read_text()
    required_readme_terms = [
        "insert_jnm_repository_identifier.py",
        "--dry-run",
        "--apply --rebuild",
        "Do not hand-edit",
    ]
    missing_readme = [term for term in required_readme_terms if term not in readme]
    if missing_readme:
        problems.append("Repository metadata README missing guidance: " + ", ".join(missing_readme))
    upload_readme = AUTHOR_UPLOAD_README_ZH.read_text()
    required_upload_readme_terms = [
        "Editorial Manager",
        "insert_jnm_repository_identifier.py",
        "overall_status=PASS",
        CURRENT_FROZEN_DIR,
        CURRENT_PUBLIC_REPRO_SHA,
        CURRENT_PUBLIC_REPRO_FILE_COUNT,
        "journal_of_nuclear_materials_submission.pdf",
        "journal_of_nuclear_materials_flat_source.zip",
        "journal_of_nuclear_materials_editorial_manager_paste_fields.md",
        "Jian Wang",
        "wjfttt@mail.ustc.edu.cn",
    ]
    missing_upload_readme = [term for term in required_upload_readme_terms if term not in upload_readme]
    if missing_upload_readme:
        problems.append("Author final upload README missing guidance: " + ", ".join(missing_upload_readme))
    return problems


def main() -> int:
    problems: list[str] = []
    for checker in [
        check_highlights,
        check_graphical_abstract,
        check_main_tex_class,
        check_flat_source_zip,
        check_main_zip_roles,
        check_upload_matrix,
        check_text_support,
    ]:
        problems.extend(checker())
    if problems:
        return fail("; ".join(problems))
    width, height = png_dimensions(GRAPHICAL_ABSTRACT)
    print(
        "PASS elsevier-upload-compliance: "
        f"{len(highlight_lines())} highlights; graphical abstract {width}x{height}px; "
        "elsarticle/frontmatter source, elsarticle-num bibliography style, flat source, upload roles, frozen repository-package routing, declarations, author upload README and DOI-insertion guidance verified"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
