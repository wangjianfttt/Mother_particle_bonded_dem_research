# JNM material-degradation state-variable audit

Purpose: protect the Journal of Nuclear Materials framing introduced after the NF scope rejection. The paper should not read as a generic DEM movie; it should expose computed state variables for Li4SiO4 ceramic breeder-bed degradation.

## Required state variables

- event time
- damaged mother-pebble identity
- bond-loss increment
- native force connectivity
- macroscopic force relaxation

## Cross-scale mechanism chain

The state variables are useful because they connect four scales that a materials-journal reviewer can audit:

1. Internal fracture chronology: event time, damaged mother-pebble identity and bond-loss increment.
2. Mesoscale load-path environment: native force connectivity, top reachability and inter-mother force edges.
3. Macroscopic bed response: top-wall force history, peak-to-endpoint relaxation and final force-sum contrast.
4. Fusion-breeder service interpretation: contact-stiffness, heat-transfer constriction and helium purge-path implications, without solving coupled transport.

This chain is the bridge from a numerical bond graph to ceramic breeder-material degradation; it keeps the manuscript from reading as a generic granular DEM visualization.

## Mechanism indices locked by the gate

| Metric | Value | Interpretation | Boundary |
| --- | ---: | --- | --- |
| endpoint_broken_bond_fraction | 1.0132e-05 fraction | Only a very small fraction of internal bonds broke by 60 micrometres. | Use as localized microcracking evidence, not as a bed-scale damage law. |
| damaged_mother_pebble_fraction | 0.01 fraction of 100 mother pebbles | Damage is confined to one mother pebble in the corrected pilot. | Do not infer converged probability from one corrected pilot. |
| damaged_pebble_rank_from_top | 2 rank | The damaged mother pebble is top-near, but not simply the geometrically highest pebble. | Rank is case-specific and local-structure dependent. |
| inter_mother_edge_densification | 1.436 ratio | The native force graph densifies before reorganizing around the microcracking sequence. | Topology ratio is a finite-bed mechanism descriptor, not a material constant. |
| top_reachability_densification | 1.354 ratio | The top-loaded force component recruits more mother pebbles before later reorganization. | Reachability depends on bed realization and loading protocol. |
| endpoint_edge_reorganization_drop | 0.06329 fraction | The endpoint graph has fewer active inter-mother force edges than the maximum sampled state. | Use as evidence of reorganization, not monotonic damage accumulation. |
| peak_to_endpoint_force_relaxation | 0.4643 fraction | The pilot exhibits peak-to-endpoint load relaxation after event-localized bond loss. | Do not report as a quasi-static elastic modulus. |
| pilot_to_independent_final_force_sum_contrast | 3.418 ratio | The fractured pilot carries a larger final inter-pebble force sum than the intact independent bed. | This is a local force-path contrast, not a universal threshold. |
| spanning_graph_with_local_damage | yes logical | The bed remains force-connected while one mother pebble has localized internal bond loss. | Connected force graph does not imply unchanged thermal or purge-flow transport. |
| strength_audit_endpoint_broken_bonds | 0 bonds | Lowering the bond-strength multipliers in the independent bed did not trigger damage by 60 micrometres. | Do not infer that strength is irrelevant; the result shows local force-path sensitivity in this bed. |

## Event-aligned topology bridge

| Event displacement (micrometres) | New broken bonds | Inter-mother edges | Top-reachable mothers | Force-network status |
| ---: | ---: | --- | --- | --- |
| 25.0 | 2 | 55 -> 67 | 48 -> 58 | spanning before=1, after=1 |
| 35.0 | 2 | 67 -> 79 | 58 -> 65 | spanning before=1, after=1 |
| 60.0 | 1 | 67 -> 74 | 56 -> 57 | spanning before=1, after=1 |

## Evidence

- The manuscript abstract, introduction and discussion define the output as material-degradation state variables.
- The cover letter presents the same state-variable framing to the editor.
- The reviewer-risk prebuttal explains why these variables are reusable beyond a single pilot calculation.
- `tables/jnm_material_degradation_mechanism_indices.csv` fixes the quantitative bridge from localized bond loss to force-network reorganization and macroscopic relaxation.
- `tables/pb007_event_aligned_topology.csv` confirms that each event increment occurs inside a measured spanning native force graph.

## Boundary

These state variables support event-sequence and mechanism interpretation only. They are not a calibrated lifetime model, a converged fracture probability, a final Li4SiO4 constitutive law or a coupled thermal-flow prediction. The heat-transfer and purge-path language is therefore a service-relevance interpretation of contact-network degradation, not a reported transport simulation.
