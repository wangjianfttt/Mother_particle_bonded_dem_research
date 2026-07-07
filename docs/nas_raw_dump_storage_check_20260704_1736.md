# NAS raw-dump storage check, 2026-07-04 17:36 CST

## Target volume

- Mounted NAS volume: `/Volumes/BulkArchive`
- Network share: `//wangjian@qunhui925.local/BulkArchive`
- Capacity check: 7.0 TiB total, about 6.9 TiB available
- Use: bulk backup for completed DEM raw outputs

## Archived raw-output locations

| Archive | Contents | Size/status |
|---|---:|---:|
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-006_large_archives_20260704` | PB-006 large archives | 197 verified files, 23.43 GiB |
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-007_old_restart_data_20260704` | old PB-007 restart/data files | 31 verified files, 4.6 GiB |
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/large_raw_outputs_before_20260704_20260704` | pre-2026-07-04 large raw outputs | 43 verified files, 2.0 GB |
| `/Volumes/BulkArchive/颗粒破碎统计研究_backup/raw_simulation_dumps_20260704_164309` | compressed old dump/local/restart backup | 11,909 entries, archive check passed |
| `/Volumes/BulkArchive/颗粒破碎统计研究_backup/pb007_raw_outputs_20260704_171122` | compressed PB-007 dump/local/restart backup | 579 entries, archive check passed |

## Local workspace check

Local project:

`<project-root>`

Fresh scan result:

- No remaining large raw DEM files above 20 MB in the usual output classes:
  `*.dump`, `*.local`, `*.restart`, `*.vtk`, `*.vtu`, `*.vtp`, `*.xyz`,
  `*.lammpstrj`.
- Remaining large local files are mainly manuscript TIFF figures, Git objects,
  LIGGGHTS source files and submission-package copies. These were left in
  place because they are not raw dump outputs.

## Restore rule

Restore archived files with `rsync -a` from the corresponding NAS archive back
to the project root. Use the SHA256 or archive manifests recorded in
`docs/nas_offload_manifests/` and the NAS archive folders before using restored
raw files for analysis.
