# ./src/tools/tools.py

"""
Tool registry.

Initializes available tools and exposes a unified mapping
for dynamic tool routing.
"""

from .ltr import LtrCalculator
from .weather import WeatherAPI

calculator = LtrCalculator()
weather_api = WeatherAPI()

TOOLS = {
    "ltr_evaluate": calculator.evaluate,
    "get_weather": weather_api.get_weather
}
