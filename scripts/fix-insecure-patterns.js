#!/usr/bin/env node
/**
 * Automated Security Pattern Fixer
 * Detects and fixes common insecure patterns in the codebase
 */

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Define patterns to fix
const patterns = [
  {
    name: 'insecure-random',
    regex: /Math\.random\(\)/g,
    replacement: 'crypto.getRandomValues(new Uint32Array(1))[0] / 0xFFFFFFFF',
    import: "const crypto = require('crypto');",
    fileTypes: ['js', 'ts'],
    description: 'Replace Math.random() with secure random'
  },
  {
    name: 'eval-usage',
    regex: /eval\s*\(/g,
    replacement: '/* SECURITY: eval() removed - refactor needed */',
    fileTypes: ['js', 'ts'],
    description: 'Remove eval() usage'
  },
  {
    name: 'hardcoded-localhost',
    regex: /http:\/\/localhost/g,
    replacement: `process.env.API_URL || 'http://localhost'`,
    fileTypes: ['js', 'ts', 'jsx', 'tsx'],
    description: 'Replace hardcoded localhost with environment variable'
  }
];

// Additional security headers for React/Next.js files
const securityHeaders = {
  'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline';",
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin'
};

function fixPatterns(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  const fixes = [];

  patterns.forEach(pattern => {
    const ext = path.extname(filePath).slice(1);
    if (!pattern.fileTypes.includes(ext)) return;

    if (pattern.regex.test(content)) {
      const matches = content.match(pattern.regex);
      content = content.replace(pattern.regex, pattern.replacement);
      modified = true;

      // Add import if needed
      if (pattern.import && !content.includes(pattern.import.split(' ').pop())) {
        content = pattern.import + '\n' + content;
      }

      fixes.push({
        pattern: pattern.name,
        count: matches ? matches.length : 0,
        description: pattern.description
      });
    }
  });

  if (modified) {
    fs.writeFileSync(filePath, content);
    console.log(`✅ Fixed ${filePath}`);
    fixes.forEach(fix => {
      console.log(`   - ${fix.description} (${fix.count} instances)`);
    });
  }

  return fixes;
}

function addSecurityHeaders(filePath) {
  if (!filePath.includes('_app.') && !filePath.includes('middleware.')) return;

  let content = fs.readFileSync(filePath, 'utf8');
  let modified = false;

  // Check if security headers are already present
  if (!content.includes('Content-Security-Policy')) {
    // Add security headers configuration
    const headerCode = `
// Security headers configuration
export const securityHeaders = ${JSON.stringify(securityHeaders, null, 2)};
`;
    content = headerCode + '\n' + content;
    modified = true;
  }

  if (modified) {
    fs.writeFileSync(filePath, content);
    console.log(`✅ Added security headers to ${filePath}`);
  }
}

// Main execution
console.log('🔍 Scanning for insecure patterns...\n');

const srcFiles = glob.sync('src/**/*.{js,ts,jsx,tsx}', { ignore: '**/node_modules/**' });
const scriptFiles = glob.sync('scripts/**/*.{js,ts}', { ignore: '**/node_modules/**' });
const allFiles = [...srcFiles, ...scriptFiles];

let totalFixes = 0;

allFiles.forEach(file => {
  const fixes = fixPatterns(file);
  totalFixes += fixes.length;
  addSecurityHeaders(file);
});

console.log(`\n✅ Security fixes complete! Fixed ${totalFixes} issues.`);

// Also fix package.json scripts if needed
const packagePath = path.join(process.cwd(), 'package.json');
if (fs.existsSync(packagePath)) {
  const pkg = JSON.parse(fs.readFileSync(packagePath, 'utf8'));

  // Add security-related scripts if not present
  if (!pkg.scripts) pkg.scripts = {};

  if (!pkg.scripts['fix:security']) {
    pkg.scripts['fix:security'] = 'node scripts/fix-insecure-patterns.js';
  }

  if (!pkg.scripts['fix:all']) {
    pkg.scripts['fix:all'] = 'npm run fix:security && npm run lint:fix && npm test';
  }

  if (!pkg.scripts['pre-push']) {
    pkg.scripts['pre-push'] = 'npm run fix:all';
  }

  fs.writeFileSync(packagePath, JSON.stringify(pkg, null, 2) + '\n');
}
