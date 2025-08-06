#!/bin/bash

# Memory Health Report Script
# Comprehensive system memory health report

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Load configuration
load_config

# Check macOS
check_macos

# Report file
REPORT_DIR="$HOME/Library/Logs/memory-toolkit/reports"
REPORT_FILE="$REPORT_DIR/health_report_$(date +%Y%m%d_%H%M%S)"

# Create report directory
mkdir -p "$REPORT_DIR"

# Generate HTML report
generate_html_report() {
    local html_file="${REPORT_FILE}.html"

    cat > "$html_file" << 'HTML_START'
<!DOCTYPE html>
<html>
<head>
    <title>macOS Memory Health Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .header {
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        .metric-box {
            display: inline-block;
            padding: 20px;
            margin: 10px;
            border-radius: 5px;
            text-align: center;
            min-width: 150px;
        }
        .good { background-color: #27ae60; color: white; }
        .warning { background-color: #f39c12; color: white; }
        .critical { background-color: #e74c3c; color: white; }
        .info { background-color: #3498db; color: white; }
        pre {
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .section {
            margin: 30px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        .recommendation {
            background-color: #fffbdd;
            border-left: 4px solid #f39c12;
            padding: 15px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
<div class="container">
HTML_START

    # Add report content
    echo "<div class='header'>" >> "$html_file"
    echo "<h1>macOS Memory Health Report</h1>" >> "$html_file"
    echo "<p>Generated on $(date '+%Y-%m-%d %H:%M:%S')</p>" >> "$html_file"
    echo "<p>System: $(sw_vers -productName) $(sw_vers -productVersion)</p>" >> "$html_file"
    echo "</div>" >> "$html_file"

    # Memory overview
    local free_mem=$(get_free_memory_mb)
    local memory_pressure=$(get_memory_pressure)
    local swap_usage=$(get_swap_usage_mb)

    echo "<h2>Memory Overview</h2>" >> "$html_file"
    echo "<div class='section'>" >> "$html_file"

    # Status boxes
    if (( free_mem < CRITICAL_MEMORY_THRESHOLD )); then
        echo "<div class='metric-box critical'>" >> "$html_file"
    elif (( free_mem < LOW_MEMORY_THRESHOLD )); then
        echo "<div class='metric-box warning'>" >> "$html_file"
    else
        echo "<div class='metric-box good'>" >> "$html_file"
    fi
    echo "<h3>Free Memory</h3><p>${free_mem} MB</p></div>" >> "$html_file"

    echo "<div class='metric-box info'>" >> "$html_file"
    echo "<h3>Memory Pressure</h3><p>${memory_pressure}%</p></div>" >> "$html_file"

    echo "<div class='metric-box info'>" >> "$html_file"
    echo "<h3>Swap Usage</h3><p>${swap_usage} MB</p></div>" >> "$html_file"

    echo "</div>" >> "$html_file"

    # Detailed VM stats
    echo "<h2>Virtual Memory Statistics</h2>" >> "$html_file"
    echo "<div class='section'><pre>" >> "$html_file"
    vm_stat >> "$html_file"
    echo "</pre></div>" >> "$html_file"

    # Top memory consumers
    echo "<h2>Top Memory Consumers</h2>" >> "$html_file"
    echo "<div class='section'><table>" >> "$html_file"
    ps aux | head -1 | awk '{print "<tr><th>" $1 "</th><th>" $2 "</th><th>" $3 "</th><th>" $4 "</th><th>" $11 "</th></tr>"}' >> "$html_file"
    ps aux | sort -nrk 4 | head -10 | awk '{print "<tr><td>" $1 "</td><td>" $2 "</td><td>" $3 "</td><td>" $4 "</td><td>" $11 "</td></tr>"}' >> "$html_file"
    echo "</table></div>" >> "$html_file"

    # Recommendations
    echo "<h2>Recommendations</h2>" >> "$html_file"
    echo "<div class='section'>" >> "$html_file"

    if (( free_mem < CRITICAL_MEMORY_THRESHOLD )); then
        echo "<div class='recommendation'>" >> "$html_file"
        echo "<strong>CRITICAL:</strong> Your system is critically low on memory. Consider:" >> "$html_file"
        echo "<ul>" >> "$html_file"
        echo "<li>Running emergency memory recovery</li>" >> "$html_file"
        echo "<li>Closing unnecessary applications</li>" >> "$html_file"
        echo "<li>Restarting your Mac</li>" >> "$html_file"
        echo "</ul>" >> "$html_file"
        echo "</div>" >> "$html_file"
    elif (( free_mem < LOW_MEMORY_THRESHOLD )); then
        echo "<div class='recommendation'>" >> "$html_file"
        echo "<strong>Warning:</strong> Memory is running low. Consider:" >> "$html_file"
        echo "<ul>" >> "$html_file"
        echo "<li>Running memory cleanup</li>" >> "$html_file"
        echo "<li>Closing some applications</li>" >> "$html_file"
        echo "<li>Checking for memory leaks</li>" >> "$html_file"
        echo "</ul>" >> "$html_file"
        echo "</div>" >> "$html_file"
    else
        echo "<p>✅ Your memory status is healthy.</p>" >> "$html_file"
    fi

    echo "</div>" >> "$html_file"

    # Close HTML
    echo "</div></body></html>" >> "$html_file"

    echo "$html_file"
}

# Generate text report
generate_text_report() {
    local text_file="${REPORT_FILE}.txt"

    {
        print_header "macOS Memory Health Report"

        echo "Generated: $(date)"
        echo "System: $(sw_vers -productName) $(sw_vers -productVersion)"
        echo "Hardware: $(sysctl -n hw.model)"
        echo "Total Memory: $(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')"
        echo

        # Memory summary
        print_memory_stats

        # Detailed VM statistics
        echo
        echo "=== Virtual Memory Statistics ==="
        vm_stat
        echo

        # Swap information
        echo "=== Swap Information ==="
        sysctl vm.swapusage
        ls -lah /var/vm/ 2>/dev/null | grep -E "swap|sleepimage"
        echo

        # Memory pressure details
        echo "=== Memory Pressure Details ==="
        memory_pressure
        echo

        # Top memory consumers
        echo "=== Top 20 Memory Consumers ==="
        ps aux | head -1
        ps aux | sort -nrk 4 | head -20
        echo

        # System caches
        echo "=== Cache Sizes ==="
        echo "User caches: $(du -sh ~/Library/Caches 2>/dev/null | awk '{print $1}')"
        echo "System caches: $(sudo du -sh /Library/Caches 2>/dev/null | awk '{print $1}')"
        echo "Browser caches:"
        du -sh ~/Library/Caches/com.apple.Safari 2>/dev/null | awk '{print "  Safari: " $1}'
        du -sh ~/Library/Caches/Google/Chrome 2>/dev/null | awk '{print "  Chrome: " $1}'
        du -sh ~/Library/Caches/Firefox 2>/dev/null | awk '{print "  Firefox: " $1}'
        echo

        # Disk space (affects virtual memory)
        echo "=== Disk Space ==="
        df -h /
        echo

        # Recent memory events
        echo "=== Recent Memory Events ==="
        log show --style syslog --predicate 'process == "kernel" AND (eventMessage CONTAINS "low memory" OR eventMessage CONTAINS "pressure")' --last 1h 2>/dev/null | tail -20
        echo

        # Recommendations
        echo "=== Recommendations ==="
        local free_mem=$(get_free_memory_mb)

        if (( free_mem < CRITICAL_MEMORY_THRESHOLD )); then
            echo "⚠️  CRITICAL: Your system is critically low on memory!"
            echo "   1. Run emergency memory recovery immediately"
            echo "   2. Close all unnecessary applications"
            echo "   3. Consider restarting your Mac"
            echo "   4. Check for memory leaks in running applications"
        elif (( free_mem < LOW_MEMORY_THRESHOLD )); then
            echo "⚠️  WARNING: Memory is running low"
            echo "   1. Run memory cleanup scripts"
            echo "   2. Close some applications"
            echo "   3. Clear browser tabs and caches"
            echo "   4. Monitor for memory-intensive processes"
        else
            echo "✅ Memory status is healthy"
            echo "   - Continue monitoring periodically"
            echo "   - Run cleanup scripts weekly for maintenance"
            echo "   - Keep 20% of disk space free for optimal performance"
        fi

        echo
        echo "=== Historical Memory Usage ==="
        if [[ -d "$HOME/Library/Logs/memory-toolkit" ]]; then
            echo "Recent memory checks:"
            grep "Free Memory" "$HOME/Library/Logs/memory-toolkit/memory-toolkit.log" 2>/dev/null | tail -10
        fi

    } > "$text_file"

    echo "$text_file"
}

# Generate JSON report
generate_json_report() {
    local json_file="${REPORT_FILE}.json"

    local free_mem=$(get_free_memory_mb)
    local memory_pressure=$(get_memory_pressure)
    local swap_usage=$(get_swap_usage_mb)
    local total_mem=$(sysctl -n hw.memsize | awk '{print $1/1024/1024}')

    cat > "$json_file" << JSON_END
{
    "report": {
        "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "system": {
            "os": "$(sw_vers -productName) $(sw_vers -productVersion)",
            "hardware": "$(sysctl -n hw.model)",
            "total_memory_mb": $total_mem
        },
        "memory_status": {
            "free_memory_mb": $free_mem,
            "memory_pressure_percent": $memory_pressure,
            "swap_usage_mb": $swap_usage,
            "health_status": "$(if (( free_mem < CRITICAL_MEMORY_THRESHOLD )); then echo "critical"; elif (( free_mem < LOW_MEMORY_THRESHOLD )); then echo "warning"; else echo "good"; fi)"
        },
        "thresholds": {
            "critical_mb": $CRITICAL_MEMORY_THRESHOLD,
            "low_mb": $LOW_MEMORY_THRESHOLD
        }
    }
}
JSON_END

    echo "$json_file"
}

# Main function
main() {
    print_header "Memory Health Report Generator"

    echo -e "${BLUE}Generating comprehensive memory health report...${NC}"
    echo

    # Generate reports based on format setting
    case "$REPORT_FORMAT" in
        html)
            local report=$(generate_html_report)
            echo -e "${GREEN}HTML report generated: $report${NC}"

            # Try to open in browser
            if command -v open &> /dev/null; then
                open "$report"
            fi
            ;;

        json)
            local report=$(generate_json_report)
            echo -e "${GREEN}JSON report generated: $report${NC}"
            ;;

        text|*)
            local report=$(generate_text_report)
            echo -e "${GREEN}Text report generated: $report${NC}"

            # Also display summary
            echo
            print_memory_stats
            ;;
    esac

    # Email report if configured
    if [[ "$ENABLE_EMAIL_REPORTS" == "true" ]] && [[ -n "$EMAIL_RECIPIENT" ]]; then
        log INFO "Emailing report to $EMAIL_RECIPIENT"
        # Note: Actual email sending would require mail server configuration
        # This is a placeholder for the functionality
    fi

    log SUCCESS "Memory health report completed"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --format)
            REPORT_FORMAT="$2"
            shift 2
            ;;
        --output)
            REPORT_FILE="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --format <text|html|json>  Output format (default: text)"
            echo "  --output <path>            Custom output path"
            echo "  --help                     Show this help message"
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
