# macOS Memory Management Toolkit

A comprehensive collection of scripts and tools for managing memory on macOS systems. This toolkit provides safe, efficient, and automated solutions for monitoring and optimizing system memory.

## 🚀 Quick Start

```bash
# Install the toolkit
./install.sh

# Check memory status
memcheck

# Clean memory (safe mode)
memclean

# Deep clean (requires confirmation)
sudo memory_deep_clean

# Emergency recovery (use with caution)
sudo emergency_recovery
```

## 📁 Directory Structure

```
macos-memory-toolkit/
├── core/                    # Core memory management scripts
├── monitoring/              # Monitoring and reporting tools
├── automation/              # Automated maintenance scripts
├── utils/                   # Utility functions and helpers
└── config/                  # Configuration files
```

## 🛠️ Core Scripts

### memory_check.sh
Quick memory status check showing current usage, pressure, and swap.

```bash
./core/memory_check.sh
```

### memory_clean.sh
Safe memory cleanup that won't affect system stability.

```bash
./core/memory_clean.sh
```

### memory_deep_clean.sh
Aggressive memory cleanup including caches and temporary files.

```bash
sudo ./core/memory_deep_clean.sh
```

### emergency_recovery.sh
Nuclear option for severe memory issues. Closes apps and performs aggressive cleanup.

```bash
sudo ./core/emergency_recovery.sh
```

## 📊 Monitoring Tools

### memory_monitor.sh
Real-time memory monitoring with automatic cleanup triggers.

```bash
./monitoring/memory_monitor.sh
```

### memory_benchmark.sh
Performance testing before and after optimization.

```bash
./monitoring/memory_benchmark.sh
```

### memory_health_report.sh
Comprehensive system memory health report.

```bash
./monitoring/memory_health_report.sh
```

## 🔄 Automation

### Daily Cleanup
Automatic daily maintenance routine.

```bash
./automation/daily_cleanup.sh
```

### Weekly Maintenance
Deep cleaning performed weekly.

```bash
./automation/weekly_maintenance.sh
```

### Cron Setup
Configure automatic scheduled cleanups.

```bash
./automation/cron_setup.sh
```

## ⚙️ Configuration

Edit `config/settings.conf` to customize:
- Memory thresholds
- Cleanup aggressiveness
- Notification preferences
- Excluded applications
- Custom paths

## 🎯 Shell Aliases

After installation, use these convenient aliases:

- `memcheck` - Quick memory status
- `memclean` - Safe memory cleanup
- `memdeep` - Deep memory cleanup
- `memreport` - Full health report
- `memmon` - Start memory monitor

## 🚨 Safety Features

- **Confirmation Prompts**: Destructive operations require confirmation
- **Backup Checks**: Verifies backups before major cleanups
- **Logging**: All operations are logged to `~/Library/Logs/memory-toolkit/`
- **Rollback**: Some operations can be reversed if issues occur
- **Disk Space**: Checks available space before operations

## 📈 Performance Metrics

The toolkit tracks:
- Memory freed per operation
- Time taken for cleanups
- Success/failure rates
- Historical memory usage
- Optimization effectiveness

## 🔧 Troubleshooting

### Common Issues

1. **"Permission denied" errors**
   - Some operations require sudo access
   - Run with: `sudo ./script_name.sh`

2. **"Command not found" after installation**
   - Restart your terminal
   - Or run: `source ~/.zshrc`

3. **Scripts not executing**
   - Ensure execute permissions: `chmod +x script_name.sh`

4. **High memory usage persists**
   - Check Activity Monitor for specific apps
   - Consider restarting problematic applications
   - As last resort, restart your Mac

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the toolkit.

## ⚠️ Disclaimer

These scripts modify system files and processes. While safety measures are in place, use at your own risk. Always ensure you have current backups before running aggressive cleanup operations.

## 📝 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

Based on best practices from the macOS community and Apple's official documentation.
