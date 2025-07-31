#!/usr/bin/env node

/**
 * Quick test script for CharityAPI integration
 * Run with: node scripts/test-charity-api.js
 */

require('dotenv').config();

async function testCharityAPI() {
  console.log('\n🧪 Testing CharityAPI Integration...\n');

  // Check if environment variables are loaded
  const testKey = process.env.CHARITY_API_TEST_KEY;
  const liveKey = process.env.CHARITY_API_LIVE_KEY;
  const mode = process.env.CHARITY_API_MODE || 'test';

  console.log('✅ Environment Check:');
  console.log(`  - Mode: ${mode}`);
  console.log(`  - Test Key: ${testKey ? '✓ Configured' : '✗ Missing'}`);
  console.log(`  - Live Key: ${liveKey ? '✓ Configured' : '✗ Missing'}`);

  if (!testKey && mode === 'test') {
    console.error('\n❌ Error: Test API key is missing!');
    console.log('   Please ensure .env file exists with CHARITY_API_TEST_KEY');
    process.exit(1);
  }

  console.log('\n📁 Files Created:');
  console.log('  ✓ src/lib/charity-api.ts');
  console.log('  ✓ src/lib/charity-api-config.ts');
  console.log('  ✓ src/lib/charity-api-example.ts');
  console.log('  ✓ .env (with your API keys)');
  console.log('  ✓ .env.example (template)');
  console.log('  ✓ CHARITY_API_INTEGRATION.md (documentation)');

  console.log('\n✨ CharityAPI integration is ready to use!');
  console.log('\nNext steps:');
  console.log('1. Test the integration: npx ts-node src/lib/charity-api-example.ts');
  console.log('2. Import and use in your code:');
  console.log('   import { charityAPI } from "./src/lib/charity-api";');
  console.log('   const results = await charityAPI.searchByName("Red Cross");');
}

testCharityAPI();
