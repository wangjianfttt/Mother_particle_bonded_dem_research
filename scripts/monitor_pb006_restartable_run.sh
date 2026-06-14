#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-PB-006-bonded-randompack-1000-seed01-prod-0p15mm-targeted-window-restartable}"
screen_hint="${2:-}"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case_dir="$root_dir/simulations/pebble_bed/PB-006"

cd "$case_dir"

echo "== screen sessions =="
screen -ls || true

echo
echo "== processes =="
ps -axo pid,ppid,etime,pcpu,pmem,rss,command | \
  rg "${case_id}|${screen_hint}|pb006_1000_0p15_restart|pb006_1000_seed02_0p15|lmp_mpi_no_vtk" || true

echo
echo "== key files =="
ls -lh \
  log.liggghts \
  "screen_${case_id}.log" \
  "screen_driver_${case_id}.out" 2>/dev/null || true

echo
echo "== latest thermo lines =="
tail -n 80 log.liggghts 2>/dev/null | \
  rg '^[[:space:]]*[0-9]+[[:space:]]+500000|Loop time|Setting up run|WARNING|ERROR' || true

echo
echo "== post files =="
find post -maxdepth 1 -type f -print | sort | xargs -r ls -lh
