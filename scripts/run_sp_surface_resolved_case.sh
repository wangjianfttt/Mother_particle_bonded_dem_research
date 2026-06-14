#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-SP-SURFACE-500-S260}"
top_vz="${2:--0.1}"
nsteps="${3:-600000}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base_dir="$root_dir/simulations/single_pebble/SP-SURFACE"
template_dir="$base_dir/templates/surface500_shell260"
case_dir="$base_dir/cases/$case_id"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"

mkdir -p "$case_dir/data" "$case_dir/meshes"
cp "$template_dir/template.multisphere" "$case_dir/data/template.multisphere"

read -r zmin zmax < <(
  python3 - "$case_dir/data/template.multisphere" <<'PY'
from pathlib import Path
import sys

zmin = float("inf")
zmax = float("-inf")
for line in Path(sys.argv[1]).read_text().splitlines():
    x, y, z, radius, _ = line.split()
    z = float(z)
    radius = float(radius)
    zmin = min(zmin, z - radius)
    zmax = max(zmax, z + radius)
print(f"{zmin - 1.0e-6:.12e} {zmax + 1.0e-4:.12e}")
PY
)

python3 "$root_dir/scripts/create_plate_stl.py" \
  --z="$zmin" --normal-z 1.0 --divisions 12 \
  --output "$case_dir/meshes/bottom_plate.stl"
python3 "$root_dir/scripts/create_plate_stl.py" \
  --z="$zmax" --normal-z=-1.0 --divisions 12 \
  --output "$case_dir/meshes/top_plate.stl"

cp "$root_dir/simulations/single_pebble/SP-RESOLUTION/in.resolution_compression.lmp" "$case_dir/"
rm -rf "$case_dir/post"
mkdir -p "$case_dir/post"

(
  cd "$case_dir"
  "$lmp" -in in.resolution_compression.lmp \
    -var nspheres 500 \
    -var nsteps "$nsteps" \
    -var top_vz "$top_vz" \
    -var create_dist 2.0e-4 \
    -var create_dist_weak 9.0e-5 \
    -screen "screen_${case_id}.log" \
    -log log.liggghts
)

python3 "$root_dir/scripts/extract_liggghts_thermo.py" \
  "$case_dir/log.liggghts" \
  --output "$root_dir/data/processed/${case_id}_thermo.csv"
python3 "$root_dir/scripts/analyze_sp002_curve.py" \
  "$root_dir/data/processed/${case_id}_thermo.csv" \
  --summary "$root_dir/data/processed/${case_id}_summary.csv" \
  --plot "$root_dir/figures/sp002/${case_id}_curve.svg"
python3 "$root_dir/scripts/analyze_bond_fragments.py" \
  "$case_dir/post"/bonds_*.local \
  --atoms 500 \
  --output "$root_dir/data/processed/${case_id}_fragments.csv"
python3 "$root_dir/scripts/draft_single_particle_failure_metrics.py" \
  "$case_dir/post" \
  --output "$root_dir/data/processed/${case_id}_failure_metrics.csv"

echo "$root_dir/data/processed/${case_id}_summary.csv"
