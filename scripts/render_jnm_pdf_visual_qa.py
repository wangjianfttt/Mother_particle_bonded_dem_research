#!/usr/bin/env python3
"""Render the JNM main PDF into page PNGs and a contact sheet."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "manuscript/journal_of_nuclear_materials_submission.pdf"
QA_DIR = ROOT / "docs/pdf_visual_qa/jnm_main_20260612"
CONTACT_SHEET = QA_DIR / "contact_sheet.png"


def render_pages() -> list[Path]:
    if not PDF.exists():
        raise FileNotFoundError(PDF)
    gs = shutil.which("gs")
    if not gs:
        raise RuntimeError("Ghostscript executable 'gs' is required to render PDF QA pages")
    QA_DIR.mkdir(parents=True, exist_ok=True)
    for path in QA_DIR.glob("page-*.png"):
        path.unlink()
    if CONTACT_SHEET.exists():
        CONTACT_SHEET.unlink()
    subprocess.run(
        [
            gs,
            "-q",
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            "-sDEVICE=png16m",
            "-r110",
            "-dTextAlphaBits=4",
            "-dGraphicsAlphaBits=4",
            f"-sOutputFile={QA_DIR / 'page-%02d.png'}",
            str(PDF),
        ],
        cwd=ROOT,
        check=True,
    )
    pages = sorted(QA_DIR.glob("page-*.png"))
    if not pages:
        raise RuntimeError("Ghostscript produced no page PNGs")
    return pages


def build_contact_sheet(pages: list[Path]) -> None:
    images = [Image.open(path).convert("RGB") for path in pages]
    thumb_width = 360
    margin = 24
    label_height = 26
    columns = 2
    thumbs: list[Image.Image] = []
    for idx, image in enumerate(images, start=1):
        scale = thumb_width / image.width
        thumb_height = int(image.height * scale)
        thumb = image.resize((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (thumb_width, thumb_height + label_height), "white")
        canvas.paste(thumb, (0, label_height))
        draw = ImageDraw.Draw(canvas)
        draw.text((6, 5), f"Page {idx}", fill=(20, 20, 20))
        thumbs.append(canvas)

    rows = (len(thumbs) + columns - 1) // columns
    cell_width = thumb_width + margin
    cell_height = max(thumb.height for thumb in thumbs) + margin
    sheet = Image.new(
        "RGB",
        (columns * cell_width + margin, rows * cell_height + margin),
        (245, 245, 245),
    )
    for idx, thumb in enumerate(thumbs):
        x = margin + (idx % columns) * cell_width
        y = margin + (idx // columns) * cell_height
        sheet.paste(thumb, (x, y))
    sheet.save(CONTACT_SHEET)


def main() -> int:
    pages = render_pages()
    build_contact_sheet(pages)
    print(CONTACT_SHEET.relative_to(ROOT))
    print(f"{len(pages)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
