# Gemini LLM Tight Integration Strategy
## V-Mart Personal AI Agent - Data Analysis Architecture

**Created:** 12 November 2025  
**Purpose:** Define strict data source hierarchy and Gemini integration for accurate, curated responses

---

## 🎯 Core Principles

### 1. **Strict Data Source Priority**
The AI MUST follow this hierarchy without exception:

```
PRIORITY 0: Greeting Detection (Simple Response Only)
    ↓
PRIORITY 1: File Browser Uploads (PDF/CSV/Excel/Images)
    ↓
PRIORITY 2: Data Catalogue Configuration (4 Master Files)
    ↓
PRIORITY 3: Live Weather Data ONLY
    ↓
PRIORITY 4: NO OTHER DATABASE OR STORED DATA
```

### 2. **No Cross-Contamination**
- When analyzing **uploaded files** → ONLY use file data
- When using **Data Catalogue** → ONLY use catalogue data (with master joins)
- For **general questions** → ONLY use live weather data
- **NEVER** mix stored database data with file-based questions

### 3. **Tight Gemini Integration**
- ALL analysis goes through Gemini LLM
- Gemini receives explicit instructions about data sources
- Gemini performs correlation, analysis, and curation
- Response must include: Insights + Recommendations + Actionables + Strategy

---

## 📋 Implementation Requirements

### **PRIORITY 0: Greeting Detection**

**Trigger:** `hi`, `hello`, `hey`, `good morning`, etc.

**Response:**
```
Hi! I am V-Mart Personal AI Agent
```

**Logic:**
- Detect exact greeting match
- Return simple string immediately
- NO Gemini call
- NO file reading
- NO database queries
- NO weather data

**Implementation:**
```python
SIMPLE_GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon", 
                     "good evening", "greetings", "namaste"]

if prompt_lower.strip() in SIMPLE_GREETINGS:
    return jsonify({"response": "Hi! I am V-Mart Personal AI Agent"})
```

---

### **PRIORITY 1: File Browser Uploads**

**When:** User uploads files via File Browser tab (PDF/CSV/Excel/Images)

**Data Sources:**
- ✅ Uploaded file content ONLY
- ✅ Multiple file correlation (if 2+ files uploaded)
- ❌ NO database data
- ❌ NO stored V-Mart data
- ❌ NO weather data (unless file contains weather info)

**Analysis Requirements:**
1. **Read:** Extract content from all uploaded files
2. **Correlate:** If multiple files, find relationships (join keys, matching IDs, etc.)
3. **Analyze:** Deep dive into patterns, trends, anomalies
4. **Curate:** Provide:
   - **Insights:** What the data reveals
   - **Recommendations:** What actions to take
   - **Actionables:** Specific steps with timelines
   - **Strategy:** Long-term approach based on findings

**Gemini Prompt Template:**
```
🚨 CRITICAL: Analyze ONLY the uploaded file(s) below

FILES: [file names and types]

FILE CONTENT:
[Full file content with markers]

USER QUESTION: [user's prompt]

REQUIREMENTS:
1. Correlate data across all files (find matching IDs, keys, relationships)
2. Analyze patterns, trends, anomalies
3. Provide:
   - Insights (what data reveals)
   - Recommendations (what to do)
   - Actionables (specific steps with timelines)
   - Strategy (long-term approach)
4. Cite exact file names and data points
5. DO NOT use external knowledge or assumptions

BEGIN ANALYSIS:
```

**File Correlation Examples:**
- **Sales.csv + Inventory.csv:** Join on Product_ID to find stock issues
- **Store_Performance.xlsx + Competition.pdf:** Match store locations to competitor proximity
- **Marketing_Plan.csv + Sales_Data.xlsx:** Correlate campaign dates with sales spikes

**Implementation Limits:**
- Max 5 files per upload (prevent rate limits)
- 20KB per file content (truncate with notice if larger)
- Show file list, types, sizes before analysis

---

### **PRIORITY 2: Data Catalogue Configuration**

**When:** User has uploaded master data via Data Catalogue tab

**Data Sources:**
- ✅ Item Master (product details, pricing, categories)
- ✅ Store Master (store locations, size, revenue)
- ✅ Competition Master (competitor stores, pricing)
- ✅ Marketing Plan (campaigns, budgets, timelines)
- ✅ Master data JOINS and correlations
- ❌ NO other database data
- ❌ NO general stored data

**Master Data Joins:**
```
Item Master + Store Master = Store-wise product performance
Store Master + Competition Master = Competitive landscape by location
Marketing Plan + Store Master = Campaign effectiveness by store
Item Master + Marketing Plan = Product-level campaign ROI
```

**Analysis Requirements:**
1. **Read:** All available master files
2. **Join:** Correlate across masters using:
   - Store_ID (Store Master ↔ Competition Master)
   - Item_ID (Item Master ↔ Marketing Plan)
   - Region/City (Store Master ↔ Competition Master)
   - Date ranges (Marketing Plan ↔ performance data)
3. **Deep Dive:** Cross-reference patterns:
   - Store revenue vs competition intensity
   - Marketing ROI by store/region
   - Item performance across stores
   - Competitive pricing vs our pricing
4. **Curate:** Provide comprehensive insights with master data references

**Gemini Prompt Template:**
```
🚨 V-MART DATA CATALOGUE CORRELATION ANALYSIS

MASTER DATA AVAILABLE:
- Item Master: [record count, columns]
- Store Master: [record count, columns]
- Competition Master: [record count, columns]
- Marketing Plan: [record count, columns]

MASTER DATA CONTENT:
[Full catalogue data with clear sections]

USER QUESTION: [user's prompt]

CORRELATION REQUIREMENTS:
1. Join masters on:
   - Store_ID (Store ↔ Competition)
   - Item_ID (Item ↔ Marketing)
   - Region/City (geographical correlation)
   - Dates (temporal analysis)
2. Analyze cross-master patterns
3. Provide:
   - Insights (correlated findings)
   - Recommendations (based on joins)
   - Actionables (specific to stores/items/regions)
   - Strategy (leveraging master data relationships)
4. Cite exact masters and record IDs

BEGIN CORRELATION ANALYSIS:
```

**Join Logic Examples:**
```python
# Example: Store performance vs competition
Store_Master[Store_ID] ← JOIN → Competition_Master[Nearby_Store_ID]
Analysis: Stores with 3+ competitors within 2km have 15% lower footfall

# Example: Marketing effectiveness
Marketing_Plan[Campaign_ID] ← JOIN → Item_Master[Promoted_Item_ID]
Analysis: Electronic items show 23% higher ROI than apparel campaigns
```

---

### **PRIORITY 3: General Chat - Weather ONLY**

**When:** No files uploaded, no catalogue data, general question

**Data Sources:**
- ✅ Live weather data ONLY (via OpenWeatherMap API)
- ❌ NO stored database data
- ❌ NO historical V-Mart data
- ❌ NO file references

**Logic:**
```python
if not file_context and not catalogue_context:
    # Check if question is weather-related
    weather_keywords = ["weather", "temperature", "rain", "forecast", "climate"]
    
    if any(kw in prompt_lower for kw in weather_keywords):
        # Fetch live weather data
        weather_data = get_live_weather(city)
        
        # Provide weather response
        response = gemini_agent.get_response(prompt, weather_context=weather_data)
    else:
        # Non-weather general question - no database
        response = "I can help with weather information or analyze uploaded files. 
                    Please upload files or ask about weather."
```

**Restricted:**
- ❌ Cannot answer "What are V-Mart's top stores?" without uploaded data
- ❌ Cannot answer "Show me sales trends" without files/catalogue
- ❌ Cannot answer "Who are our competitors?" without competition master

**Allowed:**
- ✅ "What's the weather in Mumbai?"
- ✅ "Will it rain tomorrow in Delhi?"
- ✅ "Temperature forecast for Bangalore?"

---

## 🔧 Technical Implementation

### **File Correlation Logic**

```python
def correlate_uploaded_files(file_context):
    """
    Correlate multiple uploaded files by finding common keys/IDs
    """
    correlations = []
    
    # Extract potential join keys from each file
    for i, file1 in enumerate(file_context):
        for j, file2 in enumerate(file_context):
            if i >= j:
                continue
            
            # Find common columns/fields
            common_fields = find_common_fields(file1, file2)
            
            if common_fields:
                correlations.append({
                    'file1': file1['filename'],
                    'file2': file2['filename'],
                    'join_keys': common_fields
                })
    
    return correlations
```

### **Master Data Join Logic**

```python
def join_catalogue_masters(catalogue_data):
    """
    Perform intelligent joins across master data
    """
    joins = []
    
    # Store ↔ Competition join
    if 'storeMaster' in catalogue_data and 'competitionMaster' in catalogue_data:
        joins.append({
            'type': 'Store-Competition',
            'key': 'Store_ID / Region',
            'analysis': 'Competitive landscape by store location'
        })
    
    # Item ↔ Marketing join
    if 'itemMaster' in catalogue_data and 'marketingPlan' in catalogue_data:
        joins.append({
            'type': 'Item-Marketing',
            'key': 'Item_ID / Product_Category',
            'analysis': 'Campaign effectiveness by product'
        })
    
    return joins
```

### **Response Enhancement**

```python
def enhance_gemini_response(response, data_source):
    """
    Add structured insights, recommendations, actionables, strategy
    """
    enhanced = {
        'data_source': data_source,  # 'File Browser' | 'Data Catalogue' | 'Weather'
        'response': response,
        'insights': extract_insights(response),
        'recommendations': extract_recommendations(response),
        'actionables': extract_actionables(response),
        'strategy': extract_strategy(response),
        'data_references': extract_data_refs(response)
    }
    
    return enhanced
```

---

## ⚡ Performance Optimization

### **Gemini Response Timing**

1. **Reduce Prompt Size:**
   - File content: Max 20KB per file
   - Catalogue data: Max 30KB per master
   - Truncate with clear markers

2. **Parallel Processing:**
   - Maintain Flask's parallel request handling
   - Rate limiting: 4.5s delay (13 req/min vs 15/min limit)
   - 3 retry attempts with exponential backoff (2s, 4s, 8s)

3. **Smart Context:**
   - Only include relevant sections
   - Remove redundant instructions
   - Use clear markdown formatting

4. **Streaming (Future):**
   - Consider SSE for long responses
   - Show progress indicators during analysis

---

## ✅ Validation Checklist

### **Before Deployment:**

- [ ] Greeting detection returns simple response (no Gemini call)
- [ ] File Browser uploads ONLY use file data (no database)
- [ ] Multi-file uploads correlate across files
- [ ] Data Catalogue performs master joins correctly
- [ ] General chat ONLY uses weather data (no stored data)
- [ ] Rate limiting prevents API errors
- [ ] File count limit (5 max) enforced
- [ ] Content truncation (20KB) working
- [ ] Error messages are user-friendly
- [ ] Response includes: Insights, Recommendations, Actionables, Strategy

### **Test Scenarios:**

1. **Greeting:** "Hi" → "Hi! I am V-Mart Personal AI Agent"
2. **Single File:** Upload sales.csv → Analyze only CSV data
3. **Multi File:** Upload sales.csv + inventory.xlsx → Correlate on Product_ID
4. **Data Catalogue:** Upload all 4 masters → Perform joins and analysis
5. **Weather:** "Weather in Mumbai?" → Fetch live weather
6. **Invalid:** "What are top stores?" (no files) → Request file upload
7. **Rate Limit:** 7 files → Show "max 5 files" error

---

## 🚨 Alert System

### **Before Changing Logic:**

```python
def validate_logic_change(change_description):
    """
    Alert before modifying core logic
    """
    print(f"""
    ⚠️  LOGIC CHANGE ALERT ⚠️
    
    Proposed Change: {change_description}
    
    Review Requirements:
    1. Does this maintain data source priority?
    2. Does this preserve file-only analysis?
    3. Does this keep database usage restricted to weather?
    4. Does this enhance Gemini integration?
    5. Does this improve response quality?
    
    Proceed? (y/n)
    """)
```

---

## 📊 Future Enhancements

1. **Advanced Correlation:**
   - Machine learning for automatic join key detection
   - Fuzzy matching for similar but not exact fields
   - Time-series correlation across temporal data

2. **Enhanced Curation:**
   - Auto-generate executive summaries
   - Visual charts/graphs from data
   - Export analysis to PDF/Excel

3. **Performance:**
   - Implement caching for repeat queries
   - Response streaming for real-time updates
   - Batch processing for large datasets

4. **Intelligence:**
   - Predictive analytics from master data
   - Anomaly detection across stores
   - Automated A/B test recommendations

---

## 📝 Summary

This strategy ensures:
- ✅ **Tight Gemini Integration:** All analysis through Gemini LLM
- ✅ **Data Source Purity:** No mixing of file data with stored data
- ✅ **Intelligent Correlation:** Multi-file and master data joins
- ✅ **Actionable Insights:** Always provide recommendations and strategy
- ✅ **Fast Response:** Optimized prompts and rate limiting
- ✅ **User-Friendly:** Clear messages and guidance

**Implementation Date:** 12 November 2025  
**Status:** Ready for development  
**Next Steps:** Implement changes in app.py with validation alerts
