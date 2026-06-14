#!/usr/bin/env python3
"""Create a compilable Nuclear Fusion working LaTeX draft from the Markdown manuscript."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "manuscript/nuclear_fusion_submission_draft.md"
TEX = ROOT / "manuscript/nuclear_fusion_iop_submission.tex"


FIGURES = {
    "fig1_workflow.png": ("../figures/main/fig1_workflow.pdf", "fig:workflow", "0.92", False, True),
    "single_pebble_calibration_evidence.png": (
        "../figures/sp002/single_pebble_calibration_evidence.pdf",
        "fig:single-pebble-calibration",
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
    "pb006_breakage_event_database.png": (
        "../figures/pb006/pb006_breakage_event_database.pdf",
        "fig:pb006-event-database",
        "0.92",
        False,
        True,
    ),
    "pb006_force_path_proxy.png": (
        "../figures/pb006/pb006_force_path_proxy.pdf",
        "fig:overlap-proxy",
        "0.92",
        False,
        True,
    ),
    "pb006_1000_0p15_three_stage_sequence.png": (
        "../figures/pb006/pb006_1000_0p15_three_stage_sequence.pdf",
        "fig:1000-three-stage",
        "0.92",
        False,
        True,
    ),
    "pb006_1000_orientation_sensitivity.png": (
        "../figures/pb006/pb006_1000_orientation_sensitivity.pdf",
        "fig:1000-variability",
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
        caption = "Stage-window summary for 1000-pebble bed A."
        label = "tab:stage-summary"
        resize = False
        span = False
    else:
        colspec = "lrrlrrrrrl"
        caption = "Summary of 500- and 1000-pebble event-sequence cases."
        label = "tab:event-summary"
        resize = True
        span = True
    table_env = "table"
    if span:
        out = [
            r"\begin{table*}[!t]",
            r"\centering",
            r"\caption{" + caption + "}",
            r"\label{" + label + "}",
            r"\footnotesize",
            r"\resizebox{0.98\textwidth}{!}{%",
            r"\begin{tabular}{" + colspec + "}",
            r"\hline",
        ]
        for idx, cells in enumerate(rows):
            converted = [convert_text(c) for c in cells]
            out.append(" & ".join(converted) + r" \\")
            if idx == 0:
                out.append(r"\hline")
        out += [
            r"\hline",
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
    out += [r"\begin{tabular}{" + colspec + "}", r"\hline"]
    for idx, cells in enumerate(rows):
        converted = [convert_text(c) for c in cells]
        out.append(" & ".join(converted) + r" \\")
        if idx == 0:
            out.append(r"\hline")
    out += [r"\hline", r"\end{tabular}%"]
    out.append(r"}")
    out.append(rf"\end{{{table_env}}}")
    return "\n".join(out), i


def convert_body(md: str) -> str:
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
    body = convert_body(md)
    tex = rf"""\documentclass[10pt,twocolumn]{{article}}
\usepackage[a4paper,margin=1.75cm,columnsep=0.62cm]{{geometry}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{natbib}}
\usepackage{{hyperref}}
\usepackage{{amsmath}}
\usepackage{{authblk}}
\usepackage{{caption}}
\usepackage{{dblfloatfix}}
\setlength{{\parindent}}{{1em}}
\setlength{{\parskip}}{{0pt}}
\setlength{{\textfloatsep}}{{8pt plus 2pt minus 2pt}}
\setlength{{\floatsep}}{{7pt plus 2pt minus 2pt}}
\setlength{{\intextsep}}{{7pt plus 2pt minus 2pt}}
\setlength{{\dbltextfloatsep}}{{8pt plus 2pt minus 2pt}}
\setlength{{\dblfloatsep}}{{7pt plus 2pt minus 2pt}}
\captionsetup{{font=footnotesize,labelfont=bf,skip=3pt}}
\emergencystretch=3em
\title{{{latex_escape(title)}}}
\author[1,2]{{Jian Wang\thanks{{Corresponding author: wjfttt@mail.ustc.edu.cn}}}}
\author[1]{{Siyu Wang}}
\author[1]{{Hang Zhang}}
\author[2]{{Ming-Zhun Lei}}
\author[1,2]{{Wei Wen}}
\author[2]{{Qi-Gang Wu}}
\author[1]{{Gang Shen}}
\author[1]{{Haishun Deng}}
\affil[1]{{Anhui University of Science and Technology, Huainan, Anhui 232001, China}}
\affil[2]{{Institute of Plasma Physics, Chinese Academy of Sciences, Hefei, Anhui 230031, China}}
\date{{}}

\begin{{document}}
\maketitle

{body}

\bibliographystyle{{unsrtnat}}
\bibliography{{references}}
\end{{document}}
"""
    TEX.write_text(tex)
    print(TEX)


if __name__ == "__main__":
    main()
