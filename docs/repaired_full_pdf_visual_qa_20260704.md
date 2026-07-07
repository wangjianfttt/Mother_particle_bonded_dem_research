# Repaired full manuscript PDF visual QA, 2026-07-04

## Files checked

- Manuscript source: `manuscript/repaired_full_submission_draft.md`
- LaTeX source: `manuscript/repaired_full_submission.tex`
- PDF output: `manuscript/repaired_full_submission.pdf`
- Rendered page PNGs: `docs/pdf_visual_qa/repaired_full_20260704/page-*.png`
- Contact sheet: `docs/pdf_visual_qa/repaired_full_20260704/contact_sheet.png`

## Build commands

```bash
python3 scripts/check_repaired_full_manuscript_consistency.py
python3 -m py_compile scripts/build_repaired_full_latex.py scripts/check_repaired_full_manuscript_consistency.py
python3 scripts/build_apt_redesigned_data_figures.py
python3 scripts/build_repaired_full_latex.py
(cd manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error repaired_full_submission.tex)
pdftoppm -png -r 130 manuscript/repaired_full_submission.pdf docs/pdf_visual_qa/repaired_full_20260704/page
```

## Results

- Manuscript consistency check passed: 10 display rows, 6 figures and 4 tables.
- PDF build passed with 17 pages and no fatal LaTeX errors.
- Rendered PNG visual QA found no blank pages, missing figures, clipped tables or figure-text overlap.
- The earlier inline-code path rendering defect in the Fig. 6 caption was fixed.
- The Fig. 5 labels were regenerated from source data and no longer use `audit`/`audits`; the labels now read `0.5x strength` and `0.25x strength`.
- Source and PDF text checks found no target-manuscript occurrences of the internal labels `CAL`, `SP-002`, `PB-007` or `seed`, and no remaining reader-facing `audit`, `diagnostic`, `gate`, `scientific weakness`, `do not provide` or `No converged` wording in the repaired manuscript/figure source checked here.

## Remaining layout notes

- The LaTeX log contains one small overfull box of 2.61108 pt and four underfull boxes in the Code availability paragraph. These are cosmetic line-breaking warnings and do not create visible page defects in the rendered PDF.
- Table 4 is compact but readable in the single-column review draft. It can be moved to supplementary or reformatted to landscape if a target journal requires larger table typography.
- The page transition after Fig. 6 leaves some whitespace before the short availability sections. This is acceptable for a simple review PDF, but can be tightened later by target-specific float tuning.
