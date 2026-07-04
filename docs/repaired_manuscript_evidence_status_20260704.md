# Repaired manuscript evidence status

Date: 2026-07-04

This file separates manuscript-ready evidence from running observations and missing evidence after the APT editorial rejection. It is generated from current source tables and should be refreshed whenever PB-007 material-matrix cases complete.

## Current computed status

- Macro/topology endpoint rows: 7
- Completed cracking endpoint rows: 4
- Completed intact or zero-loss endpoint rows: 3
- Material-response completed rows: 11
- Material-response running rows: 0
- Progress rows with log-derived bond loss: 6
- Completed material-matrix rows with log-derived bond loss: 6
- Material-matrix rows with final restart available: 6
- Material matrix complete: yes
- Latest maximum matrix displacement inspected: 60.0 micrometres

## Claim evidence matrix

| Claim | Status | Evidence | Boundary | Next action |
| --- | --- | --- | --- | --- |
| C1: The 500-subparticle weak-plane bonded template reproduces the intended 1 mm crush-load scale and split-type fragment mode within the tested sensitivity range. | manuscript_ready | tables/single_pebble_model_calibration_matrix.csv; tables/sp002_strength_multiplier_validation.csv; tables/sp002_weibull_ensemble_completed_summary.csv; figures/apt_redesign/fig2_single_pebble_template_validation.* | Describe as a calibrated template candidate and sensitivity-bounded representation, not a final Li4SiO4 material law. | Keep current wording conservative and link it to the completed strength-matrix section. |
| C2: The locked-template transfer creates a pre-fracture bed with zero internal-bond loss, measurable force transmission and a connected native force graph. | manuscript_ready | tables/pb007_*_acceptance_summary.csv; tables/pb007_*_native_summary.csv; figures/apt_redesign/fig3_entry_state_validation.* | Use as entry-state validation for accepted 100-particle windows only. | Reuse in revised Methods/Results; do not add stronger quasi-static claims. |
| C3: Corrected 100-particle beds reveal localized fracture-event sequences embedded in a spanning inter-particle force network. | manuscript_ready | tables/pb007_macro_topology_event_metrics.csv; tables/pb007_event_aligned_topology.csv; tables/pb007_mechanism_indices.csv; figures/apt_redesign/fig4_pilot_fracture_event_sequence.*; figures/apt_redesign/fig5_mechanism_state_space.* | Frame as event-sequence evidence from finite 100-particle windows, not converged fracture probability. | Retain as the central result and combine it with the completed material-matrix response. |
| C4: Bond-strength reduction shifts the fracture-onset response differently in early-cracking and synchronous-cracking random geometries. | manuscript_ready | tables/pb007_material_parameter_matrix_20260704.csv; tables/pb007_material_parameter_response.csv; tables/pb007_material_strength_matrix_summary.csv; data/figure_source/pb007_material_strength_response.csv; figures/pb007/pb007_material_strength_response.* | Use as finite-window material-strength evidence across two cracking geometries; do not present as a universal strength law. | Integrate into the Results strength-matrix section and rebuild the final figure/caption. |
| C5: Random packing topology and material strength jointly control whether local microcracking appears before the 60 micrometre endpoint. | manuscript_ready | tables/pb007_macro_topology_event_metrics.csv; tables/pb007_material_parameter_response.csv; tables/pb007_mechanism_variable_separation.csv; data/figure_source/pb007_mechanism_variable_separation.csv | State as finite-window topology and strength interaction evidence, not converged stochastic failure probability. | Write the synthesis around geometry-specific onset shifts and endpoint bond-loss changes. |
| C6: The repaired paper provides stochastic geometry evidence rather than isolated case reporting. | partial | tables/pb007_rescue_case_status_summary_20260704.csv; tables/pb007_macro_topology_event_metrics.csv | Do not call this a converged stochastic ensemble; describe as expanded independent-bed evidence. | Add more independent gate-passing beds after current six LIGGGHTS runs finish or free CPU capacity. |
| C7: The event-sequence variables can support future transport, permeability or thermal-contact degradation models. | future_work_only | none for coupled transport in the current project | Mention only as future coupling or implication; do not claim transport prediction. | Optional later: design reduced permeability/thermal-contact calculation after mechanical evidence is complete. |
| C8: The repaired workflow is reproducible and cloud-safe after moving large raw archives to local/NAS storage. | support_ready | docs/local_vs_nas_storage_policy.md; docs/nas_raw_dump_archive_20260704_164309.md; docs/nas_offload_large_raw_outputs_before_20260704_20260704.md; docs/nas_offload_manifests/*; scripts/offload_large_dem_archives_to_nas.py | Use for internal reproducibility/storage management, not as a scientific result. | Keep submission package compact; offload old raw dumps after postprocessing when safe. |
| C9: The CPM retargeting now has an explicit literature-gap map linking prior single-particle, packed-bed, force-network, replacement and bonded-particle studies to the present evidence chain. | support_ready | docs/cpm_literature_gap_map_20260704.md; docs/cpm_literature_gap_map_20260704.csv; scripts/build_cpm_literature_gap_map.py | Use to keep the Introduction and cover letter focused; do not turn the map into an overlong literature survey. | Refresh after any major reference or target-journal change. |
| C10: The CPM package has an explicit reviewer-risk preflight matrix linking likely concerns to evidence and claim boundaries. | support_ready | docs/cpm_reviewer_risk_preflight_20260704.md; docs/cpm_reviewer_risk_preflight_20260704.csv; scripts/build_cpm_reviewer_risk_preflight.py; scripts/check_cpm_reviewer_risk_preflight.py | Use as internal submission support, not as reader-facing manuscript text. | Refresh before any new target-journal transfer or after adding new simulations. |
| C11: The CPM material-response argument has a source-backed summary quantifying endpoint rows, strength-matrix scope, geometry-specific onset response and force-path separation. | support_ready | docs/cpm_material_response_summary_20260704.md; docs/cpm_material_response_summary_20260704.csv; scripts/build_cpm_material_response_summary.py; tables/pb007_material_parameter_response.csv | Use to support material-property dependence in the current finite-window dataset; do not present as converged fracture probability. | Regenerate after any new material-parameter simulations or endpoint-table changes. |

## Manuscript rule

The next submission draft should promote only `manuscript_ready` and `support_ready` rows into firm conclusions. `partial` rows can shape the planned argument but require additional independent beds or a deliberately bounded claim before they become final claims.
