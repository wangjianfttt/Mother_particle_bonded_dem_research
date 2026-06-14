#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-005"
mkdir -p "$case_dir/data" "$case_dir/meshes"

orientation_args=()
if [[ -n "${RANDOM_ORIENTATION_SEED:-}" ]]; then
  orientation_args=(--random-orientation-seed "$RANDOM_ORIENTATION_SEED")
fi

python3 "$root_dir/scripts/generate_staged_bed_variable_move.py" \
  --create-output "$case_dir/data/create_pebbles_far.inc" \
  --move-output "$case_dir/data/move_pebbles_to_bed.inc" \
  --nx 3 --ny 3 --nz 4 \
  --far-spacing 0.00135 \
  --target-spacing 0.00102 \
  --far-z0 -0.00135 \
  --target-z0 -0.00102 \
  "${orientation_args[@]}"

python3 "$root_dir/scripts/generate_weak_plane_template.py" \
  --input "$root_dir/simulations/single_pebble/SP-002/data/li4sio4_sp_500_nooverlap.multisphere" \
  --output "$case_dir/data/li4sio4_sp_500_cal1_x.multisphere" \
  --normal 1 0 0 \
  --offset 0.0

python3 "$root_dir/scripts/create_box_meshes.py" \
  --output-dir "$case_dir/meshes" \
  --xlo -0.00156 --xhi 0.00156 \
  --ylo -0.00156 --yhi 0.00156 \
  --zlo -0.001506 --zhi 0.00265 \
  --divisions 12
