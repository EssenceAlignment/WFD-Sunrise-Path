#!/bin/bash
# Universal Pre-Commit Force-Field
# One hook → Five problem clusters vanish → Compound quality every commit

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛡️  UNIVERSAL PRE-COMMIT FORCE-FIELD ACTIVATED${NC}"
echo "=================================================="

# Check if Python script exists
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/../scripts/force_field_implementation.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}❌ Force field implementation not found at: $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Run the Python implementation
python3 "$PYTHON_SCRIPT" "$@"
exit_code=$?

# Show force multiplication summary
if [ $exit_code -eq 0 ]; then
    echo -e "\n${GREEN}🌟 Force Multiplication Achieved!${NC}"
    echo "  → Markdown: Auto-formatted & validated"
    echo "  → Secrets: Scanned & blocked"
    echo "  → Vulnerabilities: Detected & prevented"
    echo "  → Docker: Configs validated"
    echo "  → Dependencies: Security checked"
    echo -e "\n${BLUE}Compound benefits: Every commit improves quality${NC}"
else
    echo -e "\n${RED}⚠️  Force Field Blocked Commit${NC}"
    echo "Fix the issues above and try again."
    echo -e "\n${YELLOW}Tip: Use 'git commit --allow-lint' to bypass lint errors only${NC}"
fi

exit $exit_code
