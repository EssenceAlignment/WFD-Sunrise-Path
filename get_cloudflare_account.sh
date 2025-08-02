#!/bin/bash

# Get Cloudflare Account ID using API Token
API_TOKEN=$(security find-generic-password -s "recovery-compass-cf-token" -w | tr -d '\n')

echo "🔍 Fetching Cloudflare Account ID..."
echo "📊 Token length: ${#API_TOKEN} characters"

# Try to get zones which will include account information
response=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones" \
     -H "Authorization: Bearer $API_TOKEN" \
     -H "Content-Type: application/json")

# Extract account ID from the zones response
account_id=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['result'][0]['account']['id'] if data.get('success') and data.get('result') else '')" 2>/dev/null)

if [ -z "$account_id" ]; then
    echo "❌ Failed to get account ID"
    echo "Response: $response"
else
    echo "✅ Found Account ID: $account_id"

    # Store it in keychain for future use
    security add-generic-password -a "$USER" -s "recovery-compass-cf-account-id" -w "$account_id" 2>/dev/null || \
    security add-generic-password -U -a "$USER" -s "recovery-compass-cf-account-id" -w "$account_id"

    echo "💾 Saved to keychain as 'recovery-compass-cf-account-id'"
fi
