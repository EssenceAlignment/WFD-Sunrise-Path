# GitHub Security Features Setup Guide

## For Each Recovery Compass Repository

### 1. Navigate to Security Settings

For each repository:
- `https://github.com/Recovery-Compass/recovery-compass-grant-system/settings/security_analysis`
- `https://github.com/EssenceAlignment/WFD-Sunrise-Path/settings/security_analysis`
- `https://github.com/[owner]/recovery-compass-journeys/settings/security_analysis`
- `https://github.com/Recovery-Compass/Recovery-Compass-Funding/settings/security_analysis`

### 2. Enable These Security Features (Exact Steps)

Once on the Security & analysis page, you'll see toggles. Enable these:

#### **Dependabot alerts** 
- Find: "Dependabot alerts"
- Click: **Enable** button
- What it does: Notifies you of vulnerable dependencies

#### **Dependabot security updates**
- Find: "Dependabot security updates" 
- Click: **Enable** button
- What it does: Automatically creates PRs to update vulnerable dependencies

#### **Secret scanning**
- Find: "Secret scanning"
- Click: **Enable** button
- What it does: Scans for accidentally committed API keys/passwords

#### **Secret scanning push protection** (if available)
- Find: "Push protection"
- Click: **Enable** button
- What it does: Blocks commits containing secrets

### 3. Verify CodeQL is Active

Since we added `.github/workflows/security.yml`, CodeQL should automatically run on:
- Every push to main branch
- Every pull request
- Weekly schedule (Sundays)

To verify:
1. Go to repository → **Actions** tab
2. Look for "CodeQL Analysis" workflow
3. If not visible, go to `.github/workflows/security.yml` and click "Run workflow"

### 4. Set Up Security Policy (Optional but Recommended)

From the Security tab you showed:
1. Click **"Set up a security policy"**
2. This creates `SECURITY.md` with template:

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report vulnerabilities to: security@recovery-compass.org

We will respond within 48 hours and work on a fix.
```

### 5. Branch Protection Rules (For Main Branch)

Navigate to: Settings → Branches → Add rule

1. **Branch name pattern**: `main`
2. Check these boxes:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - Under "Status checks", search and add:
     - `CodeQL`
     - `Dependabot`
3. Click **Create** or **Save changes**

### 6. Quick Verification Commands

After enabling, verify with:

```bash
# Check Dependabot alerts (should return [] if no vulnerabilities)
gh api repos/Recovery-Compass/recovery-compass-grant-system/dependabot/alerts

# Check secret scanning alerts
gh api repos/Recovery-Compass/recovery-compass-grant-system/secret-scanning/alerts

# List security features status
gh api repos/Recovery-Compass/recovery-compass-grant-system \
  --jq '.security_and_analysis'
```

## Time Required

- Per repository: ~2 minutes
- All 4 repositories: ~8 minutes total

These one-click toggles activate GitHub's security infrastructure, making your repositories grant-ready with professional security practices.
