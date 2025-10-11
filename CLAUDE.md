# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Google IP Monitor is an automated infrastructure monitoring tool that tracks changes in Google Cloud and Google Public IP ranges. It runs every 3 hours via GitHub Actions, detects IP range changes, sends Telegram notifications, and generates firewall rules in 9+ formats.

**Live Dashboard:** `https://m3hr4nn.github.io/googleipmonitor/`

## Core Components

### 1. monitor.py
- Fetches IP data from Google's `cloud.json` and `goog.json` endpoints
- Compares current data with previous day's snapshot
- Detects added/removed IP prefixes
- Sends Telegram notifications when changes detected
- Stores daily snapshots in `data/YYYY-MM-DD.json`

**Key Methods:**
- `fetch_ip_data()`: Retrieves current Google IP ranges
- `compare_data()`: Compares two datasets and finds differences
- `send_telegram_message()`: Sends formatted alerts via Telegram Bot API

### 2. generate_report.py
- Generates the main HTML dashboard (`index.html`)
- Displays statistics, changes, and historical comparison
- Uses inline CSS with Chrome-inspired dark theme
- Automatically generated after each monitoring run

### 3. generate_firewall_rules.py
- Exports IP ranges to 9 firewall formats:
  - iptables (Linux)
  - AWS Security Group (JSON)
  - Azure NSG (JSON)
  - Cisco ACL
  - pfSense Alias
  - MikroTik RouterOS Script
  - Plain Text
  - CSV
  - JSON
- Generates `exports/index.html` with download links

### 4. .github/workflows/monitor.yml
- GitHub Actions workflow running every 3 hours (`cron: '0 */3 * * *'`)
- Execution order:
  1. Run `monitor.py` (fetch & compare)
  2. Run `generate_report.py` (create dashboard)
  3. Run `generate_firewall_rules.py` (export formats)
  4. Commit and push all changes
- Requires secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (optional)

## Data Flow

```
Google APIs → monitor.py → data/YYYY-MM-DD.json
                ↓
        generate_report.py → index.html
                ↓
  generate_firewall_rules.py → exports/*
                ↓
          Git commit & push
                ↓
          GitHub Pages deployment
```

## Common Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional for Telegram)
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"

# Run monitoring pipeline
python monitor.py                    # Fetch and compare IPs
python generate_report.py            # Generate dashboard
python generate_firewall_rules.py    # Generate exports

# View locally
open index.html                      # Main dashboard
open exports/index.html              # Export page
```

### Testing Changes
```bash
# Test monitor script
python monitor.py

# Check generated files
ls -lh data/
ls -lh exports/

# View git changes
git status
git diff
```

### Manual GitHub Actions Trigger
Go to Actions → Google IP Monitor → Run workflow

## Architecture Notes

### Data Storage
- **data/** directory: Historical JSON snapshots (one file per run)
- Each file contains both `cloud` and `goog` endpoint responses
- Files persist in git for audit trail and comparison

### IP Prefix Extraction
- Extracts both `ipv4Prefix` and `ipv6Prefix` from Google's JSON
- Combines prefixes from `cloud.json` and `goog.json`
- Deduplicates and sorts prefixes

### Change Detection Logic
- Uses Python sets to compute: `added = new - old`, `removed = old - new`
- Telegram messages limited to first 10 changes (prevents spam)
- Dashboard shows up to 100 changes per category

### GitHub Pages Deployment
- Automatically deploys from `main` branch root
- Files: `index.html`, `styles.css`, `exports/*`
- No build step required (static HTML/CSS)

## Configuration

### Change Monitoring Schedule
Edit `.github/workflows/monitor.yml` cron expression:
```yaml
# Every 3 hours (default)
- cron: '0 */3 * * *'

# Every hour
- cron: '0 * * * *'

# Twice daily
- cron: '0 9,21 * * *'
```

### Add New Data Sources
Edit `monitor.py`, add to `self.urls` dictionary:
```python
self.urls = {
    'cloud': 'https://www.gstatic.com/ipranges/cloud.json',
    'goog': 'https://www.gstatic.com/ipranges/goog.json',
    'custom': 'https://your-source.com/ips.json'
}
```

### Add New Export Format
1. Add generator method to `FirewallRulesGenerator` class in `generate_firewall_rules.py`
2. Register in `formats` dictionary in `generate_all()` method
3. Update `generate_exports_index()` to add download card

### Theme Customization
Edit CSS variables in `styles.css`:
```css
:root {
    --accent-blue: #8ab4f8;   /* Primary accent */
    --accent-green: #81c995;  /* Success/additions */
    --accent-red: #f28b82;    /* Errors/removals */
}
```

## Versioning

Use **Semantic Versioning 2.0.0** for each build/release:
- MAJOR.MINOR.PATCH (e.g., 1.2.3)
- Tag releases in git: `git tag v1.2.3`

## Important Notes

- **No package.json**: This is a Python-only project
- **Zero external dependencies** except `requests` library
- **No API keys in code**: Use GitHub Secrets for Telegram credentials
- **Telegram is optional**: Dashboard and exports work without it
- **Daily snapshots**: One JSON file per run creates historical record
- **Firewall rules**: All exports regenerated on every run (always current)
- **GitHub Actions quota**: ~480 minutes/month (24% of free tier)

## Test Reports

Store test reports in `.odt` format in a directory **outside the project directory** to avoid committing them.
