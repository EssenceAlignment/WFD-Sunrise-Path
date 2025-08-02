# 🔐 Recovery Compass Secure Credentials Reference

## ✅ All Credentials Stored Securely in macOS Keychain (August 1, 2025)

### 🔑 Accessing Your Credentials

#### Cloudflare API Token:
```bash
security find-generic-password -s "recovery-compass-cf-token" -w
```

#### Cloudflare Zone ID:
```bash
security find-generic-password -s "recovery-compass-cf-zone-id" -w
```

#### Cloudflare Secret Key:
```bash
security find-generic-password -s "recovery-compass-cf-secret" -w
```

#### GitHub Token:
```bash
security find-generic-password -s "recovery-compass-github-token" -w
```

### 🚀 Quick Command Examples

#### Test Cloudflare Connection:
```bash
export CF_TOKEN=$(security find-generic-password -s "recovery-compass-cf-token" -w)
export CF_ZONE_ID=$(security find-generic-password -s "recovery-compass-cf-zone-id" -w)

# Get zone details
curl -X GET "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID" \
     -H "Authorization: Bearer $CF_TOKEN" \
     -H "Content-Type: application/json" | jq '.result.name'
```

#### Test GitHub Connection:
```bash
export GITHUB_TOKEN=$(security find-generic-password -s "recovery-compass-github-token" -w)

# Get user info
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | jq '.login'
```

### 📋 Environment Setup Script

Create this in your shell profile for easy access:
```bash
# Recovery Compass Credentials
alias rc-cf-token='export CF_TOKEN=$(security find-generic-password -s "recovery-compass-cf-token" -w)'
alias rc-cf-zone='export CF_ZONE_ID=$(security find-generic-password -s "recovery-compass-cf-zone-id" -w)'
alias rc-github='export GITHUB_TOKEN=$(security find-generic-password -s "recovery-compass-github-token" -w)'
alias rc-env='rc-cf-token && rc-cf-zone && rc-github && echo "✅ Recovery Compass environment loaded"'
```

### 🛡️ Security Notes

1. **Never commit these credentials to git**
2. **Credentials are encrypted in macOS Keychain**
3. **Access requires your macOS user password**
4. **Rotate tokens periodically**

### 🔄 To Update Credentials

```bash
# Update any credential (example for API token)
security add-generic-password -U -a "$USER" -s "recovery-compass-cf-token" -w "NEW_TOKEN_HERE"
```

### 🚨 Emergency Access

If keychain access fails, check:
1. Keychain Access app → login keychain
2. Search for "recovery-compass"
3. Double-click to view (requires password)

---
Credentials secured: August 1, 2025
