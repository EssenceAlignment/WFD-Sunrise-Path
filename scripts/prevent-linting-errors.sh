#!/bin/bash
# scripts/prevent-linting-errors.sh

echo "🛡️ Running Systematic Linting Error Prevention..."

# 1. Validate and fix .markdownlint.json
echo "📋 Checking .markdownlint.json configuration..."
if [ -f .markdownlint.json ]; then
  node -e "
  const { validateMarkdownlintConfig, autoFixMarkdownlintConfig } = require('./scripts/validate-json-configs.js');
  const errors = validateMarkdownlintConfig('.markdownlint.json');
  if (errors.length > 0) {
    console.log('Found configuration errors:', errors);
    console.log('Auto-fixing...');
    autoFixMarkdownlintConfig('.markdownlint.json');
    console.log('✅ Fixed!');
  } else {
    console.log('✅ Configuration is valid!');
  }
  "
fi

# 2. Fix all markdown files
echo "📝 Checking and fixing all markdown files..."
find . -name "*.md" -not -path "./node_modules/*" -not -path "./venv/*" -not -path "./qualtrics-api-project/rapid-deploy/node_modules/*" | while IFS= read -r file; do
  echo "Checking: $file"

  # Run validator
  node -e "
  const { MarkdownValidator, autoFixMarkdown } = require('./scripts/validate-before-save.js');
  const validator = new MarkdownValidator();
  const errors = validator.validateMarkdownFile('$file');

  if (errors.length > 0) {
    console.log('Found errors:', errors);
    console.log('Auto-fixing...');
    autoFixMarkdown('$file');
    console.log('✅ Fixed!');
  }
  "
done

# 3. Run markdownlint to verify
echo "🔍 Running final validation..."
npx markdownlint "**/*.md" --fix --ignore node_modules --ignore venv

echo "✨ All linting issues prevented and fixed!"
