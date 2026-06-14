#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-PB-006-proxy-500-settle}"
npebbles="${2:-500}"
settle_steps="${3:-300000}"
dump_every="${4:-10000}"
insert_seed="${5:-32452843}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-006"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"
out_csv="$root_dir/data/processed/${case_id}_thermo.csv"

cd "$case_dir"
rm -rf post log.liggghts warnings.liggghts "screen_${case_id}.log"
mkdir -p post data meshes
"$lmp" -in in.pb006_proxy_settle.lmp \
  -var npebbles "$npebbles" \
  -var settle_steps "$settle_steps" \
  -var dump_every "$dump_every" \
  -var insert_seed "$insert_seed" \
  -screen "screen_${case_id}.log" \
  -log log.liggghts

python3 "$root_dir/scripts/extract_liggghts_thermo.py" log.liggghts --output "$out_csv"
latest_dump="$(find post -maxdepth 1 -name 'proxy_*.dump' | sort -V | tail -1)"
python3 "$root_dir/scripts/extract_proxy_pack_centers.py" "$latest_dump" \
  --output "$case_dir/data/proxy_centers_${npebbles}_${case_id}.csv" \
  --limit "$npebbles"
cp "$case_dir/data/proxy_centers_${npebbles}_${case_id}.csv" "$case_dir/data/proxy_centers_${npebbles}.csv"
echo "$out_csv"
echo "$case_dir/data/proxy_centers_${npebbles}_${case_id}.csv"
