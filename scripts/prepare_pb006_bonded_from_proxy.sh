#!/usr/bin/env bash
set -euo pipefail

npebbles="${1:-500}"
orientation_seed="${2:-20260524}"
centers_override="${3:-}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-006"
centers="${centers_override:-$case_dir/data/proxy_centers_${npebbles}.csv}"

if [[ ! -f "$centers" ]]; then
  echo "Missing proxy centre file: $centers" >&2
  exit 1
fi

mkdir -p "$case_dir/data" "$case_dir/meshes"

python3 "$root_dir/scripts/generate_weak_plane_template.py" \
  --input "$root_dir/simulations/single_pebble/SP-002/data/li4sio4_sp_500_nooverlap.multisphere" \
  --output "$case_dir/data/li4sio4_sp_500_cal1_x.multisphere" \
  --normal 1 0 0 \
  --offset 0.0

python3 "$root_dir/scripts/generate_bonded_bed_from_centers.py" \
  --centers "$centers" \
  --create-output "$case_dir/data/create_pebbles_far.inc" \
  --move-output "$case_dir/data/move_pebbles_to_pack.inc" \
  --metadata-output "$case_dir/data/bonded_template_metadata_${npebbles}.csv" \
  --bounds-output "$case_dir/data/pack_bounds_${npebbles}.csv" \
  --orientation-seed "$orientation_seed"

python3 - "$root_dir" "$case_dir" "$npebbles" <<'PY'
import csv
import subprocess
import sys

root_dir, case_dir, npebbles = sys.argv[1], sys.argv[2], sys.argv[3]
bounds_path = f"{case_dir}/data/pack_bounds_{npebbles}.csv"
with open(bounds_path, newline="") as f:
    bounds = next(csv.DictReader(f))
with open(f"{case_dir}/data/wall_bounds.inc", "w") as f:
    for key in ("xlo", "xhi", "ylo", "yhi", "zlo", "zhi"):
        f.write(f"variable wall_{key} index {bounds[key]}\n")
cmd = [
    "python3",
    f"{root_dir}/scripts/create_box_meshes.py",
    "--output-dir",
    f"{case_dir}/meshes",
    f"--xlo={bounds['xlo']}",
    f"--xhi={bounds['xhi']}",
    f"--ylo={bounds['ylo']}",
    f"--yhi={bounds['yhi']}",
    f"--zlo={bounds['zlo']}",
    f"--zhi={bounds['zhi']}",
    "--divisions",
    "24",
]
subprocess.run(cmd, check=True)
print(bounds_path)
PY
