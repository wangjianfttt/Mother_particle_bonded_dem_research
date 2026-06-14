Flat LaTeX source bundle for Journal of Nuclear Materials submission.

All .tex, .bbl, .bib and figure files are stored at this single folder level
because Elsevier Editorial Manager may not process subfolder paths in LaTeX uploads.
The Elsevier numeric bibliography style file elsarticle-num.bst is included when available.

Compile locally with:
  latexmk -xelatex -interaction=nonstopmode -halt-on-error journal_of_nuclear_materials_submission.tex

The graphical abstract and reproducibility package are separate upload items, not embedded in this LaTeX source.
