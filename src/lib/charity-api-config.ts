/**
 * CharityAPI Configuration
 *
 * SECURITY NOTE: Never commit API keys to version control!
 * Use environment variables or secure secret management.
 */

export const config = {
  // Mode selection: 'test' for development, 'live' for production
  mode: (process.env.CHARITY_API_MODE || 'test') as 'live' | 'test',

  // API endpoint
  baseUrl: process.env.CHARITY_API_BASE_URL || 'https://api.charityapi.org/api/v1',

  // Rate limiting configuration
  rateLimit: {
    maxRequests: parseInt(process.env.CHARITY_API_RATE_LIMIT || '100'),
    windowMs: parseInt(process.env.CHARITY_API_RATE_WINDOW || '60000') // 1 minute
  },

  // Cache configuration
  cache: {
    enabled: process.env.CHARITY_API_CACHE_ENABLED !== 'false',
    ttl: parseInt(process.env.CHARITY_API_CACHE_TTL || '3600') // 1 hour in seconds
  }
};

// NTEE Code Categories for nonprofit classification
export const NTEE_CATEGORIES = {
  A: 'Arts, Culture & Humanities',
  B: 'Education',
  C: 'Environment',
  D: 'Animal-Related',
  E: 'Health Care',
  F: 'Mental Health & Crisis Intervention',
  G: 'Diseases, Disorders & Medical Disciplines',
  H: 'Medical Research',
  I: 'Crime & Legal-Related',
  J: 'Employment',
  K: 'Food, Agriculture & Nutrition',
  L: 'Housing & Shelter',
  M: 'Public Safety, Disaster Preparedness & Relief',
  N: 'Recreation & Sports',
  O: 'Youth Development',
  P: 'Human Services',
  Q: 'International, Foreign Affairs & National Security',
  R: 'Civil Rights, Social Action & Advocacy',
  S: 'Community Improvement & Capacity Building',
  T: 'Philanthropy, Voluntarism & Grantmaking Foundations',
  U: 'Science & Technology',
  V: 'Social Science',
  W: 'Public & Societal Benefit',
  X: 'Religion-Related',
  Y: 'Mutual & Membership Benefit',
  Z: 'Unknown'
};

// Helper function to get NTEE category name
export function getNTEECategoryName(code: string): string {
  const letter = code.charAt(0).toUpperCase();
  return NTEE_CATEGORIES[letter as keyof typeof NTEE_CATEGORIES] || 'Unknown';
}
