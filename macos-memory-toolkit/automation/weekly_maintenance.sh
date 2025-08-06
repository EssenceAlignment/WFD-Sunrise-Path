#!/bin/bash

# Weekly Memory Maintenance Script
# Performs deep cleaning and maintenance tasks

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# Log file for weekly maintenance
WEEKLY_LOG="$HOME/Library/Logs/memory-toolkit/weekly_maintenance.log"

# Start weekly maintenance
main() {
    local start_time=$(get_timestamp)
    local date_string=$(date '+%Y-%m-%d %H:%M:%S')

    {
        echo "======================================"
        echo "Weekly Memory Maintenance - $date_string"
        echo "======================================"
        echo

        # System information
        echo "System Information:"
        echo "macOS Version: $(sw_vers -productVersion)"
        echo "Uptime: $(uptime)"
        echo "Total Memory: $(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')"
        echo

        # Initial memory status
        echo "Initial Memory Status:"
        local initial_free=$(get_free_memory_mb)
        echo "Free Memory: ${initial_free}MB"
        echo "Memory Pressure: $(get_memory_pressure)%"
        echo "Swap Usage: $(get_swap_usage_mb)MB"
        echo

        # Run deep cleanup
        echo "Running deep memory cleanup..."
        REQUIRE_CONFIRMATION=false

        # Check if we have enough disk space
        if check_disk_space $MIN_DISK_SPACE_GB; then
            # Run deep clean if we have sudo access
            if sudo -n true 2>/dev/null; then
                echo "Running with sudo access..."
                source "$SCRIPT_DIR/../core/memory_deep_clean.sh"
            else
                echo "No sudo access, running safe cleanup only..."
                source "$SCRIPT_DIR/../core/memory_clean.sh"
            fi
        else
            echo "Insufficient disk space. Running minimal cleanup..."
            source "$SCRIPT_DIR/../core/memory_clean.sh"
        fi

        # Generate health report
        echo
        echo "Generating memory health report..."
        "$SCRIPT_DIR/../monitoring/memory_health_report.sh" --format text

        # Benchmark performance
        echo
        echo "Running memory benchmark..."
        "$SCRIPT_DIR/../monitoring/memory_benchmark.sh" full

        # Clean old benchmarks and reports
        echo
        echo "Cleaning old files..."
        find "$HOME/Library/Logs/memory-toolkit/benchmarks" -name "*.log" -mtime +30 -delete 2>/dev/null
        find "$HOME/Library/Logs/memory-toolkit/reports" -name "*.txt" -mtime +30 -delete 2>/dev/null
        find "$HOME/Library/Logs/memory-toolkit/reports" -name "*.html" -mtime +30 -delete 2>/dev/null

        # Final memory status
        echo
        echo "Final Memory Status:"
        local final_free=$(get_free_memory_mb)
        echo "Free Memory: ${final_free}MB"
        echo "Memory Pressure: $(get_memory_pressure)%"
        echo "Swap Usage: $(get_swap_usage_mb)MB"

        # Calculate improvement
        local memory_freed=$((final_free - initial_free))
        echo
        echo "Memory freed: ${memory_freed}MB"

        local end_time=$(get_timestamp)
        local duration=$(calc_time_diff $start_time $end_time)

        echo
        echo "Weekly maintenance completed in $duration"
        echo

        # Recommendations
        echo "Recommendations:"
        if (( final_free < LOW_MEMORY_THRESHOLD )); then
            echo "- Consider closing unused applications"
            echo "- Check for memory leaks in running processes"
            echo "- Consider upgrading system RAM"
        else
            echo "- Memory status is healthy"
            echo "- Continue regular maintenance schedule"
        fi
        echo

    } | tee -a "$WEEKLY_LOG"

    # Send notification if enabled
    if [[ "$ENABLE_NOTIFICATIONS" == "true" ]]; then
        notify "Weekly Memory Maintenance" "Completed. Freed ${memory_freed}MB"
    fi
}

# Check if running from cron/launchd (no terminal)
if [[ ! -t 0 ]]; then
    # Running in background, suppress color codes
    unset RED GREEN YELLOW BLUE PURPLE CYAN WHITE NC
fi

# Run main function
main
