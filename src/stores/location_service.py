"""
Unified Location Service
Combines Google Maps and OpenWeatherMap geocoding capabilities
Provides fallback and best-of-both-worlds location services
"""

import os
from typing import Any, Dict, List, Optional

from .google_maps_api import GoogleMapsService
from .models import GeoLocation
from .weather_service import WeatherService


class LocationService:
    """
    Unified location service combining Google Maps and OpenWeatherMap
    - Google Maps: Primary for detailed address geocoding
    - OpenWeatherMap: Fallback and supplement for city-level geocoding
    """

    def __init__(
        self,
        google_api_key: Optional[str] = None,
        weather_api_key: Optional[str] = None,
    ):
        """
        Initialize location service

        Args:
            google_api_key: Google Maps API key (optional, reads from env)
            weather_api_key: OpenWeatherMap API key (optional, reads from env)
        """
        self.google_maps = GoogleMapsService(
            api_key=google_api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        )
        self.weather_service = WeatherService(
            api_key=weather_api_key or os.getenv("OPENWEATHER_API_KEY")
        )

        self.has_google = self.google_maps.client is not None
        self.has_weather = self.weather_service.api_key is not None

    def geocode(self, query: str, prefer: str = "google") -> Optional[GeoLocation]:
        """
        Geocode an address or city name to coordinates

        Args:
            query: Address or city name (e.g., "Mumbai" or "123 Main St, Delhi")
            prefer: Preferred API ("google" or "weather")

        Returns:
            GeoLocation object or None if not found
        """
        # Try preferred API first
        if prefer == "google" and self.has_google:
            result = self._geocode_with_google(query)
            if result:
                return result
            # Fallback to weather API
            if self.has_weather:
                return self._geocode_with_weather(query)
        else:
            # Try weather API first
            if self.has_weather:
                result = self._geocode_with_weather(query)
                if result:
                    return result
            # Fallback to Google
            if self.has_google:
                return self._geocode_with_google(query)

        return None

    def reverse_geocode(
        self, latitude: float, longitude: float, prefer: str = "google"
    ) -> Optional[Dict[str, str]]:
        """
        Convert coordinates to location details

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            prefer: Preferred API ("google" or "weather")

        Returns:
            Dictionary with location details or None
        """
        if prefer == "google" and self.has_google:
            # Google Maps doesn't have reverse geocode in current implementation
            # Use weather API
            if self.has_weather:
                return self.weather_service.reverse_geocode(latitude, longitude)
        else:
            if self.has_weather:
                return self.weather_service.reverse_geocode(latitude, longitude)

        return None

    def get_location_with_weather(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Get location details WITH current weather in one call

        Args:
            query: Address or city name

        Returns:
            Dictionary with location + weather data
        """
        # Get coordinates
        location = self.geocode(query)
        if not location:
            return None

        # Get weather for location
        weather = None
        if self.has_weather:
            weather = self.weather_service.get_current_weather(location)

        # Get air quality
        air_quality = None
        if self.has_weather:
            air_quality = self.weather_service.get_air_quality(location)

        return {
            "location": location,
            "weather": weather.to_dict() if weather else None,
            "air_quality": air_quality,
            "timestamp": weather.last_updated if weather else None,
        }

    def find_nearby_stores_with_weather(
        self, latitude: float, longitude: float, store_name: str, radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """
        Find nearby stores AND get weather for each location

        Args:
            latitude: Center point latitude
            longitude: Center point longitude
            store_name: Store brand to search for
            radius: Search radius in meters

        Returns:
            List of stores with weather data
        """
        if not self.has_google:
            print("Google Maps API required for store search")
            return []

        # Find stores using Google Maps
        stores = self.google_maps.find_stores_nearby(
            latitude, longitude, store_name, radius
        )

        # Enrich with weather data if available
        if self.has_weather:
            for store in stores:
                location = GeoLocation(
                    latitude=store["latitude"],
                    longitude=store["longitude"],
                    address=store.get("address", ""),
                    city="",
                    state="",
                    pincode="",
                )

                weather = self.weather_service.get_current_weather(location)
                store["weather"] = weather.to_dict() if weather else None

        return stores

    def _geocode_with_google(self, address: str) -> Optional[GeoLocation]:
        """Geocode using Google Maps API"""
        try:
            result = self.google_maps.geocode_address(address)
            if not result:
                return None

            formatted_address = result.get("formatted_address", address)
            if not isinstance(formatted_address, str):
                formatted_address = str(formatted_address)

            return GeoLocation(
                latitude=result["latitude"],
                longitude=result["longitude"],
                address=formatted_address,
                city="",  # Google Maps doesn't parse city separately
                state="",
                pincode="",
            )
        except Exception as e:
            print(f"Google geocoding error: {e}")
            return None

    def _geocode_with_weather(self, city: str) -> Optional[GeoLocation]:
        """Geocode using OpenWeatherMap API (city-level)"""
        try:
            # Extract city and state if comma-separated
            parts = city.split(",")
            city_name = parts[0].strip()
            state_name = parts[1].strip() if len(parts) > 1 else None

            return self.weather_service.geocode_location(
                city=city_name, state=state_name
            )
        except Exception as e:
            print(f"Weather geocoding error: {e}")
            return None

    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get information about available capabilities

        Returns:
            Dictionary showing which features are available
        """
        return {
            "google_maps_available": self.has_google,
            "weather_api_available": self.has_weather,
            "features": {
                "address_geocoding": self.has_google or self.has_weather,
                "city_geocoding": self.has_weather,
                "reverse_geocoding": self.has_weather,
                "nearby_search": self.has_google,
                "weather_data": self.has_weather,
                "air_quality": self.has_weather,
                "weather_alerts": self.has_weather,
            },
        }


# Convenience function
def create_location_service() -> LocationService:
    """
    Create a LocationService instance with API keys from environment

    Returns:
        LocationService instance
    """
    return LocationService()


if __name__ == "__main__":
    # Example usage
    print("🗺️  Unified Location Service Test")
    print("=" * 50)

    service = create_location_service()

    # Show capabilities
    caps = service.get_capabilities()
    print("\n✨ Available Features:")
    features = caps.get("features", {})
    if isinstance(features, dict):
        for feature, available in features.items():
            status = "✅" if available else "❌"
            print(f"  {status} {feature}")

    # Test geocoding
    print("\n🔍 Testing Geocoding:")
    location = service.geocode("Mumbai, Maharashtra")
    if location:
        print(f"  ✓ Mumbai: {location.latitude}, {location.longitude}")

    # Test location with weather
    print("\n🌤️  Testing Location + Weather:")
    result = service.get_location_with_weather("Delhi")
    if result:
        loc = result.get("location")
        if loc:
            print(f"  ✓ Location: {loc.city}")
        weather = result.get("weather")
        if weather:
            print(f"  ✓ Temperature: {weather.get('temperature_celsius')}°C")
        air_quality = result.get("air_quality")
        if air_quality:
            print(f"  ✓ Air Quality: {air_quality.get('aqi_label')}")
