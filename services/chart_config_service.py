"""
Chart Configuration Service - Microservice 2

Responsibilities:
- Generate Chart.js configuration objects
- Manage chart themes and color schemes
- Define chart options (axes, tooltips, legends)
- Output to cache/chart_configs.json

This service is independent and manages all chart styling and configuration.
"""

import os
import json
from typing import Dict, List
from datetime import datetime


class ChartConfigService:
    """
    Microservice for generating Chart.js configurations.
    Single Responsibility: Chart styling and configuration management.
    """

    def __init__(self, cache_dir: str = 'cache', config_dir: str = 'config'):
        self.cache_dir = cache_dir
        self.config_dir = config_dir
        self.config_cache_file = os.path.join(cache_dir, 'chart_configs.json')

        # Chrome-inspired dark theme colors (matching existing styles.css)
        self.theme = {
            'bg_primary': '#1f1f1f',
            'bg_secondary': '#292929',
            'bg_tertiary': '#323232',
            'accent_blue': '#8ab4f8',
            'accent_green': '#81c995',
            'accent_red': '#f28b82',
            'accent_yellow': '#fdd663',
            'accent_purple': '#c58af9',
            'text_primary': '#e8eaed',
            'text_secondary': '#9aa0a6',
            'border_color': '#3c4043',
            'grid_color': '#3c404340'
        }

    def get_theme_colors(self) -> Dict:
        """Return theme color palette"""
        return self.theme

    def get_common_options(self) -> Dict:
        """Common Chart.js options for all charts"""
        return {
            'responsive': True,
            'maintainAspectRatio': False,
            'plugins': {
                'legend': {
                    'labels': {
                        'color': self.theme['text_primary'],
                        'font': {
                            'family': "'Segoe UI', Roboto, sans-serif",
                            'size': 12
                        },
                        'padding': 15,
                        'usePointStyle': True
                    }
                },
                'tooltip': {
                    'backgroundColor': self.theme['bg_tertiary'],
                    'titleColor': self.theme['text_primary'],
                    'bodyColor': self.theme['text_secondary'],
                    'borderColor': self.theme['border_color'],
                    'borderWidth': 1,
                    'padding': 12,
                    'displayColors': True,
                    'callbacks': {}
                }
            },
            'interaction': {
                'intersect': False,
                'mode': 'index'
            }
        }

    def get_line_chart_config(self, metrics: Dict) -> Dict:
        """
        Generate Line Chart configuration for IP range growth over time.

        Chart displays:
        - Total IP ranges (blue line)
        - IPv4 ranges (green line)
        - IPv6 ranges (purple line)
        """
        config = {
            'type': 'line',
            'data': {
                'labels': metrics.get('timestamps', []),
                'datasets': [
                    {
                        'label': 'Total IP Ranges',
                        'data': metrics.get('total_ranges', []),
                        'borderColor': self.theme['accent_blue'],
                        'backgroundColor': self.theme['accent_blue'] + '20',
                        'borderWidth': 2,
                        'tension': 0.4,
                        'fill': True,
                        'pointRadius': 3,
                        'pointHoverRadius': 6,
                        'pointBackgroundColor': self.theme['accent_blue']
                    },
                    {
                        'label': 'IPv4 Ranges',
                        'data': metrics.get('ipv4_counts', []),
                        'borderColor': self.theme['accent_green'],
                        'backgroundColor': self.theme['accent_green'] + '20',
                        'borderWidth': 2,
                        'tension': 0.4,
                        'fill': True,
                        'pointRadius': 2,
                        'pointHoverRadius': 5,
                        'pointBackgroundColor': self.theme['accent_green']
                    },
                    {
                        'label': 'IPv6 Ranges',
                        'data': metrics.get('ipv6_counts', []),
                        'borderColor': self.theme['accent_purple'],
                        'backgroundColor': self.theme['accent_purple'] + '20',
                        'borderWidth': 2,
                        'tension': 0.4,
                        'fill': True,
                        'pointRadius': 2,
                        'pointHoverRadius': 5,
                        'pointBackgroundColor': self.theme['accent_purple']
                    }
                ]
            },
            'options': {
                **self.get_common_options(),
                'scales': {
                    'x': {
                        'grid': {
                            'color': self.theme['grid_color'],
                            'drawBorder': False
                        },
                        'ticks': {
                            'color': self.theme['text_secondary'],
                            'maxRotation': 45,
                            'minRotation': 45
                        }
                    },
                    'y': {
                        'grid': {
                            'color': self.theme['grid_color'],
                            'drawBorder': False
                        },
                        'ticks': {
                            'color': self.theme['text_secondary']
                        },
                        'beginAtZero': False
                    }
                },
                'plugins': {
                    **self.get_common_options()['plugins'],
                    'title': {
                        'display': True,
                        'text': 'IP Range Growth Over Time',
                        'color': self.theme['text_primary'],
                        'font': {
                            'size': 16,
                            'weight': '500'
                        },
                        'padding': 20
                    }
                }
            }
        }

        return config

    def get_bar_chart_config(self, metrics: Dict) -> Dict:
        """
        Generate Bar Chart configuration for daily changes.

        Chart displays:
        - Added IP ranges (green bars)
        - Removed IP ranges (red bars)
        """
        # Limit to last 30 days for readability
        timestamps = metrics.get('timestamps', [])[-30:]
        daily_added = metrics.get('daily_added', [])[-30:]
        daily_removed = metrics.get('daily_removed', [])[-30:]

        config = {
            'type': 'bar',
            'data': {
                'labels': timestamps,
                'datasets': [
                    {
                        'label': 'Added',
                        'data': daily_added,
                        'backgroundColor': self.theme['accent_green'] + 'cc',
                        'borderColor': self.theme['accent_green'],
                        'borderWidth': 1,
                        'borderRadius': 4
                    },
                    {
                        'label': 'Removed',
                        'data': daily_removed,
                        'backgroundColor': self.theme['accent_red'] + 'cc',
                        'borderColor': self.theme['accent_red'],
                        'borderWidth': 1,
                        'borderRadius': 4
                    }
                ]
            },
            'options': {
                **self.get_common_options(),
                'scales': {
                    'x': {
                        'grid': {
                            'display': False
                        },
                        'ticks': {
                            'color': self.theme['text_secondary'],
                            'maxRotation': 45,
                            'minRotation': 45
                        }
                    },
                    'y': {
                        'grid': {
                            'color': self.theme['grid_color'],
                            'drawBorder': False
                        },
                        'ticks': {
                            'color': self.theme['text_secondary']
                        },
                        'beginAtZero': True
                    }
                },
                'plugins': {
                    **self.get_common_options()['plugins'],
                    'title': {
                        'display': True,
                        'text': 'Daily IP Range Changes (Last 30 Days)',
                        'color': self.theme['text_primary'],
                        'font': {
                            'size': 16,
                            'weight': '500'
                        },
                        'padding': 20
                    }
                }
            }
        }

        return config

    def get_pie_chart_config(self, metrics: Dict) -> Dict:
        """
        Generate Pie Chart configuration for IPv4 vs IPv6 distribution.

        Chart displays:
        - Current IPv4 count (green)
        - Current IPv6 count (purple)
        """
        summary = metrics.get('summary', {})
        ipv4_count = summary.get('current_ipv4', 0)
        ipv6_count = summary.get('current_ipv6', 0)
        total = ipv4_count + ipv6_count

        # Calculate percentages
        ipv4_percent = (ipv4_count / total * 100) if total > 0 else 0
        ipv6_percent = (ipv6_count / total * 100) if total > 0 else 0

        config = {
            'type': 'doughnut',
            'data': {
                'labels': [
                    f'IPv4 ({ipv4_percent:.1f}%)',
                    f'IPv6 ({ipv6_percent:.1f}%)'
                ],
                'datasets': [{
                    'data': [ipv4_count, ipv6_count],
                    'backgroundColor': [
                        self.theme['accent_green'] + 'dd',
                        self.theme['accent_purple'] + 'dd'
                    ],
                    'borderColor': [
                        self.theme['accent_green'],
                        self.theme['accent_purple']
                    ],
                    'borderWidth': 2,
                    'hoverOffset': 10
                }]
            },
            'options': {
                **self.get_common_options(),
                'plugins': {
                    **self.get_common_options()['plugins'],
                    'title': {
                        'display': True,
                        'text': 'IPv4 vs IPv6 Distribution',
                        'color': self.theme['text_primary'],
                        'font': {
                            'size': 16,
                            'weight': '500'
                        },
                        'padding': 20
                    },
                    'tooltip': {
                        **self.get_common_options()['plugins']['tooltip'],
                        'callbacks': {
                            'label': '(ctx) => ctx.label + ": " + ctx.parsed.toLocaleString() + " ranges"'
                        }
                    }
                },
                'cutout': '60%'
            }
        }

        return config

    def generate_all_configs(self, metrics: Dict) -> Dict:
        """
        Generate all chart configurations.

        Returns:
            Dict containing all chart configs
        """
        configs = {
            'line_chart': self.get_line_chart_config(metrics),
            'bar_chart': self.get_bar_chart_config(metrics),
            'pie_chart': self.get_pie_chart_config(metrics),
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'service': 'ChartConfigService',
                'version': '1.1.0',
                'theme': 'chrome-dark'
            }
        }

        return configs

    def save_to_cache(self, configs: Dict) -> bool:
        """Save chart configs to cache file"""
        try:
            with open(self.config_cache_file, 'w') as f:
                json.dump(configs, f, indent=2)
            print(f"✅ Chart configs cached to {self.config_cache_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving configs to cache: {e}")
            return False

    def load_from_cache(self) -> Dict:
        """Load configs from cache file"""
        if not os.path.exists(self.config_cache_file):
            return {}

        try:
            with open(self.config_cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config cache: {e}")
            return {}

    def run(self, metrics: Dict, use_cache: bool = False) -> Dict:
        """
        Execute the chart config service.

        Args:
            metrics: Aggregated metrics from DataAggregatorService
            use_cache: If True, return cached configs if available

        Returns:
            Dict containing all chart configurations
        """
        if use_cache and os.path.exists(self.config_cache_file):
            print("📦 Loading chart configs from cache")
            return self.load_from_cache()

        print("🎨 Generating chart configurations...")
        configs = self.generate_all_configs(metrics)
        self.save_to_cache(configs)

        return configs


def main():
    """Standalone execution for testing"""
    # Load metrics from aggregator service cache
    metrics_file = 'cache/metrics.json'
    if not os.path.exists(metrics_file):
        print("❌ No metrics cache found. Run aggregator_service.py first.")
        return

    with open(metrics_file, 'r') as f:
        metrics = json.load(f)

    service = ChartConfigService()
    configs = service.run(metrics)

    print("\n" + "="*50)
    print("Chart Configuration Service - Results")
    print("="*50)
    print(f"Generated {len(configs) - 1} chart configurations:")
    print(f"  - Line Chart: {len(configs['line_chart']['data']['datasets'])} datasets")
    print(f"  - Bar Chart: {len(configs['bar_chart']['data']['datasets'])} datasets")
    print(f"  - Pie Chart: {len(configs['pie_chart']['data']['datasets'])} datasets")
    print("="*50)


if __name__ == '__main__':
    main()
