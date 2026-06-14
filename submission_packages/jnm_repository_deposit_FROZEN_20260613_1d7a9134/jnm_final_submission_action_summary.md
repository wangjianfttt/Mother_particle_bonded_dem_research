# JNM final submission action summary

This is the short author-side checklist for converting the locally prepared Journal of Nuclear Materials package into a final upload. It is intentionally narrower than the full audit files.

## Current local status

- Local manuscript/package gate: `BLOCKED_EXTERNAL`
- Local failures: none
- Expected blocker: repository DOI or stable URL has not yet been inserted
- Public reproducibility package: prepared and checksum-verified
- Editorial Manager support package: prepared and checksum-verified
- Final upload manifest: prepared and checksum-verified
- Current process state: no current-workspace DEM/LIGGGHTS, LaTeX or package-rebuild process is running
- DOI-insertion route: rehearsed in an isolated temporary copy with the explicit fake-identifier override; earlier rehearsals passed after the materials-novelty positioning and key numeric checks
- Latest local hardening: the key numeric gate now also runs `scripts/check_jnm_model_parameter_consistency.py` and `scripts/check_jnm_active_run_provenance.py`, which verify Methods/Table 2 parameters and the accepted PB-007 run-to-figure provenance against active logs, wrapper overrides, raw local dumps, processed CSV outputs and single-pebble inputs. The current pre-DOI gate remains 84 PASS, 0 WARN, 1 BLOCKED_EXTERNAL and 0 FAIL; the expected post-DOI gate remains 85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL and 0 FAIL.
- Main workspace hygiene: still contains no concrete test DOI or example repository URL

## Step 1: deposit the public reproducibility package

Upload this file to Zenodo, Figshare or an institutional repository:

- `submission_packages/jnm_repository_deposit_FROZEN_20260613_1d7a9134/journal_of_nuclear_materials_reproducibility_package.zip`
- Current verified package size/count: 121 files in the public reproducibility package
- Frozen SHA256: `1d7a9134c432cb50ecc968e4ee14428ca4fd378e50d97ffc36bdedaa30693039`

Keep or upload the checksum file:

- `submission_packages/jnm_repository_deposit_FROZEN_20260613_1d7a9134/journal_of_nuclear_materials_reproducibility_package.zip.sha256`

Run `submission_packages/jnm_repository_deposit_FROZEN_20260613_1d7a9134/VERIFY_BEFORE_UPLOAD.sh` before upload. The staging folder remains useful for generation and audit, but the frozen folder is the stable upload source.

Do not use this internal Editorial Manager support package as the public repository record:

- `submission_packages/journal_of_nuclear_materials_submission_package.zip`

Use the final upload manifest as the authoritative file-by-file routing table:

- `START_HERE_JNM_SUBMISSION.md`
- `docs/jnm_final_upload_manifest.md`
- `docs/jnm_final_upload_manifest.csv`

## Step 2: use these repository metadata fields

- Title: `Reduced reproducibility package for acceptance-gated bonded-template DEM of Li4SiO4 breeder-bed fracture sequences`
- Resource type: dataset
- Version: `1.0`
- Access: open
- License: CC BY 4.0 unless the corresponding author or institution chooses another compatible license
- Keywords: Li4SiO4; ceramic breeder; fusion blanket; pebble bed; bonded-particle DEM; fracture-event sequence; native force network; Journal of Nuclear Materials

Use this structured metadata file as the source for creators and description:

- `submission_packages/jnm_repository_deposit_FROZEN_20260613_1d7a9134/journal_of_nuclear_materials_repository_metadata_zenodo.json`

Use the Chinese author-side upload checklist if needed:

- `submission_packages/jnm_repository_deposit_FROZEN_20260613_1d7a9134/jnm_repository_deposit_action_checklist_zh.md`

## Step 3: insert the DOI or stable URL

After the repository reserves or publishes a DOI/stable URL, preview the update:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --dry-run
```

Then apply it and rebuild all derived artifacts:

```bash
python3 scripts/insert_jnm_repository_identifier.py <doi-or-stable-url> --apply --rebuild
```

Expected result after a valid DOI/stable URL is inserted:

- `python3 scripts/check_jnm_submission_gate.py` returns `overall_status=PASS`
- The DOI-insertion path has been rehearsed in a temporary copy with a test DOI URL and `JNM_ALLOW_FAKE_REPOSITORY_IDENTIFIER=1`; after the figure-caption companion, frozen-deposit-packet, start-here-guide, repository copy-paste-field gates, materials-novelty positioning audit and model-parameter consistency audit are included, the expected clean post-DOI state is 85 PASS, 0 WARN, 0 BLOCKED_EXTERNAL and 0 FAIL after rebuilding the manuscript, flat source, upload DOCX files, Editorial Manager package, public reproducibility package, Chinese deposit handoff, repository-deposit staging and final upload manifest. The current public reproducibility package verifies 121 files, including the event-topology mechanism audit and Fig. 5 mechanism-figure QA, while the frozen upload packet, root start-here guide, repository copy-paste fields, JNM materials-novelty positioning audit and model-parameter audit are separately checksum/wording verified. A real DOI/stable URL does not need this fake-identifier override, and the main workspace still contains no test DOI.

## Step 4: upload to Editorial Manager

Use these prepared files:

- Manuscript PDF: `manuscript/journal_of_nuclear_materials_submission.pdf`
- Flat LaTeX source bundle, if requested: `submission_packages/journal_of_nuclear_materials_flat_source.zip`
- Highlights: `manuscript/journal_of_nuclear_materials_highlights.md`
- Cover letter: `manuscript/journal_of_nuclear_materials_cover_letter_draft.md`
- Graphical abstract: `figures/main/journal_of_nuclear_materials_graphical_abstract.png` or `.tiff`
- Supplementary material: `manuscript/journal_of_nuclear_materials_supplementary.pdf`
- Declarations text: `manuscript/journal_of_nuclear_materials_elsevier_declarations.md`

## Final author checks

- Confirm author order, affiliations and CRediT roles.
- Confirm funding and competing-interest statements.
- Confirm the generative-AI declaration wording.
- Confirm the conservative claim boundaries: calibration candidate, event-sequence evidence, no converged failure probability, no final Li4SiO4 material law and no coupled thermal-flow prediction.
