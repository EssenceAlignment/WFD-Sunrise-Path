#!/bin/bash

# Diagnostic script for testing Loki image pulls
# This helps identify if Docker Hub timeouts are network-specific

set -e

echo "=== Docker Hub Network Diagnostics ==="
echo "Date: $(date)"
echo "System: $(uname -a)"
echo ""

# Test basic connectivity
echo "1. Testing Docker Hub connectivity..."
curl -I https://hub.docker.com 2>/dev/null | head -n 1

# Test small image pull
echo -e "\n2. Testing small Alpine image pull..."
time docker pull alpine:3.20

# Test Loki specific version
echo -e "\n3. Testing Loki 2.9.0 pull..."
time docker pull grafana/loki:2.9.0 || {
    echo "ERROR: Loki 2.9.0 pull failed"
    echo "This indicates a network/throttling issue with Docker Hub"
}

# Test alternative registry (GHCR)
echo -e "\n4. Testing alternative registry (GHCR)..."
# Note: Grafana doesn't publish to GHCR, but this shows the pattern
# time docker pull ghcr.io/grafana/loki:2.9.0 || echo "Not available on GHCR"

# Show image sizes
echo -e "\n5. Image size comparison:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(alpine|loki|REPOSITORY)"

# Network diagnostics
echo -e "\n6. Network information:"
curl -s https://ipinfo.io/json 2>/dev/null | jq . || echo "Unable to fetch network info"

# Docker info
echo -e "\n7. Docker daemon info:"
docker version --format 'Client: {{.Client.Version}}\nServer: {{.Server.Version}}'

echo -e "\n=== Diagnostics Complete ==="
echo "If Loki pull failed but Alpine succeeded, consider:"
echo "- Using a Docker registry mirror"
echo "- Scheduling pulls during off-peak hours"
echo "- Using specific tags instead of 'latest'"
echo "- Setting up a local registry cache"
