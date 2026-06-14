# Manuscript reviewer-risk audit

This audit is written from a skeptical reviewer perspective. It is meant to keep the manuscript claims aligned with available PB-006 evidence.

## Current one-sentence argument

In fusion-blanket Li4SiO4 ceramic breeder beds, we show a bonded-subparticle DEM workflow that inserts intact current-calibration-candidate 1 mm pebble templates into random packed beds and resolves compression-driven mother-pebble fracture-event sequences, supported by three 500-pebble random beds plus three completed 1000-pebble 0.15 mm restartable cases that separate robust top-layer onset from orientation- and packing-sensitive late propagation.

## Major risks and required responses

| Risk | Reviewer concern | Current evidence | Required response |
| --- | --- | --- | --- |
| Template calibration is underdeveloped | A reviewer may argue that a 500-subparticle pebble is only a numerical object unless calibrated against single-pebble force-displacement and crush-load data. | SP-002-CAL1 gives 18.64 N peak load and two large fragments; literature targets are assembled but stiffness and distribution remain incomplete. | Expand single-pebble ensemble and add 250/500/1000 subparticle sensitivity before strong physical claims. |
| Loading may be too fast | Current speeds are numerical screening speeds, so force histories may include dynamic artefacts. | Speed scan suggests fragment-count convergence from 0.25 to 0.1 m/s, but not quasi-static force convergence. | Add slower or step-relaxed compression for the calibration-candidate template and at least one small bed. |
| Locked-bond insertion may bias packing | Proxy settling followed by template injection is efficient, but reviewers may ask whether it reproduces realistic contact fabric. | Zero broken internal bonds before compression; packing descriptors computed from proxy centres. | Report packing fraction, bed height, top-bin population, coordination/fabric descriptors and compare across seeds. |
| 500-pebble statistics remain limited | Three seeds support onset reproducibility but are not enough for robust probability distributions. | Three 500-pebble beds completed to 0.20 mm; onset is reproducible, later magnitude is seed-dependent. | Phrase as pilot statistics; add more seeds if claiming distributions or avalanche exponents. |
| 1000-pebble propagation statistics are still limited | A reviewer may accept the completed 0.15 mm cases but object that two packings plus one orientation replicate cannot establish bed-scale probabilities. | Seed01 reaches 98 broken bonds across pebbles 961, 980 and 1000; orient02 reaches 95 broken bonds entirely in pebble 1000 and remains quiet after 0.1200 mm; seed02 reaches 316 broken bonds across pebbles 949, 997, 998, 999 and 1000. All completed 1000-pebble cases preserve a top-layer first-break trigger. | Claim robust top-layer onset and orientation-/packing-sensitive late propagation. Do not claim a converged probability distribution until additional 1000-pebble random packings are completed. |
| Force-path mechanism is indirect | Overlap-derived contact proxies are not native LIGGGHTS contact forces. | Proxy networks explain seed02/seed03 trends but remain geometry-derived. | Add native contact-local output or explicitly label proxy analysis as a diagnostic, not a measured force chain. |
| Literature comparison is too loose | Prior Li4SiO4 and ceramic-bed work must be connected to each claim, not listed generically. | `literature/literature_matrix.md` and `docs/literature_claim_support.md` now map literature to claims. | Convert these mappings into citation-backed Introduction and Discussion paragraphs. |

## Claim wording rules for the next manuscript pass

| Overstrong wording to avoid | Safer wording now |
| --- | --- |
| The model predicts Li4SiO4 bed crushing. | The model demonstrates a calibration-candidate workflow for resolving mother-pebble breakage events in Li4SiO4-like bonded templates. |
| The 1000-pebble bed reveals post-onset propagation. | Completed 1000-pebble cases show a robust top-layer trigger but variable propagation: seed01 has a modest late burst, orient02 remains confined to pebble 1000, and seed02 develops a stronger top-bin cascade. |
| The 500-subparticle template is validated. | The 500-subparticle template is a current calibration candidate consistent with available load and morphology targets. |
| Breakage statistics are established. | Three 500-pebble seeds provide pilot statistics for onset reproducibility and seed-dependent damage magnitude. |
| Force chains cause seed03 damage. | Overlap-derived force-path proxies are consistent with stronger seed03 top-layer damage. |
