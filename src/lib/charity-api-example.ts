/**
 * CharityAPI Usage Examples
 *
 * This file demonstrates how to use the CharityAPI integration
 * with your API keys from CharityAPI.org
 */

import { CharityAPI, charityAPI } from './charity-api';
import { getNTEECategoryName } from './charity-api-config';

// Example 1: Using the default instance with environment variables
async function example1() {
  console.log('Example 1: Using default instance with environment variables');

  try {
    // Verify connection
    const isConnected = await charityAPI.verifyConnection();
    console.log(`Connection status: ${isConnected ? 'Connected' : 'Failed'}`);
    console.log(`Running in ${charityAPI.getMode()} mode`);

    // Search for charities by name
    const results = await charityAPI.searchByName('Red Cross', 5);
    console.log(`Found ${results.length} charities matching "Red Cross"`);

    results.forEach((charity) => {
      console.log(`- ${charity.name} (EIN: ${charity.ein})`);
      console.log(`  Location: ${charity.city}, ${charity.state}`);
      if (charity.ntee_code) {
        console.log(`  Category: ${getNTEECategoryName(charity.ntee_code)}`);
      }
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

// Example 2: Creating a custom instance with specific keys
async function example2() {
  console.log('\nExample 2: Using custom instance with specific configuration');

  // Initialize with your actual keys
  const customAPI = new CharityAPI({
    mode: 'test',
    testKey: 'test-CeMOaeDu107jMOtKME8jlc1GadyxH3sO4m8Lgq3BbPLMXY-vm4O_jEosKEPN9b110vymlykGlriBygXS'
  });

  try {
    // Get a specific charity by EIN
    const charity = await customAPI.getCharityByEIN('131837418'); // Example: American Red Cross
    if (charity) {
      console.log(`Found: ${charity.name}`);
      console.log(`Classification: ${charity.classification}`);
      console.log(`Deductibility: ${charity.deductibility}`);
      console.log(`Status: ${charity.status}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Example 3: Search by location
async function example3() {
  console.log('\nExample 3: Search charities by location');

  try {
    // Search for charities in California
    const californiaCharities = await charityAPI.searchByLocation('CA', 'San Francisco', 10);
    console.log(`Found ${californiaCharities.length} charities in San Francisco, CA`);

    californiaCharities.forEach((charity) => {
      console.log(`- ${charity.name}`);
      console.log(`  Address: ${charity.city}, ${charity.state} ${charity.zip}`);
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

// Example 4: Search by NTEE category
async function example4() {
  console.log('\nExample 4: Search charities by category');

  try {
    // Search for health care charities (NTEE code E)
    const healthCharities = await charityAPI.searchByCategory('E', 15);
    console.log(`Found ${healthCharities.length} health care charities`);

    healthCharities.forEach((charity) => {
      console.log(`- ${charity.name} (${charity.city}, ${charity.state})`);
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

// Example 5: Advanced search with multiple parameters
async function example5() {
  console.log('\nExample 5: Advanced search with multiple parameters');

  try {
    const searchParams = {
      state: 'NY',
      category: 'P', // Human Services
      limit: 20,
      offset: 0
    };

    const results = await charityAPI.searchCharities(searchParams);
    console.log(`Found ${results.length} human services charities in New York`);

    // Display summary statistics
    const cities = new Set(results.map((c) => c.city));
    console.log(`Across ${cities.size} different cities`);
  } catch (error) {
    console.error('Error:', error);
  }
}

// Run examples
async function runExamples() {
  // Uncomment the examples you want to run
  // await example1();
  // await example2();
  // await example3();
  // await example4();
  // await example5();

  console.log('\nTo run these examples:');
  console.log('1. Copy .env.example to .env');
  console.log('2. Add your CharityAPI keys to .env');
  console.log('3. Uncomment the examples you want to run in runExamples()');
  console.log('4. Run: npx ts-node src/lib/charity-api-example.ts');
}

// Run the examples
runExamples();
