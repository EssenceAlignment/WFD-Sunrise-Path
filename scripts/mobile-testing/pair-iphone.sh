#!/bin/bash

# Recovery Compass iPhone Pairing & Debug Setup
# Handles device pairing, logging, and Web Inspector bridge

echo "📱 Recovery Compass iPhone Pairing & Debug Setup"
echo "==============================================="

# Check if device is connected
echo "🔍 Checking for connected iOS devices..."
DEVICE_ID=$(idevice_id -l | head -1)

if [ -z "$DEVICE_ID" ]; then
    echo "❌ No iOS device found. Please connect your iPhone via USB."
    echo "   Make sure to unlock your device and trust this computer."
    exit 1
fi

echo "✅ Found device: $DEVICE_ID"

# Pair device
echo "🔐 Pairing with device..."
idevicepair pair
PAIR_STATUS=$?

if [ $PAIR_STATUS -ne 0 ]; then
    echo "⚠️  Pairing failed. Trying to validate existing pairing..."
    idevicepair validate
    VALIDATE_STATUS=$?

    if [ $VALIDATE_STATUS -ne 0 ]; then
        echo "❌ Device pairing failed. Please:"
        echo "   1. Unlock your iPhone"
        echo "   2. Tap 'Trust' when prompted"
        echo "   3. Run this script again"
        exit 1
    fi
fi

echo "✅ Device paired successfully!"

# Start device logging
echo "📝 Starting device console logging..."
echo "   Logs will be saved to: ./iphone_logs.txt"
echo "   Press Ctrl+C to stop logging"

# Kill any existing logging processes
pkill -f "idevicesyslog" 2>/dev/null

# Start logging in background
idevicesyslog -u "$DEVICE_ID" > iphone_logs.txt 2>&1 &
SYSLOG_PID=$!
echo "   Logging process started (PID: $SYSLOG_PID)"

# Start Web Inspector proxy
echo "🌐 Starting Safari Web Inspector proxy..."

# Kill any existing proxy processes
pkill -f "ios_webkit_debug_proxy" 2>/dev/null

# Start proxy
ios_webkit_debug_proxy -c "$DEVICE_ID":9221,:9222-9322 &
PROXY_PID=$!
echo "   Web Inspector proxy started (PID: $PROXY_PID)"
echo "   Access at: http://localhost:9221"

# Create stop script
cat > scripts/mobile-testing/stop-iphone-debug.sh <<EOF
#!/bin/bash
echo "🛑 Stopping iPhone debug services..."
pkill -f "idevicesyslog"
pkill -f "ios_webkit_debug_proxy"
echo "✅ Services stopped"
EOF

chmod +x scripts/mobile-testing/stop-iphone-debug.sh

echo ""
echo "✅ iPhone testing environment ready!"
echo ""
echo "📋 Next steps:"
echo "1. Open Safari on your Mac"
echo "2. Enable Develop menu: Safari → Preferences → Advanced → Show Develop menu"
echo "3. Go to: Develop → [Your iPhone] → recovery-compass.org"
echo ""
echo "🛑 To stop debugging services, run:"
echo "   ./scripts/mobile-testing/stop-iphone-debug.sh"
echo ""
echo "📊 Logs are being saved to: ./iphone_logs.txt"
