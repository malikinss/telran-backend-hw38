# ./src/tools/weather/weather_info.py

from dataclasses import dataclass


@dataclass(slots=True)
class WeatherInfo:
    """
    Data container representing current weather conditions for a city.

    Attributes:
        city: City name.
        temperature: Air temperature in Celsius.
        condition: Text description of weather condition.
        humidity: Humidity percentage.
        wind_kph: Wind speed in kilometers per hour.
    """

    city: str
    temperature: float
    condition: str
    humidity: int
    wind_kph: float

    def __str__(self) -> str:
        """
        Return human-readable weather representation.
        """
        return (
            f"City: {self.city}\n"
            f"Temperature: {self.temperature} °C\n"
            f"Condition: {self.condition}\n"
            f"Humidity: {self.humidity}%\n"
            f"Wind speed: {self.wind_kph} kph"
        )
