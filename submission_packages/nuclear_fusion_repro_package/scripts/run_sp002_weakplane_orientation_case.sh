#!/usr/bin/env bash
set -euo pipefail

case_id="${1:?case_id required}"
normal_x="${2:?normal_x required}"
normal_y="${3:?normal_y required}"
normal_z="${4:?normal_z required}"
nsteps="${5:-600000}"
top_vz="${6:--0.1}"
sigma_max="${7:-9.0e7}"
tau_max="${8:-9.0e7}"
sigma_weak="${9:-2.25e7}"
tau_weak="${10:-2.25e7}"
create_dist_weak="${11:-9.0e-5}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$root_dir/scripts/generate_weak_plane_template.py" \
  --input "$root_dir/simulations/single_pebble/SP-002/data/li4sio4_sp_500_nooverlap.multisphere" \
  --output "$root_dir/simulations/single_pebble/SP-002/data/li4sio4_sp_500_weakplane.multisphere" \
  --normal "$normal_x" "$normal_y" "$normal_z" \
  --offset 0.0

"$root_dir/scripts/run_sp002_weakplane_case.sh" \
  "$case_id" "$nsteps" "$top_vz" \
  "$sigma_max" "$tau_max" "$sigma_weak" "$tau_weak" \
  1e-6 1e-4 7.9460215e-6 1e14 5e13 "$create_dist_weak"

python3 "$root_dir/scripts/analyze_sp002_curve.py" \
  "$root_dir/data/processed/${case_id}_thermo.csv" \
  --summary "$root_dir/data/processed/${case_id}_summary.csv" \
  --plot "$root_dir/figures/sp002/${case_id}_curve.svg"

python3 "$root_dir/scripts/estimate_initial_stiffness.py" \
  "$root_dir/data/processed/${case_id}_thermo.csv" \
  --output "$root_dir/data/processed/${case_id}_initial_stiffness.csv"

python3 "$root_dir/scripts/analyze_bond_fragments.py" \
  "$root_dir/simulations/single_pebble/SP-002/post"/bonds_*.local \
  --atoms 500 \
  --output "$root_dir/data/processed/${case_id}_fragments.csv"

python3 "$root_dir/scripts/draft_single_particle_failure_metrics.py" \
  "$root_dir/simulations/single_pebble/SP-002/post" \
  --output "$root_dir/data/processed/${case_id}_failure_metrics.csv"

printf '%s\n' "$root_dir/data/processed/${case_id}_summary.csv"
