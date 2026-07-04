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

## Live recheck - 2026-07-04 23:10 CST

- Confirmed the backup target remains the nearly empty 7 TiB Synology volume:
  `/Volumes/BulkArchive` (`//wangjian@qunhui925.local/BulkArchive`), 7.0 TiB total, 6.9 TiB available, about 1% used.
- Confirmed DEM raw-output archives already stored on that volume:
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-006_large_archives_20260704`: 199 files, 23.43 GiB.
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-007_old_restart_data_20260704`: 33 files, 4.63 GiB.
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/large_raw_outputs_before_20260704_20260704`: 43 files, 1.98 GiB.
- Re-scanned local `simulations/` and `data/` for raw-output files larger than 20 MB matching `*dump*`, `*.local`, `*.restart`, `*restart*`, `*.vtk`, `*.vtp`, `*.vtu`, `*.lammpstrj`, `*.xyz` and `*.data`; remaining match count: 0.
- No additional local large DEM dump/restart files were moved in this pass because the local raw-output residue is already clear. Remaining local large files are manuscript figures, submission-package copies, Git objects and source/vendor files.

## Live recheck - 2026-07-04 23:40 CST

- Confirmed the selected backup volume is still `/Volumes/BulkArchive`
  (`//wangjian@qunhui925.local/BulkArchive`): 7.0 TiB total, 6.9 TiB available, about 1% used.
- Confirmed raw-output backup folders on the 7 TiB volume:
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-006_large_archives_20260704`: about 23 GiB.
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-007_old_restart_data_20260704`: about 4.6 GiB.
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/large_raw_outputs_before_20260704_20260704`: about 2.0 GiB.
  - `/Volumes/BulkArchive/颗粒破碎统计研究_backup/raw_simulation_dumps_20260704_164309`: about 721 MiB.
  - `/Volumes/BulkArchive/颗粒破碎统计研究_backup/pb007_raw_outputs_20260704_171122`: about 1.8 GiB.
- Verified archive metadata currently visible on NAS:
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-006_large_archives_20260704/nas_offload_pb006_large_files_manifest.csv`
  - `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-007_old_restart_data_20260704/SHA256_FROM_PROJECT_ROOT.txt`
- Re-scanned local `simulations/` and `data/` for raw-output files larger than 20 MB matching `*dump*`, `*.local`, `*.restart`, `*restart*`, `*.vtk`, `*.vtp`, `*.vtu`, `*.lammpstrj`, `*.xyz` and `*.data`; remaining match count: 0.
- No further files were moved in this pass. The large files remaining in the local workspace are manuscript figures, submission packages, Git objects and source/vendor files, so moving them would not match the raw DEM dump/restart backup request.
