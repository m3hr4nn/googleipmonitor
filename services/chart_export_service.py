"""
Chart Export Service - Microservice 4

Responsibilities:
- Export chart data in multiple formats
- Generate CSV files for Excel analysis
- Create JSON API endpoints
- Save exports to exports/charts/ directory

This service provides data portability and external integration.
"""

import os
import json
import csv
from typing import Dict, List
from datetime import datetime


class ChartExportService:
    """
    Microservice for exporting chart data.
    Single Responsibility: Multi-format data export.
    """

    def __init__(self, export_dir: str = 'exports/charts'):
        self.export_dir = export_dir
        os.makedirs(export_dir, exist_ok=True)

    def export_to_csv(self, metrics: Dict) -> str:
        """
        Export historical metrics to CSV format.

        Returns:
            Path to generated CSV file
        """
        csv_file = os.path.join(self.export_dir, 'historical_metrics.csv')

        timestamps = metrics.get('timestamps', [])
        total_ranges = metrics.get('total_ranges', [])
        ipv4_counts = metrics.get('ipv4_counts', [])
        ipv6_counts = metrics.get('ipv6_counts', [])
        daily_added = metrics.get('daily_added', [])
        daily_removed = metrics.get('daily_removed', [])

        try:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)

                # Write header
                writer.writerow([
                    'Date',
                    'Total Ranges',
                    'IPv4 Count',
                    'IPv6 Count',
                    'Daily Added',
                    'Daily Removed',
                    'Net Change'
                ])

                # Write data rows
                for i in range(len(timestamps)):
                    net_change = daily_added[i] - daily_removed[i] if i < len(daily_added) and i < len(daily_removed) else 0
                    writer.writerow([
                        timestamps[i],
                        total_ranges[i] if i < len(total_ranges) else 0,
                        ipv4_counts[i] if i < len(ipv4_counts) else 0,
                        ipv6_counts[i] if i < len(ipv6_counts) else 0,
                        daily_added[i] if i < len(daily_added) else 0,
                        daily_removed[i] if i < len(daily_removed) else 0,
                        net_change
                    ])

            print(f"✅ CSV export: {csv_file}")
            return csv_file

        except Exception as e:
            print(f"❌ Error exporting CSV: {e}")
            return ""

    def export_to_json(self, metrics: Dict) -> str:
        """
        Export metrics to JSON format (API-friendly).

        Returns:
            Path to generated JSON file
        """
        json_file = os.path.join(self.export_dir, 'historical_metrics.json')

        try:
            export_data = {
                'data': {
                    'timestamps': metrics.get('timestamps', []),
                    'total_ranges': metrics.get('total_ranges', []),
                    'ipv4_counts': metrics.get('ipv4_counts', []),
                    'ipv6_counts': metrics.get('ipv6_counts', []),
                    'daily_added': metrics.get('daily_added', []),
                    'daily_removed': metrics.get('daily_removed', [])
                },
                'summary': metrics.get('summary', {}),
                'metadata': {
                    'exported_at': datetime.now().isoformat(),
                    'service': 'ChartExportService',
                    'version': '1.1.0',
                    'format': 'json'
                }
            }

            with open(json_file, 'w') as f:
                json.dump(export_data, f, indent=2)

            print(f"✅ JSON export: {json_file}")
            return json_file

        except Exception as e:
            print(f"❌ Error exporting JSON: {e}")
            return ""

    def export_summary_markdown(self, metrics: Dict) -> str:
        """
        Export summary statistics in Markdown format.

        Returns:
            Path to generated Markdown file
        """
        md_file = os.path.join(self.export_dir, 'summary.md')
        summary = metrics.get('summary', {})
        date_range = summary.get('date_range', {})

        try:
            markdown = f"""# Google IP Monitor - Historical Analytics Summary

## Overview

- **Data Points**: {summary.get('total_data_points', 0)}
- **Date Range**: {date_range.get('start', 'N/A')} to {date_range.get('end', 'N/A')}
- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

## Current Statistics

| Metric | Value |
|--------|-------|
| Total IP Ranges | {summary.get('current_total', 0):,} |
| IPv4 Ranges | {summary.get('current_ipv4', 0):,} |
| IPv6 Ranges | {summary.get('current_ipv6', 0):,} |
| Total Growth | {summary.get('total_growth', 0):+d} |
| Avg Daily Change | {summary.get('avg_daily_change', 0):.2f} |

## Distribution

- **IPv4**: {(summary.get('current_ipv4', 0) / summary.get('current_total', 1) * 100):.1f}%
- **IPv6**: {(summary.get('current_ipv6', 0) / summary.get('current_total', 1) * 100):.1f}%

---

*Generated by Google IP Monitor v1.1.0*
"""

            with open(md_file, 'w') as f:
                f.write(markdown)

            print(f"✅ Markdown export: {md_file}")
            return md_file

        except Exception as e:
            print(f"❌ Error exporting Markdown: {e}")
            return ""

    def generate_exports_index(self) -> str:
        """
        Generate an index.html page for chart exports directory.

        Returns:
            Path to generated index file
        """
        index_file = os.path.join(self.export_dir, 'index.html')

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Historical Analytics Exports</title>
    <link rel="stylesheet" href="../../styles.css">
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="header-left">
                <div class="logo">
                    <span class="logo-icon">📊</span>
                    <h1>Historical Analytics Exports</h1>
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <div class="content">
            <div class="changes-section">
                <div class="section-header">
                    <h2>📥 Download Historical Data</h2>
                    <span class="badge">3 formats available</span>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">
                    <a href="historical_metrics.csv" download class="export-card">
                        <div class="export-icon">📊</div>
                        <h3>CSV Export</h3>
                        <p>Excel-compatible spreadsheet</p>
                        <span class="download-badge">Download .csv</span>
                    </a>

                    <a href="historical_metrics.json" download class="export-card">
                        <div class="export-icon">📦</div>
                        <h3>JSON Export</h3>
                        <p>API-friendly format</p>
                        <span class="download-badge">Download .json</span>
                    </a>

                    <a href="summary.md" download class="export-card">
                        <div class="export-icon">📄</div>
                        <h3>Summary Report</h3>
                        <p>Markdown documentation</p>
                        <span class="download-badge">Download .md</span>
                    </a>
                </div>

                <div style="margin-top: 32px; text-align: center;">
                    <a href="../../index.html" style="color: var(--accent-blue); text-decoration: none;">
                        ← Back to Dashboard
                    </a>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>Google IP Monitor • Historical Analytics Exports</p>
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

        try:
            with open(index_file, 'w') as f:
                f.write(html)

            print(f"✅ Export index: {index_file}")
            return index_file

        except Exception as e:
            print(f"❌ Error generating export index: {e}")
            return ""

    def export_all(self, metrics: Dict) -> Dict:
        """
        Execute all export operations.

        Returns:
            Dict containing paths to all generated exports
        """
        exports = {
            'csv': self.export_to_csv(metrics),
            'json': self.export_to_json(metrics),
            'markdown': self.export_summary_markdown(metrics),
            'index': self.generate_exports_index()
        }

        return exports

    def run(self, metrics: Dict) -> Dict:
        """
        Execute the chart export service.

        Args:
            metrics: Aggregated metrics from DataAggregatorService

        Returns:
            Dict containing paths to exported files
        """
        print("📤 Exporting chart data...")
        exports = self.export_all(metrics)
        print(f"✅ Exported {len([v for v in exports.values() if v])} files")

        return exports


def main():
    """Standalone execution for testing"""
    import os

    # Load metrics from cache
    metrics_file = 'cache/metrics.json'
    if not os.path.exists(metrics_file):
        print("❌ No metrics cache found. Run aggregator_service.py first.")
        return

    with open(metrics_file, 'r') as f:
        metrics = json.load(f)

    service = ChartExportService()
    exports = service.run(metrics)

    print("\n" + "="*50)
    print("Chart Export Service - Results")
    print("="*50)
    for format_name, file_path in exports.items():
        status = "✅" if file_path else "❌"
        print(f"{status} {format_name}: {file_path}")
    print("="*50)


if __name__ == '__main__':
    main()
