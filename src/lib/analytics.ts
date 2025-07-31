// Secure implementation of analytics with cryptographically secure session ID generation

declare const global: any;

export class Analytics {
  private sessionId: string;
  private isEnabled: boolean;

  constructor() {
    this.isEnabled = this.shouldEnableAnalytics();
    this.sessionId = this.generateSecureSessionId();
    this.initializeAnalytics();
  }

  /**
   * Generates a cryptographically secure session ID
   * Uses Web Crypto API in browser or Node.js crypto module
   */
  private generateSecureSessionId(): string {
    // Check if we're in a browser environment
    if (typeof window !== 'undefined' && window.crypto && window.crypto.getRandomValues) {
      // Browser environment - use Web Crypto API
      const array = new Uint8Array(16);
      window.crypto.getRandomValues(array);
      return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    } else if (typeof global !== 'undefined') {
      // Node.js environment - use crypto module
      try {
        // Use dynamic import for Node.js crypto module
        const crypto = eval('require')('crypto');
        return crypto.randomBytes(16).toString('hex');
      } catch (e) {
        // If require is not available, try using globalThis.crypto (Node.js 15+)
        if (globalThis.crypto && typeof globalThis.crypto.getRandomValues === 'function') {
          const array = new Uint8Array(16);
          globalThis.crypto.getRandomValues(array);
          return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
        }
        throw new Error('Cryptographically secure random number generation is not available in this environment');
      }
    } else {
      // Fallback for environments without crypto support
      // This should rarely happen in modern environments
      throw new Error('Cryptographically secure random number generation is not available in this environment');
    }
  }

  /**
   * Legacy method - DO NOT USE
   * @deprecated Use generateSecureSessionId instead
   */
  private generateSessionId(): string {
    console.warn('generateSessionId() is deprecated due to security concerns. Use generateSecureSessionId() instead.');
    return this.generateSecureSessionId();
  }

  private shouldEnableAnalytics(): boolean {
    // Check if analytics should be enabled based on environment or user preferences
    const isProduction = (typeof process !== 'undefined' && process.env?.NODE_ENV === 'production') ||
                        (typeof window !== 'undefined' && window.location?.hostname !== 'localhost');
    return isProduction && !this.isDoNotTrack();
  }

  private isDoNotTrack(): boolean {
    // Respect user's Do Not Track preference
    if (typeof window !== 'undefined' && window.navigator) {
      return window.navigator.doNotTrack === '1' ||
             window.navigator.doNotTrack === 'yes';
    }
    return false;
  }

  private initializeAnalytics(): void {
    if (this.isEnabled) {
      // Initialize your analytics provider here
      console.log('Analytics initialized with secure session ID');
    }
  }

  /**
   * Track an event with the analytics provider
   */
  public trackEvent(eventName: string, properties?: Record<string, any>): void {
    if (!this.isEnabled) return;

    const eventData = {
      event: eventName,
      sessionId: this.sessionId,
      timestamp: new Date().toISOString(),
      ...properties
    };

    // Send to analytics provider
    this.sendToAnalytics(eventData);
  }

  private sendToAnalytics(data: any): void {
    // Implementation depends on your analytics provider
    // Example: Google Analytics, Mixpanel, etc.
    console.log('Analytics event:', data);
  }

  /**
   * Get the current session ID
   */
  public getSessionId(): string {
    return this.sessionId;
  }
}

// Export a singleton instance
export const analytics = new Analytics();
