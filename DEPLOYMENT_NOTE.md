# Cloudflare Pages Deployment Configuration

## Project Type
Static HTML site with JavaScript utilities

## Directory Structure (Top 2 Levels)
```
/
├── index.html (Main site file)
├── wfd-survey.html
├── generate_medical_report.js
├── package.json (Development dependencies only)
├── out/ (Static assets)
│   ├── funding/
│   └── static/
└── src/
    └── lib/
```

## Cloudflare Pages Build Settings

### Configuration:
- **Root directory**: `/` (or leave blank)
- **Build command**: *(leave empty)*
- **Build output directory**: `/`

### Explanation:
This is a static site that doesn't require a build step. The HTML files are already built and ready to serve directly.

## Files to Deploy:
- All `.html` files in root
- `out/` directory and its contents
- Any associated CSS/JS files

## Build Date
- Date: August 1, 2025
- Commit: a2eee33 (latest on main)

## Notes
- No wrangler.toml found - this is Pages, not Workers
- No build process required - static files only
- The package.json contains only development/testing dependencies

## Build Error Resolution (August 1, 2025)

### Issue:
Cloudflare Pages was attempting to run `npm install --frozen-lockfile` by default, causing builds to fail with lockfile mismatch errors.

### Solution:
Since this is a static site requiring no build process, the npm install step should be eliminated entirely.

### Required Cloudflare Dashboard Settings:
1. Navigate to Cloudflare Dashboard → Pages → [Your Project] → Settings → Builds & Deployments
2. Set **Build command**: *(leave completely blank)*
3. Ensure **Build output directory**: `/`
4. Save changes and trigger redeploy

This prevents npm from running during deployment, eliminating lockfile issues for this static site.
