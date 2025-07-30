# Recovery Compass Governance Propagation - Correct Commands

## For recovery-compass-grant-system (you just initialized git ✅)

```bash

# You're currently in: /Users/ericjones/Projects/recovery-compass-journeys/recovery-compass-grant-system

# Run the propagation script from the WFD-Sunrise-Path directory:

cd /Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path
./propagate_governance.sh

# The script will now process recovery-compass-grant-system since it's a git repo

```text

## Alternative: Run directly from recovery-compass-grant-system

```bash

# If you're still in recovery-compass-grant-system:

cd /Users/ericjones/Projects/recovery-compass-journeys/recovery-compass-grant-system

# Copy governance files directly:

cp /Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path/LICENSE .
cp /Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path/CODE_OF_CONDUCT.md .
rsync -a /Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path/.github/ .github/

# Commit with IPE-compliant message:

git add LICENSE CODE_OF_CONDUCT.md .github/
git commit -m "chore(governance): add MIT licence, CoC, templates, CodeQL & Dependabot" -m "Added governance framework to ensure grant compliance consistency across all Recovery Compass repositories"

# Set up remote (replace with your actual GitHub URL):

git remote add origin https://github.com/[your-username]/recovery-compass-grant-system.git
git branch -M main
git push -u origin main

```text

## For Recovery-Compass-Funding (with conflicts)

```bash
cd /Users/ericjones/recovery-compass-grants/Recovery-Compass-Funding
git merge --abort  # Clear the merge conflict

git pull origin main  # Sync with remote

cd /Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path
./propagate_governance.sh  # Re-run script

```text

## Quick Verification

```bash

# Check all repos have MIT license:

find ~/Projects -name "LICENSE" -path "*recovery-compass*" -exec head -1 {} \;
