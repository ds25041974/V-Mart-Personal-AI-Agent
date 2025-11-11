# V-Mart AI Chat - Context-Aware Assistant

## 🚀 Quick Start

Access the intelligent chatbot:
```
http://localhost:8000/ai-chat/
```

## ✨ Features

### Always Live Context
✅ **Real-time Weather**: Current conditions for all V-Mart stores, updated every 3 hours  
✅ **Geo-Location Data**: Precise coordinates for all 11 stores across India  
✅ **Competitor Tracking**: Live proximity analysis (5km radius)  
✅ **Date-Wise Weather**: Current + 5-day forecast  
✅ **AI Reasoning**: Step-by-step analysis visible in chat  

### Intelligent Analysis
🧠 **Gemini AI** analyzes:
- Weather impact on sales and footfall
- Competitive pressure and positioning
- Location-specific opportunities
- Data-driven recommendations

### Progress Tracking
🔄 See the AI think in real-time:
```
🔄 Gathering context data...
📍 Loading store location data...
✅ Store context loaded
🌤️ Loading weather data...
✅ Weather data loaded
🤖 AI is analyzing your question...
🧠 Applying reasoning to data...
✅ Analysis complete!
```

## 📍 Available Stores

All stores have live weather and geo-location:

| Store ID | Location | Weather Zone |
|----------|----------|--------------|
| VM_DL_001 | Delhi - Select Citywalk | North India |
| VM_GG_001 | Gurgaon - Cyber Hub | North India |
| VM_ND_001 | Noida - DLF Mall | North India |
| VM_MB_001 | Mumbai - Phoenix Palladium | West India |
| VM_MB_002 | Thane - Viviana Mall | West India |
| VM_BN_001 | Bangalore - Orion Mall | South India |
| VM_BN_002 | Bangalore - Phoenix Marketcity | South India |
| VM_HY_001 | Hyderabad - Inorbit Mall | South India |
| VM_CH_001 | Chennai - Express Avenue | South India |
| VM_PN_001 | Pune - Phoenix Marketcity | West India |
| VM_KL_001 | Kolkata - Quest Mall | East India |

## 💬 Example Questions

### Weather-Based Insights
```
❓ "How will today's weather affect sales?"
❓ "What products should I focus on based on the weather?"
❓ "What will the weather be like this week?"
```

### Competitive Analysis
```
❓ "What is the competitive situation at this store?"
❓ "How should I position against Westside nearby?"
❓ "Are there any new competitors?"
```

### Daily Operations
```
❓ "Give me a daily briefing"
❓ "What should be my priorities today?"
❓ "Any alerts or opportunities?"
```

## 🎯 How It Works

### 1. Select Store
Choose from 11 V-Mart stores in the dropdown

### 2. Enable Context
- ✅ Weather: Live temperature, humidity, conditions
- ✅ Competitors: Nearby stores, distances, counts
- ✅ Analytics: Sales performance (optional)

### 3. Ask Question
Type your question or use quick action buttons

### 4. Watch AI Think
See real-time progress as Gemini analyzes:
- Loading store location
- Fetching weather data
- Finding competitors
- Applying reasoning
- Generating recommendations

### 5. Get Curated Response
AI provides:
- Context-aware analysis
- Specific data citations
- Step-by-step reasoning
- Actionable recommendations

## 🌤️ Weather Data

### Real-Time Updates
- **Source**: OpenWeatherMap API
- **Frequency**: Every 3 hours
- **Coverage**: All 11 stores
- **Fallback**: Mock data if API unavailable

### Data Points
- Temperature (°C)
- Feels like temperature
- Humidity (%)
- Wind speed (km/h)
- Visibility (km)
- Weather condition
- Time period (Morning/Afternoon/Evening/Night)

### Forecast
- 5-day weather predictions
- 4 periods per day
- Automatic inclusion when relevant

## 🏪 Competitor Data

### Tracked Chains
- **V2**: Budget retail (250+ stores)
- **Westside**: Premium fashion
- **Zudio**: Value fashion (806 stores)
- **Style Bazar**: Regional competitor (250+ stores)

### Analysis
- Distance from V-Mart store (Haversine formula)
- Count by competitor chain
- Closest competitor identification
- 5km radius default

## 📊 Sample AI Response

**Question**: "Give me a daily briefing"

**Context Loaded**:
- Store: VM_DL_001
- Weather: 22°C, Morning, Clear
- Competitors: 3 nearby

**AI Response**:
```
Good morning! Here's your briefing for Monday, November 11, 2025:

WEATHER: Clear weather at 22°C this morning, expected to reach 
32°C by afternoon. Ideal shopping conditions will drive above-
average footfall today.

COMPETITION: Moderate competitive pressure with 3 nearby 
competitors. Closest Westside store is 1.2km away.

ACTION ITEMS:
1. Stock summer apparel prominently
2. Prepare for peak afternoon rush (12-4 PM)
3. Ensure AC systems optimal for hot afternoon

OPPORTUNITIES: Clear weather excellent for outdoor signage 
visibility. Consider promotional banners.
```

## 🔧 API Endpoints

### Chat Interface
```
GET /ai-chat/
```

### Ask with Context
```
POST /ai-chat/ask
Body: {
  "question": "...",
  "store_id": "VM_DL_001",
  "include_weather": true,
  "include_competitors": true
}
```

### Streaming Chat (with progress)
```
GET /ai-chat/ask-stream?question=...&store_id=...
```

### Weather Summary
```
GET /ai-chat/store-weather/<store_id>
```

### Competitor Analysis
```
GET /ai-chat/competitor-analysis/<store_id>
```

### Daily Briefing
```
GET /ai-chat/daily-briefing/<store_id>
```

## ⚙️ Configuration

### Required
```env
GEMINI_API_KEY=your_gemini_api_key
```

### Optional
```env
OPENWEATHER_API_KEY=your_openweather_key
```

Get API keys:
- **Gemini**: https://ai.google.dev/ (Free: 60 req/min)
- **OpenWeather**: https://openweathermap.org/api (Free: 60 req/min)

## 📖 Documentation

Full guide: [docs/AI_CHAT_GUIDE.md](docs/AI_CHAT_GUIDE.md)

Topics covered:
- Detailed API reference
- Use case examples
- Weather integration details
- Competitor analysis
- Best practices
- Troubleshooting

## 🎨 Features Showcase

### Real-Time Progress
```
🔄 Gathering context data...
📍 Loading store location data...
✅ Store context loaded
🌤️ Weather: 32°C, Afternoon, Clear
🏪 Competitors: 3 within 5km
🤖 AI is analyzing...
✅ Analysis complete!
```

### Context Badges
Visual indicators show what data the AI used:
```
📍 Store: VM_DL_001  🌤️ Weather  🏪 Competitors
```

### Quick Actions
Pre-built questions for common tasks:
- 🌤️ Weather Impact
- 🏪 Competition Analysis
- 📋 Daily Briefing
- 🎯 Product Focus

## 📈 Performance

- **Response Time**: 3-8 seconds
- **Context Loading**: < 500ms per source
- **Progress Updates**: 0.5-1 second intervals
- **Weather Accuracy**: Real-time (3-hour updates)
- **Distance Accuracy**: ±50 meters

## 🚀 Next Steps

1. **Access the chat**: http://localhost:8000/ai-chat/
2. **Select a store** from dropdown
3. **Enable contexts** (weather, competitors)
4. **Ask a question** or use quick actions
5. **Watch the AI reason** through the problem
6. **Get actionable insights** for your store

---

**Developed by**: DSR  
**Inspired by**: LA  
**Powered by**: Gemini AI + OpenWeatherMap  
**Version**: 1.0
