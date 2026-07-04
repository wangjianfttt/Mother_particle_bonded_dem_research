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

Checksum:

- `submission_packages/computational_particle_mechanics_upload_ready.zip.sha256`

This zip contains:

- `01_manuscript.pdf` - manuscript PDF
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
- `README_upload_roles.txt`

## Current external item

The corresponding author e-mail is available:

- Jian Wang: `wjfttt@mail.ustc.edu.cn`

Seven coauthor e-mail addresses are not in the current local records. Use
`10_author_email_completion_sheet.docx` or `.csv` to collect them if the live
submission system requires every author's e-mail address.

Support files for this step:

- `manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.docx`
- `manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.txt`
- `manuscript/computational_particle_mechanics_live_submission_checklist.docx`
- `manuscript/computational_particle_mechanics_live_submission_checklist.md`

## Pre-submission check

Run:

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_computational_particle_mechanics_submission_package.py
```

Expected result:

```text
PASS CPM submission package: manifest=15, figures=19, docx=8, DOI and support docs verified
```

Current machine-readable readiness report:

- `docs/cpm_submission_readiness_report_20260704.md`
- `docs/cpm_submission_readiness_report_20260704.json`

Regenerate it with:

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_cpm_submission_readiness_report.py
```

The reduced reproducibility package remains:

- `submission_packages/repaired_submission_package.zip`
- `submission_packages/repaired_submission_package.zip.sha256`

The large raw restart files and full local-bond dump histories are archived
outside the GitHub repository and are not needed for initial manuscript review.
