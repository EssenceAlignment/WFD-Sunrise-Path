# Codecov Setup Guide for WFD-Sunrise-Path

## 🎯 Why Codecov for Grant Applications

- **SAMHSA**: Demonstrates code quality metrics
- **RWJF**: Shows commitment to maintainable software
- **All Funders**: Professional development practices

## 📋 Complete Setup Steps

### 1. Add Codecov Token to GitHub Secrets

1. Go to: <https://github.com/EssenceAlignment/WFD-Sunrise-Path/settings/secrets/actions>
2. Click **New repository secret**
3. Add:
   - Name: `CODECOV_TOKEN`
   - Value: `0f442ee1-84e0-49a4-a5e3-5722e006dde1`
4. Click **Add secret**

### 2. Create Basic Test Setup

Since this is primarily an HTML/CSS project, create a simple test:

**Create `package.json`** (if not exists):

```json
{
  "name": "wfd-sunrise-path",
  "version": "1.0.0",
  "description": "Recovery Compass WFD Sunrise Path",
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "@testing-library/jest-dom": "^6.0.0"
  }
}

```text

**Create `jest.config.js`**:

```javascript
module.exports = {
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    '**/*.{js,jsx}',
    '!**/node_modules/**',
    '!**/coverage/**',
    '!jest.config.js',
  ],
  testEnvironment: 'jsdom',
};

```text

**Create `tests/sample.test.js`**:

```javascript
describe('WFD Sunrise Path', () => {
  test('project exists', () => {
    expect(true).toBe(true);
  });
  
  // Add more meaningful tests as project grows
});

```text

### 3. Install Dependencies Locally

```bash
npm install --save-dev jest @testing-library/jest-dom

```text

### 4. Test Locally

```bash
npm run test:coverage

```text

### 5. Commit and Push

The workflow file has already been created at `.github/workflows/test-and-coverage.yml`

```bash
git add .
git commit -m "ci: add Codecov integration for code quality metrics"
git push origin main

```text

### 6. Add Codecov Badge to README

Add this to the top of your README.md:

```markdown
[![codecov](https://codecov.io/gh/EssenceAlignment/WFD-Sunrise-Path/branch/main/graph/badge.svg?token=YOUR_TOKEN)](https://codecov.io/gh/EssenceAlignment/WFD-Sunrise-Path)

```text

## ✅ What Happens Next

1. **On Push**: GitHub Actions runs tests and uploads coverage
2. **On PRs**: Codecov comments with coverage changes
3. **Dashboard**: View at <https://codecov.io/gh/EssenceAlignment/WFD-Sunrise-Path>

## 🎯 Grant Impact

With Codecov active, you can show:

- "Our code maintains X% test coverage"
- "All PRs are analyzed for coverage impact"
- "We use industry-standard quality metrics"

## 📊 Coverage Goals

- **Initial**: Any coverage is good (even 10%)
- **Target**: 60-70% for grant applications
- **Ideal**: 80%+ for healthcare projects

## 🔍 Troubleshooting

If coverage doesn't appear:

1. Check GitHub Actions tab for errors
2. Verify token is set in secrets
3. Ensure tests generate `lcov.info` file

Your coverage dashboard will be available at:
<https://codecov.io/gh/EssenceAlignment/WFD-Sunrise-Path>
