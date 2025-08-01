#!/bin/bash

# Setup Recovery Compass PR Automation System

set -e

echo "🚀 Setting up Recovery Compass PR Automation..."

# Check for required environment variables
if [ -z "$GITHUB_TOKEN" ] && [ -z "$GH_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN or GH_TOKEN must be set"
    echo "Please run: export GITHUB_TOKEN=your_github_token"
    exit 1
fi

# Ensure we're in the project root
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

# Install required npm packages
echo "📦 Installing npm dependencies..."
npm install --save-dev @octokit/rest

# Create automation directory structure
echo "📁 Creating automation directories..."
mkdir -p .github/workflows
mkdir -p scripts/automation
mkdir -p logs/automation

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x scripts/pr-optimization-bot.js
chmod +x scripts/setup-pr-automation.sh

# Configure GitHub repository settings
echo "⚙️ Configuring repository settings..."
if command -v gh &> /dev/null; then
    # Enable auto-merge for the repository
    gh repo edit --enable-auto-merge || echo "⚠️ Could not enable auto-merge (may require admin permissions)"

    # Create labels for automation
    gh label create "auto-split" --description "PR created by automation" --color "0052CC" || true
    gh label create "parent-pr" --description "Original PR that was split" --color "5319E7" || true
    gh label create "automation-ready" --description "Ready for automated processing" --color "0E8A16" || true
else
    echo "⚠️ GitHub CLI not installed. Please install 'gh' for full automation features"
fi

# Create automation configuration
echo "📝 Creating automation configuration..."
cat > .github/pr-automation-config.json << 'EOF'
{
  "enabled": true,
  "autoSplitThresholds": {
    "commits": 50,
    "additions": 10000,
    "files": 100
  },
  "splitStrategy": {
    "security": ["**/.env*", "**/*secret*", ".gitignore", "SECURITY*.md"],
    "docker": ["**/docker*", "**/Dockerfile*", "docker-compose*.yml"],
    "ci-cd": [".github/workflows/*", "**/*ci*", "**/*cd*"],
    "monitoring": ["**/monitor*", "**/grafana*", "**/loki*"],
    "docs": ["**/*.md", "docs/**"],
    "scripts": ["scripts/**", "**/*.sh"],
    "config": ["**/*.json", "**/*.yaml", "**/*.yml"]
  },
  "korbitIntegration": true,
  "autoConflictResolution": true
}
EOF

# Create PR-specific automation trigger
echo "🎯 Creating PR #2 specific automation..."
cat > .github/workflows/pr-2-automation.yml << 'EOF'
name: PR #2 Automation

on:
  issue_comment:
    types: [created]
  workflow_dispatch:

jobs:
  trigger-automation:
    if: |
      (github.event.issue.pull_request && github.event.issue.number == 2) ||
      github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Trigger Korbit AI
        uses: actions/github-script@v7
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: 2,
              body: '/korbit-generate-pr-description'
            });

      - name: Post Optimization Feedback
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          node scripts/post-optimization-feedback.js 2
EOF

# Create the feedback posting script
echo "💬 Creating optimization feedback script..."
cat > scripts/post-optimization-feedback.js << 'EOF'
const { Octokit } = require("@octokit/rest");
const PROptimizationBot = require("./pr-optimization-bot");

async function postOptimizationFeedback(prNumber) {
  const octokit = new Octokit({
    auth: process.env.GITHUB_TOKEN || process.env.GH_TOKEN,
  });

  const bot = new PROptimizationBot();
  const report = await bot.generateOptimizationReport(prNumber);

  const feedback = `## 🚀 Automated PR Optimization Analysis

### PR Health Score: ${report.automationScore}%

### Summary
- 📊 **Commits**: ${report.summary.commits}
- ➕ **Additions**: ${report.summary.additions.toLocaleString()}
- ➖ **Deletions**: ${report.summary.deletions.toLocaleString()}
- 📁 **Files Changed**: ${report.summary.changedFiles}

### Issues Detected
${report.issues.length === 0 ? '✅ No issues detected!' : report.issues.map(issue =>
  `- **${issue.severity.toUpperCase()}**: ${issue.message}\n  - 💡 ${issue.recommendation}`
).join('\n')}

### Automated Actions
1. ✅ Triggered Korbit AI description regeneration
2. ${report.automationScore < 70 ? '✅ Initiating automatic PR split...' : '⏭️ PR size is manageable, skipping split'}
3. ${report.issues.some(i => i.type === 'potential_secret') ? '🔒 Security scan initiated' : '✅ No security issues detected'}

### Recommendations
${report.recommendations.map(rec =>
  `- **${rec.priority.toUpperCase()}**: ${rec.action}\n  - Reason: ${rec.reason}`
).join('\n')}

### Next Steps
${report.automationScore < 70 ?
`This PR will be automatically split into smaller, reviewable chunks. Watch for new PRs with the \`auto-split\` label.` :
`This PR is ready for review. Consider enabling auto-merge once all checks pass.`}

---
*Generated by Recovery Compass Force Multiplication System at ${new Date().toISOString()}*
*Automation Score: ${report.automationScore}% | Run \`npm run pr:optimize ${prNumber}\` for manual control*`;

  await octokit.issues.createComment({
    owner: process.env.GITHUB_REPOSITORY_OWNER || 'EssenceAlignment',
    repo: process.env.GITHUB_REPOSITORY?.split('/')[1] || 'WFD-Sunrise-Path',
    issue_number: prNumber,
    body: feedback
  });

  // If score is low, trigger the split
  if (report.automationScore < 70) {
    console.log('Triggering automatic PR split...');
    const splitPRs = await bot.autoSplitPR(prNumber);

    if (splitPRs.length > 0) {
      const splitComment = `## 🎯 PR Successfully Split!

Created ${splitPRs.length} targeted PRs:
${splitPRs.map(pr => `- #${pr.number}: ${pr.type} (${pr.commits} commits)`).join('\n')}

Please review and merge these PRs in order.`;

      await octokit.issues.createComment({
        owner: process.env.GITHUB_REPOSITORY_OWNER || 'EssenceAlignment',
        repo: process.env.GITHUB_REPOSITORY?.split('/')[1] || 'WFD-Sunrise-Path',
        issue_number: prNumber,
        body: splitComment
      });
    }
  }
}

// Run if called directly
if (require.main === module) {
  const prNumber = parseInt(process.argv[2]);
  if (!prNumber) {
    console.error('Usage: node post-optimization-feedback.js <pr-number>');
    process.exit(1);
  }

  postOptimizationFeedback(prNumber)
    .then(() => console.log('✅ Optimization feedback posted'))
    .catch(err => {
      console.error('❌ Error:', err.message);
      process.exit(1);
    });
}

module.exports = { postOptimizationFeedback };
EOF

chmod +x scripts/post-optimization-feedback.js

# Add npm scripts
echo "📝 Adding npm scripts..."
if [ -f "package.json" ]; then
    # Check if scripts section exists
    if ! grep -q '"scripts"' package.json; then
        # Add scripts section using Node.js
        node -e "
        const fs = require('fs');
        const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
        pkg.scripts = pkg.scripts || {};
        pkg.scripts['pr:analyze'] = 'node scripts/pr-optimization-bot.js analyze';
        pkg.scripts['pr:split'] = 'node scripts/pr-optimization-bot.js split';
        pkg.scripts['pr:report'] = 'node scripts/pr-optimization-bot.js report';
        pkg.scripts['pr:optimize'] = 'node scripts/post-optimization-feedback.js';
        fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
        "
    else
        echo "⚠️ Please manually add the following npm scripts to package.json:"
        echo '  "pr:analyze": "node scripts/pr-optimization-bot.js analyze"'
        echo '  "pr:split": "node scripts/pr-optimization-bot.js split"'
        echo '  "pr:report": "node scripts/pr-optimization-bot.js report"'
        echo '  "pr:optimize": "node scripts/post-optimization-feedback.js"'
    fi
fi

# Create a quick automation trigger for PR #2
echo "🎯 Creating immediate PR #2 automation trigger..."
cat > scripts/trigger-pr2-automation.sh << 'EOF'
#!/bin/bash

echo "🚀 Triggering automation for PR #2..."

# Use GitHub API directly
PR_NUMBER=2
REPO="EssenceAlignment/WFD-Sunrise-Path"

# Trigger workflow
if command -v gh &> /dev/null; then
    gh workflow run pr-2-automation.yml --repo $REPO
else
    echo "Triggering via API..."
    curl -X POST \
      -H "Accept: application/vnd.github.v3+json" \
      -H "Authorization: token ${GITHUB_TOKEN:-$GH_TOKEN}" \
      https://api.github.com/repos/$REPO/actions/workflows/pr-2-automation.yml/dispatches \
      -d '{"ref":"main"}'
fi

echo "✅ Automation triggered! Check PR #2 for updates."
EOF

chmod +x scripts/trigger-pr2-automation.sh

echo "
✅ PR Automation Setup Complete!

🎯 To immediately optimize PR #2, run:
   ./scripts/trigger-pr2-automation.sh

📊 Available commands:
   npm run pr:analyze <pr-number>  - Analyze a PR
   npm run pr:split <pr-number>    - Split a large PR
   npm run pr:report <pr-number>   - Generate optimization report
   npm run pr:optimize <pr-number> - Post optimization feedback

🤖 Automation will now:
   1. Automatically detect large PRs
   2. Trigger Korbit AI descriptions
   3. Split PRs intelligently
   4. Resolve conflicts automatically
   5. Post optimization feedback

📝 Configuration: .github/pr-automation-config.json
📁 Workflows: .github/workflows/
"
