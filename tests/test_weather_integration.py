# ./tests/test_weather_integration.py

import unittest
from src.tools.weather import WeatherAPI, WeatherInfo

# --- Test Data ---
EXISTING_CITY = "London"
NON_EXISTING_CITY = "ThisCityDoesNotExist123456"


class TestWeatherIntegration(unittest.TestCase):
    """
    Integration tests for WeatherAPI.

    These tests perform real HTTP calls to the WeatherAPI service.
    Ensure the following environment variables are set:
        - WEATHER_API_KEY
        - WEATHER_API_URL

    The tests cover:
    - retrieval of weather data for an existing city,
    - handling of non-existing city queries.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initialize WeatherAPI client and validate environment.
        """
        cls.weather_api = WeatherAPI()

    # --- Helper methods ---

    def _assert_weather_info(self, info: WeatherInfo) -> None:
        """
        Assert that the WeatherInfo object contains valid data.

        Args:
            info: WeatherInfo object to validate.
        """
        self.assertIsInstance(info.city, str)
        self.assertIsInstance(info.temperature, (int, float))
        self.assertIsInstance(info.condition, str)
        self.assertIsInstance(info.humidity, int)
        self.assertIsInstance(info.wind_kph, (int, float))

    # --- Tests ---

    def test_existing_city(self) -> None:
        """
        Test that weather data is returned for a real city.
        """
        info = self.weather_api.get_weather(EXISTING_CITY)
        self._assert_weather_info(info)
        self.assertIn(EXISTING_CITY, info.city)

    def test_non_existing_city(self) -> None:
        """
        Test that querying a non-existent city raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.weather_api.get_weather(NON_EXISTING_CITY)
