# NAS raw-dump storage check, 2026-07-05

## Target NAS volume

- Selected volume: `/Volumes/BulkArchive`
- Network share: `//wangjian@qunhui925.local/BulkArchive`
- Capacity at check time: 7.0 TiB total, 6.9 TiB available
- Role: bulk backup volume for old DEM raw outputs

## Verified NAS archives

The following old raw DEM outputs are already stored on the selected NAS
backup volume:

| Archive location | Size | File count | Verification |
|---|---:|---:|---|
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-006_large_archives_20260704` | 23.430 GiB | 199 | rsync size verification and manifest present |
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/PB-007_old_restart_data_20260704` | 4.634 GiB | 33 | SHA256 manifest recorded |
| `/Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/large_raw_outputs_before_20260704_20260704` | 1.978 GiB | 43 | SHA256 manifest recorded |
| `/Volumes/BulkArchive/颗粒破碎统计研究_backup/raw_simulation_dumps_20260704_164309` | 0.704 GiB | 6 | `gzip -t old_raw_simulation_dumps.tar.gz` passed |
| `/Volumes/BulkArchive/颗粒破碎统计研究_backup/pb007_raw_outputs_20260704_171122` | 1.783 GiB | 5 | `gzip -t pb007_raw_outputs.tar.gz` passed |

Total verified raw-output storage on the NAS is about 32.53 GiB.

## Local workspace scan

Project root checked:

`/Users/wangjian-macbook13/Documents/颗粒破碎统计研究`

No remaining raw DEM output files above 10 MiB were found in the usual
simulation-output classes:

- `*.dump`
- `dump.*`
- `*.local`
- `*.restart`
- `restart*`
- `*.vtk`
- `*.vtu`
- `*.vtp`
- `*.lammpstrj`

All raw-like files remaining in the local workspace total only 3.84 MiB. The
largest remaining matches are small source-code, documentation or figure-helper
files, not large simulation dumps. Local files above 50 MiB are mainly TIFF
figures, submission-package figure copies and Git pack files, so they were not
moved in this raw-dump cleanup pass.

## Existing source-removal records

- `docs/nas_offload_pb006_removed_sources.tsv`: 197 PB-006 local source files removed after verification
- `docs/nas_offload_manifests/pb007_old_restart_data_20260704_files.txt`: 31 old PB-007 restart/data files moved
- `docs/nas_offload_manifests/large_raw_outputs_before_20260704_20260704_files.txt`: 43 older raw-output files archived

## Restore notes

Restore archived raw files only when needed. For path-preserving archives under
`DEM_ARCHIVE`, run from the project root:

```bash
rsync -a /Volumes/BulkArchive/DEM_ARCHIVE/颗粒破碎统计研究/<archive>/ ./
```

For compressed archives under `/Volumes/BulkArchive/颗粒破碎统计研究_backup`,
extract into a temporary restore directory first, inspect the manifest, then
copy back only the required case files.
