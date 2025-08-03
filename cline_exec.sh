#!/usr/bin/env bash
# Universal wrapper for Cline‑initiated tasks.
set -euo pipefail
LOG_DIR=".cline_logs"; mkdir -p "$LOG_DIR"
TS="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/task-${TS}.log"

trim_history () {
  # keep last 2 MiB of aggregated logs to avoid 200 k‑token overflow
  MAX_BYTES=$((2*1024*1024))
  for f in $LOG_DIR/*.log; do
    [ -f "$f" ] || continue
    sz=$(wc -c <"$f")
    if (( sz > MAX_BYTES )); then
      tail -c "$MAX_BYTES" "$f" >"$f.tmp" && mv "$f.tmp" "$f"
    fi
  done
}

trim_history

echo "▶ $(date) – running task $*" | tee -a "$LOG_FILE"
"$@" 2>&1 | tee -a "$LOG_FILE"
echo "✔ $(date) – task finished"   | tee -a "$LOG_FILE"
