#!/bin/bash

# macOS Memory Management Toolkit - Installation Script
# This script sets up the toolkit and configures shell integration

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}macOS Memory Management Toolkit - Installation${NC}"
echo "=============================================="
echo

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}Error: This toolkit is designed for macOS only${NC}"
    exit 1
fi

# Make all scripts executable
echo -e "${BLUE}Setting up permissions...${NC}"
find "$SCRIPT_DIR" -name "*.sh" -type f -exec chmod +x {} \;
echo -e "${GREEN}✓ Permissions set${NC}"

# Create necessary directories
echo -e "\n${BLUE}Creating directories...${NC}"
mkdir -p "$HOME/Library/Logs/memory-toolkit/"{benchmarks,reports}
echo -e "${GREEN}✓ Log directories created${NC}"

# Detect shell type
SHELL_TYPE=""
SHELL_RC=""

if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_TYPE="zsh"
    SHELL_RC="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_TYPE="bash"
    SHELL_RC="$HOME/.bashrc"
    # On macOS, .bash_profile is often used instead
    if [[ -f "$HOME/.bash_profile" ]]; then
        SHELL_RC="$HOME/.bash_profile"
    fi
else
    echo -e "${YELLOW}Warning: Unable to detect shell type${NC}"
    echo "You'll need to manually add the aliases to your shell configuration"
fi

# Add aliases to shell configuration
if [[ -n "$SHELL_RC" ]]; then
    echo -e "\n${BLUE}Configuring shell aliases...${NC}"

    # Check if already installed
    if grep -q "macos-memory-toolkit/config/aliases.sh" "$SHELL_RC" 2>/dev/null; then
        echo -e "${YELLOW}Aliases already configured in $SHELL_RC${NC}"
    else
        # Backup existing configuration
        cp "$SHELL_RC" "$SHELL_RC.backup.$(date +%Y%m%d_%H%M%S)"

        # Add source line
        echo "" >> "$SHELL_RC"
        echo "# macOS Memory Management Toolkit" >> "$SHELL_RC"
        echo "source \"$SCRIPT_DIR/config/aliases.sh\"" >> "$SHELL_RC"

        echo -e "${GREEN}✓ Aliases added to $SHELL_RC${NC}"
        echo -e "${YELLOW}Note: Restart your terminal or run: source $SHELL_RC${NC}"
    fi
fi

# Test core functionality
echo -e "\n${BLUE}Testing installation...${NC}"

# Test common functions
if source "$SCRIPT_DIR/utils/common_functions.sh" 2>/dev/null; then
    echo -e "${GREEN}✓ Common functions loaded${NC}"
else
    echo -e "${RED}✗ Failed to load common functions${NC}"
    exit 1
fi

# Check for required commands
echo -e "\n${BLUE}Checking dependencies...${NC}"

MISSING_DEPS=()

# Check for required commands
for cmd in vm_stat sysctl ps kill rm find; do
    if ! command -v "$cmd" &> /dev/null; then
        MISSING_DEPS+=("$cmd")
    fi
done

if [[ ${#MISSING_DEPS[@]} -eq 0 ]]; then
    echo -e "${GREEN}✓ All dependencies found${NC}"
else
    echo -e "${RED}Missing dependencies: ${MISSING_DEPS[*]}${NC}"
    echo "Please install missing commands and try again"
    exit 1
fi

# Optional: Create desktop shortcut
echo -e "\n${BLUE}Additional setup options:${NC}"
echo -n "Create desktop shortcuts? (y/N): "
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    cat > "$HOME/Desktop/Memory Check.command" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
./core/memory_check.sh
echo
echo "Press any key to close..."
read -n 1
EOF
    chmod +x "$HOME/Desktop/Memory Check.command"

    cat > "$HOME/Desktop/Memory Clean.command" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
./core/memory_clean.sh
echo
echo "Press any key to close..."
read -n 1
EOF
    chmod +x "$HOME/Desktop/Memory Clean.command"

    echo -e "${GREEN}✓ Desktop shortcuts created${NC}"
fi

# Display configuration summary
echo -e "\n${GREEN}Installation Complete!${NC}"
echo
echo "Installed at: $SCRIPT_DIR"
echo "Configuration: $SCRIPT_DIR/config/settings.conf"
echo "Logs directory: $HOME/Library/Logs/memory-toolkit/"
echo

# Show available commands
echo -e "${BLUE}Available Commands:${NC}"
echo "  memcheck    - Check memory status"
echo "  memclean    - Safe memory cleanup"
echo "  memdeep     - Deep cleanup (sudo)"
echo "  memrescue   - Emergency recovery (sudo)"
echo "  memmon      - Real-time monitor"
echo "  membench    - Performance benchmark"
echo "  memreport   - Health report"
echo "  memhelp     - Show help"
echo

# Final instructions
if [[ -n "$SHELL_RC" ]]; then
    echo -e "${YELLOW}To activate the toolkit:${NC}"
    echo "  source $SHELL_RC"
    echo "  OR restart your terminal"
else
    echo -e "${YELLOW}To activate the toolkit:${NC}"
    echo "  Add this line to your shell configuration:"
    echo "  source \"$SCRIPT_DIR/config/aliases.sh\""
fi

echo
echo -e "${GREEN}Type 'memhelp' after activation for usage information${NC}"
