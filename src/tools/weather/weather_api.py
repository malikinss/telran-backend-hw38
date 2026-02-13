# ./src/tools/weather/weather_api.py

import os
import requests
from typing import Any, Dict
from .weather_info import WeatherInfo

JSONType = Dict[str, Any]


class WeatherAPI:
    """
    Client for interacting with the WeatherAPI service.

    Reads API configuration from environment variables and provides
    a method for retrieving current weather information.
    """

    def __init__(
        self,
        url_env: str = "WEATHER_API_URL",
        key_env: str = "WEATHER_API_KEY",
    ) -> None:
        """
        Initialize WeatherAPI client.

        Args:
            url_env: Environment variable name for API base URL.
            key_env: Environment variable name for API key.

        Raises:
            RuntimeError: If required environment variables are missing.
        """
        self.api_url: str = os.getenv(url_env)  # type: ignore
        self.api_key: str = os.getenv(key_env)  # type: ignore

        if not self.api_url or not self.api_key:
            raise RuntimeError(
                "Weather API environment variables are not set."
            )

    def get_weather(self, city: str) -> WeatherInfo:
        """
        Fetch current weather for a given city.

        Args:
            city: Name of the city.

        Returns:
            WeatherInfo instance with current weather data.

        Raises:
            ValueError: If the city is not found or the request fails.
        """
        params: Dict[str, str] = {
            "key": self.api_key,
            "q": city,
            "aqi": "no",
        }

        try:
            response = requests.get(
                self.api_url,
                params=params,
                timeout=10,
            )
            response.raise_for_status()
            data: JSONType = response.json()

            return self._parse_weather(data, city)

        except requests.RequestException as exc:
            raise ValueError(
                f"Failed to get weather for '{city}': {exc}"
            ) from exc

    def _parse_weather(
        self,
        data: JSONType,
        city: str,
    ) -> WeatherInfo:
        """
        Convert raw API response into WeatherInfo.

        Args:
            data: JSON response from WeatherAPI.
            city: Requested city name (for error reporting).

        Returns:
            WeatherInfo object.

        Raises:
            ValueError: If API returns an error.
        """
        if "error" in data:
            raise ValueError(f"City '{city}' not found.")

        location = data["location"]["name"]
        current = data["current"]

        return WeatherInfo(
            city=location,
            temperature=current["temp_c"],
            condition=current["condition"]["text"],
            humidity=current["humidity"],
            wind_kph=current["wind_kph"],
        )
