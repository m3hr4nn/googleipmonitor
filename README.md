<div align="center">

# 🌐 Google IP Monitor

**Automated monitoring of Google's IP ranges with real-time alerts, interactive charts, and firewall rule exports**

[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/m3hr4nn/googleipmonitor/actions)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/googleipmonitor_bot)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

[Live Dashboard](https://m3hr4nn.github.io/googleipmonitor/) • [Chart Analytics](https://m3hr4nn.github.io/googleipmonitor/exports/charts/) • [Export Rules](https://m3hr4nn.github.io/googleipmonitor/exports/) • [Roadmap](ROADMAP.md)

---

**📸 [View Live Dashboard →](https://m3hr4nn.github.io/googleipmonitor/)**

</div>

---

## 🎯 Overview

Google IP Monitor is an **automated infrastructure monitoring tool** that tracks changes in Google Cloud and Google Public IP ranges. Built for DevOps engineers, network administrators, and security teams who need to stay informed about Google's infrastructure changes.

### Why Google IP Monitor?

- 🔔 **Real-time Alerts** - Get instant Telegram notifications every 3 hours when IP ranges change
- 📈 **Interactive Charts** - Visualize IP growth trends with Chart.js (Line, Bar, Pie charts)
- 🔥 **Firewall Export** - Download ready-to-use rules for 9+ firewall formats (iptables, AWS, Azure, Cisco, pfSense, MikroTik, etc.)
- 📊 **Visual Dashboard** - Beautiful Chrome-inspired dark theme interface
- 🏗️ **Microservices Architecture** - Modular, scalable, and maintainable design
- 🤖 **Fully Automated** - Runs every 3 hours via GitHub Actions, zero maintenance
- 💰 **100% Free** - No servers, no costs, forever
- 📈 **Historical Tracking** - All changes stored in Git for audit trails
- 🔒 **Secure** - No API keys exposed, runs in isolated GitHub environment

---

## ✨ Features

### 🚀 Core Features

| Feature | Description |
|---------|-------------|
| **Every 3 Hours Monitoring** | Automatically checks Google's IP ranges 8 times per day |
| **Change Detection** | Identifies added and removed IP prefixes with detailed diff reports |
| **Interactive Charts** | Line, Bar, and Pie charts showing historical trends and analytics |
| **Telegram Alerts** | Instant notifications with formatted summaries of changes |
| **9 Export Formats** | Download firewall rules for iptables, AWS, Azure, Cisco, pfSense, MikroTik, CSV, JSON, Plain Text |
| **Chart Data Exports** | Export historical metrics in CSV, JSON, and Markdown formats |
| **Web Dashboard** | Responsive, dark-themed interface showing current status and history |
| **Microservices Backend** | 5 independent services for scalability and maintainability |
| **Git-based Storage** | All data versioned and tracked in GitHub |
| **Multi-source** | Monitors both `cloud.json` and `goog.json` endpoints |

### 🔥 Firewall Export Formats

<table>
<tr>
<td width="50%">

**Cloud Providers**
- ☁️ AWS Security Group JSON
- 🔷 Azure NSG Rules JSON

**Network Equipment**
- 🌐 Cisco IOS ACL
- 🔧 MikroTik RouterOS Script

</td>
<td width="50%">

**Firewalls**
- 🐧 iptables/ip6tables Script
- 🛡️ pfSense Alias Format

**Data Formats**
- 📊 CSV (Excel compatible)
- 📦 JSON (Structured data)
- 📄 Plain Text List

</td>
</tr>
</table>

### 📱 Telegram Notifications

```
📊 Google IP Ranges Report
📅 Date: 2025-10-10 15:00
========================================

🔔 Changes detected!

➕ Added (3):
  • 34.128.0.0/16
  • 35.192.0.0/14
  • 2600:1900::/35

📊 Statistics:
  Previous: 1,234 ranges
  Current: 1,236 ranges
  Net change: +2
```

### 🌐 Dashboard Features

- **Live Statistics** - Current vs previous day comparison
- **Historical Charts** - Interactive visualizations with Chart.js
  - 📈 Line Chart: IP range growth over time
  - 📊 Bar Chart: Daily changes (last 30 days)
  - 🥧 Pie Chart: IPv4 vs IPv6 distribution
- **Change Tracking** - Color-coded additions and removals
- **One-Click Export** - Download firewall rules in your preferred format
- **Chart Data Exports** - Export metrics to CSV, JSON, Markdown
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Fast Navigation** - Quick access to exports and historical data

---

## 🎯 Use Cases

### 🏢 For Organizations

**1. Security & Compliance**
- ✅ Maintain up-to-date firewall rules for Google services
- ✅ Audit trail for regulatory compliance (SOC2, ISO 27001)
- ✅ Detect unauthorized IP range changes
- ✅ Export rules for automated deployment pipelines

**2. Network Administration**
- ✅ Update VPN and proxy configurations automatically
- ✅ Maintain accurate routing tables
- ✅ Monitor Google Cloud infrastructure expansion
- ✅ Generate router configs for Cisco/MikroTik

**3. DevOps & SRE**
- ✅ Sync infrastructure-as-code with latest Google IPs
- ✅ Prevent service disruptions due to IP changes
- ✅ Automate terraform/ansible configuration updates
- ✅ Import into AWS/Azure security groups

### 👤 For Individuals

**4. Email Security**
- ✅ Validate Google Workspace sender IPs
- ✅ Update SPF records for custom domains
- ✅ Detect email spoofing attempts
- ✅ Configure mail server whitelists

**5. API Integration**
- ✅ Whitelist Google service IPs for API endpoints
- ✅ Secure webhooks and callbacks
- ✅ Validate incoming requests
- ✅ Configure CDN and WAF rules

**6. Research & Analytics**
- ✅ Track Google's infrastructure growth
- ✅ Geographic distribution analysis
- ✅ Network topology research
- ✅ Export data for custom analysis

---

## 🚀 Quick Start

### Prerequisites

- GitHub account
- Telegram account (optional but recommended)
- 5 minutes of your time

### Step 1: Create Telegram Bot (Optional)

1. Open Telegram and search for `@BotFather`
2. Send: `/newbot`
3. Follow the prompts and save your **Bot Token**
4. Get your Chat ID from `@userinfobot`

### Step 2: Fork & Configure

1. **Fork this repository**
   ```
   https://github.com/m3hr4nn/googleipmonitor
   ```

2. **Add GitHub Secrets** (if using Telegram)
   - Go to `Settings` → `Secrets and variables` → `Actions`
   - Add `TELEGRAM_BOT_TOKEN`
   - Add `TELEGRAM_CHAT_ID`

3. **Enable GitHub Actions**
   - Go to `Actions` tab
   - Click "I understand my workflows, go ahead and enable them"

4. **Enable GitHub Pages**
   - Go to `Settings` → `Pages`
   - Source: Deploy from branch `main` → `/ (root)`
   - Click **Save**

### Step 3: Run First Monitoring

```bash
Actions → Google IP Monitor → Run workflow
```

🎉 Done! Your dashboard will be live in 2-3 minutes at:
- **Dashboard**: `https://YOUR_USERNAME.github.io/googleipmonitor/`
- **Chart Analytics**: `https://YOUR_USERNAME.github.io/googleipmonitor/exports/charts/`
- **Firewall Exports**: `https://YOUR_USERNAME.github.io/googleipmonitor/exports/`

---

## 📊 Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                GitHub Actions (Every 3 Hours)                        │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────────────────┐ │
│  │  Fetch IPs  │──▶│ Compare Data │──▶│ Generate Dashboard      │ │
│  │  from Google│   │  Find Changes│   │  + Charts (via Gateway) │ │
│  └─────────────┘   └──────────────┘   └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
           │                    │                         │
           ▼                    ▼                         ▼
    ┌──────────┐         ┌──────────┐             ┌──────────┐
    │   Git    │         │ Telegram │             │  GitHub  │
    │ History  │         │   Bot    │             │  Pages   │
    │ + Cache  │         │          │             │ Dashboard│
    └──────────┘         └──────────┘             └──────────┘
```

### Microservices Architecture (v1.1.0+)

```
generate_report.py
    ↓
ChartAPIGateway (Orchestrator)
    ↓
    ├→ [1] DataAggregatorService ────▶ cache/metrics.json
    ↓
    ├→ [2] ChartConfigService ────────▶ cache/chart_configs.json
    ↓
    ├→ [3] ChartRendererService ──────▶ HTML/JavaScript
    ↓
    └→ [4] ChartExportService ─────────▶ exports/charts/*
    ↓
Return to generate_report.py ──▶ Inject into index.html
```

**5 Independent Microservices:**
1. **DataAggregatorService** - Parse historical data and compute metrics
2. **ChartConfigService** - Generate Chart.js configurations
3. **ChartRendererService** - Render HTML/JavaScript components
4. **ChartExportService** - Export data in multiple formats
5. **ChartAPIGateway** - Orchestrate all services with error handling

For detailed architecture documentation, see [CLAUDE.md](CLAUDE.md)

---

## 🔥 Firewall Export Guide

### Quick Export

1. Visit: `https://YOUR_USERNAME.github.io/googleipmonitor/exports/`
2. Click on your desired format
3. Download and deploy!

### Format Details

#### 🐧 **iptables** 
```bash
# Download and apply
wget https://YOUR_USERNAME.github.io/googleipmonitor/exports/iptables.sh
chmod +x iptables.sh
sudo ./iptables.sh
```

#### ☁️ **AWS Security Group**
```bash
# Import via AWS CLI
aws ec2 create-security-group \
  --group-name google-ips \
  --description "Google IP Ranges" \
  --cli-input-json file://aws-security-group.json
```

#### 🔷 **Azure NSG**
```bash
# Import via Azure CLI
az network nsg create \
  --resource-group myResourceGroup \
  --name GoogleIPs
az network nsg rule create \
  --nsg-name GoogleIPs \
  --cli-input-json @azure-nsg.json
```

#### 🌐 **Cisco ACL**
```
! Copy/paste into Cisco IOS config
! File: cisco-acl.txt
configure terminal
[paste contents here]
end
write memory
```

#### 🛡️ **pfSense**
```
1. Go to Firewall > Aliases
2. Click "Import"
3. Upload pfsense-alias.txt
4. Apply changes
```

#### 🔧 **MikroTik**
```
# Upload and execute
/import file=mikrotik.rsc
```

---

## 🛠️ Configuration

### Customize Schedule

Edit `.github/workflows/monitor.yml`:

```yaml
schedule:
  # Run every 3 hours (default)
  - cron: '0 */3 * * *'
  
  # Or run every hour
  - cron: '0 * * * *'
  
  # Or run twice daily at 9 AM and 9 PM UTC
  - cron: '0 9,21 * * *'
```

### Add More Data Sources

Edit `monitor.py`:

```python
self.urls = {
    'cloud': 'https://www.gstatic.com/ipranges/cloud.json',
    'goog': 'https://www.gstatic.com/ipranges/goog.json',
    'custom': 'https://your-source.com/ips.json'  # Add your source
}
```

### Customize Charts

Edit `config/chart_settings.json`:

```json
{
  "enabled": true,
  "days_to_show": 90,
  "charts": {
    "line_chart": {"enabled": true, "height": 400},
    "bar_chart": {"enabled": true, "height": 350},
    "pie_chart": {"enabled": true, "height": 320}
  }
}
```

### Customize Theme

Edit `styles.css` to change colors:

```css
:root {
    --accent-blue: #8ab4f8;   /* Primary accent */
    --accent-green: #81c995;  /* Success/additions */
    --accent-red: #f28b82;    /* Errors/removals */
}
```

### Disable Telegram (Export Only Mode)

If you just want exports without Telegram notifications:
1. Don't add the Telegram secrets
2. The workflow will still run and generate exports
3. You'll see "Telegram credentials not set" in logs (this is fine)

---

## 🔮 Roadmap

See the detailed [ROADMAP.md](ROADMAP.md) for:
- ✅ Completed features (v1.0.0 - v1.1.0)
- 🚧 In-progress development
- 📋 Planned features with timelines
- 💡 Feature request process
- 📅 Release schedule

**Want a feature?** [Create an issue](https://github.com/m3hr4nn/googleipmonitor/issues) or vote with 👍 on existing requests!

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test your changes locally before submitting
- Update documentation if you add new features

---

## 📝 Development

### Local Setup

```bash
# Clone the repo
git clone https://github.com/m3hr4nn/googleipmonitor.git
cd googleipmonitor

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"

# Run locally
python monitor.py                    # Fetch and compare IPs
python generate_report.py            # Generate dashboard with charts
python generate_firewall_rules.py    # Generate exports

# Test microservices (v1.1.0+)
python services/chart_api_gateway.py # Test full chart pipeline

# View locally
open index.html                      # Main dashboard
open exports/charts/index.html       # Chart data exports
open exports/index.html              # Firewall exports
```

### Project Structure

```
googleipmonitor/
├── .github/workflows/
│   └── monitor.yml              # GitHub Actions (every 3 hours)
├── services/                    # 🆕 Microservices (v1.1.0)
│   ├── aggregator_service.py    # Data aggregation
│   ├── chart_config_service.py  # Chart configurations
│   ├── chart_renderer_service.py # HTML rendering
│   ├── chart_export_service.py  # Data exports
│   └── chart_api_gateway.py     # Service orchestrator
├── config/                      # 🆕 Configuration (v1.1.0)
│   └── chart_settings.json      # Chart customization
├── cache/                       # 🆕 Service cache (v1.1.0)
│   ├── metrics.json             # Aggregated metrics
│   └── chart_configs.json       # Chart.js configs
├── data/                        # Historical IP snapshots
│   └── YYYY-MM-DD.json
├── exports/
│   ├── charts/                  # 🆕 Chart data exports (v1.1.0)
│   │   ├── index.html
│   │   ├── historical_metrics.csv
│   │   ├── historical_metrics.json
│   │   └── summary.md
│   ├── index.html               # Firewall export dashboard
│   ├── iptables.sh              # Linux firewall
│   ├── aws-security-group.json  # AWS format
│   ├── azure-nsg.json           # Azure format
│   ├── cisco-acl.txt            # Cisco IOS
│   ├── pfsense-alias.txt        # pfSense
│   ├── mikrotik.rsc             # MikroTik
│   ├── plain-text.txt           # Plain text
│   ├── export.csv               # CSV format
│   └── export.json              # JSON format
├── monitor.py                   # Core monitoring logic
├── generate_report.py           # Dashboard + charts generator
├── generate_firewall_rules.py   # Firewall export generator
├── styles.css                   # Dashboard styling
├── index.html                   # Main dashboard (auto-generated)
├── CLAUDE.md                    # Architecture documentation
├── ROADMAP.md                   # 🆕 Product roadmap (v1.1.0)
├── requirements.txt             # Python dependencies
└── README.md                    # You are here!
```

### Adding a New Export Format

1. Edit `generate_firewall_rules.py`
2. Add your generator method:

```python
def generate_your_format(self, ipv4_prefixes, ipv6_prefixes):
    rules = []
    # Your format logic here
    for ip in ipv4_prefixes:
        rules.append(f"your-format: {ip}")
    return "\n".join(rules)
```

3. Add to the `formats` dictionary in `generate_all()`:

```python
formats = {
    'your-format.txt': self.generate_your_format,
    # ... other formats
}
```

4. Update the exports index page to include your format

---

## 📊 Dashboard Preview

### 🌐 Main Dashboard
Beautiful dark-themed interface with real-time statistics, interactive charts, and change tracking.

**Features:**
- 📊 Live statistics cards (Previous Day, Current Day, Net Change, IPv4/IPv6)
- 📈 Interactive charts (Line, Bar, Pie charts with Chart.js)
- 🎨 Chrome-inspired dark theme
- 🔥 Integrated exports with 9 formats
- 📱 Fully responsive design

**👉 [View Live Dashboard](https://m3hr4nn.github.io/googleipmonitor/)**

### 📈 Chart Analytics Page
Export and analyze historical IP range metrics.

**Available Exports:**
- 📊 CSV for Excel analysis
- 📦 JSON for API consumption
- 📄 Markdown for documentation

**👉 [Browse Chart Data](https://m3hr4nn.github.io/googleipmonitor/exports/charts/)**

### 🔥 Firewall Export Page
Download ready-to-use firewall rules in your preferred format.

**Available Formats:**
- 🐧 iptables/ip6tables • ☁️ AWS Security Group • 🔷 Azure NSG
- 🌐 Cisco ACL • 🛡️ pfSense • 🔧 MikroTik RouterOS
- 📄 Plain Text • 📊 CSV • 📦 JSON

**👉 [Browse Exports](https://m3hr4nn.github.io/googleipmonitor/exports/)**

---

## ❓ FAQ

<details>
<summary><b>How often does it check for changes?</b></summary>
Every 3 hours (8 times per day). You can customize this in the workflow file.
</details>

<details>
<summary><b>What firewall formats are supported?</b></summary>
Currently: iptables, AWS Security Group, Azure NSG, Cisco ACL, pfSense, MikroTik, CSV, JSON, and Plain Text. More formats can be added easily!
</details>

<details>
<summary><b>Do I need Telegram to use this?</b></summary>
No! Telegram is optional. The dashboard and exports work without it. Just don't add the Telegram secrets.
</details>

<details>
<summary><b>How do I import rules into my firewall?</b></summary>
Check the "Firewall Export Guide" section above for specific instructions for each format.
</details>

<details>
<summary><b>Can I monitor other IP sources besides Google?</b></summary>
Yes! Add any JSON/text IP source to the `urls` dictionary in `monitor.py`.
</details>

<details>
<summary><b>Will this use up my GitHub Actions quota?</b></summary>
No. With 2,000 free minutes/month and ~2 minutes per run, you use only 480 minutes/month (24% of quota).
</details>

<details>
<summary><b>Can I run this on my own server?</b></summary>
Yes! Set up a cron job to run the Python scripts. But GitHub Actions is easier and free!
</details>

<details>
<summary><b>How do I update to the latest version?</b></summary>
Sync your fork with the upstream repository, or manually copy new files from the main repo.
</details>

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=m3hr4nn/googleipmonitor&type=Date)](https://star-history.com/#m3hr4nn/googleipmonitor&Date)

---

## 💬 Support

- 📧 Issues: [GitHub Issues](https://github.com/m3hr4nn/googleipmonitor/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/m3hr4nn/googleipmonitor/discussions)
- 🌐 Dashboard: [Live Demo](https://m3hr4nn.github.io/googleipmonitor/)
- 🔥 Exports: [Export Page](https://m3hr4nn.github.io/googleipmonitor/exports/)

---

## 🙏 Acknowledgments

- [Google Cloud IP Ranges](https://www.gstatic.com/ipranges/cloud.json)
- [GitHub Actions](https://github.com/features/actions)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Roboto Font Family](https://fonts.google.com/specimen/Roboto)
- All contributors and users of this project

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/m3hr4nn/googleipmonitor?style=social)
![GitHub forks](https://img.shields.io/github/forks/m3hr4nn/googleipmonitor?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/m3hr4nn/googleipmonitor?style=social)

![GitHub last commit](https://img.shields.io/github/last-commit/m3hr4nn/googleipmonitor)
![GitHub issues](https://img.shields.io/github/issues/m3hr4nn/googleipmonitor)
![GitHub pull requests](https://img.shields.io/github/issues-pr/m3hr4nn/googleipmonitor)

---

<div align="center">

**Made with ❤️ for the DevOps community**

**If you find this useful, please consider giving it a ⭐️**

[⬆ Back to Top](#-google-ip-monitor)

</div>
