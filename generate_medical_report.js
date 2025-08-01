const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generateReports() {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // Set viewport to letter size dimensions
        await page.setViewport({
            width: 816,  // 8.5 inches at 96 DPI
            height: 1056, // 11 inches at 96 DPI
            deviceScaleFactor: 2 // Higher quality
        });

        // Read the HTML file
        const htmlPath = path.join(__dirname, 'nuha_sayegh_medical_report.html');
        const htmlContent = fs.readFileSync(htmlPath, 'utf8');

        // Load the HTML content
        await page.setContent(htmlContent, {
            waitUntil: 'networkidle0'
        });

        // Generate PNG
        await page.screenshot({
            path: 'nuha_sayegh_medical_report.png',
            fullPage: true,
            type: 'png'
        });
        console.log('PNG generated successfully');

        // Generate PDF
        await page.pdf({
            path: 'nuha_sayegh_medical_report.pdf',
            format: 'Letter',
            printBackground: true,
            margin: {
                top: '0.5in',
                bottom: '0.5in',
                left: '0.5in',
                right: '0.5in'
            }
        });
        console.log('PDF generated successfully');

    } catch (error) {
        console.error('Error generating reports:', error);
    } finally {
        await browser.close();
    }
}

generateReports();
