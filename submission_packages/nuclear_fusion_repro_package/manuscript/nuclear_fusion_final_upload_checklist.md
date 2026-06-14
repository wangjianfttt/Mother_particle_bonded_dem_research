# Nuclear Fusion final upload checklist

This checklist separates items already prepared by the project from items that require author-provided information before actual IOP submission.

## Ready files

| Item | Path | Status |
| --- | --- | --- |
| Working LaTeX manuscript | `manuscript/nuclear_fusion_iop_submission.tex` | Compiles with XeLaTeX. |
| Working manuscript PDF | `manuscript/nuclear_fusion_iop_submission.pdf` | Built successfully; 12 pages in the current local draft. |
| Markdown source draft | `manuscript/nuclear_fusion_submission_draft.md` | Current Nuclear Fusion-oriented text. |
| Cover letter draft | `manuscript/nuclear_fusion_cover_letter_draft.md` | Scientifically complete, but author details remain placeholders. |
| Figure/source-data manifest | `manuscript/nuclear_fusion_submission_asset_manifest.csv` | Complete for current 6 main figures plus Extended Data Fig. 1. |
| Reduced reproducibility package | `submission_packages/nuclear_fusion_repro_package` | Built with `MANIFEST.csv`; excludes large raw restart/local-dump histories, partial checkpoints and TIFF backups. |
| Zipped reproducibility package | `submission_packages/nuclear_fusion_repro_package.zip` | Built for upload/staging; checksum stored in `submission_packages/nuclear_fusion_repro_package.zip.sha256`. |
| Data/code package plan | `manuscript/nuclear_fusion_data_code_package_plan.md` | Defines upload scope and draft availability text. |
| Reference audit | `tables/reference_crossref_audit_20260531.csv` | DOI/title/year metadata checked against Crossref. |
| Author information template | `manuscript/nuclear_fusion_author_info_template.md` | Ready for author-provided names, affiliations, funding and ORCID ids. |
| Submission cover sheet | `manuscript/nuclear_fusion_submission_cover_sheet.md` | Ready for upload-system fields and suggested reviewers. |
| Integrity audit | `manuscript/nuclear_fusion_submission_integrity_audit_20260601.md` | Confirms LaTeX build, package presence and zip checksum. |

## Author information still needed

| Required item | Needed input |
| --- | --- |
| Author list | Filled from author note; confirm spelling before upload. |
| Affiliations | Filled for Anhui University of Science and Technology and Institute of Plasma Physics, Chinese Academy of Sciences; confirm Qi-Gang Wu affiliation before upload. |
| Corresponding author | Jian Wang, wjfttt@mail.ustc.edu.cn; ORCID still optional if available. |
| ORCID ids | Optional but recommended by IOP. |
| Funding | Filled from author-provided funding text. |
| Acknowledgements | Filled from author-provided funding text. |
| Conflict of interest statement | Filled as "The authors declare no competing interests." |
| Data repository DOI or stable URL | Needed once the reduced package is deposited; insert it in the Data Availability statement, cover letter and submission system. |

## Technical checks already passed

- The Nuclear Fusion working draft compiles to PDF using local XeLaTeX.
- The latest LaTeX check found no undefined citations and no LaTeX errors.
- Figure files used by the manuscript are found and embedded from PDF sources.
- The reduced reproducibility package has been rebuilt after adding the LaTeX/PDF draft and package-builder scripts.
- `MANIFEST.csv` now includes SHA-256 checksums for package files.
- A zipped package and separate SHA-256 checksum file have been generated for upload/staging.
- The reproducibility package zip checksum has been verified with `shasum -a 256 -c`.
- The reduced package has been cleaned to exclude partial checkpoint tables and TIFF backups; after adding the 0.03 m/s single-pebble onset check and rebuilding, the package contains 107 collected payload files plus `MANIFEST.csv`.
- A true x-normal 0.03 m/s short endpoint check has been added to the single-pebble calibration evidence and reproducibility package.
- The manuscript Data Availability and Code Availability sections now refer to the assembled reduced reproducibility package and explicitly require only the final repository DOI or stable URL before upload.

## Known cosmetic issues

- The current PDF is a working submission draft, not the final IOP production template.
- The event-summary table is wide and is currently resized to page width.
- The software bibliography entry has no DOI and is represented as a software/source entry with URL and local commit note.
- Two long monospace paths/commit strings can create minor overfull boxes; these do not block compilation but can be polished after author information is inserted.

## Recommended upload order

1. Confirm ORCID ids, if any, and Qi-Gang Wu's affiliation.
2. Deposit or stage the reduced reproducibility package and update Data Availability with the DOI or repository URL.
3. Recompile `manuscript/nuclear_fusion_iop_submission.tex`.
4. Upload the manuscript PDF, source `.tex`, `references.bib`, main figure PDFs/TIFFs and reduced data package according to IOP submission prompts.
5. Keep raw restart and full local-bond dump archives offline but accessible for reviewer request.
