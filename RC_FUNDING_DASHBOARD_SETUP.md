# 🎯 Recovery Compass Funding Dashboard Setup

## Quick Start

The `rc-funding` command provides real-time funding intelligence from your Airtable, with opportunities scored and ranked by alignment and urgency. **Now with automatic browser display!**

## Installation

1. **Make it accessible from anywhere** by adding to your PATH:

```bash
# Add this line to your ~/.bashrc or ~/.zshrc
export PATH="$PATH:/Users/ericjones/Projects/wfd-sunrise-path/WFD-Sunrise-Path/scripts"

# Reload your shell
source ~/.bashrc  # or source ~/.zshrc
```

2. **Now you can run from anywhere**:
```bash
rc-funding
```

## Usage Examples

### Basic Commands

```bash
# Web Dashboard (Default - Opens in Arc Browser)
rc-funding                  # Opens interactive dashboard in browser

# Terminal Version (Classic)
rc-funding --terminal       # Show all opportunities in terminal
rc-funding --terminal --top 10      # Top 10 opportunities
rc-funding --terminal --urgent      # Urgent opportunities only
rc-funding --terminal --web3        # Non-traditional only
rc-funding --terminal --export      # Export to CSV
```

### What You'll See

**Web Dashboard**: A beautiful, interactive dashboard opens in Arc with:
- 📊 Real-time statistics cards
- 🔍 Interactive filters (All, Urgent, Traditional, Non-Traditional, High Score)
- 🎯 Color-coded urgency indicators
- 💎 Keyword tags for each opportunity
- 🔗 Direct "Apply Now" links

**Terminal View**: Classic text-based display with scores and rankings

## Scoring System

### Alignment Score (0-100)
- **Mental Health/Recovery**: +30 points
- **Innovation/Technology**: +20 points
- **Vulnerable Populations**: +20 points
- **Web3/DAO/Crypto**: +25 points
- **Collaboration**: +15 points

### Urgency Score (0-100)
- 🔴 **<7 days**: 100 points
- 🔴 **7-14 days**: 80 points
- 🟡 **15-30 days**: 60 points
- 🟢 **31-60 days**: 40 points
- 🟢 **>60 days**: 20 points

### Combined Score
**60% Alignment + 40% Urgency** = Final ranking

## Color Codes

- 🔴 **Red**: Urgent (deadline < 14 days)
- 🟡 **Yellow**: Soon (deadline 14-30 days)
- 🟢 **Green**: Normal (deadline > 30 days)

## Pro Tips

1. **Morning Check**: Run `rc-funding --urgent` each morning to catch deadlines
2. **Weekly Review**: Run `rc-funding --export` weekly for team review
3. **Web3 Opportunities**: Run `rc-funding --web3` to see innovative funding

## Data Source

Pulls live data from your Recovery Compass Airtable:
- Base: `appNBesu9xYl5Mvm1`
- Table: `tblcfetlKrhMU4p5r` (Funding Opportunities)

## Troubleshooting

If you see "command not found":
1. Make sure you're in the right directory or have added to PATH
2. Check that the script is executable: `chmod +x scripts/rc-funding`
3. Use the full path: `./scripts/rc-funding`

---

**Your funding intelligence is now just a command away!**
