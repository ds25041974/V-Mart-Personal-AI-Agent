# V-Mart Store Locator with Geo-Mapping & Weather Integration

## Overview

A comprehensive store location management system for V-Mart that provides:
- **Geographic mapping** of all V-Mart stores across India
- **Competitor analysis** tracking V2 Retail, Zudio, Style Bazar, Max Fashion, Pantaloons, Reliance Trends, Westside, and other apparel retailers
- **Real-time weather data** for each store location (Morning, Afternoon, Evening, Night periods)
- **Proximity analysis** showing competitors near each V-Mart store
- **Interactive map visualization** with Leaflet.js
- **Automatic data updates** on schedule

---

## Features

### ✅ V-Mart Store Management
- Store locations with GPS coordinates
- Complete address and contact information
- Store size, opening hours, manager details
- City and state-wise filtering
- Active/inactive store tracking

### ✅ Competitor Tracking
- **V2 Retail** - Value fashion chain
- **Zudio** - Tata's budget fashion brand
- **Style Bazar** - Regional fashion retailer
- **Max Fashion** - Landmark Group's value fashion
- **Pantaloons** - Aditya Birla Fashion & Retail
- **Reliance Trends** - Reliance Retail fashion
- **Westside** - Tata's lifestyle brand
- **Shoppers Stop** - Premium department store
- **Lifestyle** - Landmark Group's lifestyle store
- Other regional competitors

### ✅ Weather Integration
- **Current weather** for any store location
- **4 daily periods**: Morning (6-12), Afternoon (12-18), Evening (18-22), Night (22-6)
- **Metrics**: Temperature (°C), feels-like, humidity, wind speed, visibility
- **Forecast**: 5-day weather predictions
- **Visual indicators**: Weather icons and temperature color coding

### ✅ Proximity Analysis
- Find all competitors within configurable radius (default 5km)
- Count competitors by chain
- Identify closest competitor to each store
- Distance calculations using Haversine formula
- City-wise competition mapping

### ✅ Interactive Map
- Leaflet.js-based interactive map
- Color-coded markers for each chain:
  - 🔵 **V-Mart** - Blue
  - 🟠 **V2 Retail** - Orange
  - 🟣 **Zudio** - Purple
  - 🔴 **Style Bazar** - Red
  - 🟡 **Max Fashion** - Yellow
  - 🟢 **Pantaloons** - Green
  - 🔷 **Reliance Trends** - Light Blue
  - 🟪 **Westside** - Dark Purple
- Store popup with details and real-time weather
- Responsive design for mobile/desktop
- Legend for chain identification

### ✅ Auto-Update Scheduler
- **Weather updates**: Every 3 hours
- **Proximity analysis**: Daily at 2:00 AM
- **Daily summary**: Daily at 6:00 AM
- Background thread execution
- Automatic data refresh

---

## API Endpoints

### Store Management

#### GET /stores/initialize
Initialize database with sample store data
```bash
curl -X POST http://localhost:8000/stores/initialize
```

**Response:**
```json
{
  "success": true,
  "message": "Database initialized successfully",
  "vmart_stores": 11,
  "competitor_stores": 18
}
```

#### GET /stores/vmart
Get all V-Mart stores (with optional filters)
```bash
# All stores
curl http://localhost:8000/stores/vmart

# Filter by city
curl http://localhost:8000/stores/vmart?city=Mumbai

# Filter by state
curl http://localhost:8000/stores/vmart?state=Maharashtra
```

**Response:**
```json
{
  "success": true,
  "count": 11,
  "stores": [
    {
      "store_id": "VM_DL_001",
      "store_name": "V-Mart Delhi Rohini",
      "chain": "V-Mart",
      "location": {
        "latitude": 28.7372,
        "longitude": 77.1188,
        "address": "Sector 11, Rohini",
        "city": "Delhi",
        "state": "Delhi",
        "pincode": "110085"
      },
      "phone": "+91-11-27895600",
      "opening_hours": "10:00 AM - 10:00 PM",
      "store_size_sqft": 25000,
      "is_active": true
    }
  ]
}
```

#### GET /stores/vmart/<store_id>
Get specific V-Mart store details
```bash
curl http://localhost:8000/stores/vmart/VM_DL_001
```

#### GET /stores/competitors
Get competitor stores (with optional filters)
```bash
# All competitors
curl http://localhost:8000/stores/competitors

# Filter by chain
curl http://localhost:8000/stores/competitors?chain=Zudio

# Filter by city
curl http://localhost:8000/stores/competitors?city=Bangalore
```

### Weather Data

#### GET /stores/weather/<latitude>/<longitude>
Get current weather for coordinates
```bash
curl "http://localhost:8000/stores/weather/28.7372/77.1188?city=Delhi&state=Delhi"
```

**Response:**
```json
{
  "success": true,
  "weather": {
    "location": {
      "latitude": 28.7372,
      "longitude": 77.1188,
      "city": "Delhi",
      "state": "Delhi"
    },
    "date": "2025-11-10T14:30:00",
    "period": "Afternoon",
    "temperature_celsius": 32.5,
    "feels_like_celsius": 34.2,
    "humidity": 45,
    "weather_condition": "Clear",
    "weather_description": "clear sky",
    "wind_speed": 12.5,
    "visibility": 10.0
  },
  "icon": "☀️",
  "color": "#F5A623"
}
```

#### GET /stores/weather/forecast/<latitude>/<longitude>
Get weather forecast
```bash
curl "http://localhost:8000/stores/weather/forecast/28.7372/77.1188?days=5"
```

### Proximity Analysis

#### GET /stores/proximity-analysis/<store_id>
Analyze competitors near a V-Mart store
```bash
curl "http://localhost:8000/stores/proximity-analysis/VM_DL_001?radius=5.0"
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "vmart_store": {...},
    "total_competitors": 5,
    "search_radius_km": 5.0,
    "competitors_by_chain": {
      "Zudio": [{...}],
      "V2 Retail": [{...}],
      "Max Fashion": [{...}]
    },
    "closest_competitor": {
      "store_name": "Zudio Delhi Rajouri Garden",
      "chain": "Zudio",
      "distance_km": 2.3
    }
  }
}
```

#### GET /stores/proximity-analysis/all
Analyze all V-Mart stores
```bash
curl "http://localhost:8000/stores/proximity-analysis/all?radius=5.0"
```

### City & Summary

#### GET /stores/city/<city_name>
Get all stores in a city
```bash
curl http://localhost:8000/stores/city/Mumbai
```

**Response:**
```json
{
  "success": true,
  "city": "Mumbai",
  "vmart_stores": [...],
  "competitor_stores": [...],
  "vmart_count": 2,
  "competitor_count": 4
}
```

#### GET /stores/summary
Get overall competition summary
```bash
curl http://localhost:8000/stores/summary
```

**Response:**
```json
{
  "success": true,
  "total_vmart_stores": 11,
  "total_competitor_stores": 18,
  "competitors_by_chain": {
    "Zudio": 4,
    "V2 Retail": 2,
    "Max Fashion": 3,
    "Pantaloons": 3,
    "Reliance Trends": 2,
    "Westside": 2,
    "Style Bazar": 2
  },
  "top_10_cities": [
    {"city": "Delhi", "store_count": 3},
    {"city": "Mumbai", "store_count": 2},
    {"city": "Bangalore", "store_count": 2}
  ],
  "unique_cities": 10
}
```

### Map Visualization

#### GET /stores/map
View interactive map with all stores
```bash
# Open in browser
http://localhost:8000/stores/map
```

Features:
- Interactive Leaflet.js map
- All V-Mart and competitor stores
- Color-coded markers
- Store details on click
- Real-time weather in popups
- Legend for chain identification
- Responsive design

---

## Database Schema

### V-Mart Stores Table
```sql
CREATE TABLE vmart_stores (
    store_id VARCHAR(50) PRIMARY KEY,
    store_name VARCHAR(200) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    manager_name VARCHAR(100),
    opening_hours VARCHAR(100),
    store_size_sqft INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    opened_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Competitor Stores Table
```sql
CREATE TABLE competitor_stores (
    store_id VARCHAR(50) PRIMARY KEY,
    store_name VARCHAR(200) NOT NULL,
    chain VARCHAR(100) NOT NULL,  -- V2 Retail, Zudio, etc.
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    opening_hours VARCHAR(100),
    store_size_sqft INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Weather Data Table
```sql
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    weather_date DATE NOT NULL,
    period VARCHAR(20) NOT NULL,  -- Morning, Afternoon, Evening, Night
    temperature_celsius DECIMAL(5, 2) NOT NULL,
    feels_like_celsius DECIMAL(5, 2) NOT NULL,
    humidity INTEGER NOT NULL,
    weather_condition VARCHAR(50) NOT NULL,
    weather_description TEXT,
    wind_speed DECIMAL(5, 2),
    visibility DECIMAL(5, 2),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Competitor Proximity Table
```sql
CREATE TABLE competitor_proximity (
    id SERIAL PRIMARY KEY,
    vmart_store_id VARCHAR(50) NOT NULL,
    competitor_store_id VARCHAR(50) NOT NULL,
    distance_km DECIMAL(10, 2) NOT NULL,
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vmart_store_id) REFERENCES vmart_stores(store_id),
    FOREIGN KEY (competitor_store_id) REFERENCES competitor_stores(store_id)
);
```

---

## Configuration

### Environment Variables

Create `.env` file:
```env
# OpenWeatherMap API Key (optional - mock data used if not provided)
OPENWEATHER_API_KEY=your_api_key_here

# Google Gemini API
GEMINI_API_KEY=your_gemini_key_here

# Flask
SECRET_KEY=your_secret_key
```

### Get OpenWeatherMap API Key (Free)
1. Visit: https://openweathermap.org/api
2. Sign up for free account
3. Get API key from dashboard
4. Free tier: 60 calls/minute, 1,000,000 calls/month

---

## Initial Data

### Included V-Mart Stores (11 stores)
- Delhi Rohini
- Gurgaon Sector 14
- Noida Sector 18
- Mumbai Andheri
- Mumbai Thane
- Bangalore JP Nagar
- Bangalore Whitefield
- Hyderabad Kukatpally
- Chennai T Nagar
- Pune Baner
- Kolkata Salt Lake

### Included Competitor Stores (18 stores)
- **V2 Retail**: Delhi, Mumbai
- **Zudio**: Delhi, Mumbai, Bangalore, Hyderabad
- **Style Bazar**: Delhi, Bangalore
- **Max Fashion**: Delhi, Mumbai, Bangalore
- **Pantaloons**: Delhi, Mumbai, Chennai
- **Reliance Trends**: Gurgaon, Pune
- **Westside**: Noida, Kolkata

---

## Usage Examples

### 1. Initialize Database
```python
from src.stores import StoreDatabase, initialize_stores

db = StoreDatabase("data/stores.db")
initialize_stores(db)
```

### 2. Get V-Mart Stores in a City
```python
from src.stores import StoreDatabase

db = StoreDatabase("data/stores.db")
stores = db.get_vmart_stores_by_city("Mumbai")

for store in stores:
    print(f"{store.store_name} - {store.location.address}")
```

### 3. Analyze Competition
```python
from src.stores import StoreDatabase, StoreAnalyzer

db = StoreDatabase("data/stores.db")
analyzer = StoreAnalyzer(db)

analysis = analyzer.analyze_vmart_competition("VM_DL_001", radius_km=5.0)
print(f"Competitors within 5km: {analysis.get_competitor_count()}")

for chain, stores in analysis.get_competitors_by_chain().items():
    print(f"{chain}: {len(stores)} stores")
```

### 4. Get Weather Data
```python
from src.stores import StoreDatabase, WeatherService

db = StoreDatabase("data/stores.db")
weather_service = WeatherService()

store = db.get_vmart_store("VM_DL_001")
weather = weather_service.get_current_weather(store.location)

print(f"Temperature: {weather.temperature_celsius}°C")
print(f"Condition: {weather.weather_description}")
```

### 5. Start Auto-Update Scheduler
```python
from src.stores.update_scheduler import start_store_scheduler

scheduler = start_store_scheduler()
# Runs in background, updating weather every 3 hours
```

---

## Auto-Update Schedule

### Weather Updates (Every 3 Hours)
- Fetches current weather for all V-Mart stores
- Stores data with timestamp
- Rotates through Morning/Afternoon/Evening/Night periods
- Rate-limited to avoid API quota

### Proximity Analysis (Daily at 2:00 AM)
- Recalculates competitors within 5km of each store
- Updates distance measurements
- Refreshes proximity database

### Daily Summary (Daily at 6:00 AM)
- Logs total stores count
- Reports top cities
- Summarizes competition landscape

---

## File Structure

```
src/stores/
├── __init__.py              # Package exports
├── models.py                # Data models (Store, Weather, Location, etc.)
├── database.py              # SQLite database manager
├── weather_service.py       # OpenWeatherMap integration
├── analyzer.py              # Competitor proximity analyzer
├── initial_data.py          # Sample store data
└── update_scheduler.py      # Automated updates

src/web/
├── stores_routes.py         # Flask blueprint for API endpoints

data/
└── stores.db                # SQLite database (auto-created)
```

---

## Weather Period Logic

```python
Morning:   6:00 AM  - 12:00 PM
Afternoon: 12:00 PM - 6:00 PM
Evening:   6:00 PM  - 10:00 PM
Night:     10:00 PM - 6:00 AM
```

---

## Distance Calculation

Uses **Haversine formula** for accurate geographic distance:

```python
R = 6371  # Earth radius in km
distance = R * 2 * arcsin(sqrt(
    sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
))
```

Accuracy: ±0.5% for distances < 500km

---

## Adding New Stores

### Add V-Mart Store
```python
from src.stores import StoreDatabase, Store, GeoLocation, StoreChain
from datetime import datetime

db = StoreDatabase("data/stores.db")

location = GeoLocation(
    latitude=28.6139,
    longitude=77.2090,
    address="Connaught Place",
    city="Delhi",
    state="Delhi",
    pincode="110001"
)

store = Store(
    store_id="VM_DL_002",
    store_name="V-Mart Delhi CP",
    chain=StoreChain.VMART,
    location=location,
    phone="+91-11-12345678",
    opening_hours="10:00 AM - 10:00 PM",
    store_size_sqft=30000,
    is_active=True,
    opened_date=datetime.now()
)

db.add_vmart_store(store)
```

### Add Competitor Store
```python
competitor = Store(
    store_id="ZD_DL_002",
    store_name="Zudio Delhi Connaught Place",
    chain=StoreChain.ZUDIO,
    location=location,
    opening_hours="10:00 AM - 10:00 PM",
    is_active=True
)

db.add_competitor_store(competitor)
```

---

## Troubleshooting

### Weather Data Not Loading
- Check `OPENWEATHER_API_KEY` in environment
- Verify API key is active
- Check API quota limits
- Falls back to mock data if API unavailable

### Map Not Displaying
- Ensure internet connection (Leaflet CDN required)
- Check browser console for errors
- Verify Flask app is running on correct port

### Scheduler Not Running
```python
from src.stores.update_scheduler import get_scheduler

scheduler = get_scheduler()
scheduler.start()  # Start manually if not auto-started
```

---

## Future Enhancements

🔄 **Planned Features:**
- [ ] Real-time store foot traffic data
- [ ] Sales performance correlation with weather
- [ ] Competitor pricing intelligence
- [ ] Customer demographics mapping
- [ ] Heatmap of high-competition zones
- [ ] Store opening recommendations
- [ ] Mobile app integration
- [ ] CSV/Excel export of reports
- [ ] Email alerts for new competitors
- [ ] Historical weather trends

---

## Support

**Developed by:** DSR  
**Inspired by:** LA  
**Powered by:** Gemini AI & OpenWeatherMap  
**Map Technology:** Leaflet.js

**Last Updated:** November 10, 2025  
**Version:** 1.0  
**License:** Proprietary (V-Mart Internal Use)
