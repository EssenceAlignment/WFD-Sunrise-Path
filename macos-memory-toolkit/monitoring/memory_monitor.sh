#!/bin/bash

# Memory Monitor Script
# Real-time memory monitoring with automatic cleanup triggers

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# Monitoring variables
MONITOR_PID_FILE="/tmp/memory_monitor.pid"
MONITOR_RUNNING=true

# Signal handlers
cleanup_monitor() {
    MONITOR_RUNNING=false
    rm -f "$MONITOR_PID_FILE"
    log INFO "Memory monitor stopped"
    exit 0
}

trap cleanup_monitor SIGINT SIGTERM

# Check if already running
check_existing_monitor() {
    if [[ -f "$MONITOR_PID_FILE" ]]; then
        local existing_pid=$(cat "$MONITOR_PID_FILE")
        if ps -p "$existing_pid" > /dev/null 2>&1; then
            log ERROR "Memory monitor is already running (PID: $existing_pid)"
            log INFO "Stop it with: kill $existing_pid"
            exit 1
        else
            rm -f "$MONITOR_PID_FILE"
        fi
    fi
}

# Save PID
save_pid() {
    echo $$ > "$MONITOR_PID_FILE"
    log INFO "Memory monitor started (PID: $$)"
}

# Monitor memory and trigger cleanup if needed
monitor_memory() {
    local free_mem=$(get_free_memory_mb)
    local memory_pressure=$(get_memory_pressure)
    local swap_usage=$(get_swap_usage_mb)
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Clear screen for clean display
    clear

    # Display header
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║               macOS Memory Monitor - Real-time View              ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo

    # Display current stats
    echo -e "${CYAN}Timestamp:${NC} $timestamp"
    echo -e "${CYAN}Update Interval:${NC} ${MONITOR_INTERVAL}s"
    echo

    # Memory status with color coding
    if (( free_mem < CRITICAL_MEMORY_THRESHOLD )); then
        echo -e "${RED}● Free Memory: ${free_mem}MB (CRITICAL)${NC}"
    elif (( free_mem < LOW_MEMORY_THRESHOLD )); then
        echo -e "${YELLOW}● Free Memory: ${free_mem}MB (LOW)${NC}"
    else
        echo -e "${GREEN}● Free Memory: ${free_mem}MB (GOOD)${NC}"
    fi

    echo -e "● Memory Pressure: ${memory_pressure}%"
    echo -e "● Swap Usage: ${swap_usage}MB"
    echo

    # Top memory consumers
    echo -e "${BLUE}Top 5 Memory Consumers:${NC}"
    ps aux | head -1
    ps aux | sort -nrk 4 | head -5
    echo

    # Auto-cleanup check
    if [[ "$AUTO_CLEANUP_ENABLED" == "true" ]] && (( free_mem < AUTO_CLEANUP_THRESHOLD )); then
        echo -e "${YELLOW}${WARNING_SIGN} Auto-cleanup triggered (free memory < ${AUTO_CLEANUP_THRESHOLD}MB)${NC}"
        log WARN "Auto-cleanup triggered - free memory: ${free_mem}MB"

        # Run safe cleanup without confirmation
        "$SCRIPT_DIR/../core/memory_clean.sh" --no-confirm

        # Send notification
        notify "Auto Memory Cleanup" "Free memory was ${free_mem}MB. Running cleanup..."
    fi

    # Status line
    echo -e "${CYAN}Press Ctrl+C to stop monitoring${NC}"

    # Log to file if debug mode
    if [[ "$LOG_LEVEL" == "debug" ]]; then
        log DEBUG "Memory stats - Free: ${free_mem}MB, Pressure: ${memory_pressure}%, Swap: ${swap_usage}MB"
    fi
}

# Monitor with specified interval
continuous_monitor() {
    while [[ "$MONITOR_RUNNING" == "true" ]]; do
        monitor_memory
        sleep "$MONITOR_INTERVAL"
    done
}

# Main function
main() {
    # Check if already running
    check_existing_monitor

    # Save PID
    save_pid

    # Print initial message
    log INFO "Starting memory monitor (interval: ${MONITOR_INTERVAL}s)"
    log INFO "Auto-cleanup: $AUTO_CLEANUP_ENABLED (threshold: ${AUTO_CLEANUP_THRESHOLD}MB)"

    # Start monitoring
    continuous_monitor
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --interval)
            MONITOR_INTERVAL="$2"
            shift 2
            ;;
        --auto-cleanup)
            AUTO_CLEANUP_ENABLED=true
            shift
            ;;
        --threshold)
            AUTO_CLEANUP_THRESHOLD="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --interval <seconds>    Set monitoring interval (default: 60)"
            echo "  --auto-cleanup         Enable automatic cleanup"
            echo "  --threshold <MB>       Set auto-cleanup threshold (default: 300)"
            echo "  --help                 Show this help message"
            exit 0
            ;;
        *)
            log ERROR "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run main function
main
