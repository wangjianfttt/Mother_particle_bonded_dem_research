# PB-006 restartable 1000-pebble run rules

These rules apply to `PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable`, currently running in detached screen session `pb006_1000_0p15_restart`.

## Continue-running conditions

Continue the single-core run when all of the following hold:

- The LIGGGHTS process remains active and CPU-bound.
- `log.liggghts` advances by at least one thermo point over the expected single-core wall time.
- Atom count remains 500000.
- `bond_intact` and `bond_bro` evolve plausibly; no lost atoms, `nan`, `inf` or bond-missing errors appear.
- At least one of `post/restart_pb006_a.liggghts` or `post/restart_pb006_b.liggghts` has a recent timestamp and normal size.
- Available disk space remains comfortably above the expected local-dump and restart output volume.

## Stop-or-pause conditions

Pause or terminate only if one of the following occurs:

- Multiple checks show no timestep progress and no restart/log update.
- The process is not CPU-bound and appears blocked on I/O or dead.
- Log output reports lost atoms, `nan`, `inf`, bond-atom missing errors or extreme force/energy blow-up.
- Restart files stop updating or both appear truncated.
- Disk free space drops below a safe margin for the remaining local dumps and restart files.
- Local dump I/O after the targeted window dominates runtime so strongly that the run risks failure before completion.

## MPI policy

Do not switch the current 0.15 mm production run to MPI midstream. It is better to complete one credible single-core restartable trajectory than to introduce a second source of numerical path divergence.

MPI should be tested only as a separate short-window diagnostic copied from a restart file:

1. Copy the latest restart files and input state to a separate case directory.
2. Run 1000-3000 steps using 1, 2, 4 and optionally 8 ranks.
3. Compare atom count, wall force, cumulative broken bonds, kinetic energy and restart readability.
4. Use MPI only for future deeper windows if short-window results are stable enough for the intended claim.

## Restart continuation cautions

If a manual `read_restart` continuation is needed, confirm the following before interpreting data:

- Reapply the same units, atom style, boundary, `newton`, communication, neighbor and granular material settings.
- Recreate mesh/wall fixes consistently; do not assume all mesh motion state is automatically restored.
- Preserve timestep numbering unless the whole post-processing chain is updated.
- Recreate thermo, computes, dumps and restart commands after `read_restart`.
- Run 10-100 steps first and verify continuity of wall force, atom count, bond count and energy.

## Post-run processing order

1. Confirm final timestep and target displacement.
2. Extract thermo with `scripts/extract_liggghts_thermo.py`.
3. Analyze local bond dumps with `scripts/analyze_bed_breakage_events.py`.
4. Summarize damaged pebbles and height bins with `scripts/summarize_random_pack_breakage.py`.
5. Rebuild `tables/pb006_breakage_event_database.csv`.
6. Regenerate PB-006 event figures.
7. Archive raw local dumps and logs under `simulations/pebble_bed/PB-006/archive/`.
8. Update `manuscript/main_text_v2.md`, `docs/pb006_mainline_status.md` and `tables/pb006_seed_manifest.csv`.

