#!/bin/bash

# Memory Clean Script
# Safe memory cleanup that won't affect system stability

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# Track cleanup metrics
CLEANUP_START_TIME=$(get_timestamp)
INITIAL_FREE_MEM=$(get_free_memory_mb)

# Cleanup functions
cleanup_user_caches() {
    log INFO "Cleaning user caches..."

    # Clean user cache directory
    if [[ -d "$HOME/Library/Caches" ]]; then
        local cache_size=$(du -sh "$HOME/Library/Caches" 2>/dev/null | awk '{print $1}')
        log INFO "Current user cache size: $cache_size"

        # Remove cache files older than 7 days
        find "$HOME/Library/Caches" -type f -mtime +7 -delete 2>/dev/null

        local new_size=$(du -sh "$HOME/Library/Caches" 2>/dev/null | awk '{print $1}')
        log SUCCESS "User cache cleaned. New size: $new_size"
    fi
}

cleanup_temp_files() {
    log INFO "Cleaning temporary files..."

    # Clean user temp directory
    if [[ -d "$TMPDIR" ]]; then
        local temp_count=$(find "$TMPDIR" -type f 2>/dev/null | wc -l | tr -d ' ')
        find "$TMPDIR" -type f -mtime +1 -delete 2>/dev/null
        local new_count=$(find "$TMPDIR" -type f 2>/dev/null | wc -l | tr -d ' ')
        local removed=$((temp_count - new_count))
        log SUCCESS "Removed $removed temporary files"
    fi
}

cleanup_downloads() {
    log INFO "Checking Downloads folder..."

    if [[ -d "$HOME/Downloads" ]]; then
        # Just report size, don't delete automatically
        local downloads_size=$(du -sh "$HOME/Downloads" 2>/dev/null | awk '{print $1}')
        log INFO "Downloads folder size: $downloads_size"
        echo -e "${YELLOW}Tip: Consider manually cleaning your Downloads folder${NC}"
    fi
}

cleanup_logs() {
    log INFO "Cleaning old log files..."

    # Clean user logs older than 30 days
    if [[ -d "$HOME/Library/Logs" ]]; then
        find "$HOME/Library/Logs" -type f -name "*.log" -mtime +30 -delete 2>/dev/null
        log SUCCESS "Cleaned old log files"
    fi
}

purge_memory() {
    log INFO "Purging inactive memory..."

    # Use macOS purge command if available
    if command -v purge &> /dev/null; then
        purge
        log SUCCESS "Memory purged successfully"
    else
        log WARN "purge command not available"
    fi
}

cleanup_browser_caches() {
    if [[ "$CLEAN_BROWSER_CACHES" != "true" ]]; then
        return
    fi

    log INFO "Cleaning browser caches..."

    # Safari
    if [[ -d "$HOME/Library/Caches/com.apple.Safari" ]]; then
        rm -rf "$HOME/Library/Caches/com.apple.Safari/Cache.db*" 2>/dev/null
        log SUCCESS "Safari cache cleaned"
    fi

    # Chrome
    if [[ -d "$HOME/Library/Caches/Google/Chrome" ]]; then
        rm -rf "$HOME/Library/Caches/Google/Chrome/*/Cache" 2>/dev/null
        log SUCCESS "Chrome cache cleaned"
    fi

    # Firefox
    if [[ -d "$HOME/Library/Caches/Firefox" ]]; then
        rm -rf "$HOME/Library/Caches/Firefox/Profiles/*/cache2" 2>/dev/null
        log SUCCESS "Firefox cache cleaned"
    fi
}

# Main cleanup function
main() {
    print_header "Safe Memory Cleanup"

    # Check disk space
    if ! check_disk_space $MIN_DISK_SPACE_GB; then
        if ! confirm "Low disk space detected. Continue anyway?"; then
            log WARN "Cleanup cancelled due to low disk space"
            exit 1
        fi
    fi

    # Show initial status
    echo -e "${BLUE}Initial Memory Status:${NC}"
    print_memory_stats

    # Ask for confirmation if required
    if [[ "$REQUIRE_CONFIRMATION" == "true" ]]; then
        echo
        if ! confirm "${YELLOW}This will clean caches and temporary files. Continue?${NC}"; then
            log INFO "Cleanup cancelled by user"
            exit 0
        fi
    fi

    echo
    echo -e "${GREEN}${BROOM} Starting safe cleanup...${NC}\n"

    # Perform cleanup operations
    cleanup_user_caches
    cleanup_temp_files
    cleanup_downloads
    cleanup_logs
    cleanup_browser_caches
    purge_memory

    # Clean custom paths if configured
    if [[ ${#CUSTOM_CACHE_PATHS[@]} -gt 0 ]]; then
        log INFO "Cleaning custom cache paths..."
        for path in "${CUSTOM_CACHE_PATHS[@]}"; do
            if [[ -d "$path" ]]; then
                rm -rf "$path"/* 2>/dev/null
                log SUCCESS "Cleaned: $path"
            fi
        done
    fi

    # Calculate results
    CLEANUP_END_TIME=$(get_timestamp)
    FINAL_FREE_MEM=$(get_free_memory_mb)
    MEMORY_FREED=$((FINAL_FREE_MEM - INITIAL_FREE_MEM))
    CLEANUP_DURATION=$(calc_time_diff $CLEANUP_START_TIME $CLEANUP_END_TIME)

    echo
    print_header "Cleanup Results"

    echo -e "${BLUE}Memory freed:${NC} ${MEMORY_FREED} MB"
    echo -e "${BLUE}Duration:${NC} ${CLEANUP_DURATION}"
    echo

    # Show final status
    print_memory_stats

    # Send notification
    notify "Memory Cleanup Complete" "Freed ${MEMORY_FREED}MB in ${CLEANUP_DURATION}"

    log SUCCESS "Safe cleanup completed. Freed ${MEMORY_FREED}MB"
}

# Run main function
main "$@"
