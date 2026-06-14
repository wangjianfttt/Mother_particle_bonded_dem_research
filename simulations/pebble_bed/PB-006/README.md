# PB-006 random packed calibrated-template bed

Goal: production-style bed workflow for 500-1000 nominal 1 mm Li4SiO4 mother pebbles.

The workflow has two stages:

1. Settle monodisperse 1 mm proxy spheres under gravity in a container. These proxy spheres represent rigid mother pebbles and have no internal bonds, so no internal damage can occur during packing. The current production route uses `insert/rate/region` to pour particles from an upper factory region, followed by a tail relaxation after insertion stops.
2. Extract settled proxy centres, create calibrated 500-subparticle SP-002-CAL1 bonded templates far apart to form only internal bonds, then relocate each intact template to one settled proxy centre. Compression starts only after this relocation step, and internal bond breakage is then tracked per mother pebble.

This is the intended route for statistically meaningful breakage-event sequences. The PB-005 36-pebble cases remain debugging baselines.

Current smoke checks:

- `PB-006-proxy-500-stream-fall`: 500 proxy pebbles inserted in batches and settled under gravity. The final centre range is z = 0.00049954-0.00449391 m, giving a settled bed height of about 3.99 mm.
- `PB-006-bonded-randompack-500-stream-initcheck`: the 500 settled proxy centres were replaced by calibrated bonded templates, giving 250000 subparticles and `2938000 = 500 x 5876` intact internal bonds before compression.
- No internal bonds exist during proxy settling, and the bonded-template init check reports zero broken bonds before compression.

Current production compression:

- `PB-006-bonded-randompack-500-prod-0p20mm-primitivewall`: 500 calibrated bonded templates were compressed to 0.20 mm top displacement with primitive side/bottom walls and a moving mesh top plate.
- Up to the last local bond dump at 0.1975 mm, 271 internal bond breaks were localized to 11 mother-pebble events involving 5 mother pebbles. The first event occurred at 0.0725 mm in mother pebble 500, with 23 new broken bonds.
- The event sequence is height-localized: the top height bin accumulates 223 localized broken bonds and the next bin 48, while lower bins remain intact over this displacement window.
- The thermo endpoint at 0.20 mm reports 16 additional broken bonds after the last local bond dump; the input now includes a final-step bond-local dump for future runs so terminal breaks can also be assigned to mother pebbles.
- MPI/domain-decomposed bonded compression was tested but rejected for production because the initial intact-bond count became processor-decomposition dependent. Use single-rank bonded compression until that issue is resolved; proxy settling, seed generation and post-processing can still be parallelized across independent cases.

Seed tracking:

- `tables/pb006_seed_manifest.csv` records proxy insertion seeds, template orientation seeds, settled bed height, initialization bond counts and production status.
- `seed02` has completed proxy settling, bonded-template initialization and 0.20 mm production compression. It starts with the same `2938000` intact internal bonds and zero broken bonds before compression. The full bond-local analysis assigns 246 broken internal bonds to 9 events involving 4 mother pebbles. As in seed01, the first localized event occurs at 0.0725 mm in mother pebble 500 in the top height bin. The top height bin accumulates 210 broken bonds and the next bin 36, while all lower bins remain intact over this displacement range.
- `seed03` has also completed the full 0.20 mm production compression. It settles to a lower bed height of about 3.82 mm and produces stronger top loading: the final top force is 47.86 N, compared with about 27 N for seed01 and seed02. The first localized event again occurs at 0.0725 mm in mother pebble 500. By 0.20 mm, seed03 accumulates 559 localized broken internal bonds across 22 events and 7 mother pebbles. Damage is still restricted to the top two height bins, with 500 broken bonds in the top bin and 59 in the next bin.
- Packing descriptors have been computed for seed01-seed03. At a 1.02 mm geometric-contact cutoff, seed03 has the lowest bed height, the largest top-bin population and the highest top-bin mean geometric degree. The same qualitative trend persists for 1.00-1.10 mm cutoffs. This explains why the current interpretation is that seed03 has a stronger upper-bed load path, but a direct contact-force-chain analysis is still needed.

Descriptor and comparison files:

- `tables/pb006_three_seed_packing_descriptors_cutoff1p02mm.csv`
- `tables/pb006_three_seed_active_pebble_descriptors_cutoff1p02mm.csv`
- `tables/pb006_packing_descriptor_cutoff_sensitivity.csv`
- `figures/pb006/pb006_three_seed_packing_breakage.svg`

Post-processing route for production compression:

```bash
python3 scripts/analyze_bed_breakage_events.py simulations/pebble_bed/PB-006/post/bonds_*.local \
  --npebbles 500 --nspheres 500 \
  --thermo data/processed/<case>_thermo.csv \
  --series-output data/processed/<case>_per_pebble_series.csv \
  --events-output data/processed/<case>_breakage_events.csv

python3 scripts/summarize_random_pack_breakage.py data/processed/<case>_breakage_events.csv \
  --metadata simulations/pebble_bed/PB-006/data/bonded_template_metadata_500.csv \
  --pebble-output data/processed/<case>_pebble_summary.csv \
  --height-output data/processed/<case>_height_summary.csv
```

Contact-force-chain route for future production compression:

- A direct `compute pair/gran/local id force force_normal force_tangential` route was tested, but this LIGGGHTS-INL version requires `pair/gran/local` and `wall/gran/local` computes to be defined before the first `run`. PB-006 must first run one step to create internal bonds before relocating templates and defining the real compression walls, so a direct contact-local workflow needs a separate restart/rerun design.
- The current production input therefore remains on the stable bond-local workflow. The top-wall total force is available from `mesh/surface/stress`, and force-path evidence is currently produced from overlap-derived proxy networks using saved particle dumps.

Future native contact-force post-processing, once a restart/rerun workflow is available:

```bash
python3 scripts/analyze_pb006_contact_network.py \
  --pair-dumps simulations/pebble_bed/PB-006/post/contacts_*.local simulations/pebble_bed/PB-006/post/contacts_final_*.local \
  --pair-summary-output tables/<case>_contact_pair_summary.csv \
  --pair-edge-output tables/<case>_contact_pair_edges.csv
```

An exploratory aggregation from existing `particles_*.dump` files was added in `scripts/analyze_pb006_mother_forces.py`, producing `tables/pb006_seed02_mother_force_focus.csv` and `tables/pb006_seed03_mother_force_focus.csv`. These tables are useful as a diagnostic, but particle `fx/fy/fz` does not recover the top-plate reaction accurately in the existing dumps. They should not be used as the main force-chain evidence.

The current force-path proxy uses `scripts/analyze_pb006_overlap_force_network.py`, which reconstructs inter-mother overlap edges from particle dumps and weights each overlap by `overlap^(3/2)`. It produces:

- `tables/pb006_seed02_overlap_force_proxy_summary.csv`
- `tables/pb006_seed03_overlap_force_proxy_summary.csv`
- `tables/pb006_seed02_overlap_force_proxy_edges.csv`
- `tables/pb006_seed03_overlap_force_proxy_edges.csv`
- `tables/pb006_seed02_overlap_force_proxy_topwall.csv`
- `tables/pb006_seed03_overlap_force_proxy_topwall.csv`
- `figures/pb006/pb006_seed02_seed03_overlap_force_proxy.svg`

1000-pebble scale-up route:

- `PB-006-proxy-1000-seed01-stream-fall` settled 1000 proxy mother pebbles to a bed height of 7.912 mm.
- `PB-006-bonded-randompack-1000-seed01-initcheck-light` replaced those centres with 1000 SP-002-CAL1 bonded templates and reported `5876000 = 1000 x 5876` intact internal bonds, with zero internal bond breaks before compression.
- Full particle and bond-local dumps are too expensive for the first 1000-pebble scan. The current diagnostic route is `in.pb006_bonded_compression_thermoonly.lmp`, launched by `scripts/run_pb006_bonded_compression_thermoonly.sh`. It keeps the same bonded model and template injection workflow, writes thermo every 1000 steps, suppresses periodic particle and bond-local dumps, and writes only a final bond-local dump.
- The first objective of the thermo-only 1000-pebble case is to determine the displacement at which cumulative bond breaks first appear and whether this onset is consistent with the 500-pebble three-seed set. Mother-pebble localization requires either a final local dump after the short scan or a later targeted local-dump rerun around the onset window.
- `PB-006-bonded-randompack-1000-seed01-prod-0p10mm-thermoonly` reached first cumulative bond loss at 0.0675 mm and ended at 0.10 mm with 53 broken internal bonds. Final-dump localization assigns all 53 broken bonds to top mother pebble 1000.
- The targeted follow-up route is `in.pb006_bonded_compression_targeted_window.lmp`, launched by `scripts/run_pb006_bonded_compression_targeted_window.sh`. It runs the same model without bond-local dumps until the onset window, then writes `bonds_window_*.local` every 1000 steps plus a final local dump. This is intended to recover the 1000-pebble mother-pebble event sequence without saving full-history bond dumps.
- `PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window` completes that route. The pre-window segment ends at 0.0575 mm with zero broken bonds. The local-dump window resolves six events at 0.0675, 0.0700, 0.0775, 0.0900, 0.0925 and 0.0950 mm. The event increments are 15, 8, 20, 6, 2 and 2 broken bonds, all assigned to mother pebble 1000 in the highest height bin.
- Processed outputs: `data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window_breakage_events.csv`, `data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window_pebble_summary.csv`, `data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window_height_summary.csv`, `tables/pb006_1000_targeted_window_summary.csv` and `figures/pb006/pb006_1000_targeted_window_event_sequence.svg`.
