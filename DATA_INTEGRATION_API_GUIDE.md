# V-Mart Retail Intelligence API Documentation
## Complete Guide to Data Integration & AI Insights

**Last Updated:** 11 November 2025  
**Version:** 2.0  
**Powered by:** Gemini 2.0 Flash AI

---

## 🎯 Overview

The V-Mart Retail Intelligence API provides comprehensive AI-powered insights through multiple data sources:
- **File Uploads**: CSV, Excel, PDF, JSON, Text files
- **Google Workspace**: Google Sheets integration
- **Databases**: SQL Server, PostgreSQL, Oracle, MySQL
- **Real-time AI**: Direct Gemini LLM conversation for all queries

**KEY PRINCIPLE:** All responses come directly from Gemini AI with context-aware, curated analysis including:
- Root cause analysis
- Rectification recommendations
- Implementation phases
- Fact-based analysis
- KPI tracking
- Next steps with monitoring

---

## 📊 DATA INTEGRATION ENDPOINTS

### 1. File Upload & Analysis

**Endpoint:** `POST /api/intelligence/data/upload`

**Supported Formats:**
- CSV (.csv)
- Excel (.xlsx, .xls)
- PDF (.pdf)
- JSON (.json)
- Text (.txt)

**Request (Multipart Form Data):**
```http
POST /api/intelligence/data/upload
Content-Type: multipart/form-data

file: [file binary]
data_context: "Monthly sales report for Kanpur store"
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/intelligence/data/upload \
  -F "file=@sales_data.csv" \
  -F "data_context=Monthly sales data for all stores"
```

**Response:**
```json
{
  "success": true,
  "file_type": "spreadsheet",
  "rows": 500,
  "columns": ["Date", "Store", "Sales_INR", "Transactions", "Category"],
  "numeric_summary": {
    "Sales_INR": {
      "mean": 285000,
      "min": 50000,
      "max": 950000,
      "total": 142500000
    },
    "Transactions": {
      "mean": 95,
      "total": 47500
    }
  },
  "ai_insights": "**Comprehensive Analysis from Gemini AI:**\n\n1. **Root Cause Analysis**: Sales show 15% decline in last month due to...\n2. **Key Insights**: Peak performing stores are Kanpur (₹35 Lakh) and Lucknow (₹32 Lakh)...\n3. **Rectification Steps**:\n   - Phase 1: Increase inventory for fast-moving categories\n   - Phase 2: Staff training on customer engagement\n   - Phase 3: Launch promotional campaigns\n4. **KPIs to Track**:\n   - Daily sales ₹ (Target: 15% increase)\n   - Conversion rate (Target: 25%)\n   - Average bill value (Target: ₹2,800)\n5. **Next Steps**: Implement rectification phases starting [date]...",
  "full_data": [...]
}
```

**AI Analysis Includes:**
1. **Data Understanding**: What the data represents
2. **Key Insights**: Most important findings
3. **Trends & Patterns**: Observable patterns
4. **Anomalies**: Unusual or concerning values
5. **Root Cause Analysis**: Why issues exist
6. **Rectification Steps**: How to fix problems (with phases)
7. **KPIs to Track**: Metrics to monitor
8. **Fact Analysis**: Data quality validation
9. **Implementation Phases**: Step-by-step action plan
10. **Next Steps**: Immediate actions required

---

### 2. Google Sheets Integration

**Endpoint:** `POST /api/intelligence/data/google-sheets`

**Prerequisites:**
```bash
pip install google-api-python-client google-auth-oauthlib
```

**Setup Google Credentials:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google Sheets API
3. Create Service Account → Download JSON credentials
4. Share your Google Sheet with service account email

**Request:**
```json
{
  "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "range": "Sheet1!A1:Z1000",
  "credentials_path": "/path/to/credentials.json"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/intelligence/data/google-sheets \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
    "range": "SalesData!A1:E500"
  }'
```

**Response:**
```json
{
  "success": true,
  "source": "Google Sheets",
  "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "rows": 499,
  "columns": ["Date", "Store", "Category", "Sales", "Units"],
  "data_sample": [...],
  "ai_insights": "**AI Analysis:**\n\n1. **Performance Summary**: Total sales ₹4.25 Cr across all stores...\n2. **Root Cause**: Declining trend in Menswear category due to...\n3. **Recommendations**: [Detailed recommendations]",
  "full_data": [...]
}
```

**Use Cases:**
- Daily sales tracking sheets
- Inventory management sheets
- Staff performance tracking
- Budget vs actual comparison
- Customer data analysis

---

### 3. Database Integration

**Endpoint:** `POST /api/intelligence/data/database`

**Supported Databases:**
- Microsoft SQL Server (`mssql`)
- PostgreSQL (`postgresql`)
- Oracle Database (`oracle`)
- MySQL (`mysql`)

**Prerequisites:**
```bash
# SQL Server
pip install pyodbc

# PostgreSQL
pip install psycopg2-binary

# Oracle
pip install cx_Oracle

# MySQL
pip install mysql-connector-python
```

**Request:**
```json
{
  "db_type": "mssql",
  "connection_params": {
    "host": "localhost",
    "database": "VmartRetail",
    "user": "vmart_user",
    "password": "secure_password"
  },
  "query": "SELECT Store, SUM(SalesAmount) as TotalSales, COUNT(*) as Transactions FROM Sales WHERE SaleDate >= '2025-10-01' GROUP BY Store ORDER BY TotalSales DESC",
  "query_context": "Monthly sales by store for October 2025"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/intelligence/data/database \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgresql",
    "connection_params": {
      "host": "db.vmart.com",
      "database": "retail_analytics",
      "user": "analyst",
      "password": "password123"
    },
    "query": "SELECT * FROM daily_sales WHERE date >= CURRENT_DATE - 30",
    "query_context": "Last 30 days sales data"
  }'
```

**Response:**
```json
{
  "success": true,
  "source": "mssql Database",
  "rows": 11,
  "columns": ["Store", "TotalSales", "Transactions"],
  "data_sample": [
    {"Store": "Kanpur", "TotalSales": 3500000, "Transactions": 1205},
    {"Store": "Lucknow", "TotalSales": 3200000, "Transactions": 1089}
  ],
  "numeric_summary": {
    "TotalSales": {
      "mean": 2545454,
      "total": 28000000
    }
  },
  "ai_insights": "**Database Analysis:**\n\n1. **Performance Ranking**: Kanpur leads with ₹35 Lakh...\n2. **Root Cause of Low Performance**: Muzaffarpur store (₹12 Lakh) underperforming due to...\n3. **Rectification Plan**:\n   - **Phase 1** (Week 1-2): Staff training and inventory adjustment\n   - **Phase 2** (Week 3-4): Local marketing campaigns\n   - **Phase 3** (Week 5-6): Performance monitoring and optimization\n4. **KPIs to Track Daily**:\n   - Store-wise sales ₹ (Target: 20% increase for bottom 3 stores)\n   - Transaction count (Target: 15% increase)\n   - Conversion rate by store\n5. **Next Steps**: [Detailed action items]",
  "full_data": [...]
}
```

**Security Best Practices:**
1. Use environment variables for credentials
2. Implement read-only database users
3. Use parameterized queries only
4. Enable SSL/TLS for connections
5. Rotate passwords regularly

---

## 💬 AI CONVERSATION ENDPOINT

### Chat with Gemini AI

**Endpoint:** `POST /api/intelligence/chat`

**Purpose:** Natural conversation for ANY retail question. All responses come directly from Gemini LLM with comprehensive analysis.

**Request:**
```json
{
  "query": "Why is our Muzaffarpur store underperforming?",
  "context_data": {
    "store_id": "VM_MUZ_001",
    "monthly_sales": 1200000,
    "target_sales": 2000000,
    "footfall": 5000,
    "transactions": 800
  }
}
```

**Response Format:**
```json
{
  "success": true,
  "query": "Why is our Muzaffarpur store underperforming?",
  "response": "**Root Cause Analysis for Muzaffarpur Store (VM_MUZ_001):**\n\n**Current Performance:**\n- Sales: ₹12 Lakh (40% below target of ₹20 Lakh)\n- Footfall: 5,000 visitors\n- Transactions: 800 (16% conversion rate - Below 25% benchmark)\n- Gap: ₹8 Lakh monthly revenue loss\n\n**Root Causes Identified:**\n\n1. **Low Conversion Rate (16%)**\n   - Cause: Staff engagement issues, inadequate training\n   - Impact: 450 potential customers not converting (9% gap to 25%)\n   - Revenue Loss: ₹3.6 Lakh/month\n\n2. **Low Average Bill (₹1,500 vs ₹2,500 avg)**\n   - Cause: Limited product availability, poor merchandising\n   - Impact: ₹1,000 less per transaction\n   - Revenue Loss: ₹8 Lakh/month\n\n3. **Insufficient Footfall (5,000 vs 8,000 benchmark)**\n   - Cause: Low brand awareness in locality, competition\n   - Impact: 3,000 fewer visitors\n   - Revenue Loss: ₹6 Lakh/month potential\n\n**Rectification Plan:**\n\n**Phase 1: Immediate Actions (Week 1-2)**\n- Train staff on customer engagement (2-day workshop)\n- Improve visual merchandising and displays\n- Stock fast-moving items from Kanpur/Patna stores (IST)\n- Launch local WhatsApp campaign (5km radius)\n- **Expected Impact**: 5% conversion improvement = ₹1.5 Lakh additional\n\n**Phase 2: Marketing Push (Week 3-4)**\n- Local newspaper ads and pamphlet distribution\n- Festival offer: 20% off on ₹2000+ purchases\n- Partner with local influencers\n- **Expected Impact**: 30% footfall increase = ₹3 Lakh additional\n\n**Phase 3: Sustained Improvement (Week 5-8)**\n- Monthly performance review with staff\n- Inventory optimization based on local preferences\n- Customer loyalty program launch\n- **Expected Impact**: Reach ₹18 Lakh (90% of target)\n\n**KPIs to Track (Daily):**\n- Conversion Rate: Current 16% → Target 22% (Week 4) → 25% (Week 8)\n- Average Bill: Current ₹1,500 → Target ₹2,000 (Week 4) → ₹2,500 (Week 8)\n- Daily Sales: Current ₹40,000 → Target ₹55,000 (Week 4) → ₹65,000 (Week 8)\n- Footfall: Current 167/day → Target 220/day (Week 4) → 265/day (Week 8)\n\n**Fact Analysis:**\n- Data Quality: ✅ Verified from store systems\n- Comparison Baseline: Patna store (similar demographic)\n- Assumptions: 60-day implementation timeline, ₹2 Lakh marketing budget\n\n**Next Steps:**\n1. **Tomorrow**: Schedule staff training session\n2. **Day 3**: Execute IST of 500 units from Kanpur\n3. **Day 5**: Launch local marketing campaign\n4. **Day 7**: First performance review\n5. **Day 14**: Phase 1 completion assessment\n6. **Day 30**: Phase 2 completion assessment\n7. **Day 60**: Final performance evaluation\n\n**Expected ROI:**\n- Investment: ₹2 Lakh (marketing + training)\n- Additional Revenue (8 weeks): ₹12 Lakh\n- ROI: 500% in 2 months\n\n**Monitoring Dashboard:**\nTrack these metrics daily on store manager dashboard:\n- Sales ₹ vs Target\n- Conversion Rate %\n- Average Bill ₹\n- Footfall Count\n- Staff Performance Scores",
  "type": "ai_insights"
}
```

**Example Queries:**

1. **Root Cause Analysis:**
```json
{"query": "Why did sales drop 20% last month?"}
```

2. **Rectification Planning:**
```json
{"query": "How do we fix low conversion rate at our stores?"}
```

3. **Phase Tracking:**
```json
{"query": "Create implementation plan for Diwali festival preparation"}
```

4. **Fact Analysis:**
```json
{"query": "Validate this sales data - is it accurate?", "context_data": {...}}
```

5. **KPI Recommendations:**
```json
{"query": "What KPIs should we track for inventory optimization?"}
```

6. **Next Steps:**
```json
{"query": "What are immediate actions needed to improve store performance?"}
```

**Greeting Support:**
The AI naturally handles:
- Hi, Hello, Hey
- Good Morning, Good Afternoon, Good Evening
- Namaste

Example:
```json
{"query": "Hi"}
→ Response: "Hello! I'm your V-Mart retail intelligence assistant powered by Gemini AI. I can help you with sales analysis, inventory planning, fashion trends, festival forecasting, customer analytics, and much more. What insights can I provide today?"
```

---

## 🎯 SPECIALIZED ANALYTICS ENDPOINTS

### Sales Analytics

**1. Daily Sales Analysis**
```bash
POST /api/intelligence/sales/daily
{
  "sales_data": [...],
  "store_id": "VM_KNP_001"
}
```

**2. Hourly Pattern Analysis**
```bash
POST /api/intelligence/sales/hourly
{
  "hourly_data": [...],
  "date": "2025-11-15"
}
```

**3. Salesperson Performance**
```bash
POST /api/intelligence/sales/salesperson
{
  "salesperson_data": [...],
  "period": "monthly"
}
```

**4. Sales Forecasting**
```bash
POST /api/intelligence/sales/forecast
{
  "historical_data": [...],
  "forecast_days": 30
}
```

### Festival Planning

**Upcoming Festivals**
```bash
GET /api/intelligence/festival/upcoming?region=Uttar Pradesh&months_ahead=6
```

### Custom Insights

**Universal Endpoint**
```bash
POST /api/intelligence/insights/custom
{
  "query": "Any retail question",
  "analytics_type": "sales|inventory|fashion|customer|festival|logistics|marketing",
  "context_data": {...}
}
```

---

## 🔧 INSTALLATION & SETUP

### 1. Install Dependencies

```bash
# Core AI
pip install google-generativeai

# Data Processing
pip install pandas openpyxl

# Google Workspace
pip install google-api-python-client google-auth-oauthlib

# Databases (choose what you need)
pip install pyodbc  # SQL Server
pip install psycopg2-binary  # PostgreSQL
pip install cx_Oracle  # Oracle
pip install mysql-connector-python  # MySQL

# PDF Processing
pip install PyPDF2
```

### 2. Environment Variables

Create `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_CREDENTIALS_PATH=/path/to/google-credentials.json
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

### 3. Start Server

```bash
cd "/Users/dineshsrivastava/Ai Chatbot for Gemini LLM/V-Mart Personal AI Agent"
source venv/bin/activate
python main.py
```

Server runs at: `http://localhost:8000`

---

## 📝 COMPLETE USE CASE EXAMPLES

### Use Case 1: Monthly Sales Report Analysis

**Scenario:** Upload monthly sales CSV and get comprehensive AI insights

**Step 1: Prepare CSV**
```csv
Date,Store,Category,Sales_INR,Units_Sold,Transactions
2025-10-01,Kanpur,Menswear,85000,120,45
2025-10-01,Lucknow,Womenswear,95000,145,52
...
```

**Step 2: Upload**
```bash
curl -X POST http://localhost:8000/api/intelligence/data/upload \
  -F "file=@october_sales.csv" \
  -F "data_context=October 2025 monthly sales report"
```

**Step 3: Receive AI Analysis**
- Root cause of performance issues
- Store-wise recommendations
- Category trends
- Implementation phases
- KPIs to track
- Next steps

---

### Use Case 2: Real-time Database Query Analysis

**Scenario:** Query production database and get AI insights

```bash
curl -X POST http://localhost:8000/api/intelligence/data/database \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "mssql",
    "connection_params": {
      "host": "prod-db.vmart.com",
      "database": "RetailAnalytics",
      "user": "readonly_user",
      "password": "secure_pass"
    },
    "query": "SELECT Store, Category, SUM(SalesAmount) as Sales FROM DailySales WHERE SaleDate BETWEEN ''2025-10-01'' AND ''2025-10-31'' GROUP BY Store, Category ORDER BY Sales DESC",
    "query_context": "October category performance by store"
  }'
```

**AI Response Includes:**
- Category performance analysis
- Store-specific recommendations
- Underperforming category root causes
- Rectification steps with phases
- KPI tracking dashboard design
- Implementation timeline

---

### Use Case 3: Google Sheets Live Analysis

**Scenario:** Analyze live Google Sheet with daily updates

**Step 1: Share Sheet**
- Share Google Sheet with service account email
- Grant "Viewer" access

**Step 2: Query API**
```bash
curl -X POST http://localhost:8000/api/intelligence/data/google-sheets \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
    "range": "DailySales!A1:G1000"
  }'
```

**Step 3: Get Real-time Insights**
- Daily sales trends
- Performance alerts
- Recommendations
- Automated monitoring suggestions

---

## 🎯 KEY FEATURES

### All AI Responses Include:

1. ✅ **Root Cause Analysis**
   - Why performance issues exist
   - Contributing factors
   - Historical patterns

2. ✅ **Rectification Recommendations**
   - Specific action items
   - Implementation phases (Week 1-2, 3-4, 5-8)
   - Resource requirements

3. ✅ **Phase Tracking**
   - Timeline-based implementation
   - Milestones and checkpoints
   - Progress monitoring

4. ✅ **Fact Analysis**
   - Data quality validation
   - Assumption verification
   - Source credibility check

5. ✅ **KPI Tracking**
   - Metrics to monitor daily
   - Target values
   - Tracking mechanisms

6. ✅ **Next Steps**
   - Immediate actions (Today, Tomorrow, This Week)
   - Responsible parties
   - Success criteria

---

## 🚀 QUICK START EXAMPLES

### Example 1: Simple Question
```bash
curl -X POST http://localhost:8000/api/intelligence/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What should be our Diwali inventory strategy?"}'
```

### Example 2: Upload File
```bash
curl -X POST http://localhost:8000/api/intelligence/data/upload \
  -F "file=@sales_report.xlsx" \
  -F "data_context=Weekly sales performance"
```

### Example 3: Database Query
```bash
curl -X POST http://localhost:8000/api/intelligence/data/database \
  -H "Content-Type: application/json" \
  -d '{
    "db_type": "postgresql",
    "connection_params": {"host": "localhost", "database": "vmart", "user": "user", "password": "pass"},
    "query": "SELECT * FROM sales LIMIT 100",
    "query_context": "Recent sales data"
  }'
```

---

## 📞 SUPPORT

For issues or questions:
1. Check API health: `GET /api/intelligence/health`
2. Review error messages in response
3. Verify environment variables
4. Check database connectivity
5. Validate file formats

---

**Remember:** Every endpoint returns AI insights directly from Gemini LLM with comprehensive analysis including root causes, rectifications, phases, KPIs, and next steps!

**Powered by Gemini 2.0 Flash | V-Mart Retail Intelligence System**
