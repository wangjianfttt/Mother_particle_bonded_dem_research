# NAS large-dump offload check, 2026-07-04

## Selected NAS target

- NAS volume: `/Volumes/BulkArchive`
- Network share: `//wangjian@qunhui925.local/BulkArchive`
- Capacity: 7.0 TiB total, about 6.9 TiB available at the time of check
- Intended role: bulk backup volume for old raw DEM outputs

## Existing raw-output archives

The selected 7 TiB NAS volume already contains the main old raw DEM output
archives for this project:

| Archive location | Size | Contents |
|---|---:|---|
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-006_large_archives_20260704` | 23 GiB | PB-006 large raw archives |
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-007_old_restart_data_20260704` | 4.6 GiB | PB-007 old restart/data outputs |
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/large_raw_outputs_before_20260704_20260704` | 2.0 GiB | pre-2026-07-04 large raw outputs |

The archive root currently holds about 30 GiB:

`/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究`

## Fresh scan result

The following locations were checked for remaining raw DEM output files larger
than 20 MiB in the usual dump/restart/local/VTK/trajectory classes:

- `/Users/wangjian-macbook13/Documents/颗粒破碎统计研究`
- `/Users/wangjian-macbook13/Library/CloudStorage/SynologyDrive-mac/颗粒破碎研究claude`
- `/Users/wangjian-macbook13/Library/CloudStorage/SynologyDrive-mac/论文相关/分数阶模型研究/project/cases`

No additional files above 20 MiB were found in these raw-output classes:

- `*dump*`
- `*.local`
- `*.restart`
- `restart*`
- `*.vtk`, `*.vtu`, `*.vtp`
- `*.lammpstrj`
- `*.xyz`
- `*.data`

Remaining large files in the local manuscript project are mainly TIFF figures,
submission-package figure copies, and Git pack files. They were not moved in
this pass because they are not old raw DEM dump/restart outputs.

## Restore rule

Restore archived raw files only when needed:

```bash
rsync -a /Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/<archive>/ \
  /Users/wangjian-macbook13/Documents/颗粒破碎统计研究/
```

Before using restored raw files for analysis, compare them against the
corresponding manifest or checksum file in `docs/nas_offload_manifests/` or in
the NAS archive directory.
