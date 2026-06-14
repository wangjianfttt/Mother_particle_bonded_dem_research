# Reduced reproducibility package for the Journal of Nuclear Materials submission

This reduced package supports the manuscript:

**Acceptance-gated bonded-template DEM reveals localized fracture sequences in Li4SiO4 ceramic breeder beds**

It contains the processed data, figures, tables and scripts needed to audit the manuscript-level claims without including very large restart files or full raw local-dump histories.

## Contents

- `manuscript/`: compiled manuscript PDF, LaTeX source, Markdown source, supplementary file, highlights, references, repository metadata and evidence matrices.
- `figures/`: manuscript figure files and selected validation figures.
- `tables/`: summary tables for single-pebble validation and corrected-bed evidence.
- `data/processed/`: processed thermo histories, bond-series tables, breakage-event tables, native force-network series and figure source data.
- `simulations/`: representative DEM input files and the 500-subparticle zero-overlap bonded template used to audit the model setup without shipping large restart/local-dump histories.
- `scripts/`: post-processing, figure-building, package-building and audit scripts used for the included results.
- `MANIFEST.csv`: SHA256 checksum, relative path and file size for every packaged file.
- `manuscript/journal_of_nuclear_materials_figure_table_source_data_matrix.csv`: item-level map from every manuscript figure/table and graphical abstract to output files, source data and regeneration or audit scripts.
- `manuscript/journal_of_nuclear_materials_claim_evidence_boundary_matrix.csv`: claim-level map from core manuscript statements to supporting evidence, conservative wording boundaries and likely reviewer-risk categories.

The public package intentionally excludes cover letters, author declarations,
author metadata sheets, Editorial Manager checklists, reviewer-risk prebuttals
and resubmission planning notes. Those files are maintained only in the local
submission-support package.

## Evidence boundary

The package supports a corrected 100-mother-pebble event-sequence study. It does not claim a converged Li4SiO4 failure-probability distribution or a final breeder-material law. The selected single-pebble template is a current calibration candidate, and the bed-scale evidence is interpreted as acceptance-gated event-sequence and force-network evidence.

The earlier diagnostic bed-scale fracture interpretation was withdrawn after the native force-transmission audit and is not used as manuscript evidence.

## Quick provenance map

For a fast audit, start from the two matrices in `manuscript/` and then inspect the item-specific files below.

| Manuscript item | Main packaged evidence | Main regeneration or audit script | Supported claim boundary |
| --- | --- | --- | --- |
| Fig. 2 | `tables/single_pebble_calibration_target_evidence_summary.csv`; `tables/single_pebble_model_ensemble_evidence_summary.csv`; `tables/sp002_conditioned_ensemble_completed_summary.csv` | `scripts/plot_single_pebble_calibration_evidence.py` | Current load-scale and fragment-mode matched single-pebble calibration candidate. |
| Fig. 3 | `tables/jnm_single_pebble_resolution_summary.csv`; `tables/jnm_single_pebble_rate_summary.csv` | `scripts/build_jnm_single_pebble_validation.py` | Resolution and rate sensitivity over the tested windows, not full numerical convergence. |
| Fig. 4 | Acceptance-summary and native-force summary tables listed in the Fig. 4 row of the source-data matrix. | `scripts/plot_pb007_acceptance_gate_validation.py`; `scripts/summarize_pb007_loadpath_validation.py` | Zero-pre-damage and native force-transmission acceptance gate for the corrected bed route. |
| Fig. 5 | Thermo history, breakage-event table and native force-network series listed in the Fig. 5 row of the source-data matrix. | `scripts/plot_pb007_corrected_fracture_sequence.py`; `scripts/analyze_pb007_bond_event_sequence.py`; `scripts/analyze_pb007_native_force_network_series.py` | One corrected pilot event sequence linking local internal bond loss, macro response and native force-network evolution. |
| Fig. 6 and Table 1 | `data/processed/pb007_replicate_comparison_source_data.csv`; `tables/pb007_macro_topology_event_metrics.csv`; `tables/jnm_material_degradation_mechanism_indices.csv`; `tables/pb007_event_aligned_topology.csv` | `scripts/build_pb007_replicate_comparison.py`; `scripts/summarize_pb007_mechanism_metrics.py`; `scripts/summarize_jnm_material_degradation_indices.py`; `scripts/summarize_pb007_event_aligned_topology.py` | Pilot-versus-independent-bed comparison and bounded mechanism indices, not converged stochastic failure probabilities. |

The final local submission gate report is intentionally not embedded in this public zip. It is staged beside the zip in `submission_packages/jnm_repository_deposit_staging/` so the public package does not contain a self-referential report that becomes stale after each rebuild.

## Regeneration notes

The reported DEM calculations used the simulation environment described in the manuscript Methods Summary. The reduced package is designed for manuscript-level audit and regeneration of processed outputs; it includes representative DEM input files and the zero-overlap bonded template, but it does not redistribute the local DEM executable, full restart states or complete raw local-bond dump histories.

The main manuscript PDF can be regenerated from:

```bash
python3 scripts/build_journal_of_nuclear_materials_latex.py
cd manuscript
latexmk -xelatex -interaction=nonstopmode -halt-on-error journal_of_nuclear_materials_submission.tex
```

The replicate-comparison figure and mechanism table can be regenerated from:

```bash
python3 scripts/summarize_pb007_mechanism_metrics.py
python3 scripts/build_pb007_replicate_comparison.py
```

The figure/table source-data coverage matrix can be checked with:

```bash
python3 scripts/check_jnm_source_data_matrix.py
```

The claim-evidence-boundary matrix can be checked with:

```bash
python3 scripts/check_jnm_claim_evidence_matrix.py
```

Full DEM restart files and complete raw local-bond dump histories are retained outside this reduced package because of file-size constraints. They can be assembled as a larger audit bundle if requested by reviewers or the journal.
