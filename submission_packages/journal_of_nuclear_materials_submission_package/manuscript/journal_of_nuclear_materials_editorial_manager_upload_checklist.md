# Journal of Nuclear Materials Editorial Manager upload checklist

This checklist maps the current submission artifacts to likely Elsevier Editorial Manager upload fields. Confirm the exact field names in the live submission system before final upload.

## Submission status

Current status: locally package-ready, externally blocked by repository DOI/stable URL insertion and final author approval.

Do not submit until:

- The reduced reproducibility package has been deposited in a persistent repository.
- The generated DOI or stable URL has been inserted into the manuscript Data availability statement.
- The corresponding author has confirmed the author list, affiliations, CRediT statement, competing-interest statement, data/code availability statements and conservative claim boundaries.

## File upload matrix

| Editorial Manager item | Upload file | Current state | Action before upload |
| --- | --- | --- | --- |
| Manuscript file | `manuscript/journal_of_nuclear_materials_submission.pdf` | Ready for review upload | Replace only if the repository DOI is inserted and the PDF is regenerated |
| LaTeX source files | `submission_packages/journal_of_nuclear_materials_flat_source.zip` | Ready if source upload is requested | Use this flat bundle rather than nested source paths |
| Highlights | `manuscript/journal_of_nuclear_materials_highlights.md` | Ready | Paste into the Highlights field or upload as requested |
| Cover letter | `manuscript/journal_of_nuclear_materials_cover_letter_draft.md` | Draft ready | Corresponding author should review scope-fit wording |
| Graphical abstract | `figures/main/journal_of_nuclear_materials_graphical_abstract.png` or `.tiff` | Ready | Upload separately if the system requests/permits it |
| Supplementary material | `manuscript/journal_of_nuclear_materials_supplementary.pdf` | Ready | Upload as Supplementary material or Supporting information |
| Declarations | `manuscript/journal_of_nuclear_materials_elsevier_declarations.md` | Draft ready | Paste the relevant text into the system fields after final author confirmation |
| Author metadata | `manuscript/journal_of_nuclear_materials_author_metadata.csv` | Draft ready | Use for author order, affiliations, corresponding author and CRediT entry |
| Data/code availability support | `submission_packages/journal_of_nuclear_materials_reproducibility_package.zip` | Package ready, DOI pending | Deposit externally first; do not upload only as an anonymous supplement unless the journal explicitly asks |
| Repository metadata | `manuscript/journal_of_nuclear_materials_repository_metadata_zenodo.json` | Draft ready | Use as a Zenodo/Figshare metadata source; update DOI after deposit |
| Asset manifest | `manuscript/journal_of_nuclear_materials_submission_asset_manifest.csv` | Ready | Use as an internal upload guide |
| Reviewer-risk prebuttal | `manuscript/journal_of_nuclear_materials_reviewer_risk_prebuttal.md` | Internal support ready | Do not upload unless requested; use to prepare cover-letter edits and reviewer responses |
| Figure/table source-data matrix | `manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv` | Internal support ready | Keep in reduced reproducibility package; use to answer data/figure provenance questions |
| Claim-evidence boundary matrix | `manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv` | Internal support ready | Keep internal unless requested; use to maintain conservative claim boundaries |
| Material-degradation mechanism-index audit | `docs/jnm_material_degradation_mechanism_indices_20260613.md` and `tables/jnm_material_degradation_mechanism_indices.csv` | Internal support ready | Keep in reduced reproducibility package; use to explain how fracture events, force topology and macro-response support the materials mechanism |

## Metadata to enter manually

Title:

Acceptance-gated bonded-template DEM reveals localized fracture sequences in Li4SiO4 ceramic breeder beds

Article type:

Research article

Keywords:

lithium orthosilicate; ceramic breeder material; pebble bed; bonded-particle DEM; pebble crushing; fracture-event sequence; nuclear materials

Corresponding author:

Jian Wang, `wjfttt@mail.ustc.edu.cn`

Affiliations:

1. Anhui University of Science and Technology, Huainan, Anhui 232001, China
2. Institute of Plasma Physics, Chinese Academy of Sciences, Hefei, Anhui 230031, China

Author-affiliation mapping:

- Jian Wang: 1, 2
- Siyu Wang: 1
- Hang Zhang: 1
- Ming-Zhun Lei: 2
- Wei Wen: 1, 2
- Qi-Gang Wu: 2
- Gang Shen: 1
- Haishun Deng: 1

## Final validation commands

After repository deposition, insert the DOI or stable URL with:

```bash
python3 scripts/insert_jnm_repository_identifier.py https://doi.org/10.xxxx/xxxxx --apply --rebuild
```

Preview the files that would change without writing anything:

```bash
python3 scripts/insert_jnm_repository_identifier.py https://doi.org/10.xxxx/xxxxx --dry-run
```

To prepare a small folder containing only repository-deposit files, run:

```bash
python3 scripts/build_jnm_repository_deposit_staging.py
```

Then upload `submission_packages/jnm_repository_deposit_staging/journal_of_nuclear_materials_reproducibility_package.zip` to the repository and keep the paired `.sha256` file for checksum verification.

Run these from the repository root after any final manuscript edit:

```bash
python3 scripts/build_journal_of_nuclear_materials_latex.py
cd manuscript
latexmk -xelatex -interaction=nonstopmode -halt-on-error journal_of_nuclear_materials_submission.tex
cd ..
python3 scripts/build_jnm_elsevier_flat_source_bundle.py
cd submission_packages/journal_of_nuclear_materials_flat_source
latexmk -xelatex -interaction=nonstopmode -halt-on-error journal_of_nuclear_materials_submission.tex
cd ../..
python3 scripts/check_jnm_submission_gate.py
bash scripts/build_journal_of_nuclear_materials_submission_package.sh
cd submission_packages
shasum -a 256 -c journal_of_nuclear_materials_submission_package.zip.sha256
shasum -a 256 -c journal_of_nuclear_materials_flat_source.zip.sha256
```

Then confirm that the final logs contain no unresolved citations or LaTeX fatal errors:

```bash
rg -n 'undefined|Citation.*undefined|LaTeX Error|Emergency stop|Fatal error|There were undefined citations' \
  manuscript/journal_of_nuclear_materials_submission.log \
  submission_packages/journal_of_nuclear_materials_flat_source/journal_of_nuclear_materials_submission.log
```

No output is the expected result.

The automated gate report is written to:

- `docs/jnm_final_submission_gate_report.md`
- `docs/jnm_final_submission_gate_report.json`

The expected status before repository deposition is `BLOCKED_EXTERNAL` with no `FAIL` entries. After inserting the repository DOI or stable URL and rebuilding the manuscript/package, the expected status is `PASS`.

## Scientific claim boundary for upload

Use the current conservative framing in the manuscript:

- The weak-plane single-pebble template is a current calibration candidate, not a final Li4SiO4 material law.
- The corrected 100-mother-pebble calculations provide event-sequence and sensitivity evidence, not converged failure-probability statistics.
- The earlier diagnostic bed-scale interpretation is withdrawn and should not be revived in the cover letter, highlights or response text.
- The central contribution is the acceptance-gated fracture-event diagnostic: zero seating damage, native force-connectivity gates and mother-pebble-resolved bond-loss histories.
- The reviewer-risk prebuttal should be kept internal; it is a preparation aid for maintaining conservative JNM-facing language.
- The source-data and claim-evidence matrices should remain in the reduced reproducibility package so every display item and core claim remains traceable to evidence.
- The material-degradation mechanism-index audit should be used as reviewer-support evidence for the bounded mechanism claim: localized microcracking can coexist with force-network densification/reorganization and peak-to-endpoint load relaxation, but it is not a coupled thermal-flow prediction.
