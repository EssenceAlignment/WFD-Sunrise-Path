# CharityAPI.org Integration

This project now includes integration with CharityAPI.org, a comprehensive API service for accessing nonprofit and charity data.

## Setup

### 1. API Keys

Your API keys have been successfully configured:
- **Live Key**: `live-x4InGyvRE4A0pZw5CgRnibVPtSpuyZIGd-...` (truncated for security)
- **Test Key**: `test-CeMOaeDu107jMOtKME8jlc1GadyxH3sO4m8L...` (truncated for security)
- **Email**: eric@recovery-compass.org

These keys are stored in `.env` file which is excluded from version control for security.

### 2. Configuration

The integration is configured to use **test mode** by default. To switch to live mode:

```bash
# Edit .env file
CHARITY_API_MODE=live
```

## File Structure

```
src/lib/
├── charity-api.ts          # Main API client implementation
├── charity-api-config.ts   # Configuration and constants
└── charity-api-example.ts  # Usage examples
```

## Usage

### Basic Usage

```typescript
import { charityAPI } from './src/lib/charity-api';

// Search for charities by name
const results = await charityAPI.searchByName('Red Cross');

// Get charity by EIN
const charity = await charityAPI.getCharityByEIN('131837418');

// Search by location
const localCharities = await charityAPI.searchByLocation('CA', 'San Francisco');

// Search by category (NTEE code)
const healthCharities = await charityAPI.searchByCategory('E'); // E = Health Care
```

### Advanced Usage

```typescript
import { CharityAPI } from './src/lib/charity-api';

// Create custom instance
const api = new CharityAPI({
  mode: 'test',
  testKey: process.env.CHARITY_API_TEST_KEY
});

// Advanced search with multiple parameters
const results = await api.searchCharities({
  state: 'NY',
  category: 'P', // Human Services
  limit: 50,
  offset: 0
});
```

## API Features

### Search Methods
- `searchCharities(params)` - Advanced search with multiple parameters
- `getCharityByEIN(ein)` - Get specific charity details
- `searchByName(name, limit)` - Search by charity name
- `searchByLocation(state, city, limit)` - Search by location
- `searchByCategory(nteeCode, limit)` - Search by NTEE category

### Data Structure

Each charity record includes:
- `ein` - Employer Identification Number
- `name` - Organization name
- `city`, `state`, `zip` - Location information
- `category` - NTEE category
- `classification` - Tax classification
- `deductibility` - Deductibility status
- `status` - Current status
- `ntee_code` - Full NTEE classification code
- Financial data (when available): `asset_amount`, `income_amount`, `revenue_amount`

### NTEE Categories

The API uses NTEE (National Taxonomy of Exempt Entities) codes:

- A: Arts, Culture & Humanities
- B: Education
- C: Environment
- D: Animal-Related
- E: Health Care
- F: Mental Health & Crisis Intervention
- G: Diseases, Disorders & Medical Disciplines
- H: Medical Research
- I: Crime & Legal-Related
- J: Employment
- K: Food, Agriculture & Nutrition
- L: Housing & Shelter
- M: Public Safety, Disaster Preparedness & Relief
- N: Recreation & Sports
- O: Youth Development
- P: Human Services
- Q: International, Foreign Affairs & National Security
- R: Civil Rights, Social Action & Advocacy
- S: Community Improvement & Capacity Building
- T: Philanthropy, Voluntarism & Grantmaking Foundations
- U: Science & Technology
- V: Social Science
- W: Public & Societal Benefit
- X: Religion-Related
- Y: Mutual & Membership Benefit
- Z: Unknown

## Testing the Integration

Run the example file to test your setup:

```bash
# Install dependencies if needed
npm install

# Run the examples
npx ts-node src/lib/charity-api-example.ts
```

## Security Best Practices

1. **Never commit API keys** - The `.env` file is gitignored
2. **Use test mode for development** - Only use live mode in production
3. **Rotate keys regularly** - Contact CharityAPI.org for key rotation
4. **Monitor usage** - Track API calls to avoid hitting rate limits

## Rate Limiting

Default rate limits:
- 100 requests per minute
- Configurable via environment variables

```bash
CHARITY_API_RATE_LIMIT=100
CHARITY_API_RATE_WINDOW=60000  # milliseconds
```

## Error Handling

The API client includes comprehensive error handling:

```typescript
try {
  const results = await charityAPI.searchByName('charity name');
} catch (error) {
  console.error('CharityAPI Error:', error.message);
}
```

## Environment Variables

Complete list of supported environment variables:

```bash
CHARITY_API_LIVE_KEY      # Live API key
CHARITY_API_TEST_KEY      # Test API key
CHARITY_API_MODE          # 'test' or 'live'
CHARITY_API_BASE_URL      # API endpoint (optional)
CHARITY_API_RATE_LIMIT    # Max requests per window
CHARITY_API_RATE_WINDOW   # Rate limit window in ms
CHARITY_API_CACHE_ENABLED # Enable/disable caching
CHARITY_API_CACHE_TTL     # Cache time-to-live in seconds
```

## Support

- **API Documentation**: https://charityapi.org/docs
- **Support Email**: support@charityapi.org
- **Your Account Email**: eric@recovery-compass.org

## Next Steps

1. Test the integration using the example file
2. Implement charity search features in your application
3. Consider implementing caching for frequently accessed data
4. Monitor API usage and upgrade plan if needed

Remember to keep your API keys secure and never share them publicly!
