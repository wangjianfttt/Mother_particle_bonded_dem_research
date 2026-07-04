# CPM official submission-guide alignment

Date: 2026-07-04

Official sources checked:

- ScienceDirect Guide for Authors: https://www.sciencedirect.com/journal/computational-particle-mechanics/publish/guide-for-authors
- Springer transition notice for this journal: https://link.springer.com/journal/40571/submission-guidelines

Purpose: map current upload files and support files to the live journal requirements before final submission.

| Guide item | Official source | Current package evidence | Status | Remaining action |
| --- | --- | --- | --- | --- |
| Current submission route | ScienceDirect Guide for Authors; Springer submission-guidelines transition notice | `submission_packages/computational_particle_mechanics_upload_ready.zip; START_HERE_CPM_SUBMISSION.md` | `ready` | Use the live ScienceDirect/Editorial Manager route, not the closed Springer portal. |
| Article scope | ScienceDirect Guide for Authors: journal covers computational particle mechanics, DEM, modelling and fracture/fragmentation of particulate systems. | `manuscript/computational_particle_mechanics_submission.tex; docs/cpm_literature_gap_map_20260704.md` | `ready` | Select Research article or closest available article type in the live system. |
| Double-anonymized review | ScienceDirect Guide for Authors: journal operates a double anonymized review process. | `submission_packages/computational_particle_mechanics_blinded_review_optional.zip` | `ready_if_requested` | Use the optional blinded package if the live system requests a blinded manuscript file. |
| Abstract length | ScienceDirect Guide for Authors: abstract must be concise, factual and not exceed 250 words. | `manuscript/computational_particle_mechanics_submission.tex` | `ready` | Current manuscript abstract is checked by the package script and remains within 250 words. |
| Title-page author details | ScienceDirect Guide for Authors: title page should include author names, affiliations, corresponding author and e-mail details where available. | `submission_packages/computational_particle_mechanics_upload_ready/10_author_email_completion_sheet.csv; manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.docx` | `external_metadata_pending` | Confirm seven coauthor e-mails or leave only confirmed e-mail information if the live system does not require all author e-mails. |
| Editable manuscript source | ScienceDirect Guide for Authors: submit editable source files where requested. | `submission_packages/computational_particle_mechanics_upload_ready/07_latex_source.zip` | `ready` | Upload LaTeX source zip if the system asks for source files at initial submission. |
| Highlights | Prepared as Elsevier-system support material; upload only if the live submission workflow requests highlights. | `submission_packages/computational_particle_mechanics_upload_ready/02_highlights.docx` | `ready_if_requested` | Upload the DOCX or paste the five highlights only if the live system asks for them. |
| Graphical abstract and artwork | ScienceDirect Guide for Authors: artwork files should be supplied separately; generative-AI artwork is not permitted. Graphical abstract is prepared only as live-system support material. | `submission_packages/computational_particle_mechanics_upload_ready/03_graphical_abstract.*; scripts/plot_apt_graphical_abstract.py` | `ready_if_requested` | Use the script-generated graphical abstract only if requested; do not upload generative-AI artwork. |
| Declaration of competing interest | ScienceDirect Guide for Authors: declaration files/statements are required. | `submission_packages/computational_particle_mechanics_upload_ready/04_declaration_of_competing_interest.docx` | `ready` | Upload the declaration DOCX. |
| Figure files | ScienceDirect Guide for Authors: figure files should be uploaded separately at suitable quality. | `submission_packages/computational_particle_mechanics_upload_ready/09_main_figures.zip` | `ready` | Upload 09_main_figures.zip or individual figure files if the live system separates figure upload. |
| Tables and source data | ScienceDirect Guide for Authors: tables should be editable and data availability should be stated. | `manuscript/computational_particle_mechanics_submission.tex; submission_packages/repaired_submission_package.zip` | `ready` | Use the manuscript tables and reduced reproducibility package for editable/source-backed evidence. |
| Data and code availability | ScienceDirect Guide for Authors: data/code availability statements and repository links should be supplied where applicable. | `manuscript/computational_particle_mechanics_submission.tex; DOI 10.5281/zenodo.20687351; GitHub repository` | `ready` | Paste the DOI-backed data and code statements from editorial fields. |
| Author metadata | Live submission system author-entry forms. | `submission_packages/computational_particle_mechanics_upload_ready/10_author_email_completion_sheet.csv` | `external_metadata_pending` | Fill seven coauthor e-mail addresses if the live system requires every author e-mail. |
| Final generated PDF review | Live submission system preview step. | `manuscript/computational_particle_mechanics_live_submission_checklist.md` | `external_submission_step` | Preview the system-generated PDF before clicking final submit. |

## Summary

- Local upload and reproducibility files are ready for live-system entry.
- An optional blinded-review package is available for the double-anonymized review workflow if requested by the live system.
- Highlights and graphical-abstract files are prepared as optional live-system support, not treated as confirmed compulsory CPM guide items.
- The remaining non-local items are seven coauthor e-mail addresses, live article-type/category confirmation and system-generated PDF preview.
