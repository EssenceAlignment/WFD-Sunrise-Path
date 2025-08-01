#!/bin/bash

echo "🚀 Triggering automation for PR #2..."

# Use GitHub API directly
PR_NUMBER=2
REPO="Recovery-Compass/wfd-sunrise-path"

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
