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

The upload-ready package contains the manuscript PDF, Highlights, graphical
abstract, declaration, cover letter, author contribution file, LaTeX source zip
editorial-system paste fields and separate main-figure files.

The reduced reproducibility package contains manuscript-level source data,
tables, figure-generation scripts, checking scripts, figures and the rebuilt
manuscript files. It is intended to reproduce the processed evidence used by
the paper, not the full raw DEM trajectories.

## Large raw data

Very large raw restart files and full local-bond dump histories are retained in
offline archive storage and are not stored in this GitHub repository. The
manuscript and reproducibility package use processed tables, figure-source CSV
files and representative input files to support manuscript-level regeneration.

## Basic verification

```bash
python3 scripts/check_repaired_full_manuscript_consistency.py
(cd submission_packages && shasum -a 256 -c repaired_submission_package.zip.sha256)
(cd submission_packages && shasum -a 256 -c computational_particle_mechanics_upload_ready.zip.sha256)
```

The current local verification status is recorded in:

- `docs/computational_particle_mechanics_submission_package_qa_20260704.md`
- `docs/next_stage_optimization_plan.md`
