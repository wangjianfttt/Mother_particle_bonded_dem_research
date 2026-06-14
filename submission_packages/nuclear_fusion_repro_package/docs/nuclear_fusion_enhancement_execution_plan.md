# Nuclear Fusion enhancement execution plan

Updated: 2026-06-01 CST

This plan defines the optional strengthening work after the Nuclear Fusion working submission package was prepared. The current manuscript is already defensible as a computational workflow and event-sequence paper. The purpose of these additions is to reduce likely reviewer objections, not to change the central claim.

## Claim boundary to preserve

- SP-002-CAL1 remains a current calibration candidate, not a final Li4SiO4 material law.
- The 1000-pebble calculations provide event-sequence evidence, not a converged bed-scale probability distribution.
- The overlap-derived force-path proxy is a diagnostic; direct native contact-force evidence should only be claimed after native contact output is extracted.

## Highest-value optional additions

| Priority | Addition | Why it helps Nuclear Fusion | Risk/cost | Manuscript impact |
| --- | --- | --- | --- | --- |
| 1 | Independent 1000-pebble seed03 to 0.15 mm | Weakens the "too few 1000-pebble packings" objection and tests whether seed02-like spreading recurs. | Long wall time and large local dumps unless targeted window is carefully set. | Update Fig. 3, Fig. 6, event database and Discussion wording from three to four 1000-pebble cases. |
| 2 | Slower or hold-relax x-normal SP-002-CAL1 single-pebble check | Weakens the "screening speed/dynamic artefact" objection for the template. | Moderate runtime; may shift peak force and require conservative interpretation. | Strengthens Fig. 2 and Extended Data Fig. 1; may allow "partial rate robustness" wording to become stronger. |
| 3 | Native contact-force/network output at selected PB-006 states | Converts overlap-derived proxy into direct DEM force-path evidence. | Requires careful LIGGGHTS local-output design; high risk of large files. | Upgrades Fig. 4 mechanism language if successful. |

## Seed03 PB-006 minimum safe route

Use a unique case id and archive after each stage to avoid overwriting seed01/seed02 files. Existing wrapper scripts write through the shared PB-006 directory, so the working `post/`, `log.liggghts`, `screen_*.log` and `data/proxy_centers_1000.csv` files are transient and must be archived or copied under case-specific names.

Current safety status:

- Do not directly launch seed03 from the present shared PB-006 workspace without a staging decision.
- `simulations/pebble_bed/PB-006/post/` currently contains a seed02-scale local-output working copy, about 7.4 GB.
- Available disk space was about 32 GiB at the latest check, so another 1000-pebble restartable run is possible but tight.
- `postprocess_pb006_1000_0p15_restartable.sh` is not safe for seed03 because it contains seed01-specific assumptions. Seed03 must use generic postprocessing scripts.
- `tables/pb006_seed_manifest.csv` has been updated so seed1000-02 is marked completed, not pending.

Proposed case ids:

- Proxy settling: `PB-006-proxy-1000-seed03-stream-fall`
- Initcheck: `PB-006-bonded-randompack-1000-seed03-initcheck`
- Compression: `PB-006-bonded-randompack-1000-seed03-prod-0p15mm-targeted-window-restartable`

Candidate command sequence:

```bash
scripts/run_pb006_proxy_settle.sh PB-006-proxy-1000-seed03-stream-fall 1000 300000 10000 1442695041
scripts/prepare_pb006_bonded_from_proxy.sh 1000 20260601 simulations/pebble_bed/PB-006/data/proxy_centers_1000_PB-006-proxy-1000-seed03-stream-fall.csv
scripts/run_pb006_bonded_initcheck.sh PB-006-bonded-randompack-1000-seed03-initcheck
NP=1 scripts/run_pb006_bonded_compression_targeted_window_restartable.sh PB-006-bonded-randompack-1000-seed03-prod-0p15mm-targeted-window-restartable 1000 60000 -0.5 1000 18000 1000
```

Use `pre_window_steps=18000` so local bond dumps begin before the early seed02-like breakage window. The default 39000-step pre-window would miss early events if seed03 behaves like seed02.

Postprocessing should use the generic scripts, not seed01-specific postprocess wrappers:

```bash
python3 scripts/extract_liggghts_thermo.py <archive>/log.liggghts --output data/processed/<case>_thermo.csv
python3 scripts/analyze_bed_breakage_events.py <archive>/post/bonds_window_*.local <archive>/post/bonds_final_*.local --npebbles 1000 --nspheres 500 --thermo data/processed/<case>_thermo.csv --series-output data/processed/<case>_per_pebble_series.csv --events-output data/processed/<case>_breakage_events.csv
python3 scripts/summarize_random_pack_breakage.py data/processed/<case>_breakage_events.csv --metadata <archive>/data/bonded_template_metadata_1000.csv --pebble-output data/processed/<case>_pebble_summary.csv --height-output data/processed/<case>_height_summary.csv
```

## SP-002 slower/hold-relax minimum route

Completed update: the fastest low-risk addition, a true x-normal SP-002-CAL1 run at 0.03 m/s to 0.18 mm, was completed on 2026-06-01 CST. It retained the 5876-bond x-normal branch, first broke at 0.10245 mm and ended with two major fragments of 247 and 246 subparticles. This strengthens first-break and morphology robustness across 0.10, 0.05 and 0.03 m/s screening rates, but does not support peak-load rate wording because the endpoint is before the known peak-force region.

A nominal 0.03 m/s case to 0.30 mm would require roughly 2,000,000 steps at the current timestep and remains optional.

Recommended first check:

```bash
scripts/run_sp002_weakplane_case.sh SP-002-CAL1-x-slow0p03ms-0p18mm 1200000 -0.03 9.0e7 9.0e7 2.25e7 2.25e7 1.0e-6 1.0e-4 7.9460215e-6 1.0e14 5.0e13 9.0e-5
```

The run was actually launched with the orientation wrapper to rebuild the x-normal weak-plane template cleanly:

```bash
scripts/run_sp002_weakplane_orientation_case.sh SP-002-CAL1-x-slow0p03ms-0p18mm 1 0 0 1200000 -0.03 9.0e7 9.0e7 2.25e7 2.25e7 9.0e-5
```

Outputs are archived at:

```text
simulations/single_pebble/SP-002/archive/SP-002-CAL1-x-slow0p03ms-0p18mm-completed-20260601/
```

## Native contact-force route

Do not add force-chain claims until this is tested. The safest route is a restart/rerun or selected-state local output that records wall-mother and mother-mother contact data only at a few displacements: pre-onset, onset, plateau and late burst. The target question is whether later damaged pebbles enter high-load paths before their bond loss.

## Decision recommendation

For the fastest Nuclear Fusion submission, freeze the present manuscript and submit after author metadata and repository DOI are inserted. For a stronger submission with one additional week of compute/postprocessing, run seed03 first. Run the SP-002 slower case only if the single-pebble calibration is expected to be the main reviewer concern.
