"""
Chart Renderer Service - Microservice 3

Responsibilities:
- Generate HTML canvas elements for charts
- Create Chart.js initialization scripts
- Handle responsive layouts
- Produce injectable HTML fragments

This service transforms configurations into renderable HTML/JavaScript.
"""

import json
from typing import Dict


class ChartRendererService:
    """
    Microservice for rendering Chart.js visualizations.
    Single Responsibility: HTML/JavaScript generation for charts.
    """

    def __init__(self):
        self.chartjs_cdn = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"

    def render_canvas(self, chart_id: str, height: str = "400px") -> str:
        """Generate HTML canvas element for a chart"""
        return f'''
        <div class="chart-container" style="position: relative; height: {height}; margin-bottom: 32px;">
            <canvas id="{chart_id}"></canvas>
        </div>
        '''

    def render_chart_script(self, chart_id: str, config: Dict) -> str:
        """
        Generate Chart.js initialization script.

        Args:
            chart_id: DOM element ID for the canvas
            config: Chart.js configuration object

        Returns:
            JavaScript code as string
        """
        config_json = json.dumps(config, indent=4)

        script = f'''
        <script>
        (function() {{
            const ctx = document.getElementById('{chart_id}');
            if (!ctx) {{
                console.error('Canvas element #{chart_id} not found');
                return;
            }}

            const config = {config_json};

            // Create chart instance
            new Chart(ctx, config);
        }})();
        </script>
        '''

        return script

    def render_line_chart(self, config: Dict) -> str:
        """Render line chart (IP growth over time)"""
        canvas = self.render_canvas('lineChart', height='400px')
        script = self.render_chart_script('lineChart', config)
        return canvas + script

    def render_bar_chart(self, config: Dict) -> str:
        """Render bar chart (daily changes)"""
        canvas = self.render_canvas('barChart', height='350px')
        script = self.render_chart_script('barChart', config)
        return canvas + script

    def render_pie_chart(self, config: Dict) -> str:
        """Render pie chart (IPv4 vs IPv6 distribution)"""
        canvas = self.render_canvas('pieChart', height='320px')
        script = self.render_chart_script('pieChart', config)
        return canvas + script

    def render_chartjs_cdn(self) -> str:
        """Generate Chart.js CDN script tag"""
        return f'<script src="{self.chartjs_cdn}"></script>'

    def render_charts_section(self, configs: Dict, metrics: Dict) -> str:
        """
        Render complete charts section with all charts.

        Args:
            configs: Chart configurations from ChartConfigService
            metrics: Metrics data for summary display

        Returns:
            Complete HTML section with all charts
        """
        summary = metrics.get('summary', {})
        date_range = summary.get('date_range', {})
        total_points = summary.get('total_data_points', 0)

        # Build charts HTML
        charts_html = f'''
        <div class="charts-section">
            <div class="section-header">
                <h2>📈 Historical Analytics</h2>
                <span class="badge">{date_range.get('start', 'N/A')} to {date_range.get('end', 'N/A')} • {total_points} data points</span>
            </div>

            <div class="chart-grid">
                <div class="chart-card full-width">
                    {self.render_line_chart(configs.get('line_chart', {}))}
                </div>

                <div class="chart-card">
                    {self.render_bar_chart(configs.get('bar_chart', {}))}
                </div>

                <div class="chart-card">
                    {self.render_pie_chart(configs.get('pie_chart', {}))}
                </div>
            </div>

            <div class="chart-summary">
                <div class="summary-stat">
                    <span class="label">Total Growth</span>
                    <span class="value {'positive' if summary.get('total_growth', 0) >= 0 else 'negative'}">{summary.get('total_growth', 0):+d}</span>
                </div>
                <div class="summary-stat">
                    <span class="label">Avg Daily Change</span>
                    <span class="value">{summary.get('avg_daily_change', 0):.2f}</span>
                </div>
                <div class="summary-stat">
                    <span class="label">Current IPv4</span>
                    <span class="value">{summary.get('current_ipv4', 0):,}</span>
                </div>
                <div class="summary-stat">
                    <span class="label">Current IPv6</span>
                    <span class="value">{summary.get('current_ipv6', 0):,}</span>
                </div>
            </div>
        </div>
        '''

        return charts_html

    def render_all_charts(self, configs: Dict, metrics: Dict) -> Dict:
        """
        Generate all chart HTML.

        Returns:
            Dict containing:
            - cdn_script: Chart.js CDN include
            - charts_section: Complete HTML for charts section
        """
        return {
            'cdn_script': self.render_chartjs_cdn(),
            'charts_section': self.render_charts_section(configs, metrics),
            'metadata': {
                'service': 'ChartRendererService',
                'version': '1.1.0'
            }
        }

    def run(self, configs: Dict, metrics: Dict) -> Dict:
        """
        Execute the chart renderer service.

        Args:
            configs: Chart configurations from ChartConfigService
            metrics: Aggregated metrics from DataAggregatorService

        Returns:
            Dict containing rendered HTML components
        """
        print("🖼️  Rendering charts...")
        rendered = self.render_all_charts(configs, metrics)
        print("✅ Charts rendered successfully")

        return rendered


def main():
    """Standalone execution for testing"""
    import os

    # Load configs and metrics from cache
    configs_file = 'cache/chart_configs.json'
    metrics_file = 'cache/metrics.json'

    if not os.path.exists(configs_file) or not os.path.exists(metrics_file):
        print("❌ Cache files not found. Run aggregator and config services first.")
        return

    with open(configs_file, 'r') as f:
        configs = json.load(f)

    with open(metrics_file, 'r') as f:
        metrics = json.load(f)

    service = ChartRendererService()
    rendered = service.run(configs, metrics)

    print("\n" + "="*50)
    print("Chart Renderer Service - Results")
    print("="*50)
    print(f"CDN script generated: {len(rendered['cdn_script'])} bytes")
    print(f"Charts section generated: {len(rendered['charts_section'])} bytes")
    print("="*50)

    # Save test output
    with open('cache/rendered_charts.html', 'w') as f:
        f.write(rendered['cdn_script'])
        f.write('\n')
        f.write(rendered['charts_section'])

    print("✅ Test output saved to cache/rendered_charts.html")


if __name__ == '__main__':
    main()
