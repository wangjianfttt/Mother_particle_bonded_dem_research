# JNM main-manuscript PDF visual QA, 2026-06-12

## Scope

This note records a lightweight visual QA pass for the compiled Journal of Nuclear Materials main manuscript after the Methods wording, PDF-string metadata update, material-degradation mechanism-index polish, event-aligned topology evidence update, main-result figure compaction and final code-availability wording update.

Checked file:

- `manuscript/journal_of_nuclear_materials_submission.pdf`

Rendered QA artifacts:

- `docs/pdf_visual_qa/jnm_main_20260612/page-01.png` through `page-11.png`
- `docs/pdf_visual_qa/jnm_main_20260612/contact_sheet.png`

## Rendering command

The manuscript PDF was rendered with `scripts/render_jnm_pdf_visual_qa.py`,
which calls Ghostscript because `pdftoppm` and Python PDF-rendering packages
were not available in the local environment.

```bash
python3 scripts/render_jnm_pdf_visual_qa.py
```

The script renders the 11 pages and combines them into a contact sheet using
Pillow.

The automated QA gate also checks artifact freshness in both directions:
the manuscript PDF must be newer than the active TeX and Fig. 1-Fig. 6 PDFs, and rendered artifacts must be newer than the checked PDF, so a changed manuscript or a changed figure cannot pass against stale compiled or rendered outputs.

## Visual findings

- The manuscript renders as an 11-page double-column Elsevier-style article.
- Fig. 1 to Fig. 6 appear near the relevant text flow and remain readable at page scale.
- Table 1, Table 2 and Table 3 are placed in the manuscript body and do not appear as image-only substitutes.
- The title page, abstract, keywords, declarations and references are present.
- No obvious figure-caption duplication, text overlap, missing page, blank figure, clipped main panel or misplaced table was observed in the contact-sheet inspection.

## Remaining layout warnings

The current LaTeX log contains no unresolved citations and no fatal compilation errors. The previous `hyperref` PDF-string warnings from the title/frontmatter metadata were removed by generating the title with a plain-text PDF string and disabling author-footnote commands in PDF strings.

Residual warnings are ordinary double-column layout warnings: several underfull boxes, one small 2.22 pt overfull output box and the `fixltx2e` package notice inherited from `dblfloatfix`. These are not treated as scientific or submission blockers by the automated gate.

## Boundary

This QA is a visual manuscript-layout check only. It does not replace the numerical evidence gates, source-data matrix, claim-evidence matrix, public reproducibility-package check, or external repository DOI/stable-URL insertion.
