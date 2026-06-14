# JNM final upload manifest

This manifest distinguishes the public repository deposit files from local Editorial Manager support files.

## Public repository upload

- Upload zip: `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/journal_of_nuclear_materials_reproducibility_package.zip`
- SHA256: `ffa2c5d8b73c8c39093eb7b288d4b4fabdc4e3ac2524f9f334747cd91f719430`
- Do not upload `submission_packages/journal_of_nuclear_materials_submission_package.zip` as the public data repository record.

## Machine-readable manifest

- CSV: `docs/jnm_final_upload_manifest.csv`

## Entries

| Role | Destination | Action | Path |
| --- | --- | --- | --- |
| public_reproducibility_zip | repository | UPLOAD_TO_REPOSITORY | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/journal_of_nuclear_materials_reproducibility_package.zip` |
| public_reproducibility_checksum | repository | UPLOAD_OR_RECORD_WITH_REPOSITORY | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/journal_of_nuclear_materials_reproducibility_package.zip.sha256` |
| repository_metadata_json | repository | USE_AS_METADATA_SOURCE | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/journal_of_nuclear_materials_repository_metadata_zenodo.json` |
| repository_metadata_readme | repository | USE_AS_METADATA_GUIDE | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/journal_of_nuclear_materials_repository_metadata_readme.md` |
| repository_deposit_checklist_en | repository_support | READ_BEFORE_DEPOSIT | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/jnm_repository_deposit_action_checklist.md` |
| repository_deposit_checklist_zh | repository_support | READ_BEFORE_DEPOSIT | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/jnm_repository_deposit_action_checklist_zh.md` |
| repository_deposit_handoff_zh | repository_support | READ_BEFORE_DEPOSIT | `submission_packages/jnm_repository_deposit_FROZEN_20260614_ffa2c5d8/jnm_repository_deposit_final_handoff_zh.md` |
| editorial_manager_upload_ready_zip | editorial_manager | UPLOAD_OR_UNZIP_FOR_EDITORIAL_MANAGER | `submission_packages/jnm_editorial_manager_upload_ready.zip` |
| manuscript_pdf | editorial_manager | UPLOAD_TO_EDITORIAL_MANAGER_AFTER_DOI_INSERTION | `manuscript/journal_of_nuclear_materials_submission.pdf` |
| flat_latex_source_zip | editorial_manager | UPLOAD_IF_SOURCE_FILES_REQUESTED | `submission_packages/journal_of_nuclear_materials_flat_source.zip` |
| paste_ready_fields | editorial_manager | PASTE_INTO_EDITORIAL_MANAGER_AFTER_DOI_INSERTION | `manuscript/journal_of_nuclear_materials_editorial_manager_paste_fields.md` |
| local_submission_support_package | local_support_only | DO_NOT_UPLOAD_AS_PUBLIC_REPOSITORY_RECORD | `submission_packages/journal_of_nuclear_materials_submission_package.zip` |
