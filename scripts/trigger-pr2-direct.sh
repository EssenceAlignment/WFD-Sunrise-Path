#!/bin/bash

echo "🚀 Direct PR #2 Automation Trigger"

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ] && [ -z "$GH_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN or GH_TOKEN must be set"
    exit 1
fi

TOKEN="${GITHUB_TOKEN:-$GH_TOKEN}"

# Direct API call to trigger Korbit AI
echo "📝 Triggering Korbit AI description regeneration..."
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/Recovery-Compass/wfd-sunrise-path/issues/2/comments \
  -d '{"body": "/korbit-generate-pr-description"}'

echo ""
echo "⏳ Waiting for Korbit AI to process..."
sleep 5

# Post optimization analysis
echo "📊 Posting optimization analysis..."
ANALYSIS_BODY=$(cat << 'EOF'
## 🚀 Automated PR Optimization Analysis

This PR has been flagged for automated optimization due to:
- **108 commits** (threshold: 50)
- **2,030,877 additions** (threshold: 10,000)
- **5,000+ files changed** (threshold: 100)

### Recommended Split Strategy

Based on the commit analysis, this PR should be split into the following focused PRs:

1. **🔒 Security Foundation**
   - `.gitignore` updates
   - Secret management files
   - Security documentation

2. **🏗️ Docker Infrastructure**
   - Docker configurations
   - docker-compose files
   - Container optimizations

3. **🔄 CI/CD Pipelines**
   - GitHub Actions workflows
   - Pipeline configurations
   - Automation scripts

4. **📊 Monitoring Stack**
   - Grafana/Loki setup
   - Monitoring configurations
   - Health check scripts

5. **📚 Documentation Updates**
   - All markdown files
   - Setup guides
   - Architecture docs

6. **🔧 Scripts & Automation**
   - Shell scripts
   - Python scripts
   - Automation tools

7. **⚙️ Configuration Files**
   - JSON/YAML configs
   - Environment templates
   - Settings files

### Conflict Resolution

The `.gitignore` conflict can be resolved by:
```bash
git checkout --ours .gitignore
git checkout --theirs .gitignore >> .gitignore.tmp
cat .gitignore .gitignore.tmp | sort | uniq > .gitignore
git add .gitignore
```

### Next Steps

1. Review the Korbit AI updated description
2. Consider splitting this PR using the strategy above
3. Each split PR should be <500 lines for easy review
4. Resolve conflicts before proceeding

---
*Automated by Recovery Compass PR Optimization System*
EOF
)

# Escape the body for JSON
ESCAPED_BODY=$(echo "$ANALYSIS_BODY" | jq -Rs .)

curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/Recovery-Compass/wfd-sunrise-path/issues/2/comments \
  -d "{\"body\": $ESCAPED_BODY}"

echo ""
echo "✅ Automation complete! Check PR #2 for updates."
echo ""
echo "📋 Manual follow-up actions:"
echo "1. Check if Korbit AI has updated the description"
echo "2. Review the optimization analysis"
echo "3. Decide whether to split the PR"
echo "4. Use 'npm run pr:split 2' to automatically split if desired"
