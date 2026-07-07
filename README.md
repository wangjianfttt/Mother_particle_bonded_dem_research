# Bonded-template DEM fracture-event sequences in packed brittle ceramic pebbles

This repository contains the compact code, processed data, representative
inputs, figures and submission-support materials for the manuscript:

**Bonded-template DEM reveals strength- and topology-dependent fracture-event sequences in packed brittle ceramic pebbles**

The current target route is **Computational Particle Mechanics** through the
Elsevier/ScienceDirect double-anonymized submission workflow.

## Citable archive

The citable archived package is:

https://doi.org/10.5281/zenodo.20687351

The live GitHub repository is:

https://github.com/wangjianfttt/Mother_particle_bonded_dem_research

## What is included

- `scripts/`: template generation, post-processing, figure generation and
  package-check scripts.
- `data/figure_source/`: source CSV tables for manuscript figures.
- `data/processed/`: reduced processed event and force-network tables.
- `tables/`: mechanism, material-response and endpoint summary tables.
- `figures/`: editable and raster manuscript figures.
- `manuscript/`: LaTeX/Markdown manuscript sources and manuscript-side
  source-data maps.
- `submission_packages/`: public reproducibility, upload-ready and internal
  submission-support packages.
- `docs/`: readiness reports, reviewer-risk checks, official-guide alignment
  and storage/offload records.

The repository is intended to reproduce manuscript-level processed evidence,
figures and submission materials. It is not a full raw-trajectory archive.

## Large raw data boundary

Very large DEM restart files, raw particle dumps, local-bond dumps and complete
contact histories are retained outside the GitHub repository in local/NAS
archive storage. The compact package uses processed tables, figure-source CSV
files and representative inputs for reproducible manuscript-level evidence.

The current local storage record notes zero local DEM raw/restart residues
above 20 MB in `simulations/`, with archived raw outputs under the NAS path
documented in:

- `docs/nas_raw_dump_storage_check_20260704_1736.md`
- `docs/next_stage_optimization_plan.md`

## Current submission packages

- CPM upload package:
  `submission_packages/computational_particle_mechanics_upload_ready.zip`
- CPM upload package checksum:
  `submission_packages/computational_particle_mechanics_upload_ready.zip.sha256`
- Double-anonymized blinded review package:
  `submission_packages/computational_particle_mechanics_blinded_review_package.zip`
- Public code/data reproducibility package:
  `submission_packages/computational_particle_mechanics_public_reproducibility_package.zip`
- Public code/data reproducibility checksum:
  `submission_packages/computational_particle_mechanics_public_reproducibility_package.zip.sha256`
- Internal reduced submission-support package:
  `submission_packages/repaired_submission_package.zip`
- Internal reduced submission-support checksum:
  `submission_packages/repaired_submission_package.zip.sha256`

The live readiness status is recorded in:

- `START_HERE_CPM_SUBMISSION.md`
- `docs/cpm_submission_readiness_report_20260704.md`
- `docs/cpm_external_submission_status_20260708.md`
- `docs/cpm_goal_completion_audit_20260704.md`
- `docs/cpm_live_submission_packet_20260704.md`

The current local status is
`ready_for_live_submission_after_external_metadata`: scientific evidence,
figures, source-data matrices, checks and upload packages pass local
preflight; the remaining external item is completion or confirmation of seven
non-corresponding-author e-mail entries if the live submission system requires
all author e-mails, followed by inspection of the system-generated PDF preview.

## Verification

Use the bundled Codex Python runtime if `python-docx` is not installed in the
system Python:

```bash
<user-home>/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/build_cpm_public_repro_package.py
<user-home>/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/build_repaired_submission_package.py
<user-home>/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/check_computational_particle_mechanics_submission_package.py
python3 scripts/check_cpm_public_repro_package.py
python3 scripts/check_repaired_submission_package.py
(cd submission_packages && shasum -a 256 -c computational_particle_mechanics_upload_ready.zip.sha256)
(cd submission_packages && shasum -a 256 -c computational_particle_mechanics_public_reproducibility_package.zip.sha256)
(cd submission_packages && shasum -a 256 -c repaired_submission_package.zip.sha256)
```

Expected current result:

```text
PASS CPM submission package: manifest=19, figures=19, figure source-data check, docx=11, DOI, guide alignment, public reproducibility package, live packet and double-anonymous blinded review manuscript verified
PASS CPM public reproducibility package: 93 files, manifest, checksum, representative inputs and public-file hygiene verified
PASS repaired submission package check
computational_particle_mechanics_upload_ready.zip: OK
computational_particle_mechanics_public_reproducibility_package.zip: OK
repaired_submission_package.zip: OK
```

## Citation

Please cite the archived package using the DOI above. A GitHub citation file is
provided in `CITATION.cff`.


## Public Reproducibility Package

This folder is the public code/data package for the Computational Particle
Mechanics manuscript. It intentionally excludes cover letters, author e-mail
collection files, live submission packets and editorial upload work files.

Package archive: `submission_packages/computational_particle_mechanics_public_reproducibility_package.zip`
Checksum file: `submission_packages/computational_particle_mechanics_public_reproducibility_package.zip.sha256`
Repository DOI: https://doi.org/10.5281/zenodo.20687351
