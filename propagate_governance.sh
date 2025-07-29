#!/bin/bash

# Propagate governance framework to all Recovery Compass repositories
# Ensures grant reviewers see consistent IP and security controls across all codebases

echo "🚀 Recovery Compass Governance Propagation Script"
echo "================================================"

# Source repository (current directory)
SOURCE_DIR="/Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path"

# Target repositories
REPOS=(
  "/Users/ericjones/recovery-compass-grants/Recovery-Compass-Funding"
  "/Users/ericjones/Projects/recovery-compass-journeys"
)

# Additional repositories that need to be cloned or initialized
echo ""
echo "📝 Note: The following repositories exist on GitHub but need local setup:"
echo "   - recovery-compass-grant-system (Lovable project)"
echo "   To add governance to these, clone them locally first:"
echo "   git clone https://github.com/[owner]/recovery-compass-grant-system"
echo ""

# Iterate through each repository
for REPO in "${REPOS[@]}"; do
  echo ""
  echo "⏳ Processing: $REPO"
  echo "-----------------------------------"
  
  # Check if repository exists
  if [ ! -d "$REPO" ]; then
    echo "⚠️  Repository not found: $REPO"
    echo "   Skipping..."
    continue
  fi
  
  # Check if it's a git repository
  if [ ! -d "$REPO/.git" ]; then
    echo "⚠️  Not a git repository: $REPO"
    echo "   Skipping..."
    continue
  fi
  
  # Copy governance files
  echo "📄 Copying LICENSE..."
  cp "$SOURCE_DIR/LICENSE" "$REPO/LICENSE"
  
  echo "📄 Copying CODE_OF_CONDUCT.md..."
  cp "$SOURCE_DIR/CODE_OF_CONDUCT.md" "$REPO/CODE_OF_CONDUCT.md"
  
  echo "📁 Syncing .github directory..."
  mkdir -p "$REPO/.github"
  rsync -a "$SOURCE_DIR/.github/" "$REPO/.github/"
  
  # Navigate to repository and commit
  cd "$REPO"
  
  # Check if there are changes to commit
  if git diff --quiet && git diff --cached --quiet; then
    echo "✅ No changes needed - repository already has governance files"
  else
    # Add and commit changes
    git add LICENSE CODE_OF_CONDUCT.md .github/
    git commit -m "chore(governance): sync MIT licence, CoC, templates, CodeQL & Dependabot" -m "Propagated from WFD-Sunrise-Path to ensure grant compliance consistency across all Recovery Compass repositories"
    
    # Get the current branch name
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    
    echo "🔄 Pushing to origin/$CURRENT_BRANCH..."
    if git push origin "$CURRENT_BRANCH"; then
      echo "✅ Successfully updated $REPO"
    else
      echo "❌ Failed to push to $REPO"
      echo "   You may need to push manually or check permissions"
    fi
  fi
done

echo ""
echo "🎉 Governance propagation complete!"
echo ""
echo "📋 Next steps (manual - one click each):"
echo "1. Enable Dependabot alerts: Settings → Code security"
echo "2. Set branch protection: require CodeQL + Dependabot checks"
echo "3. Install CLA Assistant (optional): GitHub Marketplace"
echo ""
echo "🔍 Verification commands:"
echo "gh repo list --json name,licenseInfo"
echo "gh api repos/{owner}/{repo}/dependabot/alerts"
