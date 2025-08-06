#!/bin/bash

# Memory Deep Clean Script
# Aggressive memory cleanup including system caches and more

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

# Track cleanup metrics
CLEANUP_START_TIME=$(get_timestamp)
INITIAL_FREE_MEM=$(get_free_memory_mb)

# Deep cleanup functions
cleanup_system_caches() {
    log INFO "Cleaning system caches..."

    # System cache directories
    sudo rm -rf /System/Library/Caches/* 2>/dev/null
    sudo rm -rf /Library/Caches/* 2>/dev/null

    log SUCCESS "System caches cleaned"
}

cleanup_dns_cache() {
    log INFO "Flushing DNS cache..."

    # Flush DNS cache (command varies by macOS version)
    sudo dscacheutil -flushcache 2>/dev/null
    sudo killall -HUP mDNSResponder 2>/dev/null

    log SUCCESS "DNS cache flushed"
}

cleanup_spotlight_index() {
    log INFO "Rebuilding Spotlight index..."

    # Disable and re-enable Spotlight
    sudo mdutil -a -i off
    sleep 2
    sudo mdutil -a -i on

    log SUCCESS "Spotlight index rebuild initiated"
}

cleanup_kernel_caches() {
    log INFO "Cleaning kernel caches..."

    # Remove kernel extension caches
    sudo rm -rf /System/Library/Caches/com.apple.kext.caches/* 2>/dev/null

    # Touch the Extensions folder to rebuild cache on next boot
    sudo touch /System/Library/Extensions

    log SUCCESS "Kernel caches cleaned"
}

cleanup_font_caches() {
    log INFO "Cleaning font caches..."

    # Remove font caches
    sudo atsutil databases -remove 2>/dev/null

    # Remove user font caches
    rm -rf ~/Library/Caches/com.apple.ATS 2>/dev/null
    rm -rf ~/Library/Caches/com.apple.fontd 2>/dev/null

    log SUCCESS "Font caches cleaned"
}

cleanup_quicklook_caches() {
    log INFO "Cleaning Quick Look caches..."

    # Reset Quick Look
    qlmanage -r cache 2>/dev/null
    rm -rf ~/Library/Caches/com.apple.QuickLookDaemon* 2>/dev/null

    log SUCCESS "Quick Look caches cleaned"
}

cleanup_swap_files() {
    log INFO "Cleaning swap files..."

    # Get current swap usage
    local swap_before=$(get_swap_usage_mb)

    # Remove swap files (they'll be recreated as needed)
    sudo rm -rf /var/vm/swapfile* 2>/dev/null

    log SUCCESS "Swap files cleaned (was using ${swap_before}MB)"
}

reset_dock_and_finder() {
    log INFO "Resetting Dock and Finder..."

    # Kill Dock and Finder to free their memory
    killall Dock 2>/dev/null
    killall Finder 2>/dev/null

    log SUCCESS "Dock and Finder reset"
}

aggressive_memory_purge() {
    log INFO "Performing aggressive memory purge..."

    # Multiple purge cycles for maximum effect
    for i in {1..3}; do
        sudo purge
        sleep 1
    done

    log SUCCESS "Aggressive memory purge completed"
}

cleanup_application_caches() {
    log INFO "Cleaning application caches..."

    # Clean all application caches
    find ~/Library/Caches -type f -delete 2>/dev/null

    # Clean application saved states
    rm -rf ~/Library/Saved\ Application\ State/* 2>/dev/null

    # Clean application logs
    find ~/Library/Logs -type f -name "*.log" -delete 2>/dev/null

    log SUCCESS "Application caches cleaned"
}

# Main deep cleanup function
main() {
    print_header "Aggressive Memory Deep Clean"

    echo -e "${RED}${WARNING_SIGN} WARNING: This will perform aggressive system cleanup!${NC}"
    echo -e "${RED}Some applications may need to rebuild caches on next launch.${NC}\n"

    # Check disk space
    if ! check_disk_space $MIN_DISK_SPACE_GB; then
        log ERROR "Insufficient disk space for deep cleanup"
        exit 1
    fi

    # Show initial status
    echo -e "${BLUE}Initial Memory Status:${NC}"
    print_memory_stats

    # Require confirmation
    echo
    if ! confirm "${RED}This will aggressively clean system files. Are you SURE?${NC}" "n"; then
        log INFO "Deep cleanup cancelled by user"
        exit 0
    fi

    # Create backup if enabled
    if [[ "$BACKUP_BEFORE_CLEANUP" == "true" ]]; then
        log INFO "Creating backup before deep cleanup..."
        backup_before_cleanup
    fi

    echo
    echo -e "${YELLOW}${BROOM} Starting aggressive deep cleanup...${NC}\n"

    # Perform all cleanup operations
    cleanup_application_caches
    cleanup_system_caches
    cleanup_dns_cache
    cleanup_font_caches
    cleanup_quicklook_caches
    cleanup_kernel_caches
    cleanup_swap_files

    # Perform safe cleanups too
    source "$SCRIPT_DIR/memory_clean.sh" --no-main
    cleanup_user_caches
    cleanup_temp_files
    cleanup_logs
    cleanup_browser_caches

    # Reset system components
    reset_dock_and_finder
    cleanup_spotlight_index

    # Final aggressive purge
    aggressive_memory_purge

    # Calculate results
    CLEANUP_END_TIME=$(get_timestamp)
    FINAL_FREE_MEM=$(get_free_memory_mb)
    MEMORY_FREED=$((FINAL_FREE_MEM - INITIAL_FREE_MEM))
    CLEANUP_DURATION=$(calc_time_diff $CLEANUP_START_TIME $CLEANUP_END_TIME)

    echo
    print_header "Deep Cleanup Results"

    echo -e "${GREEN}Memory freed:${NC} ${MEMORY_FREED} MB"
    echo -e "${GREEN}Duration:${NC} ${CLEANUP_DURATION}"
    echo

    # Show final status
    print_memory_stats

    echo
    echo -e "${YELLOW}${INFO_SIGN} Note: Some caches will rebuild on next use.${NC}"
    echo -e "${YELLOW}A restart may provide additional memory recovery.${NC}"

    # Send notification
    notify "Deep Memory Cleanup Complete" "Freed ${MEMORY_FREED}MB. Restart recommended." "Glass"

    log SUCCESS "Deep cleanup completed. Freed ${MEMORY_FREED}MB"
}

# Only run main if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
