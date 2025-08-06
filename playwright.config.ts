import { defineConfig, devices } from '@playwright/test';

/**
 * Recovery Compass Mobile Testing Configuration
 * Optimized for iPhone 15 Pro testing
 */
export default defineConfig({
  testDir: './tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['line'],
    ['html', { outputFolder: 'playwright-report' }]
  ],
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: process.env.RECOVERY_COMPASS_URL || 'https://recovery-compass.org',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* Take screenshot on failure */
    screenshot: 'only-on-failure',

    /* Video recording */
    video: 'retain-on-failure',
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'iPhone 15 Pro',
      use: {
        ...devices['iPhone 15 Pro'],
        // Force webkit browser for iOS testing
        browserName: 'webkit',
      },
    },

    {
      name: 'iPhone 15 Pro - 3G',
      use: {
        ...devices['iPhone 15 Pro'],
        browserName: 'webkit',
        // Simulate slower network
        offline: false,
        // Custom context options can be added here
      },
    },

    /* Additional mobile devices for testing */
    {
      name: 'iPhone 13',
      use: { ...devices['iPhone 13'] },
    },

    {
      name: 'iPhone SE',
      use: { ...devices['iPhone SE'] },
    },
  ],

  /* Output folder for test artifacts */
  outputDir: './test-results',
});
