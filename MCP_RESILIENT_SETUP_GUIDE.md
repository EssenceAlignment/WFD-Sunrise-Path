# MCP Resilient Setup Guide - A Pragmatic Approach

## ⚠️ Reality Check

**Nothing is permanent.** macOS updates break things. Electron apps reset configs. Shell aliases disappear. This guide provides:

- A working setup for today
- Monitoring to detect when it breaks
- Recovery procedures for when (not if) it fails
- Security practices that actually protect secrets

## 🔧 The Resilient Setup

### 1. Version-Controlled Configuration

First, let's create a proper recovery-compass configuration repository:

```bash
mkdir -p ~/recovery-compass-config
cd ~/recovery-compass-config
git init

```text

### 2. Shell Functions (Not Aliases)

Create `~/.recovery-compass/functions.sh`:

```bash
#!/bin/bash

# Recovery Compass Shell Functions

# Source this from .zshrc/.bashrc

recovery_setup() {
    local env_file="/Users/ericjones/Projects/recovery-compass-journeys/recovery-compass-grant-system/.env"
    
    if [ -f "$env_file" ]; then
        # Decrypt if encrypted

        if [ -f "$env_file.age" ]; then
            age -d -i ~/.ssh/id_ed25519 "$env_file.age" > "$env_file.tmp"
            export $(grep -v '^#' "$env_file.tmp" | xargs)
            rm -f "$env_file.tmp"
        else
            export $(grep -v '^#' "$env_file" | xargs)
        fi
        echo "✅ Recovery Compass environment loaded"
    else
        echo "❌ Environment file not found: $env_file"
        return 1
    fi
}

fix_mcp() {
    local config_dir="$HOME/Library/Application Support/Claude"
    local backup_dir="$HOME/.recovery-compass/mcp-backups"
    
    # Create backup

    mkdir -p "$backup_dir"
    if [ -f "$config_dir/claude_desktop_config.json" ]; then
        cp "$config_dir/claude_desktop_config.json" \
           "$backup_dir/claude_desktop_config.$(date +%Y%m%d_%H%M%S).json"
    fi
    
    # Apply minimal config

    cat > "$config_dir/claude_desktop_config.json" << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/ericjones/Documents", "/Users/ericjones/Desktop"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
EOF
    
    echo "✅ MCP config applied. Backups in: $backup_dir"
    echo "📋 Restart Claude Desktop to apply changes"
}

verify_recovery_compass() {
    local status=0
    
    echo "🔍 Verifying Recovery Compass Setup..."
    
    # Check shell functions

    if type recovery_setup &>/dev/null; then
        echo "✅ recovery_setup function available"
    else
        echo "❌ recovery_setup function missing"
        status=1
    fi
    
    # Check MCP config

    local mcp_config="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
    if [ -f "$mcp_config" ]; then
        echo "✅ MCP config exists"
    else
        echo "❌ MCP config missing"
        status=1
    fi
    
    # Check API keys in keychain

    local keys=("recovery-compass-github-token" "recovery-compass-openai-key")
    for key in "${keys[@]}"; do
        if security find-generic-password -s "$key" &>/dev/null; then
            echo "✅ Keychain: $key"
        else
            echo "⚠️  Keychain: $key missing"
        fi
    done
    
    return $status
}

```text

### 3. Encrypted Secrets Management

```bash

# Install age for encryption

brew install age

# Generate encryption key

age-keygen -o ~/.recovery-compass/age.key

# Encrypt your .env file

age -r $(age-keygen -y ~/.recovery-compass/age.key) \
    -o .env.age .env

# Add to .gitignore

echo "*.env" >> .gitignore
echo "!*.env.age" >> .gitignore

```text

### 4. Health Check Script

Create `~/.recovery-compass/health-check.sh`:

```bash
#!/bin/bash

# Recovery Compass Health Check

# Run daily via cron/launchd

log_file="$HOME/.recovery-compass/health-check.log"
slack_webhook="YOUR_SLACK_WEBHOOK_URL"

check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[$(date)] ❌ Missing: $1" >> "$log_file"
        return 1
    fi
    return 0
}

check_command_exists() {
    if ! command -v "$1" &>/dev/null; then
        echo "[$(date)] ❌ Missing command: $1" >> "$log_file"
        return 1
    fi
    return 0
}

# Run checks

errors=0

check_file_exists "$HOME/.recovery-compass/functions.sh" || ((errors++))
check_file_exists "$HOME/Library/Application Support/Claude/claude_desktop_config.json" || ((errors++))
check_command_exists "npx" || ((errors++))
check_command_exists "age" || ((errors++))

# Check if functions are sourced

if ! type recovery_setup &>/dev/null; then
    echo "[$(date)] ❌ Shell functions not loaded" >> "$log_file"
    ((errors++))
fi

# Alert if errors

if [ $errors -gt 0 ]; then
    # Send to Slack if webhook configured

    if [ -n "$slack_webhook" ]; then
        curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"⚠️ Recovery Compass health check failed with $errors errors\"}" \
            "$slack_webhook"
    fi
    exit 1
fi

echo "[$(date)] ✅ All checks passed" >> "$log_file"

```text

### 5. LaunchAgent for Monitoring

Create `~/Library/LaunchAgents/com.recovery-compass.health-check.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.recovery-compass.health-check</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/ericjones/.recovery-compass/health-check.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>86400</integer>
    <key>StandardOutPath</key>
    <string>/Users/ericjones/.recovery-compass/health-check.out</string>
    <key>StandardErrorPath</key>
    <string>/Users/ericjones/.recovery-compass/health-check.err</string>
</dict>
</plist>

```text

Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.recovery-compass.health-check.plist

```text

### 6. Manual Recovery Procedures

When everything breaks, here's the manual path:

```bash

# 1. Recreate MCP config manually

mkdir -p "$HOME/Library/Application Support/Claude"
cat > "$HOME/Library/Application Support/Claude/claude_desktop_config.json" << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/ericjones/Documents", "/Users/ericjones/Desktop"]
    }
  }
}
EOF

# 2. Load API keys manually

export OPENAI_API_KEY=$(security find-generic-password -s "recovery-compass-openai-key" -w)
export GITHUB_TOKEN=$(security find-generic-password -s "recovery-compass-github-token" -w)

# 3. Verify

echo $OPENAI_API_KEY | head -c 10

```text

## 🛡️ Security Hardening

### Keychain Integration

```bash

# Add API key to keychain

security add-generic-password \
    -a "$USER" \
    -s "recovery-compass-openai-key" \
    -w "your-api-key-here"

# Retrieve from keychain

security find-generic-password \
    -s "recovery-compass-openai-key" \
    -w

```text

### Git-Crypt for Team Sharing

```bash

# Setup git-crypt

brew install git-crypt
cd ~/recovery-compass-config
git-crypt init

# Add files to encrypt

echo ".env filter=git-crypt diff=git-crypt" >> .gitattributes
echo "*.key filter=git-crypt diff=git-crypt" >> .gitattributes

# Add team members

git-crypt add-gpg-user teammate@example.com

```text

## 📊 Realistic Expectations

### What Will Break

- **Shell configs**: OS updates, Oh My Zsh updates
- **MCP configs**: Claude Desktop updates, Electron migrations
- **API keys**: Rotation policies, expiration
- **File paths**: Project moves, disk migrations

### Maintenance Schedule

- **Daily**: Automated health checks
- **Weekly**: Manual verification
- **Monthly**: Update encrypted secrets
- **Quarterly**: Disaster recovery drill

### Recovery Time Objectives

- **Shell functions down**: 5 minutes (re-source)
- **MCP broken**: 10 minutes (run fix function)
- **Total system failure**: 30 minutes (manual recovery)

## 🚨 When This Guide Fails

Because it will. Here's what to do:

1. **Check the logs**:

   ```bash
   tail -f ~/.recovery-compass/health-check.log
   ```

2. **Run manual verification**:

   ```bash
   ~/.recovery-compass/verify_recovery_compass
   ```

3. **Restore from backup**:

   ```bash
   cp ~/.recovery-compass/mcp-backups/claude_desktop_config.*.json \
      "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
   ```

4. **Nuclear option** - Start fresh:

   ```bash
   rm -rf ~/.recovery-compass
   rm "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
   # Then rebuild from this guide

   ```

## 🎯 The Truth

This setup will last weeks, maybe months. Then something will break. The value isn't in permanence—it's in:

- Quick recovery when things break
- Monitoring to catch breaks early
- Documentation for future you
- Security that actually protects secrets

**Accept the impermanence. Plan for recovery. Document everything.**

---
Last tested: January 29, 2025  
Next review: February 29, 2025  
Break glass procedure: See section 6
