# Computational Particle Mechanics submission package, 2026-07-04

This repository contains the compact reproducibility and submission-support
materials for the manuscript:

**Bonded-template DEM reveals strength- and topology-dependent
fracture-event sequences in packed brittle ceramic pebbles**

The citable archived version is:

https://doi.org/10.5281/zenodo.20687351

## Current submission files

- Upload-ready Computational Particle Mechanics package:
  `submission_packages/computational_particle_mechanics_upload_ready.zip`
- Package checksum:
  `submission_packages/computational_particle_mechanics_upload_ready.zip.sha256`
- Reduced reproducibility package:
  `submission_packages/repaired_submission_package.zip`
- Reduced reproducibility checksum:
  `submission_packages/repaired_submission_package.zip.sha256`
- Optional blinded-review package for double-anonymized review:
  `submission_packages/computational_particle_mechanics_blinded_review_optional.zip`
- Optional blinded-review checksum:
  `submission_packages/computational_particle_mechanics_blinded_review_optional.zip.sha256`

The upload-ready package contains the manuscript PDF, Highlights, graphical
abstract, declaration, cover letter, author contribution file, LaTeX source zip
and editorial-system paste fields, separate main-figure files and an author
e-mail completion sheet.

The reduced reproducibility package contains manuscript-level source data,
tables, figure-generation scripts, checking scripts, figures, the rebuilt
manuscript files, and the current CPM support evidence for official-guide
alignment, literature-gap mapping, material-response summary and reviewer-risk
review. It is intended to reproduce the processed evidence used by the paper,
not the full raw DEM trajectories.

## Large raw data

Very large raw restart files and full local-bond dump histories are retained in
offline archive storage and are not stored in this GitHub repository. The
manuscript and reproducibility package use processed tables, figure-source CSV
files and representative input files to support manuscript-level regeneration.

## Basic verification

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/check_computational_particle_mechanics_submission_package.py
(cd submission_packages && shasum -a 256 -c repaired_submission_package.zip.sha256)
(cd submission_packages && shasum -a 256 -c computational_particle_mechanics_upload_ready.zip.sha256)
```

The current local verification status is recorded in:

- `START_HERE_CPM_SUBMISSION.md`
- `docs/cpm_submission_readiness_report_20260704.md`
- `docs/cpm_submission_readiness_report_20260704.json`
- `docs/cpm_live_submission_packet_20260704.md`
- `docs/cpm_live_submission_packet_20260704.csv`
- `docs/cpm_live_submission_packet_20260704.json`
- `docs/cpm_live_submission_packet_docx_qa_20260704.md`
- `docs/cpm_literature_gap_map_20260704.md`
- `docs/cpm_literature_gap_map_20260704.csv`
- `docs/cpm_official_submission_guide_alignment_20260704.md`
- `docs/cpm_official_submission_guide_alignment_20260704.csv`
- `docs/cpm_material_response_summary_20260704.md`
- `docs/cpm_material_response_summary_20260704.csv`
- `docs/computational_particle_mechanics_submission_package_qa_20260704.md`
- `docs/next_stage_optimization_plan.md`

The readiness report is intentionally kept outside the reduced reproducibility
zip because it records the current package checksum. The latest local status is
`ready_for_live_submission_after_external_metadata`; the remaining external
metadata item is seven coauthor e-mail addresses if the live submission system
requires every author's e-mail address.

The optional blinded-review package is provided because the official guide
states that the journal uses a double-anonymized review process. Use it only if
the live submission workflow requests a blinded manuscript file; otherwise use
the full manuscript in the main upload package.

Practical submission support files are:

- `manuscript/computational_particle_mechanics_coauthor_email_request_zh_en.docx`
- `manuscript/computational_particle_mechanics_live_submission_checklist.docx`
- `manuscript/computational_particle_mechanics_live_submission_packet.docx`

Regenerate the readiness report with:

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_cpm_submission_readiness_report.py
```

Regenerate the live-submission packet with:

```bash
/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_cpm_live_submission_packet.py
```

The package check also runs:

```bash
python3 scripts/check_cpm_scientific_alignment.py
python3 scripts/check_cpm_reviewer_risk_preflight.py
```

These checks verify that the manuscript, cover letter, editorial fields and
literature-gap map use the same scientific rationale, and that the main
editor/reviewer risks are mapped to current evidence and conservative
boundaries.

Regenerate the literature-gap map with:

```bash
python3 scripts/build_cpm_literature_gap_map.py
```

Regenerate the reviewer-risk preflight matrix with:

```bash
python3 scripts/build_cpm_reviewer_risk_preflight.py
```

Regenerate the material-response summary with:

```bash
python3 scripts/build_cpm_material_response_summary.py
```
