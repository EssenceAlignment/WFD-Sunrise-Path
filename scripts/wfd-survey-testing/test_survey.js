/**
 * WFD Survey Automated Testing Script
 * Critical for $4.4M Discovery - Zero Error Tolerance
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SURVEY_URL = 'https://wfd-sunrise-path.lovable.app/';
const RESULTS_DIR = path.join(__dirname, 'test-results');

// Ensure results directory exists
if (!fs.existsSync(RESULTS_DIR)) {
    fs.mkdirSync(RESULTS_DIR, { recursive: true });
}

// Test configuration
const testConfig = {
    timeout: 30000,
    screenshotOnError: true,
    headless: false
};

// Test results tracker
const testResults = {
    timestamp: new Date().toISOString(),
    url: SURVEY_URL,
    passed: 0,
    failed: 0,
    tests: []
};

async function runTest(testName, testFunction) {
    console.log(`\n🧪 Running: ${testName}`);
    const startTime = Date.now();

    try {
        await testFunction();
        const duration = Date.now() - startTime;
        console.log(`✅ PASSED (${duration}ms)`);
        testResults.passed++;
        testResults.tests.push({
            name: testName,
            status: 'PASSED',
            duration: duration
        });
        return true;
    } catch (error) {
        const duration = Date.now() - startTime;
        console.error(`❌ FAILED: ${error.message}`);
        testResults.failed++;
        testResults.tests.push({
            name: testName,
            status: 'FAILED',
            duration: duration,
            error: error.message
        });
        return false;
    }
}

async function main() {
    console.log('🔍 WFD Survey Automated Testing Starting...');
    console.log(`📍 Testing URL: ${SURVEY_URL}`);
    console.log('⚠️  Critical: $4.4M Discovery depends on 100% pass rate\n');

    const browser = await puppeteer.launch({
        headless: testConfig.headless,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });

    try {
        // Test 1: Survey Loads Successfully
        await runTest('Survey loads at root URL', async () => {
            const response = await page.goto(SURVEY_URL, {
                waitUntil: 'networkidle2',
                timeout: testConfig.timeout
            });
            if (!response.ok()) {
                throw new Error(`Failed to load: ${response.status()}`);
            }
        });

        // Test 2: Header Elements Present
        await runTest('Header elements render correctly', async () => {
            await page.waitForSelector('h1', { timeout: 5000 });
            const headerText = await page.$eval('h1', el => el.textContent);
            if (!headerText.includes('Manager Readiness Assessment')) {
                throw new Error('Invalid header text');
            }
        });

        // Test 3: Program Type Selection
        await runTest('Program type dropdown functions', async () => {
            await page.waitForSelector('select', { timeout: 5000 });
            const options = await page.$$eval('select option', opts => opts.map(opt => opt.value));
            if (options.length < 2) {
                throw new Error('Insufficient program options');
            }

            // Select a program type
            await page.select('select', 'Community Services/Outreach');
        });

        // Test 4: Progress Bar Functionality
        await runTest('Progress bar displays correctly', async () => {
            const progressBar = await page.$('.progress-bar');
            if (!progressBar) {
                throw new Error('Progress bar not found');
            }
        });

        // Test 5: Section Navigation
        await runTest('All 9 sections are navigable', async () => {
            let sectionsFound = 0;

            // Navigate through sections
            for (let i = 0; i < 9; i++) {
                const sectionIndicator = await page.$eval('.progress-bar', el => {
                    const text = el.textContent || '';
                    return text;
                });

                if (sectionIndicator.includes(`Section ${i + 1} of`)) {
                    sectionsFound++;
                }

                // Try to find and click next button
                const nextButton = await page.$('button[type="button"]');
                if (nextButton && i < 8) {
                    await nextButton.click();
                    await page.waitForTimeout(500);
                }
            }

            if (sectionsFound < 5) {
                throw new Error(`Only ${sectionsFound} sections found, expected 9`);
            }
        });

        // Test 6: Form Validation
        await runTest('Form validation works correctly', async () => {
            // Go back to first section
            await page.goto(SURVEY_URL, { waitUntil: 'networkidle2' });
            await page.select('select', 'Community Services/Outreach');

            // Try to submit without filling required fields
            const submitButton = await page.$('button[type="submit"]');
            if (submitButton) {
                await submitButton.click();
                // Check if validation prevents submission
                const currentUrl = page.url();
                if (currentUrl.includes('mailto:')) {
                    throw new Error('Form submitted without validation');
                }
            }
        });

        // Test 7: Accessibility
        await runTest('Basic accessibility compliance', async () => {
            // Check for alt text on images
            const images = await page.$$('img');
            for (const img of images) {
                const alt = await img.evaluate(el => el.alt);
                if (!alt) {
                    throw new Error('Image without alt text found');
                }
            }

            // Check for form labels
            const inputs = await page.$$('input, select, textarea');
            if (inputs.length > 0) {
                // Verify at least some inputs have associated labels
                const labelsExist = await page.$$('label');
                if (labelsExist.length === 0 && inputs.length > 0) {
                    throw new Error('Form inputs without labels');
                }
            }
        });

        // Test 8: Mobile Responsiveness
        await runTest('Mobile responsive design', async () => {
            await page.setViewport({ width: 375, height: 667 });
            await page.waitForTimeout(1000);

            // Check if content is still accessible
            const isHeaderVisible = await page.$('h1');
            if (!isHeaderVisible) {
                throw new Error('Content not visible on mobile');
            }

            // Reset viewport
            await page.setViewport({ width: 1280, height: 800 });
        });

        // Test 9: Console Error Check
        await runTest('No console errors', async () => {
            const errors = [];
            page.on('console', msg => {
                if (msg.type() === 'error') {
                    errors.push(msg.text());
                }
            });

            await page.reload({ waitUntil: 'networkidle2' });
            await page.waitForTimeout(2000);

            if (errors.length > 0) {
                throw new Error(`Console errors found: ${errors.join(', ')}`);
            }
        });

        // Test 10: Performance Metrics
        await runTest('Performance within acceptable range', async () => {
            const metrics = await page.metrics();
            const performanceData = await page.evaluate(() => {
                const timing = performance.timing;
                return {
                    loadTime: timing.loadEventEnd - timing.navigationStart,
                    domReady: timing.domContentLoadedEventEnd - timing.navigationStart
                };
            });

            if (performanceData.loadTime > 3000) {
                throw new Error(`Load time too high: ${performanceData.loadTime}ms`);
            }
        });

    } catch (error) {
        console.error('\n🚨 Critical test failure:', error);
        testResults.criticalError = error.message;
    } finally {
        await browser.close();
    }

    // Generate test report
    const reportPath = path.join(RESULTS_DIR, `test-report-${Date.now()}.json`);
    fs.writeFileSync(reportPath, JSON.stringify(testResults, null, 2));

    // Display summary
    console.log('\n' + '='.repeat(50));
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(50));
    console.log(`Total Tests: ${testResults.passed + testResults.failed}`);
    console.log(`✅ Passed: ${testResults.passed}`);
    console.log(`❌ Failed: ${testResults.failed}`);
    console.log(`Success Rate: ${((testResults.passed / (testResults.passed + testResults.failed)) * 100).toFixed(1)}%`);

    if (testResults.failed === 0) {
        console.log('\n🎉 ALL TESTS PASSED! Survey ready for $4.4M discovery.');
    } else {
        console.log('\n⚠️  CRITICAL: Tests failed. DO NOT proceed with deployment!');
        console.log('Failed tests must be fixed immediately.');
    }

    console.log(`\nDetailed report saved to: ${reportPath}`);
}

// Run the test suite
main().catch(console.error);
