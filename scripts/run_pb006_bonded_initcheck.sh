#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-PB-006-bonded-initcheck}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-006"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"
out_csv="$root_dir/data/processed/${case_id}_thermo.csv"

cd "$case_dir"
rm -f log.liggghts warnings.liggghts "screen_${case_id}.log"
"$lmp" -in in.pb006_bonded_initcheck.lmp \
  -screen "screen_${case_id}.log" \
  -log log.liggghts

python3 "$root_dir/scripts/extract_liggghts_thermo.py" log.liggghts --output "$out_csv"
echo "$out_csv"
