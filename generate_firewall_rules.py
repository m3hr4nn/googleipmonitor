import os
import json
from datetime import datetime
from glob import glob

class FirewallRulesGenerator:
    def __init__(self):
        self.data_dir = 'data'
        self.export_dir = 'exports'
        os.makedirs(self.export_dir, exist_ok=True)
    
    def load_latest_data(self):
        """Load the most recent IP data"""
        data_files = sorted(glob(os.path.join(self.data_dir, '*.json')))
        if not data_files:
            print("No data files found")
            return None
        
        latest_file = data_files[-1]
        print(f"Loading data from: {latest_file}")
        
        with open(latest_file, 'r') as f:
            return json.load(f)
    
    def extract_prefixes(self, data):
        """Extract IPv4 and IPv6 prefixes separately"""
        ipv4_prefixes = []
        ipv6_prefixes = []
        
        if data.get('cloud'):
            for p in data['cloud'].get('prefixes', []):
                if 'ipv4Prefix' in p:
                    ipv4_prefixes.append(p['ipv4Prefix'])
                if 'ipv6Prefix' in p:
                    ipv6_prefixes.append(p['ipv6Prefix'])
        
        if data.get('goog'):
            for p in data['goog'].get('prefixes', []):
                if 'ipv4Prefix' in p:
                    ipv4_prefixes.append(p['ipv4Prefix'])
                if 'ipv6Prefix' in p:
                    ipv6_prefixes.append(p['ipv6Prefix'])
        
        return sorted(set(ipv4_prefixes)), sorted(set(ipv6_prefixes))
    
    def generate_iptables(self, ipv4_prefixes, ipv6_prefixes):
        """Generate iptables rules"""
        rules = []
        rules.append("#!/bin/bash")
        rules.append("# Google IP Ranges - iptables rules")
        rules.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        rules.append("# Allow incoming traffic from Google IPs")
        rules.append("")
        
        rules.append("# IPv4 Rules")
        for ip in ipv4_prefixes:
            rules.append(f"iptables -A INPUT -s {ip} -j ACCEPT")
        
        rules.append("")
        rules.append("# IPv6 Rules")
        for ip in ipv6_prefixes:
            rules.append(f"ip6tables -A INPUT -s {ip} -j ACCEPT")
        
        return "\n".join(rules)
    
    def generate_aws_security_group(self, ipv4_prefixes, ipv6_prefixes):
        """Generate AWS Security Group JSON"""
        rules = {
            "Description": "Google IP Ranges Security Group",
            "GroupName": "google-ip-ranges",
            "IpPermissions": []
        }
        
        # Add IPv4 rules
        for ip in ipv4_prefixes:
            rules["IpPermissions"].append({
                "IpProtocol": "-1",
                "IpRanges": [{"CidrIp": ip, "Description": "Google IP Range"}]
            })
        
        # Add IPv6 rules
        for ip in ipv6_prefixes:
            rules["IpPermissions"].append({
                "IpProtocol": "-1",
                "Ipv6Ranges": [{"CidrIpv6": ip, "Description": "Google IPv6 Range"}]
            })
        
        return json.dumps(rules, indent=2)
    
    def generate_azure_nsg(self, ipv4_prefixes, ipv6_prefixes):
        """Generate Azure NSG rules JSON"""
        rules = {
            "securityRules": []
        }
        
        priority = 100
        for idx, ip in enumerate(ipv4_prefixes):
            rules["securityRules"].append({
                "name": f"AllowGoogleIPv4_{idx+1}",
                "properties": {
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": ip,
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": priority + idx,
                    "direction": "Inbound"
                }
            })
        
        priority = 2000
        for idx, ip in enumerate(ipv6_prefixes):
            rules["securityRules"].append({
                "name": f"AllowGoogleIPv6_{idx+1}",
                "properties": {
                    "protocol": "*",
                    "sourcePortRange": "*",
                    "destinationPortRange": "*",
                    "sourceAddressPrefix": ip,
                    "destinationAddressPrefix": "*",
                    "access": "Allow",
                    "priority": priority + idx,
                    "direction": "Inbound"
                }
            })
        
        return json.dumps(rules, indent=2)
    
    def generate_cisco_acl(self, ipv4_prefixes, ipv6_prefixes):
        """Generate Cisco ACL configuration"""
        rules = []
        rules.append("! Google IP Ranges - Cisco ACL")
        rules.append(f"! Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        rules.append("!")
        rules.append("ip access-list extended GOOGLE-IPS-V4")
        
        for ip in ipv4_prefixes:
            # Convert CIDR to wildcard mask
            network, prefix = ip.split('/')
            prefix_int = int(prefix)
            wildcard_bits = 32 - prefix_int
            wildcard = '.'.join([str((0xFFFFFFFF >> (32 - wildcard_bits)) >> (i * 8) & 0xFF) 
                                for i in range(3, -1, -1)])
            rules.append(f" permit ip {network} {wildcard} any")
        
        rules.append("!")
        rules.append("ipv6 access-list GOOGLE-IPS-V6")
        for ip in ipv6_prefixes:
            rules.append(f" permit ipv6 {ip} any")
        
        rules.append("!")
        
        return "\n".join(rules)
    
    def generate_pfsense(self, ipv4_prefixes, ipv6_prefixes):
        """Generate pfSense alias configuration"""
        rules = []
        rules.append("# Google IP Ranges - pfSense Alias")
        rules.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        rules.append("# Import via Firewall > Aliases > Import")
        rules.append("")
        
        rules.append("# IPv4 Networks")
        for ip in ipv4_prefixes:
            rules.append(ip)
        
        rules.append("")
        rules.append("# IPv6 Networks")
        for ip in ipv6_prefixes:
            rules.append(ip)
        
        return "\n".join(rules)
    
    def generate_plain_text(self, ipv4_prefixes, ipv6_prefixes):
        """Generate plain text list"""
        rules = []
        rules.append(f"Google IP Ranges - Plain Text")
        rules.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        rules.append(f"Total IPv4: {len(ipv4_prefixes)}")
        rules.append(f"Total IPv6: {len(ipv6_prefixes)}")
        rules.append("")
        rules.append("=== IPv4 Ranges ===")
        rules.extend(ipv4_prefixes)
        rules.append("")
        rules.append("=== IPv6 Ranges ===")
        rules.extend(ipv6_prefixes)
        
        return "\n".join(rules)
    
    def generate_csv(self, ipv4_prefixes, ipv6_prefixes):
        """Generate CSV format"""
        lines = []
        lines.append("type,prefix,description")
        
        for ip in ipv4_prefixes:
            lines.append(f"IPv4,{ip},Google IP Range")
        
        for ip in ipv6_prefixes:
            lines.append(f"IPv6,{ip},Google IP Range")
        
        return "\n".join(lines)
    
    def generate_json_export(self, ipv4_prefixes, ipv6_prefixes):
        """Generate JSON export"""
        data = {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
            "total_ranges": len(ipv4_prefixes) + len(ipv6_prefixes),
            "ipv4": {
                "count": len(ipv4_prefixes),
                "ranges": ipv4_prefixes
            },
            "ipv6": {
                "count": len(ipv6_prefixes),
                "ranges": ipv6_prefixes
            }
        }
        return json.dumps(data, indent=2)
    
    def generate_mikrotik(self, ipv4_prefixes, ipv6_prefixes):
        """Generate MikroTik RouterOS script"""
        rules = []
        rules.append("# Google IP Ranges - MikroTik RouterOS")
        rules.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        rules.append("")
        rules.append("# Create address list")
        rules.append("/ip firewall address-list")
        
        for ip in ipv4_prefixes:
            rules.append(f"add list=google-ips address={ip} comment=\"Google IPv4\"")
        
        rules.append("")
        rules.append("/ipv6 firewall address-list")
        for ip in ipv6_prefixes:
            rules.append(f"add list=google-ips-v6 address={ip} comment=\"Google IPv6\"")
        
        return "\n".join(rules)
    
    def generate_all(self):
        """Generate all firewall formats"""
        print("Loading latest IP data...")
        data = self.load_latest_data()
        if not data:
            return
        
        ipv4_prefixes, ipv6_prefixes = self.extract_prefixes(data)
        print(f"Found {len(ipv4_prefixes)} IPv4 and {len(ipv6_prefixes)} IPv6 ranges")
        
        formats = {
            'iptables.sh': self.generate_iptables,
            'aws-security-group.json': self.generate_aws_security_group,
            'azure-nsg.json': self.generate_azure_nsg,
            'cisco-acl.txt': self.generate_cisco_acl,
            'pfsense-alias.txt': self.generate_pfsense,
            'mikrotik.rsc': self.generate_mikrotik,
            'plain-text.txt': self.generate_plain_text,
            'export.csv': self.generate_csv,
            'export.json': self.generate_json_export
        }
        
        for filename, generator in formats.items():
            output = generator(ipv4_prefixes, ipv6_prefixes)
            filepath = os.path.join(self.export_dir, filename)
            with open(filepath, 'w') as f:
                f.write(output)
            print(f"✅ Generated: {filepath}")
        
        # Generate index.html for exports directory
        self.generate_exports_index(ipv4_prefixes, ipv6_prefixes)
        print(f"✅ Generated: {os.path.join(self.export_dir, 'index.html')}")
    
    def generate_exports_index(self, ipv4_prefixes, ipv6_prefixes):
        """Generate an index page for the exports directory"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google IP Monitor - Firewall Rules Export</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="header-left">
                <div class="logo">
                    <span class="logo-icon">🔥</span>
                    <h1>Firewall Rules Export</h1>
                </div>
            </div>
            <div class="header-right">
                <a href="../index.html" style="color: var(--accent-blue); text-decoration: none;">← Back to Dashboard</a>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="content">
            <div class="stats">
                <div class="stat-card">
                    <h3>IPv4 Ranges</h3>
                    <div class="number">{len(ipv4_prefixes):,}</div>
                </div>
                <div class="stat-card">
                    <h3>IPv6 Ranges</h3>
                    <div class="number">{len(ipv6_prefixes):,}</div>
                </div>
                <div class="stat-card">
                    <h3>Export Formats</h3>
                    <div class="number">9</div>
                </div>
            </div>

            <div class="changes-section">
                <div class="section-header">
                    <h2>Available Export Formats</h2>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 16px;">
                    <a href="iptables.sh" download class="export-card">
                        <div class="export-icon">🐧</div>
                        <h3>iptables</h3>
                        <p>Linux firewall rules</p>
                        <span class="download-badge">Download .sh</span>
                    </a>
                    
                    <a href="aws-security-group.json" download class="export-card">
                        <div class="export-icon">☁️</div>
                        <h3>AWS Security Group</h3>
                        <p>Amazon Web Services</p>
                        <span class="download-badge">Download .json</span>
                    </a>
                    
                    <a href="azure-nsg.json" download class="export-card">
                        <div class="export-icon">🔷</div>
                        <h3>Azure NSG</h3>
                        <p>Microsoft Azure Network Security Group</p>
                        <span class="download-badge">Download .json</span>
                    </a>
                    
                    <a href="cisco-acl.txt" download class="export-card">
                        <div class="export-icon">🌐</div>
                        <h3>Cisco ACL</h3>
                        <p>Cisco IOS access lists</p>
                        <span class="download-badge">Download .txt</span>
                    </a>
                    
                    <a href="pfsense-alias.txt" download class="export-card">
                        <div class="export-icon">🛡️</div>
                        <h3>pfSense</h3>
                        <p>pfSense firewall alias</p>
                        <span class="download-badge">Download .txt</span>
                    </a>
                    
                    <a href="mikrotik.rsc" download class="export-card">
                        <div class="export-icon">🔧</div>
                        <h3>MikroTik</h3>
                        <p>RouterOS script</p>
                        <span class="download-badge">Download .rsc</span>
                    </a>
                    
                    <a href="plain-text.txt" download class="export-card">
                        <div class="export-icon">📄</div>
                        <h3>Plain Text</h3>
                        <p>Simple text list</p>
                        <span class="download-badge">Download .txt</span>
                    </a>
                    
                    <a href="export.csv" download class="export-card">
                        <div class="export-icon">📊</div>
                        <h3>CSV</h3>
                        <p>Comma-separated values</p>
                        <span class="download-badge">Download .csv</span>
                    </a>
                    
                    <a href="export.json" download class="export-card">
                        <div class="export-icon">📦</div>
                        <h3>JSON</h3>
                        <p>Structured JSON data</p>
                        <span class="download-badge">Download .json</span>
                    </a>
                </div>
            </div>
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
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 8px;
        }}
        
        .export-card p {{
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 16px;
        }}
        
        .download-badge {{
            background-color: var(--accent-blue);
            color: var(--bg-primary);
            padding: 8px 16px;
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
        
        filepath = os.path.join(self.export_dir, 'index.html')
        with open(filepath, 'w') as f:
            f.write(html)

if __name__ == '__main__':
    generator = FirewallRulesGenerator()
    generator.generate_all()
