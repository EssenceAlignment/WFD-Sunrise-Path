# 📱 Recovery Compass - iPhone Developer Testing Guide

## Overview
This guide provides comprehensive instructions for testing Recovery Compass on iPhone 15 Pro using Developer Mode, Safari Web Inspector, and automated Playwright tests.

## Prerequisites

### 1. macOS Requirements
- macOS 11.0 or later
- Xcode Command Line Tools installed
- Homebrew package manager

### 2. iPhone Requirements
- iPhone 15 Pro (or compatible iOS device)
- iOS 17.0 or later
- USB-C cable for connection

## 🔧 One-Time Setup

### Step 1: Enable iPhone Developer Mode

1. On your iPhone, go to:
   - **Settings** → **Privacy & Security** → **Developer Mode** → Toggle **ON**
   - Your phone will restart

2. After restart:
   - Unlock your iPhone
   - You'll see a prompt to enable Developer Mode
   - Tap **Turn On** and enter your passcode

### Step 2: Enable Safari Web Inspector

1. On your iPhone:
   - **Settings** → **Safari** → **Advanced**
   - Toggle **Web Inspector** → **ON**

### Step 3: Configure Network Link Conditioner

1. On your iPhone:
   - **Settings** → **Developer** → **Network Link Conditioner**
   - Enable it and select **"3G Lossy"** preset
   - This simulates real-world conditions for unhoused users

### Step 4: Setup macOS Environment

Run the setup script:
```bash
./scripts/mobile-testing/setup-iphone-testing.sh
```

This will install:
- `libimobiledevice` - iOS device communication
- `ideviceinstaller` - App management
- `ios-webkit-debug-proxy` - Safari debugging
- `playwright` - Automated testing
- `ffmpeg` - Video recording

## 🚀 Running Tests

### Option 1: Automated Testing

1. Connect your iPhone via USB
2. Trust the computer when prompted on iPhone
3. Run the pairing script:
   ```bash
   ./scripts/mobile-testing/pair-iphone.sh
   ```

4. Execute the test suite:
   ```bash
   node scripts/mobile-testing/run-recovery-compass-tests.js
   ```

   Options:
   - `--headed` - See the browser during tests
   - `--test "test name"` - Run specific test

### Option 2: Manual Testing with Logging

1. Start device logging:
   ```bash
   idevicesyslog -u $(idevice_id -l | head -1) | tee iphone_logs.txt
   ```

2. Start Web Inspector proxy:
   ```bash
   ios_webkit_debug_proxy -c $(idevice_id -l | head -1):9221
   ```

3. Open Safari on Mac:
   - Enable Develop menu: Safari → Preferences → Advanced → Show Develop menu
   - Go to: Develop → [Your iPhone] → recovery-compass.org

## 📊 Test Scenarios

### 1. Compass Companion Journaling
Tests the journaling feature under mobile conditions:
- Text input on mobile keyboard
- Offline data persistence
- Edge storage sync (KV + R2 + D1)

### 2. Funding Dashboard Mobile View
Validates responsive design and interactions:
- Touch interactions with funding cards
- Mobile viewport constraints
- Performance under 3G conditions

### 3. PWA Offline Fallback
Tests Progressive Web App capabilities:
- Service worker registration
- Offline mode handling
- Cache persistence

### 4. iOS Share Sheet Integration
Validates native iOS features:
- Share button functionality
- Safari share sheet
- Shortcut integration

### 5. Edge Storage Verification
Confirms Cloudflare Workers integration:
- API health checks
- Edge request monitoring
- Storage behavior validation

### 6. Console Error Monitoring
Tracks JavaScript errors:
- Runtime error capture
- Console warning analysis
- Performance metrics

## 📱 Network Simulation

### 3G Lossy Preset Details
- **Bandwidth**: 780 Kbps down / 330 Kbps up
- **Latency**: 100ms
- **Packet Loss**: 10%
- **DNS Delay**: 200ms

This simulates typical conditions for users with:
- Limited cellular data
- Weak signal areas
- Congested networks
- Older devices

## 🔍 Analyzing Results

### Test Artifacts Location
- **Screenshots**: `./screenshots/`
- **Videos**: `./videos/`
- **HTML Report**: `./playwright-report/index.html`
- **Console Logs**: `./iphone_logs.txt`
- **Test Results**: `./test-results/`

### Viewing Test Report
```bash
open playwright-report/index.html
```

### Common Issues to Check

1. **JavaScript Errors**
   - Check `iphone_logs.txt` for runtime errors
   - Review console output in test results

2. **Performance Issues**
   - Check page load times in 3G simulation
   - Monitor memory usage in Safari Inspector

3. **UI/UX Problems**
   - Review screenshots for layout issues
   - Check touch target sizes (minimum 44x44 points)

4. **Edge Storage Failures**
   - Verify Cloudflare headers in network logs
   - Check API response times

## 🛠 Troubleshooting

### Device Not Found
```bash
# Check device connection
idevice_id -l

# Re-pair device
idevicepair unpair
idevicepair pair
```

### Web Inspector Not Working
1. Restart Safari on Mac
2. Reconnect iPhone
3. Ensure Developer Mode is still enabled
4. Try different USB port/cable

### Tests Timing Out
1. Increase timeout in test files
2. Check Network Link Conditioner settings
3. Verify Recovery Compass URL is accessible

### Logging Issues
```bash
# Kill existing logging processes
pkill -f "idevicesyslog"
pkill -f "ios_webkit_debug_proxy"

# Restart logging
./scripts/mobile-testing/pair-iphone.sh
```

## 📋 Manual Testing Checklist

When running manual tests, verify:

- [ ] Journal entries save and persist
- [ ] Funding dashboard loads within 3 seconds
- [ ] Offline mode shows appropriate message
- [ ] Share sheet opens correctly
- [ ] No JavaScript errors in console
- [ ] Touch interactions feel responsive
- [ ] Text is readable without zooming
- [ ] Forms are easily fillable
- [ ] Navigation is intuitive
- [ ] Back button works as expected

## 🔄 Continuous Testing

### Setting Up Automated Runs
1. Create a cron job or scheduled task
2. Use environment variables for configuration:
   ```bash
   export RECOVERY_COMPASS_URL="https://recovery-compass.org"
   ```

3. Run tests periodically:
   ```bash
   # Add to crontab for daily runs
   0 2 * * * cd /path/to/project && npm test
   ```

### Integration with CI/CD
The tests are configured to work with GitHub Actions and other CI platforms. See `.github/workflows/mobile-testing.yml` for integration examples.

## 📱 Additional Mobile Devices

To test on other iOS devices, update `playwright.config.ts`:
- iPhone 13
- iPhone SE
- iPad Pro
- iPad Mini

## 🎯 Performance Benchmarks

Expected performance under 3G conditions:
- Initial page load: < 5 seconds
- Journal save: < 2 seconds
- Dashboard render: < 3 seconds
- Offline detection: < 1 second

## 📚 Resources

- [Playwright Mobile Testing](https://playwright.dev/docs/emulation)
- [iOS Developer Mode](https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device)
- [Safari Web Inspector](https://developer.apple.com/safari/tools/)
- [Network Link Conditioner](https://developer.apple.com/download/more/)

---

For questions or issues, refer to the Recovery Compass development team or file an issue in the repository.
