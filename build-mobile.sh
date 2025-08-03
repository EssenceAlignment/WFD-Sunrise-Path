#!/bin/bash

# WFD Dashboard Mobile Build Script

echo "🏗️  Building WFD Dashboard for mobile deployment..."

# Create dist directory
echo "📁 Creating dist directory..."
mkdir -p dist

# Copy HTML files
echo "📄 Copying HTML files..."
cp index.html dist/ 2>/dev/null || echo "⚠️  index.html not found"
cp wfd-survey.html dist/ 2>/dev/null || echo "⚠️  wfd-survey.html not found"
cp mcp-dashboard.html dist/ 2>/dev/null || true

# Copy directories if they exist
echo "📂 Copying resource directories..."
[ -d "styles" ] && cp -r styles dist/ && echo "✅ Copied styles directory"
[ -d "scripts" ] && cp -r scripts dist/ && echo "✅ Copied scripts directory"
[ -d "src" ] && cp -r src dist/ && echo "✅ Copied src directory"

# Copy any other static assets
[ -f "favicon.ico" ] && cp favicon.ico dist/

echo ""
echo "✅ Build complete! Your web app is ready in the 'dist' directory."
echo ""
echo "Next steps:"
echo "1. Run 'npm run cap:sync' to sync with Capacitor"
echo "2. Run 'npm run cap:run:ios' or 'npm run cap:run:android' to test on devices"
echo ""
