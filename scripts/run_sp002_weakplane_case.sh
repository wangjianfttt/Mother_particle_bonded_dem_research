#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-SP-002-weakplane}"
nsteps="${2:-20000}"
top_vz="${3:--0.1}"
sigma_max="${4:-1.2e8}"
tau_max="${5:-1.2e8}"
sigma_weak="${6:-6.0e7}"
tau_weak="${7:-6.0e7}"
bottom_gap_m="${8:-1.0e-6}"
top_gap_m="${9:-1.0e-4}"
z_shift_m="${10:-7.9460215e-6}"
kn_bond="${11:-1.0e14}"
kt_bond="${12:-5.0e13}"
create_dist_weak="${13:-1.10e-4}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/single_pebble/SP-002"
lmp="$root_dir/external/LIGGGHTS-INL/src/lmp_mpi_no_vtk"
template="$case_dir/data/li4sio4_sp_500_weakplane.multisphere"
out_csv="$root_dir/data/processed/${case_id}_thermo.csv"

read -r zmin zmax < <(
  python3 - "$template" "$bottom_gap_m" "$top_gap_m" "$z_shift_m" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
bottom_gap = float(sys.argv[2])
top_gap = float(sys.argv[3])
z_shift = float(sys.argv[4])
zmin = 1e30
zmax = -1e30
for line in p.read_text().splitlines():
    parts = line.split()
    if len(parts) < 4:
        continue
    try:
        x, y, z, r = map(float, parts[:4])
    except ValueError:
        continue
    zmin = min(zmin, z - r)
    zmax = max(zmax, z + r)
print(f"{zmin + z_shift - bottom_gap:.12e} {zmax + z_shift + top_gap:.12e}")
PY
)

python3 "$root_dir/scripts/create_plate_stl.py" \
  --z="$zmin" --normal-z 1.0 --divisions 12 \
  --output "$case_dir/meshes/bottom_plate.stl"
python3 "$root_dir/scripts/create_plate_stl.py" \
  --z="$zmax" --normal-z=-1.0 --divisions 12 \
  --output "$case_dir/meshes/top_plate.stl"

cd "$case_dir"
rm -rf post log.liggghts warnings.liggghts "screen_${case_id}.log"
mkdir -p post
"$lmp" -in in.plate_compression_weakplane.lmp \
  -var nsteps "$nsteps" \
  -var top_vz "$top_vz" \
  -var sigma_max "$sigma_max" \
  -var tau_max "$tau_max" \
  -var sigma_weak "$sigma_weak" \
  -var tau_weak "$tau_weak" \
  -var kn_bond "$kn_bond" \
  -var kt_bond "$kt_bond" \
  -var create_dist_weak "$create_dist_weak" \
  -screen "screen_${case_id}.log" \
  -log log.liggghts

python3 "$root_dir/scripts/extract_liggghts_thermo.py" log.liggghts --output "$out_csv"
echo "$out_csv"
