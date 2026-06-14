# Submission readiness checklist

Historical note: this checklist records the earlier Nuclear Fusion/PB-006 preparation route and is no longer the authoritative submission guide. For the active Journal of Nuclear Materials package, start from `START_HERE_JNM_SUBMISSION.md` and the current gate report at `docs/jnm_final_submission_gate_report.md`.

This checklist keeps the fastest paper path aligned with the project evidence. The target paper is a high-quality computational study, not yet a final predictive Li4SiO4 material-law paper.

## Current manuscript position

Working title:

Mother-pebble-resolved fracture sequences in random Li4SiO4 breeder beds by bonded-particle DEM

One-sentence argument:

In ceramic breeder pebble beds for fusion blankets, we show that a locked bonded-template DEM workflow can insert 500-subparticle Li4SiO4 mother pebbles into random beds without precompression bond loss and resolve compression-driven mother-pebble fracture-event sequences, supported by single-pebble calibration-candidate checks, three 500-pebble random beds and completed 1000-pebble restartable onset/post-onset cases.

## Claims ready for main text

| Claim | Evidence | Status |
| --- | --- | --- |
| The workflow prevents deposition-induced internal damage. | 500-pebble init: 250000 subparticles, 2938000 intact bonds, zero broken bonds; 1000-pebble init: 500000 subparticles, 5876000 intact bonds, zero broken bonds. | Ready |
| SP-002-CAL1 is a defensible current calibration candidate. | Peak 18.64 N, first break 0.1025 mm, two major fragments 227/224; true x-normal 0.05 m/s keeps first break and split morphology with peak 21.64 N. | Ready with conservative wording |
| 500-pebble random beds have reproducible onset but seed-dependent growth. | Three seeds first break at 0.0725 mm in mother pebble 500; final localized bond loss 246-559 bonds and 4-7 damaged pebbles. | Ready |
| Upper-bed geometry is consistent with stronger cascades. | Seed03 has lower bed height, larger top-bin population, higher top-bin mean degree and broader overlap-derived force-path proxy. | Ready as diagnostic, not native force proof |
| 1000-pebble restartable runs support robust top-layer onset and variable post-onset growth. | Seed01: 15 events, 98 bonds, 3 damaged pebbles; orient02: 9 events, 95 bonds, one damaged pebble; seed02: 31 events, 316 bonds, 5 damaged pebbles. | Ready as event-sequence evidence |
| Independent 1000-pebble packing statistics are being added. | seed1000-02 proxy, initcheck, 0.15 mm compression, archiving and generic postprocessing are complete. Damage remains in the top bin but spreads over pebbles 1000, 999, 998, 997 and 949. | Ready with conservative wording |

## Main figure package

| Figure | Purpose | Current files | Decision |
| --- | --- | --- | --- |
| Fig. 1 | Locked-template workflow | `figures/main/fig1_workflow.*` | Main |
| Fig. 2 | Single-pebble calibration candidate | `figures/sp002/single_pebble_calibration_evidence.*` | Main or extended-data depending on journal length |
| Fig. 3 | Three 500-pebble and resolved 1000-pebble event statistics | `figures/pb006/pb006_breakage_event_database.*`, `figures/pb006/pb006_three_seed_packing_breakage.*` | Main; combined event database now includes orient02 and seed02-1000 |
| Fig. 4 | Packing/force-path diagnostic | `figures/pb006/pb006_seed02_seed03_overlap_force_proxy.*` | Main with conservative caption |
| Fig. 5 | 1000-pebble three-stage sequence | `figures/pb006/pb006_1000_0p15_three_stage_sequence.*` | Main |
| Fig. 6 | 1000-pebble orientation sensitivity | `figures/pb006/pb006_1000_orientation_sensitivity.*` | Main |
| Extended Data Fig. 1 | Single-pebble force-displacement overlay | `figures/sp002/sp002_force_displacement_overlay.*`, `tables/sp002_force_displacement_overlay_metrics.csv` | Added to support curve-level calibration screening |

## Must-finish before submission

1. Replace placeholder author names, affiliations, ORCID ids, acknowledgements and funding information in the Nuclear Fusion working draft.
2. Archive source data and reduced simulation inputs in a persistent repository before submission; the local reduced package is currently in `submission_packages/nuclear_fusion_repro_package`.
3. Optional strength upgrade: run one more independent 1000-pebble packing or a slower/hold-relax single-pebble check if the target journal demands stronger statistical or quasi-static evidence.

## Completed during current paper-preparation pass

- Added orient02 to `scripts/build_pb006_event_database.py`.
- Rebuilt `tables/pb006_breakage_event_database.csv` and `tables/pb006_breakage_event_database_summary.csv`; orient02 is now included as `seed01-1000-orient02-0p15`.
- Regenerated `figures/pb006/pb006_breakage_event_database.*` from the updated database.
- Inserted the main figure package into `manuscript/main_text_v2.md` with conservative captions.
- Replaced `manuscript/figure_captions.md` with the current JNM-aligned graphical abstract, 6-main-figure and 2-supplementary-figure caption/source-data companion.
- Verified DOI/title/year metadata against Crossref and saved `tables/reference_crossref_audit_20260531.csv`.
- Added missing authors, volume, issue and page/article-number fields to `manuscript/references.bib`.
- Created the current paper snapshot as `manuscript/submission_draft_v1.md`.
- Targeted Nuclear Fusion as the journal and created `manuscript/nuclear_fusion_submission_draft.md`, `manuscript/nuclear_fusion_targeting_plan.md` and `manuscript/nuclear_fusion_cover_letter_draft.md`.
- Created a reduced reproducibility package plan and builder: `manuscript/nuclear_fusion_data_code_package_plan.md` and `scripts/build_nuclear_fusion_repro_package.py`.
- Built the current reduced reproducibility package under `submission_packages/nuclear_fusion_repro_package` with a `MANIFEST.csv`.
- Created and compiled a working LaTeX/PDF submission draft: `manuscript/nuclear_fusion_iop_submission.tex` and `manuscript/nuclear_fusion_iop_submission.pdf`.

## Conservative wording rules

- Say "current calibration candidate", not "calibrated Li4SiO4 material law".
- Say "overlap-derived force-path proxy", not "measured/native force chain".
- Say "robust top-layer trigger in completed cases", not "universal bed-scale breakage probability".
- Say "orientation-sensitive post-onset propagation", not "deterministic crack propagation law".
- Say "screening or restartable numerical loading protocol", not "fully quasi-static compression", until slower or hold-relax checks are complete.
