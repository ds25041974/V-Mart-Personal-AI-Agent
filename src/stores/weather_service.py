"""
Weather Service Integration
Fetches weather data from OpenWeatherMap API for store locations
Enhanced with geocoding, air quality, and weather alerts
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import requests

from .models import GeoLocation, WeatherData, WeatherPeriod


class WeatherService:
    """Weather data service using OpenWeatherMap API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize weather service

        Args:
            api_key: OpenWeatherMap API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "https://api.openweathermap.org/geo/1.0"

    def geocode_location(
        self, city: str, state: Optional[str] = None, country: str = "IN"
    ) -> Optional[GeoLocation]:
        """
        Convert city name to coordinates using OpenWeatherMap Geocoding API

        Args:
            city: City name (e.g., "Mumbai", "Delhi")
            state: Optional state name for precision
            country: Country code (default: "IN" for India)

        Returns:
            GeoLocation object or None if not found
        """
        if not self.api_key:
            print("Warning: No OpenWeatherMap API key configured")
            return None

        try:
            # Build location query
            query = f"{city}"
            if state:
                query += f",{state}"
            query += f",{country}"

            url = f"{self.geo_url}/direct"
            params = {"q": query, "limit": 1, "appid": self.api_key}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                print(f"Location not found: {query}")
                return None

            result = data[0]
            return GeoLocation(
                latitude=result["lat"],
                longitude=result["lon"],
                address="",
                city=result.get("name", city),
                state=result.get("state", state or ""),
                pincode="",
            )

        except Exception as e:
            print(f"Error geocoding location: {e}")
            return None

    def reverse_geocode(
        self, latitude: float, longitude: float
    ) -> Optional[Dict[str, str]]:
        """
        Convert coordinates to location name using OpenWeatherMap Reverse Geocoding

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            Dictionary with 'city', 'state', 'country' or None if error
        """
        if not self.api_key:
            print("Warning: No OpenWeatherMap API key configured")
            return None

        try:
            url = f"{self.geo_url}/reverse"
            params = {
                "lat": latitude,
                "lon": longitude,
                "limit": 1,
                "appid": self.api_key,
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data:
                return None

            result = data[0]
            return {
                "city": result.get("name", "Unknown"),
                "state": result.get("state", ""),
                "country": result.get("country", ""),
                "local_names": result.get("local_names", {}),
            }

        except Exception as e:
            print(f"Error reverse geocoding: {e}")
            return None

    def get_air_quality(self, location: GeoLocation) -> Optional[Dict]:
        """
        Get air quality data for a location

        Args:
            location: GeoLocation object with coordinates

        Returns:
            Dictionary with AQI and pollutant data or None if error
        """
        if not self.api_key:
            print("Warning: No OpenWeatherMap API key configured")
            return None

        try:
            url = "https://api.openweathermap.org/data/2.5/air_pollution"
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.api_key,
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get("list"):
                return None

            aqi_data = data["list"][0]

            # AQI levels: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
            aqi_labels = {
                1: "Good",
                2: "Fair",
                3: "Moderate",
                4: "Poor",
                5: "Very Poor",
            }

            return {
                "aqi": aqi_data["main"]["aqi"],
                "aqi_label": aqi_labels.get(aqi_data["main"]["aqi"], "Unknown"),
                "components": aqi_data.get("components", {}),
                "timestamp": datetime.now(),
                "location": {
                    "city": location.city,
                    "coordinates": f"{location.latitude}, {location.longitude}",
                },
            }

        except Exception as e:
            print(f"Error fetching air quality: {e}")
            return None

    def get_weather_alerts(self, location: GeoLocation) -> Optional[List[Dict]]:
        """
        Get weather alerts/warnings for a location (requires One Call API 3.0)

        Args:
            location: GeoLocation object with coordinates

        Returns:
            List of alert dictionaries or None if unavailable
        """
        if not self.api_key:
            print("Warning: No OpenWeatherMap API key configured")
            return None

        try:
            url = "https://api.openweathermap.org/data/3.0/onecall"
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.api_key,
                "exclude": "minutely,hourly,daily",  # Only get alerts
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 401:
                print("Weather alerts require One Call API 3.0 subscription")
                return None

            response.raise_for_status()
            data = response.json()

            alerts = data.get("alerts", [])
            if not alerts:
                return []

            formatted_alerts = []
            for alert in alerts:
                formatted_alerts.append(
                    {
                        "sender": alert.get("sender_name", "Unknown"),
                        "event": alert.get("event", "Weather Alert"),
                        "description": alert.get("description", ""),
                        "start": datetime.fromtimestamp(alert.get("start", 0)),
                        "end": datetime.fromtimestamp(alert.get("end", 0)),
                        "tags": alert.get("tags", []),
                    }
                )

            return formatted_alerts

        except Exception as e:
            print(f"Error fetching weather alerts: {e}")
            return None

    def get_current_weather(self, location: GeoLocation) -> Optional[WeatherData]:
        """
        Get current weather for a location

        Args:
            location: GeoLocation object with coordinates

        Returns:
            WeatherData object or None if error
        """
        if not self.api_key:
            print("Warning: No OpenWeatherMap API key configured")
            return self._get_mock_weather(location)

        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.api_key,
                "units": "metric",  # Celsius
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return self._parse_current_weather(data, location)

        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_mock_weather(location)

    def get_forecast_weather(
        self, location: GeoLocation, days: int = 15
    ) -> List[WeatherData]:
        """
        Get weather forecast for upcoming days (up to 15 days)

        Args:
            location: GeoLocation object with coordinates
            days: Number of days to forecast (1-15, default 15)

        Returns:
            List of WeatherData objects for different periods
        """
        # Limit to 15 days maximum
        days = min(days, 15)

        if not self.api_key:
            print("Warning: No OpenWeatherMap API key configured")
            return self._get_mock_forecast(location, days)

        try:
            # For 5 days or less, use standard forecast API (free)
            if days <= 5:
                url = f"{self.base_url}/forecast"
                params = {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "appid": self.api_key,
                    "units": "metric",
                    "cnt": days * 8,  # 8 forecasts per day (3-hour intervals)
                }

                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                return self._parse_forecast_weather(data, location)

            else:
                # For 6-15 days, try One Call API 3.0 (requires subscription)
                # Falls back to mock data if not available
                url = "https://api.openweathermap.org/data/3.0/onecall"
                params = {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "appid": self.api_key,
                    "units": "metric",
                    "exclude": "minutely,hourly,alerts",  # Only daily forecast
                }

                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 401:
                    # API key doesn't have access to One Call API - use mock data
                    print(
                        f"One Call API not available (15-day forecast requires subscription). Using mock data for days 6-{days}"
                    )
                    # Get 5-day real forecast + mock data for remaining days
                    real_forecast = self.get_forecast_weather(location, days=5)
                    mock_forecast = self._get_mock_forecast(
                        location, days - 5, start_day=5
                    )
                    return real_forecast + mock_forecast

                response.raise_for_status()
                data = response.json()

                return self._parse_onecall_forecast(data, location, days)

        except Exception as e:
            print(f"Error fetching {days}-day forecast: {e}")
            return self._get_mock_forecast(location, days)

    def get_weather_by_period(
        self, location: GeoLocation, target_date: datetime
    ) -> Dict[WeatherPeriod, WeatherData]:
        """
        Get weather for all periods (Morning, Afternoon, Evening, Night) of a date

        Args:
            location: GeoLocation object
            target_date: Target date

        Returns:
            Dictionary mapping WeatherPeriod to WeatherData
        """
        forecast = self.get_forecast_weather(location, days=5)

        weather_by_period = {}
        target_day = target_date.date()

        for weather in forecast:
            if weather.date.date() == target_day:
                weather_by_period[weather.period] = weather

        return weather_by_period

    def _parse_current_weather(self, data: Dict, location: GeoLocation) -> WeatherData:
        """Parse OpenWeatherMap current weather response"""
        current_hour = datetime.now().hour
        period = self._get_period_from_hour(current_hour)

        return WeatherData(
            location=location,
            date=datetime.now(),
            period=period,
            temperature_celsius=data["main"]["temp"],
            feels_like_celsius=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            weather_condition=data["weather"][0]["main"],
            weather_description=data["weather"][0]["description"],
            wind_speed=data["wind"]["speed"] * 3.6,  # m/s to km/h
            visibility=data.get("visibility", 10000) / 1000,  # meters to km
            last_updated=datetime.now(),
        )

    def _parse_forecast_weather(
        self, data: Dict, location: GeoLocation
    ) -> List[WeatherData]:
        """Parse OpenWeatherMap forecast response (5-day, 3-hour intervals)"""
        weather_list = []

        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            period = self._get_period_from_hour(dt.hour)

            weather = WeatherData(
                location=location,
                date=dt,
                period=period,
                temperature_celsius=item["main"]["temp"],
                feels_like_celsius=item["main"]["feels_like"],
                humidity=item["main"]["humidity"],
                weather_condition=item["weather"][0]["main"],
                weather_description=item["weather"][0]["description"],
                wind_speed=item["wind"]["speed"] * 3.6,
                visibility=item.get("visibility", 10000) / 1000,
                last_updated=datetime.now(),
            )
            weather_list.append(weather)

        return weather_list

    def _parse_onecall_forecast(
        self, data: Dict, location: GeoLocation, days: int
    ) -> List[WeatherData]:
        """Parse OpenWeatherMap One Call API forecast (up to 15 days)"""
        weather_list = []

        # One Call API returns daily forecasts
        for i, daily in enumerate(data.get("daily", [])[:days]):
            base_date = datetime.fromtimestamp(daily["dt"])

            # Generate weather for different periods of the day
            for period in WeatherPeriod:
                # Use different temperature values based on period
                if period == WeatherPeriod.MORNING:
                    temp = daily["temp"]["morn"]
                    feels_like = daily["feels_like"]["morn"]
                elif period == WeatherPeriod.AFTERNOON:
                    temp = daily["temp"]["day"]
                    feels_like = daily["feels_like"]["day"]
                elif period == WeatherPeriod.EVENING:
                    temp = daily["temp"]["eve"]
                    feels_like = daily["feels_like"]["eve"]
                else:  # NIGHT
                    temp = daily["temp"]["night"]
                    feels_like = daily["feels_like"]["night"]

                weather = WeatherData(
                    location=location,
                    date=base_date,
                    period=period,
                    temperature_celsius=temp,
                    feels_like_celsius=feels_like,
                    humidity=daily["humidity"],
                    weather_condition=daily["weather"][0]["main"],
                    weather_description=daily["weather"][0]["description"],
                    wind_speed=daily["wind_speed"] * 3.6,  # m/s to km/h
                    visibility=10.0,  # Daily forecast doesn't include visibility
                    last_updated=datetime.now(),
                )
                weather_list.append(weather)

        return weather_list

    def _get_period_from_hour(self, hour: int) -> WeatherPeriod:
        """Determine period from hour (24-hour format)"""
        if 6 <= hour < 12:
            return WeatherPeriod.MORNING
        elif 12 <= hour < 18:
            return WeatherPeriod.AFTERNOON
        elif 18 <= hour < 22:
            return WeatherPeriod.EVENING
        else:
            return WeatherPeriod.NIGHT

    def _get_mock_weather(self, location: GeoLocation) -> WeatherData:
        """Generate mock weather data when API is unavailable"""
        current_hour = datetime.now().hour
        period = self._get_period_from_hour(current_hour)

        # Simulate weather based on period
        temp_by_period = {
            WeatherPeriod.MORNING: 22,
            WeatherPeriod.AFTERNOON: 32,
            WeatherPeriod.EVENING: 28,
            WeatherPeriod.NIGHT: 20,
        }

        return WeatherData(
            location=location,
            date=datetime.now(),
            period=period,
            temperature_celsius=temp_by_period[period],
            feels_like_celsius=temp_by_period[period] + 2,
            humidity=65,
            weather_condition="Clear",
            weather_description="clear sky",
            wind_speed=15.0,
            visibility=10.0,
            last_updated=datetime.now(),
        )

    def _get_mock_forecast(
        self, location: GeoLocation, days: int, start_day: int = 0
    ) -> List[WeatherData]:
        """
        Generate mock forecast data

        Args:
            location: GeoLocation object
            days: Number of days to forecast
            start_day: Starting day offset (0 = today, 1 = tomorrow, etc.)
        """
        forecast = []

        for day in range(start_day, start_day + days):
            date = datetime.now() + timedelta(days=day)

            for period in WeatherPeriod:
                temp_variations = {
                    WeatherPeriod.MORNING: 22,
                    WeatherPeriod.AFTERNOON: 32,
                    WeatherPeriod.EVENING: 28,
                    WeatherPeriod.NIGHT: 20,
                }

                # Add realistic variations based on day
                day_variation = (day % 7) - 3  # -3 to +3 variation

                weather = WeatherData(
                    location=location,
                    date=date,
                    period=period,
                    temperature_celsius=temp_variations[period] + day_variation,
                    feels_like_celsius=temp_variations[period] + day_variation + 2,
                    humidity=55 + (day * 3) % 30,  # 55-85% range
                    weather_condition="Clear"
                    if day % 3 == 0
                    else ("Cloudy" if day % 3 == 1 else "Rain"),
                    weather_description="clear sky"
                    if day % 3 == 0
                    else ("few clouds" if day % 3 == 1 else "light rain"),
                    wind_speed=10.0 + (day * 1.5) % 15,  # 10-25 km/h range
                    visibility=10.0,
                    last_updated=datetime.now(),
                )
                forecast.append(weather)

        return forecast


def get_weather_icon(condition: str) -> str:
    """Get weather icon emoji based on condition"""
    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️",
    }
    return icons.get(condition, "🌤️")


def get_temperature_color(temp_celsius: float) -> str:
    """Get color code for temperature visualization"""
    if temp_celsius < 15:
        return "#4A90E2"  # Blue (Cold)
    elif temp_celsius < 25:
        return "#7ED321"  # Green (Pleasant)
    elif temp_celsius < 35:
        return "#F5A623"  # Orange (Warm)
    else:
        return "#D0021B"  # Red (Hot)
