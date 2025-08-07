#!/usr/bin/env node

/**
 * ES Module Migration Script
 * Helps identify and convert CommonJS files to ES modules
 * Prevents "require is not defined" errors in ES module projects
 */

import fs from 'fs';
import path from 'path';
import { glob } from 'glob';
import process from 'process';

const COMMONJS_PATTERNS = {
  require: /require\s*\(/g,
  moduleExports: /module\.exports/g,
  exports: /exports\./g,
  dirname: /__dirname/g,
  filename: /__filename/g
};

const EXCLUDE_PATHS = [
  'node_modules',
  'dist',
  'build',
  '.git',
  'coverage',
  'public',
  'static'
];

class ESModuleMigrator {
  constructor() {
    this.issues = [];
    this.fixedFiles = [];
  }

  async findCommonJSFiles() {
    console.log('🔍 Scanning for CommonJS syntax in .js files...\n');

    const files = await glob('**/*.js', {
      ignore: EXCLUDE_PATHS.map(p => `${p}/**`)
    });

    for (const file of files) {
      const content = await fs.promises.readFile(file, 'utf8');
      const issues = this.detectCommonJS(content);

      if (issues.length > 0) {
        this.issues.push({ file, issues, content });
      }
    }

    return this.issues;
  }

  detectCommonJS(content) {
    const issues = [];

    Object.entries(COMMONJS_PATTERNS).forEach(([name, pattern]) => {
      const matches = content.match(pattern);
      if (matches) {
        issues.push({
          type: name,
          count: matches.length,
          pattern: pattern.toString()
        });
      }
    });

    return issues;
  }

  generateReport() {
    if (this.issues.length === 0) {
      console.log('✅ No CommonJS syntax found! Your project is ES module compliant.\n');
      return;
    }

    console.log(`⚠️  Found CommonJS syntax in ${this.issues.length} files:\n`);

    this.issues.forEach(({ file, issues }) => {
      console.log(`📄 ${file}`);
      issues.forEach(issue => {
        console.log(`   - ${issue.type}: ${issue.count} occurrence(s)`);
      });
      console.log('');
    });

    console.log('\n📊 Summary:');
    console.log(`Total files with issues: ${this.issues.length}`);
    console.log('\n💡 Solutions:');
    console.log('1. Convert files to ES modules (recommended)');
    console.log('2. Rename .js files to .cjs to keep CommonJS syntax');
    console.log('3. Remove "type": "module" from package.json (not recommended)');
  }

  async createMigrationGuide() {
    const guide = `# ES Module Migration Guide

## Files Requiring Migration

${this.issues.map(({ file, issues }) => {
  return `### ${file}
Issues found:
${issues.map(i => `- ${i.type}: ${i.count} occurrence(s)`).join('\n')}
`;
}).join('\n')}

## Migration Steps

### Option 1: Convert to ES Modules (Recommended)

1. Replace CommonJS imports:
   \`\`\`javascript
   // CommonJS
   const { Octokit } = require("@octokit/rest");
   const fs = require('fs');

   // ES Module
   import { Octokit } from "@octokit/rest";
   import fs from 'fs';
   \`\`\`

2. Replace CommonJS exports:
   \`\`\`javascript
   // CommonJS
   module.exports = MyClass;
   exports.myFunction = myFunction;

   // ES Module
   export default MyClass;
   export { myFunction };
   \`\`\`

3. Replace __dirname and __filename:
   \`\`\`javascript
   // CommonJS
   const currentDir = __dirname;
   const currentFile = __filename;

   // ES Module
   import { fileURLToPath } from 'url';
   import { dirname } from 'path';

   const __filename = fileURLToPath(import.meta.url);
   const __dirname = dirname(__filename);
   \`\`\`

### Option 2: Keep CommonJS Syntax

Rename files from \`.js\` to \`.cjs\`:
\`\`\`bash
mv script.js script.cjs
\`\`\`

Then update any references to these files in your workflows and scripts.

## Automated Conversion Script

Run this script to help with conversion:
\`\`\`bash
node scripts/es-module-converter.js
\`\`\`

## Prevention

1. Add ESLint rules to catch CommonJS syntax
2. Use pre-commit hooks to validate ES module compliance
3. Update CI/CD to check for CommonJS syntax
`;

    await fs.promises.writeFile(
      path.join(process.cwd(), 'ES_MODULE_MIGRATION.md'),
      guide
    );

    console.log('\n📝 Created ES_MODULE_MIGRATION.md with detailed migration guide');
  }
}

// Run the migrator
async function main() {
  const migrator = new ESModuleMigrator();

  try {
    await migrator.findCommonJSFiles();
    migrator.generateReport();

    if (migrator.issues.length > 0) {
      await migrator.createMigrationGuide();
      process.exit(1); // Exit with error to fail CI if needed
    }
  } catch (error) {
    console.error('❌ Error during migration scan:', error);
    process.exit(1);
  }
}

main();
