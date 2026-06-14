# Figure captions for the Journal of Nuclear Materials submission

This file is an author-facing caption and source-data companion. The wording below is aligned with the active JNM manuscript and avoids reader-facing internal run labels.

## Graphical abstract

Acceptance-gated bonded-template workflow for resolving localized fracture events in Li4SiO4 ceramic breeder beds. The visual summarizes the intact 500-subparticle mother-pebble template, zero-pre-damage insertion into a gravity-settled bed, native force-network validation and mother-pebble-resolved fracture-event extraction. The message is intentionally bounded: the workflow provides auditable fracture-event and force-network histories for ceramic breeder-material degradation, not a converged blanket design-margin prediction.

Display files:

- `figures/main/journal_of_nuclear_materials_graphical_abstract.png`
- `figures/main/journal_of_nuclear_materials_graphical_abstract.pdf`
- `figures/main/journal_of_nuclear_materials_graphical_abstract.tiff`

## Fig. 1 | Locked-template workflow for fracture-resolved Li4SiO4 breeder-bed compression.

A nominal 1 mm mother pebble is represented by a 500-subparticle bonded template. Proxy spheres first settle under gravity without internal bonds. The settled proxy centres are then replaced by intact bonded templates, so internal bond failure is absent during bed formation and is activated only during compression. The corrected route adds explicit acceptance gates: zero internal-bond loss before loading, native mother-mother force connectivity, six-wall force output and gravity-baseline-corrected incremental force balance. Bond-state records are converted into a mother-pebble-resolved fracture-event database.

Display file:

- `figures/main/fig1_workflow.png`

## Fig. 2 | Single-pebble calibration evidence for the current 500-subparticle template.

In panels b and c, "homogeneous" denotes a uniform-bond-strength template, "selected template" denotes the x-normal weak-plane calibration candidate, "orthogonal" denotes weak-plane orientation variants, "strength multiplier" denotes deterministic bond-strength scaling, and "Weibull trial" denotes a stochastic strength sample. The selected weak-plane template lies in the provisional 1 mm crush-load target window and preserves a two-major-fragment mode, but it is treated as a current calibration candidate rather than a final Li4SiO4 material law. The load window and interpretation are anchored to published Li4SiO4 crush and elastic-response studies.

Display files:

- `figures/sp002/single_pebble_calibration_evidence.svg`
- `figures/sp002/single_pebble_calibration_evidence.pdf`
- `figures/sp002/single_pebble_calibration_evidence.png`
- `figures/sp002/single_pebble_calibration_evidence.tiff`

Traceable source files:

- `tables/single_pebble_calibration_target_evidence_summary.csv`
- `tables/single_pebble_model_ensemble_evidence_summary.csv`

## Fig. 3 | Subparticle-resolution and loading-rate sensitivity of the single-pebble template.

Panel a shows force-displacement curves for 250, 500 and 1000 subparticles. Panel b compares peak load and first-break displacement normalized by the 500-subparticle result. Panel c shows matched-boundary force-displacement curves at 0.10, 0.05 and 0.03 m s-1. Panel d reports final largest- and second-largest-fragment fractions across loading rates. Onset and split topology are robust, whereas peak load retains moderate resolution and rate sensitivity.

Display files:

- `figures/sp002/jnm_single_pebble_validation.svg`
- `figures/sp002/jnm_single_pebble_validation.pdf`
- `figures/sp002/jnm_single_pebble_validation.png`

Traceable source files:

- `tables/jnm_single_pebble_resolution_summary.csv`
- `tables/jnm_single_pebble_rate_summary.csv`

## Fig. 4 | Corrected pre-damage force-transmission validation.

The corrected route validates the 100-mother-pebble bed before fracture interpretation. Panel a shows relaxed endpoint top-wall force and gravity-baseline-corrected six-wall incremental force during the accepted 5 micrometre entry protocol; faint traces show within-step relaxation. Panel b shows the incremental force-balance residual at relaxed endpoints, with the final value entering the 5% gate. Panel c confirms zero internal-bond damage throughout the entry protocol. Panel d gives the native final-state force-network gate.

Display files:

- `figures/pb007/pb007_acceptance_gate_validation.png`
- `figures/pb007/pb007_acceptance_gate_validation.pdf`
- `figures/pb007/pb007_acceptance_gate_validation.svg`

Traceable source files:

- `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_acceptance_summary.csv`
- `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_summary.csv`

## Fig. 5 | Corrected fracture-event sequence and native force-network evolution.

Panel a shows the top-wall force and mother-pebble-resolved event windows during the 60 micrometre corrected compression pilot. Panel b shows cumulative internal-bond loss from the thermo history with event-window localization; all localized events occur in mother pebble 78. Panel c reports native inter-mother force-network topology at sampled displacements, showing a spanning graph that densifies and then reorganizes. Panel d identifies the damaged mother pebble as a top-near but not geometrically highest pebble. No error bars are shown because this is one corrected pilot sequence, not an ensemble statistic.

Display files:

- `figures/pb007/pb007_corrected_fracture_sequence.svg`
- `figures/pb007/pb007_corrected_fracture_sequence.pdf`
- `figures/pb007/pb007_corrected_fracture_sequence.png`

Traceable source files:

- `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_bond_series.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_force_network_series.csv`
- `tables/pb007_event_aligned_topology.csv`

## Fig. 6 | Corrected-case comparison separates force connectivity from fracture onset.

Panel a compares top-wall force histories for the corrected pilot, an intact independent corrected bed, a third independent corrected bed with delayed microcracking and the 0.5x and 0.25x bond-strength audits of the intact bed. Panel b shows event-localized cumulative internal-bond loss: the pilot loses five bonds in one upper-bed mother pebble, the intact bed and its weakened-bond audits remain undamaged to 60 micrometres and the third bed loses ten bonds near the endpoint in two upper-bed mother pebbles. Panel c reports native inter-mother force edges and top-reachable mother-pebble counts for the pilot, intact independent bed and delayed-cracking third bed. Panel d gives an endpoint mechanism fingerprint, with each metric normalized to its own maximum across corrected cases and labelled with the pilot, intact-bed and delayed-bed values. All corrected cases retain a spanning native force graph at the endpoint, but only two of the three independent bed geometries develop internal bond loss, indicating local force-path sensitivity rather than a deterministic displacement-only or bond-strength-multiplier threshold.

Display files:

- `figures/pb007/pb007_replicate_comparison.svg`
- `figures/pb007/pb007_replicate_comparison.pdf`
- `figures/pb007/pb007_replicate_comparison.png`

Traceable source files:

- `data/processed/pb007_replicate_comparison_source_data.csv`
- `tables/pb007_macro_topology_event_metrics.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_thermo.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_bond_series.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_breakage_events.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-seed03-600ksettle-y1p5e10-10krelax-60um-nohold-fracture-seed03_native_force_network_series.csv`

## Supplementary Fig. S1 | Single-pebble fragment morphology.

Final morphology of the matched-rate single-pebble rerun at 0.30 mm displacement, rendered from particle positions and intact-bond records. The 500 subparticles are coloured by final intact-bond connected component: largest fragment, second-largest fragment and smaller fragments. Semi-transparent tubes show the remaining intact internal bonds. The final graph contains 5335 intact bonds and 40 fragments, with the two largest fragments containing 236 and 226 subparticles.

Display and source files:

- `figures/sp002/single_pebble_fragment_morphology_paraview.png`
- `figures/sp002/single_pebble_fragment_particles.vtp`
- `figures/sp002/single_pebble_fragment_bonds.vtp`
- `tables/sp002_single_pebble_fragment_visualization_summary.csv`

## Supplementary Fig. S2 | Force-displacement overlay for the selected weak-plane template.

The selected weak-plane reference, matched-rate rerun and slower onset check are compared against the provisional 1 mm load target window and a near-size literature displacement/load anchor. The 0.10 and 0.05 m s-1 traces first lose internal bonds at 0.1025 mm, while the 0.03 m s-1 short run first breaks at 0.10245 mm and is not used for peak-load comparison because it stops at 0.18 mm. The panel supports template-level calibration screening but not a final Li4SiO4 material law.

Display and source files:

- `figures/sp002/sp002_force_displacement_overlay.svg`
- `figures/sp002/sp002_force_displacement_overlay.pdf`
- `figures/sp002/sp002_force_displacement_overlay.png`
- `figures/sp002/sp002_force_displacement_overlay.tiff`
- `tables/sp002_force_displacement_overlay_metrics.csv`
