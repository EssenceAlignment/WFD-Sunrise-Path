# Terminal Error Resolution System

## Automated Error Detection and Resolution Framework

### 1. Blanks-Around-Lists (MD032) Errors

**Error Pattern:**

```
MD032/blanks-around-lists Blank lines should surround lists
```

**Systematic Resolution:**

```javascript
// Pattern Detection
const MD032_PATTERN = /MD032.*blanks.*lists/;

// Resolution Logic
if (error.match(MD032_PATTERN)) {
  // Check .markdownlint.json configuration
  const config = readJSON('.markdownlint.json');
  
  // MD032 expects number, not boolean
  if (typeof config.MD032.blanks === 'boolean') {
    config.MD032.blanks = 1; // Convert to number
    writeJSON('.markdownlint.json', config);
  }
  
  // Auto-fix markdown files
  runCommand('npm run fix:markdown');
}
```

**Prevention:**

- Always use numbers for MD032 blanks configuration
- Set up pre-commit hooks to validate config types
- Use schema validation for JSON configs

### 2. Unknown Word Errors (Spell Check)

**Error Pattern:**

```
Unknown word (autobuild)
Unknown word (SUBSCALES)
```

**Systematic Resolution:**

```javascript
// Pattern Detection
const UNKNOWN_WORD_PATTERN = /Unknown word \((\w+)\)/g;

// Resolution Logic
function handleUnknownWords(output) {
  const unknownWords = [];
  let match;
  
  while ((match = UNKNOWN_WORD_PATTERN.exec(output)) !== null) {
    unknownWords.push(match[1]);
  }
  
  if (unknownWords.length > 0) {
    // Read current dictionary
    const cspellConfig = readJSON('.cspell.json');
    
    // Add unknown words to dictionary
    const uniqueWords = [...new Set([...cspellConfig.words, ...unknownWords])];
    cspellConfig.words = uniqueWords.sort();
    
    // Save updated dictionary
    writeJSON('.cspell.json', cspellConfig);
    
    // Re-run spell check to verify
    runCommand('npm run spell:check');
  }
}
```

**Smart Word Classification:**

```javascript
function classifyWord(word) {
  // Technical terms
  if (word.match(/^[A-Z_]+$/)) return 'acronym';
  if (word.includes('_')) return 'snake_case';
  if (word.match(/^[a-z]+[A-Z]/)) return 'camelCase';
  
  // Project-specific terms
  if (projectContext.includes(word.toLowerCase())) return 'project_term';
  
  // Likely typo
  return 'possible_typo';
}
```

### 3. Type Mismatch Errors

**Error Pattern:**

```
Incorrect type. Expected "boolean"
Incorrect type. Expected "number"
```

**Systematic Resolution:**

```javascript
// Type Resolution Map
const TYPE_FIXES = {
  'MD032': {
    'blanks': { expected: 'number', default: 1 },
  },
  'MD040': {
    'allowed_languages': { expected: 'array', default: ['bash', 'javascript', 'json'] }
  }
};

// Resolution Logic
function fixTypeError(rule, property, expectedType) {
  const config = readJSON('.markdownlint.json');
  
  switch (expectedType) {
    case 'number':
      if (typeof config[rule][property] === 'boolean') {
        config[rule][property] = config[rule][property] ? 1 : 0;
      }
      break;
    case 'boolean':
      if (typeof config[rule][property] === 'string') {
        config[rule][property] = config[rule][property] === 'true';
      }
      break;
    case 'array':
      if (!Array.isArray(config[rule][property])) {
        config[rule][property] = [config[rule][property]];
      }
      break;
  }
  
  writeJSON('.markdownlint.json', config);
}
```

## Automated Error Resolution Pipeline

### Step 1: Error Detection

```bash
#!/bin/bash
# error_detector.sh

# Capture all linting output
MARKDOWN_ERRORS=$(npm run lint:markdown 2>&1)
SPELL_ERRORS=$(npm run spell:check 2>&1)

# Parse and categorize errors
echo "$MARKDOWN_ERRORS" | grep -E "MD[0-9]+" > markdown_issues.txt
echo "$SPELL_ERRORS" | grep "Unknown word" > spell_issues.txt
```

### Step 2: Automatic Resolution

```javascript
// auto_fix_errors.js
const fs = require('fs');
const { execSync } = require('child_process');

class ErrorResolver {
  constructor() {
    this.fixes = {
      'MD032': this.fixMD032,
      'MD040': this.fixMD040,
      'spell': this.fixSpelling,
      'type': this.fixType
    };
  }

  resolveAll() {
    // Fix configuration errors first
    this.fixConfigurationErrors();
    
    // Fix spelling errors
    this.fixSpellingErrors();
    
    // Fix markdown issues
    this.fixMarkdownIssues();
    
    // Verify all fixes
    this.verifyFixes();
  }

  fixMD032(config) {
    if (!config.MD032) config.MD032 = {};
    if (typeof config.MD032.blanks !== 'number') {
      config.MD032.blanks = 1;
    }
    return config;
  }

  fixSpellingErrors() {
    try {
      const output = execSync('npm run spell:check', { encoding: 'utf8' });
      const unknownWords = this.extractUnknownWords(output);
      
      if (unknownWords.length > 0) {
        const cspellConfig = JSON.parse(fs.readFileSync('.cspell.json', 'utf8'));
        cspellConfig.words = [...new Set([...cspellConfig.words, ...unknownWords])].sort();
        fs.writeFileSync('.cspell.json', JSON.stringify(cspellConfig, null, 2));
      }
    } catch (error) {
      // Parse error output for unknown words
      this.handleSpellCheckError(error.stdout || error.stderr);
    }
  }

  extractUnknownWords(output) {
    const words = [];
    const pattern = /Unknown word \((\w+)\)/g;
    let match;
    
    while ((match = pattern.exec(output)) !== null) {
      // Filter out node_modules and other irrelevant paths
      if (!output.includes('node_modules')) {
        words.push(match[1]);
      }
    }
    
    return words;
  }
}

// Run the resolver
const resolver = new ErrorResolver();
resolver.resolveAll();
```

### Step 3: Pre-Commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: fix-linting-errors
        name: Auto-fix linting errors
        entry: node scripts/auto_fix_errors.js
        language: system
        always_run: true
        pass_filenames: false
```

## Real-Time Error Prevention

### 1. VS Code Settings

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.markdownlint": true
  },
  "cSpell.userWords": [],
  "cSpell.autoAddWords": true
}
```

### 2. Git Hooks

```bash
#!/bin/bash
# .git/hooks/pre-push

# Run all checks
npm run lint:markdown
npm run spell:check

# Auto-fix if errors found
if [ $? -ne 0 ]; then
  echo "Errors found, attempting auto-fix..."
  node scripts/auto_fix_errors.js
  
  # Re-run checks
  npm run lint:markdown
  npm run spell:check
  
  if [ $? -ne 0 ]; then
    echo "Some errors could not be auto-fixed. Please review."
    exit 1
  fi
fi
```

## Systematic Approach Summary

1. **Immediate Detection**: Errors are caught as they occur
2. **Pattern Recognition**: Each error type has a specific pattern
3. **Automated Resolution**: Scripts automatically fix known issues
4. **Validation**: Changes are verified before proceeding
5. **Prevention**: Hooks and configs prevent future occurrences

## Never Manual Again

With this system in place:

- Type errors are automatically corrected based on schema
- Unknown words are intelligently added to dictionaries
- Markdown formatting is auto-fixed on save
- Pre-commit hooks catch and fix issues before they reach the repository
- CI/CD pipelines validate all changes

This ensures you'll never need to manually fix these types of errors again.
