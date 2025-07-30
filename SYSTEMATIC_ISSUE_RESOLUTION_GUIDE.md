# Systematic Issue Resolution Guide

## Overview

This guide demonstrates how I systematically approach and resolve common development issues to prevent them from recurring.

## Issue Types & Resolution Strategies

### 1. Markdown Formatting Issues (e.g., 'blanks-around-lists')

**Detection:**
```bash
# Run markdownlint to find all issues
npx markdownlint "**/*.md" --config .markdownlint.json
```

**Common Issues & Fixes:**

#### MD032 - Blanks around lists
```markdown
# ❌ Incorrect
Some text
- List item

# ✅ Correct
Some text

- List item
```

#### MD040 - Fenced code blocks should have language
```markdown
# ❌ Incorrect
```
code here
```

# ✅ Correct
```bash
code here
```
```

**Automated Fix:**
```bash
# Auto-fix markdown issues
npx markdownlint "**/*.md" --fix
```

### 2. Spelling Issues (e.g., 'autobuild: unknown word')

**Detection:**
```bash
# Check spelling
npx cspell "**/*.{md,yml,yaml,ts,tsx,js,jsx}"
```

**Resolution Strategies:**

#### Add to Dictionary (for valid technical terms)
```bash
# Add to accepted words
echo "autobuild" >> styles/Vocab/Base/accept.txt
echo "biopsychosocial" >> styles/Vocab/Base/accept.txt
```

#### Fix Typos
```bash
# Find and replace typos
find . -type f -name "*.md" -exec sed -i '' 's/receive/receive/g' {} +
```

### 3. YAML Schema Issues (e.g., 'incorrect type: Expected Boolean')

**Detection:**
```bash
# Validate YAML files
yamllint .github/workflows/*.yml
```

**Common Issues & Fixes:**

#### Boolean Type Errors
```yaml
# ❌ Incorrect
uses-feature: "true"  # String instead of boolean

# ✅ Correct
uses-feature: true    # Boolean value
```

#### Proper YAML Structure
```yaml
# ❌ Incorrect
on: [push,pull_request]  # Missing space

# ✅ Correct
on: [push, pull_request]  # Proper spacing
```

### 4. TypeScript/JavaScript Issues

**Detection:**
```bash
# Run TypeScript compiler
npx tsc --noEmit

# Run ESLint
npx eslint "**/*.{ts,tsx,js,jsx}"
```

**Common Fixes:**

#### Missing Dependencies
```bash
# Install missing types
npm install --save-dev @types/react @types/node
```

#### Import Issues
```typescript
// ❌ Incorrect
import React from 'react'  // Missing semicolon

// ✅ Correct
import React from 'react';
```

## Systematic Approach Workflow

### 1. Pre-commit Checks

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: local
    hooks:
      - id: markdownlint
        name: Markdownlint
        entry: npx markdownlint
        language: system
        files: '\.md$'

      - id: cspell
        name: Spell Check
        entry: npx cspell
        language: system
        files: '\.(md|yml|yaml|ts|tsx|js|jsx)$'

      - id: yamllint
        name: YAML Lint
        entry: yamllint
        language: system
        files: '\.(yml|yaml)$'
```

### 2. Automated Fix Script

Create `scripts/fix-all-issues.sh`:
```bash
#!/bin/bash

echo "🔧 Fixing common issues systematically..."

# Fix markdown issues
echo "📝 Fixing markdown formatting..."
npx markdownlint "**/*.md" --fix

# Add blank lines around lists
find . -name "*.md" -type f -exec sed -i '' 's/\([^[:space:]]\)\n\(-\|\*\|+\|[0-9]\+\.\)/\1\n\n\2/g' {} +

# Fix code block languages
find . -name "*.md" -type f -exec sed -i '' 's/^```$/```text/g' {} +

# Fix YAML boolean values
echo "📋 Fixing YAML issues..."
find .github/workflows -name "*.yml" -exec sed -i '' 's/: "true"/: true/g' {} +
find .github/workflows -name "*.yml" -exec sed -i '' 's/: "false"/: false/g' {} +

# Update spell check dictionary
echo "📖 Updating spell check dictionary..."
sort -u styles/Vocab/Base/accept.txt -o styles/Vocab/Base/accept.txt

echo "✅ Fixes applied!"
```

### 3. CI/CD Integration

Add to `.github/workflows/lint.yml`:
```yaml
name: Lint All Files

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Markdown Lint
        run: npx markdownlint "**/*.md"

      - name: Spell Check
        run: npx cspell "**/*.{md,yml,yaml,ts,tsx,js,jsx}"

      - name: YAML Lint
        run: yamllint .github/workflows/
```

## Prevention Strategies

### 1. Editor Configuration

`.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.markdownlint": true
  },
  "cSpell.enabled": true,
  "yaml.schemas": {
    "https://json.schemastore.org/github-workflow.json": ".github/workflows/*.yml"
  }
}
```

### 2. Documentation Standards

- Always add blank lines before and after lists
- Always specify language in code blocks
- Use boolean values (not strings) in YAML
- Add technical terms to dictionary immediately

### 3. Regular Maintenance

```bash
# Weekly maintenance script
#!/bin/bash

# Update dependencies
npm update

# Run all linters
npm run lint:all

# Update spell check dictionary
npx cspell --words-only "**/*.md" | sort -u >> styles/Vocab/Base/accept.txt

# Clean up duplicates
sort -u styles/Vocab/Base/accept.txt -o styles/Vocab/Base/accept.txt
```

## Error Resolution Flowchart

```
Error Detected
    ↓
Is it a known pattern?
    ├─ Yes → Apply standard fix
    └─ No → Document new pattern
              ↓
         Add to this guide
              ↓
         Create automated fix
              ↓
         Add to pre-commit hooks
```

## Commitment Message Standards

When fixing these issues:
```bash
# Markdown fixes
git commit -m "fix(docs): resolve markdown formatting issues - add blank lines around lists"

# Spelling fixes
git commit -m "fix(spelling): add technical terms to dictionary"

# YAML fixes
git commit -m "fix(ci): correct boolean types in workflow files"

# Multiple fixes
git commit -m "fix: resolve linting issues across codebase

- Add blank lines around markdown lists
- Fix YAML boolean type errors
- Add technical terms to spell check dictionary"
```

---

By following this systematic approach, common issues are:
1. **Detected early** through pre-commit hooks
2. **Fixed automatically** where possible
3. **Prevented** through proper configuration
4. **Documented** for future reference
