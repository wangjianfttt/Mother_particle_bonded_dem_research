#!/usr/bin/env python3
"""Create a single-column LaTeX/PDF-ready draft from the repaired manuscript."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "manuscript/repaired_full_submission_draft.md"
TEX = ROOT / "manuscript/repaired_full_submission.tex"


FIGURES = {
    "fig1_workflow.png": ("../figures/main/fig1_workflow.pdf", "fig:workflow", "0.92"),
    "fig2_single_pebble_template_validation.png": (
        "../figures/apt_redesign/fig2_single_pebble_template_validation.pdf",
        "fig:single-pebble-template-validation",
        "0.92",
    ),
    "fig3_entry_state_validation.png": (
        "../figures/apt_redesign/fig3_entry_state_validation.pdf",
        "fig:entry-state-validation",
        "0.92",
    ),
    "fig4_pilot_fracture_event_sequence.png": (
        "../figures/apt_redesign/fig4_pilot_fracture_event_sequence.pdf",
        "fig:pilot-fracture-sequence",
        "0.92",
    ),
    "fig5_mechanism_state_space.png": (
        "../figures/apt_redesign/fig5_mechanism_state_space.pdf",
        "fig:mechanism-state-space",
        "0.92",
    ),
    "pb007_replicate_comparison.png": (
        "../figures/pb007/pb007_replicate_comparison.pdf",
        "fig:mechanism-state-space",
        "0.98",
    ),
    "pb007_material_strength_response.png": (
        "../figures/pb007/pb007_material_strength_response.pdf",
        "fig:material-strength-response",
        "0.92",
    ),
}


TABLE_SPECS = {
    "Parameter": (
        r">{\raggedright\arraybackslash}p{0.29\textwidth}"
        r">{\raggedright\arraybackslash}p{0.18\textwidth}"
        r">{\raggedright\arraybackslash}X",
        "tab:model-parameters",
        r"\scriptsize",
    ),
    "Quantity": (
        r">{\raggedright\arraybackslash}p{0.17\textwidth}"
        r">{\raggedright\arraybackslash}p{0.17\textwidth}"
        r">{\raggedright\arraybackslash}p{0.22\textwidth}"
        r">{\raggedright\arraybackslash}p{0.17\textwidth}"
        r">{\raggedright\arraybackslash}X",
        "tab:fracture-sequence",
        r"\scriptsize",
    ),
    "State variable": (
        r">{\raggedright\arraybackslash}p{0.20\textwidth}"
        r">{\raggedright\arraybackslash}p{0.30\textwidth}"
        r">{\raggedright\arraybackslash}p{0.25\textwidth}"
        r">{\raggedright\arraybackslash}X",
        "tab:state-variables",
        r"\scriptsize",
    ),
    "Geometry class": (
        r">{\raggedright\arraybackslash}p{0.18\textwidth}"
        r">{\centering\arraybackslash}p{0.10\textwidth}"
        r">{\centering\arraybackslash}p{0.14\textwidth}"
        r">{\centering\arraybackslash}p{0.12\textwidth}"
        r">{\centering\arraybackslash}p{0.12\textwidth}"
        r">{\centering\arraybackslash}p{0.12\textwidth}"
        r">{\centering\arraybackslash}X",
        "tab:strength-matrix",
        r"\tiny",
    ),
}


def latex_escape(text: str) -> str:
    placeholders: list[str] = []

    def stash(pattern: str, value: str) -> str:
        placeholders.append(value)
        return f"@@PLACEHOLDER{len(placeholders)-1}@@"

    text = re.sub(r"\\cite\{[^}]+\}", lambda m: stash("", m.group(0)), text)
    text = re.sub(r"\\url\{[^}]+\}", lambda m: stash("", m.group(0)), text)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace("Li4SiO4", r"Li$_4$SiO$_4$")
    text = text.replace(" m s-1", r" m s$^{-1}$")
    text = text.replace(" kg m-3", r" kg m$^{-3}$")
    text = text.replace(" N m-3", r" N m$^{-3}$")
    text = text.replace("1.0e14", r"$1.0\times10^{14}$")
    text = text.replace("5.0e13", r"$5.0\times10^{13}$")
    text = text.replace("1.5e10", r"$1.5\times10^{10}$")
    text = text.replace("1.638e-2", r"$1.638\times10^{-2}$")
    text = text.replace("1.559e-2", r"$1.559\times10^{-2}$")
    text = text.replace("500-subparticle", "500-subparticle")
    for idx, value in enumerate(placeholders):
        text = text.replace(latex_escape(f"@@PLACEHOLDER{idx}@@"), value)
    return text


def convert_cites(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        keys = [part.strip().lstrip("@") for part in match.group(1).split(";")]
        return r"\cite{" + ",".join(key for key in keys if key) + "}"

    return re.sub(r"\[@([^\]]+)\]", repl, text)


def convert_text(text: str) -> str:
    citations: list[str] = []
    urls: list[str] = []
    inline_codes: list[str] = []

    def stash_cite(match: re.Match[str]) -> str:
        citations.append(convert_cites(match.group(0)))
        return f"@@CITE{len(citations)-1}@@"

    def stash_url(match: re.Match[str]) -> str:
        urls.append(r"\url{" + match.group(0) + "}")
        return f"@@URL{len(urls)-1}@@"

    def stash_code(match: re.Match[str]) -> str:
        inline_codes.append(r"\texttt{" + latex_escape(match.group(1)) + "}")
        return f"@@CODE{len(inline_codes)-1}@@"

    text = re.sub(r"\[@[^\]]+\]", stash_cite, text)
    text = re.sub(r"https?://[^\s,.;]+(?:[.,;][^\s,.;]+)*", stash_url, text)
    text = re.sub(r"`([^`]+)`", stash_code, text)
    text = latex_escape(text)
    for idx, cite in enumerate(citations):
        text = text.replace(latex_escape(f"@@CITE{idx}@@"), cite)
    for idx, url in enumerate(urls):
        text = text.replace(latex_escape(f"@@URL{idx}@@"), url)
    for idx, code in enumerate(inline_codes):
        text = text.replace(latex_escape(f"@@CODE{idx}@@"), code)
    return text


def clean_caption_text(text: str) -> str:
    text = re.sub(r"^\*\*(.*?)\.\*\*\s*", r"\1. ", text.strip())
    if "|" in text:
        label, rest = text.split("|", 1)
        text = f"{label.strip()}. {rest.strip()}"
    text = re.sub(r"^Fig\.\s*\d+\.\s*", "", text)
    return convert_text(text)


def table_caption(line: str) -> str:
    stripped = line.strip().strip("*")
    stripped = re.sub(r"^Table\s+\d+\s*\|\s*", "", stripped)
    stripped = stripped.rstrip(".")
    return convert_text(stripped)


def convert_table(lines: list[str], start: int, pending_caption: str | None) -> tuple[str, int]:
    block: list[str] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        block.append(lines[i].strip())
        i += 1
    rows: list[list[str]] = []
    for row in block:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        rows.append(cells)
    if not rows:
        return "", i
    header = rows[0]
    colspec, label, size_cmd = TABLE_SPECS.get(
        header[0],
        (r">{\raggedright\arraybackslash}X" * len(header), "tab:table", r"\scriptsize"),
    )
    caption = pending_caption or "Simulation summary."
    out = [
        r"\begin{table}[!t]",
        r"\centering",
        r"\caption{" + caption + "}",
        r"\label{" + label + "}",
        size_cmd,
        r"\setlength{\tabcolsep}{2.2pt}",
        r"\renewcommand{\arraystretch}{1.12}",
        r"\begin{tabularx}{0.98\textwidth}{" + colspec + "}",
        r"\toprule",
    ]
    for idx, cells in enumerate(rows):
        out.append(" & ".join(convert_text(cell) for cell in cells) + r" \\")
        if idx == 0:
            out.append(r"\midrule")
    out += [r"\bottomrule", r"\end{tabularx}", r"\end{table}", ""]
    return "\n".join(out), i


def convert_body(md: str, keywords: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    pending_table_caption: str | None = None
    before_abstract = True
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith("## Abstract"):
            before_abstract = False
        if before_abstract and (
            stripped.startswith("Article type:")
            or stripped.startswith("Keywords:")
            or stripped.startswith("Authors:")
            or stripped.startswith("Affiliations:")
            or stripped.startswith("Author affiliations:")
            or stripped.startswith("*Corresponding author:")
            or stripped.startswith("- ")
            or re.match(r"^\d+\.\s", stripped)
        ):
            i += 1
            continue
        if stripped.startswith("!["):
            path_match = re.search(r"\(([^)]+)\)", stripped)
            path = path_match.group(1) if path_match else ""
            basename = Path(path).name
            fig_path, label, width = FIGURES.get(basename, (path, "fig:unknown", "0.92"))
            caption_line = ""
            if i + 2 < len(lines) and not lines[i + 1].strip():
                caption_line = lines[i + 2]
                i_skip = 3
            elif i + 1 < len(lines):
                caption_line = lines[i + 1]
                i_skip = 2
            else:
                i_skip = 1
            out += [
                r"\begin{figure}[!t]",
                r"\centering",
                rf"\includegraphics[width={width}\textwidth]{{{fig_path}}}",
                r"\caption{" + clean_caption_text(caption_line) + "}",
                r"\label{" + label + "}",
                r"\end{figure}",
                "",
            ]
            i += i_skip
            continue
        if stripped.startswith("**Table"):
            pending_table_caption = table_caption(stripped)
            i += 1
            continue
        if stripped.startswith("|"):
            table_tex, i = convert_table(lines, i, pending_table_caption)
            pending_table_caption = None
            if table_tex:
                out.append(table_tex)
            continue
        if stripped.startswith("# "):
            i += 1
            continue
        if stripped.startswith("## Abstract"):
            out.append(r"\begin{abstract}")
            i += 1
            continue
        if stripped.startswith("## "):
            title = re.sub(r"^\d+\.\s+", "", stripped[3:])
            if title == "Introduction" and r"\begin{abstract}" in out:
                out += [
                    r"\end{abstract}",
                    "",
                    r"\begin{keyword}",
                    convert_text(keywords),
                    r"\end{keyword}",
                    r"\end{frontmatter}",
                    "",
                ]
            if title != "References":
                out.append(r"\section{" + latex_escape(title) + "}")
            i += 1
            continue
        if stripped.startswith("### "):
            title = re.sub(r"^\d+(?:\.\d+)*\s+", "", stripped[4:])
            out.append(r"\subsection{" + latex_escape(title) + "}")
            i += 1
            continue
        if stripped:
            out.append(convert_text(stripped))
            out.append("")
        else:
            out.append("")
        i += 1
    return "\n".join(out)


def texorpdf(text: str) -> str:
    return r"\texorpdfstring{" + latex_escape(text) + "}{" + text.replace('Li4SiO4', 'Li4SiO4') + "}"


def main() -> None:
    md = MD.read_text(encoding="utf-8")
    title_match = re.match(r"# (.+)", md)
    title = title_match.group(1) if title_match else "Repaired manuscript"
    keyword_match = re.search(r"^Keywords:\s*(.+)$", md, re.MULTILINE)
    keywords = keyword_match.group(1) if keyword_match else "brittle ceramic pebble; bonded-particle DEM"
    body = convert_body(md, keywords)
    tex = rf"""\documentclass[preprint,12pt]{{elsarticle}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{tabularx}}
\usepackage{{amsmath}}
\usepackage{{url}}
\usepackage{{caption}}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{{hyperref}}
\biboptions{{numbers,sort&compress}}
\captionsetup{{font=footnotesize,labelfont=bf,skip=3pt}}
\setlength{{\parindent}}{{1em}}
\setlength{{\parskip}}{{0pt}}
\setlength{{\textfloatsep}}{{8pt plus 2pt minus 2pt}}
\setlength{{\floatsep}}{{7pt plus 2pt minus 2pt}}
\setlength{{\intextsep}}{{7pt plus 2pt minus 2pt}}
\emergencystretch=3em

\journal{{To be determined}}

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
    TEX.write_text(tex, encoding="utf-8")
    print(TEX)


if __name__ == "__main__":
    main()
