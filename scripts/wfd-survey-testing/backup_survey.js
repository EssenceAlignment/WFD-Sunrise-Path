#!/usr/bin/env node
/**
 * WFD Survey Backup Documentation Script
 * Creates local backup of working survey implementation
 */

const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

const BACKUP_DIR = path.join(process.env.HOME, 'Documents/WFD_Survey_Backup');
const TIMESTAMP = new Date().toISOString().replace(/[:.]/g, '-');

/**
 * Create backup directory structure
 */
async function setupBackupDirectory() {
  const dirs = [
    BACKUP_DIR,
    path.join(BACKUP_DIR, TIMESTAMP),
    path.join(BACKUP_DIR, TIMESTAMP, 'html'),
    path.join(BACKUP_DIR, TIMESTAMP, 'screenshots'),
    path.join(BACKUP_DIR, TIMESTAMP, 'api'),
    path.join(BACKUP_DIR, TIMESTAMP, 'form-fields')
  ];

  for (const dir of dirs) {
    await fs.mkdir(dir, { recursive: true });
  }

  console.log(`✅ Backup directory created: ${path.join(BACKUP_DIR, TIMESTAMP)}`);
  return path.join(BACKUP_DIR, TIMESTAMP);
}

/**
 * Capture survey HTML and assets
 */
async function captureSurveyHTML(page, backupPath) {
  console.log('📄 Capturing survey HTML...');

  // Get full page HTML
  const html = await page.content();
  await fs.writeFile(
    path.join(backupPath, 'html', 'survey-full.html'),
    html
  );

  // Get all form field names and IDs
  const formFields = await page.evaluate(() => {
    const fields = [];
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
      fields.push({
        type: input.type || input.tagName.toLowerCase(),
        name: input.name,
        id: input.id,
        placeholder: input.placeholder,
        required: input.required,
        value: input.value
      });
    });
    return fields;
  });

  await fs.writeFile(
    path.join(backupPath, 'form-fields', 'all-fields.json'),
    JSON.stringify(formFields, null, 2)
  );

  console.log(`✅ Captured ${formFields.length} form fields`);
}

/**
 * Capture screenshots of each section
 */
async function captureScreenshots(page, backupPath) {
  console.log('📸 Capturing screenshots...');

  // Full page screenshot
  await page.screenshot({
    path: path.join(backupPath, 'screenshots', '00-full-page.png'),
    fullPage: true
  });

  // Viewport screenshot
  await page.screenshot({
    path: path.join(backupPath, 'screenshots', '01-viewport.png')
  });

  // Try to capture each section if possible
  const sections = await page.locator('[data-section], .section, [class*="section"]').all();

  for (let i = 0; i < sections.length && i < 10; i++) {
    try {
      await sections[i].screenshot({
        path: path.join(backupPath, 'screenshots', `section-${i + 1}.png`)
      });
    } catch (e) {
      // Section might not be visible
    }
  }

  console.log('✅ Screenshots captured');
}

/**
 * Extract API endpoints and network requests
 */
async function captureNetworkData(page, backupPath) {
  console.log('🌐 Capturing network data...');

  const networkData = {
    apis: [],
    resources: [],
    formActions: []
  };

  // Monitor network requests
  page.on('request', request => {
    const url = request.url();
    const type = request.resourceType();

    if (type === 'xhr' || type === 'fetch') {
      networkData.apis.push({
        url,
        method: request.method(),
        headers: request.headers()
      });
    }

    if (type === 'document' || type === 'script' || type === 'stylesheet') {
      networkData.resources.push({
        url,
        type
      });
    }
  });

  // Check form actions
  const formActions = await page.evaluate(() => {
    const forms = document.querySelectorAll('form');
    return Array.from(forms).map(form => ({
      action: form.action,
      method: form.method,
      id: form.id
    }));
  });

  networkData.formActions = formActions;

  await fs.writeFile(
    path.join(backupPath, 'api', 'network-data.json'),
    JSON.stringify(networkData, null, 2)
  );

  console.log('✅ Network data captured');
}

/**
 * Create comprehensive survey documentation
 */
async function createDocumentation(backupPath) {
  console.log('📝 Creating documentation...');

  const documentation = `# WFD Survey Backup Documentation

**Backup Date**: ${new Date().toLocaleString()}
**Location**: ${backupPath}

## Contents

### HTML Files
- \`html/survey-full.html\` - Complete HTML snapshot of the survey

### Screenshots
- \`screenshots/00-full-page.png\` - Full page capture
- \`screenshots/01-viewport.png\` - Viewport capture
- \`screenshots/section-*.png\` - Individual section captures

### Form Data
- \`form-fields/all-fields.json\` - All form field metadata

### API/Network
- \`api/network-data.json\` - Captured API endpoints and resources

## Survey Structure

Based on the captured data, the survey contains:
- Multiple sections with form inputs
- Progress tracking functionality
- Email submission capability

## Restoration Instructions

1. To view the static HTML:
   \`\`\`bash
   open html/survey-full.html
   \`\`\`

2. To analyze form structure:
   \`\`\`bash
   cat form-fields/all-fields.json | jq .
   \`\`\`

3. To review API endpoints:
   \`\`\`bash
   cat api/network-data.json | jq .
   \`\`\`

## Important Notes

- This is a static backup and may not include dynamic functionality
- JavaScript interactions are preserved in the HTML but may not work offline
- Form submissions will not work without the backend server
- Use this backup for reference and disaster recovery only
`;

  await fs.writeFile(
    path.join(backupPath, 'README.md'),
    documentation
  );

  console.log('✅ Documentation created');
}

/**
 * Main backup function
 */
async function backupSurvey() {
  console.log('🔄 Starting WFD Survey Backup...\n');

  const browser = await chromium.launch({
    headless: false, // Show browser for verification
    viewport: { width: 1280, height: 800 }
  });

  try {
    const page = await browser.newPage();
    const backupPath = await setupBackupDirectory();

    // Navigate to survey
    console.log('🌐 Loading survey...');
    await page.goto('https://wfd-sunrise-path.lovable.app/survey', {
      waitUntil: 'networkidle'
    });

    // Wait for content to load
    await page.waitForTimeout(3000);

    // Perform backup tasks
    await captureSurveyHTML(page, backupPath);
    await captureScreenshots(page, backupPath);
    await captureNetworkData(page, backupPath);
    await createDocumentation(backupPath);

    console.log('\n✅ Backup completed successfully!');
    console.log(`📁 Location: ${backupPath}`);

    // Create latest symlink
    const latestLink = path.join(BACKUP_DIR, 'latest');
    try {
      await fs.unlink(latestLink);
    } catch (e) {
      // Link might not exist
    }
    await fs.symlink(backupPath, latestLink);

  } catch (error) {
    console.error('❌ Backup failed:', error);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

// Run backup
if (require.main === module) {
  backupSurvey();
}

module.exports = { backupSurvey };
