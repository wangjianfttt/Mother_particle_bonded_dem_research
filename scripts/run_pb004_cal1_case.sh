#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-PB-004-CAL1-12pebble}"
relax_steps="${2:-1000}"
compress_steps="${3:-60000}"
top_vz="${4:--0.5}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-004"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"
out_csv="$root_dir/data/processed/${case_id}_thermo.csv"

cd "$case_dir"
rm -rf post log.liggghts warnings.liggghts "screen_${case_id}.log"
mkdir -p post
"$lmp" -in in.pb004_cal1_staged_compression.lmp \
  -var relax_steps "$relax_steps" \
  -var compress_steps "$compress_steps" \
  -var top_vz "$top_vz" \
  -screen "screen_${case_id}.log" \
  -log log.liggghts

python3 "$root_dir/scripts/extract_liggghts_thermo.py" log.liggghts --output "$out_csv"
echo "$out_csv"
