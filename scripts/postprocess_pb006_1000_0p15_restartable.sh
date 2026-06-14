#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-006"
bundled_python="/Users/wangjian-macbook13/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
if [[ -x "$bundled_python" ]]; then
  python_bin="$bundled_python"
else
  python_bin="${PYTHON:-python3}"
fi
thermo_csv="$root_dir/data/processed/${case_id}_thermo.csv"
events_csv="$root_dir/data/processed/${case_id}_breakage_events.csv"
late_events_csv="$root_dir/data/processed/${case_id}_late_window_breakage_events.csv"
series_csv="$root_dir/data/processed/${case_id}_per_pebble_series.csv"
pebble_csv="$root_dir/data/processed/${case_id}_pebble_summary.csv"
height_csv="$root_dir/data/processed/${case_id}_height_summary.csv"
summary_csv="$root_dir/tables/pb006_1000_0p15_restartable_summary.csv"
early_events_csv="$root_dir/data/processed/PB-006-bonded-randompack-1000-seed01-prod-0p10mm-targeted-window_breakage_events.csv"

cd "$case_dir"
if [[ "${ALLOW_INCOMPLETE:-0}" != "1" ]]; then
  if ps -axo command | grep -F "$case_id" | grep -F "lmp_mpi_no_vtk" >/dev/null; then
    echo "The restartable case is still running; wait for completion or set ALLOW_INCOMPLETE=1 for a diagnostic partial postprocess." >&2
    exit 1
  fi
  if ! compgen -G "post/bonds_final_*.local" >/dev/null; then
    echo "No final local bond dump found. Refusing final postprocess on an incomplete window." >&2
    exit 1
  fi
fi

shopt -s nullglob
bond_dumps=(post/bonds_window_*.local post/bonds_final_*.local)
if [[ "${#bond_dumps[@]}" -eq 0 ]]; then
  echo "No local bond dumps found in $case_dir/post" >&2
  exit 1
fi

"$python_bin" "$root_dir/scripts/extract_liggghts_thermo.py" log.liggghts --output "$thermo_csv"

"$python_bin" "$root_dir/scripts/analyze_bed_breakage_events.py" \
  "${bond_dumps[@]}" \
  --npebbles 1000 \
  --nspheres 500 \
  --thermo "$thermo_csv" \
  --series-output "$series_csv" \
  --events-output "$late_events_csv"

"$python_bin" "$root_dir/scripts/combine_pb006_restartable_events.py" \
  --early-events "$early_events_csv" \
  --late-events "$late_events_csv" \
  --output "$events_csv"

"$python_bin" "$root_dir/scripts/summarize_random_pack_breakage.py" \
  "$events_csv" \
  --metadata data/bonded_template_metadata_1000.csv \
  --pebble-output "$pebble_csv" \
  --height-output "$height_csv"

cd "$root_dir"

"$python_bin" scripts/summarize_pb006_1000_short.py \
  --thermo "$thermo_csv" \
  --events "$events_csv" \
  --height-summary "$height_csv" \
  --pebble-summary "$pebble_csv" \
  --packing-summary tables/pb006_1000_proxy_packing_summary.csv \
  --case "$case_id" \
  --npebbles 1000 \
  --output "$summary_csv"

"$python_bin" scripts/build_pb006_event_database.py
grep -F "seed01-1000-0p15-restartable" tables/pb006_breakage_event_database_summary.csv >/dev/null

"$python_bin" scripts/plot_pb006_event_database.py

echo "$thermo_csv"
echo "$events_csv"
echo "$summary_csv"
