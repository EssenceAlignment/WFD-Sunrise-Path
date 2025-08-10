# WFD-COMPLIANCE.ORG Deployment Guide

## Domain: wfd-compliance.org
## Repository: https://github.com/EssenceAlignment/WFD-Sunrise-Path

## 🚀 Deployment Steps

### Step 1: AWS Amplify Setup
1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
2. Click "New app" → "Host web app"
3. Choose "GitHub" as your source provider
4. Authorize AWS Amplify to access your GitHub account
5. Select repository: `EssenceAlignment/WFD-Sunrise-Path`
6. Select branch: `main`
7. App name: `wfd-compliance`
8. The build settings will automatically detect `amplify.yml`
9. Click "Save and deploy"

### Step 2: Custom Domain Configuration in Amplify
1. In AWS Amplify Console, go to your app
2. Navigate to "Domain management" in the left sidebar
3. Click "Add domain"
4. Enter: `wfd-compliance.org`
5. AWS will provide DNS records to add to Cloudflare

### Step 3: Cloudflare DNS Configuration
1. Log into [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Select `wfd-compliance.org` domain
3. Go to DNS settings
4. Add the records provided by AWS Amplify:
   - Type: CNAME
   - Name: @ (or root)
   - Target: [Your Amplify app URL].amplifyapp.com
   - Proxy status: Proxied (orange cloud ON)
   
5. Add www subdomain:
   - Type: CNAME
   - Name: www
   - Target: [Your Amplify app URL].amplifyapp.com
   - Proxy status: Proxied (orange cloud ON)

### Step 4: Cloudflare Cache and Performance Settings
1. In Cloudflare Dashboard for `wfd-compliance.org`:
2. Go to "Caching" → "Configuration"
3. Set Browser Cache TTL: 4 hours
4. Go to "Page Rules"
5. Create rule for `*wfd-compliance.org/*`:
   - Cache Level: Standard
   - Edge Cache TTL: 2 hours
   - Always Use HTTPS: On

### Step 5: SSL/TLS Configuration
1. In Cloudflare, go to "SSL/TLS" → "Overview"
2. Set encryption mode to "Full (strict)"
3. Enable "Always Use HTTPS"
4. Enable "Automatic HTTPS Rewrites"

## 📊 Monitoring
- AWS Amplify Console: Monitor builds and deployments
- Cloudflare Analytics: Track traffic and performance
- GitHub Actions: Monitor CI/CD pipeline

## 🔄 Continuous Deployment
Every push to the `main` branch will automatically trigger:
1. GitHub Actions workflows (if configured)
2. AWS Amplify build and deployment
3. Cloudflare cache purge (via Page Rules)

## 🔒 Security Headers (Cloudflare Transform Rules)
Add these via Transform Rules in Cloudflare:
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

## 📝 Environment Variables
Set in AWS Amplify Console under "Environment variables":
- `ENVIRONMENT`: production
- `DOMAIN`: wfd-compliance.org
- Add any API keys or secrets needed by the application

## ✅ Verification Checklist
- [ ] AWS Amplify app created and connected to GitHub
- [ ] Domain added in AWS Amplify
- [ ] DNS records configured in Cloudflare
- [ ] SSL/TLS properly configured
- [ ] Cache rules set up
- [ ] Security headers configured
- [ ] Site accessible at https://wfd-compliance.org
- [ ] Site accessible at https://www.wfd-compliance.org

## 🚨 Troubleshooting
- DNS propagation can take up to 48 hours
- Check Cloudflare DNS settings if site doesn't load
- Verify AWS Amplify build logs for deployment issues
- Clear Cloudflare cache if updates aren't showing

---
*Last Updated: August 2025*
*Maintained by: Recovery Compass Team*
