# JNM repository deposit staging

This folder contains the files needed to deposit the reduced reproducibility package for the Journal of Nuclear Materials submission.
The manuscript source package inside the zip is Elsevier-native (`elsarticle`/`frontmatter`) and uses the bundled `elsarticle-num.bst` numeric bibliography style.

## Upload this file to the repository

- `journal_of_nuclear_materials_reproducibility_package.zip`

Keep the checksum file with your records and, if the repository allows multiple files, upload it as supporting metadata:

- `journal_of_nuclear_materials_reproducibility_package.zip.sha256`

From this staging folder, verify the package checksum before upload:

```bash
shasum -a 256 -c journal_of_nuclear_materials_reproducibility_package.zip.sha256
```

## Suggested repository metadata

- Title: Reduced reproducibility package for acceptance-gated bonded-template DEM of Li4SiO4 breeder-bed fracture sequences
- Upload type: dataset
- License: cc-by-4.0
- Access: open
- Version: 1.0
- Language: eng
- Keywords: Li4SiO4, ceramic breeder, fusion blanket, pebble bed, bonded-particle DEM, fracture-event sequence, native force network, Journal of Nuclear Materials

Use `journal_of_nuclear_materials_repository_metadata_zenodo.json` as the structured metadata source.
Use `jnm_repository_deposit_action_checklist.md` as the step-by-step author-side upload checklist.
Use `jnm_repository_deposit_action_checklist_zh.md` as the Chinese author-side upload checklist.
Use `jnm_repository_deposit_final_handoff_zh.md` as the concise Chinese final handoff for the corresponding author.
Use `jnm_final_submission_action_summary.md` as the compact final upload sequence.

From the project root, this read-only command prints the upload file, checksum and current gate status:

```bash
python3 scripts/print_jnm_repository_deposit_packet.py
```

## After the repository reserves or publishes a DOI/stable URL

From the project root, run:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

Before applying, preview with:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
```

The current final-gate report is included here for audit context. Before DOI insertion, its expected status is `BLOCKED_EXTERNAL` with no local `FAIL` entries.
