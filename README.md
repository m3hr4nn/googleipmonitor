# Google IP Monitor

Google IP Monitor watches Google Cloud and Google public IP ranges, detects prefix changes, sends optional Telegram alerts, and publishes a static dashboard through GitHub Pages.

## How it works

GitHub Actions runs the pipeline every three hours:

1. `monitor.py` fetches `cloud.json` and `goog.json`, compares them with the latest saved snapshot, and writes `data/YYYY-MM-DD.json`.
2. `generate_report.py` builds the one-page dashboard and interactive Chart.js analytics.
3. `generate_firewall_rules.py` creates rules for iptables, AWS, Azure, Cisco, pfSense, MikroTik, plain text, CSV, and JSON.
4. Generated data, charts, exports, and dashboard files are committed and published by GitHub Pages.

## Benefits and uses

- Detect Google IP range additions and removals automatically.
- Receive change notifications in Telegram without maintaining a server.
- Review IPv4/IPv6 counts, historical growth, and daily changes in one page.
- Download ready-to-use firewall rules for cloud, network, and Linux platforms.
- Keep an auditable history of snapshots in Git.

This is useful for firewall maintenance, allowlists, proxy and VPN rules, email security, compliance reviews, and infrastructure monitoring.

## Run locally

```bash
pip install -r requirements.txt
python3 monitor.py
python3 generate_report.py
python3 generate_firewall_rules.py
```

Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to enable alerts. Open `index.html` locally to view the dashboard. GitHub Actions requires the same values as repository secrets.

The project is MIT licensed. See `LICENSE` for details.
