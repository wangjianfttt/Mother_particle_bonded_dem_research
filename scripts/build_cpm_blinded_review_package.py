#!/usr/bin/env python3
"""Build an optional blinded-review manuscript package for CPM submission."""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
OUT_ROOT = ROOT / "submission_packages"
OUT_DIR = OUT_ROOT / "computational_particle_mechanics_blinded_review_optional"
OUT_ZIP = OUT_ROOT / "computational_particle_mechanics_blinded_review_optional.zip"

SOURCE_TEX = MANUSCRIPT / "computational_particle_mechanics_submission.tex"
BLINDED_TEX = MANUSCRIPT / "computational_particle_mechanics_blinded_submission.tex"
BLINDED_PDF = MANUSCRIPT / "computational_particle_mechanics_blinded_submission.pdf"

FORBIDDEN_BLINDED_TERMS = [
    "Jian Wang",
    "Siyu Wang",
    "Hang Zhang",
    "Ming-Zhun Lei",
    "Wei Wen",
    "Qi-Gang Wu",
    "Gang Shen",
    "Haishun Deng",
    "wjfttt@mail.ustc.edu.cn",
    "Anhui University of Science and Technology",
    "Institute of Plasma Physics",
    "Chinese Academy of Sciences",
    "Anhui Provincial Natural Science Foundation",
    "DSJJ-2025-08",
    "AIMTEERC202307",
    "2024M753266",
    "2022AH010052",
    "2021yjrc51",
    "2019HSC-CIP006",
    "wangjianfttt",
    "10.5281/zenodo.20687351",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replace_section(text: str, section: str, replacement: str) -> str:
    pattern = re.compile(
        rf"\\section\{{{re.escape(section)}\}}\n.*?(?=\n\\section\{{|\\bibliographystyle)",
        re.DOTALL,
    )
    updated, count = pattern.subn(lambda _match: replacement.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"section not found or duplicated: {section}")
    return updated


def remove_section(text: str, section: str) -> str:
    pattern = re.compile(
        rf"\n\\section\{{{re.escape(section)}\}}\n.*?(?=\n\\section\{{|\\bibliographystyle)",
        re.DOTALL,
    )
    updated, count = pattern.subn("\n", text, count=1)
    if count != 1:
        raise RuntimeError(f"section not found or duplicated: {section}")
    return updated


def build_blinded_tex() -> None:
    text = SOURCE_TEX.read_text(encoding="utf-8")
    filtered: list[str] = []
    inserted_anonymous = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("\\author", "\\ead", "\\cortext", "\\address")):
            continue
        filtered.append(line)
        if stripped.startswith("\\title{") and not inserted_anonymous:
            filtered.append("\\author{Anonymous author(s)}")
            inserted_anonymous = True
    text = "\n".join(filtered) + "\n"
    text = replace_section(
        text,
        "Data availability statement",
        r"""\section{Data availability statement}

Processed event tables, native force-network summaries, material-response tables, figure source data and post-processing scripts are supplied as anonymous supplementary review files. Repository identifiers and author-linked archive information will be restored in the accepted version.
""",
    )
    text = replace_section(
        text,
        "Code availability statement",
        r"""\section{Code availability statement}

Template-generation, run-control, figure-generation and post-processing scripts are supplied as anonymous supplementary review files. Author-linked repository identifiers will be restored in the accepted version.
""",
    )
    text = remove_section(text, "Acknowledgements")
    text = remove_section(text, "Author contributions")
    BLINDED_TEX.write_text(text, encoding="utf-8")


def compile_blinded_pdf() -> None:
    cmd = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        BLINDED_TEX.name,
    ]
    proc = subprocess.run(cmd, cwd=MANUSCRIPT, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.stdout + proc.stderr)
    if not BLINDED_PDF.exists():
        raise FileNotFoundError(BLINDED_PDF)


def check_blinded_text() -> None:
    text = BLINDED_TEX.read_text(encoding="utf-8", errors="ignore")
    found = [term for term in FORBIDDEN_BLINDED_TERMS if term in text]
    if found:
        raise SystemExit("Blinded TeX still contains identifying terms: " + ", ".join(found))


def reset_output() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    if OUT_ZIP.exists():
        OUT_ZIP.unlink()
    sha = Path(str(OUT_ZIP) + ".sha256")
    if sha.exists():
        sha.unlink()


def copy_outputs() -> None:
    reset_output()
    files = [
        (BLINDED_PDF, "01_blinded_manuscript.pdf"),
        (BLINDED_TEX, "01_blinded_manuscript.tex"),
        (MANUSCRIPT / "references.bib", "references.bib"),
    ]
    for src, name in files:
        shutil.copy2(src, OUT_DIR / name)
    (OUT_DIR / "README_blinded_review_optional.txt").write_text(
        "\n".join(
            [
                "Optional blinded-review package for Computational Particle Mechanics.",
                "",
                "Use this package only if the live submission system requests a blinded manuscript file.",
                "The main upload package remains submission_packages/computational_particle_mechanics_upload_ready.zip.",
                "",
                "Files:",
                "- 01_blinded_manuscript.pdf: author-identifying information removed.",
                "- 01_blinded_manuscript.tex: editable blinded LaTeX source.",
                "- references.bib: bibliography source used by the blinded TeX file.",
                "",
                "Author names, affiliations, e-mail address, acknowledgements, contribution statement, author-linked DOI and GitHub identifiers are absent from the blinded TeX source.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def zip_output() -> None:
    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(OUT_DIR.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(OUT_DIR.parent))
    Path(str(OUT_ZIP) + ".sha256").write_text(f"{sha256(OUT_ZIP)}  {OUT_ZIP.name}\n", encoding="utf-8")


def main() -> None:
    build_blinded_tex()
    check_blinded_text()
    compile_blinded_pdf()
    copy_outputs()
    zip_output()
    print(BLINDED_TEX)
    print(BLINDED_PDF)
    print(OUT_DIR)
    print(OUT_ZIP)
    print(Path(str(OUT_ZIP) + ".sha256"))


if __name__ == "__main__":
    main()
