# Comprehensive Guardrail System

## Overview

This repository now implements a multi-layered guardrail system that prevents common errors from ever reaching the
codebase. No more manual fixes for linting, spelling, or type errors.

## Layers of Protection

### 1. Editor Level (Immediate Feedback)

- **VS Code Settings** (.vscode/settings.json)
  - Auto-format on save
  - Markdownlint integration
  - CSpell custom dictionary
  - YAML schema validation
  - Type checking inline

### 2. Pre-Commit Level (Local Enforcement)

- **Pre-commit hooks** (.pre-commit-config.yaml)
  - Markdownlint with auto-fix
  - Vale style checking
  - YAML type validation
  - JSON validation
  - CSpell spell checking
  - Trailing whitespace removal
  - End-of-file fixer

### 3. CI/CD Level (Remote Enforcement)

- **GitHub Actions** (.github/workflows/comprehensive-lint.yml)
  - All pre-commit checks
  - Additional validation
  - Merge conflict detection
  - Summary reports

## Configuration Files

### Markdownlint (.markdownlint.json)

```json
"MD032": {
  "ul_single": 1,
  "ol_single": 1,
  "ul_multi": 1,
  "ol_multi": 1
}
```

- Properly configured for blanks around lists
- No more boolean/number type errors

### YAML Lint (.yamllint)

```yaml
truthy:
  allowed-values: ['true', 'false']
  check-keys: true
```

- Enforces strict boolean types
- Prevents "Expected Boolean" errors

### Vale (.vale.ini)

- Custom word list in styles/TermSwap/WordList.txt
- Project-specific terms (autobuild, SUBSCALES, etc.)
- Integrated with pre-commit and CI

### CSpell (.cspell.json)

- Comprehensive project dictionary
- Auto-updated by VS Code
- Synced with Vale word list

### EditorConfig (.editorconfig)

- Consistent formatting across all IDEs
- Language-specific indentation rules
- Line ending normalization

## Dictionary Governance

* `pending.txt` terms must be promoted to `accepted.txt` via PR within **7 days** or are auto-purged by the weekly `purge-pending-words` workflow.

## How It Works

### Local Development

1. **Write code** - VS Code provides inline feedback
2. **Save file** - Auto-formatting applied
3. **Commit** - Pre-commit hooks run automatically
4. **Push** - Only clean code reaches the repository

### CI/CD Pipeline

1. **Push/PR** - GitHub Actions triggered
2. **All checks run** - Same rules as local
3. **Status reported** - Branch protection enforces
4. **Merge blocked** - Until all checks pass

## Maintenance

### Adding New Words

1. Add to `.cspell.json` words array
2. Add to `styles/TermSwap/WordList.txt`
3. Commit both files

### Updating Linters

```bash
/Users/ericjones/Library/Python/3.12/bin/pre-commit autoupdate
```

### Running Manually

```bash
# Run all checks
/Users/ericjones/Library/Python/3.12/bin/pre-commit run --all-files

# Run specific check
/Users/ericjones/Library/Python/3.12/bin/pre-commit run markdownlint --all-files
```

## Never Manual Again

With this system:

- ❌ No more "blanks-around-lists" errors
- ❌ No more "unknown word" failures
- ❌ No more "Expected Boolean" type mismatches
- ❌ No more manual formatting fixes
- ✅ Automatic error prevention
- ✅ Consistent code quality
- ✅ Zero manual intervention

The guardrails are now stronger than any individual's habits or AI's suggestions.
