# Journal of Nuclear Materials submission-readiness audit (2026-06-12)

This audit records the current evidence boundary for the Journal of Nuclear Materials submission package after the PB-006 force-transmission withdrawal and PB-007 corrected-route rebuild.

Update note (2026-06-13): the latest final gate supersedes the counts below where they are older than the live report. The current live state is `BLOCKED_EXTERNAL` with 84 PASS, 0 WARN, 1 BLOCKED_EXTERNAL and 0 FAIL; the public reproducibility package verifies 125 files after adding the event-topology mechanism audit, Fig. 5 mechanism-figure QA and final-upload manifest checks, and the final gate also verifies the figure-caption companion, frozen repository-deposit packet, root start-here guide, repository copy-paste fields, model-parameter consistency audit and active PB-007 run provenance capsule.

## Current state

Status: internally submit-ready after repository DOI insertion and final author approval, but not yet a completed predictive design study.

Latest manuscript-facing polish: the active Journal of Nuclear Materials draft now removes internal case-code labels from the reader-facing narrative and confines low-level run-file terms and software provenance to appropriate manuscript locations. The article text and generated TeX no longer contain PB-006, PB-007, SP-002 or CAL1 labels; those identifiers remain only in repository filenames, audit documents and reproducibility-package paths where they are needed for traceability. The regenerated manuscript PDF, flat source bundle and main submission package compile or verify without unresolved citations or LaTeX errors.

Automated final-gate status: `scripts/check_jnm_submission_gate.py` writes `docs/jnm_final_submission_gate_report.md` and `.json`. The current gate result is `BLOCKED_EXTERNAL` with 84 PASS, 0 WARN, 1 BLOCKED_EXTERNAL and 0 FAIL: required files, CSV paths, LaTeX logs, package checksums, graphical-abstract dimensions, Highlights length, abstract scope, reference metadata and citation coverage, manuscript figure/table integrity, figure-caption companion integrity, compiled-PDF frontmatter extraction, source-data coverage, claim-evidence boundaries, scientific-storyline consistency, objective-completion/evidence-boundary consistency, title consistency, key numeric and model-parameter consistency, public reduced-package coverage, public reproducibility-package hygiene, Elsevier upload compliance, official JNM scope alignment, repository-deposit staging integrity, frozen repository-deposit packet integrity, root start-here-guide integrity, repository copy-paste-field integrity, final upload manifest integrity, public upload text hygiene, reader-facing terminology hygiene, author metadata, declarations, Editorial Manager paste-field consistency, cover-letter support and reader-facing manuscript labels pass. The reference gate currently verifies 18 active citations against 18 complete BibTeX entries. The upload-compliance gate verifies 5 Highlights, a 3535 x 1421 px graphical abstract, an `elsarticle`/`frontmatter` manuscript source, `elsarticle-num` bibliography style with bundled `.bst`, a clean flat LaTeX source zip, upload-role artifacts, declarations support and DOI-insertion guidance. The repository-deposit staging gate verifies the 11-file staging folder, manifest hashes, public package checksum, required zip members, Zenodo metadata, README instructions, concise Chinese final handoff and expected pre-DOI gate state. The frozen-deposit gate verifies the frozen upload zip checksum, Zenodo metadata JSON syntax and upload instructions; the start-here gate verifies the root upload entry file, frozen path, DOI commands and 84/85 gate counts; the copy-paste-field gate verifies repository metadata fields for author-side deposit. The public reproducibility package gate verifies 125 files, manifest hashes, checksum, representative DEM inputs, objective-completion audit, title-consistency checker, reader-facing terminology checker, event-aligned topology summary, event-topology mechanism audit, Fig. 5 mechanism-figure QA and exclusion of internal submission-support files; the current final gate report is staged beside the public zip rather than embedded inside it to avoid self-referential stale reports. The public-upload text hygiene gate verifies that public-facing manuscript/support text has no machine-local absolute paths, no reader-facing internal case labels and only scoped DOI placeholders. The PDF frontmatter gate verifies that the compiled PDF exposes the title, all 8 authors, both affiliations, Abstract, Keywords and declaration/data-availability text after the `elsarticle` conversion. The only blocker is still external repository DOI/stable URL insertion, but the gate now scans the manuscript, TeX, claim-evidence matrix, reviewer-risk matrix, asset manifest, upload matrix, repository metadata README, final action summary and mainline status for unresolved repository placeholders or `ready_after_repository_identifier_insert` labels.

DOI-insertion rehearsal: a clean temporary-copy test of `python3 scripts/insert_jnm_repository_identifier.py <test-doi-url> --apply --rebuild` completed successfully after gate-script hardening. The current 84-PASS/121-file public-package state still has only the external DOI/stable-URL blocker. The latest local hardening adds model-parameter consistency to the key-numeric gate; after DOI insertion, the expected clean state is 85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL and 0 FAIL. The fake-identifier override remains only for isolated rehearsal; the main workspace still contains no test DOI.

Author-metadata status: `manuscript/journal_of_nuclear_materials_author_metadata.csv` and `manuscript/journal_of_nuclear_materials_author_declaration_checklist.md` now provide a submission-system-ready author order, affiliation mapping, corresponding-author email, CRediT roles, funding confirmation and declaration checklist. `scripts/check_jnm_author_metadata.py` confirms that the CSV author order, corresponding-author email and affiliation mapping match the active manuscript draft.

Current submission draft:

- `manuscript/journal_of_nuclear_materials_submission_draft.md`
- `manuscript/journal_of_nuclear_materials_submission.tex`
- `manuscript/journal_of_nuclear_materials_submission.pdf`
- `submission_packages/journal_of_nuclear_materials_reproducibility_package.zip`
- `figures/main/journal_of_nuclear_materials_graphical_abstract.png`
- `manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv`
- `manuscript/journal_of_nuclear_materials_author_metadata.csv`
- `manuscript/journal_of_nuclear_materials_author_declaration_checklist.md`
- `manuscript/journal_of_nuclear_materials_editorial_manager_upload_checklist.md`
- `manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv`
- `manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md`
- `manuscript/journal_of_nuclear_materials_elsevier_declarations.md`
- `manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json`
- `manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv`
- `manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv`
- `docs/jnm_objective_completion_audit_20260613.md`
- `docs/jnm_repository_deposit_final_handoff_zh.md`
- `docs/jnm_final_submission_gate_report.md`
- `scripts/check_jnm_submission_gate.py`
- `scripts/check_jnm_author_metadata.py`

## Claim-evidence audit

| Manuscript claim | Primary evidence | Status | Required wording boundary |
| --- | --- | --- | --- |
| A 1 mm Li4SiO4 mother pebble can be represented by a 500-subparticle bonded template for event-sequence screening | Fig. 2, Fig. 3, `tables/jnm_single_pebble_resolution_summary.csv`, `tables/jnm_single_pebble_rate_summary.csv` | Supported as a calibration candidate | Do not call it a final Li4SiO4 material law |
| First-break displacement and split morphology are robust over the tested resolution and rate windows | Fig. 3 and matching resolution/rate summary tables | Supported over tested 250-1000 subparticles and 0.03-0.10 m/s | Peak load is still moderately resolution/rate sensitive |
| Corrected bed fracture interpretation requires zero pre-damage, native force connectivity and force-balance gates | Fig. 4, corrected-bed acceptance summaries, `docs/jnm_force_transmission_validation_audit_20260612.md` | Strongly supported as a method requirement | Superseded diagnostic bed-scale claims must remain withdrawn |
| The corrected pilot shows localized upper-bed microcracking | Fig. 5, Table 1, pilot bond/event/native-force tables | Supported for one corrected pilot | Do not generalize to bed-wide fragmentation or probability |
| Independent seed02 and 0.5x/0.25x audits remain intact despite spanning native force graphs | Fig. 6, `tables/pb007_macro_topology_event_metrics.csv`, seed02 processed CSVs | Supported as sensitivity evidence | State as local force-path sensitivity, not as a universal threshold |
| The work is relevant to nuclear materials rather than only granular mechanics | Introduction, Discussion, Fig. 1, breeder-bed citations | Supported if Li4SiO4 degradation, purge paths and blanket integrity remain central | Avoid overclaiming ITER/CFETR design-margin prediction |

## Current strongest manuscript message

The paper is strongest when framed as an acceptance-gated computational materials diagnostic: it shows how intact bonded breeder-pebble templates can be inserted into random beds without seating damage, how invalid load-path cases can be rejected, and how mother-pebble-resolved fracture-event sequences and native force-network changes can be extracted once the corrected gate passes.

## Reviewer risks still present

1. Ensemble size remains small: two corrected 100-mother-pebble beds plus two strength-window audits are not enough for failure-probability statistics.
2. The contact modulus used for the corrected bed route is a gate-passing numerical protocol, not a fully calibrated breeder-material stiffness.
3. The single-pebble weak-plane template is a reduced-order defect representation; experimental elastic calibration and stochastic strength distributions remain future work.
4. The persistent repository DOI or stable URL is still missing from the Data availability statement and several submission-support files; this is expected until the reduced reproducibility package is deposited.
5. A journal-specific final submission check is still required in Editorial Manager for graphical abstract, supplementary-file and source-file item types.

## Submission packaging audit

The public reduced reproducibility package currently contains the manuscript PDF/TEX/Markdown, references, highlights, supplementary file, main figures, source tables, processed corrected-bed event and native-force data, representative DEM inputs, package/audit scripts and post-processing scripts. It excludes cover letters, author declarations, author metadata sheets, Editorial Manager checklists, reviewer-risk prebuttals, resubmission planning notes, very large restart files and full raw local-bond histories; the manuscript correctly states that the large raw archives can be provided as larger audit bundles on request.

Additional upload-support files are now prepared: a flat LaTeX source bundle for Editorial Manager, an Elsevier declarations draft, a Zenodo-style metadata JSON file, an upload asset manifest and an Editorial Manager upload checklist/matrix. These files reduce administrative risk but still require final author-side confirmation before upload.

Reviewer-risk support added: `manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md` and `manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv` now map likely JNM reviewer concerns to manuscript evidence, conservative wording boundaries and remaining author/external actions. This document is for internal preparation, not routine upload.

Source-data coverage support added: `manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv` maps Fig. 1-Fig. 6, Table 1-Table 2 and the graphical abstract to output files, source-data files and generation or audit scripts. `scripts/check_jnm_source_data_matrix.py` verifies that every listed file exists and is non-empty.

Claim-evidence boundary support added: `manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv` maps the nine core manuscript claims to evidence files, claim status, wording boundaries and reviewer-risk links. `scripts/check_jnm_claim_evidence_matrix.py` verifies that every claim has explicit conservative boundaries and existing evidence paths. The DOI insertion helper also updates the matrix after repository deposition so the data-availability boundary cannot remain stale.

Reduced-package coverage support added: `scripts/check_jnm_repro_package_coverage.py` verifies that all non-circular files referenced by the source-data and claim-evidence matrices are present in the public reduced package directory and zip archive. `scripts/check_jnm_public_repro_package.py` additionally verifies the 112-file manifest, checksum, representative DEM inputs, reader-facing terminology checker, fake repository identifier checker, event-aligned topology summary and exclusion of internal submission-support files. `scripts/print_jnm_repository_deposit_packet.py` provides a read-only Chinese/English summary of the exact upload zip, SHA256 and current gate state. `docs/jnm_repository_deposit_final_handoff_zh.md` provides the corresponding-author-facing Chinese handoff with the current upload zip, package SHA256, checksum SHA256 and post-DOI commands; it is staged for repository deposit support but intentionally excluded from the public reproducibility zip to avoid a self-referential package hash.

Elsevier general author guidance relevant to the final upload:

- Highlights should be three to five bullets, with each bullet no more than 85 characters including spaces.
- If LaTeX source files are requested, Elsevier's LaTeX instructions caution that Editorial Manager cannot process figure/source paths in subfolders; a flat upload bundle may be needed even though the local reproducibility package keeps organized folders.
- A declaration of generative AI use must be handled according to Elsevier policy if AI-assisted tools were used in manuscript preparation.

## Recommendation

Submit after the following final administrative steps:

1. Deposit `submission_packages/journal_of_nuclear_materials_reproducibility_package.zip` in Zenodo, Figshare or an institutional repository and insert the DOI/stable URL.
2. Confirm with all authors that the author list, affiliations, CRediT statement and acknowledgements are final.
3. Upload the prepared graphical abstract as a separate file if the Journal of Nuclear Materials submission form requests or allows it.
4. Prepare a flat LaTeX source upload bundle if Editorial Manager requests source files rather than only the compiled PDF.
5. Confirm or edit the generative-AI declaration in `manuscript/journal_of_nuclear_materials_elsevier_declarations.md` before upload.
