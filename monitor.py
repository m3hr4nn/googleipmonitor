import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Set
import hashlib

class GoogleIPMonitor:
    def __init__(self):
        self.urls = {
            'cloud': 'https://www.gstatic.com/ipranges/cloud.json',
            'goog': 'https://www.gstatic.com/ipranges/goog.json'
        }
        self.data_dir = 'data'
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_ip_data(self) -> Dict:
        """Fetch current IP data from Google"""
        data = {}
        for name, url in self.urls.items():
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data[name] = response.json()
            except Exception as e:
                print(f"Error fetching {name}: {e}")
                data[name] = None
        return data
    
    def save_data(self, data: Dict, date: str):
        """Save IP data to file"""
        filename = os.path.join(self.data_dir, f'{date}.json')
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved data to {filename}")
    
    def load_data(self, date: str) -> Dict:
        """Load IP data from file"""
        filename = os.path.join(self.data_dir, f'{date}.json')
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            return json.load(f)
    
    def extract_prefixes(self, data: Dict) -> Set[str]:
        """Extract all IP prefixes from data"""
        prefixes = set()
        
        if data.get('cloud'):
            for prefix_entry in data['cloud'].get('prefixes', []):
                if 'ipv4Prefix' in prefix_entry:
                    prefixes.add(prefix_entry['ipv4Prefix'])
                if 'ipv6Prefix' in prefix_entry:
                    prefixes.add(prefix_entry['ipv6Prefix'])
        
        if data.get('goog'):
            for prefix_entry in data['goog'].get('prefixes', []):
                if 'ipv4Prefix' in prefix_entry:
                    prefixes.add(prefix_entry['ipv4Prefix'])
                if 'ipv6Prefix' in prefix_entry:
                    prefixes.add(prefix_entry['ipv6Prefix'])
        
        return prefixes
    
    def compare_data(self, old_data: Dict, new_data: Dict) -> Dict:
        """Compare two datasets and find differences"""
        if not old_data or not new_data:
            return {
                'added': [],
                'removed': [],
                'total_current': 0,
                'has_changes': False
            }
        
        old_prefixes = self.extract_prefixes(old_data)
        new_prefixes = self.extract_prefixes(new_data)
        
        added = new_prefixes - old_prefixes
        removed = old_prefixes - new_prefixes
        
        return {
            'added': sorted(list(added)),
            'removed': sorted(list(removed)),
            'total_current': len(new_prefixes),
            'total_previous': len(old_prefixes),
            'has_changes': len(added) > 0 or len(removed) > 0
        }
    
    def format_report(self, comparison: Dict, today: str, yesterday: str) -> str:
        """Format comparison results as a readable report"""
        report = f"📊 Google IP Ranges Report\n"
        report += f"📅 Date: {today}\n"
        report += f"{'='*40}\n\n"
        
        if not comparison['has_changes']:
            report += "✅ No changes detected\n"
            report += f"📦 Total IP ranges: {comparison['total_current']}\n"
        else:
            report += "🔔 Changes detected!\n\n"
            
            if comparison['added']:
                report += f"➕ Added ({len(comparison['added'])}):\n"
                for ip in comparison['added'][:10]:  # Limit to first 10
                    report += f"  • {ip}\n"
                if len(comparison['added']) > 10:
                    report += f"  ... and {len(comparison['added']) - 10} more\n"
                report += "\n"
            
            if comparison['removed']:
                report += f"➖ Removed ({len(comparison['removed'])}):\n"
                for ip in comparison['removed'][:10]:  # Limit to first 10
                    report += f"  • {ip}\n"
                if len(comparison['removed']) > 10:
                    report += f"  ... and {len(comparison['removed']) - 10} more\n"
                report += "\n"
            
            report += f"📊 Statistics:\n"
            report += f"  Previous: {comparison['total_previous']} ranges\n"
            report += f"  Current: {comparison['total_current']} ranges\n"
            report += f"  Net change: {comparison['total_current'] - comparison['total_previous']:+d}\n"
        
        return report
    
    def send_telegram_message(self, message: str):
        """Send message to Telegram"""
        if not self.telegram_token or not self.telegram_chat_id:
            print("Telegram credentials not set")
            return False
        
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': self.telegram_chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print("Telegram message sent successfully")
            return True
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
            return False
    
    def run(self):
        """Main execution flow"""
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = datetime.now().strftime('%Y-%m-%d')  # You'd calculate actual yesterday
        
        print(f"Fetching Google IP data for {today}...")
        current_data = self.fetch_ip_data()
        
        if not current_data['cloud'] and not current_data['goog']:
            print("Failed to fetch data")
            return
        
        # Save today's data
        self.save_data(current_data, today)
        
        # Load yesterday's data
        previous_data = self.load_data(yesterday)
        
        # Compare
        comparison = self.compare_data(previous_data, current_data)
        
        # Generate report
        report = self.format_report(comparison, today, yesterday)
        print("\n" + report)
        
        # Send to Telegram
        self.send_telegram_message(report)

if __name__ == '__main__':
    monitor = GoogleIPMonitor()
    monitor.run()
