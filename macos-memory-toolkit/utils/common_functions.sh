#!/bin/bash

# Common functions for macOS Memory Management Toolkit
# Source this file in other scripts: source "$(dirname "$0")/../utils/common_functions.sh"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Icons
CHECK_MARK="✅"
CROSS_MARK="❌"
WARNING_SIGN="⚠️"
INFO_SIGN="ℹ️"
ROCKET="🚀"
BROOM="🧹"
CHART="📊"
GEAR="⚙️"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLKIT_DIR="$(dirname "$SCRIPT_DIR")"

# Load configuration
load_config() {
    local config_file="$TOOLKIT_DIR/config/settings.conf"
    if [[ -f "$config_file" ]]; then
        source "$config_file"
    else
        # Default values if config doesn't exist
        LOW_MEMORY_THRESHOLD=500
        CRITICAL_MEMORY_THRESHOLD=200
        CLEANUP_AGGRESSIVENESS="moderate"
        ENABLE_NOTIFICATIONS=true
        LOG_LEVEL="info"
    fi
}

# Logging functions
log() {
    local level=$1
    shift
    local message="$@"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local log_file="$HOME/Library/Logs/memory-toolkit/memory-toolkit.log"

    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "$log_file")"

    echo "[$timestamp] [$level] $message" >> "$log_file"

    # Also print to console based on log level
    case $level in
        ERROR)
            echo -e "${RED}${CROSS_MARK} $message${NC}" >&2
            ;;
        WARN)
            echo -e "${YELLOW}${WARNING_SIGN} $message${NC}"
            ;;
        INFO)
            echo -e "${BLUE}${INFO_SIGN} $message${NC}"
            ;;
        SUCCESS)
            echo -e "${GREEN}${CHECK_MARK} $message${NC}"
            ;;
        DEBUG)
            if [[ "$LOG_LEVEL" == "debug" ]]; then
                echo -e "${PURPLE}[DEBUG] $message${NC}"
            fi
            ;;
    esac
}

# Check if running on macOS
check_macos() {
    if [[ "$(uname)" != "Darwin" ]]; then
        log ERROR "This script is designed for macOS only"
        exit 1
    fi
}

# Check if running with sudo when required
check_sudo() {
    if [[ $EUID -ne 0 ]]; then
        log ERROR "This operation requires sudo privileges"
        log INFO "Please run with: sudo $0"
        exit 1
    fi
}

# Get free memory in MB
get_free_memory_mb() {
    local pages_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
    local pages_inactive=$(vm_stat | grep "Pages inactive" | awk '{print $3}' | sed 's/\.//')
    local page_size=$(vm_stat | head -1 | grep -o '[0-9]*')

    # Calculate free memory (free + inactive pages)
    local total_pages=$((pages_free + pages_inactive))
    local free_mb=$((total_pages * page_size / 1048576))

    echo $free_mb
}

# Get memory pressure
get_memory_pressure() {
    memory_pressure | grep "System-wide memory free percentage" | awk '{print $5}' | sed 's/%//'
}

# Get swap usage in MB
get_swap_usage_mb() {
    sysctl vm.swapusage | grep -o "used = [0-9.]*M" | awk '{print $3}' | sed 's/M//'
}

# Format bytes to human readable
format_bytes() {
    local bytes=$1
    local units=("B" "KB" "MB" "GB" "TB")
    local unit=0

    while (( $(echo "$bytes > 1024" | bc -l) )) && (( unit < ${#units[@]} - 1 )); do
        bytes=$(echo "scale=2; $bytes / 1024" | bc)
        ((unit++))
    done

    printf "%.2f %s" "$bytes" "${units[$unit]}"
}

# Progress bar
show_progress() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((width * current / total))

    printf "\r["
    printf "%${completed}s" | tr ' ' '='
    printf "%$((width - completed))s" | tr ' ' '-'
    printf "] %3d%%" "$percentage"

    if [[ $current -eq $total ]]; then
        echo
    fi
}

# Spinner animation
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'

    while ps -p $pid > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# Confirmation prompt
confirm() {
    local message="${1:-Are you sure you want to continue?}"
    local default="${2:-n}"

    if [[ $default == "y" ]]; then
        local prompt="$message [Y/n]: "
        local default_return=0
    else
        local prompt="$message [y/N]: "
        local default_return=1
    fi

    read -p "$prompt" response
    response=${response:-$default}

    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        [nN][oO]|[nN])
            return 1
            ;;
        *)
            return $default_return
            ;;
    esac
}

# Check disk space
check_disk_space() {
    local required_gb=${1:-5}  # Default 5GB required
    local available_gb=$(df -g / | awk 'NR==2 {print $4}')

    if (( available_gb < required_gb )); then
        log WARN "Low disk space: ${available_gb}GB available, ${required_gb}GB recommended"
        return 1
    fi
    return 0
}

# Send notification (if enabled)
notify() {
    local title="$1"
    local message="$2"
    local sound="${3:-default}"

    if [[ "$ENABLE_NOTIFICATIONS" == "true" ]] && command -v osascript &> /dev/null; then
        osascript -e "display notification \"$message\" with title \"$title\" sound name \"$sound\""
    fi
}

# Get current timestamp for benchmarking
get_timestamp() {
    echo $(date +%s)
}

# Calculate time difference
calc_time_diff() {
    local start=$1
    local end=$2
    local diff=$((end - start))

    if (( diff < 60 )); then
        echo "${diff} seconds"
    elif (( diff < 3600 )); then
        echo "$((diff / 60)) minutes $((diff % 60)) seconds"
    else
        echo "$((diff / 3600)) hours $((diff % 3600 / 60)) minutes"
    fi
}

# Backup important files before cleanup
backup_before_cleanup() {
    local backup_dir="$HOME/Library/MemoryToolkitBackups/$(date +%Y%m%d_%H%M%S)"

    log INFO "Creating backup directory: $backup_dir"
    mkdir -p "$backup_dir"

    # Add any important files to backup here
    # Example: cp -r "$HOME/Library/Preferences" "$backup_dir/" 2>/dev/null

    echo "$backup_dir"
}

# Print section header
print_header() {
    local title="$1"
    local width=60
    local padding=$(( (width - ${#title} - 2) / 2 ))

    echo
    echo -e "${BLUE}$(printf '=%.0s' {1..60})${NC}"
    printf "${BLUE}=%*s%s%*s=${NC}\n" $padding "" "$title" $padding ""
    echo -e "${BLUE}$(printf '=%.0s' {1..60})${NC}"
    echo
}

# Print memory stats table
print_memory_stats() {
    local free_mem=$(get_free_memory_mb)
    local memory_pressure=$(get_memory_pressure)
    local swap_usage=$(get_swap_usage_mb)

    print_header "Memory Status"

    printf "%-20s: %s MB\n" "Free Memory" "$free_mem"
    printf "%-20s: %s%%\n" "Memory Pressure" "$memory_pressure"
    printf "%-20s: %s MB\n" "Swap Usage" "$swap_usage"

    # Color code based on status
    if (( free_mem < CRITICAL_MEMORY_THRESHOLD )); then
        echo -e "\n${RED}⚠️  CRITICAL: Very low memory!${NC}"
    elif (( free_mem < LOW_MEMORY_THRESHOLD )); then
        echo -e "\n${YELLOW}⚠️  WARNING: Low memory${NC}"
    else
        echo -e "\n${GREEN}✅ Memory status: Good${NC}"
    fi
}

# Export all functions
export -f log check_macos check_sudo get_free_memory_mb get_memory_pressure
export -f get_swap_usage_mb format_bytes show_progress spinner confirm
export -f check_disk_space notify get_timestamp calc_time_diff
export -f backup_before_cleanup print_header print_memory_stats load_config
