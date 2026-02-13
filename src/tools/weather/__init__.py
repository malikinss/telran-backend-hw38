# ./src/tools/weather/__init__.py

"""
Weather package.

Provides:
    - WeatherAPI: Client for retrieving weather data.
    - WeatherInfo: Data model representing weather conditions.
"""

from .weather_api import WeatherAPI
from .weather_info import WeatherInfo

__all__ = [
    "WeatherAPI",
    "WeatherInfo",
]
