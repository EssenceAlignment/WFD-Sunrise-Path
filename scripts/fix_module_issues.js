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
