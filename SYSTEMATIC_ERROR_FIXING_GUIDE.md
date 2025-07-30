# Systematic Error Fixing Guide

## Understanding Common Configuration Errors

### 1. Type Mismatch Errors (e.g., "Expected Boolean")

**Problem Pattern:**

```json
"MD032": {
  "blanks": true  // ERROR: Expected number, got boolean
}
```text

**Systematic Solution:**

1. Check the rule documentation or schema
2. MD032 expects a number for blank lines count
3. Fix: Change `true` to `1` (or appropriate number)

**How to identify the correct type:**

- Look at the error message: "Incorrect type. Expected 'boolean'" tells you what type is needed
- Check the markdownlint documentation for each rule
- Common types: boolean, number, string, array

### 2. Spell Check Errors (Unknown Words)

**Problem Pattern:**

```text
Unknown word (SUBSCALES)
Unknown word (autobuild)
```text

**Systematic Solution:**

1. Determine if it's a valid technical term or typo
2. If valid, add to `.cspell.json` dictionary
3. If typo, fix in the source file

**Decision Tree:**

- Is it a proper name? → Add to dictionary
- Is it a technical term? → Add to dictionary
- Is it a project-specific term? → Add to dictionary
- Is it a typo? → Fix the spelling

### 3. Markdown Lint Errors

**Common Issues:**

- MD032: Blank lines around lists
- MD040: Fenced code blocks need language specification
- MD013: Line length exceeds limit

**Systematic Fixes:**

```markdown
# MD032 - Add blank lines around lists
Before list

- Item 1
- Item 2

After list

# MD040 - Specify language for code blocks
```text
This is a text block
```text

```bash
echo "This is a bash command"
```text

# MD013 - Break long lines

Instead of: This is a very long line that exceeds the 120 character limit and will cause an error in markdownlint
Use: This is a line that is broken up properly
to stay within the 120 character limit.

```text

## Automated Systematic Approach

### Step 1: Identify All Issues
```bash
# Run all linters to get complete picture
npm run lint:markdown
npm run spell:check
# Check for type errors in configs
```text

### Step 2: Categorize Issues

1. Configuration errors (JSON schema violations)
2. Spelling issues (unknown words)
3. Formatting issues (markdown violations)

### Step 3: Fix Systematically

1. Fix configuration files first (they affect how linters run)
2. Update dictionaries for valid terms
3. Fix source files last

### Step 4: Verify Fixes

```bash
# Re-run all checks
npm run lint:markdown
npm run spell:check
```text

## Prevention Strategy

### 1. Pre-commit Hooks

Set up git hooks to run linters before commits

### 2. CI/CD Integration

GitHub Actions already configured to catch issues

### 3. Regular Maintenance

- Review and update `.cspell.json` dictionary
- Keep `.markdownlint.json` rules reasonable
- Document project-specific terms

## Common Configuration Fixes

### .markdownlint.json

```json
{
  "MD032": {
    "blanks": 1  // Number, not boolean
  },
  "MD040": {
    "allowed_languages": ["bash", "javascript", "json", "yaml", "text", ""]
  }
}
```text

### .cspell.json

```json
{
  "words": [
    "autobuild",
    "SUBSCALES",
    "project-specific-terms"
  ]
}
```text

## Error Resolution Workflow

1. **Read the error carefully**
   - Note the file and line number
   - Understand what type/format is expected

2. **Check documentation**
   - For type errors: Check the tool's schema
   - For lint errors: Check the rule documentation

3. **Apply the minimal fix**
   - Don't over-correct
   - Keep changes focused

4. **Test the fix**
   - Run the specific linter
   - Verify no new errors introduced

5. **Document if needed**
   - Add comments for non-obvious fixes
   - Update project documentation
