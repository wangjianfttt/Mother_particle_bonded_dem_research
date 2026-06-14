# Mother-pebble-resolved fracture modelling of Li4SiO4 breeder beds: corrected bonded-template validation route

Target journal: Journal of Nuclear Materials

Status: PB-007 revision draft skeleton. Not submission-ready until PB-007 pre-damage force-balance and corrected fracture-sequence calculations pass the gates in `docs/jnm_revision_gate_after_pb006_audit_20260612.md`.

## Provisional title

Surface-supported bonded-template DEM for fracture-resolved Li4SiO4 breeder-pebble beds

## Abstract placeholder

Lithium orthosilicate pebbles are ceramic breeder materials whose fracture can alter contact topology, bed stiffness, heat-transfer paths and purge-gas access in solid breeder blankets. This study develops a bonded-template DEM route for resolving mother-pebble-level fracture events while preventing artificial pre-damage during bed formation. A 500-subparticle single-pebble template is first evaluated against crush-load scale, first-break displacement, split morphology, resolution sensitivity and loading-rate sensitivity. A surface-supported template then improves directional support for proxy-to-template transfer. Rigid-clump gravity settling followed by bonded-template transfer is used to form a mechanically connected random bed. Before any fracture sequence is interpreted, the corrected bed must satisfy zero internal-bond loss, native mother-mother contact-force connectivity, six-wall force output and gravity-baseline-corrected incremental force balance. The PB-006 calculations are retained only as a diagnostic of why these acceptance gates are necessary. The final Results section will be completed only after PB-007 passes the pre-damage validation and corrected compression-fracture calculations.

## 1. Introduction skeleton

- Li4SiO4 breeder pebbles provide tritium-generating ceramic inventory while also defining load-bearing, thermal and purge-flow pathways in solid breeder blankets.
- Fracture and fragment generation can change contact topology, local stiffness, thermal conductance and helium pressure-drop pathways.
- Experiments provide crush load, bed compression and breakage-ratio evidence, but cannot directly resolve the hidden time order of mother-pebble fracture inside an opaque bed.
- Rigid-particle DEM and crush-probability approaches describe bulk response or failure likelihood, but do not directly provide mother-pebble-resolved fracture-event sequences.
- Bonded-particle DEM can resolve subparticle bond loss, but only if the bonded mother pebble is inserted into the bed without pre-damage and with a mechanically connected load path.
- This work therefore frames the contribution as a validated workflow with explicit acceptance gates, not as a final Li4SiO4 lifetime law.

## 2. Results skeleton

### 2.1 Single-pebble calibration candidate

Use current Fig. 2/Fig. 3 evidence and conservative language:

- 500-subparticle weak-plane template matches the target load scale and two-major-fragment morphology as a current calibration candidate.
- 250/500/1000-subparticle and 0.03-0.10 m s-1 checks bound onset, morphology and peak-load sensitivity.
- Keep Supplementary Fig. S1 as morphology evidence.

### 2.2 Surface-supported template for bed insertion

Use `tables/jnm_surface_resolved_template_validation.csv`:

- random-core reference directional support is insufficient for proxy replacement;
- surface-supported candidate improves q05/median/q95 directional diameter to 0.99355/0.99639/0.99889 mm;
- single-pebble first break and peak load remain close to the reference scale;
- final fragments remain split-type with two dominant pieces of 220 and 213 subparticles.

### 2.3 Corrected random-bed initialization by rigid-clump settling

Use `tables/pb007_rigid_surface_100_settle_summary.csv` and bonded-transfer metadata:

- 100 mother pebbles, 50,000 subparticles after transfer;
- 164 inter-pebble geometric/native candidate edges after rigid settling;
- largest component 99/100;
- 27 bottom-contacting pebbles;
- transferred bonded coordinates reproduce the rigid dump at nanometre-scale precision;
- initial internal-bond count is exactly 493,500 = 100 x 4,935.

### 2.4 Pre-damage force-transmission acceptance gate

The corrected bed was first compressed by five 1 micrometre step-relaxation increments before any fracture-sequence result was interpreted. The purpose of this stage was to test whether the bonded-template bed could transmit load through a native mother-pebble contact graph while retaining zero internal-bond damage. Because the bottom wall already carries bed self-weight after gravity settling, the relevant balance metric is not the raw top/bottom force ratio. Instead, the last zero-top-force state was used as a gravity baseline, and the top-wall load was compared with the increment in total six-wall vertical force.

The 100-mother-pebble pilot passed this pre-damage gate at 5 micrometres of top-wall displacement. The top-wall load was 1.713e-4 N, while the gravity-baseline-corrected six-wall incremental force was 1.704e-4 N, giving a force-balance residual of 0.542%. The intact internal-bond count remained 493,500 throughout the run and no broken internal bonds were reported. Native local-contact output at the final state contained 165 mother-mother force edges and 298 inter-pebble subcontacts; the top-loaded set reached 99 of 100 mother pebbles and 26 bottom-contacting pebbles. These results establish a zero-pre-damage, load-bearing starting protocol for the subsequent corrected fracture-sequence calculation.

The corresponding data products are `tables/pb007_bonded_steprelaxed_100_5um_acceptance_summary.csv`, `tables/pb007_bonded_steprelaxed_100_5um_native_summary.csv` and `figures/pb007/pb007_step_relaxed_validation_5um.png`. This section should be converted from draft prose to final manuscript prose only after the fracture-sequence figure is also available.

A direct stiffness-restoration check shows why an additional gate is required before the fracture run. When the same zero-displacement bed was switched directly to the single-pebble contact modulus of 9.0e10 Pa, 14 internal bonds were lost without top-wall compression. A short contact-modulus screen then identified zero pre-damage at 5.0e8, 5.0e9 and 2.0e10 Pa, but spurious bond loss at 3.0e10 and 5.0e10 Pa. These checks are recorded in `tables/pb007_stiffness_restore_young_screen.csv` and are treated as protocol tests, not physical fracture events. The corrected fracture sequence should therefore begin from a zero-damage restored stiffness, currently bounded by the 2.0e10 Pa screened pilot unless a graded restoration protocol is introduced.

At 2.0e10 Pa, a short 5 micrometre compression pilot retained all 493,500 internal bonds. This confirms zero pre-damage under short compression at the screened stiffness, but it is not yet a final force-transmission result because the restored high-stiffness bed continues to relax a large initial wall-force state. Extending the pre-compression relaxation to 10,000 steps substantially improved the balance metric while preserving zero damage. At 5 micrometres, the restored-stiffness pilot gave a top-wall load of 1.084e-2 N and a gravity-baseline-corrected six-wall incremental force of 1.023e-2 N, corresponding to a final residual of 5.595%. Native final-state output retained a spanning mother-pebble force graph, but only 25 mother-mother force edges were active. Longer hold times, slower step-relaxed loading and a corrected continuous-compression pilot all retained zero damage, but did not improve the final force-balance gate because the small restored-stiffness bed undergoes contact-network oscillation between top-wall loading and bottom/side-wall reaction. These cases are therefore treated as protocol-development results rather than fracture evidence.

Reducing the restored contact modulus to 1.5e10 Pa while retaining the 10,000-step pre-compression relaxation and five 1 micrometre step-relaxation increments provides the current gate-passing corrected-fracture entry protocol. At 5 micrometres, the final top-wall load was 1.638e-2 N and the gravity-baseline-corrected six-wall incremental force was 1.559e-2 N, giving a final balance residual of 4.799%. All 493,500 internal bonds remained intact. The native final-state force graph contained 36 mother-mother edges; the top-loaded set reached 28 mother pebbles and 3 bottom-contacting pebbles, so the load-bearing graph remained spanning. This result is used only to define the next corrected fracture-sequence pilot and is not interpreted as a final Li4SiO4 contact law.

### 2.5 Corrected fracture-event sequence

The corrected 60 micrometre compression pilot was then launched from the 1.5e10 Pa gate-passing entry protocol with periodic local internal-bond dumps and native pair/wall contact dumps. The run completed without restart continuation. At the final displacement, 493,495 of 493,500 internal bonds remained intact; the five lost bonds were not distributed through the bed but were confined to one top-near mother pebble, pebble 78 (`pebble_z_mm=2.96658`, rank from top 2). The mother-pebble event table records three event increments: two lost internal bonds at 25 micrometres, two additional lost bonds at 35 micrometres, and one additional lost bond at 60 micrometres. No other mother pebble shows internal-bond loss in the completed pilot.

The native force-network series shows that the damage event occurred after the load-bearing contact graph had already become spanning. Inter-mother force edges increased from 55 at 10 micrometres to 67 at 25 micrometres and 79 at 40 micrometres, while top-reachable mother pebbles increased from 48 to 58 and 65 over the same snapshots. By 55 micrometres, the graph remained spanning but reorganized to 67 inter-mother edges and 56 top-reachable mother pebbles. The final native graph contained 74 inter-mother edges and 119 inter-pebble subcontacts, with 57 mother pebbles reachable from the top-loaded set and 11 bottom-contacting mother pebbles in that reachable component.

These results support a localized microcracking mechanism rather than bed-wide fragmentation within the simulated displacement range. In the corrected PB-007 pilot, force-chain densification and reorganization precede the first detectable internal bond loss, and the subsequent microcrack growth remains confined to a single upper-bed mother pebble through 60 micrometres. The result should be presented as a corrected 100-mother-pebble pilot sequence and not as a converged population statistic.

## 3. Discussion skeleton

- Main contribution: a failure-aware workflow for avoiding false bed-scale fracture claims caused by proxy-to-template gaps.
- Materials relevance: corrected mesoscopic fracture-event data can support assessment of breeder-bed contact degradation, fragment generation, heat-transfer contacts and purge-flow pathway risk.
- Conservative boundary: current template is a calibration candidate; current PB-007 is a validation route; corrected fracture statistics are pending until acceptance gates pass.
- PB-006 should be discussed only internally or, if included, as a short methodological caution in Supplementary/Limitations, not as Results.

## 4. Methods skeleton

Include:

- DEM contact and bond model parameters;
- surface-supported template generation;
- single-pebble calibration and sensitivity cases;
- rigid-clump settling;
- rigid-to-bonded transfer with insertion-frame correction;
- six-wall native contact-force output;
- step-relaxed loading and gravity-baseline-corrected force-balance metric;
- event extraction after corrected compression only.

## Figure plan for revised manuscript

1. Workflow and acceptance gates: surface-supported template -> rigid-clump settling -> bonded transfer -> six-wall force validation -> fracture sequence.
2. Single-pebble calibration and sensitivity.
3. Surface-supported template and rigid-bed connectivity/transfer validation.
4. PB-007 pre-damage force-transmission gate: native force graph, zero bond loss, wall-force balance and kinetic-energy relaxation.
5. Corrected fracture-event sequence, only after PB-007 fracture run exists.
6. Mechanism figure linking native load path, fracture onset and topology evolution, only after corrected fracture run exists.

## Submission status

Not ready for Journal of Nuclear Materials submission. The revised manuscript becomes submission-candidate only after Fig. 4-Fig. 6 are rebuilt from corrected PB-007 evidence and the current PB-006 bed-scale claims are removed from the submitted package.
