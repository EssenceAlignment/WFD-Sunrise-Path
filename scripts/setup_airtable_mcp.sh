#!/bin/bash

# Recovery Compass Airtable MCP Server Setup
# This script sets up the Airtable MCP integration for funding lead management

echo "🚀 Setting up Airtable MCP Server for Recovery Compass..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if API key exists in keychain
check_api_key() {
    echo -e "${YELLOW}Checking for Airtable API key in keychain...${NC}"

    if security find-generic-password -s "recovery-compass-airtable-key" -w &>/dev/null; then
        echo -e "${GREEN}✅ Airtable API key found in keychain${NC}"
        return 0
    else
        echo -e "${RED}❌ Airtable API key not found in keychain${NC}"
        echo "Please add your Airtable API key to keychain:"
        echo "security add-generic-password -a \"\$USER\" -s \"recovery-compass-airtable-key\" -w \"your-api-key-here\""
        return 1
    fi
}

# Install Airtable MCP server
install_airtable_server() {
    echo -e "${YELLOW}Installing Airtable MCP server...${NC}"

    # Test if npm/npx is available
    if ! command -v npx &> /dev/null; then
        echo -e "${RED}❌ npx not found. Please install Node.js first.${NC}"
        return 1
    fi

    # Pre-install to cache
    echo "Pre-installing @domdomegg/mcp-server-airtable..."
    npm install -g @domdomegg/mcp-server-airtable

    echo -e "${GREEN}✅ Airtable MCP server installed${NC}"
}

# Test Airtable connection
test_airtable_connection() {
    echo -e "${YELLOW}Testing Airtable connection...${NC}"

    # Get API key from keychain
    API_KEY=$(security find-generic-password -s "recovery-compass-airtable-key" -w 2>/dev/null)

    if [ -z "$API_KEY" ]; then
        echo -e "${RED}❌ Could not retrieve API key${NC}"
        return 1
    fi

    # Test API connection with curl
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer $API_KEY" \
        "https://api.airtable.com/v0/meta/bases")

    if [ "$RESPONSE" = "200" ]; then
        echo -e "${GREEN}✅ Airtable API connection successful${NC}"
        return 0
    else
        echo -e "${RED}❌ Airtable API connection failed (HTTP $RESPONSE)${NC}"
        return 1
    fi
}

# Main setup
main() {
    echo "Recovery Compass Airtable MCP Integration Setup"
    echo "=============================================="
    echo ""

    # Check API key
    if ! check_api_key; then
        exit 1
    fi

    # Install server
    install_airtable_server

    # Test connection
    if test_airtable_connection; then
        echo ""
        echo -e "${GREEN}✅ Airtable MCP server setup complete!${NC}"
        echo ""
        echo "Next steps:"
        echo "1. Restart Claude Desktop to load the new configuration"
        echo "2. Look for 'airtable' in the MCP servers list"
        echo "3. Use the Airtable tools to manage funding leads"
        echo ""
        echo "Available Airtable tools:"
        echo "- List bases"
        echo "- List tables"
        echo "- Read/write records"
        echo "- Manage fields and schemas"
    else
        echo -e "${RED}Setup completed with warnings. Please check your API key.${NC}"
    fi
}

# Run main
main
