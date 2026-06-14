# Journal of Nuclear Materials submission start here

This is the shortest path from the current local package to submission.

## Current verified state

- No current-workspace DEM/LIGGGHTS, LaTeX or package-rebuild process is running.
- The main workspace is intentionally still in the pre-DOI state:

```text
overall_status=BLOCKED_EXTERNAL
84 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL
```

- The DOI-insertion/rebuild route has been rehearsed in an isolated temporary copy using the explicit fake-identifier override. That temporary copy reached:

```text
overall_status=PASS
85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL
```

- The main workspace contains no concrete test DOI or example repository URL; insert only the real repository DOI or stable URL after depositing the frozen package below.

## 1. Upload the frozen repository package first

Use this folder:

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/`

Run:

```bash
submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/VERIFY_BEFORE_UPLOAD.sh
```

Upload this file to Zenodo, Figshare or an institutional repository:

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_reproducibility_package.zip`

Frozen SHA256:

`b9a8bd2e16ea84ed874e31bac701fb0a45b22fe9435b3a2c898306c518a28a30`

Use the metadata in:

`submission_packages/jnm_repository_deposit_FROZEN_20260614_b9a8bd2e/journal_of_nuclear_materials_repository_metadata_zenodo.json`

For copy-paste repository fields, use:

`docs/jnm_repository_deposit_copy_paste_fields.md`

Do not upload `submission_packages/journal_of_nuclear_materials_submission_package.zip` as the public data record.

## 2. Insert the repository DOI or stable URL

After the repository gives a DOI or stable URL, run from the project root:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

Expected final gate after DOI insertion:

```text
overall_status=PASS
85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL, 0 FAIL
```

## 3. Submit to Editorial Manager

Use the files listed in:

`docs/jnm_author_final_upload_readme_zh.md`

Current pre-DOI local gate is intentionally:

```text
overall_status=BLOCKED_EXTERNAL
84 PASS, 0 WARN, 1 BLOCKED_EXTERNAL, 0 FAIL
```

The only blocker should be the repository DOI/stable URL.
