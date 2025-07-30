#!/bin/bash
# Test Kompose conversion locally
# This simulates what the CI will do

echo "=== Kompose Conversion Test ==="
echo "This script tests conversion of docker-compose to Kubernetes manifests"
echo ""

# Check if Kompose is installed
if ! command -v kompose &> /dev/null; then
    echo "❌ Kompose not installed locally"
    echo "To install: brew install kompose (Mac) or see https://kompose.io"
    echo ""
    echo "The CI workflow will handle this automatically."
    exit 0
fi

echo "✅ Kompose found: $(kompose version)"
echo ""

# Create output directory
mkdir -p k8s-manifests

# Convert minimal stack
echo "Converting docker-compose.minimal.yml..."
kompose convert -f docker-compose.minimal.yml -o k8s-manifests/

# Check results
echo ""
echo "=== Generated Kubernetes Manifests ==="
ls -la k8s-manifests/

echo ""
echo "=== Summary ==="
echo "Deployments: $(ls k8s-manifests/*deployment.yaml 2>/dev/null | wc -l)"
echo "Services: $(ls k8s-manifests/*service.yaml 2>/dev/null | wc -l)"
echo "PVCs: $(ls k8s-manifests/*persistentvolumeclaim.yaml 2>/dev/null | wc -l)"
echo "ConfigMaps: $(ls k8s-manifests/*configmap.yaml 2>/dev/null | wc -l)"

echo ""
echo "✅ Kompose conversion test complete"
echo "See k8s-manifests/ for generated files"
