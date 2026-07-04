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

## Live recheck - 2026-07-04 21:12 CST

- Confirmed selected NAS target: `/Volumes/BulkArchive` (`//wangjian@qunhui925.local/BulkArchive`), 7.0 TiB total, 6.9 TiB available, about 1% used.
- Confirmed archived DEM raw-output folders on the 7 TiB volume:
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-006_large_archives_20260704` (about 23 GiB)
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-007_old_restart_data_20260704` (about 4.6 GiB)
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/large_raw_outputs_before_20260704_20260704` (about 2.0 GiB)
  - `/Volumes/BulkArchive/颗粒破碎统计研究_backup/raw_simulation_dumps_20260704_164309` (about 721 MiB)
  - `/Volumes/BulkArchive/颗粒破碎统计研究_backup/pb007_raw_outputs_20260704_171122` (about 1.8 GiB)
- Re-scanned the local workspace for raw-output files larger than 20 MB matching `*.dump`, `*dump*`, `*.local`, `*.restart`, `*.vtk`, `*.vtu`, `*.vtp`, `*.xyz` and `*.lammpstrj`; no remaining matches were found.
- Large files still present locally are manuscript figures, submission bundles, Git objects and source/vendor files. These were not moved because they are not raw DEM dump/restart outputs.
