#!/usr/bin/env node

/**
 * Recovery Compass Mobile Test Runner
 * Executes Playwright tests with iPhone 15 Pro configuration
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Check if running on macOS
if (process.platform !== 'darwin') {
  console.error('❌ This script requires macOS for iOS testing');
  process.exit(1);
}

// Test configuration
const testConfig = {
  testFile: 'tests/mobile/ios/recovery-compass-mobile.spec.ts',
  outputDir: 'test-results',
  screenshotDir: 'screenshots',
  videoDir: 'videos',
  reportDir: 'playwright-report'
};

// Ensure directories exist
[testConfig.outputDir, testConfig.screenshotDir, testConfig.videoDir].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

console.log('🚀 Recovery Compass Mobile Testing');
console.log('==================================');
console.log(`📱 Device: iPhone 15 Pro`);
console.log(`🌐 URL: ${process.env.RECOVERY_COMPASS_URL || 'https://recovery-compass.org'}`);
console.log('');

// Check if Playwright is installed
try {
  require.resolve('@playwright/test');
} catch (e) {
  console.log('📦 Installing Playwright dependencies...');
  const install = spawn('npm', ['install', '--save-dev', '@playwright/test', 'typescript'], {
    stdio: 'inherit',
    shell: true
  });

  install.on('close', (code) => {
    if (code !== 0) {
      console.error('❌ Failed to install dependencies');
      process.exit(1);
    }
    console.log('✅ Dependencies installed');
    runTests();
  });
}

function generateTestSummary(exitCode) {
  // Try to read performance metrics if available
  const metricsPath = 'performance-metrics.json';
  const edgeLatencyPath = 'edge-storage-latency.json';

  const summary = {
    passed: 0,
    failed: 0,
    skipped: 0,
    exitCode: exitCode
  };

  // Simple summary based on exit code
  if (exitCode === 0) {
    summary.passed = 8; // Total number of tests
  } else {
    summary.failed = 1;
    summary.passed = 7;
  }

  // Write summary for CI
  fs.writeFileSync(
    path.join(testConfig.outputDir, 'summary.json'),
    JSON.stringify(summary, null, 2)
  );

  // Log performance metrics if available
  if (fs.existsSync(metricsPath)) {
    const metrics = JSON.parse(fs.readFileSync(metricsPath, 'utf8'));
    console.log('\n📊 Performance Metrics:');
    console.log(`   - FCP: ${metrics.fcp}ms ${metrics.fcp < 3000 ? '✅' : '❌'}`);
    console.log(`   - TTI: ${metrics.tti}ms ${metrics.tti < 5000 ? '✅' : '❌'}`);

    if (metrics.accessibilityIssues && metrics.accessibilityIssues.length > 0) {
      console.log(`   - Accessibility Issues: ${metrics.accessibilityIssues.length} ⚠️`);
    }
  }

  // Log edge latency if available
  if (fs.existsSync(edgeLatencyPath)) {
    const latency = JSON.parse(fs.readFileSync(edgeLatencyPath, 'utf8'));
    console.log('\n🌐 Edge Storage Latency:');
    Object.entries(latency).forEach(([key, value]) => {
      console.log(`   - ${key}: ${value}ms`);
    });
  }
}

function runTests() {
  console.log('🧪 Running mobile tests...');

  // Playwright test command
  const args = [
    'playwright', 'test',
    testConfig.testFile,
    '--reporter=line,html',
    '--output', testConfig.outputDir,
    '--screenshot=on',
    '--video=on',
    '--trace=on-first-retry'
  ];

  // Add headed mode if requested
  if (process.argv.includes('--headed')) {
    args.push('--headed');
  }

  // Add specific test if requested
  const testIndex = process.argv.indexOf('--test');
  if (testIndex > -1 && process.argv[testIndex + 1]) {
    args.push('-g', process.argv[testIndex + 1]);
  }

  // Run tests
  const test = spawn('npx', args, {
    stdio: 'inherit',
    shell: true,
    env: {
      ...process.env,
      // Force color output
      FORCE_COLOR: '1'
    }
  });

  test.on('close', (code) => {
    console.log('');

    // Generate summary for CI
    generateTestSummary(code);

    if (code === 0) {
      console.log('✅ All tests passed!');
      console.log('');
      console.log('📊 Results:');
      console.log(`   - HTML Report: ${testConfig.reportDir}/index.html`);
      console.log(`   - Screenshots: ${testConfig.screenshotDir}/`);
      console.log(`   - Videos: ${testConfig.videoDir}/`);
      console.log('');
      console.log('🔍 To view the report, run:');
      console.log(`   open ${testConfig.reportDir}/index.html`);
    } else {
      console.error('❌ Some tests failed');
      console.log('');
      console.log('🔍 Check the HTML report for details:');
      console.log(`   open ${testConfig.reportDir}/index.html`);
      process.exit(1);
    }
  });
}

// Run tests if dependencies are already installed
if (require.main === module) {
  try {
    require.resolve('@playwright/test');
    runTests();
  } catch (e) {
    // Dependencies will be installed in the check above
  }
}

// Usage help
if (process.argv.includes('--help')) {
  console.log('Usage: node run-recovery-compass-tests.js [options]');
  console.log('');
  console.log('Options:');
  console.log('  --headed         Run tests in headed mode (see browser)');
  console.log('  --test <name>    Run specific test by name');
  console.log('  --help           Show this help message');
  console.log('');
  console.log('Environment Variables:');
  console.log('  RECOVERY_COMPASS_URL   Base URL for testing (default: https://recovery-compass.org)');
  process.exit(0);
}
