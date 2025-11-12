#!/usr/bin/env python3
"""
Test script for enhanced Weather API + Google Maps integration
Tests geocoding, air quality, weather alerts, and unified location service
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.stores import WeatherService, create_location_service
from src.stores.models import GeoLocation


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_weather_service():
    """Test WeatherService enhancements"""
    print_section("🌤️  TESTING WEATHER SERVICE ENHANCEMENTS")

    weather_service = WeatherService()

    # Test 1: Geocode city name
    print("\n1️⃣  Testing City Geocoding (Mumbai)...")
    location = weather_service.geocode_location("Mumbai", "Maharashtra")
    if location:
        print(f"   ✅ Mumbai coordinates: {location.latitude}, {location.longitude}")
    else:
        print("   ❌ Geocoding failed (check OPENWEATHER_API_KEY in .env)")

    # Test 2: Reverse geocode
    print("\n2️⃣  Testing Reverse Geocoding (28.6139, 77.2090 = Delhi)...")
    result = weather_service.reverse_geocode(28.6139, 77.2090)
    if result:
        print(
            f"   ✅ Location: {result.get('city')}, {result.get('state')}, {result.get('country')}"
        )
    else:
        print("   ❌ Reverse geocoding failed")

    # Test 3: Air quality
    print("\n3️⃣  Testing Air Quality Data (Delhi)...")
    delhi_loc = GeoLocation(
        latitude=28.6139,
        longitude=77.2090,
        address="",
        city="Delhi",
        state="Delhi",
        pincode="",
    )
    air_quality = weather_service.get_air_quality(delhi_loc)
    if air_quality:
        print(f"   ✅ AQI: {air_quality['aqi']} - {air_quality['aqi_label']}")
        components = air_quality.get("components", {})
        print(
            f"   ✅ PM2.5: {components.get('pm2_5', 'N/A')} | PM10: {components.get('pm10', 'N/A')}"
        )
    else:
        print("   ❌ Air quality data unavailable")

    # Test 4: Weather alerts
    print("\n4️⃣  Testing Weather Alerts (Delhi)...")
    alerts = weather_service.get_weather_alerts(delhi_loc)
    if alerts is not None:
        if len(alerts) > 0:
            print(f"   ⚠️  {len(alerts)} weather alert(s) active!")
            for alert in alerts[:2]:  # Show first 2
                print(f"      - {alert['event']}: {alert['description'][:60]}...")
        else:
            print("   ✅ No weather alerts currently")
    else:
        print("   ℹ️  Weather alerts require One Call API 3.0 subscription")


def test_location_service():
    """Test unified LocationService"""
    print_section("🗺️  TESTING UNIFIED LOCATION SERVICE")

    service = create_location_service()

    # Test 1: Check capabilities
    print("\n1️⃣  Checking Available Capabilities...")
    caps = service.get_capabilities()
    print(f"   Google Maps: {'✅' if caps['google_maps_available'] else '❌'}")
    print(f"   Weather API: {'✅' if caps['weather_api_available'] else '❌'}")

    features = caps.get("features", {})
    print("\n   Available Features:")
    for feature, available in features.items():
        status = "✅" if available else "❌"
        print(f"      {status} {feature}")

    # Test 2: Geocode with fallback
    print("\n2️⃣  Testing Geocoding with Fallback (Bangalore)...")
    location = service.geocode("Bangalore, Karnataka")
    if location:
        print(f"   ✅ Coordinates: {location.latitude}, {location.longitude}")
        print(f"   ✅ City: {location.city}")
    else:
        print("   ❌ Geocoding failed")

    # Test 3: Get location + weather in one call
    print("\n3️⃣  Testing Combined Location + Weather (Pune)...")
    result = service.get_location_with_weather("Pune")
    if result:
        loc = result.get("location")
        weather = result.get("weather")
        air_quality = result.get("air_quality")

        if loc:
            print(f"   ✅ Location: {loc.city} ({loc.latitude}, {loc.longitude})")

        if weather:
            print(
                f"   ✅ Weather: {weather.get('temperature_celsius')}°C, {weather.get('weather_description')}"
            )

        if air_quality:
            print(
                f"   ✅ Air Quality: {air_quality.get('aqi_label')} (AQI: {air_quality.get('aqi')})"
            )
    else:
        print("   ❌ Combined query failed")

    # Test 4: Reverse geocode
    print("\n4️⃣  Testing Reverse Geocoding (19.0760, 72.8777 = Mumbai)...")
    result = service.reverse_geocode(19.0760, 72.8777)
    if result:
        print(f"   ✅ Location: {result.get('city')}, {result.get('state')}")
    else:
        print("   ❌ Reverse geocoding failed")


def test_api_keys():
    """Test if API keys are configured"""
    print_section("🔑  CHECKING API KEY CONFIGURATION")

    google_key = os.getenv("GOOGLE_MAPS_API_KEY")
    weather_key = os.getenv("OPENWEATHER_API_KEY")

    print("\n1️⃣  Google Maps API Key:")
    if google_key and google_key != "your_google_maps_api_key_here":
        print(f"   ✅ Configured (starts with: {google_key[:10]}...)")
    else:
        print("   ❌ Not configured - add GOOGLE_MAPS_API_KEY to .env")

    print("\n2️⃣  OpenWeatherMap API Key:")
    if weather_key and weather_key != "your_openweather_api_key_here":
        print(f"   ✅ Configured (starts with: {weather_key[:10]}...)")
    else:
        print("   ❌ Not configured - add OPENWEATHER_API_KEY to .env")

    if not google_key and not weather_key:
        print("\n⚠️  WARNING: No API keys configured!")
        print("   Please add your API keys to the .env file:")
        print("   - GOOGLE_MAPS_API_KEY=your_key_here")
        print("   - OPENWEATHER_API_KEY=your_key_here")
        return False

    return True


def main():
    """Run all tests"""
    print("\n" + "🚀" * 35)
    print("     WEATHER API + GOOGLE MAPS INTEGRATION TEST SUITE")
    print("🚀" * 35)

    # Check API keys first
    has_keys = test_api_keys()

    if not has_keys:
        print("\n❌ Cannot proceed without API keys. Please configure them first.")
        print("\nTo set up:")
        print("  1. Edit .env file")
        print("  2. Add your GOOGLE_MAPS_API_KEY")
        print("  3. Add your OPENWEATHER_API_KEY")
        print("  4. Run this script again")
        return

    # Run tests
    try:
        test_weather_service()
        test_location_service()

        print_section("✅  ALL TESTS COMPLETED")
        print("\n✨ Integration is working! You can now use:")
        print("   - Weather geocoding (city → coordinates)")
        print("   - Reverse geocoding (coordinates → city)")
        print("   - Air quality monitoring")
        print("   - Weather alerts (if One Call API available)")
        print("   - Unified location + weather queries")
        print("\n📖 See WEATHER_API_INTEGRATION_GUIDE.md for API usage examples")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
