#!/bin/bash

# Memory Check Script
# Quick memory status check for macOS

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# Main function
main() {
    print_header "macOS Memory Check"

    # Get detailed memory statistics
    echo -e "${CYAN}${CHART} Gathering memory statistics...${NC}\n"

    # VM Statistics
    echo -e "${BLUE}Virtual Memory Statistics:${NC}"
    vm_stat | head -20
    echo

    # Memory Pressure
    echo -e "${BLUE}Memory Pressure:${NC}"
    memory_pressure | head -10
    echo

    # Swap Usage
    echo -e "${BLUE}Swap Usage:${NC}"
    sysctl vm.swapusage
    echo

    # Top Memory Consumers
    echo -e "${BLUE}Top 10 Memory Consumers:${NC}"
    ps aux | head -1
    ps aux | sort -nrk 4 | head -10
    echo

    # Disk Space (affects virtual memory)
    echo -e "${BLUE}Disk Space:${NC}"
    df -h /
    echo

    # Print formatted summary
    print_memory_stats

    # Log the check
    log INFO "Memory check completed"

    # Check if cleanup is recommended
    local free_mem=$(get_free_memory_mb)
    if (( free_mem < LOW_MEMORY_THRESHOLD )); then
        echo
        echo -e "${YELLOW}${WARNING_SIGN} Recommendation:${NC}"
        echo "  Consider running memory cleanup:"
        echo "  ${GREEN}./memory_clean.sh${NC} for safe cleanup"
        echo "  ${YELLOW}sudo ./memory_deep_clean.sh${NC} for aggressive cleanup"
    fi
}

# Run main function
main "$@"
