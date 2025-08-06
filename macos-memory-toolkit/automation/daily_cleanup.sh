#!/bin/bash

# Daily Memory Cleanup Script
# Performs routine maintenance to keep memory optimized

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# Log file for daily cleanup
DAILY_LOG="$HOME/Library/Logs/memory-toolkit/daily_cleanup.log"

# Start daily cleanup
main() {
    local start_time=$(get_timestamp)
    local date_string=$(date '+%Y-%m-%d %H:%M:%S')

    {
        echo "======================================"
        echo "Daily Memory Cleanup - $date_string"
        echo "======================================"
        echo

        # Check current memory status
        echo "Initial Memory Status:"
        echo "Free Memory: $(get_free_memory_mb)MB"
        echo "Memory Pressure: $(get_memory_pressure)%"
        echo "Swap Usage: $(get_swap_usage_mb)MB"
        echo

        # Only run cleanup if memory is below threshold
        local free_mem=$(get_free_memory_mb)
        if (( free_mem < LOW_MEMORY_THRESHOLD )); then
            echo "Memory below threshold. Running cleanup..."

            # Run safe cleanup without confirmation
            REQUIRE_CONFIRMATION=false
            source "$SCRIPT_DIR/../core/memory_clean.sh"

            echo
            echo "Final Memory Status:"
            echo "Free Memory: $(get_free_memory_mb)MB"
            echo "Memory Pressure: $(get_memory_pressure)%"
            echo "Swap Usage: $(get_swap_usage_mb)MB"
        else
            echo "Memory status is healthy. Skipping cleanup."
        fi

        # Log retention cleanup
        echo
        echo "Cleaning old logs..."
        find "$HOME/Library/Logs/memory-toolkit" -name "*.log" -mtime +${LOG_RETENTION_DAYS} -delete 2>/dev/null

        local end_time=$(get_timestamp)
        local duration=$(calc_time_diff $start_time $end_time)

        echo
        echo "Daily cleanup completed in $duration"
        echo

    } | tee -a "$DAILY_LOG"

    # Send notification if enabled
    if [[ "$ENABLE_NOTIFICATIONS" == "true" ]]; then
        notify "Daily Memory Cleanup" "Completed successfully"
    fi
}

# Check if running from cron/launchd (no terminal)
if [[ ! -t 0 ]]; then
    # Running in background, suppress color codes
    unset RED GREEN YELLOW BLUE PURPLE CYAN WHITE NC
fi

# Run main function
main
