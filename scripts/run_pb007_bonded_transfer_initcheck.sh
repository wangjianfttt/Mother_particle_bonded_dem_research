#!/usr/bin/env bash
set -euo pipefail

rigid_case="${1:-PB-007-rigid-surface-20-pilot}"
final_step="${2:-200000}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base_dir="$root_dir/simulations/pebble_bed/PB-007"
rigid_dir="$base_dir/cases/$rigid_case"
case_id="${rigid_case/rigid-surface/bonded-transfer}"
case_dir="$base_dir/cases/$case_id"
template_dir="$root_dir/simulations/single_pebble/SP-SURFACE/templates/surface500_shell260"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"
step_padded="$(printf '%08d' "$final_step")"

mkdir -p "$case_dir/data" "$case_dir/post"
cp "$template_dir/template.multisphere" "$case_dir/data/"
cp "$base_dir/in.pb007_bonded_transfer_initcheck.lmp" "$case_dir/"

python3 "$root_dir/scripts/prepare_pb007_bonded_from_rigid.py" \
  --clumps "$rigid_dir/post/clumps_${step_padded}.local" \
  --sphere-dump "$rigid_dir/post/spheres_${step_padded}.dump" \
  --template "$template_dir/template.multisphere" \
  --insertion-reference-dump "$root_dir/simulations/single_pebble/SP-SURFACE/cases/SP-SURFACE-500-S260/post/particles_0.dump" \
  --create-output "$case_dir/data/create_pebbles_far.inc" \
  --move-output "$case_dir/data/move_pebbles_to_pack.inc" \
  --metadata-output "$case_dir/data/bonded_template_metadata.csv" \
  --bounds-output "$case_dir/data/bed_bounds.csv"

npebbles="$(awk -F, 'NR==2 {print $7}' "$case_dir/data/bed_bounds.csv")"
rm -rf "$case_dir/post"
mkdir -p "$case_dir/post"

(
  cd "$case_dir"
  "$lmp" -in in.pb007_bonded_transfer_initcheck.lmp \
    -var npebbles "$npebbles" \
    -screen "screen_${case_id}.log" \
    -log log.liggghts
)

echo "$case_dir"
