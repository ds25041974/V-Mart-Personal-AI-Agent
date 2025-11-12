# ⚡ Weather API Quick Start

## 🎯 What You Got

Your V-Mart AI Agent now has **enhanced weather and location capabilities** combining:
- **OpenWeatherMap API** - Weather, geocoding, air quality
- **Google Maps API** - Advanced geocoding and places

## 🚀 Quick Setup (3 Minutes)

### Step 1: Add API Keys to .env

```bash
# Edit the .env file
nano "/Users/dineshsrivastava/Ai Chatbot for Gemini LLM/V-Mart Personal AI Agent/.env"

# Add these two lines (replace with your actual keys):
OPENWEATHER_API_KEY=your_openweather_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
```

### Step 2: Get API Keys

#### OpenWeatherMap (FREE, Required)
1. Go to: https://openweathermap.org/api
2. Click "Sign Up" → Create account
3. Go to "API keys" → Copy your key
4. Paste into `.env` file

#### Google Maps (OPTIONAL)
1. Go to: https://console.cloud.google.com/google/maps-apis
2. Create project → Enable "Geocoding API"
3. Create credentials → API key
4. Add restrictions (IP address)
5. Paste into `.env` file

### Step 3: Test Integration

```bash
cd "/Users/dineshsrivastava/Ai Chatbot for Gemini LLM/V-Mart Personal AI Agent"
python test_weather_integration.py
```

## ✨ New Features

### 1️⃣ Geocoding (City → Coordinates)
```bash
curl "http://localhost:8000/stores/geocode?query=Mumbai"
```

### 2️⃣ Air Quality Monitoring
```bash
curl "http://localhost:8000/stores/air-quality/28.6139/77.2090"
```

### 3️⃣ Location + Weather in One Call
```bash
curl "http://localhost:8000/stores/location-with-weather?query=Delhi"
```

### 4️⃣ Reverse Geocoding
```bash
curl "http://localhost:8000/stores/reverse-geocode?lat=19.0760&lon=72.8777"
```

## 📝 Python Usage

```python
from src.stores import create_location_service

# Create service
service = create_location_service()

# Geocode a city
location = service.geocode("Bangalore")
print(f"Coordinates: {location.latitude}, {location.longitude}")

# Get weather + air quality
result = service.get_location_with_weather("Pune")
print(f"Temp: {result['weather']['temperature_celsius']}°C")
print(f"AQI: {result['air_quality']['aqi_label']}")
```

## 💡 Chat Integration Examples

**User:** "What's the weather in Mumbai?"
```python
result = service.get_location_with_weather("Mumbai")
# Returns: location + weather + air quality
```

**User:** "Find V-Mart stores near Connaught Place"
```python
location = service.geocode("Connaught Place, Delhi")
stores = service.find_nearby_stores_with_weather(
    location.latitude, location.longitude, "V-Mart", 5000
)
```

## 💰 Cost

**OpenWeatherMap FREE tier:**
- ✅ 1,000,000 calls/month
- ✅ All features (weather, geocoding, air quality)
- ✅ Perfect for production use

**Google Maps (Optional):**
- ✅ $200 free credit/month (~40,000 requests)
- Can skip if using only OpenWeatherMap

## 📖 Full Documentation

See `WEATHER_API_INTEGRATION_GUIDE.md` for:
- Complete API reference
- Advanced usage examples
- Cost optimization tips
- Security best practices

## ✅ Checklist

- [ ] Added OPENWEATHER_API_KEY to .env
- [ ] (Optional) Added GOOGLE_MAPS_API_KEY to .env
- [ ] Ran test script successfully
- [ ] Tested geocoding endpoint
- [ ] Tested air quality endpoint
- [ ] Read full documentation

## 🆘 Troubleshooting

**"API key not configured"**
→ Check `.env` file has correct key

**"Location not found"**
→ Try format: "City, State" (e.g., "Mumbai, Maharashtra")

**"Air quality unavailable"**
→ Some locations don't have AQI data, this is normal

## 🎉 You're Ready!

Your integration is complete. Start using it in:
1. **API endpoints** - Test with curl
2. **Python code** - Import and use services
3. **Chatbot** - Location-based queries
4. **Store analytics** - Weather insights

---

**Need Help?** Check `WEATHER_API_INTEGRATION_GUIDE.md` for detailed examples.
