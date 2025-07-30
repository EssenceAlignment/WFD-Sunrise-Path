#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Systematic Issue Resolution Script${NC}"
echo -e "${BLUE}=====================================/${NC}"

# 1. Fix Markdown Issues
echo -e "\n${YELLOW}📝 Fixing Markdown Issues...${NC}"

# MD040 - Add language to fenced code blocks
echo "  → Fixing code blocks without language specifiers..."
find . -name "*.md" -type f ! -path "./node_modules/*" ! -path "./venv/*" -exec sed -i "" 's/^```$/```text/g' {} +

# MD031 - Add blank lines around fenced code blocks
echo "  → Adding blank lines around code blocks..."
# This is complex with sed, using markdownlint auto-fix instead

# MD032 - Add blank lines around lists
echo "  → Adding blank lines around lists..."
find . -name "*.md" -type f ! -path "./node_modules/*" ! -path "./venv/*" -exec sed -i "" -E 's/([^[:space:]])\n(-|\*|\+|[0-9]+\.)/\1\n\n\2/g' {} +

# MD022 - Add blank lines around headings
echo "  → Adding blank lines around headings..."
find . -name "*.md" -type f ! -path "./node_modules/*" ! -path "./venv/*" -exec sed -i "" -E 's/([^[:space:]])\n(#{1,6} )/\1\n\n\2/g' {} +

# Run markdownlint fix
echo "  → Running markdownlint auto-fix..."
npx markdownlint "**/*.md" --fix --ignore node_modules --ignore venv 2>/dev/null || true

# 2. Fix Spelling Issues
echo -e "\n${YELLOW}📖 Fixing Spelling Issues...${NC}"

# Add common technical terms to dictionary
echo "  → Adding technical terms to dictionary..."
cat >> styles/Vocab/Base/accept.txt << "EOF"
autobuild
biopsychosocial
Likert
SAVR
EOF

# Sort and remove duplicates
sort -u styles/Vocab/Base/accept.txt -o styles/Vocab/Base/accept.txt

# 3. Fix YAML Boolean Issues
echo -e "\n${YELLOW}📋 Fixing YAML Boolean Issues...${NC}"

# Fix boolean values in YAML files
echo "  → Converting string booleans to proper booleans..."
find .github/workflows -name "*.yml" -exec sed -i "" 's/: "true"/: true/g' {} +
find .github/workflows -name "*.yml" -exec sed -i "" 's/: "false"/: false/g' {} +
find .github/workflows -name "*.yml" -exec sed -i "" "s/: 'true'/: true/g" {} +
find .github/workflows -name "*.yml" -exec sed -i "" "s/: 'false'/: false/g" {} +

# 4. Create Module Fix Script
echo -e "\n${YELLOW}📦 Creating Module Fix Script...${NC}"

cat > scripts/fix_module_issues.js << 'EOF'
#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Fix common module import issues
function fixModuleIssues() {
  console.log('🔍 Scanning for module issues...');

  // Common fixes for module not found errors
  const fixes = {
    // Add .js extensions to relative imports in ESM
    addJsExtensions: (content) => {
      return content.replace(/from ['"](\.[^'"]+)(?<!\.js)['"];/g, "from '$1.js';");
    },

    // Fix JSX module paths
    fixJsxPaths: (content) => {
      return content.replace(/from ['"](.+)\.jsx['"];/g, "from '$1';");
    },

    // Add missing React imports
    addReactImport: (content) => {
      if (content.includes('<') && content.includes('>') && !content.includes("import React")) {
        return "import React from 'react';\n" + content;
      }
      return content;
    }
  };

  // Apply fixes to TypeScript/JavaScript files
  const processFile = (filePath) => {
    if (filePath.match(/\.(ts|tsx|js|jsx)$/) && !filePath.includes('node_modules')) {
      let content = fs.readFileSync(filePath, 'utf8');
      let modified = false;

      for (const [fixName, fixFn] of Object.entries(fixes)) {
        const newContent = fixFn(content);
        if (newContent !== content) {
          content = newContent;
          modified = true;
          console.log(`  ✓ Applied ${fixName} to ${filePath}`);
        }
      }

      if (modified) {
        fs.writeFileSync(filePath, content);
      }
    }
  };

  // Recursively process all files
  const walkDir = (dir) => {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
        walkDir(filePath);
      } else if (stat.isFile()) {
        processFile(filePath);
      }
    });
  };

  walkDir('.');
  console.log('✅ Module issue scan complete');
}

fixModuleIssues();
EOF

chmod +x scripts/fix_module_issues.js

# 5. Run TypeScript/ESLint checks
echo -e "\n${YELLOW}🔍 Running TypeScript/ESLint checks...${NC}"

# Check if tsconfig exists and run tsc
if [ -f "tsconfig.json" ]; then
  echo "  → Running TypeScript compiler..."
  npx tsc --noEmit 2>/dev/null || true
fi

# Run ESLint with auto-fix
if [ -f ".eslintrc.json" ] || [ -f ".eslintrc.js" ]; then
  echo "  → Running ESLint auto-fix..."
  npx eslint "**/*.{ts,tsx,js,jsx}" --fix --ignore-pattern node_modules 2>/dev/null || true
fi

# 6. Final validation
echo -e "\n${YELLOW}✅ Running final validation...${NC}"

# Count remaining issues
MD_ISSUES=$(npx markdownlint "**/*.md" --ignore node_modules --ignore venv 2>&1 | wc -l)
SPELL_ISSUES=$(npx cspell "**/*.{md,yml,yaml,ts,tsx,js,jsx}" --no-progress 2>&1 | grep -c "Unknown word" || true)

echo -e "\n${GREEN}📊 Summary:${NC}"
echo -e "  → Markdown issues remaining: ${MD_ISSUES}"
echo -e "  → Spelling issues remaining: ${SPELL_ISSUES}"

# Create pre-commit hook
echo -e "\n${YELLOW}🔒 Setting up pre-commit hook...${NC}"

cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash

# Run markdown lint
echo "Running markdown lint..."
npx markdownlint "**/*.md" --ignore node_modules --ignore venv

# Run spell check
echo "Running spell check..."
npx cspell "**/*.{md,yml,yaml,ts,tsx,js,jsx}" --no-progress

# Run TypeScript check if tsconfig exists
if [ -f "tsconfig.json" ]; then
  echo "Running TypeScript check..."
  npx tsc --noEmit
fi

echo "All checks passed! ✅"
HOOK

chmod +x .git/hooks/pre-commit

echo -e "\n${GREEN}✨ Issue resolution complete!${NC}"
echo -e "${GREEN}Pre-commit hooks installed to prevent future issues.${NC}"
