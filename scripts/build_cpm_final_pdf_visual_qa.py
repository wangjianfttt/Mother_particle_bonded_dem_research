#!/usr/bin/env python3
"""Render and summarize the final CPM manuscript PDF for submission QA."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "manuscript" / "computational_particle_mechanics_submission.pdf"
UPLOAD_PDF = (
    ROOT
    / "submission_packages"
    / "computational_particle_mechanics_upload_ready"
    / "01_manuscript.pdf"
)
OUT_DIR = ROOT / "docs" / "pdf_visual_qa" / "cpm_final_submission_20260704"
REPORT_MD = ROOT / "docs" / "cpm_final_pdf_visual_qa_20260704.md"
REPORT_JSON = ROOT / "docs" / "cpm_final_pdf_visual_qa_20260704.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def render_pdf() -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("page-*.png"):
        old.unlink()
    prefix = OUT_DIR / "page"
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise SystemExit("pdftoppm not found; install poppler or use the bundled runtime.")
    run([pdftoppm, "-png", "-r", "140", str(PDF), str(prefix)])
    pages = sorted(OUT_DIR.glob("page-*.png"))
    if not pages:
        raise SystemExit("PDF rendering produced no PNG pages")
    for index, page in enumerate(pages, start=1):
        target = OUT_DIR / f"page-{index:02d}.png"
        if page != target:
            page.rename(target)
    return sorted(OUT_DIR.glob("page-*.png"))


def page_metrics(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("L")
    white = Image.new("L", image.size, 255)
    diff = ImageChops.difference(image, white)
    stat = ImageStat.Stat(diff)
    mask = diff.point(lambda pixel: 255 if pixel > 8 else 0)
    bbox = mask.getbbox()
    nonwhite = sum(mask.histogram()[1:])
    total = image.size[0] * image.size[1]
    return {
        "file": str(path.relative_to(ROOT)),
        "width": image.size[0],
        "height": image.size[1],
        "mean_ink_distance": round(stat.mean[0], 4),
        "nonwhite_ratio": round(nonwhite / total, 6),
        "content_bbox": bbox,
        "blank_flag": nonwhite / total < 0.003 or bbox is None,
    }


def make_contact_sheet(pages: list[Path], columns: int = 3) -> Path:
    thumbs = []
    for page in pages:
        img = Image.open(page).convert("RGB")
        img.thumbnail((420, 594))
        canvas = Image.new("RGB", (430, 624), "white")
        canvas.paste(img, ((430 - img.width) // 2, 10))
        thumbs.append(canvas)
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * 430, rows * 624), "white")
    for idx, thumb in enumerate(thumbs):
        x = (idx % columns) * 430
        y = (idx // columns) * 624
        sheet.paste(thumb, (x, y))
    path = OUT_DIR / "contact_sheet.png"
    sheet.save(path)
    return path


def extract_pdf_info() -> dict[str, object]:
    reader = PdfReader(str(PDF))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return {
        "page_count": len(reader.pages),
        "contains_title": "Bonded-template DEM reveals" in text,
        "contains_doi": "10.5281/zenodo.20687351" in text,
        "contains_references_heading": "References" in text,
        "unresolved_reference_tokens": text.count("??"),
    }


def build_payload() -> dict[str, object]:
    pages = render_pdf()
    contact_sheet = make_contact_sheet(pages)
    metrics = [page_metrics(path) for path in pages]
    pdf_info = extract_pdf_info()
    manuscript_sha = sha256(PDF)
    upload_sha = sha256(UPLOAD_PDF)
    blank_pages = [m["file"] for m in metrics if m["blank_flag"]]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "manuscript_pdf": str(PDF.relative_to(ROOT)),
        "upload_pdf": str(UPLOAD_PDF.relative_to(ROOT)),
        "manuscript_pdf_sha256": manuscript_sha,
        "upload_pdf_sha256": upload_sha,
        "manuscript_matches_upload_pdf": manuscript_sha == upload_sha,
        "visual_qa_dir": str(OUT_DIR.relative_to(ROOT)),
        "contact_sheet": str(contact_sheet.relative_to(ROOT)),
        **pdf_info,
        "page_metrics": metrics,
        "blank_page_count": len(blank_pages),
        "blank_pages": blank_pages,
        "status": "PASS"
        if manuscript_sha == upload_sha
        and len(blank_pages) == 0
        and pdf_info["contains_title"]
        and pdf_info["contains_doi"]
        and pdf_info["contains_references_heading"]
        and pdf_info["unresolved_reference_tokens"] == 0
        else "CHECK",
    }


def write_markdown(payload: dict[str, object]) -> None:
    lines = [
        "# CPM Final PDF Visual QA",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        f"- Status: `{payload['status']}`",
        f"- Manuscript PDF: `{payload['manuscript_pdf']}`",
        f"- Upload PDF: `{payload['upload_pdf']}`",
        f"- Manuscript/upload SHA match: `{payload['manuscript_matches_upload_pdf']}`",
        f"- Page count: `{payload['page_count']}`",
        f"- Blank page count: `{payload['blank_page_count']}`",
        f"- Contains title: `{payload['contains_title']}`",
        f"- Contains DOI: `{payload['contains_doi']}`",
        f"- Contains references heading: `{payload['contains_references_heading']}`",
        f"- Unresolved reference token count: `{payload['unresolved_reference_tokens']}`",
        f"- Contact sheet: `{payload['contact_sheet']}`",
        "",
        "## Rendered Pages",
        "",
        "| Page | PNG | Nonwhite ratio | Blank flag |",
        "| ---: | --- | ---: | --- |",
    ]
    metrics = payload["page_metrics"]
    assert isinstance(metrics, list)
    for idx, item in enumerate(metrics, start=1):
        assert isinstance(item, dict)
        lines.append(
            f"| {idx} | `{item['file']}` | {item['nonwhite_ratio']} | `{item['blank_flag']}` |"
        )
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    payload = build_payload()
    REPORT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_markdown(payload)
    print(REPORT_MD)
    print(REPORT_JSON)
    print(payload["contact_sheet"])
    if payload["status"] != "PASS":
        raise SystemExit("CPM final PDF visual QA requires review")


if __name__ == "__main__":
    main()
