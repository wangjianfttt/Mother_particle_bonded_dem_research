#!/usr/bin/env bash
set -euo pipefail

rigid_case="${1:-PB-007-rigid-surface-100-pilot}"
final_step="${2:-300000}"
stage_steps="${3:-5000}"
compress_steps="${4:-4000}"
post_steps="${5:-10000}"
top_speed="${6:-0.5}"
case_suffix="${7:-10um}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base_dir="$root_dir/simulations/pebble_bed/PB-007"
rigid_dir="$base_dir/cases/$rigid_case"
case_id="${rigid_case/rigid-surface/bonded-loadpath}-${case_suffix}"
case_dir="$base_dir/cases/$case_id"
template_dir="$root_dir/simulations/single_pebble/SP-SURFACE/templates/surface500_shell260"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"
step_padded="$(printf '%08d' "$final_step")"

mkdir -p "$case_dir/data" "$case_dir/meshes" "$case_dir/post"
cp "$template_dir/template.multisphere" "$case_dir/data/"
cp "$base_dir/in.pb007_bonded_loadpath_validation.lmp" "$case_dir/"

python3 "$root_dir/scripts/prepare_pb007_bonded_from_rigid.py" \
  --clumps "$rigid_dir/post/clumps_${step_padded}.local" \
  --sphere-dump "$rigid_dir/post/spheres_${step_padded}.dump" \
  --template "$template_dir/template.multisphere" \
  --insertion-reference-dump "$root_dir/simulations/single_pebble/SP-SURFACE/cases/SP-SURFACE-500-S260/post/particles_0.dump" \
  --far-origin-x 0.012 \
  --far-origin-y 0.012 \
  --far-origin-z 0.015 \
  --create-output "$case_dir/data/create_pebbles_far.inc" \
  --move-output "$case_dir/data/move_pebbles_to_pack.inc" \
  --metadata-output "$case_dir/data/bonded_template_metadata.csv" \
  --bounds-output "$case_dir/data/bed_bounds.csv"

read -r zhi npebbles < <(
  awk -F, 'NR==2 {print $6, $7}' "$case_dir/data/bed_bounds.csv"
)
python3 "$root_dir/scripts/create_box_meshes.py" \
  --output-dir "$case_dir/meshes" \
  --xlo -0.003 --xhi 0.003 --ylo -0.003 --yhi 0.003 \
  --zlo 0.0 --zhi "$zhi" --divisions 12

rm -rf "$case_dir/post"
mkdir -p "$case_dir/post"
(
  cd "$case_dir"
  "$lmp" -in in.pb007_bonded_loadpath_validation.lmp \
    -var npebbles "$npebbles" \
    -var stage_steps "$stage_steps" \
    -var compress_steps "$compress_steps" \
    -var post_steps "$post_steps" \
    -var top_speed "$top_speed" \
    -screen "screen_${case_id}.log" \
    -log log.liggghts
)

python3 "$root_dir/scripts/extract_liggghts_thermo.py" \
  "$case_dir/log.liggghts" \
  --output "$root_dir/data/processed/${case_id}_thermo.csv"

echo "$case_dir"
