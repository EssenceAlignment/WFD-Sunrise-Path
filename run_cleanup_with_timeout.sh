#!/bin/bash
# Wrapper script with hard timeout for Cline polling (180 s)

echo "Running cleanup script with 180s timeout..."
timeout 180s ./execute_systematic_cleanup.sh || {
  exit_code=$?
  if [ $exit_code -eq 124 ]; then
    echo "Script exceeded 180 s — aborting run."
  else
    echo "Script exited with code: $exit_code"
  fi
  exit $exit_code
}
