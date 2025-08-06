#!/bin/bash

# Memory Benchmark Script
# Performance testing before and after optimization

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# Benchmark results storage
BENCHMARK_DIR="$HOME/Library/Logs/memory-toolkit/benchmarks"
BENCHMARK_FILE="$BENCHMARK_DIR/benchmark_$(date +%Y%m%d_%H%M%S).log"

# Create benchmark directory
mkdir -p "$BENCHMARK_DIR"

# Benchmark functions
run_memory_test() {
    local test_name="$1"
    local test_command="$2"
    local start_time=$(get_timestamp)

    echo -e "${BLUE}Running test: $test_name${NC}"
    eval "$test_command" > /dev/null 2>&1

    local end_time=$(get_timestamp)
    local duration=$((end_time - start_time))

    echo "Test: $test_name - Duration: ${duration}s" >> "$BENCHMARK_FILE"
    echo -e "${GREEN}✓ Completed in ${duration}s${NC}"
}

# Memory allocation test
memory_allocation_test() {
    log INFO "Running memory allocation test..."

    # Create a temporary file for memory test
    local temp_file="/tmp/memory_benchmark_$$"

    # Allocate 100MB
    dd if=/dev/zero of="$temp_file" bs=1m count=100 2>/dev/null

    # Clean up
    rm -f "$temp_file"
}

# Cache performance test
cache_performance_test() {
    log INFO "Running cache performance test..."

    # Read a large file multiple times
    local test_file="/usr/share/dict/words"
    if [[ -f "$test_file" ]]; then
        for i in {1..10}; do
            cat "$test_file" > /dev/null
        done
    fi
}

# Application launch test
app_launch_test() {
    log INFO "Running application launch test..."

    # Test launching and quitting Calculator app
    osascript -e 'tell application "Calculator" to launch' 2>/dev/null
    sleep 2
    osascript -e 'tell application "Calculator" to quit' 2>/dev/null
}

# Collect system metrics
collect_metrics() {
    local phase="$1"

    echo -e "\n=== $phase Metrics ===" >> "$BENCHMARK_FILE"

    # Memory stats
    echo "Free Memory: $(get_free_memory_mb)MB" >> "$BENCHMARK_FILE"
    echo "Memory Pressure: $(get_memory_pressure)%" >> "$BENCHMARK_FILE"
    echo "Swap Usage: $(get_swap_usage_mb)MB" >> "$BENCHMARK_FILE"

    # VM stats
    echo -e "\nVM Statistics:" >> "$BENCHMARK_FILE"
    vm_stat | head -10 >> "$BENCHMARK_FILE"

    # Top processes
    echo -e "\nTop Memory Consumers:" >> "$BENCHMARK_FILE"
    ps aux | sort -nrk 4 | head -5 >> "$BENCHMARK_FILE"
}

# Run performance benchmark
run_performance_benchmark() {
    print_header "Performance Benchmark"

    echo "Benchmark started at: $(date)" >> "$BENCHMARK_FILE"
    echo "System: $(sw_vers -productName) $(sw_vers -productVersion)" >> "$BENCHMARK_FILE"
    echo "Hardware: $(sysctl -n hw.model)" >> "$BENCHMARK_FILE"
    echo "Total Memory: $(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')" >> "$BENCHMARK_FILE"
    echo "" >> "$BENCHMARK_FILE"

    # Run tests
    run_memory_test "Memory Allocation" memory_allocation_test
    run_memory_test "Cache Performance" cache_performance_test
    run_memory_test "App Launch" app_launch_test

    echo
}

# Compare before/after optimization
compare_optimization() {
    local before_file="$1"
    local after_file="$2"

    if [[ ! -f "$before_file" ]] || [[ ! -f "$after_file" ]]; then
        log ERROR "Comparison files not found"
        return 1
    fi

    print_header "Optimization Comparison"

    # Extract and compare key metrics
    local before_free=$(grep "Free Memory:" "$before_file" | head -1 | awk '{print $3}' | sed 's/MB//')
    local after_free=$(grep "Free Memory:" "$after_file" | tail -1 | awk '{print $3}' | sed 's/MB//')
    local memory_gain=$((after_free - before_free))

    local before_swap=$(grep "Swap Usage:" "$before_file" | head -1 | awk '{print $3}' | sed 's/MB//')
    local after_swap=$(grep "Swap Usage:" "$after_file" | tail -1 | awk '{print $3}' | sed 's/MB//')
    local swap_reduction=$((before_swap - after_swap))

    echo -e "${BLUE}Memory Improvement:${NC}"
    echo "  Before: ${before_free}MB free"
    echo "  After:  ${after_free}MB free"
    echo -e "  ${GREEN}Gain:   +${memory_gain}MB${NC}"
    echo

    echo -e "${BLUE}Swap Reduction:${NC}"
    echo "  Before: ${before_swap}MB used"
    echo "  After:  ${after_swap}MB used"
    echo -e "  ${GREEN}Reduced: -${swap_reduction}MB${NC}"
    echo

    # Calculate improvement percentage
    if [[ $before_free -gt 0 ]]; then
        local improvement=$(echo "scale=2; ($memory_gain / $before_free) * 100" | bc)
        echo -e "${GREEN}Overall Memory Improvement: ${improvement}%${NC}"
    fi
}

# Main function
main() {
    local mode="${1:-full}"

    case "$mode" in
        before)
            print_header "Pre-Optimization Benchmark"
            collect_metrics "BEFORE"
            run_performance_benchmark
            echo -e "\n${GREEN}Benchmark saved to: $BENCHMARK_FILE${NC}"
            echo -e "${YELLOW}Run cleanup, then use 'after' mode to compare${NC}"
            ;;

        after)
            print_header "Post-Optimization Benchmark"
            collect_metrics "AFTER"
            run_performance_benchmark
            echo -e "\n${GREEN}Benchmark saved to: $BENCHMARK_FILE${NC}"

            # Find the most recent 'before' benchmark
            local before_file=$(ls -t "$BENCHMARK_DIR"/benchmark_*.log 2>/dev/null | grep -v "$BENCHMARK_FILE" | head -1)
            if [[ -n "$before_file" ]]; then
                compare_optimization "$before_file" "$BENCHMARK_FILE"
            fi
            ;;

        compare)
            if [[ $# -lt 3 ]]; then
                echo "Usage: $0 compare <before_file> <after_file>"
                exit 1
            fi
            compare_optimization "$2" "$3"
            ;;

        full|*)
            print_header "Full Memory Benchmark"

            # Before optimization
            echo -e "${BLUE}Phase 1: Pre-optimization metrics${NC}"
            collect_metrics "BEFORE OPTIMIZATION"
            run_performance_benchmark

            # Get user confirmation
            echo
            if confirm "${YELLOW}Run memory cleanup before post-optimization test?${NC}" "y"; then
                echo -e "\n${GREEN}Running safe memory cleanup...${NC}"
                "$SCRIPT_DIR/../core/memory_clean.sh"
                sleep 5
            fi

            # After optimization
            echo -e "\n${BLUE}Phase 2: Post-optimization metrics${NC}"
            collect_metrics "AFTER OPTIMIZATION"
            run_performance_benchmark

            # Show comparison
            compare_optimization "$BENCHMARK_FILE" "$BENCHMARK_FILE"

            echo -e "\n${GREEN}Full benchmark saved to: $BENCHMARK_FILE${NC}"
            ;;
    esac

    # Log completion
    log SUCCESS "Memory benchmark completed"
}

# Show help
show_help() {
    echo "Usage: $0 [mode]"
    echo
    echo "Modes:"
    echo "  before    Run pre-optimization benchmark"
    echo "  after     Run post-optimization benchmark and compare"
    echo "  full      Run complete before/after benchmark (default)"
    echo "  compare   Compare two benchmark files"
    echo
    echo "Examples:"
    echo "  $0 before"
    echo "  $0 after"
    echo "  $0 compare file1.log file2.log"
}

# Parse arguments
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Run main function
main "$@"
