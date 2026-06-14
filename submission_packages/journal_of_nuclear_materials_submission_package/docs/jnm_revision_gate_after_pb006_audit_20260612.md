# JNM revision gate after PB-006 force-transmission audit (2026-06-12)

## Current decision

The current Journal of Nuclear Materials manuscript, cover letter, highlights, figure captions and submission package must remain on hold. PB-006 can no longer be used as bed-scale evidence for force-chain-mediated fracture, macroscopic bed response, top-layer propagation or 1000-pebble event-sequence mechanisms.

The only defensible PB-006 role is historical workflow diagnosis: it demonstrated that the original event-extraction machinery worked, but the physical bed did not transmit load to the bottom plate during the reported fracture window.

## Manuscript sections that must be withdrawn or rewritten

The following parts of `manuscript/journal_of_nuclear_materials_submission_draft.md` must not be submitted in their present form:

1. Abstract claims about three 500-pebble beds and restartable 1000-pebble post-onset propagation.
2. Results section `Random 500-pebble beds show reproducible onset but seed-dependent growth`.
3. Results section `Macroscopic bed response co-evolves with localized fracture`.
4. Results section `Upper-bed packing controls the strength of the breakage cascade`.
5. Results section `A 1000-pebble bed preserves the early top-layer trigger`, including the event table and Table 2.
6. Discussion claims that current bed-scale results reveal where damage starts, spreads and forms a packing-sensitive growth path.
7. Methods descriptions that present PB-006 bed compression as a valid bed-scale mechanics workflow rather than a superseded diagnostic route.

## Figures and tables that must be removed from the main JNM story

Withdraw from the main manuscript and current submission package:

- `figures/pb006/jnm_bed_macro_response.*`
- `figures/pb006/pb006_force_path_proxy.*`
- `figures/pb006/pb006_seed02_seed03_overlap_force_proxy.*`
- `figures/pb006/pb006_breakage_event_database.*`
- `figures/pb006/pb006_1000_0p15_three_stage_sequence.*`
- `figures/pb006/pb006_1000_orientation_sensitivity.*`
- `figures/pb006/pb006_500_vs_1000_short_comparison.*`
- `figures/pb006/pb006_1000_targeted_window_event_sequence.*`

The corresponding PB-006 tables may remain archived for reproducibility, but not as JNM bed-scale evidence.

## Evidence that can remain in the revised JNM manuscript

The following evidence can remain, with conservative wording:

1. Single-pebble calibration-candidate evidence: crush-load scale, first-break displacement, split-type morphology, resolution sensitivity and rate sensitivity.
2. Surface-resolved 500-subparticle template evidence in `tables/jnm_surface_resolved_template_validation.csv`:
   - directional diameter support improved from the random-core template;
   - first break 0.0915 mm;
   - peak top load 18.7523 N;
   - two dominant final fragments of 220 and 213 subparticles.
3. PB-007 rigid-clump settling geometry in `tables/pb007_rigid_surface_100_settle_summary.csv`:
   - 100 mother pebbles;
   - 164 inter-pebble edges;
   - largest component 99/100;
   - 27 bottom-contacting pebbles;
   - maximum overlap about 1.04 micrometres.
4. PB-007 bonded transfer accuracy and exact intact-bond initialization, once summarized in the revised Methods/Results.

## PB-007 acceptance gates before any new bed-scale fracture claim

A corrected PB-007 bed calculation must pass all gates below before fracture-event statistics are interpreted:

1. Zero internal-bond loss during rigid settling, bonded transfer, seating and pre-onset loading.
2. Native mother-mother contact-force graph with a top-to-bottom reachable path.
3. Six-wall native wall-contact output, including side-wall vertical force.
4. A gravity-baseline-corrected incremental force balance during pre-damage compression. Top and bottom absolute reactions alone are insufficient because the bottom plate carries bed self-weight before top compression.
5. Low residual kinetic energy after each loading increment or a documented step-relaxation convergence trend.
6. No use of restart-continuation evidence unless bond state restoration is independently verified. The current restart route is invalid because the bond counter was not preserved.

## Replacement JNM story line

The revised paper should be rebuilt around this conservative sequence:

1. A bonded-template Li4SiO4 mother pebble is calibrated only as a current load-scale and fragment-mode candidate.
2. The old PB-006 route is disclosed internally as a failure mode of proxy-to-template geometry transfer, not used as a submitted result.
3. A surface-resolved template and rigid-clump deposition create a mechanically connected bed without pre-damage.
4. PB-007 acceptance gates prove the corrected bed can transmit load before fracture.
5. Only after those gates pass should the paper report a corrected mother-pebble-resolved fracture-event sequence.

Until step 5 exists, the JNM manuscript is a method-validation draft, not a submission-ready fracture-sequence paper.
