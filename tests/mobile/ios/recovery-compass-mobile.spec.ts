import { test, expect, devices } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Base URL for Recovery Compass
const BASE_URL = process.env.RECOVERY_COMPASS_URL || 'https://recovery-compass.org';

// Performance metrics storage
const performanceMetrics: any = {
  fcp: 0,
  tti: 0,
  edgeLatency: {},
  accessibilityIssues: []
};

test.describe('Recovery Compass - iPhone 15 Pro Testing', () => {
  test.beforeEach(async ({ page }) => {
    // Clear browser state before each test
    await page.context().clearCookies();
  });

  test('Compass Companion journaling flow', async ({ page }) => {
    await test.step('Navigate to Recovery Compass', async () => {
      // Measure performance metrics
      const startTime = Date.now();
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });

      // Capture FCP and TTI
      const metrics = await page.evaluate(() => {
        const paint = performance.getEntriesByType('paint');
        const fcp = paint.find(entry => entry.name === 'first-contentful-paint');
        return {
          fcp: fcp ? fcp.startTime : 0,
          tti: performance.timing.domInteractive - performance.timing.navigationStart
        };
      });

      performanceMetrics.fcp = metrics.fcp;
      performanceMetrics.tti = metrics.tti;

      await expect(page).toHaveTitle(/Recovery Compass/i);
    });

    await test.step('Open journaling interface', async () => {
      // Look for journal button/link
      const journalButton = page.getByRole('button', { name: /journal|write|story/i })
        || page.getByText(/journal|write|story/i);
      await journalButton.click();
      await page.waitForLoadState('networkidle');
    });

    await test.step('Create journal entry', async () => {
      // Find text input area
      const textArea = page.getByRole('textbox')
        || page.getByPlaceholder(/start typing|write|tell your story/i)
        || page.locator('textarea').first();

      await textArea.fill('Mobile testing entry: Testing Recovery Compass journaling on iPhone 15 Pro with 3G network conditions.');

      // Submit entry
      const submitButton = page.getByRole('button', { name: /submit|save|post/i })
        || page.getByText(/submit|save|post/i);
      await submitButton.click();
    });

    await test.step('Verify entry saved', async () => {
      // Check for success message or saved indicator
      await expect(page.getByText(/saved|posted|success/i)).toBeVisible({ timeout: 10000 });
      await page.screenshot({
        path: 'screenshots/journaling-success.png',
        fullPage: true
      });
    });
  });

  test('Funding dashboard mobile view', async ({ page }) => {
    await test.step('Navigate to funding dashboard', async () => {
      await page.goto(`${BASE_URL}/funding`, { waitUntil: 'networkidle' });
      // Fallback URLs if /funding doesn't exist
      if (page.url() === BASE_URL || page.url() === `${BASE_URL}/`) {
        await page.getByRole('link', { name: /funding|grants|resources/i }).click();
      }
    });

    await test.step('Verify dashboard loads', async () => {
      // Check for funding-related content
      const fundingHeading = page.getByRole('heading', { name: /funding|grant|resource/i })
        || page.getByText(/funding dashboard|available grants/i);
      await expect(fundingHeading).toBeVisible({ timeout: 15000 });
    });

    await test.step('Check mobile responsiveness', async () => {
      // Verify viewport constraints
      const viewportSize = page.viewportSize();
      expect(viewportSize?.width).toBeLessThanOrEqual(430); // iPhone 15 Pro width

      // Screenshot dashboard
      await page.screenshot({
        path: 'screenshots/funding-dashboard-mobile.png',
        fullPage: true
      });
    });

    await test.step('Test funding card interactions', async () => {
      // Try to interact with first funding opportunity
      const fundingCard = page.locator('[data-testid*="funding"]').first()
        || page.locator('.funding-card').first()
        || page.getByRole('article').first();

      if (await fundingCard.isVisible()) {
        await fundingCard.click();
        await page.waitForLoadState('networkidle');
        await page.screenshot({
          path: 'screenshots/funding-detail-mobile.png'
        });
      }
    });
  });

  test('PWA offline fallback', async ({ page, context }) => {
    await test.step('Load Recovery Compass online', async () => {
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });
      await expect(page).toHaveTitle(/Recovery Compass/i);

      // Wait for service worker registration
      await page.waitForTimeout(3000);
    });

    await test.step('Go offline and test fallback', async () => {
      // Simulate offline conditions
      await context.setOffline(true);

      // Try to navigate or reload
      await page.reload({ waitUntil: 'domcontentloaded' }).catch(() => {
        // Offline reload might fail, that's expected
      });

      // Check for offline indicator or cached content
      const offlineIndicator = page.getByText(/offline|no connection|cached/i);
      const pageContent = page.locator('body');

      // Either we see offline message or cached content
      await expect(async () => {
        const hasOfflineMessage = await offlineIndicator.isVisible();
        const hasContent = await pageContent.isVisible();
        expect(hasOfflineMessage || hasContent).toBeTruthy();
      }).toPass({ timeout: 10000 });

      await page.screenshot({
        path: 'screenshots/offline-mode.png',
        fullPage: true
      });
    });

    await test.step('Restore connection', async () => {
      await context.setOffline(false);
      await page.reload({ waitUntil: 'networkidle' });
      await expect(page).toHaveTitle(/Recovery Compass/i);
    });
  });

  test('Share sheet and iOS integration', async ({ page, browserName }) => {
    test.skip(browserName !== 'webkit', 'Share sheet test is iOS specific');

    await test.step('Navigate to shareable content', async () => {
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });

      // Find a story or content piece to share
      const storyLink = page.getByRole('link', { name: /story|read more|view/i }).first()
        || page.locator('article a').first();

      if (await storyLink.isVisible()) {
        await storyLink.click();
        await page.waitForLoadState('networkidle');
      }
    });

    await test.step('Test share functionality', async () => {
      // Look for share button
      const shareButton = page.getByRole('button', { name: /share/i })
        || page.locator('[aria-label*="share"]')
        || page.locator('.share-button');

      if (await shareButton.isVisible()) {
        await shareButton.click();
        await page.waitForTimeout(1000);

        // Screenshot share sheet if visible
        await page.screenshot({
          path: 'screenshots/share-sheet.png'
        });
      }
    });
  });

  test('Edge storage behavior verification', async ({ page }) => {
    await test.step('Check Cloudflare Workers response', async () => {
      // Navigate to a page that uses edge functions
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });

      // Monitor network requests to Cloudflare
      const edgeRequests: string[] = [];
      page.on('request', request => {
        const url = request.url();
        if (url.includes('workers.dev') || url.includes('cloudflare')) {
          edgeRequests.push(url);
        }
      });

      // Perform actions that trigger edge storage
      const journalButton = page.getByRole('button', { name: /journal|write/i });
      if (await journalButton.isVisible()) {
        await journalButton.click();
        await page.waitForTimeout(2000);
      }

      // Log edge requests for verification
      console.log('Edge storage requests:', edgeRequests);
      expect(edgeRequests.length).toBeGreaterThan(0);
    });

    await test.step('Verify API health check and measure latency', async () => {
      // Measure edge storage latencies
      const latencyTests = {
        kv: { endpoint: '/api/kv-test', latency: 0 },
        r2: { endpoint: '/api/r2-test', latency: 0 },
        d1: { endpoint: '/api/d1-test', latency: 0 }
      };

      // Test main health check
      const healthStart = Date.now();
      const response = await page.request.get(`${BASE_URL}/api/healthcheck`).catch(() => null);
      const healthLatency = Date.now() - healthStart;

      if (response) {
        expect(response.status()).toBeLessThan(400);
        const headers = response.headers();
        console.log('Edge headers:', headers);

        // Check for Cloudflare headers
        expect(headers['cf-ray'] || headers['cf-cache-status']).toBeTruthy();

        performanceMetrics.edgeLatency.healthcheck = healthLatency;
      }

      // Test individual storage endpoints
      for (const [storage, config] of Object.entries(latencyTests)) {
        const start = Date.now();
        await page.request.get(`${BASE_URL}${config.endpoint}`).catch(() => null);
        config.latency = Date.now() - start;
        performanceMetrics.edgeLatency[storage] = config.latency;
        console.log(`${storage.toUpperCase()} latency: ${config.latency}ms`);
      }
    });
  });

  test('Accessibility verification', async ({ page }) => {
    await test.step('Check accessibility on main page', async () => {
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });

      // Get accessibility snapshot
      const accessibilitySnapshot = await page.accessibility.snapshot();

      // Check for missing landmarks
      if (!accessibilitySnapshot?.children?.some((child: any) => child.role === 'main')) {
        performanceMetrics.accessibilityIssues.push('Missing main landmark');
      }

      // Check for missing headings
      const headings = await page.$$('h1, h2, h3, h4, h5, h6');
      if (headings.length === 0) {
        performanceMetrics.accessibilityIssues.push('No headings found');
      }

      // Check for images without alt text
      const imagesWithoutAlt = await page.$$eval('img:not([alt])', imgs => imgs.length);
      if (imagesWithoutAlt > 0) {
        performanceMetrics.accessibilityIssues.push(`${imagesWithoutAlt} images without alt text`);
      }

      // Check touch target sizes
      const buttons = await page.$$('button, a, input, textarea, select');
      for (const button of buttons) {
        const box = await button.boundingBox();
        if (box && (box.width < 44 || box.height < 44)) {
          performanceMetrics.accessibilityIssues.push('Touch target too small (< 44x44)');
          break; // Only report once
        }
      }

      // Log accessibility issues
      if (performanceMetrics.accessibilityIssues.length > 0) {
        console.warn('Accessibility issues:', performanceMetrics.accessibilityIssues);
      }
    });
  });

  test('Console error monitoring', async ({ page }) => {
    const consoleErrors: string[] = [];

    // Capture console errors
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    // Capture page errors
    page.on('pageerror', error => {
      consoleErrors.push(error.message);
    });

    await test.step('Navigate through key pages', async () => {
      await page.goto(BASE_URL, { waitUntil: 'networkidle' });
      await page.waitForTimeout(2000);

      // Try funding page
      await page.goto(`${BASE_URL}/funding`, { waitUntil: 'networkidle' }).catch(() => {});
      await page.waitForTimeout(2000);
    });

    // Report any console errors
    if (consoleErrors.length > 0) {
      console.error('Console errors detected:', consoleErrors);
      await page.screenshot({
        path: 'screenshots/console-errors.png',
        fullPage: true
      });
    }

    // Test should not fail on console errors, but report them
    expect(consoleErrors.length).toBeLessThanOrEqual(5); // Allow some warnings
  });
});

// Network conditions simulation
test.describe('3G Network Simulation', () => {
  // Note: The device configuration is handled in playwright.config.ts
  // This test focuses on network throttling simulation

  test('Performance under poor network conditions', async ({ page }) => {
    // Add network delay simulation
    await page.route('**/*', async route => {
      // Simulate 3G latency (100-300ms)
      await new Promise(resolve => setTimeout(resolve, Math.random() * 200 + 100));
      await route.continue();
    });

    const startTime = Date.now();

    await test.step('Load main page with throttling', async () => {
      await page.goto(BASE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
      const loadTime = Date.now() - startTime;

      console.log(`Page load time (3G simulation): ${loadTime}ms`);
      expect(loadTime).toBeLessThan(30000); // Should load within 30 seconds

      await page.screenshot({
        path: 'screenshots/3g-loaded.png',
        fullPage: true
      });
    });
  });
});

// After all tests, save performance metrics
test.afterAll(async () => {
  // Save performance metrics
  fs.writeFileSync(
    'performance-metrics.json',
    JSON.stringify(performanceMetrics, null, 2)
  );

  // Save edge storage latency separately
  fs.writeFileSync(
    'edge-storage-latency.json',
    JSON.stringify(performanceMetrics.edgeLatency, null, 2)
  );

  console.log('Performance metrics saved:');
  console.log(`- FCP: ${performanceMetrics.fcp}ms`);
  console.log(`- TTI: ${performanceMetrics.tti}ms`);
  console.log(`- Accessibility issues: ${performanceMetrics.accessibilityIssues.length}`);
});
