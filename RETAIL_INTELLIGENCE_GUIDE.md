# V-Mart Retail Intelligence System
## AI-Powered Analytics, Forecasting & Planning

**Powered by Google Gemini 2.0 Flash**

---

## 🎯 Overview

V-Mart Retail Intelligence System is a comprehensive AI-powered platform that provides:
- **Real-time insights** for retail operations
- **Predictive analytics** for sales, inventory, and trends
- **Smart recommendations** for buying, merchandising, and planning
- **Natural conversation** with Gemini AI for any retail query

---

## 🚀 Features

### 1. **Sales Performance Analysis**
- Daily, weekly, monthly sales analysis with INR amounts
- Hourly sales patterns for peak hour identification
- Salesperson performance tracking and ranking
- Sales target vs actual achievement monitoring
- YoY, MoM, WoW growth analysis

**API Endpoint:** `POST /api/intelligence/sales/daily`

**Example Request:**
```json
{
  "sales_data": [
    {"date": "2025-11-01", "amount": 250000, "transactions": 85},
    {"date": "2025-11-02", "amount": 310000, "transactions": 102}
  ],
  "store_id": "VM_KNP_001"
}
```

**Example Response:**
```json
{
  "success": true,
  "summary": {
    "total_sales": "₹5.60 Lakh",
    "avg_daily_sales": "₹1.87 Lakh",
    "total_transactions": "530 transactions"
  },
  "ai_insights": "Sales show strong performance with 15.5% growth..."
}
```

---

### 2. **Hourly Sales Analysis**
Identify peak sales hours to optimize staffing, inventory, and promotions.

**API Endpoint:** `POST /api/intelligence/sales/hourly`

**Example Request:**
```json
{
  "hourly_data": [
    {"hour": 10, "amount": 15000, "transactions": 8},
    {"hour": 11, "amount": 28000, "transactions": 15},
    {"hour": 12, "amount": 45000, "transactions": 22}
  ],
  "date": "2025-11-15"
}
```

**Response includes:**
- Peak hour identification (time, sales ₹, percentage)
- Slowest hour analysis
- Staffing recommendations
- Promotional timing suggestions

---

### 3. **Inventory Planning & Forecasting**
AI-powered inventory optimization with procurement recommendations.

**Features:**
- Stock-out risk analysis
- Overstock identification
- Inter-Store Transfer (IST) planning
- Procurement recommendations (quantities + ₹ amounts)
- Seasonal inventory planning

**API Endpoint:** `POST /api/intelligence/insights/custom`

**Example:**
```json
{
  "query": "Plan inventory for next month's festive season",
  "analytics_type": "inventory",
  "context_data": {
    "current_stock": {"menswear": 1500, "womenswear": 2200},
    "avg_daily_sales": {"menswear": 50, "womenswear": 75}
  }
}
```

---

### 4. **Fashion & Trend Analysis**
Global and local fashion trend insights for buying and merchandising.

**Capabilities:**
- Global fashion trend analysis (seasonal)
- Indian market trend analysis (tier-2/3 cities)
- Image recognition for product attribute identification
- Buying recommendations with ₹ budget allocation
- Merchandising strategy suggestions

**Image Analysis (Gemini Vision):**
```json
{
  "query": "Analyze this product image and identify attributes",
  "analytics_type": "fashion",
  "context_data": {
    "image_path": "/path/to/product.jpg"
  }
}
```

**AI Response Example:**
- Product Type: Women's Kurti
- Color: Royal Blue
- Pattern: Floral Print
- Fabric: Cotton Blend
- Style: Casual/Festive
- Target Price Range: ₹499-₹799
- Recommendation: High demand for festive season

---

### 5. **Indian Festival Planning**
Comprehensive festival calendar with sales forecasting.

**Major Festivals Covered:**
- Diwali (3.5x sales multiplier)
- Durga Puja (3.0x)
- Eid (2.5x)
- Navratri (2.5x)
- Holi (2.0x)
- Raksha Bandhan (1.8x)
- Christmas, New Year

**Regional Festivals:**
- **Uttar Pradesh:** Chhath Puja, Ram Navami, Janmashtami
- **Bihar:** Chhath Puja, Makar Sankranti
- **Madhya Pradesh:** Teej, Gangaur
- **Rajasthan:** Gangaur, Teej, Desert Festival

**API Endpoint:** `GET /api/intelligence/festival/upcoming?region=Uttar Pradesh&months_ahead=3`

**Festival Inventory Planning:**
```json
{
  "query": "Plan inventory for Diwali 2025",
  "analytics_type": "festival",
  "context_data": {
    "festival": "Diwali",
    "base_daily_sales": 200000,
    "historical_growth": 3.5
  }
}
```

---

### 6. **Customer Analytics & Footfall Analysis**
Understand customer behavior and optimize conversion.

**Analyses:**
- Footfall patterns (hourly, daily, weekly)
- Sales conversion rates
- Customer demographics
- Catchment area analysis (within 5km radius)
- Customer Lifetime Value (CLV)
- Retention strategies

**Example Query:**
```json
{
  "query": "Analyze customer catchment area for Kanpur store",
  "analytics_type": "customer",
  "context_data": {
    "store_location": [26.4499, 80.3319],
    "monthly_footfall": 12500,
    "transactions": 3200,
    "sales_inr": 8500000
  }
}
```

**AI Insights Include:**
- Conversion Rate: 25.6% (3,200/12,500)
- Average Bill: ₹2,656
- Catchment Radius: 3-5 km
- Demographics: 70% families, 30% youth
- Recommendations for improving conversion

---

### 7. **Logistics & Operations Optimization**
Route planning, IST optimization, and people planning.

**Features:**
- Best route planning for deliveries
- Inter-Store Transfer (IST) optimization
- Warehouse utilization analysis
- Transportation cost reduction
- People planning & scheduling
- Operational bottleneck identification

**Example:**
```json
{
  "query": "Optimize inter-store transfer from Kanpur to Lucknow",
  "analytics_type": "logistics",
  "context_data": {
    "source_store": "VM_KNP_001",
    "target_store": "VM_LKO_001",
    "items": {"menswear_shirts": 200, "womenswear_kurtis": 150},
    "distance_km": 85
  }
}
```

---

### 8. **Marketing Performance Analysis**
Campaign ROI, channel effectiveness, and budget optimization.

**Metrics Tracked:**
- Campaign performance (₹ spent vs ₹ revenue)
- ROI calculation
- Channel effectiveness (Online, Offline, Social Media)
- Customer Acquisition Cost (CAC)
- Marketing Mix Optimization
- Budget allocation recommendations

**Example:**
```json
{
  "query": "Analyze last month's Diwali campaign performance",
  "analytics_type": "marketing",
  "context_data": {
    "campaign_spend_inr": 250000,
    "revenue_generated_inr": 1200000,
    "reach": 50000,
    "conversions": 850
  }
}
```

**AI Response:**
- ROI: 380% (₹12 Lakh revenue from ₹2.5 Lakh spend)
- CAC: ₹294 per customer
- Conversion Rate: 1.7%
- Recommendation: Increase budget for similar campaigns

---

### 9. **Natural Conversation with Gemini AI**
Chat naturally with the AI assistant for any retail query.

**Greetings Handled:**
- Hi, Hello, Hey
- Good Morning, Good Afternoon, Good Evening
- Namaste

**Example Conversations:**

**User:** "Hi"
**AI:** "Hello! I'm your V-Mart retail intelligence assistant. How can I help you today with sales analysis, inventory planning, fashion trends, or any other retail insights?"

**User:** "What will be the impact of weather on today's sales at Kanpur store?"
**AI:** *Analyzes weather data, historical correlation, provides detailed insights with ₹ impact*

**User:** "Should we increase menswear inventory for next month?"
**AI:** *Analyzes sales trends, seasonality, forecasts demand, recommends quantities and ₹ amounts*

---

## 📊 Data Formatting Standards

### Currency (INR)
- **₹1,500** - Amounts under 1 Lakh
- **₹1.50 Lakh** - Lakhs (1-99.99 Lakh)
- **₹1.25 Cr** - Crores (1+ Crore)

### Quantities
- **1,500 units** - With commas for thousands
- **1.5 Lakh pieces** - For large quantities

### Percentages
- **15.5%** - One decimal place
- **↑ 15.5%** - With growth arrow

### Dates
- **15-Nov-2025** - Short format (DD-MMM-YYYY)

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/intelligence/chat` | POST | Chat with AI for any retail query |
| `/api/intelligence/sales/daily` | POST | Daily sales analysis |
| `/api/intelligence/sales/hourly` | POST | Hourly sales pattern analysis |
| `/api/intelligence/sales/salesperson` | POST | Salesperson performance analysis |
| `/api/intelligence/sales/forecast` | POST | Sales forecasting |
| `/api/intelligence/festival/upcoming` | GET | Upcoming festivals |
| `/api/intelligence/insights/custom` | POST | Custom AI insights for any query |
| `/api/intelligence/health` | GET | System health check |

---

## 🎨 Use Cases

### Use Case 1: Peak Hour Staffing
**Question:** "What are the peak sales hours for our Kanpur store?"

**AI Analysis:**
- Analyzes hourly sales data
- Identifies peak hours: 11 AM-1 PM, 6 PM-8 PM
- Recommends: Add 2 more staff during peak hours
- Expected Impact: 15% increase in conversion

### Use Case 2: Festival Inventory Planning
**Question:** "How much inventory do we need for Diwali at all stores?"

**AI Analysis:**
- Historical Diwali sales: 3.5x normal
- Current avg daily sales: ₹2 Lakh
- Diwali period: 5 days
- **Forecast:** ₹35 Lakh (₹2L × 3.5 × 5 days)
- **Inventory Needed:** 5,000 pieces menswear, 7,000 pieces womenswear
- **Procurement Budget:** ₹18 Lakh

### Use Case 3: Underperforming Store Analysis
**Question:** "Why is Muzaffarpur store underperforming?"

**AI Analysis:**
- Compares with similar stores (Patna, Kanpur)
- Analyzes footfall, conversion, avg bill
- Identifies: Low conversion rate (18% vs 25% avg)
- **Recommendations:**
  1. Staff training on customer engagement
  2. Improve merchandising display
  3. Local festival promotions
  4. Expected improvement: 7% conversion increase = ₹2.5 Lakh monthly

---

## 🔐 Google Workspace Integration

Connect with Google apps for comprehensive data:

1. **Google Sheets:** Sales data, inventory sheets
2. **Google Drive:** Product catalogs, reports
3. **Google Analytics:** Website traffic, online sales
4. **Gmail:** Supplier communications, reports

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install google-generativeai google-auth-oauthlib google-api-python-client
```

### 2. Set Environment Variables
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export OPENWEATHER_API_KEY="your-weather-api-key"
```

### 3. Start Server
```bash
python main.py
```

### 4. Test AI Chat
```bash
curl -X POST http://localhost:8000/api/intelligence/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hi, how can you help me?"}'
```

---

## 💡 Tips for Best Results

1. **Be Specific:** "Analyze Kanpur store sales for last week" vs "Analyze sales"
2. **Provide Context:** Include dates, store IDs, amounts
3. **Ask Follow-ups:** AI maintains conversation context
4. **Use INR:** Always think in Indian Rupees (₹)
5. **Consider Festivals:** Indian festivals drive 40-50% annual sales

---

## 📈 Performance Metrics

The system analyzes:
- **Sales:** Daily, hourly, by category, by salesperson
- **Inventory:** Stock levels, turnover, stock-out risk
- **Customers:** Footfall, conversion, lifetime value
- **Marketing:** ROI, CAC, channel effectiveness
- **Operations:** IST, logistics, people planning
- **Fashion:** Trends, buying priorities, pricing

---

## 🎯 Business Impact

**Expected Benefits:**
- **15-20% increase** in sales through optimized staffing and inventory
- **25-30% reduction** in stock-outs during peak seasons
- **10-15% improvement** in inventory turnover
- **20-25% better** marketing ROI through targeted campaigns
- **Faster decision-making** with AI-powered insights

---

## 🆘 Support

For issues or questions:
1. Check AI health: `GET /api/intelligence/health`
2. Ask the AI: "How do I analyze X?"
3. Review this documentation

**Remember:** The AI is context-aware and learns from your queries. The more you interact, the better it understands your specific needs!

---

**Powered by Google Gemini 2.0 Flash | Built for V-Mart Retail Operations**
