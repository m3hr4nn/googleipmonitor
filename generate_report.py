import os
import json
from datetime import datetime, timedelta

def generate_html_report():
    """Generate HTML report from stored data"""
    
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Load data
    data_dir = 'data'
    today_file = os.path.join(data_dir, f'{today}.json')
    yesterday_file = os.path.join(data_dir, f'{yesterday}.json')
    
    today_data = None
    yesterday_data = None
    
    if os.path.exists(today_file):
        with open(today_file, 'r') as f:
            today_data = json.load(f)
    
    if os.path.exists(yesterday_file):
        with open(yesterday_file, 'r') as f:
            yesterday_data = json.load(f)
    
    # Extract prefixes
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
    
    # Generate HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google IP Monitor Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .header p {{
                font-size: 1.2em;
                opacity: 0.9;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .stat-card {{
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                border: 2px solid #e9ecef;
            }}
            
            .stat-card h3 {{
                color: #6c757d;
                font-size: 0.9em;
                text-transform: uppercase;
                margin-bottom: 10px;
            }}
            
            .stat-card .number {{
                font-size: 2.5em;
                font-weight: bold;
                color: #667eea;
            }}
            
            .changes-section {{
                margin-bottom: 40px;
            }}
            
            .changes-section h2 {{
                color: #333;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }}
            
            .change-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
                gap: 20px;
            }}
            
            .change-box {{
                background: #f8f9fa;
                border-radius: 15px;
                padding: 25px;
            }}
            
            .change-box.added {{
                border-left: 5px solid #28a745;
            }}
            
            .change-box.removed {{
                border-left: 5px solid #dc3545;
            }}
            
            .change-box h3 {{
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .change-box.added h3 {{
                color: #28a745;
            }}
            
            .change-box.removed h3 {{
                color: #dc3545;
            }}
            
            .ip-list {{
                max-height: 400px;
                overflow-y: auto;
                background: white;
                border-radius: 10px;
                padding: 15px;
            }}
            
            .ip-item {{
                padding: 8px;
                margin: 5px 0;
                background: #e9ecef;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }}
            
            .no-changes {{
                text-align: center;
                padding: 60px 20px;
                color: #6c757d;
            }}
            
            .no-changes .icon {{
                font-size: 4em;
                margin-bottom: 20px;
            }}
            
            .footer {{
                text-align: center;
                padding: 20px;
                color: #6c757d;
                font-size: 0.9em;
                border-top: 1px solid #e9ecef;
            }}
            
            .badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: bold;
            }}
            
            .badge.success {{
                background: #d4edda;
                color: #155724;
            }}
            
            .badge.danger {{
                background: #f8d7da;
                color: #721c24;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌐 Google IP Monitor</h1>
                <p>Daily IP Range Change Report</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stat-card">
                        <h3>Yesterday</h3>
                        <div class="number">{len(yesterday_prefixes)}</div>
                        <p>{yesterday}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Today</h3>
                        <div class="number">{len(today_prefixes)}</div>
                        <p>{today}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Net Change</h3>
                        <div class="number" style="color: {'#28a745' if len(today_prefixes) >= len(yesterday_prefixes) else '#dc3545'}">
                            {len(today_prefixes) - len(yesterday_prefixes):+d}
                        </div>
                        <p>IP Ranges</p>
                    </div>
                </div>
                
                <div class="changes-section">
                    <h2>📊 Changes Detected</h2>
                    
                    {f'''
                    <div class="change-grid">
                        <div class="change-box added">
                            <h3>
                                <span>➕</span>
                                <span>Added Ranges</span>
                                <span class="badge success">{len(added)}</span>
                            </h3>
                            <div class="ip-list">
                                {"".join([f'<div class="ip-item">{ip}</div>' for ip in added]) if added else '<p style="text-align:center;color:#6c757d;">No ranges added</p>'}
                            </div>
                        </div>
                        
                        <div class="change-box removed">
                            <h3>
                                <span>➖</span>
                                <span>Removed Ranges</span>
                                <span class="badge danger">{len(removed)}</span>
                            </h3>
                            <div class="ip-list">
                                {"".join([f'<div class="ip-item">{ip}</div>' for ip in removed]) if removed else '<p style="text-align:center;color:#6c757d;">No ranges removed</p>'}
                            </div>
                        </div>
                    </div>
                    ''' if (added or removed) else '''
                    <div class="no-changes">
                        <div class="icon">✅</div>
                        <h3>No Changes Detected</h3>
                        <p>All IP ranges remain unchanged from yesterday</p>
                    </div>
                    '''}
                </div>
            </div>
            
            <div class="footer">
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p>Monitoring Google Cloud and Public IP Ranges</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save HTML
    with open('index.html', 'w') as f:
        f.write(html)
    
    print("HTML report generated: index.html")

if __name__ == '__main__':
    generate_html_report()
