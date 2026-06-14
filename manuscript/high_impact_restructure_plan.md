# High-impact manuscript restructure plan

This plan turns the current project record into a tighter high-impact manuscript. The goal is not to overclaim, but to make the central advance easy to judge: a bonded-template DEM workflow that resolves mother-pebble fracture-event sequences in random Li4SiO4 breeder beds.

## Core argument

Fusion breeder pebble-bed crushing is usually measured macroscopically or treated probabilistically, but this work resolves the internal bond-breakage sequence of individual 1 mm Li4SiO4 pebbles after intact bonded templates are inserted into random packed beds.

Evidence boundary: the strongest statistical evidence remains the three-seed 500-pebble PB-006 set, while the completed 1000-pebble seed01, orient02 and seed02 restartable runs support scale-up, robust top-layer onset and variable post-onset propagation. They do not yet establish a converged bed-scale probability distribution.

Sharper version for a high-impact abstract:

By representing each Li4SiO4 breeder pebble as 500 bonded subparticles and using a two-stage proxy-deposition/intact-template-injection protocol, this work connects single-pebble fracture calibration to statistically resolved compression damage in 500-pebble beds and onset-resolved damage in a 1000-pebble bed.

## Recommended title options

1. Mother-pebble-resolved fracture sequences in random Li4SiO4 breeder beds by bonded-particle DEM
2. Tracking lithium orthosilicate pebble crushing inside random fusion-blanket beds
3. Bonded-template DEM reveals localized crushing sequences in ceramic breeder pebble beds
4. From single-pebble fracture to bed-scale crushing events in Li4SiO4 breeder beds
5. Resolving compression-driven breakage events in crushable fusion-blanket pebble beds
6. A bonded-subparticle framework for fracture-resolved compression of Li4SiO4 breeder pebble beds
7. From single-pebble fracture calibration to thousand-pebble bed damage in ceramic fusion breeders
8. Scalable numerical experiments for breakage statistics in ceramic breeder pebble beds

## New Results Architecture

### Result 1: Calibrated bonded templates give each 1 mm pebble an internal failure state

Purpose: establish that the mother pebble is not a rigid proxy but a breakable body.

Main evidence:

- 500-subparticle template.
- SP-002-CAL1 peak load 18.64 N.
- Two major fragments of 227 and 224 subparticles.
- Orientation/strength multiplier scans show scatter and morphology retention.

Claim wording:

The current template is a calibration candidate consistent with available load and fragmentation targets, not a final material law.

### Result 2: Locked-template insertion separates random packing from internal breakage

Purpose: answer the user's central concern: the 500 subparticles must form one intact pebble before bed compression.

Main evidence:

- Proxy spheres settle under gravity first.
- Bonded templates are created far apart and translated as intact 500-subparticle groups.
- 500-pebble init: 250000 subparticles, 2938000 intact bonds, zero broken bonds.
- 1000-pebble init: 500000 subparticles, 5876000 intact bonds, zero broken bonds.

Claim wording:

The workflow prevents internal bond breakage during deposition by construction, then activates bond failure during compression.

Reviewer framing:

This section should be introduced as a methodological control rather than a convenience. It answers whether proxy-sphere deposition followed by bonded-template injection creates a defensible initial state.

### Result 3: Three 500-pebble beds reveal reproducible onset and seed-dependent growth

Purpose: this is the statistical core of the paper.

Main evidence:

- seed01: 271 localized broken bonds, 11 events, 5 damaged pebbles.
- seed02: 246 localized broken bonds, 9 events, 4 damaged pebbles.
- seed03: 559 localized broken bonds, 22 events, 7 damaged pebbles.
- all first break at 0.0725 mm in mother pebble 500.
- damage remains in the top two height bins through 0.20 mm.

Claim wording:

Onset is reproducible across independent random packs, while later event magnitude is controlled by upper-bed packing structure.

Suggested stage language:

- Stage I: compaction and load-path formation with no internal bond loss.
- Stage II: first top-layer mother-pebble damage.
- Stage III: lateral top-layer propagation or plateau depending on packing.
- Stage IV: localized upper-bed damage accumulation through the endpoint.

### Result 4: Packing descriptors and overlap-force proxies explain event amplification

Purpose: move beyond event counting toward mechanism.

Main evidence:

- seed03 has lower bed height, larger top-bin population and higher top-bin mean degree.
- overlap-derived proxy networks show broader top loading in seed03.
- seed03 breakage laterally spreads across pebbles 498-500 at 0.0975 mm.

Claim wording:

Upper-bed geometry is consistent with stronger load-path broadening and larger breakage cascades; native contact-force output is still needed for final force-chain proof.

### Result 5: 1000-pebble scale-up preserves the early top-layer trigger

Purpose: show that the method is not confined to 500 pebbles.

Main evidence:

- 1000 proxy bed height 7.912 mm.
- 500000 subparticles and 5876000 intact bonds.
- first cumulative bond loss at 0.0675 mm.
- targeted local dumps resolve six events from 0.0675 to 0.0950 mm.
- all 53 broken bonds assigned to mother pebble 1000.
- completed restartable 0.15 mm runs now include seed01, orient02 and seed02; seed02 gives 31 events and 316 broken bonds over five top-bin pebbles.

Claim wording:

The 1000-pebble runs confirm scale-up and onset localization and show that post-onset propagation varies strongly with template orientation and independent packing.

Keep probability language conservative until additional independent 1000-pebble packings are completed.

### Result 6: Blanket-design relevance of fracture-resolved outputs

Purpose: translate DEM outputs into fusion blanket language without overclaiming transport predictions.

Main evidence:

- onset displacement and force.
- damaged mother-pebble fraction.
- spatial localization by height bin.
- event-rate and cascade metrics.
- fragment-size descriptors where available.

Claim wording:

The workflow provides fracture-resolved inputs for later thermo-mechanical and purge-gas transport coupling, rather than directly predicting tritium release or permeability in the present manuscript.

## Main Figure Plan

| Figure | Role | Panels |
| --- | --- | --- |
| Fig. 1 | Workflow figure | single-pebble bonded template; proxy settling; locked template injection; compression; event extraction |
| Fig. 2 | Single-pebble calibration | force-displacement target; rejected homogeneous case; CAL1 two-fragment graph; orientation scatter |
| Fig. 3 | Locked-template random-bed initialization | proxy bed; 500/1000 intact bond counts; zero broken bonds; height distribution |
| Fig. 4 | 500-pebble event sequence | cumulative broken bonds vs displacement for three seeds; first event markers; damaged pebble rank |
| Fig. 5 | Packing-controlled event amplification | packing descriptors; top-bin damage; overlap-force proxy comparison seed02 vs seed03 |
| Fig. 6 | 1000-pebble scale-up and targeted-window onset | 500 vs 1000 onset comparison; 1000 event increments; localization to pebble 1000 |
| Fig. 7, optional if 0.15 mm completes | Large-bed post-onset propagation | 0.10-0.15 mm event increments; damaged-pebble spread; force evolution |

Supplementary:

- full strength scan.
- speed scan.
- stiffness scan.
- PB-003/PB-004/PB-005 debugging beds.
- full event tables.
- cutoff sensitivity.
- restartable 0.15 mm monitoring table until complete.

## Abstract Skeleton

Context: ceramic breeder pebble beds must retain load-bearing and purge-gas pathways, but internal crushing sequences are difficult to observe experimentally.

Gap: existing bed-scale models often track whole-particle probabilities or macroscopic response rather than internal bond-loss sequences within each pebble.

Approach: we build 1 mm Li4SiO4 bonded templates from 500 subparticles, calibrate a weak-plane candidate, insert intact templates into random beds formed by proxy-sphere settling, and compress the bed in LIGGGHTS-INL.

Key results: three 500-pebble beds share the same first-break displacement and top-pebble trigger, while later damage varies with upper-bed packing; a 1000-pebble run resolves six onset events localized to the highest pebble.

Implication: the workflow connects single-pebble fracture calibration to mother-pebble-resolved bed crushing statistics.

Boundary: quantitative prediction still requires fuller stiffness calibration, slower loading verification, native contact-force output and deeper 1000-pebble repeats.

## Reviewer-risk controls

| Risk | Manuscript control |
| --- | --- |
| Template not validated | Call it a calibration candidate; keep load/morphology evidence near the claim. |
| Too many debugging beds | Move PB-003/PB-005 details to Supplementary; keep main text focused on PB-006. |
| 1000-pebble result too short | Present it as scale-up/onset only until 0.15 mm restartable run finishes. |
| Force-path proxy not native force | Label as overlap-derived diagnostic; do not claim measured force chains. |
| 500-pebble statistics too small for distributions | Claim reproducible onset and seed-dependent magnitude, not universal avalanche laws. |
| 0.20 mm compression seems large | Separate onset-regime metrics from accelerated large-compression damage evolution. |
