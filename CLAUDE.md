# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Google IP Monitor is an automated infrastructure monitoring tool that tracks changes in Google Cloud and Google Public IP ranges. It runs every 3 hours via GitHub Actions, detects IP range changes, sends Telegram notifications, generates firewall rules in 9+ formats, and visualizes historical trends with interactive charts.

**Live Dashboard:** `https://m3hr4nn.github.io/googleipmonitor/`

**Architecture:** Microservices-based design with independent, modular services for scalability and maintainability.

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
- Integrates Chart API Gateway for historical analytics
- Uses external CSS (`styles.css`) with Chrome-inspired dark theme
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

### 4. Historical Charts Microservices (services/)
**Microservices Architecture** - Independent, modular services for chart generation:

#### Service 1: Data Aggregator (`aggregator_service.py`)
- Parses historical JSON data from `data/` directory
- Computes metrics: total ranges, IPv4/IPv6 counts, daily changes
- Outputs to `cache/metrics.json`
- **Single Responsibility:** Data parsing and metric computation

#### Service 2: Chart Config (`chart_config_service.py`)
- Generates Chart.js configuration objects
- Manages dark theme colors matching dashboard
- Defines axes, tooltips, legends
- Outputs to `cache/chart_configs.json`
- **Single Responsibility:** Chart styling and configuration

#### Service 3: Chart Renderer (`chart_renderer_service.py`)
- Generates HTML canvas elements
- Creates Chart.js initialization scripts
- Handles responsive layouts
- Returns injectable HTML fragments
- **Single Responsibility:** HTML/JavaScript generation

#### Service 4: Chart Exporter (`chart_export_service.py`)
- Exports data to CSV, JSON, Markdown formats
- Generates `exports/charts/index.html`
- Provides data portability for external tools
- **Single Responsibility:** Multi-format data export

#### Service 5: API Gateway (`chart_api_gateway.py`)
- Orchestrates all chart microservices
- Manages service lifecycle and execution order
- Handles errors with graceful fallbacks
- Provides unified interface
- **Single Responsibility:** Service coordination

**Chart Types:**
- Line Chart: IP range growth over time (total, IPv4, IPv6)
- Bar Chart: Daily changes (added/removed) - last 30 days
- Pie Chart: IPv4 vs IPv6 distribution

**Configuration:** `config/chart_settings.json` - customizable options for all charts

### 5. .github/workflows/monitor.yml
- GitHub Actions workflow running every 3 hours (`cron: '0 */3 * * *'`)
- Execution order:
  1. Run `monitor.py` (fetch & compare)
  2. Run `generate_report.py` (create dashboard + charts via gateway)
  3. Run `generate_firewall_rules.py` (export formats)
  4. Commit and push all changes (including `cache/`)
- Requires secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (optional)

## Data Flow

### Main Pipeline
```
Google APIs → monitor.py → data/YYYY-MM-DD.json
                ↓
        generate_report.py → ChartAPIGateway → index.html
                ↓                     ↓
  generate_firewall_rules.py    cache/*.json
                ↓                     ↓
          Git commit & push    exports/charts/*
                ↓
          GitHub Pages deployment
```

### Chart Microservices Pipeline
```
generate_report.py
    ↓
ChartAPIGateway (Orchestrator)
    ↓
    ├→ [1] DataAggregatorService → cache/metrics.json
    ↓
    ├→ [2] ChartConfigService → cache/chart_configs.json
    ↓
    ├→ [3] ChartRendererService → HTML fragments
    ↓
    └→ [4] ChartExportService → exports/charts/*
    ↓
Return aggregated result → inject into index.html
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
open exports/index.html              # Firewall rules export
open exports/charts/index.html       # Chart data exports

# Test individual microservices
python services/aggregator_service.py      # Test data aggregation
python services/chart_config_service.py    # Test chart configs
python services/chart_renderer_service.py  # Test HTML rendering
python services/chart_export_service.py    # Test data exports
python services/chart_api_gateway.py       # Test full pipeline
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
- Files: `index.html`, `styles.css`, `exports/*`, `cache/*`
- Chart.js loaded via CDN (no build step required)
- Static HTML/CSS with client-side JavaScript rendering

### Microservices Architecture Benefits
1. **Separation of Concerns**: Each service has single responsibility
2. **Independent Testing**: Services can be tested in isolation
3. **Scalability**: Services can be enhanced independently
4. **Maintainability**: Clear interfaces between components
5. **Reusability**: Services can be used by other features
6. **Graceful Degradation**: Gateway handles service failures

### Cache Management
- **cache/metrics.json**: Aggregated historical metrics
- **cache/chart_configs.json**: Chart.js configuration objects
- Cached data committed to git for GitHub Pages compatibility
- Services support `use_cache` parameter for performance

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

### Chart Configuration
Edit `config/chart_settings.json`:
```json
{
  "enabled": true,
  "days_to_show": 90,
  "use_cache": true,
  "charts": {
    "line_chart": {"enabled": true, "height": 400},
    "bar_chart": {"enabled": true, "height": 350},
    "pie_chart": {"enabled": true, "height": 320}
  },
  "exports": {"csv": true, "json": true, "markdown": true}
}
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

### Add New Chart Type
1. Add method to `ChartConfigService` (e.g., `get_area_chart_config()`)
2. Add rendering method to `ChartRendererService` (e.g., `render_area_chart()`)
3. Update `ChartAPIGateway` to include new chart
4. Add CSS styling to `styles.css` if needed

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
