# JNM Editorial Manager upload-ready folder

This folder contains the minimal local files that the corresponding author is likely to upload or paste into Elsevier Editorial Manager.
It deliberately excludes internal reviewer-risk prebuttal files, claim-evidence matrices and raw simulation archives.

Important: before final submission, deposit the reduced reproducibility package in a persistent repository and run:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

After that command, rebuild this folder and use the refreshed files below.

## File roles

| Role | File | Source |
| --- | --- | --- |
| 01_manuscript_pdf | `01_manuscript_pdf.pdf` | `manuscript/journal_of_nuclear_materials_submission.pdf` |
| 02_flat_latex_source | `02_flat_latex_source.zip` | `submission_packages/journal_of_nuclear_materials_flat_source.zip` |
| 02_flat_latex_source_sha256 | `02_flat_latex_source_sha256.zip.sha256` | `submission_packages/journal_of_nuclear_materials_flat_source.zip.sha256` |
| 03_highlights | `03_highlights.md` | `manuscript/journal_of_nuclear_materials_highlights.md` |
| 04_cover_letter | `04_cover_letter.md` | `manuscript/journal_of_nuclear_materials_cover_letter_draft.md` |
| 04_cover_letter_docx | `04_cover_letter_docx.docx` | `manuscript/journal_of_nuclear_materials_cover_letter.docx` |
| 05_graphical_abstract_png | `05_graphical_abstract_png.png` | `figures/main/journal_of_nuclear_materials_graphical_abstract.png` |
| 05_graphical_abstract_tiff | `05_graphical_abstract_tiff.tiff` | `figures/main/journal_of_nuclear_materials_graphical_abstract.tiff` |
| 06_supplementary_pdf | `06_supplementary_pdf.pdf` | `manuscript/journal_of_nuclear_materials_supplementary.pdf` |
| 07_declarations | `07_declarations.md` | `manuscript/journal_of_nuclear_materials_elsevier_declarations.md` |
| 07_declarations_docx | `07_declarations_docx.docx` | `manuscript/journal_of_nuclear_materials_elsevier_declarations.docx` |
| 08_paste_ready_fields | `08_paste_ready_fields.md` | `manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md` |
| 09_author_metadata | `09_author_metadata.csv` | `manuscript/journal_of_nuclear_materials_author_metadata.csv` |
| 10_author_final_upload_readme_zh | `10_author_final_upload_readme_zh.md` | `docs/jnm_author_final_upload_readme_zh.md` |
| 11_coauthor_final_approval_packet | `11_coauthor_final_approval_packet.md` | `docs/jnm_coauthor_final_approval_packet.md` |
| 12_final_submission_action_summary | `12_final_submission_action_summary.md` | `docs/jnm_final_submission_action_summary.md` |

Do not upload `reviewer_risk_prebuttal`, `claim_evidence_boundary_matrix` or large raw restart/local-bond dump files unless the editor explicitly requests them.
