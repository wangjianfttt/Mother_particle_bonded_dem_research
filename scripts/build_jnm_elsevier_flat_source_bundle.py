#!/usr/bin/env python3
"""Build a flat LaTeX source bundle for Elsevier Editorial Manager upload."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
OUT_DIR = ROOT / "submission_packages" / "journal_of_nuclear_materials_flat_source"
ZIP_PATH = ROOT / "submission_packages" / "journal_of_nuclear_materials_flat_source.zip"
TEX_IN = MANUSCRIPT / "journal_of_nuclear_materials_submission.tex"
TEX_OUT = OUT_DIR / "journal_of_nuclear_materials_submission.tex"
ELSARTICLE_NUM_BST = Path("/usr/local/texlive/2021/texmf-dist/bibtex/bst/elsarticle/elsarticle-num.bst")


def copy_required_sources() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    for name in [
        "journal_of_nuclear_materials_submission.bbl",
        "references.bib",
    ]:
        shutil.copy2(MANUSCRIPT / name, OUT_DIR / name)
    if ELSARTICLE_NUM_BST.exists():
        shutil.copy2(ELSARTICLE_NUM_BST, OUT_DIR / ELSARTICLE_NUM_BST.name)


def flatten_graphics(tex: str) -> str:
    pattern = re.compile(r"(\\includegraphics(?:\[[^\]]*\])?\{)([^}]+)(\})")
    copied: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        prefix, source, suffix = match.groups()
        source_path = (MANUSCRIPT / source).resolve()
        if not source_path.exists():
            source_path = (ROOT / source).resolve()
        if not source_path.exists():
            raise FileNotFoundError(f"Could not resolve included graphic: {source}")
        flat_name = source_path.name
        if flat_name in copied and copied[flat_name] != str(source_path):
            stem = source_path.stem.replace(".", "_")
            flat_name = f"{stem}_{len(copied)}{source_path.suffix}"
        shutil.copy2(source_path, OUT_DIR / flat_name)
        copied[flat_name] = str(source_path)
        return f"{prefix}{flat_name}{suffix}"

    return pattern.sub(repl, tex)


def write_flat_tex() -> None:
    tex = TEX_IN.read_text()
    tex = flatten_graphics(tex)
    # Keep references in the same folder and avoid relying on subfolder paths.
    tex = tex.replace(r"\bibliography{references}", r"\bibliography{references}")
    TEX_OUT.write_text(tex)


def write_readme() -> None:
    (OUT_DIR / "README_flat_source.txt").write_text(
        "\n".join(
            [
                "Flat LaTeX source bundle for Journal of Nuclear Materials submission.",
                "",
                "All .tex, .bbl, .bib and figure files are stored at this single folder level",
                "because Elsevier Editorial Manager may not process subfolder paths in LaTeX uploads.",
                "The Elsevier numeric bibliography style file elsarticle-num.bst is included when available.",
                "",
                "Compile locally with:",
                "  latexmk -xelatex -interaction=nonstopmode -halt-on-error journal_of_nuclear_materials_submission.tex",
                "",
                "The graphical abstract and reproducibility package are separate upload items, not embedded in this LaTeX source.",
            ]
        )
        + "\n"
    )


def zip_bundle() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    subprocess.run(
        ["zip", "-qr", str(ZIP_PATH), OUT_DIR.name],
        cwd=OUT_DIR.parent,
        check=True,
    )
    sha_path = ZIP_PATH.with_suffix(ZIP_PATH.suffix + ".sha256")
    digest = subprocess.check_output(["shasum", "-a", "256", str(ZIP_PATH)], text=True)
    sha_path.write_text(digest)


def compile_flat_source_for_qa() -> None:
    """Compile after zipping so QA logs exist without entering the upload zip."""
    subprocess.run(
        [
            "latexmk",
            "-xelatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            TEX_OUT.name,
        ],
        cwd=OUT_DIR,
        check=True,
    )


def main() -> None:
    copy_required_sources()
    write_flat_tex()
    write_readme()
    zip_bundle()
    compile_flat_source_for_qa()
    print(OUT_DIR)
    print(ZIP_PATH)


if __name__ == "__main__":
    main()
