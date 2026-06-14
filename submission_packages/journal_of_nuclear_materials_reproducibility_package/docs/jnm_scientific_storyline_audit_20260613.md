# JNM scientific storyline audit

This audit checks whether the active Journal of Nuclear Materials manuscript keeps the scientific argument aligned with the actual corrected-bed evidence. It is intentionally stricter than a file-presence check: it verifies that the manuscript, event tables, macro-topology metrics, native-force-network series and material-degradation indices all support the same bounded mechanism.

## Checked storyline

- The manuscript presents the study as a nuclear-materials degradation problem for Li4SiO4 ceramic breeder beds, not as a generic DEM exercise.
- The corrected pilot contains a time-ordered internal-bond-loss sequence at 25, 35 and 60 micrometres.
- The event sequence localizes in one upper-bed mother pebble, mother pebble 78, with rank from top 2.
- The endpoint pilot damage is five broken internal bonds, not bed-wide fragmentation.
- Native force-network data remain spanning during sampled pilot states while inter-mother force edges and top-reachable mother-pebble counts evolve.
- The independent corrected bed and its 0.5x and 0.25x strength-window audits remain intact to 60 micrometres while retaining spanning native force graphs.
- The event-aligned topology table links each bond-loss window to the nearest native force-network states, confirming that the recorded fracture increments occur inside measured spanning force graphs.
- The mechanism indices link small bond loss to force-network reorganization and macro-response relaxation, without converting them into failure probabilities, bulk moduli or coupled thermal-flow predictions.

## Current automated result

`python3 scripts/check_jnm_scientific_storyline.py`

Result:

`PASS scientific storyline: event sequence, macro response, native-force topology, mechanism indices and conservative boundaries are consistent`

## Data invariants enforced

| Evidence item | Required value |
| --- | --- |
| Pilot event rows | 3 |
| Pilot event displacements | 25, 35 and 60 micrometres |
| Damaged mother pebble | 78 |
| Damaged-pebble rank from top | 2 |
| Endpoint cumulative broken bonds | 5 |
| Early native-force edge sequence | 55, 67 and 79 inter-mother edges |
| Early top-reachability sequence | 48, 58 and 65 mother pebbles |
| Event-aligned 25 micrometre topology | +2 bonds; 55 -> 67 inter-mother edges; 48 -> 58 top-reachable mother pebbles; spanning before and after |
| Event-aligned 35 micrometre topology | +2 bonds; 67 -> 79 inter-mother edges; 58 -> 65 top-reachable mother pebbles; spanning before and after |
| Event-aligned 60 micrometre topology | +1 bond; 67 -> 74 inter-mother edges; 56 -> 57 top-reachable mother pebbles; spanning before and after |
| Pilot final inter-mother edges | 74 |
| Independent-bed final inter-mother edges | 83 |
| Endpoint broken-bond fraction | 1.0132e-05 |
| Inter-mother edge densification | 1.436 |
| Top-reachability densification | 1.354 |
| Peak-to-endpoint force relaxation | 0.4643 |
| Pilot/independent final force-sum contrast | 3.418 |

## Boundary enforced

The gate requires manuscript wording that frames the result as event-sequence and mechanism evidence. It explicitly protects against overclaiming a converged fracture probability, a final Li4SiO4 material law, a lifetime/design-margin prediction, or a coupled thermal-flow prediction.
