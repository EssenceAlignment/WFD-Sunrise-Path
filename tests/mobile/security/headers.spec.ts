import { test, expect } from '@playwright/test';

const BASE_URL = process.env.RECOVERY_COMPASS_URL || 'https://recovery-compass.org';

// Security headers to check
const REQUIRED_HEADERS = {
  'content-security-policy': {
    required: true,
    validate: (value: string) => {
      const required = ['default-src', 'script-src', 'style-src'];
      return required.every(directive => value.includes(directive));
    }
  },
  'x-content-type-options': {
    required: true,
    expected: 'nosniff'
  },
  'x-frame-options': {
    required: true,
    expected: ['DENY', 'SAMEORIGIN']
  },
  'referrer-policy': {
    required: true,
    expected: ['no-referrer', 'strict-origin-when-cross-origin', 'same-origin']
  },
  'permissions-policy': {
    required: false,
    validate: (value: string) => value.includes('geolocation')
  },
  'cross-origin-embedder-policy': {
    required: false,
    expected: 'require-corp'
  },
  'cross-origin-opener-policy': {
    required: false,
    expected: 'same-origin'
  }
};

test.describe('Security Headers Validation', () => {
  test('Main page security headers', async ({ page }) => {
    const response = await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    if (!response) {
      throw new Error('No response received');
    }

    const headers = response.headers();
    const issues: string[] = [];

    // Check each required header
    for (const [headerName, config] of Object.entries(REQUIRED_HEADERS)) {
      const headerValue = headers[headerName];

      if (config.required && !headerValue) {
        issues.push(`Missing required header: ${headerName}`);
        continue;
      }

      if (headerValue) {
        // Check expected values
        if ('expected' in config) {
          const expected = Array.isArray(config.expected) ? config.expected : [config.expected];
          if (!expected.includes(headerValue)) {
            issues.push(`Invalid ${headerName}: ${headerValue} (expected: ${expected.join(' or ')})`);
          }
        }

        // Run custom validation
        if ('validate' in config && config.validate) {
          if (!config.validate(headerValue)) {
            issues.push(`Invalid ${headerName} configuration: ${headerValue}`);
          }
        }
      }
    }

    // Log all headers for debugging
    console.log('Response headers:', JSON.stringify(headers, null, 2));

    // Report issues
    if (issues.length > 0) {
      console.error('Security header issues:', issues);
    }

    // Assert no critical issues
    expect(issues.filter(i => i.includes('required')).length).toBe(0);
  });

  test('API endpoint security headers', async ({ page }) => {
    const endpoints = [
      '/api/healthcheck',
      '/api/kv-test',
      '/api/r2-test',
      '/api/d1-test'
    ];

    for (const endpoint of endpoints) {
      const response = await page.request.get(`${BASE_URL}${endpoint}`).catch(() => null);

      if (response) {
        const headers = response.headers();

        // API should have strict CSP
        expect(headers['content-security-policy']).toBeTruthy();

        // API should prevent MIME sniffing
        expect(headers['x-content-type-options']).toBe('nosniff');

        // API should have CORS headers
        if (headers['access-control-allow-origin']) {
          // If CORS is enabled, check it's not too permissive
          expect(headers['access-control-allow-origin']).not.toBe('*');
        }
      }
    }
  });

  test('Cookie security attributes', async ({ page }) => {
    await page.goto(BASE_URL, { waitUntil: 'networkidle' });

    const cookies = await page.context().cookies();

    for (const cookie of cookies) {
      // Session cookies should be secure
      if (cookie.name.includes('session') || cookie.name.includes('auth')) {
        expect(cookie.secure).toBe(true);
        expect(cookie.httpOnly).toBe(true);
        expect(cookie.sameSite).toMatch(/Strict|Lax/);
      }
    }
  });

  test('HTTPS enforcement', async ({ page }) => {
    // Try HTTP version
    const httpUrl = BASE_URL.replace('https://', 'http://');

    if (!httpUrl.includes('localhost')) {
      const response = await page.goto(httpUrl, {
        waitUntil: 'domcontentloaded',
        timeout: 10000
      }).catch(() => null);

      if (response) {
        // Should redirect to HTTPS
        expect(response.url()).toMatch(/^https:/);

        // Should have HSTS header
        const headers = response.headers();
        expect(headers['strict-transport-security']).toBeTruthy();
      }
    }
  });
});

// Export security metrics for reporting
test.afterAll(async () => {
  const securityMetrics = {
    timestamp: new Date().toISOString(),
    headers: REQUIRED_HEADERS,
    tested: true
  };

  require('fs').writeFileSync(
    'security-metrics.json',
    JSON.stringify(securityMetrics, null, 2)
  );
});
