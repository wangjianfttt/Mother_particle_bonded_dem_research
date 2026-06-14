# PB-007 step-relaxed validation status

Updated: 2026-06-12 CST

## Active case

`PB-007-bonded-steprelaxed-100-pilot-5um-steprelaxed`

Command:

```bash
scripts/run_pb007_bonded_step_relaxed_validation.sh \
  PB-007-rigid-surface-100-pilot 300000 \
  5000 1000 20000 0.2 5 5um-steprelaxed
```

## Purpose

This case replaces the invalid restart-continuation route with a single in-run step-relaxed protocol. It tests whether the corrected PB-007 100-mother-pebble bed can transmit load before any internal bond loss.

## Acceptance logic

The previous raw top/bottom absolute-force ratio is not the correct gate because the bottom wall carries bed self-weight before top compression. The active gate is therefore gravity-baseline-corrected incremental wall-force balance:

- baseline = last zero-top-force state before compression;
- incremental all-wall force = current six-wall vertical force minus baseline six-wall vertical force;
- incremental residual = mismatch between incremental all-wall force magnitude and top-wall load, normalized by top-wall load.

The case also requires zero internal-bond loss and native contact-force output at the final state.

## Final post-processed evidence

The run completed and wrote final particle, pair-local, wall-local and restart files in:

`simulations/pebble_bed/PB-007/cases/PB-007-bonded-steprelaxed-100-pilot-5um-steprelaxed/post`

Final analysis products:

- thermo history: `data/processed/PB-007-bonded-steprelaxed-100-pilot-5um-steprelaxed_thermo.csv`;
- acceptance table: `tables/pb007_bonded_steprelaxed_100_5um_acceptance_summary.csv`;
- native mother-pebble graph: `tables/pb007_bonded_steprelaxed_100_5um_native_summary.csv`;
- validation figure: `figures/pb007/pb007_step_relaxed_validation_5um.png` and `.pdf`.

Key values from the last valid physical thermo row at step 110001:

- top-wall displacement: 5.0 micrometres;
- top-wall load: 1.713e-4 N;
- gravity-baseline-corrected incremental six-wall force: 1.704e-4 N;
- incremental wall-force balance residual: 0.542%;
- kinetic energy: 1.393e-11 J;
- initial/minimum internal intact bonds: 493,500/493,500;
- maximum broken internal bonds over the output history: 0.

Native final local-contact analysis gives 165 mother-mother force edges and 298 inter-pebble subcontacts. The top-loaded set reaches 99 of 100 mother pebbles and includes 26 bottom-contacting mother pebbles, so the final native force graph is spanning in the top-to-bottom sense.

Note: the LIGGGHTS `run 0` line written after final local dumps reports `bond_int = 0` and approximately doubled wall-stress values. It is treated as an output-trigger artefact. The acceptance table uses the last valid row with `bond_int > 0`; the final local dumps are used for network topology, not for the force-balance scalar.

## Current interpretation

This case passes the PB-007 pre-damage force-transmission acceptance gate for a 100-mother-pebble pilot: the bed remains undamaged, the native contact graph spans from the top-loaded region to bottom-contacting pebbles, and the gravity-baseline-corrected six-wall incremental force closes to within 1% at 5 micrometres. This is sufficient to replace the invalid PB-006 force-transmission premise and to justify launching the corrected PB-007 fracture-sequence calculation. It is not yet a fracture-statistics result.
