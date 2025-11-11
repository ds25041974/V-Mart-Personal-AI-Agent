# 🎯 Quick Reference: Ask Gemini About Your Business

## What Changed?

Gemini AI now **automatically uses live analytics data** when you ask business questions!

## How to Use

Just ask naturally - **no special commands needed**:

### ✅ Sales Questions
```
"How are sales at Delhi store?"
"Show me revenue trends"
"Which categories are performing well?"
"What was our growth last month?"
```

### ✅ Inventory Questions
```
"What should I reorder?"
"Show me inventory status"
"Any stockout risks?"
"Which items are overstocked?"
```

### ✅ Weather Impact
```
"How does weather affect sales?"
"What sells well in rain?"
"Weather impact on Delhi store?"
```

### ✅ Competition Analysis
```
"What's our market position?"
"How many competitors nearby?"
"Are we competitive in Bangalore?"
```

### ✅ Business Insights
```
"What should I focus on today?"
"Give me a business overview"
"Any urgent recommendations?"
"Show me critical insights"
```

## What Gemini Knows

For **every question**, Gemini automatically receives:

📊 **Sales Data (Last 30 Days)**
- Total revenue
- Growth percentage
- Peak sales periods
- Trending categories

📦 **Inventory Status**
- Critical reorders
- Stockout risks
- Overstock items
- Recommendations

🌤️ **Weather Impact**
- Sales correlation
- Affected categories
- Weather-based tips

🏪 **Competition**
- Competitor count
- Market share
- Competitive position

💡 **Business Insights**
- Priority recommendations
- Action items
- Confidence scores

## Example Conversation

**You**: "How's our Delhi store doing?"

**Gemini** (with live data):
```
Based on Delhi store's current analytics:

📊 SALES PERFORMANCE (Last 30 days):
- Revenue: ₹3.07M (↑16.09% growth) ✅
- Peak Period: Saturday Afternoon
- Top Categories: Kids Wear (+27%), Women's Wear (+32%)

📦 INVENTORY ALERTS:
- Critical: Kids Wear needs reorder (250 units)
- Overstock: Winter Wear (45 days excess)

💡 RECOMMENDATIONS:
1. Stock up Kids Wear before weekend
2. Plan clearance for winter items
3. Increase staff Saturday afternoons

Overall: Strong performance with good growth! 
Focus on capitalizing on trending categories.
```

## Store Detection

Gemini automatically detects which store you're asking about:

✅ **By Store ID**: "VM_DL_001", "VM_BLR_002"
✅ **By City**: "Delhi store", "Bangalore", "Mumbai"  
✅ **By Name**: "V-Mart Delhi Central"
✅ **Default**: Delhi store if not specified

## Network Queries

Ask about all stores:

```
"How are all stores performing?"
"Compare store performance"
"Network-wide sales trends"
"Best performing locations"
```

## What Makes It Smart?

### 🎯 Context-Aware
- Asks about sales? Gets sales data
- Asks about inventory? Gets inventory data
- Asks general question? Gets comprehensive overview

### 📈 Data-Driven
- Every answer backed by real metrics
- Specific numbers cited (not generic advice)
- Current data (30-day rolling window)

### 🔄 Always Updated
- Live analytics every time you ask
- No stale data
- Real-time insights

## Access Points

### 💬 Chat Interface
http://localhost:8000
- Just log in and ask questions

### 📊 Analytics Dashboard
http://localhost:8000/analytics/dashboard-ui/VM_DL_001
- Visual analytics (if you prefer charts)

### 🔌 API Endpoints
```bash
# Sales trends
GET /analytics/sales-trends/VM_DL_001

# Inventory recommendations  
GET /analytics/inventory-recommendations/VM_DL_001

# Business insights
GET /analytics/insights/VM_DL_001

# Network summary
GET /analytics/all-stores/summary
```

## Tips for Best Results

### ✅ Do:
- Ask specific questions: "Delhi store sales?"
- Use natural language: "How are we doing?"
- Combine topics: "Sales and inventory for Mumbai?"

### ❌ Don't:
- Use technical jargon: No need for "execute query"
- Specify parameters: No need for "last 30 days" (automatic)
- Request raw data: Ask for insights instead

## Quick Test

Try asking Gemini right now:

```
"What should I focus on today for VM_DL_001?"
```

You should get:
- Current sales performance
- Urgent inventory actions
- Priority recommendations
- All backed by live data! ✅

## Questions?

Gemini can now answer ANY business question using:
- 11 V-Mart store locations
- Sales analytics
- Inventory data
- Weather correlation
- Competition intelligence
- AI-powered insights

Just ask naturally! 🚀

---

**Status**: ✅ Live and Working  
**Data**: ✅ Real-time (30-day rolling)  
**Stores**: ✅ All 11 locations  
**AI**: ✅ Gemini 2.0 Flash with Analytics
