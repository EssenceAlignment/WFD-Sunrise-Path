#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Define patterns to fix with their replacements
const patterns = [
  {
    name: 'insecure-random',
    regex: /Math\.random\(\)/g,
    replacement: 'crypto.getRandomValues(new Uint32Array(1))[0] / 0xFFFFFFFF',
    importNode: "const crypto = globalThis.crypto || require('crypto').webcrypto;",
    importBrowser: "// crypto is available globally in browsers",
    description: 'Replace Math.random() with crypto.getRandomValues()',
  },
  {
    name: 'insecure-date-random',
    regex: /Date\.now\(\)\s*\*\s*Math\.random\(\)/g,
    replacement: 'crypto.getRandomValues(new BigUint64Array(1))[0]',
    importNode: "const crypto = globalThis.crypto || require('crypto').webcrypto;",
    importBrowser: "// crypto is available globally in browsers",
    description: 'Replace Date.now() * Math.random() with secure random',
  },
  {
    name: 'weak-array-shuffle',
    regex: /array\.sort\(\(\)\s*=>\s*Math\.random\(\)\s*-\s*0\.5\)/g,
    replacement: 'array.sort(() => crypto.getRandomValues(new Uint32Array(1))[0] / 0xFFFFFFFF - 0.5)',
    importNode: "const crypto = globalThis.crypto || require('crypto').webcrypto;",
    importBrowser: "// crypto is available globally in browsers",
    description: 'Replace weak array shuffle with secure random',
  },
];

// Statistics tracking
const stats = {
  filesScanned: 0,
  filesModified: 0,
  patternsFixed: 0,
  errors: [],
};

function detectEnvironment(content, filePath) {
  // Check if it's a browser file
  const isBrowser = content.includes('window') ||
                   content.includes('document') ||
                   filePath.includes('browser') ||
                   filePath.includes('client');

  // Check if it's TypeScript
  const isTypeScript = filePath.endsWith('.ts') || filePath.endsWith('.tsx');

  return { isBrowser, isTypeScript };
}

function addImportIfNeeded(content, pattern, environment) {
  const importStatement = environment.isBrowser ? pattern.importBrowser : pattern.importNode;

  // Check if crypto is already imported
  if (content.includes('crypto') || content.includes(importStatement)) {
    return content;
  }

  // Add import at the top of the file
  if (environment.isTypeScript) {
    // For TypeScript, add after any existing imports
    const importMatch = content.match(/^(import .+\n)+/m);
    if (importMatch) {
      const lastImportEnd = importMatch.index + importMatch[0].length;
      return content.slice(0, lastImportEnd) + importStatement + '\n' + content.slice(lastImportEnd);
    }
  }

  // Add at the very beginning with a comment
  return `${importStatement}\n\n${content}`;
}

function fixPatterns(filePath) {
  try {
    stats.filesScanned++;

    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;
    const environment = detectEnvironment(content, filePath);

    patterns.forEach(pattern => {
      if (pattern.regex.test(content)) {
        console.log(`📝 Found ${pattern.name} in ${filePath}`);

        // Add import if needed
        if (!environment.isBrowser) {
          content = addImportIfNeeded(content, pattern, environment);
        }

        // Replace the pattern
        const matches = content.match(pattern.regex)?.length || 0;
        content = content.replace(pattern.regex, pattern.replacement);

        stats.patternsFixed += matches;
        modified = true;

        console.log(`   ✅ Fixed ${matches} occurrence(s): ${pattern.description}`);
      }
    });

    if (modified) {
      fs.writeFileSync(filePath, content);
      stats.filesModified++;
      console.log(`   💾 Saved ${filePath}\n`);
    }
  } catch (error) {
    stats.errors.push({ file: filePath, error: error.message });
    console.error(`❌ Error processing ${filePath}: ${error.message}`);
  }
}

// Main execution
console.log('🔍 Scanning for insecure patterns...\n');

// Find all JavaScript and TypeScript files
const files = glob.sync('**/*.{js,jsx,ts,tsx}', {
  ignore: [
    'node_modules/**',
    'coverage/**',
    'dist/**',
    'build/**',
    '*.min.js',
    'vendor/**',
  ],
});

// Process each file
files.forEach(fixPatterns);

// Report results
console.log('\n📊 Summary:');
console.log(`   Files scanned: ${stats.filesScanned}`);
console.log(`   Files modified: ${stats.filesModified}`);
console.log(`   Patterns fixed: ${stats.patternsFixed}`);

if (stats.errors.length > 0) {
  console.log(`\n⚠️  Errors encountered:`);
  stats.errors.forEach(({ file, error }) => {
    console.log(`   - ${file}: ${error}`);
  });
}

if (stats.filesModified > 0) {
  console.log('\n✨ Security patterns have been automatically fixed!');
  console.log('📝 Please review the changes and run tests to ensure everything works correctly.');
} else {
  console.log('\n✅ No insecure patterns found. Your code is already secure!');
}

// Exit with error code if fixes were needed (for CI)
process.exit(stats.filesModified > 0 ? 1 : 0);
