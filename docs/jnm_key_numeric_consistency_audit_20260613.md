# JNM key numeric-consistency audit

Purpose: verify that the headline numbers used in the active Journal of Nuclear Materials manuscript are reproduced from processed evidence files rather than copied manually without traceability.

## Checked sources

- Manuscript: `manuscript/journal_of_nuclear_materials_submission_draft.md`
- Pilot breakage events: `data/processed/PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_breakage_events.csv`
- Pilot acceptance summary: `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_acceptance_summary.csv`
- Pilot native-force summary: `tables/pb007_PB-007-bonded-steprelaxed-100-pilot-y1p5e10-10krelax-60um-fracture-pilot_native_summary.csv`
- Corrected-case macro/topology metrics: `tables/pb007_macro_topology_event_metrics.csv`
- Mechanism indices: `tables/jnm_material_degradation_mechanism_indices.csv`

## Headline numbers

| Manuscript number | Evidence value | Source | Interpretation boundary |
| --- | --- | --- | --- |
| Initial internal bonds: 493,500 | 493,500 | Pilot acceptance summary | Required intact-bond count for 100 mother pebbles before compression. |
| Final intact internal bonds: 493,495 | 493,495 | Pilot acceptance summary | Five lost bonds in the corrected pilot, not bed-wide fragmentation. |
| Pilot event displacements: 25, 35 and 60 micrometres | 25, 35, 60 micrometres | Pilot breakage-event table | Three localized event increments, not a continuous damage law. |
| Pilot event increments: +2, +2 and +1 | +2, +2, +1 broken bonds | Pilot breakage-event table | Event-localized bond loss in one mother pebble. |
| Damaged mother: mother pebble 78 | 78 | Pilot breakage-event table | Case-specific location, not a universal initiation site. |
| Damaged height rank: rank from top 2 | 2 | Pilot breakage-event table | Top-near but not geometrically highest. |
| Pilot final native force edges: 74 inter-mother edges | 74 | Pilot native-force summary | Spanning graph remains after localized damage. |
| Pilot final inter-pebble subcontacts: 119 inter-pebble subcontacts | 119 | Pilot native-force summary | Native force-contact count, not overlap proxy. |
| Pilot final top reachability: 57 mother pebbles reachable | 57 | Pilot native-force summary | Force-graph reachability descriptor. |
| Pilot final bottom reachability: 11 bottom-contacting mother pebbles | 11 | Pilot native-force summary | Top-to-bottom load-path evidence. |
| Peak-to-endpoint force relaxation: 46.4% | 0.4643 | Mechanism-index table | Macro-response signature, not elastic modulus. |
| Inter-mother edge densification: 1.44x | 1.436 | Mechanism-index table | Finite-bed topology descriptor. |
| Top-reachability densification: 1.35x | 1.354 | Mechanism-index table | Finite-bed topology descriptor. |
| Independent-bed final force edges: 83 inter-mother edges | 83 | Corrected-case macro/topology metrics | Intact independent bed still has a spanning native graph. |
| Independent-bed bottom reachability: 18 bottom-contacting mother pebbles | 18 | Corrected-case macro/topology metrics | Supports load-path sensitivity rather than no-contact artefact. |
| Independent-bed strength audits: 0.5x and 0.25x | 0 endpoint broken bonds in both audits | Corrected-case macro/topology metrics | Negative strength-window audits, not proof that strength is irrelevant. |

## Audit result

The active manuscript uses these numbers with conservative interpretation: the corrected pilot gives localized event-sequence evidence, while the independent bed and 0.5x/0.25x audits show local force-path sensitivity. The manuscript should retain the phrase "not a converged fracture probability" or equivalent wording wherever these numbers are summarized.
