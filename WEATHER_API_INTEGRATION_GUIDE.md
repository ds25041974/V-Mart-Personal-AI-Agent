# 🌤️ Weather API + Google Maps Integration Guide

## Overview

This guide covers the enhanced weather and location services that combine **OpenWeatherMap** and **Google Maps** APIs for comprehensive geo-location and weather capabilities.

## 🎯 Key Features

### ✅ What's New

1. **Geocoding (City → Coordinates)**
   - Convert city names to GPS coordinates
   - Uses OpenWeatherMap Geocoding API
   - Free with basic OpenWeatherMap account

2. **Reverse Geocoding (Coordinates → City)**
   - Convert GPS coordinates to location names
   - Get city, state, and country information

3. **Air Quality Monitoring**
   - Real-time Air Quality Index (AQI)
   - Pollutant levels (PM2.5, PM10, CO, NO2, etc.)
   - AQI labels: Good, Fair, Moderate, Poor, Very Poor

4. **Weather Alerts**
   - Severe weather warnings
   - Storm, heat wave, and other alerts
   - Requires One Call API 3.0 (paid subscription)

5. **Unified Location Service**
   - Combines Google Maps + OpenWeatherMap
   - Automatic fallback between APIs
   - Get location + weather in one call

---

## 🔧 Setup

### Step 1: Get API Keys

#### OpenWeatherMap API (Required)
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Get API key from dashboard
4. **Free tier includes:**
   - Current weather data
   - 5-day forecast
   - Geocoding
   - Air quality data
   - **Limit:** 60 calls/minute, 1,000,000 calls/month

#### Google Maps API (Optional)
1. Go to https://console.cloud.google.com/google/maps-apis
2. Create project and enable APIs:
   - Geocoding API
   - Places API
3. Create API key
4. **Add restrictions:**
   - Application restrictions (IP addresses or HTTP referrers)
   - API restrictions (only enable needed APIs)

### Step 2: Configure .env File

Add your API keys to `.env`:

```bash
# OpenWeatherMap API Key (Weather & Geocoding)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Google Maps API Key (Geocoding & Places API)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

**Security Note:** Never commit `.env` file to Git! It's already in `.gitignore`.

### Step 3: Test Integration

Run the test script:

```bash
python test_weather_integration.py
```

---

## 📡 API Endpoints

### 1. Geocode Location

**Endpoint:** `GET /stores/geocode`

Convert city or address to coordinates.

**Query Parameters:**
- `query` (required): City or address name
- `prefer` (optional): Preferred API - "google" or "weather" (default: "google")

**Example:**
```bash
curl "http://localhost:8000/stores/geocode?query=Mumbai,Maharashtra"
```

**Response:**
```json
{
  "success": true,
  "location": {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "address": "",
    "city": "Mumbai",
    "state": "Maharashtra"
  }
}
```

---

### 2. Reverse Geocode

**Endpoint:** `GET /stores/reverse-geocode`

Convert coordinates to location name.

**Query Parameters:**
- `lat` (required): Latitude
- `lon` (required): Longitude

**Example:**
```bash
curl "http://localhost:8000/stores/reverse-geocode?lat=28.6139&lon=77.2090"
```

**Response:**
```json
{
  "success": true,
  "location": {
    "city": "Delhi",
    "state": "Delhi",
    "country": "IN",
    "local_names": {...}
  }
}
```

---

### 3. Air Quality Data

**Endpoint:** `GET /stores/air-quality/<latitude>/<longitude>`

Get air quality index and pollutant levels.

**Example:**
```bash
curl "http://localhost:8000/stores/air-quality/28.6139/77.2090?city=Delhi"
```

**Response:**
```json
{
  "success": true,
  "air_quality": {
    "aqi": 3,
    "aqi_label": "Moderate",
    "components": {
      "pm2_5": 45.2,
      "pm10": 78.5,
      "no2": 25.3,
      "o3": 12.1,
      "co": 280.5
    },
    "timestamp": "2025-11-12T10:30:00",
    "location": {
      "city": "Delhi",
      "coordinates": "28.6139, 77.2090"
    }
  }
}
```

**AQI Levels:**
- **1 = Good** - Air quality is satisfactory
- **2 = Fair** - Acceptable for most people
- **3 = Moderate** - May affect sensitive individuals
- **4 = Poor** - May affect general population
- **5 = Very Poor** - Health warnings

---

### 4. Weather Alerts

**Endpoint:** `GET /stores/weather-alerts/<latitude>/<longitude>`

Get severe weather warnings (requires One Call API 3.0 subscription).

**Example:**
```bash
curl "http://localhost:8000/stores/weather-alerts/28.6139/77.2090?city=Delhi"
```

**Response (with alerts):**
```json
{
  "success": true,
  "count": 1,
  "alerts": [
    {
      "sender": "India Meteorological Department",
      "event": "Heat Wave Warning",
      "description": "Heat wave conditions expected to prevail...",
      "start": "2025-11-12T06:00:00",
      "end": "2025-11-14T18:00:00",
      "tags": ["Extreme temperature"]
    }
  ]
}
```

**Response (no subscription):**
```json
{
  "success": false,
  "error": "Weather alerts unavailable (requires One Call API 3.0 subscription)"
}
```

---

### 5. Location + Weather (Combined)

**Endpoint:** `GET /stores/location-with-weather`

Get location details AND weather in one call.

**Query Parameters:**
- `query` (required): City or address name

**Example:**
```bash
curl "http://localhost:8000/stores/location-with-weather?query=Pune"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "location": {
      "latitude": 18.5204,
      "longitude": 73.8567,
      "city": "Pune",
      "state": "Maharashtra"
    },
    "weather": {
      "temperature_celsius": 28.5,
      "feels_like_celsius": 30.2,
      "humidity": 65,
      "weather_condition": "Clear",
      "weather_description": "clear sky",
      "wind_speed": 12.5,
      "visibility": 10.0
    },
    "air_quality": {
      "aqi": 2,
      "aqi_label": "Fair",
      "components": {...}
    },
    "timestamp": "2025-11-12T10:30:00"
  }
}
```

---

### 6. Service Capabilities

**Endpoint:** `GET /stores/capabilities`

Check which features are available based on configured API keys.

**Example:**
```bash
curl "http://localhost:8000/stores/capabilities"
```

**Response:**
```json
{
  "success": true,
  "capabilities": {
    "google_maps_available": true,
    "weather_api_available": true,
    "features": {
      "address_geocoding": true,
      "city_geocoding": true,
      "reverse_geocoding": true,
      "nearby_search": true,
      "weather_data": true,
      "air_quality": true,
      "weather_alerts": false
    }
  }
}
```

---

## 💻 Python API Usage

### Example 1: Basic Weather Service

```python
from src.stores import WeatherService
from src.stores.models import GeoLocation

# Initialize service
weather_service = WeatherService()

# Geocode a city
location = weather_service.geocode_location("Mumbai", "Maharashtra")
print(f"Mumbai: {location.latitude}, {location.longitude}")

# Get air quality
air_quality = weather_service.get_air_quality(location)
print(f"AQI: {air_quality['aqi_label']}")

# Reverse geocode
result = weather_service.reverse_geocode(28.6139, 77.2090)
print(f"Location: {result['city']}, {result['state']}")
```

### Example 2: Unified Location Service

```python
from src.stores import create_location_service

# Initialize service (reads API keys from .env)
service = create_location_service()

# Check capabilities
caps = service.get_capabilities()
print(f"Google Maps: {caps['google_maps_available']}")
print(f"Weather API: {caps['weather_api_available']}")

# Geocode with automatic fallback
location = service.geocode("Bangalore, Karnataka")

# Get location + weather in one call
result = service.get_location_with_weather("Delhi")
print(f"Temperature: {result['weather']['temperature_celsius']}°C")
print(f"Air Quality: {result['air_quality']['aqi_label']}")

# Find nearby stores with weather
stores = service.find_nearby_stores_with_weather(
    latitude=28.6139,
    longitude=77.2090,
    store_name="V-Mart",
    radius=5000  # 5km
)
```

---

## 🎯 Use Cases

### 1. Store Location Intelligence

```python
# Get weather for all V-Mart stores
from src.stores import StoreDatabase, WeatherService

db = StoreDatabase("data/stores.db")
weather_service = WeatherService()

stores = db.get_vmart_stores_by_city("Mumbai")
for store in stores:
    weather = weather_service.get_current_weather(store.location)
    air_quality = weather_service.get_air_quality(store.location)
    
    print(f"{store.store_name}:")
    print(f"  Weather: {weather.temperature_celsius}°C, {weather.weather_description}")
    print(f"  Air Quality: {air_quality['aqi_label']}")
```

### 2. Customer Query with Location

```python
# User asks: "What's the weather near Connaught Place?"
service = create_location_service()

# Geocode the location
location = service.geocode("Connaught Place, Delhi")

# Get weather + air quality
result = service.get_location_with_weather("Connaught Place, Delhi")

# Check for alerts
alerts = weather_service.get_weather_alerts(location)
if alerts:
    print(f"⚠️ {len(alerts)} weather alert(s) active!")
```

### 3. Find Stores Near User

```python
# User provides their current location
user_lat, user_lon = 19.0760, 72.8777  # Mumbai

# Find nearby V-Mart stores with weather
stores = service.find_nearby_stores_with_weather(
    latitude=user_lat,
    longitude=user_lon,
    store_name="V-Mart",
    radius=10000  # 10km
)

for store in stores:
    print(f"{store['name']}:")
    print(f"  Distance: {store.get('distance', 'N/A')} km")
    if store.get('weather'):
        print(f"  Weather: {store['weather']['temperature_celsius']}°C")
```

---

## 💰 Cost Estimation

### OpenWeatherMap (Required)

**Free Tier:**
- ✅ Current weather
- ✅ 5-day forecast
- ✅ Geocoding
- ✅ Air quality
- ✅ 60 calls/minute
- ✅ 1,000,000 calls/month

**One Call API 3.0 (Weather Alerts):**
- ❌ Not included in free tier
- 💵 $0.0012 per call
- For 1,000 calls/month: ~$1.20/month

### Google Maps (Optional)

**Free Tier:**
- ✅ $200 free credit/month
- ✅ Covers ~40,000 geocoding requests

**After Free Tier:**
- 💵 Geocoding: $0.005 per request
- 💵 Places API: $0.017 per request

**Recommendation:** Use OpenWeatherMap for geocoding (free) and Google Maps only for detailed address lookup.

---

## 🔒 Security Best Practices

### 1. API Key Protection

✅ **DO:**
- Store keys in `.env` file only
- Add `.env` to `.gitignore`
- Use environment variables in code
- Add API restrictions in provider consoles

❌ **DON'T:**
- Hard-code API keys
- Commit keys to Git
- Share keys in chat or email
- Use keys without restrictions

### 2. Google Maps Restrictions

In Google Cloud Console, add:
- **Application restrictions:**
  - IP addresses (for server)
  - HTTP referrers (for web apps)
- **API restrictions:**
  - Enable only: Geocoding API, Places API

### 3. Rate Limiting

Monitor API usage:
- OpenWeatherMap: 60 calls/minute
- Google Maps: Watch $200/month credit

---

## 🐛 Troubleshooting

### Issue: "API key not configured"

**Solution:**
1. Check `.env` file exists
2. Verify key format (starts with correct prefix)
3. Restart server after adding keys

### Issue: "Geocoding failed"

**Solution:**
1. Check API key is valid
2. Verify internet connection
3. Try different city format: "City, State"

### Issue: "Weather alerts unavailable"

**Solution:**
- This is normal for free tier
- Upgrade to One Call API 3.0 if needed
- Or ignore alerts feature

### Issue: "Air quality data unavailable"

**Solution:**
1. Check OpenWeatherMap API key
2. Verify coordinates are valid
3. Some locations may not have AQI data

---

## 📊 Testing

Run comprehensive tests:

```bash
# Test all features
python test_weather_integration.py

# Test individual components
python -m src.stores.weather_service
python -m src.stores.location_service
```

---

## 🚀 Next Steps

1. **Add Your API Keys** to `.env` file
2. **Run Tests** with `python test_weather_integration.py`
3. **Start Server** with `python backend_server.py`
4. **Try API Endpoints** using curl or Postman
5. **Integrate with Chatbot** for location-based queries

---

## 📞 Support

- **OpenWeatherMap Docs:** https://openweathermap.org/api
- **Google Maps Docs:** https://developers.google.com/maps
- **Issues:** Create GitHub issue in repository

---

**Status:** ✅ Ready for production  
**Created:** November 12, 2025  
**Version:** 1.0.0
