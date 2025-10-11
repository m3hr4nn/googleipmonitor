import os
import json
from datetime import datetime, timedelta
from glob import glob

def generate_html_report():
    data_dir = 'data'
    
    # Get all available data files
    data_files = sorted(glob(os.path.join(data_dir, '*.json')))
    
    if len(data_files) == 0:
        print("No data files found")
        return
    
    # Get the two most recent files
    if len(data_files) >= 2:
        yesterday_file = data_files[-2]
        today_file = data_files[-1]
    else:
        # First run - use the same file for both
        yesterday_file = data_files[-1]
        today_file = data_files[-1]
    
    print(f"Using files: {yesterday_file} and {today_file}")
    
    today_data = None
    yesterday_data = None
    
    with open(today_file, 'r') as f:
        today_data = json.load(f)
    
    with open(yesterday_file, 'r') as f:
        yesterday_data = json.load(f)
    
    # Extract dates from filenames
    today_date = os.path.basename(today_file).replace('.json', '')
    yesterday_date = os.path.basename(yesterday_file).replace('.json', '')
    
    def extract_prefixes(data):
        if not data:
            return set()
        prefixes = set()
        if data.get('cloud'):
            for p in data['cloud'].get('prefixes', []):
                if 'ipv4Prefix' in p:
                    prefixes.add(p['ipv4Prefix'])
                if 'ipv6Prefix' in p:
                    prefixes.add(p['ipv6Prefix'])
        if data.get('goog'):
            for p in data['goog'].get('prefixes', []):
                if 'ipv4Prefix' in p:
                    prefixes.add(p['ipv4Prefix'])
                if 'ipv6Prefix' in p:
                    prefixes.add(p['ipv6Prefix'])
        return prefixes
    
    today_prefixes = extract_prefixes(today_data)
    yesterday_prefixes = extract_prefixes(yesterday_data)
    
    added = sorted(list(today_prefixes - yesterday_prefixes))
    removed = sorted(list(yesterday_prefixes - today_prefixes))
    
    # Separate IPv4 and IPv6 for detailed stats
    today_ipv4 = sorted([ip for ip in today_prefixes if ':' not in ip])
    today_ipv6 = sorted([ip for ip in today_prefixes if ':' in ip])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google IP Monitor - Dashboard</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="header-left">
                <div class="logo">
                    <span class="logo-icon">🌐</span>
                    <h1>Google IP Monitor</h1>
                </div>
            </div>
            <div class="header-right">
                <div class="last-update">Last update: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</div>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="content">
            <div class="stats">
                <div class="stat-card previous">
                    <h3>Previous Day</h3>
                    <div class="number">{len(yesterday_prefixes):,}</div>
                    <p>{yesterday_date}</p>
                </div>
                <div class="stat-card current">
                    <h3>Current Day</h3>
                    <div class="number">{len(today_prefixes):,}</div>
                    <p>{today_date}</p>
                </div>
                <div class="stat-card change">
                    <h3>Net Change</h3>
                    <div class="number {'positive' if len(today_prefixes) >= len(yesterday_prefixes) else 'negative'}">{len(today_prefixes) - len(yesterday_prefixes):+d}</div>
                    <p>IP Ranges</p>
                </div>
                <div class="stat-card">
                    <h3>IPv4 Ranges</h3>
                    <div class="number">{len(today_ipv4):,}</div>
                    <p>Active</p>
                </div>
                <div class="stat-card">
                    <h3>IPv6 Ranges</h3>
                    <div class="number">{len(today_ipv6):,}</div>
                    <p>Active</p>
                </div>
            </div>

            <div class="changes-section">
                <div class="section-header">
                    <h2>📊 Changes Detected</h2>
                    <span class="badge">{len(added) + len(removed)} total changes</span>
                </div>
                {f'''<div class="change-grid">
                    <div class="change-box added">
                        <div class="change-box-header">
                            <div class="change-box-title">
                                <h3>➕ Added</h3>
                            </div>
                            <span class="count-badge">{len(added)}</span>
                        </div>
                        <div class="ip-list">{''.join([f'<div class="ip-item">{ip}</div>' for ip in added[:100]]) if added else '<div class="empty-state"><p>No ranges added</p></div>'}</div>
                    </div>
                    <div class="change-box removed">
                        <div class="change-box-header">
                            <div class="change-box-title">
                                <h3>➖ Removed</h3>
                            </div>
                            <span class="count-badge">{len(removed)}</span>
                        </div>
                        <div class="ip-list">{''.join([f'<div class="ip-item">{ip}</div>' for ip in removed[:100]]) if removed else '<div class="empty-state"><p>No ranges removed</p></div>'}</div>
                    </div>
                </div>''' if (added or removed) else '''<div class="no-changes">
                    <div class="icon">✅</div>
                    <h3>No Changes Detected</h3>
                    <p>All IP ranges remain unchanged</p>
                </div>'''}
            </div>

            <div class="changes-section">
                <div class="section-header">
                    <h2>🔥 Firewall Rules Export</h2>
                    <span class="badge">9 formats available</span>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; margin-bottom: 32px;">
                    <a href="exports/iptables.sh" download class="export-card">
                        <div class="export-icon">🐧</div>
                        <h3>iptables</h3>
                        <p>Linux firewall rules</p>
                        <span class="download-badge">Download .sh</span>
                    </a>

                    <a href="exports/aws-security-group.json" download class="export-card">
                        <div class="export-icon">☁️</div>
                        <h3>AWS Security Group</h3>
                        <p>Amazon Web Services</p>
                        <span class="download-badge">Download .json</span>
                    </a>

                    <a href="exports/azure-nsg.json" download class="export-card">
                        <div class="export-icon">🔷</div>
                        <h3>Azure NSG</h3>
                        <p>Microsoft Azure</p>
                        <span class="download-badge">Download .json</span>
                    </a>

                    <a href="exports/cisco-acl.txt" download class="export-card">
                        <div class="export-icon">🌐</div>
                        <h3>Cisco ACL</h3>
                        <p>Cisco IOS access lists</p>
                        <span class="download-badge">Download .txt</span>
                    </a>

                    <a href="exports/pfsense-alias.txt" download class="export-card">
                        <div class="export-icon">🛡️</div>
                        <h3>pfSense</h3>
                        <p>pfSense firewall alias</p>
                        <span class="download-badge">Download .txt</span>
                    </a>

                    <a href="exports/mikrotik.rsc" download class="export-card">
                        <div class="export-icon">🔧</div>
                        <h3>MikroTik</h3>
                        <p>RouterOS script</p>
                        <span class="download-badge">Download .rsc</span>
                    </a>

                    <a href="exports/plain-text.txt" download class="export-card">
                        <div class="export-icon">📄</div>
                        <h3>Plain Text</h3>
                        <p>Simple text list</p>
                        <span class="download-badge">Download .txt</span>
                    </a>

                    <a href="exports/export.csv" download class="export-card">
                        <div class="export-icon">📊</div>
                        <h3>CSV</h3>
                        <p>Comma-separated values</p>
                        <span class="download-badge">Download .csv</span>
                    </a>

                    <a href="exports/export.json" download class="export-card">
                        <div class="export-icon">📦</div>
                        <h3>JSON</h3>
                        <p>Structured JSON data</p>
                        <span class="download-badge">Download .json</span>
                    </a>
                </div>

                <div style="text-align: center;">
                    <a href="exports/index.html" style="color: var(--accent-blue); text-decoration: none; font-size: 14px;">
                        View all export formats →
                    </a>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>Monitoring Google Cloud and Public IP Ranges • <a href="https://github.com/m3hr4nn/googleipmonitor" target="_blank">GitHub</a></p>
        </div>
    </div>

    <style>
        .export-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            text-decoration: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .export-card:hover {{
            background-color: var(--bg-tertiary);
            border-color: var(--accent-blue);
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        }}

        .export-icon {{
            font-size: 48px;
            margin-bottom: 12px;
        }}

        .export-card h3 {{
            color: var(--text-primary);
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 8px;
        }}

        .export-card p {{
            color: var(--text-secondary);
            font-size: 13px;
            margin-bottom: 16px;
        }}

        .download-badge {{
            background-color: var(--accent-blue);
            color: var(--bg-primary);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }}

        .export-card:hover .download-badge {{
            background-color: var(--accent-green);
        }}
    </style>
</body>
</html>"""
    
    with open('index.html', 'w') as f:
        f.write(html)
    
    print("✅ HTML report generated: index.html")

if __name__ == '__main__':
    generate_html_report()



