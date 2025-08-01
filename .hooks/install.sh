#!/bin/bash
# Force Field Installation Script
# Installs pre-commit hooks for force multiplication

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "🛡️  Installing Universal Pre-Commit Force-Field"
echo "=============================================="

# Make scripts executable
chmod +x "$SCRIPT_DIR/force_field.sh"
chmod +x "$REPO_ROOT/scripts/force_field_implementation.py"

# Install husky for JS projects
if [ -f "$REPO_ROOT/package.json" ]; then
    echo "📦 Installing husky for JavaScript project..."
    cd "$REPO_ROOT"
    npm install --save-dev husky
    npx husky install
    npx husky add .husky/pre-commit "$SCRIPT_DIR/force_field.sh"
    echo "✅ Husky pre-commit hook installed"
fi

# Install pre-commit for Python projects
if [ -f "$REPO_ROOT/requirements.txt" ] || [ -f "$REPO_ROOT/setup.py" ]; then
    echo "🐍 Installing pre-commit for Python project..."
    pip install pre-commit

    # Create .pre-commit-config.yaml
    cat > "$REPO_ROOT/.pre-commit-config.yaml" << EOF
repos:
  - repo: local
    hooks:
      - id: force-field
        name: Universal Pre-Commit Force-Field
        entry: .hooks/force_field.sh
        language: script
        pass_filenames: false
        always_run: true
EOF

    pre-commit install
    echo "✅ Pre-commit hook installed"
fi

# Install dependencies
echo ""
echo "📋 Installing force-field dependencies..."

# Check and install required tools
tools=(
    "markdownlint:npm install -g markdownlint-cli"
    "detect-secrets:pip install detect-secrets"
    "trivy:brew install trivy || curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin"
    "cspell:npm install -g cspell"
)

for tool_cmd in "${tools[@]}"; do
    tool="${tool_cmd%%:*}"
    install="${tool_cmd#*:}"

    if ! command -v "$tool" &> /dev/null; then
        echo "Installing $tool..."
        eval "$install"
    else
        echo "✓ $tool already installed"
    fi
done

# Create .secrets.baseline if it doesn't exist
if [ ! -f "$REPO_ROOT/.secrets.baseline" ]; then
    echo "Creating secrets baseline..."
    cd "$REPO_ROOT"
    detect-secrets scan --baseline .secrets.baseline
fi

# Create metrics directory
mkdir -p "$REPO_ROOT/metrics"

echo ""
echo "✅ Force-Field Installation Complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Test the hook: git commit -m 'test'"
echo "2. Review blocked issues (if any)"
echo "3. Commit with confidence!"
echo ""
echo "💡 Force multiplication achieved:"
echo "   One hook → Five problem clusters prevented → Compound quality"
