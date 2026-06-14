# Nuclear Fusion data and code package plan

This file defines the reduced reproducibility package for a Nuclear Fusion submission. It deliberately excludes very large restart and full local-bond dump histories unless they are needed for audit or reviewer request.

## Package principle

The upload package should allow a reviewer to reproduce the manuscript figures and tables from reduced event data, while the full raw simulation outputs remain archived locally or in a larger case bundle. This keeps the public repository useful without making it impractically large.

## Core manuscript data

| Category | Include | Purpose |
| --- | --- | --- |
| Single-pebble calibration tables | `tables/single_pebble_calibration_target_evidence_summary.csv`; `tables/single_pebble_model_ensemble_evidence_summary.csv`; `tables/sp002_force_displacement_overlay_metrics.csv` | Supports Fig. 2 and Extended Data Fig. 1. |
| PB-006 event database | `tables/pb006_breakage_event_database.csv`; `tables/pb006_breakage_event_database_summary.csv`; `tables/pb006_1000_orientation_sensitivity_metrics.csv` | Supports Fig. 3, Fig. 6 and the main event-summary table. |
| 1000-pebble processed events | `data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable_*`; `data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_*`; `data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_*` | Supports the 1000-pebble event-sequence claims. |
| 500-pebble processed events | `data/processed/PB-006-bonded-randompack-500-*breakage_events.csv`; corresponding `*_height_summary.csv`, `*_pebble_summary.csv`, `*_per_pebble_series.csv` | Supports three-seed 500-pebble onset and growth comparison. |
| Packing and force-path proxy tables | `tables/pb006_three_seed_packing_descriptors_cutoff1p02mm.csv`; `tables/pb006_seed02_overlap_force_proxy_*`; `tables/pb006_seed03_overlap_force_proxy_*`; `tables/pb006_1000_seed02_packing_descriptors_cutoff1p02mm.csv` | Supports packing/overlap-proxy interpretation. |
| Figure files | Main figure PDFs listed in `manuscript/nuclear_fusion_submission_asset_manifest.csv`; TIFF backups retained locally for production request | Supports manuscript review while keeping the reduced package compact. |
| Reference audit | `tables/reference_crossref_audit_20260531.csv` | Documents DOI/title/year checks. |

## Code to include

| Script group | Include | Purpose |
| --- | --- | --- |
| Template generation | `scripts/generate_bonded_sphere.py`; `scripts/generate_weak_plane_template.py`; `scripts/export_liggghts_multiplespheres.py`; `scripts/generate_bonded_bed_from_centers.py` | Reconstructs bonded templates and template-in-bed input data. |
| DEM run control | `scripts/run_sp002_weakplane_case.sh`; `scripts/run_sp002_weakplane_orientation_case.sh`; `scripts/run_pb006_proxy_settle.sh`; `scripts/run_pb006_bonded_initcheck.sh`; `scripts/run_pb006_bonded_compression_targeted_window_restartable.sh` | Documents simulation launch workflow. |
| Post-processing | `scripts/extract_liggghts_thermo.py`; `scripts/analyze_bed_breakage_events.py`; `scripts/summarize_random_pack_breakage.py`; `scripts/build_pb006_event_database.py`; `scripts/analyze_pb006_packing_descriptors.py`; `scripts/analyze_pb006_overlap_force_network.py` | Rebuilds event tables and diagnostics. |
| Plotting | `scripts/plot_main_workflow_figure.py`; `scripts/plot_single_pebble_calibration_evidence.py`; `scripts/plot_sp002_force_displacement_overlay.py`; `scripts/plot_pb006_event_database.py`; `scripts/plot_pb006_1000_0p15_sequence.py`; `scripts/plot_pb006_1000_orientation_sensitivity.py`; `scripts/plot_pb006_overlap_force_proxy.py` | Recreates manuscript figures. |

## Simulation inputs to include

| Input path | Purpose |
| --- | --- |
| `simulations/pebble_bed/PB-006/in.pb006_proxy_settle.lmp` | Proxy-packing stage. |
| `simulations/pebble_bed/PB-006/in.pb006_bonded_initcheck.lmp` | Locked-template initialization check. |
| `simulations/pebble_bed/PB-006/in.pb006_bonded_compression_targeted_window_restartable.lmp` | Restartable targeted-window compression. |
| `simulations/pebble_bed/PB-006/data/proxy_centers_500*.csv` | 500-pebble packing centres. |
| `simulations/pebble_bed/PB-006/data/proxy_centers_1000*.csv` | 1000-pebble packing centres. |
| `simulations/pebble_bed/PB-006/data/bonded_template_metadata_500.csv`; `simulations/pebble_bed/PB-006/data/bonded_template_metadata_1000.csv` | Mother-pebble id, height-bin and insertion metadata. |

## Exclude from default reduced package

- Raw restart files.
- Full local-bond dump sequences not needed to regenerate processed CSVs.
- Large screen/log archives unless a reviewer requests exact run logs.
- TIFF backup figures, unless the submission system or production editor specifically requests them.
- Incomplete partial seed02 checkpoint tables, except as local provenance.

## Submission-ready Data Availability text for Nuclear Fusion

The processed event tables, figure source data, manuscript figures, DEM input files and post-processing scripts supporting this study have been assembled in a reduced reproducibility package with a checksum manifest. For submission, this package should be deposited in a persistent repository such as Zenodo, Figshare or an institutional repository, and the final DOI or stable URL should be inserted in the manuscript before upload. Large raw restart files and full local-bond dump histories are retained as local case archives and can be provided as larger audit bundles on reasonable request, subject to repository file-size limits and institutional storage constraints.

## Submission-ready Code Availability text for Nuclear Fusion

All Python and shell scripts used for bonded-template generation, random-bed construction, event extraction, post-processing and figure generation are included in the reduced reproducibility package. Compiler details and build flags should be recorded in the repository metadata before final upload.

## Repository metadata to complete before upload

- Repository: [Zenodo/Figshare/institutional repository to be selected].
- Record title: Mother-pebble-resolved fracture sequences in random Li4SiO4 breeder beds for fusion blankets by bonded-particle DEM: reduced data and scripts.
- Creators: [match manuscript author order].
- Identifier: [DOI or stable URL to be added].
- Licence: recommend CC BY 4.0 for data and MIT/BSD-compatible licence for scripts, subject to institutional approval.
- Version: v1.0-submission.
- Related publication: Nuclear Fusion submission, title as above.
