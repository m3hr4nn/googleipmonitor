"""
Chart API Gateway - Microservice 5 (Orchestrator)

Responsibilities:
- Coordinate all chart microservices
- Manage service lifecycle and execution order
- Handle errors and provide fallbacks
- Provide unified interface for chart generation

This is the entry point for the entire chart generation pipeline.
"""

import os
import json
from typing import Dict, Optional
from datetime import datetime

from services.aggregator_service import DataAggregatorService
from services.chart_config_service import ChartConfigService
from services.chart_renderer_service import ChartRendererService
from services.chart_export_service import ChartExportService


class ChartAPIGateway:
    """
    API Gateway / Orchestrator for chart microservices.
    Coordinates the execution of all chart-related services.
    """

    def __init__(self, config_file: Optional[str] = 'config/chart_settings.json'):
        self.config = self._load_config(config_file)
        self.enabled = self.config.get('enabled', True)

        # Initialize all microservices
        self.aggregator = DataAggregatorService()
        self.config_service = ChartConfigService()
        self.renderer = ChartRendererService()
        self.exporter = ChartExportService()

        self.execution_log = []

    def _load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        if not os.path.exists(config_file):
            # Return default config if file doesn't exist
            return {
                'enabled': True,
                'days_to_show': 90,
                'use_cache': True,
                'charts': {
                    'line_chart': {'enabled': True},
                    'bar_chart': {'enabled': True},
                    'pie_chart': {'enabled': True}
                },
                'exports': {
                    'csv': True,
                    'json': True,
                    'markdown': True
                }
            }

        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Error loading config from {config_file}: {e}")
            return {'enabled': True, 'days_to_show': 90}

    def _log_execution(self, service: str, status: str, message: str):
        """Log service execution for debugging"""
        self.execution_log.append({
            'timestamp': datetime.now().isoformat(),
            'service': service,
            'status': status,
            'message': message
        })

    def get_service_status(self) -> Dict:
        """
        Check status of all microservices.

        Returns:
            Dict with service health information
        """
        status = {
            'gateway': 'operational',
            'services': {
                'aggregator': 'operational' if self.aggregator else 'unavailable',
                'config_service': 'operational' if self.config_service else 'unavailable',
                'renderer': 'operational' if self.renderer else 'unavailable',
                'exporter': 'operational' if self.exporter else 'unavailable'
            },
            'configuration': {
                'enabled': self.enabled,
                'days_to_show': self.config.get('days_to_show', 90),
                'use_cache': self.config.get('use_cache', True)
            },
            'execution_log': self.execution_log[-10:]  # Last 10 entries
        }

        return status

    def refresh_cache(self) -> bool:
        """
        Force refresh of all cached data.

        Returns:
            True if successful, False otherwise
        """
        try:
            print("🔄 Refreshing cache...")

            # Step 1: Aggregate data
            metrics = self.aggregator.run(
                days=self.config.get('days_to_show', 90),
                use_cache=False
            )

            # Step 2: Generate configs
            configs = self.config_service.run(metrics, use_cache=False)

            print("✅ Cache refreshed successfully")
            return True

        except Exception as e:
            print(f"❌ Error refreshing cache: {e}")
            return False

    def generate_all_charts(self) -> Dict:
        """
        Main method: Orchestrate all services to generate charts.

        Execution order:
        1. DataAggregatorService - Parse historical data
        2. ChartConfigService - Generate Chart.js configs
        3. ChartRendererService - Render HTML/JavaScript
        4. ChartExportService - Export data formats

        Returns:
            Dict containing all generated content and exports
        """
        if not self.enabled:
            self._log_execution('gateway', 'disabled', 'Chart generation disabled in config')
            return {
                'enabled': False,
                'cdn_script': '',
                'charts_section': '',
                'exports': {}
            }

        try:
            print("\n" + "="*60)
            print("🚀 Chart API Gateway - Starting Pipeline")
            print("="*60)

            # Step 1: Data Aggregation
            print("\n[1/4] Data Aggregation Service")
            try:
                metrics = self.aggregator.run(
                    days=self.config.get('days_to_show', 90),
                    use_cache=self.config.get('use_cache', True)
                )
                self._log_execution('aggregator', 'success', f"Processed {metrics['summary']['total_data_points']} data points")
            except Exception as e:
                self._log_execution('aggregator', 'error', str(e))
                raise Exception(f"Aggregator service failed: {e}")

            # Check if we have data
            if metrics['summary']['total_data_points'] == 0:
                print("⚠️  No historical data available. Skipping chart generation.")
                self._log_execution('gateway', 'warning', 'No historical data available')
                return {
                    'enabled': True,
                    'has_data': False,
                    'cdn_script': '',
                    'charts_section': '<p>No historical data available yet. Charts will appear after data collection.</p>',
                    'exports': {}
                }

            # Step 2: Chart Configuration
            print("\n[2/4] Chart Configuration Service")
            try:
                configs = self.config_service.run(
                    metrics,
                    use_cache=self.config.get('use_cache', True)
                )
                self._log_execution('config_service', 'success', 'Generated chart configurations')
            except Exception as e:
                self._log_execution('config_service', 'error', str(e))
                raise Exception(f"Config service failed: {e}")

            # Step 3: Chart Rendering
            print("\n[3/4] Chart Renderer Service")
            try:
                rendered = self.renderer.run(configs, metrics)
                self._log_execution('renderer', 'success', 'Rendered HTML/JavaScript')
            except Exception as e:
                self._log_execution('renderer', 'error', str(e))
                raise Exception(f"Renderer service failed: {e}")

            # Step 4: Data Export
            print("\n[4/4] Chart Export Service")
            try:
                if self.config.get('exports', {}).get('enabled', True):
                    exports = self.exporter.run(metrics)
                    self._log_execution('exporter', 'success', f"Exported {len(exports)} formats")
                else:
                    exports = {}
                    self._log_execution('exporter', 'skipped', 'Exports disabled in config')
            except Exception as e:
                self._log_execution('exporter', 'warning', f"Export failed: {e}")
                # Non-critical, continue
                exports = {}

            print("\n" + "="*60)
            print("✅ Chart Pipeline Completed Successfully")
            print("="*60)

            # Return aggregated result
            result = {
                'enabled': True,
                'has_data': True,
                'cdn_script': rendered['cdn_script'],
                'charts_section': rendered['charts_section'],
                'exports': exports,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'service': 'ChartAPIGateway',
                    'version': '1.1.0',
                    'data_points': metrics['summary']['total_data_points'],
                    'date_range': metrics['summary']['date_range']
                }
            }

            return result

        except Exception as e:
            print(f"\n❌ Chart pipeline failed: {e}")
            self._log_execution('gateway', 'error', str(e))

            # Return graceful fallback
            return {
                'enabled': True,
                'has_data': False,
                'error': str(e),
                'cdn_script': '',
                'charts_section': f'<p>Chart generation temporarily unavailable. Error: {str(e)}</p>',
                'exports': {}
            }

    def run(self) -> Dict:
        """
        Execute the gateway (alias for generate_all_charts).

        Returns:
            Dict containing all generated content
        """
        return self.generate_all_charts()


def main():
    """Standalone execution for testing"""
    gateway = ChartAPIGateway()

    # Check service status
    print("Checking service status...")
    status = gateway.get_service_status()
    print(f"Gateway: {status['gateway']}")
    print(f"Services: {status['services']}")
    print(f"Config: {status['configuration']}")

    # Generate all charts
    result = gateway.run()

    print("\n" + "="*60)
    print("Chart API Gateway - Final Results")
    print("="*60)
    print(f"Enabled: {result.get('enabled')}")
    print(f"Has Data: {result.get('has_data')}")
    print(f"CDN Script: {len(result.get('cdn_script', ''))} bytes")
    print(f"Charts Section: {len(result.get('charts_section', ''))} bytes")
    print(f"Exports: {list(result.get('exports', {}).keys())}")

    if 'metadata' in result:
        print(f"\nMetadata:")
        print(f"  Data Points: {result['metadata'].get('data_points')}")
        print(f"  Date Range: {result['metadata'].get('date_range')}")

    print("="*60)

    # Save execution log
    log_file = 'cache/gateway_execution.log'
    with open(log_file, 'w') as f:
        json.dump(gateway.execution_log, f, indent=2)
    print(f"\n📝 Execution log saved to {log_file}")


if __name__ == '__main__':
    main()
