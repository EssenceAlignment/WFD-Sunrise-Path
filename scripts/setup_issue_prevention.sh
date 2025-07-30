#!/bin/bash

echo "🛡️ Setting up Issue Prevention System"
echo "===================================="

# 1. VS Code Settings for Auto-formatting
echo "📝 Configuring VS Code settings..."
cat > .vscode/settings.json << 'EOF'
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.markdownlint": "explicit",
    "source.fixAll.eslint": "explicit"
  },
  "[markdown]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "DavidAnson.vscode-markdownlint"
  },
  "[yaml]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "redhat.vscode-yaml"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "cSpell.enabled": true,
  "cSpell.autoFixOnSave": true,
  "yaml.schemas": {
    "https://json.schemastore.org/github-workflow.json": ".github/workflows/*.yml"
  },
  "markdownlint.config": {
    "MD013": { "line_length": 120 },
    "MD031": true,
    "MD032": true,
    "MD040": true
  }
}
EOF

# 2. EditorConfig for consistent formatting
echo "📐 Setting up EditorConfig..."
cat > .editorconfig << 'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
indent_size = 2

[*.{yml,yaml}]
indent_size = 2

[*.{js,jsx,ts,tsx}]
indent_size = 2

[Makefile]
indent_style = tab
EOF

# 3. Markdownlint configuration
echo "📋 Configuring markdownlint..."
cat > .markdownlint.json << 'EOF'
{
  "default": true,
  "MD013": {
    "line_length": 120,
    "heading_line_length": 120,
    "code_block_line_length": 120,
    "code_blocks": false,
    "tables": false,
    "headings": true,
    "headers": true,
    "strict": false,
    "stern": false
  },
  "MD031": true,
  "MD032": true,
  "MD040": true,
  "MD004": {
    "style": "dash"
  },
  "MD007": {
    "indent": 2
  },
  "MD022": true,
  "MD024": {
    "siblings_only": true
  }
}
EOF

# 4. CSpell configuration
echo "📖 Configuring spell checker..."
cat > .cspell.json << 'EOF'
{
  "version": "0.2",
  "language": "en",
  "words": [
    "autobuild",
    "biopsychosocial",
    "Likert",
    "SAVR",
    "markdownlint",
    "cspell",
    "yamllint",
    "tsconfig",
    "eslint",
    "prettier",
    "editorconfig",
    "gitignore",
    "npmrc",
    "yarnrc",
    "nvmrc"
  ],
  "ignorePaths": [
    "node_modules/**",
    "venv/**",
    ".git/**",
    "coverage/**",
    "dist/**",
    "build/**",
    "*.min.js",
    "*.min.css"
  ],
  "dictionaries": ["en_US", "typescript", "node", "npm", "html", "css", "bash"]
}
EOF

# 5. GitHub Actions for CI/CD
echo "🚀 Setting up GitHub Actions..."
mkdir -p .github/workflows

cat > .github/workflows/lint-all.yml << 'EOF'
name: Lint All Files

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Markdown Lint
      run: npx markdownlint "**/*.md" --ignore node_modules

    - name: Spell Check
      run: npx cspell "**/*.{md,yml,yaml,ts,tsx,js,jsx}" --no-progress

    - name: YAML Lint
      run: |
        pip install yamllint
        yamllint .github/workflows/

    - name: TypeScript Check
      if: ${{ hashFiles('tsconfig.json') != '' }}
      run: npx tsc --noEmit

    - name: ESLint
      if: ${{ hashFiles('.eslintrc.*') != '' }}
      run: npx eslint "**/*.{ts,tsx,js,jsx}" --ignore-pattern node_modules
EOF

# 6. Pre-commit configuration
echo "🔒 Setting up pre-commit hooks..."
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: local
    hooks:
      - id: markdownlint
        name: Markdownlint
        entry: npx markdownlint
        language: system
        files: '\.md$'
        exclude: 'node_modules|venv'

      - id: cspell
        name: Spell Check
        entry: npx cspell
        language: system
        files: '\.(md|yml|yaml|ts|tsx|js|jsx)$'
        exclude: 'node_modules|venv'

      - id: fix-yaml-booleans
        name: Fix YAML Booleans
        entry: bash -c 'find .github/workflows -name "*.yml" -exec sed -i "" "s/: \"true\"/: true/g; s/: \"false\"/: false/g" {} +'
        language: system
        files: '\.ya?ml$'
        pass_filenames: false
EOF

# 7. Install pre-commit if available
if command -v pre-commit &> /dev/null; then
  echo "Installing pre-commit hooks..."
  pre-commit install
else
  echo "pre-commit not found. Install with: pip install pre-commit"
fi

echo "✅ Issue Prevention System Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Run: chmod +x scripts/fix_all_issues.sh"
echo "2. Run: ./scripts/fix_all_issues.sh"
echo "3. Install VS Code extensions:"
echo "   - markdownlint"
echo "   - Code Spell Checker"
echo "   - YAML"
echo "   - ESLint"
echo "   - Prettier"
