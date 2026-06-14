#!/usr/bin/env bash
set -euo pipefail

count="${1:?subparticle count required}"
case_id="${2:-SP-RES-${count}}"
top_vz="${3:--0.1}"
nsteps="${4:-600000}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base_dir="$root_dir/simulations/single_pebble/SP-RESOLUTION"
case_dir="$base_dir/cases/$case_id"
template_dir="$base_dir/templates/sp_${count}_d1mm_nooverlap"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"

mkdir -p "$template_dir" "$case_dir/data" "$case_dir/meshes" "$case_dir/post"

python3 "$root_dir/scripts/generate_bonded_sphere.py" \
  --count "$count" \
  --diameter-mm 1.0 \
  --seed 20260523 \
  --packing-fraction 0.30 \
  --bond-factor 2.35 \
  --min-distance-factor 2.05 \
  --out-dir "$template_dir"

python3 "$root_dir/scripts/export_liggghts_multiplespheres.py" \
  --particles "$template_dir/particles.csv" \
  --output "$case_dir/data/template_nooverlap.multisphere"

python3 "$root_dir/scripts/generate_weak_plane_template.py" \
  --input "$case_dir/data/template_nooverlap.multisphere" \
  --output "$case_dir/data/template.multisphere" \
  --normal 1.0 0.0 0.0 \
  --offset 0.0

read -r zmin zmax < <(
  python3 - "$case_dir/data/template.multisphere" <<'PY'
from pathlib import Path
import sys

zmin = float("inf")
zmax = float("-inf")
for line in Path(sys.argv[1]).read_text().splitlines():
    parts = line.split()
    if len(parts) < 4:
        continue
    _, _, z, r = map(float, parts[:4])
    zmin = min(zmin, z - r)
    zmax = max(zmax, z + r)
print(f"{zmin - 1.0e-6:.12e} {zmax + 1.0e-4:.12e}")
PY
)

read -r create_dist create_dist_weak < <(
  python3 - "$case_dir/data/template.multisphere" <<'PY'
from pathlib import Path
import sys

reference_radius = 4.2171633e-5
radius = float(Path(sys.argv[1]).read_text().splitlines()[0].split()[3])
scale = radius / reference_radius
print(f"{2.0e-4 * scale:.12e} {9.0e-5 * scale:.12e}")
PY
)

python3 "$root_dir/scripts/create_plate_stl.py" \
  --z="$zmin" --normal-z 1.0 --divisions 12 \
  --output "$case_dir/meshes/bottom_plate.stl"
python3 "$root_dir/scripts/create_plate_stl.py" \
  --z="$zmax" --normal-z=-1.0 --divisions 12 \
  --output "$case_dir/meshes/top_plate.stl"

cp "$base_dir/in.resolution_compression.lmp" "$case_dir/"
rm -rf "$case_dir/post"
mkdir -p "$case_dir/post"

(
  cd "$case_dir"
  "$lmp" -in in.resolution_compression.lmp \
    -var nspheres "$count" \
    -var nsteps "$nsteps" \
    -var top_vz "$top_vz" \
    -var create_dist "$create_dist" \
    -var create_dist_weak "$create_dist_weak" \
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
python3 "$root_dir/scripts/estimate_initial_stiffness.py" \
  "$root_dir/data/processed/${case_id}_thermo.csv" \
  --output "$root_dir/data/processed/${case_id}_initial_stiffness.csv"
python3 "$root_dir/scripts/analyze_bond_fragments.py" \
  "$case_dir/post"/bonds_*.local \
  --atoms "$count" \
  --output "$root_dir/data/processed/${case_id}_fragments.csv"
python3 "$root_dir/scripts/draft_single_particle_failure_metrics.py" \
  "$case_dir/post" \
  --output "$root_dir/data/processed/${case_id}_failure_metrics.csv"

printf '%s\n' "$root_dir/data/processed/${case_id}_summary.csv"
