---
name: Mobile CI Automation
about: Set up automated build pipeline for mobile app deployment
title: '[MOBILE] Create mobile-build.yml GitHub Action for automated builds'
labels: mobile, ci-cd, automation, week-3
assignees: ''
---

## 🚀 Mobile CI/CD Pipeline Implementation

### Overview
Create a GitHub Action workflow that automatically builds, tests, and uploads mobile app artifacts to Firebase App Distribution and TestFlight for staged rollouts.

### Requirements
- [ ] Create `.github/workflows/mobile-build.yml`
- [ ] Configure iOS build with code signing
- [ ] Configure Android build with keystore
- [ ] Upload artifacts to distribution platforms
- [ ] Notify team on successful builds

### Implementation Details

```yaml
# .github/workflows/mobile-build.yml
name: Mobile App Build & Deploy

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'capacitor.config.ts'
      - 'package.json'
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          npm ci
          npm run build

      - name: Sync Capacitor
        run: npx cap sync android

      - name: Build Android APK
        run: |
          cd android
          ./gradlew assembleRelease

      - name: Upload to Firebase
        uses: wzieba/Firebase-Distribution-Github-Action@v1
        with:
          appId: ${{ secrets.FIREBASE_ANDROID_APP_ID }}
          token: ${{ secrets.FIREBASE_TOKEN }}
          groups: internal-testers
          file: android/app/build/outputs/apk/release/app-release.apk

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: latest-stable

      - name: Install dependencies
        run: |
          npm ci
          npm run build

      - name: Sync Capacitor
        run: npx cap sync ios

      - name: Build iOS IPA
        run: |
          cd ios/App
          xcodebuild -workspace App.xcworkspace \
            -scheme App \
            -configuration Release \
            -archivePath build/App.xcarchive \
            archive

      - name: Upload to TestFlight
        uses: apple-actions/upload-testflight-build@v1
        with:
          app-path: ios/App/build/App.ipa
          issuer-id: ${{ secrets.APPSTORE_ISSUER_ID }}
          api-key-id: ${{ secrets.APPSTORE_KEY_ID }}
          api-private-key: ${{ secrets.APPSTORE_PRIVATE_KEY }}
```

### Secrets Required
- `FIREBASE_ANDROID_APP_ID`
- `FIREBASE_TOKEN`
- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `APPSTORE_ISSUER_ID`
- `APPSTORE_KEY_ID`
- `APPSTORE_PRIVATE_KEY`

### Acceptance Criteria
- [ ] Builds trigger automatically on relevant code changes
- [ ] Android APK builds successfully and uploads to Firebase
- [ ] iOS IPA builds successfully and uploads to TestFlight
- [ ] Build status notifications sent to Slack/Discord
- [ ] Build artifacts stored for 30 days

### Timeline
- **Owner**: CI Lead
- **Deadline**: Week 3, Day 3
- **Dependencies**: App signing certificates must be configured

### Resources
- [GitHub Actions for Mobile](https://docs.github.com/en/actions/deployment/deploying-xcode-applications)
- [Firebase App Distribution](https://firebase.google.com/docs/app-distribution)
- [TestFlight Documentation](https://developer.apple.com/testflight/)
