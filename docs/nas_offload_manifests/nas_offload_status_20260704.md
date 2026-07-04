# NAS offload status - 2026-07-04

Workspace: `/Users/wangjian-macbook13/Documents/颗粒破碎统计研究`

NAS target selected for backup:

- `/Volumes/BulkArchive`
- Capacity check: 7.0 TiB total, 6.9 TiB available, about 1% used

Archived location:

- `/Volumes/BulkArchive/颗粒破碎统计研究_backup_20260704`

Archived content already present on NAS:

- `raw_simulation_archives/`
- `obsolete_submission_packages/`
- `MOVE_MANIFEST.txt`
- `MOVE_MANIFEST_POSTCHECK.txt`

Post-check summary:

- No remaining local simulation raw-output files were found under `simulations/` with the following suffixes or patterns: `.local`, `.restart`, `.dump`, `dump.*`, `.lammpstrj`, `.vtk`, `.vtu`, `.data`.
- Remaining local project size is dominated by figure files, submission-package copies, and Git history, not by DEM dump/restart files.
- Current manuscript-facing and reproducibility files were left in place.

