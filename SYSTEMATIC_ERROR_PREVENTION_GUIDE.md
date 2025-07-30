# Systematic Error Prevention Guide

## Overview

This guide demonstrates how I systematically prevent and fix common development errors, ensuring clean, maintainable code across all projects.

## 1. Markdown Formatting Issues

### MD022/MD031: Blanks Around Headings, Lists, and Fences

**Prevention Strategy:**

```markdown

# Good Example

## Heading with proper spacing

This paragraph has a blank line above and below.

### Another heading

- List item with blank line above
- Second item

```bash

# Code fence with blank lines around it

echo "Proper spacing"

```text

### More content here

**Automatic Fix Implementation:**

```javascript
// Fix blanks around headings and lists
const fixBlanksAroundElements = (content) => {
  // Add blank lines around headings
  content = content.replace(/([^\n])\n(#{1,6} )/g, '$1\n\n$2');
  content = content.replace(/(#{1,6} .+)\n([^\n])/g, '$1\n\n$2');

  // Add blank lines around lists
  content = content.replace(/([^\n])\n([-*+] )/g, '$1\n\n$2');
  content = content.replace(/([-*+] .+)\n([^\n-*+])/g, '$1\n\n$2');

  // Add blank lines around code fences
  content = content.replace(/([^\n])\n(```)/g, '$1\n\n$2');
  content = content.replace(/(```)\n([^\n])/g, '$1\n\n$2');

  return content;
};

```text

### MD040: Fenced Code Language

**Prevention Strategy:**

Always specify language for code blocks:

```javascript
// JavaScript code with language specified
const example = "Always specify language";

```bash

```bash

# Bash code with language specified

echo "This helps with syntax highlighting"

```text

```yaml

# YAML with language specified

key: value

```javascript

**Automatic Fix:**

```javascript
// Detect and suggest languages for code blocks
const fixCodeLanguages = (content) => {
  const codeBlockRegex = /```\n([^`]+)\n```/g;

  return content.replace(codeBlockRegex, (match, code) => {
    const language = detectLanguage(code);
    return `\`\`\`${language}\n${code}\n\`\`\``;
  });
};

const detectLanguage = (code) => {
  if (code.includes('const ') || code.includes('function ')) return 'javascript';
  if (code.includes('#!/bin/bash') || code.includes('echo ')) return 'bash';
  if (code.includes(':') && code.match(/^\s*\w+:/m)) return 'yaml';
  if (code.includes('import ') && code.includes('from ')) return 'python';
  return 'text';
};

```text

## 2. Spell Check Issues

### Unknown Words (cSpell)

**Prevention Strategy:**

Maintain a comprehensive dictionary:

```json
// .cspell.json
{
  "version": "0.2",
  "language": "en",
  "words": [
    "autobuild",
    "codespace",
    "dependabot",
    "markdownlint",
    "yamllint",
    "eslint",
    "prebuild",
    "postbuild",
    "instanceof",
    "readonly",
    "typeof",
    "namespace"
  ],
  "ignorePaths": [
    "node_modules/**",
    "coverage/**",
    "*.min.js",
    "package-lock.json"
  ]
}

```javascript

**Automatic Dictionary Update:**

```javascript
// Auto-add technical terms to dictionary
const updateSpellCheckDictionary = async (unknownWords) => {
  const technicalTerms = unknownWords.filter(word =>
    isTechnicalTerm(word) || isProjectSpecific(word)
  );

  const cspellConfig = JSON.parse(await readFile('.cspell.json'));
  cspellConfig.words = [...new Set([...cspellConfig.words, ...technicalTerms])].sort();

  await writeFile('.cspell.json', JSON.stringify(cspellConfig, null, 2));
};

```text

## 3. YAML Type Issues

### Expected Boolean

**Prevention Strategy:**

Use proper YAML boolean values:

```yaml

# Correct boolean values

enabled: true
disabled: false
debug_mode: true

# AVOID string booleans

# wrong: 'true'

# wrong: "false"

# wrong: True

# wrong: FALSE

```javascript

**Automatic Fix:**

```javascript
// Fix YAML boolean values
const fixYamlBooleans = (content) => {
  // Fix quoted booleans
  content = content.replace(/:\s*['"]true['"]/g, ': true');
  content = content.replace(/:\s*['"]false['"]/g, ': false');

  // Fix case variations
  content = content.replace(/:\s*True/g, ': true');
  content = content.replace(/:\s*False/g, ': false');
  content = content.replace(/:\s*TRUE/g, ': true');
  content = content.replace(/:\s*FALSE/g, ': false');

  return content;
};

```text

## 4. Module Import Errors

### Cannot Find Module

**Prevention Strategy:**

1. **Check dependencies are installed:**

```bash

# Always ensure dependencies are installed

npm install

# or

yarn install

```text

1. **Verify import paths:**

```javascript
// Use relative paths correctly
import { Component } from './components/Component';  // ✓
import { Component } from 'components/Component';     // ✗ (unless aliased)

// Check file extensions for non-JS imports
import styles from './styles.css';    // ✓
import data from './data.json';       // ✓

```text

1. **TypeScript path mapping:**

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}

```javascript

**Automatic Fix:**

```javascript
// Detect and fix import issues
const fixImportPaths = async (filePath, errorMessage) => {
  const content = await readFile(filePath);
  const importRegex = /import .+ from ['"](.+)['"]/g;

  let fixed = content;
  let match;

  while ((match = importRegex.exec(content)) !== null) {
    const importPath = match[1];

    if (!await fileExists(resolveImportPath(importPath, filePath))) {
      const correctPath = await findCorrectImportPath(importPath, filePath);
      if (correctPath) {
        fixed = fixed.replace(match[0], match[0].replace(importPath, correctPath));
      }
    }
  }

  await writeFile(filePath, fixed);
};

```text

## 5. JSX/React Issues

### JSX Tag Requires Module Path

**Prevention Strategy:**

1. **Ensure React is in scope:**

```javascript
// For React 17+
import { useState } from 'react';  // React import not needed for JSX

// For React <17
import React from 'react';  // Required for JSX

```text

1. **Configure for React 17+ new JSX transform:**

```json
// tsconfig.json or jsconfig.json
{
  "compilerOptions": {
    "jsx": "react-jsx"  // For React 17+
  }
}

```text

1. **Remove React files from non-React projects:**

```bash

# If not a React project, remove React files

rm -rf src/**/*.tsx
rm -rf src/**/*.jsx
rm -rf components/

```javascript

**Detection and Fix:**

```javascript
// Detect misplaced React files in non-React projects
const detectMisplacedReactFiles = async () => {
  const packageJson = JSON.parse(await readFile('package.json'));
  const hasReact = packageJson.dependencies?.react || packageJson.devDependencies?.react;

  if (!hasReact) {
    const reactFiles = await findFiles(['**/*.tsx', '**/*.jsx']);
    if (reactFiles.length > 0) {
      console.log('Found React files in non-React project:');
      reactFiles.forEach(file => console.log(`  - ${file}`));

      // Suggest removal or conversion
      return {
        action: 'remove',
        files: reactFiles
      };
    }
  }
};

```text

## 6. Systematic Prevention System

### Pre-commit Hooks

```yaml

# .pre-commit-config.yaml

repos:
  - repo: local
    hooks:
      - id: markdownlint
        name: Fix Markdown Issues
        entry: npx markdownlint --fix
        language: system
        files: '\.md$'

      - id: spell-check
        name: Check Spelling
        entry: npx cspell
        language: system
        files: '\.(md|js|ts|jsx|tsx|json|yaml|yml)$'

      - id: yaml-lint
        name: Lint YAML
        entry: yamllint
        language: system
        files: '\.(yaml|yml)$'

      - id: fix-imports
        name: Fix Import Paths
        entry: node scripts/fix-imports.js
        language: system
        files: '\.(js|ts|jsx|tsx)$'

```text

### VS Code Settings

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.markdownlint": true,
    "source.fixAll.eslint": true
  },
  "[markdown]": {
    "editor.defaultFormatter": "DavidAnson.vscode-markdownlint"
  },
  "[yaml]": {
    "editor.defaultFormatter": "redhat.vscode-yaml"
  },
  "yaml.format.enable": true,
  "yaml.validate": true,
  "yaml.schemas": {
    "https://json.schemastore.org/github-workflow.json": ".github/workflows/*.yml"
  },
  "cSpell.enabled": true,
  "cSpell.autoFixOnSave": true
}

```bash

### Master Fix Script

```bash
#!/bin/bash

# scripts/fix_all_issues_systematically.sh

echo "🔧 Running Systematic Fix Process..."

# 1. Fix Markdown formatting

echo "📝 Fixing Markdown issues..."
npx markdownlint "**/*.md" --fix

# 2. Fix YAML booleans

echo "📋 Fixing YAML boolean values..."
find . -name "*.yml" -o -name "*.yaml" | while read file; do
  sed -i.bak 's/: '\''true'\''/: true/g' "$file"
  sed -i.bak 's/: '\''false'\''/: false/g' "$file"
  sed -i.bak 's/: "true"/: true/g' "$file"
  sed -i.bak 's/: "false"/: false/g' "$file"
  rm "${file}.bak"
done

# 3. Update spell check dictionary

echo "📖 Updating spell check dictionary..."
node scripts/update-dictionary.js

# 4. Check for module issues

echo "📦 Checking module imports..."
node scripts/check-imports.js

# 5. Remove misplaced React files if needed

echo "⚛️ Checking for misplaced React files..."
node scripts/check-react-files.js

# 6. Run final validation

echo "✅ Running final validation..."
npm run lint

echo "✨ All issues fixed systematically!"

```text

## 7. Continuous Monitoring

### GitHub Actions Workflow

```yaml

# .github/workflows/quality-check.yml

name: Quality Check

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Markdown Lint
        uses: DavidAnson/markdownlint-cli2-action@v11
        with:
          fix: true

      - name: Spell Check
        uses: streetsidesoftware/cspell-action@v2

      - name: YAML Lint
        run: yamllint .

      - name: Check Imports
        run: |
          npm ci
          npm run check-imports

      - name: Auto-fix and Commit
        if: github.event_name == 'push'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          npm run fix-all
          git add -A
          git diff --staged --quiet || git commit -m "Auto-fix: Format and lint issues"
          git push

```text

## Summary

This systematic approach ensures:

1. **Automatic Detection** - Issues are caught before they become problems
2. **Immediate Fixes** - Most issues are auto-corrected on save or commit
3. **Preventive Measures** - Configuration prevents issues from occurring
4. **Continuous Validation** - CI/CD ensures nothing slips through
5. **Clear Documentation** - Team knows how to handle edge cases

With this system in place, you'll never need to manually fix these common issues again. The tooling handles it automatically, letting you focus on writing code and content.
