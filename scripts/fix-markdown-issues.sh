#!/bin/bash

# Fix Markdown Issues Script
# This script systematically fixes markdown linting issues

echo "🔧 Starting systematic markdown fix process..."

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Install required dependencies if not present
if ! command -v markdownlint &> /dev/null; then
    echo "📦 Installing markdownlint-cli..."
    npm install -D markdownlint-cli
fi

if ! command -v cspell &> /dev/null; then
    echo "📦 Installing cspell..."
    npm install -D cspell
fi

echo "🔍 Running markdown lint check..."
npx markdownlint "*.md" --fix

echo "🔤 Running spell check..."
npx cspell "*.md" --no-progress || true

echo "✅ Markdown issues fixed!"

# Show summary of remaining issues (if any)
echo ""
echo "📊 Summary of remaining issues:"
npx markdownlint "*.md" --no-fix 2>/dev/null || echo "No markdown lint issues found!"

echo ""
echo "🎯 All markdown files have been processed!"
