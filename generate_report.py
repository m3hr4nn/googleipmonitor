import json
import os
from datetime import datetime
from glob import glob

from services.chart_api_gateway import ChartAPIGateway


def extract_prefixes(data):
    """Return unique IPv4 and IPv6 prefixes from a Google snapshot."""
    if not data:
        return set()

    prefixes = set()
    for source in ('cloud', 'goog'):
        if not data.get(source):
            continue
        for entry in data[source].get('prefixes', []):
            prefixes.update(
                value for key, value in entry.items()
                if key in ('ipv4Prefix', 'ipv6Prefix')
            )
    return prefixes


def render_ip_items(prefixes):
    """Render a bounded list of prefixes for the dashboard."""
    return ''.join(
        f'<div class="ip-item"><code>{prefix}</code></div>'
        for prefix in prefixes[:100]
    )


def render_changes(added, removed):
    """Render the change state for the current snapshot."""
    if not added and not removed:
        return '''
                <div class="no-changes">
                    <div class="no-changes-icon">✓</div>
                    <div>
                        <h3>No changes detected</h3>
                        <p>Google’s published ranges match the previous snapshot.</p>
                    </div>
                </div>'''

    return f'''
                <div class="change-grid">
                    <article class="change-box added">
                        <div class="change-box-header">
                            <div class="change-box-title">
                                <span class="change-icon">+</span>
                                <h3>Added ranges</h3>
                            </div>
                            <span class="count-badge">{len(added)}</span>
                        </div>
                        <div class="ip-list">{render_ip_items(added) or '<div class="empty-state"><p>No ranges added</p></div>'}</div>
                    </article>
                    <article class="change-box removed">
                        <div class="change-box-header">
                            <div class="change-box-title">
                                <span class="change-icon">−</span>
                                <h3>Removed ranges</h3>
                            </div>
                            <span class="count-badge">{len(removed)}</span>
                        </div>
                        <div class="ip-list">{render_ip_items(removed) or '<div class="empty-state"><p>No ranges removed</p></div>'}</div>
                    </article>
                </div>'''


def generate_html_report():
    data_dir = 'data'

    print("\n🚀 Initializing Chart API Gateway...")
    chart_result = ChartAPIGateway().run()

    data_files = sorted(glob(os.path.join(data_dir, '*.json')))
    if not data_files:
        print("No data files found")
        return

    if len(data_files) >= 2:
        previous_file, current_file = data_files[-2:]
    else:
        previous_file = current_file = data_files[-1]

    print(f"Using files: {previous_file} and {current_file}")

    with open(current_file, 'r') as file:
        current_data = json.load(file)
    with open(previous_file, 'r') as file:
        previous_data = json.load(file)

    current_date = os.path.basename(current_file).replace('.json', '')
    previous_date = os.path.basename(previous_file).replace('.json', '')

    current_prefixes = extract_prefixes(current_data)
    previous_prefixes = extract_prefixes(previous_data)
    added = sorted(current_prefixes - previous_prefixes)
    removed = sorted(previous_prefixes - current_prefixes)
    current_ipv4 = sorted(prefix for prefix in current_prefixes if ':' not in prefix)
    current_ipv6 = sorted(prefix for prefix in current_prefixes if ':' in prefix)
    total_changes = len(added) + len(removed)
    net_change = len(current_prefixes) - len(previous_prefixes)
    change_class = 'positive' if net_change >= 0 else 'negative'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0b1020">
    <title>Google IP Monitor · Network intelligence</title>
    <link rel="stylesheet" href="styles.css">
    {chart_result.get('cdn_script', '')}
</head>
<body>
    <div class="ambient-glow glow-a"></div>
    <div class="ambient-glow glow-b"></div>

    <header class="site-header">
        <div class="header-content">
            <a class="brand" href="#overview" aria-label="Google IP Monitor home">
                <span class="brand-mark" aria-hidden="true">
                    <svg viewBox="0 0 32 32" role="img"><circle cx="16" cy="16" r="12"></circle><path d="M4 16h24M16 4c3.2 3.3 4.7 7.3 4.7 12S19.2 24.7 16 28c-3.2-3.3-4.7-7.3-4.7-12S12.8 7.3 16 4Z"></path></svg>
                </span>
                <span class="brand-copy"><strong>Google IP Monitor</strong><small>Network intelligence</small></span>
            </a>
            <nav class="header-nav" aria-label="Dashboard sections">
                <a href="#overview">Overview</a>
                <a href="#analytics">Analytics</a>
                <a href="#changes">Changes</a>
                <a href="#exports">Exports</a>
            </nav>
            <div class="last-update"><span class="status-dot" aria-hidden="true"></span><span>Updated {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</span></div>
        </div>
    </header>

    <main class="page-shell">
        <section class="hero" id="overview">
            <div class="hero-copy">
                <span class="eyebrow"><span class="eyebrow-pulse"></span> Live network telemetry</span>
                <h1>Google IP ranges,<br><span>at a glance.</span></h1>
                <p>Track Google Cloud and public IP infrastructure with a clear, continuously updated view of growth, changes, and ready-to-use firewall rules.</p>
                <div class="hero-actions">
                    <a class="button button-primary" href="#analytics">Explore analytics <span>↓</span></a>
                    <a class="button button-secondary" href="#exports">Download rules <span>↗</span></a>
                </div>
            </div>
            <div class="hero-panel glass-panel">
                <div class="panel-topline"><span>MONITOR STATUS</span><span class="live-pill"><span class="status-dot"></span>Operational</span></div>
                <div class="signal-visual" aria-hidden="true">
                    <div class="signal-ring ring-one"></div>
                    <div class="signal-ring ring-two"></div>
                    <div class="signal-core"><span>LIVE</span><strong>24/7</strong></div>
                </div>
                <div class="hero-panel-footer">
                    <div><strong>{len(current_prefixes):,}</strong><span>active ranges</span></div>
                    <div><strong>{total_changes:,}</strong><span>changes in view</span></div>
                </div>
            </div>
        </section>

        <section class="snapshot-section" aria-labelledby="snapshot-title">
            <div class="section-intro">
                <div><span class="section-kicker">Latest snapshot</span><h2 id="snapshot-title">A sharper view of the network</h2></div>
                <p>Comparing <strong>{current_date}</strong> with <strong>{previous_date}</strong></p>
            </div>
            <div class="stats">
                <article class="stat-card previous"><div class="stat-card-top"><span class="stat-icon">◷</span><span>Baseline</span></div><h3>Previous snapshot</h3><div class="number">{len(previous_prefixes):,}</div><p>{previous_date}</p></article>
                <article class="stat-card current"><div class="stat-card-top"><span class="stat-icon">◉</span><span class="live-label">Live</span></div><h3>Current ranges</h3><div class="number">{len(current_prefixes):,}</div><p>{current_date}</p></article>
                <article class="stat-card change"><div class="stat-card-top"><span class="stat-icon">↗</span><span>Delta</span></div><h3>Net change</h3><div class="number {change_class}">{net_change:+d}</div><p>IP ranges</p></article>
                <article class="stat-card ipv4-card"><div class="stat-card-top"><span class="stat-icon">4</span><span>Protocol</span></div><h3>IPv4 ranges</h3><div class="number">{len(current_ipv4):,}</div><p>Active prefixes</p></article>
                <article class="stat-card ipv6-card"><div class="stat-card-top"><span class="stat-icon">6</span><span>Protocol</span></div><h3>IPv6 ranges</h3><div class="number">{len(current_ipv6):,}</div><p>Active prefixes</p></article>
            </div>
        </section>

        {chart_result.get('charts_section', '')}

        <section class="changes-section" id="changes">
            <div class="section-header"><div><span class="section-kicker">Diff monitor</span><h2>What changed?</h2></div><span class="badge">{total_changes} total changes</span></div>
            {render_changes(added, removed)}
        </section>

        <section class="exports-section" id="exports">
            <div class="section-header"><div><span class="section-kicker">Ready for production</span><h2>Firewall rule exports</h2></div><span class="badge">9 formats</span></div>
            <p class="section-description">Take the latest Google ranges into your existing security workflow.</p>
            <div class="export-grid">
                <a href="exports/iptables.sh" download class="export-card"><span class="export-icon">⌘</span><span class="export-card-copy"><h3>iptables</h3><p>Linux firewall rules</p></span><span class="download-badge">.sh ↗</span></a>
                <a href="exports/aws-security-group.json" download class="export-card"><span class="export-icon">☁</span><span class="export-card-copy"><h3>AWS Security Group</h3><p>Amazon Web Services</p></span><span class="download-badge">.json ↗</span></a>
                <a href="exports/azure-nsg.json" download class="export-card"><span class="export-icon">◆</span><span class="export-card-copy"><h3>Azure NSG</h3><p>Microsoft Azure</p></span><span class="download-badge">.json ↗</span></a>
                <a href="exports/cisco-acl.txt" download class="export-card"><span class="export-icon">◈</span><span class="export-card-copy"><h3>Cisco ACL</h3><p>Cisco IOS access lists</p></span><span class="download-badge">.txt ↗</span></a>
                <a href="exports/pfsense-alias.txt" download class="export-card"><span class="export-icon">◇</span><span class="export-card-copy"><h3>pfSense</h3><p>Firewall alias</p></span><span class="download-badge">.txt ↗</span></a>
                <a href="exports/mikrotik.rsc" download class="export-card"><span class="export-icon">⌁</span><span class="export-card-copy"><h3>MikroTik</h3><p>RouterOS script</p></span><span class="download-badge">.rsc ↗</span></a>
                <a href="exports/plain-text.txt" download class="export-card"><span class="export-icon">≡</span><span class="export-card-copy"><h3>Plain text</h3><p>Simple prefix list</p></span><span class="download-badge">.txt ↗</span></a>
                <a href="exports/export.csv" download class="export-card"><span class="export-icon">▦</span><span class="export-card-copy"><h3>CSV</h3><p>Spreadsheet compatible</p></span><span class="download-badge">.csv ↗</span></a>
                <a href="exports/export.json" download class="export-card"><span class="export-icon">{{ }}</span><span class="export-card-copy"><h3>JSON</h3><p>Structured data</p></span><span class="download-badge">.json ↗</span></a>
            </div>
            <div class="analytics-exports">
                <div class="section-header compact-header"><div><span class="section-kicker">Bring the data with you</span><h2>Historical data exports</h2></div><span class="badge">3 formats</span></div>
                <div class="export-grid export-grid-compact">
                    <a href="exports/charts/historical_metrics.csv" download class="export-card compact"><span class="export-icon">▦</span><span class="export-card-copy"><h3>Historical CSV</h3><p>Excel-compatible trends</p></span><span class="download-badge">.csv ↗</span></a>
                    <a href="exports/charts/historical_metrics.json" download class="export-card compact"><span class="export-icon">{{ }}</span><span class="export-card-copy"><h3>Historical JSON</h3><p>API-friendly metrics</p></span><span class="download-badge">.json ↗</span></a>
                    <a href="exports/charts/summary.md" download class="export-card compact"><span class="export-icon">✦</span><span class="export-card-copy"><h3>Summary report</h3><p>Readable markdown brief</p></span><span class="download-badge">.md ↗</span></a>
                </div>
            </div>
        </section>

        <footer class="footer"><p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p><p>Monitoring Google Cloud and Public IP Ranges · <a href="https://github.com/m3hr4nn/googleipmonitor" target="_blank" rel="noopener">View source on GitHub ↗</a></p></footer>
    </main>
</body>
</html>"""

    with open('index.html', 'w') as file:
        clean_html = '\n'.join(line.rstrip() for line in html.splitlines()) + '\n'
        file.write(clean_html)

    print("✅ HTML report generated: index.html")


if __name__ == '__main__':
    generate_html_report()
