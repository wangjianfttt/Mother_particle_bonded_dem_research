#!/usr/bin/env bash
set -euo pipefail

case_id="${1:?Usage: $0 CASE_ID [baseline_step]}"
baseline_step="${2:-10001}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-007/cases/$case_id"
thermo_csv="$root_dir/data/processed/${case_id}_thermo.csv"
native_summary="$root_dir/tables/pb007_${case_id}_native_summary.csv"
native_edges="$root_dir/tables/pb007_${case_id}_native_edges.csv"
native_series="$root_dir/data/processed/${case_id}_native_force_network_series.csv"
acceptance_summary="$root_dir/tables/pb007_${case_id}_acceptance_summary.csv"
validation_csv="$root_dir/data/processed/${case_id}_validation_curve.csv"
validation_fig="$root_dir/figures/pb007/${case_id}_validation.png"
bond_series="$root_dir/data/processed/${case_id}_bond_series.csv"
bond_events="$root_dir/data/processed/${case_id}_breakage_events.csv"

if [[ ! -d "$case_dir" ]]; then
  echo "Missing case directory: $case_dir" >&2
  exit 1
fi

python3 "$root_dir/scripts/extract_liggghts_thermo.py" \
  "$case_dir/log.liggghts" \
  --output "$thermo_csv"

if [[ ! -s "$case_dir/post/pairs_final.local" || ! -s "$case_dir/post/walls_final.local" ]]; then
  echo "Final native contact dumps are not available yet." >&2
  exit 2
fi

python3 "$root_dir/scripts/analyze_pb007_native_force_network.py" \
  --pairs "$case_dir/post/pairs_final.local" \
  --walls "$case_dir/post/walls_final.local" \
  --summary "$native_summary" \
  --edges "$native_edges"

if compgen -G "$case_dir/post/pairs_event_*.local" > /dev/null && compgen -G "$case_dir/post/walls_event_*.local" > /dev/null; then
  python3 "$root_dir/scripts/analyze_pb007_native_force_network_series.py" \
    --case-dir "$case_dir" \
    --output "$native_series"
fi

python3 "$root_dir/scripts/summarize_pb007_loadpath_validation.py" \
  --thermo "$thermo_csv" \
  --native-summary "$native_summary" \
  --output "$acceptance_summary" \
  --baseline-step "$baseline_step"

python3 "$root_dir/scripts/build_pb007_step_relaxed_validation.py" \
  --thermo "$thermo_csv" \
  --output "$validation_fig" \
  --csv "$validation_csv" \
  --baseline-step "$baseline_step"

shopt -s nullglob
bond_dumps=("$case_dir"/post/bonds_event_*.local)
if [[ -s "$case_dir/post/bonds_final.local" ]]; then
  bond_dumps+=("$case_dir/post/bonds_final.local")
fi
shopt -u nullglob

if (( ${#bond_dumps[@]} == 0 )); then
  echo "No PB-007 bond local dumps are available yet." >&2
  exit 3
fi

python3 "$root_dir/scripts/analyze_pb007_bond_event_sequence.py" \
  "${bond_dumps[@]}" \
  --npebbles 100 \
  --nspheres 500 \
  --thermo "$thermo_csv" \
  --metadata "$case_dir/data/bonded_template_metadata.csv" \
  --series-output "$bond_series" \
  --events-output "$bond_events"

echo "$thermo_csv"
echo "$native_summary"
if [[ -s "$native_series" ]]; then
  echo "$native_series"
fi
echo "$acceptance_summary"
echo "$validation_fig"
echo "$bond_series"
echo "$bond_events"
