# ./tests/__init__.py

"""
Test suite package.

Provides access to all test case classes in the package.
"""

from .test_weather_integration import TestWeatherIntegration
from .test_ltr_evaluation import TestLtrEvaluation
from .test_regex import TestRegEx

__all__ = [
    "TestWeatherIntegration",
    "TestLtrEvaluation",
    "TestRegEx",
]
