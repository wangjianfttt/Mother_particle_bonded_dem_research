# Nuclear Fusion targeting plan

## Decision

Target Nuclear Fusion as a computational fusion-blanket mechanics paper, not as a generic DEM-method paper. The manuscript should emphasize why mother-pebble-resolved fracture sequences matter for ceramic breeder blanket design: local pebble crushing can reorganize the load-bearing skeleton, alter pore pathways, and affect the interpretation of macroscopic bed-compression tests.

## Official requirements checked

- Journal: Nuclear Fusion, IOP Publishing.
- Article type: Paper.
- Expected scope: original research relevant to controlled thermonuclear fusion and fusion technology.
- Abstract target: keep within the normal IOP limit of about 300 words.
- Initial submission: figures and tables may be embedded in the manuscript PDF.
- Figure formats: PDF/EPS preferred for line/vector art; TIFF/PNG/JPG acceptable for raster files.
- Data/supplementary material: provide source data and enough simulation/post-processing information for reproducibility.

Sources checked on 2026-05-31:

- `https://publishingsupport.iopscience.iop.org/journals/nuclear-fusion/`
- `https://publishingsupport.iopscience.iop.org/author-guidelines/`
- `https://publishingsupport.iopscience.iop.org/questions/figures-and-tables/`

## Fit to Nuclear Fusion

| Requirement | Current manuscript fit | Action |
| --- | --- | --- |
| Fusion relevance | Strong if framed around ceramic breeder blanket integrity, purge-gas pathways and design interpretation. | Keep fusion-blanket motivation in the title, abstract and first Introduction paragraph. |
| Original contribution | Locked bonded-template insertion and mother-pebble-resolved event sequencing are clear technical contributions. | Avoid presenting the paper as only a LIGGGHTS implementation note. |
| Validation | SP-002-CAL1 matches a provisional crush-load and split-fragment target, but is not a final material law. | Keep all calibration language conservative. |
| Statistical confidence | Three 500-pebble seeds and three 1000-pebble event-sequence cases support onset and propagation claims. | Do not claim converged bed-scale probability distributions. |
| Mechanism | Packing descriptors and overlap-derived proxies support load-path broadening. | Say "consistent with"; do not claim native force-chain measurement. |
| Reproducibility | Scripts, processed tables, figures and archived case folders exist locally. | Prepare a reduced data package before submission. |

## Recommended Nuclear Fusion story

One-sentence argument:

In Li4SiO4 breeder beds for fusion blankets, a locked bonded-template DEM workflow allows 500-subparticle mother pebbles to be inserted into random packings without deposition-induced damage and reveals a robust top-layer fracture trigger with packing- and orientation-sensitive post-onset propagation.

Result order:

1. Fusion-blanket problem and locked-template workflow.
2. Single-pebble calibration candidate and its limits.
3. Zero precompression bond-loss insertion in 500- and 1000-pebble beds.
4. Three 500-pebble random-bed event sequences.
5. Packing and overlap-proxy diagnostics for seed-dependent cascades.
6. 1000-pebble restartable event sequences and orientation/packing sensitivity.

## Main manuscript files

- Nuclear Fusion draft: `manuscript/nuclear_fusion_submission_draft.md`
- General submission draft: `manuscript/submission_draft_v1.md`
- Captions: `manuscript/figure_captions.md`
- References: `manuscript/references.bib`
- Reference audit: `tables/reference_crossref_audit_20260531.csv`
- Readiness checklist: `manuscript/submission_readiness_checklist.md`
- Submission asset manifest: `manuscript/nuclear_fusion_submission_asset_manifest.csv`
- Data/code package plan: `manuscript/nuclear_fusion_data_code_package_plan.md`
- Final upload checklist: `manuscript/nuclear_fusion_final_upload_checklist.md`
- Author information template: `manuscript/nuclear_fusion_author_info_template.md`
- Submission cover sheet: `manuscript/nuclear_fusion_submission_cover_sheet.md`
- Reviewer-risk prebuttal: `manuscript/nuclear_fusion_reviewer_response_prebuttal.md`

## Remaining before actual upload

1. Convert the Markdown manuscript to IOP-compatible LaTeX or Word.
2. Replace local absolute image links with embedded figures in the compiled PDF.
3. Add author names, affiliations, ORCID ids, acknowledgements and funding.
4. Prepare a reduced data/reproducibility package and write final Data Availability wording.
5. Decide whether to submit now as a method/event-sequence paper or first run one additional independent 1000-pebble packing for stronger statistical breadth.

## Progress after Nuclear Fusion targeting

- Created `manuscript/nuclear_fusion_submission_draft.md` with a Nuclear Fusion-specific title, keywords and stronger fusion-blanket opening paragraph.
- Created `manuscript/nuclear_fusion_cover_letter_draft.md`.
- Created `manuscript/nuclear_fusion_submission_asset_manifest.csv` to map each figure to preferred PDF, backup TIFF and source data.
- Created `manuscript/nuclear_fusion_data_code_package_plan.md` to define the reduced reproducibility package, included scripts, simulation inputs and draft availability statements.
- Created `manuscript/nuclear_fusion_final_upload_checklist.md` to separate ready files from author-provided information still needed before IOP upload.
- Created `manuscript/nuclear_fusion_author_info_template.md` and `manuscript/nuclear_fusion_submission_cover_sheet.md` for final author-side metadata and upload-system fields.
- Created `manuscript/nuclear_fusion_reviewer_response_prebuttal.md` to anticipate likely Nuclear Fusion reviewer objections and response strategies.
- Updated the automated continuation task so future heartbeats prioritize Nuclear Fusion formatting and submission packaging rather than generic exploratory work.
