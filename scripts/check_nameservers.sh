#!/bin/bash
# Check nameserver propagation for recovery-compass.org

echo "Checking nameservers for recovery-compass.org..."
NS_RESULT=$(dig +short NS recovery-compass.org | sort)
echo "$NS_RESULT"

# Check if we have the correct nameservers
if echo "$NS_RESULT" | grep -q "desi.ns.cloudflare.com" && \
   echo "$NS_RESULT" | grep -q "fred.ns.cloudflare.com" && \
   ! echo "$NS_RESULT" | grep -q "becky.ns.cloudflare.com" && \
   ! echo "$NS_RESULT" | grep -q "joel.ns.cloudflare.com"; then
    echo "✅ Nameservers updated successfully!"
    echo "Zone should now be active in Cloudflare."
    exit 0
else
    echo "⏳ Still showing old nameservers. Propagation pending..."
    echo "Expected: desi.ns.cloudflare.com, fred.ns.cloudflare.com"
    echo "Current: $NS_RESULT"
    exit 1
fi
