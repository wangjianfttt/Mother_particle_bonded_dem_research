#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-PB-007-rigid-surface-50-smoke}"
npebbles="${2:-50}"
settle_steps="${3:-300000}"
young="${4:-5.0e7}"
dt="${5:-2.0e-7}"
insert_seed="${6:-32452843}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base_dir="$root_dir/simulations/pebble_bed/PB-007"
template_dir="$root_dir/simulations/single_pebble/SP-SURFACE/templates/surface500_shell260"
case_dir="$base_dir/cases/$case_id"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"

mkdir -p "$case_dir/data" "$case_dir/post"
cp "$template_dir/template_rigid.multisphere" "$case_dir/data/"
cp "$base_dir/in.pb007_rigid_surface_settle.lmp" "$case_dir/"
rm -rf "$case_dir/post"
mkdir -p "$case_dir/post"

(
  cd "$case_dir"
  "$lmp" -in in.pb007_rigid_surface_settle.lmp \
    -var npebbles "$npebbles" \
    -var settle_steps "$settle_steps" \
    -var young "$young" \
    -var dt "$dt" \
    -var insert_seed "$insert_seed" \
    -screen "screen_${case_id}.log" \
    -log log.liggghts
)

echo "$case_dir"
