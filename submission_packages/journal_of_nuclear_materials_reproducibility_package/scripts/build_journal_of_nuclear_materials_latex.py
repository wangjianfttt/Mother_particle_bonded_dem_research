#!/usr/bin/env python3
"""Create a compilable Journal of Nuclear Materials working LaTeX draft."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "manuscript/journal_of_nuclear_materials_submission_draft.md"
TEX = ROOT / "manuscript/journal_of_nuclear_materials_submission.tex"


FIGURES = {
    "fig1_workflow.png": ("../figures/main/fig1_workflow.pdf", "fig:workflow", "0.92", False, True),
    "single_pebble_calibration_evidence.png": (
        "../figures/sp002/single_pebble_calibration_evidence.pdf",
        "fig:single-pebble-calibration",
        "0.92",
        False,
        True,
    ),
    "jnm_single_pebble_validation.png": (
        "../figures/sp002/jnm_single_pebble_validation.pdf",
        "fig:single-pebble-validation",
        "0.92",
        False,
        True,
    ),
    "single_pebble_fragment_morphology_paraview.png": (
        "../figures/sp002/single_pebble_fragment_morphology_paraview.png",
        "",
        "0.92",
        True,
        False,
    ),
    "sp002_force_displacement_overlay.png": (
        "../figures/sp002/sp002_force_displacement_overlay.pdf",
        "",
        "0.92",
        True,
        True,
    ),
    "pb007_acceptance_gate_validation.png": (
        "../figures/pb007/pb007_acceptance_gate_validation.pdf",
        "fig:pb007-force-validation",
        "0.92",
        False,
        True,
    ),
    "pb007_corrected_fracture_sequence.png": (
        "../figures/pb007/pb007_corrected_fracture_sequence.pdf",
        "fig:pb007-fracture-sequence",
        "0.92",
        False,
        True,
    ),
    "pb007_replicate_comparison.png": (
        "../figures/pb007/pb007_replicate_comparison.pdf",
        "fig:pb007-replicate-comparison",
        "0.92",
        False,
        True,
    ),
}


def latex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("Li4SiO4", r"Li$_4$SiO$_4$")
    text = text.replace(" m s-1", r" m s$^{-1}$")
    text = text.replace("0p15", "0p15")
    return text


def pdf_string(text: str) -> str:
    """Return plain text for PDF metadata and bookmarks."""
    return text.replace("Li4SiO4", "Li4SiO4")


def texorpdf(text: str) -> str:
    return r"\texorpdfstring{" + latex_escape(text) + "}{" + pdf_string(text) + "}"


def convert_cites(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        keys = [p.strip().lstrip("@") for p in match.group(1).split(";")]
        return r"\cite{" + ",".join(k for k in keys if k) + "}"

    return re.sub(r"\[@([^\]]+)\]", repl, text)


def convert_text(text: str) -> str:
    citations: list[str] = []

    def stash_cite(match: re.Match[str]) -> str:
        idx = len(citations)
        citations.append(convert_cites(match.group(0)))
        return f"@@CITE{idx}@@"

    text = re.sub(r"\[@[^\]]+\]", stash_cite, text)
    text = convert_inline_code(text)
    text = latex_escape(text)
    for idx, cite in enumerate(citations):
        text = text.replace(latex_escape(f"@@CITE{idx}@@"), cite)
    text = text.replace(r"\\_", r"\_")
    return text


def convert_inline_code(text: str) -> str:
    return re.sub(r"`([^`]+)`", lambda m: r"\texttt{" + latex_escape(m.group(1)) + "}", text)


def clean_caption_text(text: str) -> tuple[str, str]:
    text = re.sub(r"^\*\*(.*?)\.\*\*\s*", r"\1. ", text.strip())
    if "|" in text:
        label, rest = text.split("|", 1)
        caption = label.strip() + ". " + rest.strip()
    else:
        caption = text
    caption = re.sub(r"^Fig\.\s*\d+\.\s*", "", caption)
    title = caption.split(".", 1)[0].lower()
    return convert_text(caption), title


def convert_table(lines: list[str], start: int) -> tuple[str, int]:
    block = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        block.append(lines[i].strip())
        i += 1
    rows = []
    for row in block:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if all(set(c) <= {"-", ":", " "} for c in cells):
            continue
        rows.append(cells)
    header = rows[0] if rows else []
    if header and header[0] == "Stage":
        colspec = "lrrrr"
        caption = "Stage-window summary."
        label = "tab:stage-summary"
        resize = False
        span = False
    elif header and header[0] == "State variable":
        colspec = "llll"
        caption = "Material-degradation state-variable synthesis from the corrected calculations."
        label = "tab:material-state-variables"
        resize = True
        span = True
    elif header and header[0] == "Parameter":
        colspec = "llll"
        caption = "Model and bonded-template parameters used in the present simulations."
        label = "tab:model-parameters"
        resize = True
        span = True
    elif header and header[0] == "Quantity":
        colspec = "l" * max(1, len(header))
        caption = "Corrected fracture-sequence evidence."
        label = "tab:pb007-fracture-evidence"
        resize = True
        span = True
    else:
        colspec = "lll"
        caption = "Simulation summary."
        label = "tab:simulation-summary"
        resize = True
        span = False
    table_env = "table"
    if label == "tab:model-parameters":
        out = [
            r"\begin{strip}",
            r"\vspace{-0.6\baselineskip}",
            r"\centering",
            r"\captionof{table}{" + caption + "}",
            r"\label{" + label + "}",
            r"\scriptsize",
            r"\resizebox{0.98\textwidth}{!}{%",
            r"\begin{tabular}{" + colspec + "}",
            r"\toprule",
        ]
        for idx, cells in enumerate(rows):
            converted = [convert_text(c) for c in cells]
            out.append(" & ".join(converted) + r" \\")
            if idx == 0:
                out.append(r"\midrule")
        out += [
            r"\bottomrule",
            r"\end{tabular}%",
            r"}",
            r"\vspace{-0.6\baselineskip}",
            r"\end{strip}",
        ]
        return "\n".join(out), i
    if span:
        out = [
            r"\begin{table*}[!t]",
            r"\centering",
            r"\caption{" + caption + "}",
            r"\label{" + label + "}",
            r"\footnotesize",
            r"\resizebox{0.98\textwidth}{!}{%",
            r"\begin{tabular}{" + colspec + "}",
            r"\toprule",
        ]
        for idx, cells in enumerate(rows):
            converted = [convert_text(c) for c in cells]
            out.append(" & ".join(converted) + r" \\")
            if idx == 0:
                out.append(r"\midrule")
        out += [
            r"\bottomrule",
            r"\end{tabular}%",
            r"}",
            r"\end{table*}",
        ]
        return "\n".join(out), i
    out = [
        rf"\begin{{{table_env}}}[!t]",
        r"\centering",
        r"\caption{" + caption + "}",
        r"\label{" + label + "}",
    ]
    out += [r"\scriptsize", r"\resizebox{\linewidth}{!}{%"]
    out += [r"\begin{tabular}{" + colspec + "}", r"\toprule"]
    for idx, cells in enumerate(rows):
        converted = [convert_text(c) for c in cells]
        out.append(" & ".join(converted) + r" \\")
        if idx == 0:
            out.append(r"\midrule")
    out += [r"\bottomrule", r"\end{tabular}%"]
    out.append(r"}")
    out.append(rf"\end{{{table_env}}}")
    return "\n".join(out), i


def convert_body(md: str, keywords: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    before_abstract = True
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("## Abstract"):
            before_abstract = False
        if stripped.startswith("Target journal:") or stripped.startswith("Article type:") or stripped.startswith("Keywords:"):
            i += 1
            continue
        if before_abstract and (
            stripped.startswith("Authors:")
            or stripped.startswith("Affiliations:")
            or stripped.startswith("Author affiliations:")
            or stripped.startswith("*Corresponding author:")
            or re.match(r"^\d+\.\s", stripped)
            or stripped.startswith("- ")
        ):
            i += 1
            continue
        if stripped.startswith("!["):
            path_match = re.search(r"\(([^)]+)\)", stripped)
            caption_line = lines[i + 2] if i + 2 < len(lines) and lines[i + 1].strip() == "" else lines[i + 1]
            path = path_match.group(1) if path_match else ""
            basename = Path(path).name
            figure_file, label, width, unnumbered, span = FIGURES.get(basename, (path, "fig:unknown", "0.95", False, False))
            caption, _ = clean_caption_text(caption_line)
            figure_env = "figure*" if span else "figure"
            width_unit = r"\textwidth" if span else r"\linewidth"
            out += [
                rf"\begin{{{figure_env}}}[!t]",
                r"\centering",
                r"\includegraphics[width=" + width + width_unit + "]{" + figure_file + "}",
            ]
            if unnumbered:
                out.append(r"\caption*{" + caption + "}")
            else:
                out += [r"\caption{" + caption + "}", r"\label{" + label + "}"]
            out += [rf"\end{{{figure_env}}}", ""]
            i += 3 if i + 1 < len(lines) and lines[i + 1].strip() == "" else 2
            continue
        if stripped.startswith("|"):
            table_tex, i = convert_table(lines, i)
            out.append(table_tex)
            out.append("")
            continue
        if stripped.startswith("# "):
            i += 1
            continue
        if stripped.startswith("## Abstract"):
            out.append(r"\begin{abstract}")
            i += 1
            continue
        if stripped.startswith("## "):
            if out and out[-1] == r"\begin{abstract}":
                pass
            title = stripped[3:]
            if title == "Introduction" and r"\begin{abstract}" in out:
                out.append(r"\end{abstract}")
                out.append("")
                out.append(r"\begin{keyword}")
                out.append(convert_text(keywords))
                out.append(r"\end{keyword}")
                out.append(r"\end{frontmatter}")
                out.append("")
            if title not in {"References"}:
                out.append(r"\section{" + latex_escape(title) + "}")
            i += 1
            continue
        if stripped.startswith("### "):
            out.append(r"\subsection{" + latex_escape(stripped[4:]) + "}")
            i += 1
            continue
        if stripped.startswith("**") and "| " in stripped:
            i += 1
            continue
        if stripped:
            text = convert_text(stripped)
            out.append(text)
            out.append("")
        else:
            out.append("")
        i += 1
    return "\n".join(out)


def main() -> None:
    md = MD.read_text()
    title = re.match(r"# (.+)", md).group(1)
    keyword_match = re.search(r"^Keywords:\s*(.+)$", md, re.MULTILINE)
    keywords = keyword_match.group(1) if keyword_match else "Li4SiO4; ceramic breeder material; pebble bed; fracture-event sequence"
    body = convert_body(md, keywords)
    tex = rf"""\documentclass[5p,twocolumn]{{elsarticle}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\biboptions{{numbers,sort&compress}}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{{hyperref}}
\pdfstringdefDisableCommands{{%
  \def\corref#1{{}}%
  \def\cnotenum#1{{}}%
}}
\usepackage{{amsmath}}
\usepackage{{caption}}
\usepackage{{dblfloatfix}}
\usepackage{{cuted}}
\setlength{{\parindent}}{{1em}}
\setlength{{\parskip}}{{0pt}}
\setlength{{\textfloatsep}}{{8pt plus 2pt minus 2pt}}
\setlength{{\floatsep}}{{7pt plus 2pt minus 2pt}}
\setlength{{\intextsep}}{{7pt plus 2pt minus 2pt}}
\setlength{{\dbltextfloatsep}}{{8pt plus 2pt minus 2pt}}
\setlength{{\dblfloatsep}}{{7pt plus 2pt minus 2pt}}
\captionsetup{{font=footnotesize,labelfont=bf,skip=3pt}}
\emergencystretch=3em

\journal{{Journal of Nuclear Materials}}

\begin{{document}}
\begin{{frontmatter}}
\title{{{texorpdf(title)}}}
\author[aff1,aff2]{{Jian Wang\corref{{cor1}}}}
\ead{{wjfttt@mail.ustc.edu.cn}}
\author[aff1]{{Siyu Wang}}
\author[aff1]{{Hang Zhang}}
\author[aff2]{{Ming-Zhun Lei}}
\author[aff1,aff2]{{Wei Wen}}
\author[aff2]{{Qi-Gang Wu}}
\author[aff1]{{Gang Shen}}
\author[aff1]{{Haishun Deng}}
\cortext[cor1]{{Corresponding author.}}
\address[aff1]{{Anhui University of Science and Technology, Huainan, Anhui 232001, China}}
\address[aff2]{{Institute of Plasma Physics, Chinese Academy of Sciences, Hefei, Anhui 230031, China}}

{body}

\bibliographystyle{{elsarticle-num}}
\bibliography{{references}}
\end{{document}}
"""
    TEX.write_text(tex)
    print(TEX)


if __name__ == "__main__":
    main()
