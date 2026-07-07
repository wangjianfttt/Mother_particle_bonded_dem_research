# START HERE - Computational Particle Mechanics submission

Use this file as the handoff point for the current retargeted submission.

## Target

- Journal: Computational Particle Mechanics
- Manuscript title: Bonded-template DEM reveals strength- and
  topology-dependent fracture-event sequences in packed brittle ceramic pebbles
- Article type to select: Research article, or the closest equivalent offered
  by the live Elsevier/ScienceDirect submission system
- Citable data/code archive: https://doi.org/10.5281/zenodo.20687351
- GitHub repository: `wangjianfttt/Mother_particle_bonded_dem_research`

## Upload-ready package

Use:

- `submission_packages/computational_particle_mechanics_upload_ready.zip`

Route note:

- The Springer journal page states that submissions closed there on 1 July
  2025 and points authors to the Elsevier journal site.
- The current ScienceDirect Guide for Authors supports double-anonymized
  review, and the package is prepared for that path.
- Use the blinded manuscript as the review manuscript. Keep the author-bearing PDF/Word backup for title-page, source-file, production or explicit live-system requests.

Checksum:

- `submission_packages/computational_particle_mechanics_upload_ready.zip.sha256`

This zip contains:

- `00_title_page_author_details.docx` - title page and author metadata
- `01_review_manuscript_blinded.pdf` - blinded review manuscript PDF
- `01_review_manuscript_blinded.tex` - blinded review manuscript source
- `02_highlights.docx` - Highlights
- `03_graphical_abstract.png` / `.tiff` - graphical abstract
- `03_graphical_abstract.pdf` / `.svg` - editable graphical abstract backups
- `04_declaration_of_competing_interest.docx`
- `05_cover_letter.docx`
- `06_author_emails_and_contributions.docx`
- `07_latex_source.zip`
- `08_editorial_submission_fields.docx`
- `09_main_figures.zip`
- `10_author_email_completion_sheet.docx` / `.csv`
- `11_full_author_manuscript_for_production.pdf` - full author manuscript for
  title-page or production-source roles only
- `12_full_author_manuscript_single_column.docx` - single-column Word
  manuscript backup for source-file requests only
- `README_upload_roles.txt`

Double-anonymized review manuscript package:

- `submission_packages/computational_particle_mechanics_blinded_review_package.zip`
- `submission_packages/computational_particle_mechanics_blinded_review_package.zip.sha256`

Use the blinded manuscript as the review manuscript for the Elsevier /
ScienceDirect double-anonymized review route. Use the full author-bearing
manuscript, single-column Word backup and author-details files for title-page,
metadata, source-file or production roles.
A legacy compatibility copy remains available as
`submission_packages/computational_particle_mechanics_blinded_review_optional.zip`.

## Current external item

The corresponding author e-mail is available:

- Jian Wang: `wjfttt@mail.ustc.edu.cn`

Seven coauthor e-mail addresses are not in the current local records. Use
`10_author_email_completion_sheet.docx` or `.csv` to collect them if the live
submission system requires every author's e-mail address.

Four public candidate e-mail records have been collected for confirmation, but
they have not been promoted into the formal author metadata. These candidates
are confirmation aids only; do not enter them into the live submission system
until the corresponding author or coauthor confirms the address:

- `docs/cpm_author_email_public_lookup_20260704.md`
- `docs/cpm_author_email_public_lookup_20260704.csv`
- `docs/cpm_goal_completion_audit_20260704.md`
- `docs/cpm_goal_completion_audit_20260704.csv`
- `docs/cpm_goal_completion_audit_20260704.json`

Support files for this step:

- `manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.docx`
- `manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.txt`
- `manuscript/computational_particle_mechanics_author_email_collection_packet.docx`
- `manuscript/computational_particle_mechanics_author_email_collection_packet.csv`
- `manuscript/computational_particle_mechanics_author_email_collection_packet.md`
- `manuscript/computational_particle_mechanics_author_email_collection_packet.txt`
- `manuscript/computational_particle_mechanics_individual_contact_messages.docx`
- `manuscript/computational_particle_mechanics_individual_contact_messages.csv`
- `manuscript/computational_particle_mechanics_individual_contact_messages.md`
- `manuscript/computational_particle_mechanics_individual_contact_messages.txt`
- `manuscript/computational_particle_mechanics_live_submission_checklist.docx`
- `manuscript/computational_particle_mechanics_live_submission_checklist.md`
- `manuscript/computational_particle_mechanics_live_submission_packet.docx`
- `docs/cpm_live_submission_action_sheet_20260704.md`
- `docs/cpm_live_submission_action_sheet_20260704.csv`
- `docs/cpm_live_submission_action_sheet_20260704.json`
- `docs/cpm_live_submission_packet_20260704.md`
- `docs/cpm_live_submission_packet_20260704.csv`
- `docs/cpm_live_submission_packet_20260704.json`
- `docs/cpm_live_submission_packet_docx_qa_20260704.md`
- `docs/cpm_author_email_public_lookup_20260704.md`
- `docs/cpm_author_email_public_lookup_20260704.csv`

## Pre-submission check

Run:

```bash
<user-home>/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_computational_particle_mechanics_submission_package.py
```

Expected result:

```text
PASS CPM scientific alignment: manuscript, cover letter, fields and gap map match
PASS CPM reviewer-risk preflight: 7 risks mapped to current evidence and boundaries
PASS CPM submission package: manifest=19, figures=19, docx=11, DOI, guide alignment, live packet and double-anonymous blinded review manuscript verified
```

Current machine-readable readiness report:

- `docs/cpm_submission_readiness_report_20260704.md`
- `docs/cpm_submission_readiness_report_20260704.json`
- `docs/cpm_final_pdf_visual_qa_20260704.md`
- `docs/cpm_final_pdf_visual_qa_20260704.json`

Latest local status recorded in the readiness report:

- Local package ready: `True`
- Reduced reproducibility package CPM support members: `47/47` present
- Missing reduced-package CPM support members: `0`
- Current final PDF visual QA: `PASS`, 19 pages, 0 blank pages, author-production PDF SHA match, blinded review PDF checked
- Single-column Word manuscript backup: `12_full_author_manuscript_single_column.docx`
- External metadata still pending: seven coauthor e-mail addresses if the live
  submission system requires all author e-mails

Current literature-gap and novelty support:

- `docs/cpm_literature_gap_map_20260704.md`
- `docs/cpm_literature_gap_map_20260704.csv`
- `docs/cpm_official_submission_guide_alignment_20260704.md`
- `docs/cpm_official_submission_guide_alignment_20260704.csv`
- `docs/cpm_material_response_summary_20260704.md`
- `docs/cpm_material_response_summary_20260704.csv`
- `docs/cpm_reviewer_risk_preflight_20260704.md`
- `docs/cpm_reviewer_risk_preflight_20260704.csv`

Regenerate it with:

```bash
<user-home>/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_cpm_submission_readiness_report.py
```

The reduced reproducibility package remains:

- `submission_packages/repaired_submission_package.zip`
- `submission_packages/repaired_submission_package.zip.sha256`

It contains the current official-guide alignment, literature-gap map,
material-response summary, reviewer-risk matrix, live-submission packet and the
scripts used to regenerate/check those support files. The live readiness report
itself is kept outside the zip because it records the current package checksum.

The large raw restart files and full local-bond dump histories are archived
outside the GitHub repository and are not needed for initial manuscript review.
