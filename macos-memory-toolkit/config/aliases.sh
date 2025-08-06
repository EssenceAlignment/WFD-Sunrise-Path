#!/bin/bash

# macOS Memory Management Toolkit - Shell Aliases
# Add this to your ~/.zshrc or ~/.bashrc:
# source /path/to/macos-memory-toolkit/config/aliases.sh

# Get the toolkit directory - hardcoded for reliability
TOOLKIT_DIR="/Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path/macos-memory-toolkit"

# Quick memory check
alias memcheck="$TOOLKIT_DIR/core/memory_check.sh"

# Safe memory cleanup
alias memclean="$TOOLKIT_DIR/core/memory_clean.sh"

# Deep memory cleanup (requires sudo)
alias memdeep="sudo $TOOLKIT_DIR/core/memory_deep_clean.sh"

# Emergency recovery (requires sudo)
alias memrescue="sudo $TOOLKIT_DIR/core/emergency_recovery.sh"

# Memory monitoring
alias memmon="$TOOLKIT_DIR/monitoring/memory_monitor.sh"

# Memory benchmark
alias membench="$TOOLKIT_DIR/monitoring/memory_benchmark.sh"

# Memory health report
alias memreport="$TOOLKIT_DIR/monitoring/memory_health_report.sh"

# Quick actions
alias memstatus="$TOOLKIT_DIR/core/memory_check.sh | grep -E 'Free Memory|Memory Pressure|Swap Usage'"
alias memtop="ps aux | sort -nrk 4 | head -10"
alias memkill="$TOOLKIT_DIR/core/memory_clean.sh --no-confirm"

# Memory toolkit help
memhelp() {
    echo "macOS Memory Management Toolkit - Quick Reference"
    echo "================================================"
    echo
    echo "Basic Commands:"
    echo "  memcheck    - Check current memory status"
    echo "  memclean    - Safe memory cleanup"
    echo "  memdeep     - Aggressive cleanup (sudo)"
    echo "  memrescue   - Emergency recovery (sudo)"
    echo
    echo "Monitoring:"
    echo "  memmon      - Real-time memory monitor"
    echo "  membench    - Memory benchmark"
    echo "  memreport   - Generate health report"
    echo
    echo "Quick Actions:"
    echo "  memstatus   - Quick memory summary"
    echo "  memtop      - Top memory consumers"
    echo "  memkill     - Auto cleanup (no confirm)"
    echo
    echo "Options:"
    echo "  Most commands support --help for details"
    echo
    echo "Configuration:"
    echo "  Edit: $TOOLKIT_DIR/config/settings.conf"
}

# Advanced functions
meminfo() {
    echo "System Memory Information"
    echo "========================"
    echo "Total RAM: $(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')"
    echo "CPU Model: $(sysctl -n machdep.cpu.brand_string)"
    echo "Uptime: $(uptime)"
    echo
    $TOOLKIT_DIR/core/memory_check.sh | grep -E 'Free Memory|Memory Pressure|Swap Usage'
}

# Clean specific app caches
memclean-safari() {
    echo "Cleaning Safari caches..."
    rm -rf ~/Library/Caches/com.apple.Safari/Cache.db*
    rm -rf ~/Library/Caches/com.apple.Safari/Webpage\ Previews
    echo "Safari caches cleaned"
}

memclean-chrome() {
    echo "Cleaning Chrome caches..."
    rm -rf ~/Library/Caches/Google/Chrome/*/Cache
    rm -rf ~/Library/Caches/Google/Chrome/*/Code\ Cache
    echo "Chrome caches cleaned"
}

memclean-xcode() {
    echo "Cleaning Xcode caches..."
    rm -rf ~/Library/Developer/Xcode/DerivedData/*
    rm -rf ~/Library/Caches/com.apple.dt.Xcode
    echo "Xcode caches cleaned"
}

# Memory usage by app
memapp() {
    local app_name="$1"
    if [[ -z "$app_name" ]]; then
        echo "Usage: memapp <app_name>"
        echo "Example: memapp Chrome"
        return 1
    fi

    echo "Memory usage for $app_name:"
    ps aux | grep -i "$app_name" | grep -v grep | awk '{sum += $6} END {print "Total: " sum/1024 " MB"}'
    echo
    ps aux | head -1
    ps aux | grep -i "$app_name" | grep -v grep | sort -nrk 6
}

# Export toolkit directory for other scripts
export MEMORY_TOOLKIT_DIR="$TOOLKIT_DIR"

# Completion for zsh (if available)
if [[ -n "$ZSH_VERSION" ]]; then
    # Basic completion for memory toolkit commands
    _memory_toolkit_completion() {
        local -a commands
        commands=(
            'memcheck:Check memory status'
            'memclean:Safe memory cleanup'
            'memdeep:Deep memory cleanup'
            'memrescue:Emergency recovery'
            'memmon:Memory monitor'
            'membench:Memory benchmark'
            'memreport:Health report'
            'memhelp:Show help'
        )
        _describe 'memory toolkit' commands
    }

    compdef _memory_toolkit_completion memcheck memclean memdeep memrescue memmon membench memreport
fi

echo "Memory Toolkit aliases loaded. Type 'memhelp' for usage."
