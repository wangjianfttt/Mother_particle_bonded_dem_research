# Disk cleanup log, 2026-06-01

Scope: conservative cleanup of regenerated or already archived working data in the pebble-breakage project directory.

Pre-cleanup state recorded during audit:

- Project `simulations/`: 34G.
- `simulations/pebble_bed/PB-006/post/`: 7.4G.
- `simulations/single_pebble/SP-002/post/`: 118M.
- Old PB-006 forced restart data files: about 5.9G total.
- Filesystem free space: 28Gi by `df -h .`.

Deleted items:

- `simulations/pebble_bed/PB-006/post/`.
- `simulations/single_pebble/SP-002/post/`.
- `simulations/pebble_bed/PB-006/restart_forced_liggghts_1132.data`.
- `simulations/pebble_bed/PB-006/restart_forced_liggghts_2359.data`.
- `simulations/pebble_bed/PB-006/restart_forced_liggghts_3078.data`.
- `simulations/pebble_bed/PB-006/restart_forced_liggghts_757.data`.
- Temporary LaTeX build sidecars for `manuscript/nuclear_fusion_iop_submission`.

Post-cleanup checks:

- Project `simulations/`: 20G.
- `simulations/pebble_bed/PB-006/`: 19G.
- `simulations/single_pebble/SP-002/`: 430M.
- Critical seed02 final local dump remains in the completed archive.
- `manuscript/nuclear_fusion_iop_submission.pdf` remains present.
- `submission_packages/nuclear_fusion_repro_package.zip` remains present.
- No detached screen simulations were running at cleanup time.

Estimated project-local space recovered: about 14G.

Conservative exclusions:

- Completed `archive/` directories were retained because they are the raw evidence chain for PB-006 and SP-002.
- Submission figures, processed tables, manuscript files, and the reproducibility package were retained.
- `.git/objects` was not modified manually.
