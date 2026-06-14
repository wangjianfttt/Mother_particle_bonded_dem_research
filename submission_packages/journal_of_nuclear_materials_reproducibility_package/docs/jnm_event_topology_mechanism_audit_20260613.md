# Event-aligned topology mechanism audit

This audit connects the localized internal-bond-loss events used in Fig. 5 and Table 1 to the nearest native force-network states. It is generated from `tables/pb007_event_aligned_topology.csv` and `tables/jnm_material_degradation_mechanism_indices.csv`; no additional data are inferred.

## Event sequence and force-network state

| Event | Displacement (um) | New broken bonds | Mother pebble | Rank from top | Inter-mother edges before -> after | Top-reachable mothers before -> after | Inter-pebble force sum before -> after (N) | Spanning graph |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | 25.0 | 2 | 78 | 2 | 55 -> 67 (Delta 12) | 48 -> 58 (Delta 10) | 0.542 -> 0.389 | 1 -> 1 |
| 2 | 35.0 | 2 | 78 | 2 | 67 -> 79 (Delta 12) | 58 -> 65 (Delta 7) | 0.389 -> 1.04 | 1 -> 1 |
| 3 | 60.0 | 1 | 78 | 2 | 67 -> 74 (Delta 7) | 56 -> 57 (Delta 1) | 0.675 -> 0.864 | 1 -> 1 |

## Mechanistic interpretation

- All three localized bond-loss increments occur in mother pebble 78, a top-near pebble with rank-from-top 2.
- The native force graph is already spanning before every localized event and remains spanning after every localized event.
- The first two event windows coincide with recruitment of additional inter-mother force edges and top-reachable mother pebbles, whereas the final event occurs after a partial network reorganization.
- The endpoint broken-bond fraction remains small, but the event windows are embedded in measurable force-network densification and load redistribution.

## Quantitative mechanism indices

| Metric | Value | Interpretation | Boundary |
| --- | ---: | --- | --- |
| endpoint_broken_bond_fraction | 1.0132e-05 | Only a very small fraction of internal bonds broke by 60 micrometres. | Use as localized microcracking evidence, not as a bed-scale damage law. |
| damaged_mother_pebble_fraction | 0.01 | Damage is confined to one mother pebble in the corrected pilot. | Do not infer converged probability from one corrected pilot. |
| inter_mother_edge_densification | 1.436 | The native force graph densifies before reorganizing around the microcracking sequence. | Topology ratio is a finite-bed mechanism descriptor, not a material constant. |
| top_reachability_densification | 1.354 | The top-loaded force component recruits more mother pebbles before later reorganization. | Reachability depends on bed realization and loading protocol. |
| endpoint_edge_reorganization_drop | 0.06329 | The endpoint graph has fewer active inter-mother force edges than the maximum sampled state. | Use as evidence of reorganization, not monotonic damage accumulation. |
| peak_to_endpoint_force_relaxation | 0.4643 | The pilot exhibits peak-to-endpoint load relaxation after event-localized bond loss. | Do not report as a quasi-static elastic modulus. |
| pilot_to_independent_final_force_sum_contrast | 3.418 | The fractured pilot carries a larger final inter-pebble force sum than the intact independent bed. | This is a local force-path contrast, not a universal threshold. |
| spanning_graph_with_local_damage | yes | The bed remains force-connected while one mother pebble has localized internal bond loss. | Connected force graph does not imply unchanged thermal or purge-flow transport. |

## Claim boundary

This audit supports a bounded materials-degradation mechanism: early breeder-pebble microcracking can be localized while the native contact-force network remains globally connected and reorganizes. It does not establish a converged fracture probability, a bulk elastic modulus, a blanket lifetime estimate or a coupled thermal-flow prediction.
