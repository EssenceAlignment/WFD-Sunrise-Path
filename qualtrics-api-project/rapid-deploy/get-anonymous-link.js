require('dotenv').config();
const axios = require('axios');
const fs = require('fs').promises;

const API_TOKEN = process.env.QUALTRICS_API_TOKEN;
const DATACENTER = process.env.QUALTRICS_DATACENTER;
const BASE_URL = `https://${DATACENTER}.qualtrics.com/API/v3`;

async function getAnonymousLink() {
  try {
    // Read survey ID from file or command line
    let surveyId;
    if (process.argv[2]) {
      surveyId = process.argv[2];
    } else {
      try {
        surveyId = await fs.readFile('survey-id.txt', 'utf8');
        surveyId = surveyId.trim();
      } catch (error) {
        console.error('❌ No survey ID found. Run create-wfd-survey.js first or provide survey ID as argument.');
        process.exit(1);
      }
    }
    
    console.log(`🔗 Getting anonymous link for survey: ${surveyId}\n`);
    
    // Step 1: Create a distribution
    console.log('Creating distribution...');
    const distributionResponse = await axios.post(
      `${BASE_URL}/distributions`,
      {
        surveyId: surveyId,
        linkType: "Anonymous",
        description: "WFD Manager Assessment - Anonymous Link",
        action: "CreateDistribution",
        expirationDate: "2025-12-31 00:00:00",
        header: {
          fromEmail: "noreply@qemailserver.com",
          fromName: "WFD Survey",
          subject: "Manager Readiness Assessment"
        }
      },
      {
        headers: {
          'X-API-TOKEN': API_TOKEN,
          'Content-Type': 'application/json'
        }
      }
    );
    
    const distributionId = distributionResponse.data.result.id;
    console.log(`✅ Distribution created: ${distributionId}`);
    
    // Step 2: Get the anonymous link
    console.log('\nRetrieving anonymous link...');
    const linksResponse = await axios.get(
      `${BASE_URL}/distributions/${distributionId}/links`,
      {
        headers: { 'X-API-TOKEN': API_TOKEN }
      }
    );
    
    const anonymousLink = linksResponse.data.result.elements[0].link;
    
    // Save the link to a file
    await fs.writeFile('anonymous-link.txt', anonymousLink);
    
    console.log('\n' + '='.repeat(60));
    console.log('🎉 SUCCESS! Anonymous survey link:');
    console.log('='.repeat(60));
    console.log(`\n${anonymousLink}\n`);
    console.log('='.repeat(60));
    console.log('\n✅ Link saved to: anonymous-link.txt');
    console.log('📧 Add this link to your email to Donna!');
    
    // Also create a formatted email snippet
    const emailSnippet = `
**1. Manager Assessment Survey (LIVE NOW)**  
The manager assessment is now live at ${anonymousLink}. As you requested, it uses the validated ORIC-12 instrument plus additional questions about current data practices. Skip logic ensures Community Services managers don't see Interim Housing questions and vice versa. All responses feed directly into the dashboard for real-time readiness tracking.
`;
    
    await fs.writeFile('email-snippet.txt', emailSnippet);
    console.log('\n📝 Email snippet saved to: email-snippet.txt');
    
    return anonymousLink;
    
  } catch (error) {
    console.error('\n❌ Error getting anonymous link:', error.response?.data || error.message);
    
    if (error.response?.status === 404) {
      console.error('\n⚠️  Survey not found. Make sure the survey exists and is activated.');
    }
    
    throw error;
  }
}

// Execute
getAnonymousLink().catch(error => {
  console.error('\n💥 Failed to get link:', error);
  process.exit(1);
});
