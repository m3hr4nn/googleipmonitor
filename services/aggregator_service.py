"""
Data Aggregation Service - Microservice 1

Responsibilities:
- Parse historical JSON data files
- Extract metrics (total ranges, IPv4/IPv6 counts, daily changes)
- Generate aggregated statistics
- Output to cache/metrics.json

This service is independent and reusable by other components.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Set
from glob import glob


class DataAggregatorService:
    """
    Microservice for aggregating historical IP range data.
    Single Responsibility: Data parsing and metric computation.
    """

    def __init__(self, data_dir: str = 'data', cache_dir: str = 'cache'):
        self.data_dir = data_dir
        self.cache_dir = cache_dir
        self.metrics_cache_file = os.path.join(cache_dir, 'metrics.json')

        # Ensure cache directory exists
        os.makedirs(cache_dir, exist_ok=True)

    def extract_prefixes(self, data: Dict) -> Set[str]:
        """Extract all IP prefixes from a data snapshot"""
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

    def separate_ipv4_ipv6(self, prefixes: Set[str]) -> Dict[str, List[str]]:
        """Separate IPv4 and IPv6 prefixes"""
        ipv4 = [ip for ip in prefixes if ':' not in ip]
        ipv6 = [ip for ip in prefixes if ':' in ip]
        return {
            'ipv4': sorted(ipv4),
            'ipv6': sorted(ipv6)
        }

    def load_historical_data(self, days: int = 90) -> List[Dict]:
        """
        Load historical data files from the last N days.
        Returns list of (date, data) tuples.
        """
        data_files = sorted(glob(os.path.join(self.data_dir, '*.json')))

        if not data_files:
            print("Warning: No historical data files found")
            return []

        # Limit to last N days
        data_files = data_files[-days:] if len(data_files) > days else data_files

        historical_data = []

        for file_path in data_files:
            try:
                date_str = os.path.basename(file_path).replace('.json', '')
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    historical_data.append({
                        'date': date_str,
                        'data': data
                    })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue

        return historical_data

    def aggregate_all_data(self, days: int = 90) -> Dict:
        """
        Main aggregation method.
        Computes all metrics and returns structured data.
        """
        historical_data = self.load_historical_data(days)

        if not historical_data:
            return self._get_empty_metrics()

        timestamps = []
        total_ranges = []
        ipv4_counts = []
        ipv6_counts = []
        daily_added = []
        daily_removed = []

        previous_prefixes = None

        for entry in historical_data:
            date = entry['date']
            data = entry['data']

            current_prefixes = self.extract_prefixes(data)
            split = self.separate_ipv4_ipv6(current_prefixes)

            timestamps.append(date)
            total_ranges.append(len(current_prefixes))
            ipv4_counts.append(len(split['ipv4']))
            ipv6_counts.append(len(split['ipv6']))

            # Calculate daily changes
            if previous_prefixes is not None:
                added = current_prefixes - previous_prefixes
                removed = previous_prefixes - current_prefixes
                daily_added.append(len(added))
                daily_removed.append(len(removed))
            else:
                daily_added.append(0)
                daily_removed.append(0)

            previous_prefixes = current_prefixes

        # Calculate trends
        metrics = {
            'timestamps': timestamps,
            'total_ranges': total_ranges,
            'ipv4_counts': ipv4_counts,
            'ipv6_counts': ipv6_counts,
            'daily_added': daily_added,
            'daily_removed': daily_removed,
            'summary': {
                'total_data_points': len(timestamps),
                'date_range': {
                    'start': timestamps[0] if timestamps else None,
                    'end': timestamps[-1] if timestamps else None
                },
                'current_total': total_ranges[-1] if total_ranges else 0,
                'current_ipv4': ipv4_counts[-1] if ipv4_counts else 0,
                'current_ipv6': ipv6_counts[-1] if ipv6_counts else 0,
                'total_growth': total_ranges[-1] - total_ranges[0] if len(total_ranges) > 1 else 0,
                'avg_daily_change': sum(daily_added) / len(daily_added) if daily_added else 0
            },
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'service': 'DataAggregatorService',
                'version': '1.1.0'
            }
        }

        return metrics

    def _get_empty_metrics(self) -> Dict:
        """Return empty metrics structure when no data available"""
        return {
            'timestamps': [],
            'total_ranges': [],
            'ipv4_counts': [],
            'ipv6_counts': [],
            'daily_added': [],
            'daily_removed': [],
            'summary': {
                'total_data_points': 0,
                'date_range': {'start': None, 'end': None},
                'current_total': 0,
                'current_ipv4': 0,
                'current_ipv6': 0,
                'total_growth': 0,
                'avg_daily_change': 0
            },
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'service': 'DataAggregatorService',
                'version': '1.1.0'
            }
        }

    def save_to_cache(self, metrics: Dict) -> bool:
        """Save aggregated metrics to cache file"""
        try:
            with open(self.metrics_cache_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            print(f"✅ Metrics cached to {self.metrics_cache_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving metrics to cache: {e}")
            return False

    def load_from_cache(self) -> Dict:
        """Load metrics from cache file"""
        if not os.path.exists(self.metrics_cache_file):
            return self._get_empty_metrics()

        try:
            with open(self.metrics_cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
            return self._get_empty_metrics()

    def run(self, days: int = 90, use_cache: bool = False) -> Dict:
        """
        Execute the aggregation service.

        Args:
            days: Number of days of historical data to process
            use_cache: If True, return cached data if available

        Returns:
            Dict containing aggregated metrics
        """
        if use_cache and os.path.exists(self.metrics_cache_file):
            print("📦 Loading metrics from cache")
            return self.load_from_cache()

        print(f"📊 Aggregating historical data (last {days} days)...")
        metrics = self.aggregate_all_data(days)
        self.save_to_cache(metrics)

        return metrics


def main():
    """Standalone execution for testing"""
    service = DataAggregatorService()
    metrics = service.run(days=90)

    print("\n" + "="*50)
    print("Data Aggregation Service - Results")
    print("="*50)
    print(f"Total data points: {metrics['summary']['total_data_points']}")
    print(f"Date range: {metrics['summary']['date_range']['start']} to {metrics['summary']['date_range']['end']}")
    print(f"Current total ranges: {metrics['summary']['current_total']}")
    print(f"Current IPv4: {metrics['summary']['current_ipv4']}")
    print(f"Current IPv6: {metrics['summary']['current_ipv6']}")
    print(f"Total growth: {metrics['summary']['total_growth']:+d}")
    print(f"Avg daily change: {metrics['summary']['avg_daily_change']:.2f}")
    print("="*50)


if __name__ == '__main__':
    main()
