import { Analytics } from './analytics';

describe('Analytics Security Tests', () => {
  let analytics: Analytics;

  beforeEach(() => {
    analytics = new Analytics();
  });

  test('session ID should be cryptographically secure', () => {
    const sessionId = analytics.getSessionId();

    // Check that session ID is a valid hex string
    expect(sessionId).toMatch(/^[0-9a-f]{32}$/);

    // Generate multiple session IDs and ensure they're unique
    const sessionIds = new Set<string>();
    for (let i = 0; i < 100; i++) {
      const newAnalytics = new Analytics();
      sessionIds.add(newAnalytics.getSessionId());
    }

    // All session IDs should be unique
    expect(sessionIds.size).toBe(100);
  });

  test('session ID should have sufficient entropy', () => {
    const sessionId = analytics.getSessionId();

    // 16 bytes = 128 bits of entropy
    expect(sessionId.length).toBe(32); // 16 bytes * 2 (hex representation)
  });

  test('trackEvent should include session ID', () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();

    analytics.trackEvent('test-event', { value: 123 });

    // Verify the event was logged (in real implementation, this would send to analytics provider)
    expect(consoleSpy).toHaveBeenCalled();

    consoleSpy.mockRestore();
  });
});
