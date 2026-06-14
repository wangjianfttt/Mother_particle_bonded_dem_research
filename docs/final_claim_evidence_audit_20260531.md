# Final claim-evidence audit, 2026-05-31

This audit checks whether `manuscript/main_text_v2.md` stays inside the current evidence boundary after adding the completed PB-006 seed1000-02 case.

## Main manuscript claims

| Claim | Current evidence | Audit result |
| --- | --- | --- |
| SP-002-CAL1 is a current single-pebble calibration candidate. | CAL1 x-normal peak force 18.637 N, first break 0.1025 mm, two major fragments 227/224; x-normal 0.05 m/s rerun peak 21.642 N, first break 0.1025 mm, two major fragments 236/226; `figures/sp002/single_pebble_calibration_evidence.*`; `figures/sp002/sp002_force_displacement_overlay.*`. | Supported with conservative wording. It must not be called a final Li4SiO4 material law. |
| Locked-template insertion prevents precompression internal damage. | 500-pebble init: 250000 subparticles and 2938000 intact bonds; 1000-pebble init: 500000 subparticles and 5876000 intact bonds; zero precompression broken bonds in accepted initchecks. | Supported computationally. |
| Three 500-pebble random beds have reproducible onset but seed-dependent growth. | `tables/pb006_breakage_event_database_summary.csv`: all three 500-pebble seeds first break at 0.0724975 mm in mother pebble 500; final damage ranges 246-559 broken bonds and 4-7 damaged pebbles. | Supported as pilot statistics, not as a converged distribution. |
| Upper-bed packing is consistent with stronger cascades. | Packing descriptors and overlap-derived proxy force-path outputs show stronger upper-bed connectivity/loading footprint for the stronger 500-pebble cascade. | Supported as geometry-derived diagnostic evidence only. Native contact-force output remains a future requirement. |
| Completed 1000-pebble restartable cases preserve a top-layer trigger but differ in propagation. | `tables/pb006_1000_orientation_sensitivity_metrics.csv`: seed01 15 events/98 bonds/3 pebbles; orient02 9 events/95 bonds/1 pebble; seed02 31 events/316 bonds/5 pebbles. All damage remains top-bin; first break is in pebble 1000 at 0.0599975-0.0724975 mm. | Supported as event-sequence variability. It does not establish bed-scale probability. |

## Wording audit

Safe wording currently present:

- "current calibration candidate"
- "not a final Li4SiO4 material law"
- "overlap-derived force-path proxy"
- "event-sequence evidence"
- "not yet full probability statistics"
- "screening protocol"

Terms to continue avoiding:

- "validated Li4SiO4 material law"
- "fully quasi-static compression"
- "measured/native force chain" for proxy outputs
- "converged bed-scale probability"
- "universal fracture propagation law"

## Current submit-readiness judgement

The manuscript is now defensible as a computational workflow and event-sequence paper. The remaining blockers for a stronger submission are not missing PB-006 seed1000-02 data, but presentation and validation depth:

1. Verify figure/caption consistency after the seed02 update.
2. Verify `manuscript/references.bib` DOI and metadata.
3. Decide whether to freeze the current 1000-pebble evidence set or launch seed1000-03.
4. Add native force-chain evidence only if the claim is upgraded from "consistent with" to a direct mechanism claim.
