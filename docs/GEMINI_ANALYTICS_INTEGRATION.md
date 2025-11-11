# Gemini AI Analytics Integration

## Overview

The V-Mart Personal AI Agent now automatically uses **live analytics data** when answering business questions. Gemini AI has access to real-time store performance, sales trends, inventory levels, weather impact, and competition analysis.

## How It Works

### Automatic Context Detection

When you ask a business-related question, the system:

1. **Detects Analytics Keywords** in your question:
   - Sales, revenue, growth, performance
   - Inventory, stock, reorder, shortage
   - Weather, seasonal, climate
   - Competition, competitors, market share
   - Trends, forecast, demand
   - Recommendations, insights, advice

2. **Identifies the Store** you're asking about:
   - By store ID: "What are sales for VM_DL_001?"
   - By city name: "How is Delhi store performing?"
   - By store name: "Show me Bangalore metrics"
   - Default: Delhi store (VM_DL_001) if not specified

3. **Fetches Relevant Analytics**:
   - Sales trends (last 30 days by default)
   - Inventory recommendations
   - Weather impact analysis
   - Competition analysis
   - Business insights with priorities

4. **Provides Data-Driven Responses**:
   - Gemini receives the analytics data as context
   - Responses cite specific numbers and trends
   - Recommendations based on actual performance metrics
   - Insights backed by multi-dimensional analysis

## Example Questions

### Sales Performance
```
Q: "How are sales performing at our Delhi store?"

Gemini receives:
- Total sales: ₹4,299,096.87
- Sales growth: +15.84%
- Peak period: Sunday Afternoon
- Trending categories: Kids Wear (+27.9%), Women's Wear (+32.4%)

Response: Data-driven analysis with specific numbers and recommendations
```

### Inventory Management
```
Q: "What inventory should we reorder for Bangalore?"

Gemini receives:
- 6 categories analyzed
- Critical reorder items
- Seasonal factors
- Stockout risk levels

Response: Prioritized reorder recommendations with quantities
```

### Weather Impact
```
Q: "How does weather affect our Mumbai store sales?"

Gemini receives:
- Weather correlation data
- Sales variance by condition
- Affected categories
- Temperature impact

Response: Weather-based sales strategies and category planning
```

### Competition Analysis
```
Q: "What's our competitive position in Chennai?"

Gemini receives:
- Competitor count and proximity
- Estimated market share
- Sales impact percentage
- Competitive advantages and threats

Response: Strategic recommendations for competitive positioning
```

### Business Insights
```
Q: "What should I focus on this week?"

Gemini receives:
- Critical insights (2-day expiry)
- High priority recommendations
- Action items by category
- Confidence scores

Response: Prioritized action plan with rationale
```

### Network-Wide Queries
```
Q: "How are all stores performing overall?"

Gemini receives:
- Network summary across 11 stores
- Total revenue: ₹40.5M
- Average growth rate
- Store-by-store comparison

Response: Network-level insights and benchmarking
```

## Analytics Data Included

### Store Information
- Store ID, name, location
- City and state
- Operating hours

### Sales Analytics (Last 30 Days)
- Total sales and growth percentage
- Average daily sales
- Peak sales periods (day/time)
- Trending categories with growth rates
- Underperforming categories

### Inventory Status
- Categories analyzed
- Critical reorder items
- High priority reorders
- Overstock items
- Top recommendations with quantities

### Weather Impact
- Primary weather condition
- Temperature range
- Sales variance by weather
- Affected product categories
- Weather-based recommendations

### Competition Analysis
- Number of nearby competitors
- Nearest competitor distance
- Estimated market share
- Sales impact percentage
- Competitive advantages
- Competitive threats
- Strategic recommendations

### Business Insights
- Critical insights count
- High priority insights
- Recommended actions
- Priority levels (Critical/High/Medium/Low)
- Confidence scores
- Expiration dates

## Technical Implementation

### Architecture

```
User Question
    ↓
Chat Endpoint (/ask)
    ↓
Keyword Detection (analytics-related?)
    ↓
AnalyticsContextProvider
    ↓
Store Detection (from question)
    ↓
Analytics Engine (fetch data)
    ↓
Context Formatting (for AI)
    ↓
GeminiAgent (with analytics context)
    ↓
Data-Driven Response
```

### Components

1. **AnalyticsContextProvider** (`src/analytics/context_provider.py`)
   - Analyzes user questions
   - Detects relevant analytics categories
   - Fetches data from AnalyticsEngine
   - Formats context for Gemini AI

2. **Enhanced GeminiAgent** (`src/agent/gemini_agent.py`)
   - New parameter: `analytics_context`
   - Injects analytics data into system prompt
   - Instructs AI to cite specific data points
   - Ensures data-driven recommendations

3. **Updated Chat Endpoint** (`src/web/app.py`)
   - Detects analytics-related questions
   - Calls AnalyticsContextProvider
   - Passes context to GeminiAgent
   - Adds analytics source attribution

## Benefits

### 1. Data-Driven Insights
- Every recommendation backed by actual metrics
- No generic advice - specific to your store's performance
- Real numbers cited in responses

### 2. Contextual Awareness
- Understands your store's current situation
- Considers multiple factors (sales, weather, competition)
- Provides holistic recommendations

### 3. Time-Saving
- No need to check multiple dashboards
- Get insights through natural conversation
- Quick access to complex analytics

### 4. Actionable Recommendations
- Prioritized based on urgency
- Specific quantities for reorders
- Clear next steps with rationale

### 5. Multi-Dimensional Analysis
- Sales trends + weather impact + competition
- Inventory optimization with seasonal factors
- Comprehensive business intelligence

## Usage Tips

### Be Specific
```
❌ "How's business?"
✅ "How are sales at our Delhi store this month?"
```

### Ask About Specific Stores
```
❌ "Show me sales"
✅ "What are the sales trends for Bangalore store?"
```

### Request Specific Insights
```
❌ "Give me some tips"
✅ "What inventory should I reorder based on current trends?"
```

### Combine Multiple Factors
```
"How does weather affect our sales in Mumbai, and what should we stock for the monsoon season?"
```

### Ask for Comparisons
```
"Compare sales performance across all stores and identify the top performers"
```

## Sample Conversations

### Conversation 1: Morning Briefing
```
You: "Good morning! What should I focus on today for Delhi store?"

Gemini (with analytics): "Good morning! Based on Delhi store's current analytics:

📊 SALES PERFORMANCE (Last 30 days):
- Total Revenue: ₹4,299,096.87 (↑15.84% growth)
- Peak Period: Sunday Afternoon
- Strong Categories: Kids Wear (+27.9%), Women's Wear (+32.4%)

🔴 CRITICAL PRIORITIES TODAY:

1. INVENTORY REORDERS (High Priority):
   - Kids Wear: Reorder 250 units (stockout risk: 45%)
   - Women's Wear: Reorder 180 units (stockout risk: 38%)
   
2. CAPITALIZE ON TRENDING CATEGORIES:
   - Promote Kids Wear and Women's Wear during peak hours
   - Ensure stock availability for weekend rush
   
3. WEATHER CONSIDERATION:
   - Partly Cloudy conditions expected
   - Historical data shows 8% boost in indoor shopping
   
Recommended Actions:
- Process urgent reorders by noon
- Brief sales team on trending categories
- Plan Sunday afternoon staffing accordingly"
```

### Conversation 2: Inventory Planning
```
You: "What's our inventory situation in Bangalore?"

Gemini (with analytics): "Here's the current inventory status for Bangalore store:

📦 INVENTORY ANALYSIS:

Categories Analyzed: 6
- Critical Reorders: 2 items
- High Priority: 1 item
- Overstock: 1 category

🔴 CRITICAL REORDERS (Immediate Action):
1. Men's Wear: Reorder 300 units
   - Current stock: 45 days supply left
   - Seasonal demand increasing
   - Expected stockout risk: 52%

2. Accessories: Reorder 150 units
   - Days of supply: 3 days
   - High turnover rate
   
⚠️ HIGH PRIORITY:
1. Footwear: Reorder 120 units (7 days supply)

💰 OVERSTOCK ALERT:
- Winter Wear: 95 days of excess stock (₹45,000 tied up)
- Recommendation: Clearance sale or transfer to northern stores

Next Steps:
1. Place critical orders today
2. Plan clearance strategy for winter wear
3. Monitor high-turnover categories daily"
```

### Conversation 3: Competition Strategy
```
You: "How are we positioned against competitors in Chennai?"

Gemini (with analytics): "Here's your competitive analysis for Chennai store:

🎯 COMPETITIVE POSITION:

Market Overview:
- Nearby Competitors: 4 stores
- Nearest Competitor: 2.3 km away
- Your Market Share: ~35% (estimated)
- Sales Impact: -8% due to competition

✅ YOUR COMPETITIVE ADVANTAGES:
1. Strategic location near residential area
2. Strong customer loyalty in Women's Wear segment
3. Better pricing on Kids Wear category

⚠️ COMPETITIVE THREATS:
1. New competitor opened 2.3 km away (3 months ago)
2. Aggressive pricing on Men's Wear
3. Extended operating hours

📈 RECOMMENDED STRATEGIES:

1. LEVERAGE STRENGTHS:
   - Promote Women's Wear and Kids Wear heavily
   - Launch loyalty program to retain customers
   - Highlight location convenience

2. COUNTER THREATS:
   - Review Men's Wear pricing strategy
   - Consider extended hours on weekends
   - Improve in-store experience

3. MARKET EXPANSION:
   - Target untapped customer segments
   - Community engagement programs
   - Partner with local businesses

Expected Outcome: Market share increase of 5-8% in 3 months"
```

## API Integration

For programmatic access, you can still use the REST API endpoints:

```bash
# Get sales trends
GET /analytics/sales-trends/VM_DL_001?days=30

# Get inventory recommendations
GET /analytics/inventory-recommendations/VM_DL_001

# Get business insights
GET /analytics/insights/VM_DL_001?priority=critical

# Get complete dashboard
GET /analytics/dashboard/VM_DL_001?days=30
```

## Future Enhancements

### Planned Features
1. **Voice-to-Analytics**: Ask questions via voice
2. **Automated Alerts**: Proactive insights via email/SMS
3. **Predictive Queries**: AI suggests what to ask based on anomalies
4. **Custom Dashboards**: Personalized analytics views
5. **Historical Comparisons**: Year-over-year trends
6. **Sentiment Analysis**: Customer feedback integration

### Advanced Analytics
- Machine learning forecasts
- Customer segmentation insights
- Product affinity analysis
- Pricing optimization recommendations

## Troubleshooting

### Analytics Not Appearing
- Check if question contains analytics keywords
- Specify store ID or city name
- Use phrases like "sales", "inventory", "performance"

### Wrong Store Data
- Explicitly mention store ID: "VM_DL_001"
- Use city name: "Delhi store"
- Default is Delhi if not specified

### Need More Details
- Ask follow-up questions
- Request specific metrics: "Show me exact numbers"
- Specify time period: "Last 60 days" instead of default 30

## Support

For issues or questions:
- Check the main analytics guide: `docs/ANALYTICS_GUIDE.md`
- Review API documentation
- Contact: DSR (Developer)

---

**Powered by Gemini AI with Live V-Mart Analytics**
