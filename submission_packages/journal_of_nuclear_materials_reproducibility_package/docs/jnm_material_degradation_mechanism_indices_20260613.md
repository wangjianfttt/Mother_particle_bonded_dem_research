# JNM material-degradation mechanism indices

This audit converts the corrected PB-007 fracture and native-force outputs into bounded material-degradation descriptors for the Journal of Nuclear Materials manuscript. It does not introduce new simulation results; every index is recomputed from existing processed event, thermo and native-force data.

| Metric | Value | Unit | Interpretation | Boundary |
| --- | ---: | --- | --- | --- |
| endpoint_broken_bond_fraction | 1.0132e-05 | fraction | Only a very small fraction of internal bonds broke by 60 micrometres. | Use as localized microcracking evidence, not as a bed-scale damage law. |
| damaged_mother_pebble_fraction | 0.01 | fraction of 100 mother pebbles | Damage is confined to one mother pebble in the corrected pilot. | Do not infer converged probability from one corrected pilot. |
| damaged_pebble_rank_from_top | 2 | rank | The damaged mother pebble is top-near, but not simply the geometrically highest pebble. | Rank is case-specific and local-structure dependent. |
| inter_mother_edge_densification | 1.436 | ratio | The native force graph densifies before reorganizing around the microcracking sequence. | Topology ratio is a finite-bed mechanism descriptor, not a material constant. |
| top_reachability_densification | 1.354 | ratio | The top-loaded force component recruits more mother pebbles before later reorganization. | Reachability depends on bed realization and loading protocol. |
| endpoint_edge_reorganization_drop | 0.06329 | fraction | The endpoint graph has fewer active inter-mother force edges than the maximum sampled state. | Use as evidence of reorganization, not monotonic damage accumulation. |
| peak_to_endpoint_force_relaxation | 0.4643 | fraction | The pilot exhibits peak-to-endpoint load relaxation after event-localized bond loss. | Do not report as a quasi-static elastic modulus. |
| pilot_to_independent_final_force_sum_contrast | 3.418 | ratio | The fractured pilot carries a larger final inter-pebble force sum than the intact independent bed. | This is a local force-path contrast, not a universal threshold. |
| spanning_graph_with_local_damage | yes | logical | The bed remains force-connected while one mother pebble has localized internal bond loss. | Connected force graph does not imply unchanged thermal or purge-flow transport. |
| strength_audit_endpoint_broken_bonds | 0 | bonds | Lowering the bond-strength multipliers in the independent bed did not trigger damage by 60 micrometres. | Do not infer that strength is irrelevant; the result shows local force-path sensitivity in this bed. |

Primary inputs:
- `tables/pb007_macro_topology_event_metrics.csv`
- `tables/pb007_event_aligned_topology.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv`
- `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_force_network_series.csv`

Event-aligned topology support:

| Event displacement (micrometres) | New broken bonds | Previous -> next inter-mother edges | Previous -> next top-reachable mother pebbles | Force-sum ratio |
| ---: | ---: | ---: | ---: | ---: |
| 25 | 2 | 55 -> 67 | 48 -> 58 | 0.719 |
| 35 | 2 | 67 -> 79 | 58 -> 65 | 2.678 |
| 60 | 1 | 67 -> 74 | 56 -> 57 | 1.280 |

The intended manuscript use is mechanistic: localized internal bond loss can coexist with a spanning native force graph and a reorganizing contact topology. The event-aligned table shows that each recorded bond-loss increment sits inside a measured spanning force network rather than outside the validated load path. The indices should not be used as converged failure probabilities, bulk elastic moduli, or coupled heat-flow/purge-flow predictions.
