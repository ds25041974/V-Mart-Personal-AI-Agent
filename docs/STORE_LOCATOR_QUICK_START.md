# V-Mart Store Locator - Quick Start Guide

## 🚀 Getting Started

The Store Locator system is now running at **http://localhost:8000**

---

## ⚡ Quick Actions

### 1. Initialize Database (First Time Only)
```bash
curl -X POST http://localhost:8000/stores/initialize
```

**What it does:**
- Creates database tables
- Adds 11 V-Mart stores
- Adds 18 competitor stores
- Across 10 major Indian cities

**Expected Output:**
```json
{
  "success": true,
  "message": "Database initialized successfully",
  "vmart_stores": 11,
  "competitor_stores": 18
}
```

### 2. View Interactive Map
Open in browser:
```
http://localhost:8000/stores/map
```

**Features:**
- 🔵 Blue markers: V-Mart stores
- 🟠 Orange markers: V2 Retail
- 🟣 Purple markers: Zudio
- 🔴 Red markers: Style Bazar
- 🟡 Yellow markers: Max Fashion
- 🟢 Green markers: Pantaloons
- Click any marker for store details + real-time weather

---

## 📊 API Examples

### Get All V-Mart Stores
```bash
curl http://localhost:8000/stores/vmart
```

### Get Stores in Mumbai
```bash
curl "http://localhost:8000/stores/vmart?city=Mumbai"
```

### Get Competitor Stores
```bash
curl http://localhost:8000/stores/competitors
```

### Get Only Zudio Stores
```bash
curl "http://localhost:8000/stores/competitors?chain=Zudio"
```

### Get Weather for a Location
```bash
curl "http://localhost:8000/stores/weather/28.7372/77.1188?city=Delhi&state=Delhi"
```

### Analyze Competition Near a Store
```bash
curl "http://localhost:8000/stores/proximity-analysis/VM_DL_001?radius=5.0"
```

### Get All Stores in a City
```bash
curl http://localhost:8000/stores/city/Bangalore
```

### Get Overall Summary
```bash
curl http://localhost:8000/stores/summary
```

---

## 🗺️ Current Store Coverage

### V-Mart Stores (11 locations)
| Store ID | City | Address |
|----------|------|---------|
| VM_DL_001 | Delhi | Rohini Sector 11 |
| VM_GGN_001 | Gurgaon | Sector 14 Market |
| VM_NDA_001 | Noida | Sector 18, Atta Market |
| VM_MUM_001 | Mumbai | Andheri West |
| VM_MUM_002 | Thane | Ghodbunder Road |
| VM_BLR_001 | Bangalore | JP Nagar 3rd Phase |
| VM_BLR_002 | Bangalore | Whitefield Main Road |
| VM_HYD_001 | Hyderabad | KPHB Colony, Kukatpally |
| VM_CHN_001 | Chennai | Usman Road, T Nagar |
| VM_PUN_001 | Pune | Baner Road |
| VM_KOL_001 | Kolkata | Salt Lake Sector V |

### Competitor Chains Tracked
- **V2 Retail** - 2 stores
- **Zudio** (Tata) - 4 stores
- **Style Bazar** - 2 stores
- **Max Fashion** (Landmark) - 3 stores
- **Pantaloons** (Aditya Birla) - 3 stores
- **Reliance Trends** - 2 stores
- **Westside** (Tata) - 2 stores

---

## 🌤️ Weather Integration

### What Data is Tracked
- **Temperature**: Real-time in Celsius
- **Feels Like**: Perceived temperature
- **Humidity**: Percentage
- **Wind Speed**: km/h
- **Visibility**: km
- **Condition**: Clear, Cloudy, Rainy, etc.

### Time Periods
- ☀️ **Morning**: 6 AM - 12 PM
- ⛅ **Afternoon**: 12 PM - 6 PM
- 🌆 **Evening**: 6 PM - 10 PM
- 🌙 **Night**: 10 PM - 6 AM

### API Key (Optional)
Get free API key from: https://openweathermap.org/api

Add to `.env`:
```env
OPENWEATHER_API_KEY=your_key_here
```

**Note:** System works without API key (uses mock weather data)

---

## 🔄 Auto-Updates

### Scheduler Status
The system automatically updates:

1. **Weather Data** - Every 3 hours
   - Fetches current weather for all stores
   - Stores historical data
   
2. **Proximity Analysis** - Daily at 2:00 AM
   - Recalculates competitor distances
   - Updates competition metrics
   
3. **Daily Summary** - Daily at 6:00 AM
   - Logs store statistics
   - Reports top cities
   - Competition overview

**Check Scheduler:**
```bash
# See logs
tail -f ~/Library/Logs/vmart-ai.log
```

---

## 📍 Adding New Stores

### Via Python Code
```python
from src.stores import StoreDatabase, Store, GeoLocation, StoreChain
from datetime import datetime

db = StoreDatabase("data/stores.db")

# Add V-Mart Store
location = GeoLocation(
    latitude=28.6139,
    longitude=77.2090,
    address="Connaught Place",
    city="Delhi",
    state="Delhi",
    pincode="110001"
)

store = Store(
    store_id="VM_DL_003",
    store_name="V-Mart Delhi CP",
    chain=StoreChain.VMART,
    location=location,
    phone="+91-11-12345678",
    opening_hours="10:00 AM - 10:00 PM",
    store_size_sqft=30000,
    is_active=True
)

db.add_vmart_store(store)
print("✓ Store added successfully")
```

### Via API (Future Feature)
Coming soon: POST endpoint to add stores via API

---

## 🎯 Common Use Cases

### 1. Find All Competitors in My City
```bash
curl http://localhost:8000/stores/city/Mumbai
```

**Use Case:** Market research, competition analysis

### 2. Check Weather Before Store Visit
```bash
curl "http://localhost:8000/stores/weather/19.1136/72.8697?city=Mumbai"
```

**Use Case:** Delivery planning, staff scheduling

### 3. Identify Overcrowded Markets
```bash
curl http://localhost:8000/stores/proximity-analysis/all
```

**Use Case:** Expansion planning, avoid saturated areas

### 4. Monitor Top Performing Cities
```bash
curl http://localhost:8000/stores/summary
```

**Use Case:** Regional strategy, resource allocation

---

## 🔧 Troubleshooting

### Database Not Found
**Error:** `no such table: vmart_stores`

**Solution:**
```bash
curl -X POST http://localhost:8000/stores/initialize
```

### Weather API Not Working
**Symptom:** Mock weather data always showing

**Solution:**
1. Get API key: https://openweathermap.org/api
2. Add to `.env`: `OPENWEATHER_API_KEY=your_key`
3. Restart server

### Map Not Loading
**Symptom:** Blank page at /stores/map

**Solution:**
1. Check internet connection (Leaflet CDN required)
2. Initialize database first
3. Check browser console for errors

### Scheduler Not Running
**Symptom:** No auto-updates

**Solution:**
Check server logs:
```bash
tail -f ~/Library/Logs/vmart-ai.log
```

Look for:
```
✓ Store Update Scheduler initialized
Scheduler started
```

---

## 📱 Mobile Access

The map is fully responsive! Access from:
- 📱 Mobile browsers
- 💻 Tablets
- 🖥️ Desktops

**URL:** http://your-server-ip:8000/stores/map

---

## 🔐 Security Notes

### Public Endpoints (No Auth Required)
- `/stores/vmart` - Store listings
- `/stores/competitors` - Competitor data
- `/stores/weather/*` - Weather data
- `/stores/map` - Map visualization
- `/stores/summary` - Statistics

### Protected Endpoints (Future)
- Adding/editing stores (admin only)
- Deleting stores (admin only)
- Bulk operations (admin only)

---

## 📈 Performance Tips

### For Large Datasets
1. **Use Filters**: Prefer city/state filters over fetching all stores
2. **Pagination**: Request data in batches
3. **Caching**: Weather data is cached for 3 hours
4. **Indexing**: Database indexes on city, state, coordinates

### Optimal Radius
- **Urban areas**: 3-5 km
- **Suburban**: 5-10 km
- **Rural**: 10-20 km

---

## 🎓 Learning Resources

### Technologies Used
- **Backend**: Flask, SQLite
- **Maps**: Leaflet.js (OpenStreetMap)
- **Weather**: OpenWeatherMap API
- **Scheduling**: Python schedule library
- **Distance**: Haversine formula

### Tutorials
- Leaflet.js: https://leafletjs.com/examples.html
- OpenWeatherMap: https://openweathermap.org/appid
- Flask Blueprints: https://flask.palletsprojects.com/blueprints/

---

## 🚀 Next Steps

1. **Initialize database**: `POST /stores/initialize`
2. **View map**: http://localhost:8000/stores/map
3. **Test APIs**: Try the example curl commands above
4. **Add stores**: Use Python code to add your stores
5. **Monitor updates**: Watch scheduler logs
6. **Explore data**: Browse summary and proximity analysis

---

## 💬 Support

**Documentation:** `docs/STORE_LOCATOR_GUIDE.md`  
**API Reference:** See STORE_LOCATOR_GUIDE.md  
**Developed by:** DSR  
**Version:** 1.0  
**Date:** November 10, 2025

---

**Ready to explore your store network! 🎉**
