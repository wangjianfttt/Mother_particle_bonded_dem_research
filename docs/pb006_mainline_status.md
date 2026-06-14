# PB-006 mainline status: random bed breakage-event sequence

This note keeps the project aligned with the central objective: insert current-calibration-candidate 1 mm Li4SiO4 bonded templates into random pebble beds and study the compression-driven sequence of internal bond breakage and mother-pebble crushing events.

## Central workflow

1. Generate one current-calibration-candidate 1 mm mother-pebble template from 500 bonded subparticles.
2. Use rigid 1 mm proxy spheres to form a random packed bed under gravity. Proxy settling cannot break internal bonds because no internal subparticle bonds exist during this stage.
3. Replace each settled proxy centre with one intact 500-subparticle bonded template. Internal bonds are created while templates are far apart, then each 500-subparticle group is translated as a locked unit into the packed bed.
4. Compress the bed with primitive side/bottom walls and a moving top mesh plate.
5. Track bond-breakage events by comparing per-mother-pebble internal bond graphs across local bond dumps or, for large 1000-pebble runs, by combining thermo scans with targeted local-dump windows.

## Evidence completed

| Scale | Status | Main evidence |
| --- | --- | --- |
| Single 1 mm template | Current calibration candidate is SP-002-CAL1, a 500-subparticle weak-plane template. | Peak top force 18.64 N; first break 0.1025 mm; final major fragments 227 and 224 subparticles. |
| 500-pebble random beds | Three independent 500-pebble beds completed to 0.20 mm. | All seeds first break at 0.0725 mm in the highest mother pebble; later damage differs by upper-bed packing. |
| 1000-pebble initialization | One 1000-pebble random bed initialized with locked bonded templates. | 500000 subparticles; 5876000 intact internal bonds; zero broken bonds before compression. |
| 1000-pebble onset and post-onset window | One 1000-pebble short compression resolved to 0.10 mm with targeted local dumps. The seed01 restartable 0.15 mm run and one randomized-orientation replicate have completed and have been postprocessed. | Seed01: six onset events at 0.0675-0.0950 mm; 53 broken bonds; all in mother pebble 1000. A damage-quiet plateau persists to 0.1300 mm, followed by renewed late-window bond loss from 0.1325 to 0.1500 mm. The final seed01 0.15 mm event database contains 15 localized events, 98 broken bonds and 3 damaged mother pebbles, all in the top height bin. Orient02: first break also occurs in pebble 1000 at 0.0725 mm, but all 95 broken bonds remain in pebble 1000 and no new damage appears after 0.1200 mm through 0.1500 mm. |
| Event database | Existing 500-pebble and 1000-pebble resolved local events are combined into one table and figure. | `tables/pb006_breakage_event_database.csv`, `tables/pb006_breakage_event_database_summary.csv`, `figures/pb006/pb006_breakage_event_database.svg`. |

## Current numerical boundary

The interpretable 1000-pebble evidence now extends to 0.15 mm for the seed01 restartable run and one fixed-geometry randomized-orientation replicate. These two cases support a conservative claim that the first top-layer trigger is reproducible, while post-onset propagation is sensitive to template orientation or local load-path details.

Two earlier deeper single-core 1000-pebble attempts behaved abnormally and are archived as diagnostics rather than physical results:

- `PB-006-bonded-randompack-1000-seed01-prod-0p20mm-thermoonly` passed relax and reached about 0.0475 mm with zero broken bonds, then stopped updating thermo output while the LIGGGHTS process remained at full CPU.
- `PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-late` passed relax, created 5876000 intact internal bonds and entered the compression pre-window, but it was terminated before reaching the local-dump window. The final log contains early compression thermo rows through step 3078 and a forced restart file, so it is a progress/monitoring diagnostic rather than a physical result. Logs are archived in `simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-late-aborted-before-compression-thermo/`.

These diagnostics should not be interpreted as evidence for post-onset propagation. The manuscript should therefore claim the following conservative position: the workflow scales to 1000 pebbles, preserves zero precompression bond loss, and resolves 0.15 mm event sequences in completed restartable calculations, while robust bed-scale probability statements still require additional independent 1000-pebble packings.

## Next execution strategy

1. Keep the existing 500-pebble three-seed set as the current statistical bed-scale evidence.
2. Keep the 1000-pebble 0.10 mm targeted-window run as an onset and scalability check.
3. Use the restartable targeted-window input `in.pb006_bonded_compression_targeted_window_restartable.lmp`, which adds flushed thermo output and alternating restart files during the long compression stages.
4. Treat statistical 1000-pebble post-onset propagation claims conservatively: seed01, orient02 and seed02 now provide event-sequence evidence, but not a converged probability distribution.

Latest independent 1000-pebble proxy packing:

- Case id: `PB-006-proxy-1000-seed02-stream-fall`
- Purpose: generate the next independent 1000-pebble proxy packing before bonded-template insertion.
- Completion status at 2026-05-31 CST: detached screen session `pb006_proxy_1000_seed02` ended normally. The run produced `data/processed/PB-006-proxy-1000-seed02-stream-fall_thermo.csv` and `simulations/pebble_bed/PB-006/data/proxy_centers_1000_PB-006-proxy-1000-seed02-stream-fall.csv`.
- Proxy quality check: the centre file contains 1000 pebbles; the settled height is 7.71755 mm; the final tail-step kinetic energy is 3.91e-13 J.
- Bonded-template initcheck: passed with 500000 subparticles, 5876000 intact internal bonds and zero precompression bond loss. The initcheck state and logs are archived in `simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed02-initcheck-20260531/`.
- Compression status: `PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable` completed normally. The final post/log/screen/data/mesh files are archived in `simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable-completed-20260531/`.
- Progress update at 2026-05-31 13:06 CST: seed1000-02 has entered the targeted local-dump window and written `post/bonds_window_20000.local` through `post/bonds_window_27000.local`. Thermo output shows the first bond loss at step 25000, top displacement 0.0599975 mm, with 15 newly broken bonds. Additional increments of 9 and 13 broken bonds appear at steps 26000 and 27000, giving 37 cumulative thermo-counted broken bonds by 0.0649975 mm. Mother-pebble localization is pending completion or a safe postprocessing checkpoint.
- Progress update at 2026-05-31 14:40 CST: local dumps have advanced through `post/bonds_window_40000.local`. After the early 37-bond onset cluster, the run shows a quiet interval from steps 28000-34000, then renewed bond loss at steps 35000, 36000, 37000, 39000 and 40000. The cumulative thermo-counted broken-bond total is 99 by step 40000, top displacement 0.0974975 mm. This resembles the onset-cluster/quiet-interval/renewed-growth motif seen in seed01, but mother-pebble localization should wait for postprocessing.
- Partial localization update at 2026-05-31 CST: a checkpoint analysis of available `bonds_window_20000.local` through `bonds_window_48000.local` produced `data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_breakage_events.csv`. Through 0.1174975 mm, the local-dump analysis finds 20 localized events, 180 broken bonds and 3 damaged mother pebbles. Damage is confined to the top height bin and involves mother pebbles 1000, 999 and 998, with 95, 51 and 34 broken bonds respectively. Treat this as a checkpoint only until the run completes and a final local dump is available.

Completed restartable run:

- Screen session: `pb006_1000_0p15_restart`
- Case id: `PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable`
- Monitor command: `scripts/monitor_pb006_restartable_run.sh`
- Purpose: recover the 0.10-0.15 mm post-onset window with flushed thermo and periodic restart files.
- Completion status at 2026-05-27 00:22 CST: the detached screen session has ended normally. The run reached step 61001, corresponding to 0.1500 mm top displacement, and wrote `post/bonds_final_61001.local`.
- Thermo-level sequence: the trajectory reproduced the completed 0.10 mm onset cluster with 53 cumulative broken bonds by 0.0950 mm, then stayed quiet through 0.1300 mm. New late-window bond loss appeared at steps 54000, 55000, 56000, 57000, 58000, 59000, 60000 and 61000, with increments of 1, 9, 1, 15, 8, 9, 1 and 1 broken bonds. The final cumulative broken-bond count is 98.
- Mother-pebble-resolved sequence after postprocessing: the 0.15 mm restartable case contains 15 localized events involving mother pebbles 961, 980 and 1000. All localized bond loss remains in the top height bin.

Completed randomized-orientation replicate:

- Screen session: `pb006_1000_orient02_0p15`
- Case id: `PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable`
- Orientation seed: `20260528`, using the same 1000-proxy seed01 centres.
- Completion status at 2026-05-27 18:44 CST: the detached screen session ended normally. The run reached step 61001, corresponding to 0.1500 mm top displacement, and wrote `post/bonds_final_61001.local`.
- Initialization control: 500000 subparticles; 5876000 intact internal bonds; zero broken bonds before compression.
- Thermo-level sequence: the first break occurs at step 30000, top displacement 0.0724975 mm. Cumulative broken bonds reach 95 by step 49000, top displacement 0.1199975 mm, and remain unchanged from 0.1200 to 0.1500 mm.
- Mother-pebble-resolved sequence after postprocessing: orient02 contains 9 localized events and 95 broken bonds, all in mother pebble 1000 and all in the top height bin. Compared with seed01, the onset location is reproduced but late-window propagation to neighbouring upper-layer pebbles is not reproduced.

## Postprocessing readiness

The completed 0.15 mm restartable case was postprocessed with:

```bash
scripts/postprocess_pb006_1000_0p15_restartable.sh
```

This script extracted thermo data, built mother-pebble-resolved breakage events by combining the completed 0.10 mm onset events with the 0.10-0.15 mm late-window local bond dumps, summarized damaged pebbles by height, appended the restartable case to the combined PB-006 event database, and regenerated the manuscript-ready event-database figure.

Key outputs:

- `data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable_breakage_events.csv`
- `tables/pb006_1000_0p15_restartable_summary.csv`
- `tables/pb006_breakage_event_database_summary.csv`
- `figures/pb006/pb006_breakage_event_database.svg`

Orient02 postprocessing used the generic scripts rather than the seed01-specific restartable postprocessor:

```bash
python3 scripts/extract_liggghts_thermo.py simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable-completed-20260527/log.liggghts --output data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_thermo.csv
python3 scripts/analyze_bed_breakage_events.py simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable-completed-20260527/post/bonds_window_*.local simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable-completed-20260527/post/bonds_final_*.local --npebbles 1000 --nspheres 500 --thermo data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_thermo.csv --series-output data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_per_pebble_series.csv --events-output data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_breakage_events.csv
python3 scripts/summarize_random_pack_breakage.py data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_breakage_events.csv --metadata simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable-completed-20260527/data/bonded_template_metadata_1000.csv --pebble-output data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_pebble_summary.csv --height-output data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_height_summary.csv
```

Orient02 key outputs:

- `data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_breakage_events.csv`
- `data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_per_pebble_series.csv`
- `data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_pebble_summary.csv`
- `data/processed/PB-006-bonded-randompack-1000-seed01-orient02-prod-0p15mm-targeted-window-restartable_height_summary.csv`
- `tables/pb006_1000_seed01_orient02_0p15_summary.csv`

Orientation-sensitivity comparison outputs:

- `tables/pb006_1000_orientation_sensitivity_metrics.csv`
- `figures/pb006/pb006_1000_orientation_sensitivity.svg`
- `figures/pb006/pb006_1000_orientation_sensitivity.pdf`
- `figures/pb006/pb006_1000_orientation_sensitivity.png`
- `figures/pb006/pb006_1000_orientation_sensitivity.tiff`

Combined event-database update:

- On 2026-05-31 CST, `seed01-1000-orient02-0p15` was added to `scripts/build_pb006_event_database.py`.
- `tables/pb006_breakage_event_database.csv`, `tables/pb006_breakage_event_database_summary.csv` and `figures/pb006/pb006_breakage_event_database.*` were regenerated. The summary now includes orient02 with 9 events, 95 broken bonds, 1 damaged mother pebble and first break at 0.0724975 mm in mother pebble 1000.

## Completed 1000-pebble seed02 0.15 mm case

The `PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable` compression case completed normally on 2026-05-31 CST. The detached screen session ended, the run reached step 61001, top displacement 0.1500 mm, and wrote `post/bonds_final_61001.local`. Thermo output ended with 316 cumulative broken bonds and final top force 40.260049 N.

Partial localization was updated on 2026-05-31 CST using the generic event scripts:

```bash
python3 scripts/extract_liggghts_thermo.py simulations/pebble_bed/PB-006/log.liggghts --output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_thermo.csv
python3 scripts/analyze_bed_breakage_events.py simulations/pebble_bed/PB-006/post/bonds_window_*.local --npebbles 1000 --nspheres 500 --thermo data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_thermo.csv --series-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_per_pebble_series.csv --events-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_breakage_events.csv
python3 scripts/summarize_random_pack_breakage.py data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_breakage_events.csv --metadata simulations/pebble_bed/PB-006/data/bonded_template_metadata_1000.csv --pebble-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_pebble_summary.csv --height-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_partial_height_summary.csv
```

Checkpoint interpretation through 0.1199975 mm:

- 22 localized events and 201 broken bonds have been assigned.
- Four top-bin mother pebbles are damaged: pebble 1000 has 95 broken bonds in 11 events, pebble 999 has 51 broken bonds in 5 events, pebble 998 has 51 broken bonds in 5 events, and pebble 997 has 4 broken bonds in 1 event.
- The first event occurs at step 25000, top displacement 0.0599975 mm, in mother pebble 1000.
- The damage sequence at this checkpoint showed top-layer cascade from mother pebble 1000 to 999, then 998 and 997.

Final generic postprocessing used the archived case bundle:

```bash
python3 scripts/extract_liggghts_thermo.py simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable-completed-20260531/log.liggghts --output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_thermo.csv
python3 scripts/analyze_bed_breakage_events.py simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable-completed-20260531/post/bonds_window_*.local simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable-completed-20260531/post/bonds_final_*.local --npebbles 1000 --nspheres 500 --thermo data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_thermo.csv --series-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_per_pebble_series.csv --events-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_breakage_events.csv
python3 scripts/summarize_random_pack_breakage.py data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_breakage_events.csv --metadata simulations/pebble_bed/PB-006/archive/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable-completed-20260531/data/bonded_template_metadata_1000.csv --pebble-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_pebble_summary.csv --height-output data/processed/PB-006-bonded-randompack-1000-seed02-prod-0p15mm-targeted-window-restartable_height_summary.csv
```

Final mother-pebble-resolved sequence:

- 31 localized events, 316 broken internal bonds and 5 damaged mother pebbles.
- All localized damage remains in the top height bin.
- Damaged mother pebbles are 1000, 999, 998, 997 and 949.
- Per-pebble totals are 121 broken bonds in pebble 1000, 51 in pebble 999, 80 in pebble 998, 61 in pebble 997 and 3 in pebble 949.
- First break occurs at 0.0599975 mm in mother pebble 1000; the last localized event occurs at 0.1499975 mm in mother pebble 949.

Database and figure updates:

- `seed02-1000-0p15-restartable` was added to `scripts/build_pb006_event_database.py`.
- `tables/pb006_breakage_event_database.csv`, `tables/pb006_breakage_event_database_summary.csv` and `figures/pb006/pb006_breakage_event_database.*` were regenerated.
- `tables/pb006_1000_seed02_0p15_summary.csv` was created.
- `tables/pb006_1000_orientation_sensitivity_metrics.csv` and `figures/pb006/pb006_1000_orientation_sensitivity.*` were regenerated with seed02 included as an independent-packing replicate.
