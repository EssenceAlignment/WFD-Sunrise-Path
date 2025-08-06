#!/bin/bash

# Emergency Memory Recovery Script
# Nuclear option for severe memory issues - closes apps and frees memory aggressively

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# This script requires sudo
check_sudo

# Track recovery metrics
RECOVERY_START_TIME=$(get_timestamp)
INITIAL_FREE_MEM=$(get_free_memory_mb)

# Kill memory-heavy processes
kill_memory_hogs() {
    log INFO "Identifying and terminating memory-heavy processes..."

    # Get list of processes using more than 100MB
    local heavy_processes=$(ps aux | awk '$6 > 100000 {print $2, $11, $6}' | sort -k3 -nr)

    echo -e "${YELLOW}Top memory-consuming processes:${NC}"
    ps aux | head -1
    ps aux | sort -nrk 6 | head -10
    echo

    # Kill non-essential processes
    local killed_count=0
    while IFS= read -r line; do
        local pid=$(echo "$line" | awk '{print $1}')
        local process=$(echo "$line" | awk '{print $2}')
        local memory=$(echo "$line" | awk '{print $3}')

        # Skip excluded apps and system processes
        local skip=false
        for excluded in "${EXCLUDED_APPS[@]}"; do
            if [[ "$process" == *"$excluded"* ]]; then
                skip=true
                break
            fi
        done

        if [[ "$skip" == "false" ]] && [[ "$pid" != "$$" ]]; then
            log WARN "Killing $process (PID: $pid, Memory: $((memory/1024))MB)"
            sudo kill -9 "$pid" 2>/dev/null && ((killed_count++))
        fi
    done <<< "$heavy_processes"

    log SUCCESS "Terminated $killed_count memory-heavy processes"
}

# Kill specific applications known to use lots of memory
kill_known_memory_hogs() {
    log INFO "Terminating known memory-intensive applications..."

    local apps_to_kill=(
        "Google Chrome"
        "Safari"
        "Firefox"
        "Microsoft Edge"
        "Slack"
        "Microsoft Teams"
        "Zoom"
        "Discord"
        "Spotify"
        "Mail"
        "Photos"
        "Music"
        "TV"
        "iMovie"
        "Final Cut Pro"
        "Logic Pro"
        "Xcode"
        "Android Studio"
        "IntelliJ IDEA"
        "Visual Studio Code"
        "Docker Desktop"
        "Parallels Desktop"
        "VMware Fusion"
    )

    for app in "${apps_to_kill[@]}"; do
        if pgrep -f "$app" > /dev/null; then
            log WARN "Terminating $app..."
            pkill -f "$app" 2>/dev/null
        fi
    done

    log SUCCESS "Known memory-intensive applications terminated"
}

# Emergency system cleanup
emergency_system_cleanup() {
    log INFO "Performing emergency system cleanup..."

    # Kill all user processes except current shell
    local current_user=$(whoami)
    local current_pid=$$

    # Get all user processes
    local user_processes=$(ps -u "$current_user" -o pid= | grep -v "$current_pid")

    echo -e "${RED}Terminating all user processes...${NC}"
    for pid in $user_processes; do
        sudo kill -9 "$pid" 2>/dev/null
    done

    # Force quit all apps
    osascript -e 'tell application "System Events" to set appList to name of every process whose background only is false' | tr ',' '\n' | while read app; do
        local is_excluded=false
        for excluded in "${EXCLUDED_APPS[@]}"; do
            if [[ "$app" == "$excluded" ]]; then
                is_excluded=true
                break
            fi
        done
        if [[ "$is_excluded" == "false" ]]; then
            osascript -e "tell application \"$app\" to quit" 2>/dev/null
        fi
    done

    log SUCCESS "Emergency system cleanup completed"
}

# Extreme memory recovery
extreme_memory_recovery() {
    log INFO "Performing extreme memory recovery..."

    # Stop all launch agents
    launchctl list | grep -v com.apple | awk '{print $3}' | while read agent; do
        launchctl unload "$agent" 2>/dev/null
    done

    # Clear all possible caches
    sudo rm -rf /System/Library/Caches/* 2>/dev/null
    sudo rm -rf /Library/Caches/* 2>/dev/null
    sudo rm -rf ~/Library/Caches/* 2>/dev/null
    sudo rm -rf /tmp/* 2>/dev/null
    sudo rm -rf /var/tmp/* 2>/dev/null
    sudo rm -rf /var/folders/* 2>/dev/null

    # Remove all swap files
    sudo rm -rf /var/vm/* 2>/dev/null

    # Disable and re-enable swap
    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.dynamic_pager.plist 2>/dev/null
    sleep 2
    sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.dynamic_pager.plist 2>/dev/null

    # Multiple aggressive purges
    for i in {1..5}; do
        sudo purge
        sleep 1
    done

    log SUCCESS "Extreme memory recovery completed"
}

# Main emergency recovery function
main() {
    print_header "EMERGENCY MEMORY RECOVERY"

    echo -e "${RED}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                          ⚠️  CRITICAL WARNING ⚠️                    ║${NC}"
    echo -e "${RED}║                                                                  ║${NC}"
    echo -e "${RED}║  This will FORCEFULLY CLOSE ALL APPLICATIONS and perform        ║${NC}"
    echo -e "${RED}║  AGGRESSIVE system cleanup. You WILL LOSE any unsaved work!     ║${NC}"
    echo -e "${RED}║                                                                  ║${NC}"
    echo -e "${RED}║  Only use this as a LAST RESORT when your system is unusable!   ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo

    # Show current critical status
    local free_mem=$(get_free_memory_mb)
    local swap_usage=$(get_swap_usage_mb)

    echo -e "${RED}CRITICAL MEMORY STATUS:${NC}"
    echo -e "Free Memory: ${RED}${free_mem}MB${NC}"
    echo -e "Swap Usage: ${RED}${swap_usage}MB${NC}"
    echo

    # Multiple confirmation required
    if ! confirm "${RED}⚠️  Do you want to proceed with EMERGENCY RECOVERY?${NC}" "n"; then
        log INFO "Emergency recovery cancelled"
        exit 0
    fi

    echo
    if ! confirm "${RED}⚠️  Are you ABSOLUTELY SURE? This will close EVERYTHING!${NC}" "n"; then
        log INFO "Emergency recovery cancelled"
        exit 0
    fi

    echo
    echo -e "${RED}${ROCKET} INITIATING EMERGENCY RECOVERY IN 5 SECONDS...${NC}"
    echo -e "${RED}Press Ctrl+C NOW to cancel!${NC}"

    # Countdown
    for i in {5..1}; do
        echo -e "${RED}$i...${NC}"
        sleep 1
    done

    echo
    echo -e "${RED}EMERGENCY RECOVERY STARTED!${NC}"
    echo

    # Send notification before starting
    notify "EMERGENCY RECOVERY STARTED" "All applications will be closed!" "Sosumi"

    # Execute emergency recovery steps
    log WARN "Starting emergency memory recovery sequence"

    # Step 1: Kill known memory hogs
    kill_known_memory_hogs
    sleep 2

    # Step 2: Kill remaining heavy processes
    kill_memory_hogs
    sleep 2

    # Step 3: Emergency system cleanup
    emergency_system_cleanup
    sleep 2

    # Step 4: Deep clean (reuse from deep clean script)
    source "$SCRIPT_DIR/memory_deep_clean.sh" --no-main
    cleanup_application_caches
    cleanup_system_caches
    cleanup_dns_cache
    cleanup_swap_files

    # Step 5: Extreme recovery measures
    extreme_memory_recovery

    # Reset critical system components
    sudo killall -HUP WindowServer 2>/dev/null
    killall Dock 2>/dev/null
    killall Finder 2>/dev/null
    killall SystemUIServer 2>/dev/null

    # Calculate results
    RECOVERY_END_TIME=$(get_timestamp)
    FINAL_FREE_MEM=$(get_free_memory_mb)
    MEMORY_RECOVERED=$((FINAL_FREE_MEM - INITIAL_FREE_MEM))
    RECOVERY_DURATION=$(calc_time_diff $RECOVERY_START_TIME $RECOVERY_END_TIME)

    echo
    print_header "EMERGENCY RECOVERY COMPLETE"

    echo -e "${GREEN}Memory recovered:${NC} ${MEMORY_RECOVERED} MB"
    echo -e "${GREEN}Duration:${NC} ${RECOVERY_DURATION}"
    echo -e "${GREEN}Free memory now:${NC} ${FINAL_FREE_MEM} MB"
    echo

    echo -e "${YELLOW}${WARNING_SIGN} IMPORTANT:${NC}"
    echo "  • All applications have been closed"
    echo "  • You may need to restart some system services"
    echo "  • Consider restarting your Mac for best results"
    echo "  • Check Activity Monitor for any remaining issues"
    echo

    # Send completion notification
    notify "EMERGENCY RECOVERY COMPLETE" "Recovered ${MEMORY_RECOVERED}MB. Restart recommended." "Glass"

    log SUCCESS "Emergency recovery completed. Recovered ${MEMORY_RECOVERED}MB"

    # Suggest next steps
    echo -e "${BLUE}Recommended next steps:${NC}"
    echo "1. Save any important work and restart your Mac"
    echo "2. After restart, run: ${GREEN}memory_check.sh${NC}"
    echo "3. Consider upgrading RAM if this happens frequently"
}

# Run main function
main "$@"
