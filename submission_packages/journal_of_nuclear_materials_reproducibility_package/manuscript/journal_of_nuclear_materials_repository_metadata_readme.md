# Repository metadata draft for the reduced reproducibility package

This file accompanies `journal_of_nuclear_materials_repository_metadata_zenodo.json` and records how to use it when depositing the reduced reproducibility package.

## Recommended deposited file

Deposit:

- `submission_packages/journal_of_nuclear_materials_reproducibility_package.zip`

Also keep locally:

- `submission_packages/journal_of_nuclear_materials_reproducibility_package.zip.sha256`

## Suggested repository title

Reduced reproducibility package for acceptance-gated bonded-template DEM of Li4SiO4 breeder-bed fracture sequences

## Suggested repository description

This reduced reproducibility package supports the manuscript "Acceptance-gated bonded-template DEM reveals localized fracture sequences in Li4SiO4 ceramic breeder beds". It contains processed single-pebble validation summaries, corrected-bed thermo histories, mother-pebble bond-series tables, breakage-event tables, native force-network summaries, figure source data, manuscript figures and post-processing scripts. Very large DEM restart files and complete raw local-bond dump histories are retained outside this reduced package and can be assembled as larger audit bundles on reasonable request.

The corresponding live GitHub repository is:

https://github.com/wangjianfttt/Mother_particle_bonded_dem_research

The citable archived package uses the DOI:

https://doi.org/10.5281/zenodo.20687351

## Suggested license

Use `CC BY 4.0` for the reduced data/figure/script package unless the corresponding author or institution prefers another repository license. If code reuse is expected, consider adding a separate software license before public release.

## Required final edits after deposit

After the repository creates a DOI or stable URL, use the helper script rather than editing files by hand:

```bash
python3 scripts/insert_jnm_repository_identifier.py https://doi.org/10.xxxx/xxxxx --dry-run
python3 scripts/insert_jnm_repository_identifier.py https://doi.org/10.xxxx/xxxxx --apply --rebuild
```

The `--rebuild` path regenerates the manuscript TeX/PDF, the flat Elsevier source bundle, the main submission package, the public reproducibility package, the Chinese deposit handoff, the repository-deposit staging folder and the final gate report. It refreshes the staging folder after the handoff is regenerated so package hashes and handoff text remain synchronized. Do not hand-edit `manuscript/journal_of_nuclear_materials_submission.tex`; it is regenerated from the Markdown draft.

The current dry-run coverage includes these files:

- `manuscript/journal_of_nuclear_materials_submission_draft.md`
- `manuscript/journal_of_nuclear_materials_cover_letter_draft.md`
- `manuscript/journal_of_nuclear_materials_elsevier_declarations.md`
- `manuscript/journal_of_nuclear_materials_editorial_manager_upload_matrix.csv`
- `manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv`
- `manuscript/journal_of_nuclear_materials_repository_metadata_readme.md`
- `manuscript/journal_of_nuclear_materials_reviewer_risk_matrix.csv`
- `manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv`
- `manuscript/journal_of_nuclear_materials_resubmission_plan.md`
- `docs/jnm_submission_readiness_audit_20260612.md`
- `docs/next_stage_optimization_plan.md`
- `manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json`

Search for:

```text
https://doi.org/10.5281/zenodo.20687351
repository DOI or stable URL
repository identifier inserted: https://doi.org/10.5281/zenodo.20687351
```

The preferred update route is now:

```bash
python3 scripts/insert_jnm_repository_identifier.py https://doi.org/10.xxxx/xxxxx --apply --rebuild
```

Use `--dry-run` first to preview the files that would change. After the rebuild, the expected final gate status is `PASS`; if the gate remains `BLOCKED_EXTERNAL`, inspect `docs/jnm_final_submission_gate_report.md` for the remaining placeholder file.
