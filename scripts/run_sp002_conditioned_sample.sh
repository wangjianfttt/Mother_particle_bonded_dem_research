#!/usr/bin/env bash
set -euo pipefail

sample_id="${1:?sample_id required}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plan="$root_dir/tables/orientation_conditioned_strength_sampling_plan.csv"

read -r orientation bulk weak < <(
  python3 - "$plan" "$sample_id" <<'PY'
import csv
import sys
from pathlib import Path

plan = Path(sys.argv[1])
sample_id = sys.argv[2]
with plan.open(newline="") as f:
    for row in csv.DictReader(f):
        if row["sample_id"] == sample_id:
            print(
                row["orientation_label"],
                float(row["bulk_strength_MPa_if_CAL1_bulk90"]),
                float(row["weakplane_strength_MPa_if_CAL1_weak22p5"]),
            )
            break
    else:
        raise SystemExit(f"sample_id {sample_id} not found in {plan}")
PY
)

case "$orientation" in
  x)
    normal_x=1
    normal_y=0
    normal_z=0
    ;;
  xy30)
    normal_x=0.8660254
    normal_y=0.5
    normal_z=0
    ;;
  y)
    normal_x=0
    normal_y=1
    normal_z=0
    ;;
  xy45)
    normal_x=1
    normal_y=1
    normal_z=0
    ;;
  tilt_xz)
    normal_x=1
    normal_y=0
    normal_z=0.5
    ;;
  *)
    echo "Unknown orientation_label: $orientation" >&2
    exit 2
    ;;
esac

case_id="$(printf 'SP-002-CWB-%02d-%s-bulk%s-weak%s' \
  "$sample_id" "$orientation" \
  "$(python3 - "$bulk" <<'PY'
import sys
print(str(round(float(sys.argv[1]), 3)).replace(".", "p"))
PY
)" \
  "$(python3 - "$weak" <<'PY'
import sys
print(str(round(float(sys.argv[1]), 3)).replace(".", "p"))
PY
)")"

"$root_dir/scripts/run_sp002_weakplane_orientation_case.sh" \
  "$case_id" "$normal_x" "$normal_y" "$normal_z" \
  600000 -0.1 \
  "$(python3 - "$bulk" <<'PY'
import sys
print(float(sys.argv[1]) * 1e6)
PY
)" \
  "$(python3 - "$bulk" <<'PY'
import sys
print(float(sys.argv[1]) * 1e6)
PY
)" \
  "$(python3 - "$weak" <<'PY'
import sys
print(float(sys.argv[1]) * 1e6)
PY
)" \
  "$(python3 - "$weak" <<'PY'
import sys
print(float(sys.argv[1]) * 1e6)
PY
)" \
  9.0e-5

echo "$case_id"
