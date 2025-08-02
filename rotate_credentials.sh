#!/bin/bash
# Credential Rotation Helper Script
# Date: August 1, 2025

echo "🔐 Recovery Compass Credential Rotation Helper"
echo "============================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to store in keychain
store_in_keychain() {
    local service_name=$1
    local account=$2
    local password=$3

    security add-generic-password -U -a "$account" -s "$service_name" -w "$password"
    echo -e "${GREEN}✅ Stored in keychain: $service_name${NC}"
}

# Function to check if value exists in keychain
check_keychain() {
    local service_name=$1
    if security find-generic-password -s "$service_name" &>/dev/null; then
        echo -e "${GREEN}✓ Found: $service_name${NC}"
    else
        echo -e "${RED}✗ Missing: $service_name${NC}"
    fi
}

echo -e "\n${YELLOW}Step 1: Checking existing keychain entries${NC}"
echo "----------------------------------------"
check_keychain "recovery-compass-cf-token"
check_keychain "recovery-compass-github-token"
check_keychain "recovery-compass-supabase-service"
check_keychain "recovery-compass-openai-key"
check_keychain "recovery-compass-anthropic-key"

echo -e "\n${YELLOW}Step 2: Rotation Checklist${NC}"
echo "----------------------------------------"
echo "[ ] 1. Supabase: https://supabase.com/dashboard/project/shcuzhyonrpacdynxjjd/settings/api"
echo "[ ] 2. OpenAI: https://platform.openai.com/api-keys"
echo "[ ] 3. Anthropic: https://console.anthropic.com/settings/keys"
echo "[ ] 4. GitHub: https://github.com/settings/tokens"
echo "[ ] 5. Docker: https://hub.docker.com/settings/security"
echo "[ ] 6. Linear: https://linear.app/settings/api"
echo "[ ] 7. Airtable: https://airtable.com/create/tokens"
echo "[ ] 8. Perplexity: https://www.perplexity.ai/settings/api"

echo -e "\n${YELLOW}Step 3: Commands to run after rotation${NC}"
echo "----------------------------------------"
echo "# Example: Store new credentials (DO NOT PASTE ACTUAL KEYS HERE)"
echo 'security add-generic-password -U -a "$USER" -s "recovery-compass-supabase-service" -w "NEW_SERVICE_KEY"'
echo 'security add-generic-password -U -a "$USER" -s "recovery-compass-openai-key" -w "NEW_OPENAI_KEY"'

echo -e "\n${YELLOW}Step 4: Update Cloudflare Secrets${NC}"
echo "----------------------------------------"
echo "# After rotation, update production secrets:"
echo 'export CF_TOKEN=$(security find-generic-password -s "recovery-compass-cf-token" -w)'
echo 'wrangler secret put SUPABASE_SERVICE_KEY'
echo 'wrangler secret put OPENAI_API_KEY'

echo -e "\n${RED}IMPORTANT: Never paste actual keys in terminal or logs!${NC}"
