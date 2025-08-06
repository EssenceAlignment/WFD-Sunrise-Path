# macOS Memory Management Toolkit - Quick Start Guide

## 🚀 Installation

1. **Run the installer:**
   ```bash
   cd macos-memory-toolkit
   ./install.sh
   ```

2. **Restart your terminal or run:**
   ```bash
   source ~/.zshrc  # or ~/.bashrc
   ```

## 🎯 Basic Commands

After installation, use these commands from anywhere:

- `memcheck` - Check current memory status
- `memclean` - Safe memory cleanup (no sudo required)
- `memdeep` - Aggressive cleanup (requires sudo)
- `memrescue` - Emergency recovery (requires sudo, use with caution!)
- `memhelp` - Show all available commands

## 📊 Monitoring & Reports

- `memmon` - Real-time memory monitor
- `membench` - Run performance benchmarks
- `memreport` - Generate detailed health report

## 🔄 Automation

**Set up automatic cleanup:**
```bash
./automation/cron_setup.sh
```

Or manually run:
- `./automation/daily_cleanup.sh` - Daily maintenance
- `./automation/weekly_maintenance.sh` - Weekly deep clean

## ⚙️ Configuration

Edit `config/settings.conf` to customize:
- Memory thresholds
- Cleanup aggressiveness
- Notification preferences
- Auto-cleanup settings

## 🆘 Emergency Situations

If your Mac is running critically low on memory:

1. First try: `memclean`
2. If that's not enough: `sudo memdeep`
3. Last resort: `sudo memrescue` (closes all apps!)

## 📈 Best Practices

1. Run `memcheck` regularly to monitor status
2. Use `memclean` weekly for maintenance
3. Keep 20% of disk space free for virtual memory
4. Restart your Mac if memory issues persist

## 🔍 Troubleshooting

- **Permission denied**: Some commands need `sudo`
- **Command not found**: Restart terminal or source your shell config
- **Scripts not running**: Check if executable with `ls -la`

## 📝 Logs

All logs are stored in:
```
~/Library/Logs/memory-toolkit/
```

---

For detailed documentation, see [README.md](README.md)
