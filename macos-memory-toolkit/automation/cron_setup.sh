#!/bin/bash

# Cron Setup Script
# Helps configure automated memory cleanup schedules

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source common functions
source "$SCRIPT_DIR/../utils/common_functions.sh"

# Check macOS
check_macos

# Show current cron jobs
show_current_cron() {
    echo -e "${BLUE}Current cron jobs:${NC}"
    crontab -l 2>/dev/null || echo "No cron jobs configured"
    echo
}

# Add cron job
add_cron_job() {
    local schedule="$1"
    local script="$2"
    local description="$3"

    # Create a temporary file
    local temp_cron=$(mktemp)

    # Get existing crontab
    crontab -l 2>/dev/null > "$temp_cron" || true

    # Check if job already exists
    if grep -q "$script" "$temp_cron"; then
        echo -e "${YELLOW}Job already exists for $script${NC}"
        return 1
    fi

    # Add new job
    echo "# Memory Toolkit - $description" >> "$temp_cron"
    echo "$schedule $script >> /dev/null 2>&1" >> "$temp_cron"

    # Install new crontab
    crontab "$temp_cron"
    rm "$temp_cron"

    echo -e "${GREEN}✓ Added: $description${NC}"
    echo "  Schedule: $schedule"
    echo "  Script: $script"
}

# Remove memory toolkit cron jobs
remove_cron_jobs() {
    local temp_cron=$(mktemp)

    # Get existing crontab and remove memory toolkit jobs
    crontab -l 2>/dev/null | grep -v "Memory Toolkit" > "$temp_cron" || true

    # Install cleaned crontab
    if [[ -s "$temp_cron" ]]; then
        crontab "$temp_cron"
    else
        crontab -r 2>/dev/null || true
    fi

    rm "$temp_cron"
    echo -e "${GREEN}✓ Removed all Memory Toolkit cron jobs${NC}"
}

# Main menu
main() {
    print_header "Memory Toolkit - Cron Schedule Setup"

    echo "This tool helps you schedule automatic memory cleanup tasks."
    echo

    show_current_cron

    echo -e "${BLUE}Options:${NC}"
    echo "1) Add daily cleanup (runs at 3 AM)"
    echo "2) Add weekly maintenance (runs Sunday at 2 AM)"
    echo "3) Add custom schedule"
    echo "4) Remove all Memory Toolkit cron jobs"
    echo "5) Exit"
    echo

    read -p "Select option (1-5): " choice

    case $choice in
        1)
            # Daily cleanup at 3 AM
            if add_cron_job "0 3 * * *" "$SCRIPT_DIR/daily_cleanup.sh" "Daily Cleanup (3 AM)"; then
                echo -e "\n${GREEN}Daily cleanup scheduled successfully!${NC}"
            fi
            ;;

        2)
            # Weekly maintenance on Sunday at 2 AM
            if add_cron_job "0 2 * * 0" "$SCRIPT_DIR/weekly_maintenance.sh" "Weekly Maintenance (Sunday 2 AM)"; then
                echo -e "\n${GREEN}Weekly maintenance scheduled successfully!${NC}"
            fi
            ;;

        3)
            # Custom schedule
            echo
            echo -e "${BLUE}Custom Schedule Setup${NC}"
            echo "Cron format: minute hour day month weekday"
            echo "Examples:"
            echo "  0 3 * * *     = Daily at 3:00 AM"
            echo "  0 2 * * 0     = Sunday at 2:00 AM"
            echo "  */30 * * * *  = Every 30 minutes"
            echo

            read -p "Enter cron schedule: " schedule

            echo
            echo "Available scripts:"
            echo "1) daily_cleanup.sh"
            echo "2) weekly_maintenance.sh"
            read -p "Select script (1-2): " script_choice

            case $script_choice in
                1)
                    if add_cron_job "$schedule" "$SCRIPT_DIR/daily_cleanup.sh" "Custom Daily Cleanup"; then
                        echo -e "\n${GREEN}Custom schedule added successfully!${NC}"
                    fi
                    ;;
                2)
                    if add_cron_job "$schedule" "$SCRIPT_DIR/weekly_maintenance.sh" "Custom Weekly Maintenance"; then
                        echo -e "\n${GREEN}Custom schedule added successfully!${NC}"
                    fi
                    ;;
                *)
                    echo -e "${RED}Invalid selection${NC}"
                    ;;
            esac
            ;;

        4)
            # Remove all jobs
            if confirm "Remove all Memory Toolkit cron jobs?"; then
                remove_cron_jobs
            fi
            ;;

        5)
            echo "Exiting..."
            exit 0
            ;;

        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac

    echo
    echo -e "${BLUE}Current cron configuration:${NC}"
    crontab -l 2>/dev/null | grep "Memory Toolkit" || echo "No Memory Toolkit jobs configured"

    echo
    echo -e "${YELLOW}Note: Make sure your Mac is awake at scheduled times for cron jobs to run.${NC}"
    echo -e "${YELLOW}Consider using launchd instead for better reliability on macOS.${NC}"
}

# Run main function
main
