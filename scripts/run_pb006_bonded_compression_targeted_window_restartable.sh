#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-PB-006-bonded-randompack-1000-targeted-window-restartable}"
relax_steps="${2:-1000}"
compress_steps="${3:-60000}"
top_vz="${4:--0.5}"
thermo_every="${5:-1000}"
pre_window_steps="${6:-39000}"
restart_every="${7:-1000}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-006"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"
out_csv="$root_dir/data/processed/${case_id}_thermo.csv"
np="${NP:-1}"

cd "$case_dir"
rm -rf post log.liggghts warnings.liggghts "screen_${case_id}.log"
mkdir -p post
if [[ "$np" -gt 1 ]]; then
  runner=(mpirun -np "$np" "$lmp")
else
  runner=("$lmp")
fi

"${runner[@]}" -in in.pb006_bonded_compression_targeted_window_restartable.lmp \
  -var relax_steps "$relax_steps" \
  -var compress_steps "$compress_steps" \
  -var top_vz "$top_vz" \
  -var thermo_every "$thermo_every" \
  -var pre_window_steps "$pre_window_steps" \
  -var restart_every "$restart_every" \
  -screen "screen_${case_id}.log" \
  -log log.liggghts

python3 "$root_dir/scripts/extract_liggghts_thermo.py" log.liggghts --output "$out_csv"
echo "$out_csv"
