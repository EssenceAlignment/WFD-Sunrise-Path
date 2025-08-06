/**
 * WFD Survey Performance Monitor
 * Real-time performance tracking for survey deployment
 * Critical for $4.4M discovery validation
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const SURVEY_URL = 'https://wfd-sunrise-path.lovable.app/';
const RESULTS_DIR = path.join(__dirname, 'performance-results');

// Ensure results directory exists
if (!fs.existsSync(RESULTS_DIR)) {
    fs.mkdirSync(RESULTS_DIR, { recursive: true });
}

async function monitorPerformance() {
    console.log('🔍 WFD Survey Performance Monitor Starting...');
    console.log('📊 Monitoring:', SURVEY_URL);

    const browser = await puppeteer.launch({
        headless: false,
        devtools: true
    });

    const page = await browser.newPage();

    // Enable performance monitoring
    await page.evaluateOnNewDocument(() => {
        window.performanceData = {
            resourceTimings: [],
            navigationTiming: {},
            memoryUsage: [],
            errorCount: 0,
            consoleErrors: []
        };

        // Track resource loading
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                window.performanceData.resourceTimings.push({
                    name: entry.name,
                    duration: entry.duration,
                    size: entry.transferSize || 0,
                    type: entry.initiatorType
                });
            }
        });
        observer.observe({ entryTypes: ['resource', 'navigation'] });

        // Track console errors
        window.addEventListener('error', (e) => {
            window.performanceData.errorCount++;
            window.performanceData.consoleErrors.push({
                message: e.message,
                timestamp: new Date().toISOString()
            });
        });
    });

    // Collect performance metrics
    const metrics = {
        timestamp: new Date().toISOString(),
        url: SURVEY_URL,
        loadMetrics: {},
        resourceMetrics: [],
        memoryMetrics: {},
        errors: []
    };

    try {
        // Navigate and measure
        const startTime = Date.now();
        await page.goto(SURVEY_URL, { waitUntil: 'networkidle2' });
        const loadTime = Date.now() - startTime;

        // Get navigation timing
        const navTiming = await page.evaluate(() => {
            const timing = performance.timing;
            return {
                domContentLoaded: timing.domContentLoadedEventEnd - timing.domContentLoadedEventStart,
                loadComplete: timing.loadEventEnd - timing.loadEventStart,
                firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
                firstContentfulPaint: performance.getEntriesByType('paint')[1]?.startTime || 0
            };
        });

        // Get resource metrics
        const resources = await page.evaluate(() => window.performanceData.resourceTimings);

        // Get memory usage (if available)
        const memoryUsage = await page.evaluate(() => {
            if (performance.memory) {
                return {
                    usedJSHeapSize: (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + ' MB',
                    totalJSHeapSize: (performance.memory.totalJSHeapSize / 1048576).toFixed(2) + ' MB',
                    limit: (performance.memory.jsHeapSizeLimit / 1048576).toFixed(2) + ' MB'
                };
            }
            return null;
        });

        // Test survey sections navigation
        console.log('\n🔄 Testing Survey Section Performance...');

        // Click through survey sections
        const sectionTimings = [];

        // Select program type to enable navigation
        await page.waitForSelector('select', { timeout: 5000 });
        await page.select('select', 'Community Services/Outreach');

        // Measure section transitions
        for (let i = 1; i <= 9; i++) {
            const sectionStart = Date.now();

            // Click next button if available
            const nextButton = await page.$('button:contains("Next")');
            if (nextButton) {
                await nextButton.click();
                await page.waitForTimeout(500); // Wait for transition
            }

            const sectionTime = Date.now() - sectionStart;
            sectionTimings.push({
                section: i,
                transitionTime: sectionTime + 'ms'
            });
        }

        // Compile metrics
        metrics.loadMetrics = {
            totalLoadTime: loadTime + 'ms',
            ...navTiming
        };
        metrics.resourceMetrics = resources;
        metrics.memoryMetrics = memoryUsage;
        metrics.sectionPerformance = sectionTimings;
        metrics.errors = await page.evaluate(() => window.performanceData.consoleErrors);

        // Generate report
        const report = {
            ...metrics,
            summary: {
                status: metrics.errors.length === 0 ? '✅ HEALTHY' : '⚠️ ERRORS DETECTED',
                totalResources: resources.length,
                avgResourceTime: resources.length > 0
                    ? (resources.reduce((sum, r) => sum + r.duration, 0) / resources.length).toFixed(2) + 'ms'
                    : '0ms',
                criticalMetrics: {
                    firstContentfulPaint: navTiming.firstContentfulPaint + 'ms',
                    totalLoadTime: loadTime + 'ms',
                    errorCount: metrics.errors.length
                }
            }
        };

        // Save report
        const reportPath = path.join(RESULTS_DIR, `performance-${Date.now()}.json`);
        fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

        // Display summary
        console.log('\n📊 Performance Summary:');
        console.log('========================');
        console.log(`Status: ${report.summary.status}`);
        console.log(`Load Time: ${report.summary.criticalMetrics.totalLoadTime}`);
        console.log(`First Paint: ${report.summary.criticalMetrics.firstContentfulPaint}`);
        console.log(`Resources Loaded: ${report.summary.totalResources}`);
        console.log(`Errors: ${report.summary.criticalMetrics.errorCount}`);
        console.log(`\nDetailed report saved to: ${reportPath}`);

        // Check for performance issues
        if (loadTime > 3000) {
            console.log('\n⚠️  WARNING: Load time exceeds 3 seconds!');
        }
        if (metrics.errors.length > 0) {
            console.log('\n🚨 ERRORS DETECTED:');
            metrics.errors.forEach(err => console.log(`  - ${err.message}`));
        }

    } catch (error) {
        console.error('❌ Performance monitoring failed:', error);
        metrics.errors.push({
            message: error.message,
            timestamp: new Date().toISOString()
        });
    }

    await browser.close();
    console.log('\n✅ Performance monitoring complete!');
}

// Run performance monitor
monitorPerformance().catch(console.error);

// Export for programmatic use
module.exports = { monitorPerformance };
