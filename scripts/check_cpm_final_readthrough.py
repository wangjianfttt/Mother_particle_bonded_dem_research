#!/usr/bin/env python3
"""Final read-through checks for the CPM submission package.

This script is intentionally stricter than the package manifest checks. It
guards reader-facing issues that caused repeated revision churn: stale internal
labels, missing display-item references, stale PDF visual QA and unsynchronized
strong-force-tail mechanism numbers.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "manuscript" / "computational_particle_mechanics_submission.tex"
PDF = ROOT / "manuscript" / "computational_particle_mechanics_submission.pdf"
VISUAL_QA_JSON = ROOT / "docs" / "cpm_final_pdf_visual_qa_20260704.json"
UPLOAD_ZIP = ROOT / "submission_packages" / "computational_particle_mechanics_upload_ready.zip"
SUPPORT_ZIP = ROOT / "submission_packages" / "repaired_submission_package.zip"
REPORT_MD = ROOT / "docs" / "cpm_final_readthrough_qa_20260708.md"
REPORT_JSON = ROOT / "docs" / "cpm_final_readthrough_qa_20260708.json"


FORBIDDEN_READER_TERMS = [
    r"\baudit\b",
    r"\bdiagnostic\b",
    r"\bgate\b",
    r"\bhowever\b",
    r"\btherefore\b",
    r"\brather than\b",
    r"\bnot only\b",
    r"\bPB-00[0-9]\b",
    r"\bSP-00[0-9]\b",
    r"\bCAL[0-9]\b",
]

FORBIDDEN_ROUTE_TERMS_IN_SOURCE = [
    "Advanced Powder Technology",
    "Journal of Nuclear Materials",
    "Nuclear Fusion",
]


REQUIRED_TEX_PHRASES = {
    "zero_loss_force_range": "0.113-0.253 N",
    "cracking_force_range": "0.575-1.328 N",
    "f95_range": "0.0382-0.0686 N",
    "f95_ratio": "3.16",
    "f99_ratio": "1.86",
    "f95_caption": "95th-percentile edge force",
    "doi": "10.5281/zenodo.20687351",
}


REQUIRED_UPLOAD_FIGURE_MEMBERS = [
    "figures/main/fig1_workflow.pdf",
    "figures/apt_redesign/fig2_single_pebble_template_validation.pdf",
    "figures/apt_redesign/fig3_entry_state_validation.pdf",
    "figures/apt_redesign/fig4_pilot_fracture_event_sequence.pdf",
    "figures/pb007/pb007_replicate_comparison.pdf",
    "figures/pb007/pb007_material_strength_response.pdf",
]


REQUIRED_SUPPORT_MEMBERS = [
    "repaired_submission_package/scripts/summarize_pb007_strong_force_retention.py",
    "repaired_submission_package/tables/pb007_strong_force_tail_state_metrics.csv",
    "repaired_submission_package/tables/pb007_strong_force_retention.csv",
]


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def add(results: list[CheckResult], name: str, ok: bool, detail: str) -> None:
    results.append(CheckResult(name, "PASS" if ok else "FAIL", detail))


def extract_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        try:
            proc = subprocess.run(
                ["pdftotext", str(path), "-"],
                check=True,
                capture_output=True,
                text=True,
            )
            return proc.stdout
        except Exception as exc:
            raise RuntimeError(f"cannot extract PDF text from {path}: {exc}") from exc


def check_visual_qa(results: list[CheckResult]) -> None:
    data = json.loads(VISUAL_QA_JSON.read_text())
    current_sha = sha256(PDF)
    checks = {
        "status": data.get("status") == "PASS",
        "page_count": isinstance(data.get("page_count"), int) and data.get("page_count") >= 1,
        "blank_page_count": data.get("blank_page_count") == 0 and not data.get("blank_pages"),
        "title_doi_references": all(
            data.get(k)
            for k in ["contains_title", "contains_doi", "contains_references_heading"]
        ),
        "unresolved_refs": data.get("unresolved_reference_tokens") == 0,
        "sha_fresh": data.get("manuscript_pdf_sha256") == current_sha,
        "author_pdf_match": data.get("author_production_matches_manuscript_pdf") is True,
        "blinded_identifiers": data.get("blinded_review_forbidden_hits") == [],
    }
    failed = [name for name, ok in checks.items() if not ok]
    add(
        results,
        "pdf_visual_qa_freshness",
        not failed,
        "all visual-QA checks passed" if not failed else f"failed: {', '.join(failed)}",
    )


def check_reader_terms(results: list[CheckResult], tex: str, pdf_text: str) -> None:
    combined = {
        "tex": tex,
        "pdf": pdf_text,
    }
    hits: list[str] = []
    for source, text in combined.items():
        for pattern in FORBIDDEN_READER_TERMS:
            if re.search(pattern, text, re.IGNORECASE):
                hits.append(f"{source}:{pattern}")
    for phrase in FORBIDDEN_ROUTE_TERMS_IN_SOURCE:
        if phrase in tex:
            hits.append(f"tex:{phrase}")
    add(results, "reader_facing_forbidden_terms", not hits, "no hits" if not hits else "; ".join(hits))


def check_display_references(results: list[CheckResult], tex: str) -> None:
    figure_labels = re.findall(r"\\label\{fig:[^}]+\}", tex)
    table_labels = re.findall(r"\\label\{tab:[^}]+\}", tex)
    fig_hits = {n: re.search(rf"Fig\.\s*{n}\b", tex) is not None for n in range(1, 7)}
    table_hits = {n: re.search(rf"Table\s*{n}\b", tex) is not None for n in range(1, 5)}

    duplicate_labels = []
    for label in figure_labels + table_labels:
        if (figure_labels + table_labels).count(label) > 1 and label not in duplicate_labels:
            duplicate_labels.append(label)

    ok = (
        len(figure_labels) == 6
        and len(table_labels) == 4
        and all(fig_hits.values())
        and all(table_hits.values())
        and not duplicate_labels
    )
    detail = (
        f"fig_labels={len(figure_labels)}, table_labels={len(table_labels)}, "
        f"fig_refs={fig_hits}, table_refs={table_hits}, duplicates={duplicate_labels}"
    )
    add(results, "display_item_references", ok, detail)


def check_required_phrases(results: list[CheckResult], tex: str, pdf_text: str) -> None:
    missing_tex = [name for name, phrase in REQUIRED_TEX_PHRASES.items() if phrase not in tex]
    # PDF extraction can insert line breaks; check only robust compact tokens there.
    compact_pdf = re.sub(r"\s+", " ", pdf_text)
    robust_pdf_phrases = {
        "f95_ratio": "3.16",
        "f99_ratio": "1.86",
        "doi": "10.5281/zenodo.20687351",
    }
    missing_pdf = [name for name, phrase in robust_pdf_phrases.items() if phrase not in compact_pdf]
    add(
        results,
        "strong_force_tail_numbers",
        not missing_tex and not missing_pdf,
        f"missing_tex={missing_tex}, missing_pdf={missing_pdf}",
    )


def check_nested_packages(results: list[CheckResult]) -> None:
    with zipfile.ZipFile(UPLOAD_ZIP) as outer:
        figure_zip_names = [name for name in outer.namelist() if name.endswith("09_main_figures.zip")]
        if not figure_zip_names:
            add(results, "upload_nested_figures", False, "09_main_figures.zip missing")
        else:
            with zipfile.ZipFile(io.BytesIO(outer.read(figure_zip_names[0]))) as inner:
                inner_names = set(inner.namelist())
            missing = [name for name in REQUIRED_UPLOAD_FIGURE_MEMBERS if name not in inner_names]
            add(
                results,
                "upload_nested_figures",
                not missing,
                "all required figure PDFs present" if not missing else f"missing={missing}",
            )

    with zipfile.ZipFile(SUPPORT_ZIP) as support:
        support_names = set(support.namelist())
    missing_support = [name for name in REQUIRED_SUPPORT_MEMBERS if name not in support_names]
    add(
        results,
        "support_package_force_tail_sources",
        not missing_support,
        "force-tail sources present" if not missing_support else f"missing={missing_support}",
    )


def check_large_raw_residue(results: list[CheckResult]) -> None:
    case_root = ROOT / "simulations" / "pebble_bed" / "PB-007" / "cases"
    patterns = {".local", ".dump", ".restart", ".vtk"}
    large = []
    if case_root.exists():
        for path in case_root.rglob("*"):
            if path.is_symlink():
                continue
            if path.is_file() and path.suffix in patterns and path.stat().st_size > 20 * 1024 * 1024:
                large.append(str(path.relative_to(ROOT)))
    add(
        results,
        "large_local_raw_residue",
        not large,
        "no local raw-like files above 20 MiB" if not large else "; ".join(large[:20]),
    )


def write_reports(results: list[CheckResult]) -> None:
    status = "PASS" if all(r.status == "PASS" for r in results) else "FAIL"
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "results": [r.__dict__ for r in results],
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# CPM Final Readthrough QA",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"Status: `{status}`",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for r in results:
        detail = r.detail.replace("|", "\\|")
        lines.append(f"| {r.name} | `{r.status}` | {detail} |")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    results: list[CheckResult] = []
    tex = TEX.read_text(encoding="utf-8")
    pdf_text = extract_pdf_text(PDF)

    check_visual_qa(results)
    check_reader_terms(results, tex, pdf_text)
    check_display_references(results, tex)
    check_required_phrases(results, tex, pdf_text)
    check_nested_packages(results)
    check_large_raw_residue(results)
    write_reports(results)

    for result in results:
        print(f"{result.status} {result.name}: {result.detail}")
    status = all(r.status == "PASS" for r in results)
    print(REPORT_MD)
    return 0 if status else 1


if __name__ == "__main__":
    sys.exit(main())
