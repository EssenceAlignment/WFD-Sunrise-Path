# 📱 WFD Dashboard Mobile Deployment Guide

Your WFD dashboard is now configured with Capacitor for native mobile deployment! This guide will walk you through deploying to iOS and Android devices.

## 🚀 Mobile Optimizations Completed

### ✅ Capacitor Setup
- Installed all required Capacitor dependencies
- Created `capacitor.config.ts` with WFD app configuration
- Added mobile deployment scripts to `package.json`
- Configured splash screen with WFD brand colors (#6B46C1)

### 📋 Prerequisites

Before deploying to mobile devices, ensure you have:

**For iOS:**
- macOS computer with Xcode installed
- Apple Developer account (for device testing)
- iOS device or simulator

**For Android:**
- Android Studio installed
- Android SDK configured
- Android device or emulator

## 📱 Deployment Steps

### 1. **Export to GitHub**
First, commit and push your changes to GitHub:

```bash
git add .
git commit -m "Add Capacitor mobile support"
git push origin main
```

### 2. **Clone and Install Locally**
On your development machine:

```bash
git clone https://github.com/Recovery-Compass/wfd-sunrise-path.git
cd wfd-sunrise-path
npm install
```

### 3. **Build Your Web App**
Since your project uses HTML files, create a dist directory:

```bash
mkdir -p dist
cp index.html wfd-survey.html dist/
cp -r styles dist/ 2>/dev/null || true
cp -r scripts dist/ 2>/dev/null || true
```

### 4. **Add Mobile Platforms**

**For iOS:**
```bash
npm run cap:add:ios
```

**For Android:**
```bash
npm run cap:add:android
```

### 5. **Sync Capacitor**
This copies your web app to the native projects:

```bash
npm run cap:sync
```

### 6. **Run on Devices**

**iOS (Physical Device or Simulator):**
```bash
npm run cap:run:ios
```

**Android (Physical Device or Emulator):**
```bash
npm run cap:run:android
```

### 7. **Open in Native IDEs**
For more control over the build process:

**iOS (Opens in Xcode):**
```bash
npm run cap:open:ios
```

**Android (Opens in Android Studio):**
```bash
npm run cap:open:android
```

## 🛠️ Troubleshooting

### Common Issues

1. **"webDir is not a directory"**
   - Ensure you've created the dist directory and copied your files
   - Run the build step again

2. **iOS Signing Issues**
   - Open the project in Xcode
   - Select your development team in the project settings
   - Enable automatic code signing

3. **Android Build Errors**
   - Ensure Android Studio is properly installed
   - Accept all SDK licenses: `sdkmanager --licenses`
   - Update gradle if needed

### Mobile-Specific Features

Your app is configured with:
- **Splash Screen**: Purple (#6B46C1) background with 2-second duration
- **App Name**: "WFD Dashboard"
- **App ID**: `org.whittier.wfd`
- **iOS Safe Areas**: Automatically handled
- **Android Debug Logging**: Enabled for development

## 📦 Production Deployment

### iOS App Store
1. Archive in Xcode: Product → Archive
2. Upload to App Store Connect
3. Submit for review

### Google Play Store
1. Build signed APK/AAB in Android Studio
2. Upload to Google Play Console
3. Complete store listing and submit

## 🔧 Updating Your App

When you make changes to your web app:

1. Update your HTML/CSS/JS files
2. Copy to dist directory
3. Run `npm run cap:sync`
4. Rebuild in Xcode/Android Studio

## 📚 Additional Resources

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [iOS Deployment Guide](https://capacitorjs.com/docs/ios)
- [Android Deployment Guide](https://capacitorjs.com/docs/android)

## 🎉 Next Steps

Your WFD dashboard is now ready for mobile deployment! The app will provide a native experience with:
- Touch-optimized interactions
- Native splash screen
- App-like performance
- Offline capabilities (if implemented)

For questions or issues, refer to the Capacitor documentation or reach out to your development team.
