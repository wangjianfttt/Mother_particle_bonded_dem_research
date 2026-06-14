# SP-002 preliminary single-pebble compression results

## Purpose

SP-002 is the first working single-pebble compression case using a 500-subparticle bonded multisphere and two rigid `mesh/surface/stress` plates in LIGGGHTS-INL.

These results are numerical workflow checks, not final calibrated material results.

## Geometry and model

- Mother pebble nominal diameter: 1.0 mm
- Subparticles: 500
- Initial intact bonds: 6723
- Contact model: `gran model hertz tangential history cohesion bond stressBreak on createBondAlways off`
- Bottom plate: fixed mesh plate
- Top plate: moving mesh plate
- Output: thermo table parsed from `log.liggghts`

The inserted particle coordinates are shifted relative to the raw multisphere template. For the current template, the effective z-shift is approximately `7.9460215e-6 m`, used by `scripts/run_sp002_plate_case.sh`.

## Strength scan

Fast loading setup:

- Top plate speed: 1.0 m/s
- Bottom gap: 1.0 um
- Top initial gap: 100 um
- End displacement: 0.15 mm

| Case | Bond strength | Peak top force | First break displacement | Final broken bonds |
| --- | ---: | ---: | ---: | ---: |
| SP-002-strength-25MPa | 25 MPa | 3.99 N | 0.105 mm | 242 |
| SP-002-strength-50MPa | 50 MPa | 6.67 N | 0.105 mm | 193 |
| SP-002-strength-100MPa | 100 MPa | 16.47 N | 0.110 mm | 123 |

Summary file: `data/processed/SP-002-strength-scan_summary.csv`.

The trend is physically sensible: increasing bond strength increases the crush-load scale and reduces final bond breakage.

## Loading-rate sensitivity

Bond strength fixed at 50 MPa.

| Top speed | Peak top force | Peak bottom force | First break displacement | Final broken bonds |
| ---: | ---: | ---: | ---: | ---: |
| 1.0 m/s | 6.67 N | 5.48 N | 0.105 mm | 193 |
| 0.5 m/s | 7.19 N | 5.44 N | 0.108 mm | 123 |
| 0.25 m/s | 6.99 N | 5.82 N | 0.106 mm | 105 |
| 0.1 m/s | 6.45 N | 6.06 N | 0.109 mm | 106 |

Summary file: `data/processed/SP-002-speed-sensitivity-50MPa_summary.csv`.

The final broken-bond count changes strongly from 1.0 to 0.5 m/s, but is nearly unchanged between 0.25 and 0.1 m/s. The current 50 MPa setup is therefore approaching a useful quasi-static regime for breakage count at 0.25 m/s and below, although force oscillations still need damping/relaxation checks before direct comparison with experiments.

## Fragment statistics

For the 50 MPa, 0.1 m/s case, a bond-local dump was added:

```lammps
compute bond_force all pair/gran/local/bond
dump bdmp all local ${dump_every} post/bonds_*.local c_bond_force[7] c_bond_force[8]
```

The fragment post-processing script `scripts/analyze_bond_fragments.py` treats intact bonds as graph edges and subparticles as graph nodes.

Result for `SP-002-speed-0p1ms-50MPa-bonds`:

- First fragmentation event: step 218000, one single-particle fragment detached.
- Final state at step 300000: 6617 intact bonds, 7 fragments.
- Largest final fragment: 494 subparticles.
- Single-particle final fragments: 6.

Fragment file: `data/processed/SP-002-speed-0p1ms-50MPa-bonds_fragments.csv`.

## Bond-stiffness screening

At fixed bond strength of 50 MPa, three stiffness settings were screened with `kt = kn / 2`.

| Normal bond stiffness | Estimated initial stiffness | Final broken bonds | Interpretation |
| ---: | ---: | ---: | --- |
| 5.0e13 N m-3 | 452 N mm-1 | 53 | Plausible screening case |
| 1.0e14 N m-3 | 570 N mm-1 | 53 | Plausible screening case |
| 2.0e14 N m-3 | 465 N mm-1 | 4727 | Rejected pending smaller timestep check |

The highest stiffness produced a large abrupt bond-loss event immediately after contact, suggesting numerical instability or an overly brittle parameter combination. It should not be used for physical interpretation until rerun with a smaller timestep and/or a step-relax protocol.

## Known numerical notes

- `fix print` currently triggers MPI abort for this bonded mesh-wall setup; use thermo-log extraction instead.
- A contact-model whitelist entry is required in the local LIGGGHTS-INL build:

```text
GRAN_MODEL(HERTZ, TANGENTIAL_HISTORY, COHESION_BOND, ROLLING_OFF, SURFACE_DEFAULT)
```

- With too small a bottom gap, a small preload is introduced. The current workflow uses this deliberately as a bottom support; final calibration should quantify or subtract the preload.

## Next simulation steps

1. Introduce a quasi-static step-relax protocol or additional damping check to reduce force oscillations.
2. Add bond stiffness scanning after the strength trend is stable.
3. Calibrate the strength and stiffness pair against literature single-pebble crush load and elastic slope.
4. Extend fragment statistics to include fragment mass distribution and spatial detachment locations.
5. Move calibrated single-pebble templates into a pebble-bed compression model.

## Bed-scale workflow check

PB-001 was created as a 12-pebble ordered bed, each pebble using the same 500-subparticle bonded template. The first spacing setting created cross-pebble bonds, which is nonphysical. Increasing the initial centre spacing to 1.30 mm eliminated this artefact and produced exactly `80676 = 12 x 6723` intact internal bonds.

A short fast-loading contact test reached 0.10 mm top displacement, produced a peak top force of 36.10 N and broke 308 bonds. The bottom reaction remained zero, indicating that the current ordered bed is not yet a physically meaningful supported compression test. The next PB-001 revision should include settling, bottom support and lateral confinement.

PB-002 compressed the same separated ordered bed with a lower top plate. This preserved the no-new-cross-bond condition, but the bottom reaction was still zero after 0.80 mm top displacement, while 8419 bonds broke. The result shows that simply compressing an initially loose ordered bed mainly damages the upper pebbles before a supported bed skeleton forms.

PB-003 therefore introduced a staged initialization. The 12 pebbles were first created at 1.35 mm spacing and run for one step to create internal bonds only; atom-id groups were then translated into a compact 2 x 2 x 3 bed. In the `PB-003-staged-target1000` diagnostic, no new bonds were created after relocation and both top and bottom wall reactions became non-zero, but relocation and preload broke about 140 bonds before the compression stage.

The improved `PB-003-staged-target1020-supported` case used 1.02 mm target spacing and bottom plate `z = -1.506 mm`. It preserved all `80676 = 12 x 6723` internal bonds before compression, produced a bottom support reaction, and generated compression-induced bond breakage only after about 0.100 mm top displacement. At 0.12 mm displacement, the peak top force was 26.15 N and 212 bonds had broken. Intact-bond graph analysis gives 24 connected components at the final sampled state: the original 12 main pebble components plus 12 single-subparticle fragments. This is the current baseline for bed-scale production simulations.

## PB-004 calibrated-template bed event sequence

PB-004 is the first bed-scale run using the SP-002-CAL1 weak-plane 1 mm pebble template. Each mother pebble contains 500 subparticles and approximately 5876 internal bonds after weak-plane bond creation; the 12-pebble bed starts with 70512 internal bonds.

The supported `PB-004-CAL1-supported-events-0p30mm` run compressed the bed to 0.30 mm top displacement. Per-pebble event tracking assigns atom-id ranges to mother-pebble ids and compares each bond dump to the initial internal bond graph.

Files:

- `data/processed/PB-004-CAL1-supported-events-0p30mm_breakage_events.csv`
- `data/processed/PB-004-CAL1-supported-events-0p30mm_per_pebble_series.csv`
- `data/processed/PB-004-CAL1-supported-events-0p30mm_layer_summary.csv`

First observations:

- Top layer pebbles 9-12 break first at 0.1025 mm top displacement.
- Middle layer pebbles 5-8 begin breaking at 0.2125 mm top displacement.
- Bottom layer pebbles 1-4 do not break within 0.30 mm displacement.
- Total internal broken bonds by 0.30 mm are 658 in the top layer and 160 in the middle layer.
- Peak top force is about 67.94 N at 0.2725 mm top displacement.

This is the first complete end-to-end result linking calibrated single-pebble bonded templates to a bed-scale compression breakage-event sequence. The present ordered 2 x 2 x 3 bed should still be treated as a mechanistic baseline; production cases require larger and less symmetric random beds, stronger control of support/load transfer, and multiple calibrated template orientations/strength multipliers.

## PB-005 larger-bed statistical check

PB-005 increases the bed from 12 to 36 mother pebbles in a 3 x 3 x 4 ordered stack. Each mother pebble still uses the SP-002-CAL1 1 mm weak-plane template with 500 subparticles. The staged create-then-translate workflow avoids cross-pebble cohesive bonds and starts the deterministic orientation case with `211536 = 36 x 5876` internal bonds.

Files:

- `data/processed/PB-005-CAL1-36pebble-events-0p15mm_breakage_events.csv`
- `data/processed/PB-005-CAL1-36pebble-events-0p15mm_layer_summary.csv`
- `data/processed/PB-005-CAL1-36pebble-randori-events-0p15mm_breakage_events.csv`
- `data/processed/PB-005-CAL1-36pebble-randori-events-0p15mm_layer_summary.csv`

The deterministic 36-pebble bed reaches first internal bond breakage in the top layer at 0.1287 mm top displacement. All nine top-layer mother pebbles break synchronously and accumulate 34 broken internal bonds each by 0.15 mm. This confirms the larger-bed workflow but also reveals a symmetry artefact: simply increasing the number of pebbles is not enough if all templates have the same weak-plane orientation and the bed is perfectly ordered.

To break this artificial synchrony, the PB-005 generator was extended to assign a random quaternion orientation to each whole 500-subparticle template. The random-orientation case breaks earlier, at 0.1187 mm, and produces a broader event sequence. All nine top-layer mother pebbles break by 0.15 mm, but their cumulative broken-bond counts vary from 33 to 70 instead of all being identical. The layer summary gives 24 top-layer events and 430 broken internal bonds by 0.15 mm, while the lower three layers remain intact over this displacement window.

This is the current statistically useful bed-scale baseline. The next bed runs should extend the random-orientation case to larger displacement so that middle-layer and bottom-layer participation can be quantified, and should add stochastic strength multipliers or random packed beds to reduce residual lattice symmetry.

## PB-006 random packed production workflow

PB-006 replaces the ordered bed with a two-stage random-packing workflow intended for 500-1000 mother pebbles. Stage A uses monodisperse 1 mm proxy spheres and `insert/rate/region` to pour particles under gravity into a confined container. These proxy particles have no internal bonded subparticles, so internal pebble damage is impossible during packing. Stage B extracts the settled proxy centres, creates SP-002-CAL1 500-subparticle bonded templates far apart to form only internal bonds, and relocates each intact bonded template to one settled centre. Internal bond breakage is therefore first allowed and first measured only during the subsequent compression stage.

The current 500-pebble smoke workflow is:

- `PB-006-proxy-500-stream-fall`: 500 proxy pebbles naturally inserted and settled. Final centre range is z = 0.00049954-0.00449391 m, corresponding to a settled bed height of about 3.99 mm.
- `PB-006-bonded-randompack-500-stream-initcheck`: the settled centres are replaced by 500 calibrated bonded templates, giving 250000 subparticles and `2938000 = 500 x 5876` intact internal bonds.
- The compression-before-loading check gives zero broken internal bonds, which verifies the intended locked-bond packing protocol.

The first production compression case, `PB-006-bonded-randompack-500-prod-0p20mm-primitivewall`, compressed this random bed to 0.20 mm top displacement. Up to the last local bond dump at 0.1975 mm, 271 broken internal bonds are localized to 11 mother-pebble events involving 5 mother pebbles. The first localized event occurs at 0.0725 mm in mother pebble 500, with 23 new broken bonds. Height-resolved statistics show that early damage is concentrated near the moving plate: 223 localized broken bonds occur in the top height bin and 48 in the next bin, while lower bins remain intact over this displacement window. The thermo endpoint at 0.20 mm reports 16 additional broken bonds after the last local dump, so future runs now include a final-step local bond dump to close this assignment gap.

The second production compression case, `PB-006-bonded-randompack-500-seed02-prod-0p20mm-primitivewall`, used an independent proxy-packing seed and settled to a height of about 4.08 mm. It also initialized with 250000 subparticles, `2938000` intact internal bonds and zero broken bonds before compression. With the final-step local bond dump enabled, all 246 broken internal bonds at 0.20 mm are localized to 9 events involving 4 mother pebbles. The first event again occurs at 0.0725 mm in mother pebble 500 in the top height bin, but with 42 broken bonds. The top two height bins accumulate 210 and 36 broken bonds, respectively, while lower bins remain intact.

The third production compression case, `PB-006-bonded-randompack-500-seed03-prod-0p20mm-primitivewall`, settled to a lower bed height of about 3.82 mm and generated a stronger response. It again preserved all `2938000` internal bonds before compression and first broke at 0.0725 mm in mother pebble 500. By 0.20 mm, seed03 localized 559 broken internal bonds to 22 events involving 7 mother pebbles. Damage remained restricted to the top two height bins, with 500 broken bonds in the top bin and 59 in the next bin. The final top force reached 47.86 N, compared with about 27 N for seed01 and seed02.

Packing-descriptor post-processing now links this stronger seed03 response to the settled upper-bed geometry. Using a 1.02 mm geometric-contact cutoff, seed03 has the lowest bed height (3.82 mm), the largest top-bin population (28 pebbles, compared with 15 and 9 for seed01 and seed02), and the highest top-bin mean geometric degree (3.54, compared with 3.00 and 2.89). The first breaking pebble is the highest pebble in all three seeds, but its geometric degree is 4 in seed03 and 3 in seed01/seed02. This descriptor trend is robust to contact cutoffs from 1.00 to 1.10 mm: seed03 remains the lower, more crowded upper-bed state and also shows the largest localized bond loss. This supports a contact-network/load-path interpretation of the seed effect, although direct force-chain analysis from contact dumps is still required before making a final causal claim.

An overlap-derived force-path proxy was added from the archived seed02 and seed03 particle dumps. The script `scripts/analyze_pb006_overlap_force_network.py` maps subparticle overlaps across different mother pebbles and weights each overlap by `overlap^(3/2)`, which is proportional to Hertzian normal force for identical material parameters. It also estimates top-wall loading from subparticle overlap with the moving top plane. This is not native LIGGGHTS contact-local force, but it provides a direct geometry-based test of the load-path interpretation. The proxy supports the seed03 mechanism: at 0.0975 mm, seed03 has top-wall loading on pebbles 498-500, matching the timestep where bond breakage spreads laterally across these same top pebbles. At 0.1975 mm, seed03 has four top-wall-loaded pebbles and six inter-pebble proxy edges, compared with two top-wall-loaded pebbles and four inter-pebble edges in seed02.

Files:

- `tables/pb006_three_seed_packing_descriptors_cutoff1p02mm.csv`
- `tables/pb006_three_seed_active_pebble_descriptors_cutoff1p02mm.csv`
- `tables/pb006_packing_descriptor_cutoff_sensitivity.csv`
- `figures/pb006/pb006_three_seed_packing_breakage.svg`
- `figures/pb006/pb006_three_seed_packing_breakage.pdf`
- `figures/pb006/pb006_three_seed_packing_breakage.tiff`
- `tables/pb006_seed02_overlap_force_proxy_summary.csv`
- `tables/pb006_seed03_overlap_force_proxy_summary.csv`
- `tables/pb006_seed02_overlap_force_proxy_edges.csv`
- `tables/pb006_seed03_overlap_force_proxy_edges.csv`
- `tables/pb006_seed02_overlap_force_proxy_topwall.csv`
- `tables/pb006_seed03_overlap_force_proxy_topwall.csv`
- `figures/pb006/pb006_seed02_seed03_overlap_force_proxy.svg`

This PB-006 route is now the preferred production model for the requested breakage-event sequence study. PB-005 remains useful as a computational debugging case, but publishable bed statistics should come from PB-006-style random packs, with multiple packing seeds and template orientation/strength samples. MPI/domain-decomposed bonded compression currently gives processor-dependent intact-bond counts and is therefore not used for production results; independent seed cases should instead be run as separate single-rank jobs.

## PB-006 1000-pebble scale-up check

The same proxy-settle to bonded-template route was extended to 1000 mother pebbles. The `PB-006-proxy-1000-seed01-stream-fall` proxy case inserts and settles 1000 monodisperse 1 mm proxy pebbles under gravity. The final settled bed contains 1000 centres, has a height of 7.912 mm and reaches low residual kinetic energy after the tail relaxation. At a 1.02 mm centre-distance cutoff, the 1000-pebble proxy bed has 2564 geometric contacts, a global mean degree of 5.128, 58 pebbles in the top height bin and a top-bin mean degree of 3.845.

The settled centres were then converted into 1000 SP-002-CAL1 bonded templates, giving 500000 subparticles. A lightweight bonded initialization check was added to avoid writing multi-million-row local bond dumps during scale-up checks. The first run step reports 5876000 created and intact internal bonds, exactly `1000 x 5876`, with zero broken bonds. This confirms that the locked-bond template-injection workflow scales from 500 to 1000 mother pebbles at initialization. A full 1000-pebble compression run is now computationally feasible but should be scheduled as a production job because memory use reaches the multi-GB range and single-rank compression will be slow.

Files:

- `simulations/pebble_bed/PB-006/data/proxy_centers_1000_PB-006-proxy-1000-seed01-stream-fall.csv`
- `data/processed/PB-006-proxy-1000-seed01-stream-fall_thermo.csv`
- `data/processed/PB-006-bonded-randompack-1000-seed01-initcheck-light_thermo.csv`
- `tables/pb006_1000_proxy_packing_summary.csv`
- `simulations/pebble_bed/PB-006/in.pb006_bonded_initcheck.lmp`
- `scripts/run_pb006_bonded_initcheck.sh`
