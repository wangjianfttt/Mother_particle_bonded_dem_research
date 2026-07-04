# Computational Particle Mechanics submission package QA, 2026-07-04

## Output package

Directory:

- `submission_packages/computational_particle_mechanics_upload_ready`

ZIP:

- `submission_packages/computational_particle_mechanics_upload_ready.zip`
- `submission_packages/computational_particle_mechanics_upload_ready.zip.sha256`

## Included upload files

| Role | File |
|---|---|
| Manuscript | `01_manuscript.pdf` |
| Highlights | `02_highlights.docx` |
| Graphical abstract | `03_graphical_abstract.png`, `03_graphical_abstract.tiff` |
| Editable graphical abstract backup | `03_graphical_abstract.pdf`, `03_graphical_abstract.svg` |
| Declaration of competing interest | `04_declaration_of_competing_interest.docx` |
| Cover letter | `05_cover_letter.docx` |
| Author e-mails and CRediT contributions | `06_author_emails_and_contributions.docx` |
| LaTeX manuscript source | `07_latex_source.zip` |
| Editorial system paste fields | `08_editorial_submission_fields.docx` |
| Main figure files | `09_main_figures.zip` |
| Author e-mail completion sheet | `10_author_email_completion_sheet.docx`, `10_author_email_completion_sheet.csv` |
| Upload guide | `README_upload_roles.txt` |

## Build command

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_computational_particle_mechanics_submission_package.py
```

The system `python3` does not include `python-docx`, so the bundled Python
runtime must be used for this package builder.

## Verification

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 - <<'PY'
from pathlib import Path
import csv
import hashlib
import zipfile
from docx import Document

root = Path("submission_packages")
zip_path = root / "computational_particle_mechanics_upload_ready.zip"
sha_path = Path(str(zip_path) + ".sha256")
with zipfile.ZipFile(zip_path) as zf:
    assert zf.testzip() is None
digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
assert digest == sha_path.read_text().split()[0]
rows = list(csv.DictReader((root / "computational_particle_mechanics_upload_ready" / "MANIFEST.csv").open()))
assert len(rows) == 15
with zipfile.ZipFile(root / "computational_particle_mechanics_upload_ready" / "07_latex_source.zip") as zf:
    assert zf.testzip() is None
with zipfile.ZipFile(root / "computational_particle_mechanics_upload_ready" / "09_main_figures.zip") as zf:
    assert zf.testzip() is None
    assert len(zf.namelist()) == 19
for name in [
    "02_highlights.docx",
    "04_declaration_of_competing_interest.docx",
    "05_cover_letter.docx",
    "06_author_emails_and_contributions.docx",
    "08_editorial_submission_fields.docx",
    "10_author_email_completion_sheet.docx",
]:
    Document(root / "computational_particle_mechanics_upload_ready" / name)
print("PASS")
PY
```

Observed result:

- ZIP integrity: pass.
- ZIP SHA256: pass.
- Manifest: 15 records after adding the LaTeX source zip, editorial
  submission-fields Word file, separate main-figure package and author e-mail
  completion files.
- Word files: all open successfully with `python-docx`.
- `07_latex_source.zip` opens successfully and contains the target-specific
  source file `manuscript/computational_particle_mechanics_submission.tex`.
- `09_main_figures.zip` opens successfully and contains 19 members: a README
  plus PDF, PNG and SVG versions of the six main figures.
- `10_author_email_completion_sheet.csv` contains eight author rows, with seven
  coauthor e-mail fields still marked as missing in current records.
- The five Highlights contain 83, 76, 84, 82 and 73 characters, respectively,
  so they satisfy the common Elsevier 85-character limit.

## Independent LaTeX-source compile check

The source zip was extracted to a temporary directory and compiled from the
extracted `manuscript` directory:

```bash
rm -rf /tmp/cpm_latex_source_check4
mkdir -p /tmp/cpm_latex_source_check4
unzip -q submission_packages/computational_particle_mechanics_upload_ready/07_latex_source.zip -d /tmp/cpm_latex_source_check4
cd /tmp/cpm_latex_source_check4/manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error computational_particle_mechanics_submission.tex
```

Observed result:

- Compile status: pass.
- Output PDF: `computational_particle_mechanics_submission.pdf`.
- PDF pages: 18.
- Final `.log` scan: no unresolved citation warnings, no LaTeX errors, no fatal
  error and no emergency stop.
- The target-specific TeX file uses
  `\journal{Computational Particle Mechanics}`.

## Render and text-hygiene checks

Current target PDF:

- `manuscript/computational_particle_mechanics_submission.pdf`
- PDF pages: 18.
- Rendered-page QA folder:
  `docs/pdf_visual_qa/cpm_submission_20260704_intro_update/`
- Contact sheet:
  `docs/pdf_visual_qa/cpm_submission_20260704_intro_update/contact_sheet.png`
- Rendered page PNG count: 18.

Reader-facing text scan:

```bash
rg -n -i "\b(audit|diagnostic|gate|however|therefore|rather than|not only|not .* but|CAL|SP-00|PB-00|Advanced Powder|Journal of Nuclear Materials|Nuclear Fusion)\b" \
  manuscript/computational_particle_mechanics_submission.tex \
  manuscript/computational_particle_mechanics_cover_letter.md \
  manuscript/computational_particle_mechanics_highlights.md \
  manuscript/computational_particle_mechanics_editorial_fields.md \
  submission_packages/computational_particle_mechanics_upload_ready/README_upload_roles.txt
```

Observed result:

- No matching reader-facing residues were reported for the scanned CPM
  submission files.

## Notes

- This package is target-specific for Computational Particle Mechanics and does
  not overwrite `submission_packages/repaired_editorial_upload_ready`.
- The full reproducibility package remains
  `submission_packages/repaired_submission_package.zip`.
- `08_editorial_submission_fields.docx` is a helper file for copying title,
  abstract, keywords, highlights, declarations and availability statements into
  the live submission system. It is not necessarily an upload category.
- `09_main_figures.zip` is included because Elsevier author instructions ask
  authors to provide figures as separate files along with the manuscript. The
  LaTeX source zip also contains the figure PDFs needed for compilation.
- Computational Particle Mechanics is currently routed through the
  Elsevier/ScienceDirect journal page, so the final upload categories should be
  checked in the live submission system.
- The corresponding author's e-mail is available. Other coauthor e-mail fields
  are still marked as not provided in current records and should be completed if
  the submission system requires all author e-mails.
