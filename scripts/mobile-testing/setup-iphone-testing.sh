#!/bin/bash

# Recovery Compass iPhone Developer Testing Setup Script
# Configures macOS environment for mobile testing

echo "🚀 Recovery Compass iPhone Developer Testing Setup"
echo "=================================================="

# Check for CI mode
CI_MODE=false
if [[ "$1" == "--ci" ]] || [[ "$CI" == "true" ]]; then
    CI_MODE=true
    echo "🤖 Running in CI mode"
fi

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script requires macOS to test iOS devices"
    exit 1
fi

# Skip Homebrew setup in CI
if [[ "$CI_MODE" == false ]]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "📦 Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    echo "📱 Installing iOS development tools..."

    # Install required tools
    brew install libimobiledevice ideviceinstaller ios-webkit-debug-proxy ffmpeg node@20 2>/dev/null || {
        echo "⚠️  Some tools may already be installed, continuing..."
    }
else
    echo "🤖 Skipping Homebrew setup in CI mode"
fi

# Install global NPM tools
echo "📦 Installing Playwright for mobile testing..."
npm install -g playwright@1.44.0 ts-node typescript 2>/dev/null || {
    echo "⚠️  Some npm packages may already be installed, continuing..."
}

# Create testing directory if not in project
if [[ ! -d "tests/mobile" ]]; then
    mkdir -p tests/mobile/ios scripts/mobile-testing docs/mobile-testing screenshots
fi

# Initialize package.json for Playwright if needed
if [[ ! -f "package.json" ]] || ! grep -q "playwright" package.json; then
    echo "🎭 Setting up Playwright..."
    npm install --save-dev @playwright/test typescript
    npx playwright install webkit
fi

# Create TypeScript config for tests
cat > tsconfig.test.json <<'EOF'
{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "moduleResolution": "node",
    "types": ["@playwright/test"],
    "outDir": "./dist",
    "rootDir": "./tests"
  },
  "include": ["tests/**/*.ts"]
}
EOF

echo "✅ Setup complete!"
echo ""
echo "📱 Next steps:"
echo "1. Enable Developer Mode on your iPhone:"
echo "   Settings → Privacy & Security → Developer Mode → ON"
echo ""
echo "2. Enable Safari Web Inspector:"
echo "   Settings → Safari → Advanced → Web Inspector → ON"
echo ""
echo "3. Configure Network Link Conditioner:"
echo "   Settings → Developer → Network Link Conditioner → 3G Lossy"
echo ""
echo "4. Connect iPhone via USB and run:"
echo "   ./scripts/mobile-testing/pair-iphone.sh"
