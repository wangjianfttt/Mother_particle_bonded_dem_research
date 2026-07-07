# Repaired manuscript evidence status

Date: 2026-07-04

This file separates manuscript-ready evidence from running observations and missing evidence after the APT editorial rejection. It is generated from current source tables and should be refreshed whenever PB-007 material-matrix cases complete.

## Current computed status

- Macro/topology endpoint rows: 9
- Completed cracking endpoint rows: 4
- Completed intact or zero-loss endpoint rows: 5
- Larger-bed endpoint rows: 2
- Larger-bed intact comparison rows: 2
- Material-response completed rows: 11
- Material-response running rows: 0
- Progress rows with log-derived bond loss: 6
- Postprocessed material-matrix rows: 6
- Postprocessed material-matrix rows with endpoint bond loss: 6
- Material matrix complete: yes
- Latest maximum matrix displacement inspected: 60.0 micrometres

## Claim evidence matrix

| Claim | Status | Evidence | Boundary | Next action |
| --- | --- | --- | --- | --- |
| C1: The 500-subparticle weak-plane bonded template reproduces the intended 1 mm crush-load scale and split-type fragment mode within the tested sensitivity range. | manuscript_ready | tables/single_pebble_model_calibration_matrix.csv; tables/sp002_strength_multiplier_validation.csv; tables/sp002_weibull_ensemble_completed_summary.csv; figures/apt_redesign/fig2_single_pebble_template_validation.* | Describe as a calibrated template candidate and sensitivity-bounded representation, not a final Li4SiO4 material law. | Keep current wording conservative and link it to the completed strength-matrix section. |
| C2: The locked-template transfer creates a pre-fracture bed with zero internal-bond loss, measurable force transmission and a connected native force graph. | manuscript_ready | tables/pb007_*_acceptance_summary.csv; tables/pb007_*_native_summary.csv; figures/apt_redesign/fig3_entry_state_validation.* | Use as entry-state validation for selected 100-parent-particle windows only. | Reuse in revised Methods/Results; do not add stronger quasi-static claims. |
| C3: Corrected finite-window beds reveal localized fracture-event sequences and zero-loss controls embedded in spanning inter-particle force networks. | manuscript_ready | tables/pb007_macro_topology_event_metrics.csv; tables/pb007_event_aligned_topology.csv; tables/pb007_mechanism_indices.csv; figures/apt_redesign/fig4_pilot_fracture_event_sequence.*; figures/apt_redesign/fig5_mechanism_state_space.* | Frame as finite-window event-sequence and intact-comparison evidence, not converged fracture probability. | Retain as the central result and combine it with the completed material-matrix response. |
| C4: Bond-strength reduction shifts the fracture-onset response differently in early-cracking and synchronous-cracking random geometries. | manuscript_ready | tables/pb007_material_parameter_matrix_20260704.csv; tables/pb007_material_parameter_response.csv; tables/pb007_material_strength_matrix_summary.csv; data/figure_source/pb007_material_strength_response.csv; figures/pb007/pb007_material_strength_response.* | Use as finite-window material-strength evidence across two cracking geometries; do not present as a universal strength law. | Integrate into the Results strength-matrix section and rebuild the final figure/caption. |
| C5: Random packing topology and material strength jointly control whether local microcracking appears before the 60 micrometre endpoint. | manuscript_ready | tables/pb007_macro_topology_event_metrics.csv; tables/pb007_material_parameter_response.csv; tables/pb007_mechanism_variable_separation.csv; data/figure_source/pb007_mechanism_variable_separation.csv | State as finite-window topology and strength interaction evidence, not converged stochastic failure probability. | Write the synthesis around geometry-specific onset shifts and endpoint bond-loss changes. |
| C6: The repaired paper provides expanded random-geometry and scale-check evidence rather than isolated case reporting. | partial | tables/pb007_rescue_case_status_summary_20260704.csv; tables/pb007_macro_topology_event_metrics.csv | Do not call this a converged stochastic ensemble; describe as expanded finite-window evidence with two larger-bed intact endpoint comparisons. | Add another larger-bed cracking or near-onset case only if the next target journal demands scale robustness beyond the present bounded claim. |
| C7: The event-sequence variables can support future transport, permeability or thermal-contact degradation models. | future_work_only | none for coupled transport in the current project | Mention only as future coupling or implication; do not claim transport prediction. | Optional later: design reduced permeability/thermal-contact calculation after mechanical evidence is complete. |
| C8: The repaired workflow is reproducible and cloud-safe after moving large raw archives to local/NAS storage. | support_ready | docs/local_vs_nas_storage_policy.md; docs/nas_raw_dump_archive_20260704_164309.md; docs/nas_offload_large_raw_outputs_before_20260704_20260704.md; docs/nas_offload_manifests/*; scripts/offload_large_dem_archives_to_nas.py | Use for internal reproducibility/storage management, not as a scientific result. | Keep submission package compact; offload old raw dumps after postprocessing when safe. |

## Manuscript rule

The next submission draft should promote only `manuscript_ready` and `support_ready` rows into firm conclusions. `partial` rows can shape the planned argument but require additional independent beds or a deliberately bounded claim before they become final claims.
