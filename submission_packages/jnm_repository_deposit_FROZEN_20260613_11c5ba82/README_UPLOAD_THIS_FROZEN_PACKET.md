# Frozen JNM repository deposit packet

This folder is a frozen copy of the repository-deposit packet prepared for the Journal of Nuclear Materials submission.

## Upload this file

Upload only this public reproducibility package to Zenodo, Figshare or an institutional repository:

`journal_of_nuclear_materials_reproducibility_package.zip`

Current SHA256:

`11c5ba82a7912540861437e4d30c589cb4ff65afaed2a7bc63d6c685a7a95fc7`

Verify before upload:

```bash
shasum -a 256 -c journal_of_nuclear_materials_reproducibility_package.zip.sha256
```

Expected output:

```text
journal_of_nuclear_materials_reproducibility_package.zip: OK
```

## Use these supporting files

- `journal_of_nuclear_materials_repository_metadata_zenodo.json`: metadata source for repository title, creators, description, keywords and license.
- `journal_of_nuclear_materials_repository_metadata_readme.md`: human-readable metadata guide.
- `jnm_repository_deposit_action_checklist.md`: English upload checklist.
- `jnm_repository_deposit_action_checklist_zh.md`: Chinese upload checklist.
- `jnm_repository_deposit_final_handoff_zh.md`: Chinese final handoff.
- `jnm_final_upload_manifest.md` and `.csv`: routing table distinguishing repository files from Editorial Manager files.

## Do not mix hashes

If the project package is rebuilt later, the staging zip hash may change. For this frozen packet, keep the zip and `.sha256` file together and use the SHA above.

After the repository gives a DOI or stable URL, return to the project root and run:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```
