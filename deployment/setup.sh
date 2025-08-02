#!/bin/bash
# Recovery Compass MCP Launcher Setup Script

set -euo pipefail

echo "=== Recovery Compass MCP Launcher Setup ==="

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use sudo)"
   exit 1
fi

# Create recovery user if not exists
if ! id "recovery" &>/dev/null; then
    echo "Creating recovery user..."
    useradd -r -s /bin/false recovery
fi

# Create directories
echo "Creating directories..."
mkdir -p /etc/recovery-compass
mkdir -p /opt/recovery-compass/mcp-launcher
mkdir -p /var/lib/recovery-compass/ctx

# Set permissions
chown -R recovery:recovery /var/lib/recovery-compass
chmod 755 /var/lib/recovery-compass

# Copy launcher files
echo "Installing MCP launcher..."
cp -r mcp-launcher/* /opt/recovery-compass/mcp-launcher/
chown -R recovery:recovery /opt/recovery-compass/mcp-launcher

# Create environment file template if not exists
if [ ! -f /etc/recovery-compass/env ]; then
    echo "Creating environment template..."
    cat > /etc/recovery-compass/env <<'EOF'
# Recovery Compass MCP Environment Variables
# IMPORTANT: Add your actual CF_API_TOKEN here
CF_API_TOKEN=
CF_ACCOUNT_ID=8147f0100bb7ce99a5c143b6cf6976da
EOF
    chmod 640 /etc/recovery-compass/env
    chown root:recovery /etc/recovery-compass/env
    echo ""
    echo "⚠️  IMPORTANT: Edit /etc/recovery-compass/env and add your CF_API_TOKEN"
    echo ""
fi

# Install systemd service
echo "Installing systemd service..."
cp deployment/mcp.service /etc/systemd/system/
systemctl daemon-reload

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Edit /etc/recovery-compass/env and add your CF_API_TOKEN"
echo "2. Start the service: sudo systemctl start mcp"
echo "3. Enable auto-start: sudo systemctl enable mcp"
echo "4. Check status: sudo systemctl status mcp"
echo "5. View logs: sudo journalctl -u mcp -f"
echo ""
echo "Health check: curl http://localhost:8787/healthz"
echo ""
