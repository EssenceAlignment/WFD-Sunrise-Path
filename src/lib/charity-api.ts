/**
 * CharityAPI.org Integration Module
 *
 * This module provides a secure interface to the CharityAPI.org service
 * for nonprofit and charity data access.
 */

import { config } from './charity-api-config';

export interface CharityAPIConfig {
  mode?: 'live' | 'test';
  liveKey?: string;
  testKey?: string;
  baseUrl?: string;
}

export interface CharitySearchParams {
  ein?: string;
  name?: string;
  city?: string;
  state?: string;
  zip?: string;
  category?: string;
  limit?: number;
  offset?: number;
}

export interface CharityData {
  ein: string;
  name: string;
  city: string;
  state: string;
  zip: string;
  category: string;
  classification: string;
  deductibility: string;
  foundation: string;
  activity: string;
  organization: string;
  status: string;
  tax_period?: string;
  asset_amount?: number;
  income_amount?: number;
  revenue_amount?: number;
  ntee_code?: string;
  sort_name?: string;
  ruling_date?: string;
}

export class CharityAPI {
  private apiKey: string;
  private baseUrl: string;
  private mode: 'live' | 'test';
  private useProxy: boolean;

  constructor(config: CharityAPIConfig = {}) {
    this.mode = config.mode || 'test';
    this.useProxy = process.env.USE_API_PROXY === 'true';

    // Use proxy if enabled, otherwise direct API
    if (this.useProxy) {
      this.baseUrl = config.baseUrl || process.env.API_PROXY_URL || 'http://localhost:8088/api/v1';
    } else {
      this.baseUrl = config.baseUrl || 'https://api.charityapi.org/api/v1';
    }

    // Use environment variables or provided config
    const liveKey = config.liveKey || process.env.CHARITY_API_LIVE_KEY;
    const testKey = config.testKey || process.env.CHARITY_API_TEST_KEY;

    if (this.mode === 'live' && !liveKey) {
      throw new Error('Live API key is required for live mode');
    }

    if (this.mode === 'test' && !testKey) {
      throw new Error('Test API key is required for test mode');
    }

    this.apiKey = this.mode === 'live' ? liveKey! : testKey!;
  }

  /**
   * Search for charities based on various parameters
   */
  async searchCharities(params: CharitySearchParams): Promise<CharityData[]> {
    const queryParams = new URLSearchParams();

    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        queryParams.append(key, value.toString());
      }
    });

    const response = await this.makeRequest(`/charities?${queryParams.toString()}`);
    return response.data || [];
  }

  /**
   * Get detailed information about a specific charity by EIN
   */
  async getCharityByEIN(ein: string): Promise<CharityData | null> {
    const response = await this.makeRequest(`/charities/${ein}`);
    return response.data || null;
  }

  /**
   * Search charities by name with fuzzy matching
   */
  async searchByName(name: string, limit: number = 10): Promise<CharityData[]> {
    return this.searchCharities({ name, limit });
  }

  /**
   * Search charities by location
   */
  async searchByLocation(state: string, city?: string, limit: number = 20): Promise<CharityData[]> {
    return this.searchCharities({ state, city, limit });
  }

  /**
   * Get charities by NTEE category code
   */
  async searchByCategory(category: string, limit: number = 20): Promise<CharityData[]> {
    return this.searchCharities({ category, limit });
  }

  /**
   * Make an authenticated request to the CharityAPI
   */
  private async makeRequest(endpoint: string): Promise<any> {
    const url = this.useProxy
      ? `${this.baseUrl}${endpoint}`
      : `${this.baseUrl}${endpoint}`;

    try {
      const headers: HeadersInit = {
        'X-API-Key': this.apiKey,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      };

      // Add proxy-specific headers
      if (this.useProxy) {
        headers['Host'] = 'api.charityapi.org';
        headers['X-API-Mode'] = this.mode;
      }

      const response = await fetch(url, {
        method: 'GET',
        headers
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`CharityAPI Error: ${response.status} - ${errorData.message || response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`CharityAPI Request Failed: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Get the current mode (live or test)
   */
  getMode(): string {
    return this.mode;
  }

  /**
   * Verify API key is valid by making a test request
   */
  async verifyConnection(): Promise<boolean> {
    try {
      await this.searchCharities({ limit: 1 });
      return true;
    } catch (error) {
      return false;
    }
  }
}

// Export a default instance for convenience
export const charityAPI = new CharityAPI();
