# GitHub Security Features Setup Guide

## For Each Recovery Compass Repository

### 1. Navigate to Security Settings

For each repository:

- `https://github.com/Recovery-Compass/recovery-compass-grant-system/settings/security_analysis`
- `https://github.com/EssenceAlignment/WFD-Sunrise-Path/settings/security_analysis`
- `https://github.com/[owner]/recovery-compass-journeys/settings/security_analysis`
- `https://github.com/Recovery-Compass/Recovery-Compass-Funding/settings/security_analysis`

### 2. Enable These Security Features (Based on Your Advanced Security Page)

You're in the Advanced Security settings. Enable these features:

#### **Secret Protection Section**

1. **Push protection**
   - Find: "Push protection" under Secret Protection
   - Toggle: **ON**
   - What it does: Blocks commits that contain supported secrets

2. **Validity checks** (Optional but recommended)
   - Find: "Validity checks"
   - Toggle: **ON**
   - What it does: Automatically verifies if a secret is valid

3. **Non-provider patterns** (Optional)
   - Find: "Non-provider patterns"
   - Toggle: **ON**
   - What it does: Scans for non-provider patterns

4. **Scan for generic passwords** (Optional)
   - Find: "Scan for generic passwords"
   - Toggle: **ON**
   - What it does: Copilot Secret Scanning detects passwords using AI

#### **Code Security Section**

1. **Dependency graph**
   - Find: "Dependency graph"
   - Toggle: **ON**
   - What it does: Understand your dependencies

2. **Dependabot alerts**
   - Find: "Dependabot alerts" under Dependabot section
   - Toggle: **ON**
   - What it does: Receive alerts for vulnerabilities

3. **Dependabot security updates**
   - Find: "Dependabot security updates"
   - Toggle: **ON**
   - What it does: Automatically opens PRs to fix vulnerabilities

4. **Grouped security updates** (Optional but helpful)
   - Find: "Grouped security updates"
   - Toggle: **ON**
   - What it does: Groups updates into fewer PRs

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

## Priority Features for Grant Applications

**Essential (Enable These First):**

1. **Push protection** - Prevents accidental secret commits
2. **Dependency graph** - Shows your dependencies
3. **Dependabot alerts** - Critical for security compliance
4. **Dependabot security updates** - Auto-fixes vulnerabilities

**Nice to Have:**

- Validity checks
- Grouped security updates
- Scan for generic passwords (AI-powered)

## Time Required

- Per repository: ~2 minutes
- All 4 repositories: ~8 minutes total

These toggles activate GitHub's Advanced Security infrastructure, demonstrating to grant reviewers that Recovery Compass uses enterprise-grade security practices.
