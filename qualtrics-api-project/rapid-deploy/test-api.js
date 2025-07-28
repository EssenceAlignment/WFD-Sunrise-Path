require('dotenv').config();
const axios = require('axios');

const API_TOKEN = process.env.QUALTRICS_API_TOKEN;
const DATACENTER = process.env.QUALTRICS_DATACENTER;
const BASE_URL = `https://${DATACENTER}.qualtrics.com/API/v3`;

async function testConnection() {
  console.log('🔌 Testing Qualtrics API connection...\n');
  console.log(`Data Center: ${DATACENTER}`);
  console.log(`Base URL: ${BASE_URL}`);
  console.log(`API Token: ${API_TOKEN.substring(0, 10)}...`);
  
  try {
    // Test whoami endpoint
    const response = await axios.get(`${BASE_URL}/whoami`, {
      headers: {
        'X-API-TOKEN': API_TOKEN
      }
    });
    
    console.log('\n✅ Connection successful!');
    console.log('User:', response.data.result.userName);
    console.log('Brand:', response.data.result.brandId);
    console.log('Account Type:', response.data.result.accountType);
    
    // List existing surveys
    const surveysResponse = await axios.get(`${BASE_URL}/surveys`, {
      headers: {
        'X-API-TOKEN': API_TOKEN
      }
    });
    
    console.log(`\n📋 You have ${surveysResponse.data.result.elements.length} surveys in your account`);
    
    return true;
  } catch (error) {
    console.error('\n❌ Connection failed!');
    console.error('Error:', error.response?.data || error.message);
    console.error('\nPlease check:');
    console.error('1. Your API token is correct');
    console.error('2. Your datacenter is correct');
    console.error('3. You have API access enabled');
    return false;
  }
}

// Run the test
testConnection().then(success => {
  if (success) {
    console.log('\n🚀 Ready to create survey!');
  } else {
    console.log('\n⚠️  Fix connection issues before proceeding');
  }
});
