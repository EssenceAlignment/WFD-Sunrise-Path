# Cloudflare MCP Server Troubleshooting Guide

## 🔧 Common Connection Issues & Solutions

### Error: "localhost refused to connect"

This error typically means the MCP server isn't running or is configured incorrectly.

## 📋 Troubleshooting Steps

### 1. Check MCP Server Status

```bash
# Check if the MCP server process is running
ps aux | grep cloudflare-server

# Check if port is in use (MCP servers typically use specific ports)
lsof -i :PORT_NUMBER
```text

### 2. Verify MCP Configuration

Check your MCP configuration file (usually in `~/.config/claude/mcp.json` or similar):

```json
{
  "mcpServers": {
    "cloudflare-analyzer": {
      "command": "node",
      "args": ["/Users/ericjones/Documents/Cline/MCP/cloudflare-server/build/index.js"],
      "env": {
        "CLOUDFLARE_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```text

### 3. Common Fixes

#### A. Restart the MCP Server

```bash
# Navigate to the cloudflare server directory
cd /Users/ericjones/Documents/Cline/MCP/cloudflare-server

# Rebuild if necessary
npm run build

# Start the server manually to see errors
node build/index.js
```text

#### B. Check Environment Variables

Ensure your Cloudflare API credentials are set:

```bash
# Check if environment variable is set
echo $CLOUDFLARE_API_TOKEN

# Or set it temporarily
export CLOUDFLARE_API_TOKEN="your-token-here"
```text

#### C. Permission Issues

```bash
# Ensure the server has execute permissions
chmod +x /Users/ericjones/Documents/Cline/MCP/cloudflare-server/build/index.js

# Check file ownership
ls -la /Users/ericjones/Documents/Cline/MCP/cloudflare-server/
```text

### 4. Alternative: Direct Cloudflare API Usage

If MCP continues to fail, you can interact with Cloudflare directly:

#### Using Wrangler CLI

```bash
# Install Wrangler globally
npm install -g wrangler

# Login to Cloudflare
wrangler login

# List your Workers
wrangler list

# Deploy a Worker
wrangler deploy
```text

#### Using cURL for API Calls

```bash
# Example: List zones
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
     -H "Authorization: Bearer YOUR_API_TOKEN" \
     -H "Content-Type: application/json"
```text

### 5. Debug MCP Server

Create a test script to debug the server:

```javascript
// test-mcp-server.js
const { spawn } = require('child_process');

const server = spawn('node', [
  '/Users/ericjones/Documents/Cline/MCP/cloudflare-server/build/index.js'
]);

server.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

server.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

server.on('close', (code) => {
  console.log(`Server exited with code ${code}`);
});
```text

### 6. Check Dependencies

```bash
# Navigate to the server directory
cd /Users/ericjones/Documents/Cline/MCP/cloudflare-server

# Check if all dependencies are installed
npm list

# Reinstall dependencies
npm install

# Check for vulnerabilities
npm audit
```text

### 7. Firewall/Security Software

- Check if any firewall is blocking localhost connections
- Temporarily disable antivirus/security software
- Check macOS Security & Privacy settings

### 8. Alternative MCP Server Setup

If the current server continues to fail, consider:

1. **Using the filesystem MCP server instead** (which is confirmed working)
2. **Creating a simpler proxy server** for Cloudflare operations
3. **Using Cloudflare's REST API directly** in your code

## 🚀 Quick Recovery Path

If you need to continue working without MCP:

1. **For Secrets Store**: Use `wrangler secret put` directly
2. **For Turnstile**: Implement via Cloudflare dashboard
3. **For AI Gateway**: Configure through Cloudflare UI

## 📞 Support Resources

- Cloudflare Discord: <https://discord.cloudflare.com>
- MCP GitHub Issues: Check the MCP repository for known issues
- Cloudflare Status: <https://www.cloudflarestatus.com/>

## 💡 Workaround for Recovery Compass

Since your Cloudflare infrastructure is already deployed, you can:

1. Use the Cloudflare dashboard for manual operations
2. Use Wrangler CLI for deployments
3. Implement the security features directly in your code

The MCP server is a convenience tool, not a blocker for your progress!

---

**Note**: The Cloudflare features (Secrets Store, Turnstile, AI Gateway) can all be implemented without the MCP server. Your Recovery Compass infrastructure remains fully functional.
