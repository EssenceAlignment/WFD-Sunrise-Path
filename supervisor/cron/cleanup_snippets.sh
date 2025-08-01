#!/bin/bash
# Cleanup old provenance snippets
# Add to crontab: 0 2 * * * /path/to/cleanup_snippets.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

# Change to project directory
cd "$PROJECT_ROOT"

# Run Python cleanup script
/usr/bin/python3 -c "
import sys
sys.path.append('.')
from supervisor.provenance.tracker import ProvenanceTracker

tracker = ProvenanceTracker()
removed = tracker.cleanup_old_snippets()
print(f'Cleanup complete. Removed {removed} old snippets.')
"

# Log the cleanup
echo "[$(date)] Provenance cleanup completed" >> "$PROJECT_ROOT/supervisor/logs/cleanup.log"
