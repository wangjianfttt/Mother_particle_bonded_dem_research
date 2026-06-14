# Repository deposit action checklist for the JNM reproducibility package

This checklist is for the author-side repository deposit that must be completed before final Journal of Nuclear Materials upload.

## 1. Files to upload

Upload the reduced public package:

- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip`

Also upload or retain with the repository record, if the repository allows supporting files:

- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip.sha256`
- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_repository_metadata_zenodo.json`
- `submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_repository_metadata_readme.md`

Do not upload the internal Editorial Manager support package as the public data record:

- `submission_packages/journal_of_nuclear_materials_submission_package.zip`

That internal package contains cover-letter, declaration and reviewer-preparation support files and is not the public reproducibility package.

## 2. Repository metadata to enter

Use this title:

Reduced reproducibility package for acceptance-gated bonded-template DEM of Li4SiO4 breeder-bed fracture sequences

Use these core fields:

- Upload/resource type: dataset
- Version: 1.0
- Access: open
- License: CC BY 4.0, unless the corresponding author or institution chooses another compatible license
- Language: English
- Keywords: Li4SiO4; ceramic breeder; fusion blanket; pebble bed; bonded-particle DEM; fracture-event sequence; native force network; Journal of Nuclear Materials

Use `journal_of_nuclear_materials_repository_metadata_zenodo.json` as the structured metadata source, but confirm author names, affiliations, ORCID identifiers and repository community before publishing.

## 3. Before publishing the repository record

Confirm that the public package contains only public manuscript, processed-data, figure, script, representative-input and audit artifacts. It should not contain cover-letter drafts, author declaration checklists, reviewer-risk prebuttal files or local absolute paths.

Local checks before upload:

```bash
python3 scripts/check_jnm_public_repro_package.py
python3 scripts/check_jnm_repository_deposit_staging.py
cd submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e
shasum -a 256 -c journal_of_nuclear_materials_reproducibility_package.zip.sha256
cd -
```

Expected current pre-DOI status:

- public reproducibility package: PASS
- repository-deposit staging: PASS
- final submission gate: BLOCKED_EXTERNAL only because the DOI/stable URL is still missing

## 4. After DOI or stable URL is reserved

Preview DOI insertion from the project root:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
```

Then apply and rebuild:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

The helper updates the data availability statement, submission-support files, repository metadata readme, evidence matrices and mainline status, then rebuilds the manuscript PDF, flat source bundle, submission package, public reproducibility package, Chinese deposit handoff, deposit staging folder and final gate report. The staging folder is refreshed after the handoff is regenerated so the package checksum and handoff text stay synchronized.

## 5. Final expected local gate

After DOI insertion, run:

```bash
python3 scripts/check_jnm_submission_gate.py --strict
```

The expected final local status after a valid DOI/stable URL is inserted is `PASS`. If the status remains `BLOCKED_EXTERNAL`, inspect:

- `docs/jnm_final_submission_gate_report.md`

and update the listed remaining placeholder file through the DOI insertion helper rather than editing generated TeX by hand.
