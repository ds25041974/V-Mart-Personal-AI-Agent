# Gemini Integration - Quick QA Validation Checklist

**Date:** November 12, 2025  
**Version:** v2.5  
**Status:** Ready for Manual Testing

---

## Pre-Deployment Checklist

### ✅ Code Verification (COMPLETED)

- [x] **PRIORITY 0:** Simple greeting detection implemented
- [x] **PRIORITY 1:** File Browser multi-file correlation working
- [x] **PRIORITY 2:** Data Catalogue master joins functional
- [x] **PRIORITY 3:** Weather-only database restriction enforced
- [x] **Rate Limiting:** 4.5s delay, 3 retries configured
- [x] **Formatting:** Tables for numbers, paragraphs for text
- [x] **File Limits:** Max 5 files, 20KB each
- [x] **Master Limits:** 30KB per master catalogue
- [x] **Response Structure:** Insights/Recommendations/Actionables/Strategy
- [x] **Server Running:** Port 8000, PID confirmed

---

## Manual Testing Checklist (REQUIRED)

### 🧪 Test 1: Simple Greeting
**Purpose:** Verify instant response without Gemini call

- [ ] Open AI Chat interface at `http://127.0.0.1:8000/ai-chat/`
- [ ] Type: `hi`
- [ ] **Expected:** "Hi! I am V-Mart Personal AI Agent" (instant, < 1 second)
- [ ] **Verify:** No loading spinner, no API delay
- [ ] Try: `hello`, `hey` (should all work)

**Pass Criteria:** Instant greeting response for all variations

---

### 📊 Test 2: File Browser - Single File
**Purpose:** Verify file upload and formatting

**Steps:**
1. [ ] Upload single CSV file with numerical data (sales, revenue, etc.)
2. [ ] Ask: "Analyze the uploaded data and show insights"
3. [ ] Wait for response (4.5s+ delay expected)

**Expected Output Structure:**
```markdown
📈 INSIGHTS (What data reveals):
[Tables with numbers]
| Store ID | Revenue | Analysis |
|----------|---------|----------|
| ...      | ...     | ...      |

[Paragraphs for observations - clean text, no bullets]

💡 RECOMMENDATIONS:
| Priority | Action | Impact |
|----------|--------|--------|

✅ ACTIONABLES:
| Step | Action | Timeline | Owner |
|------|--------|----------|-------|

🎯 STRATEGY:
[Clean paragraphs]
```

**Pass Criteria:**
- [ ] Tables present for numerical data (pipe symbols |, separators ---)
- [ ] Paragraphs for text (no excessive bullets •••)
- [ ] All 4 sections present (Insights, Recommendations, Actionables, Strategy)
- [ ] Special characters limited to: , . ? &

---

### 📚 Test 3: File Browser - Multiple Files
**Purpose:** Verify multi-file correlation

**Steps:**
1. [ ] Upload 3-5 CSV files with related data
2. [ ] Ask: "Correlate data across all files and find patterns"
3. [ ] Wait for response

**Expected:**
- [ ] References to multiple files (File 1, File 2, etc.)
- [ ] Cross-correlation insights
- [ ] Common patterns identified
- [ ] All files mentioned in analysis

**Pass Criteria:** Response correlates data from all uploaded files

---

### 🗂️ Test 4: Data Catalogue - Master Joins
**Purpose:** Verify master data correlation

**Steps:**
1. [ ] Load 2-4 master files in Data Catalogue browsers:
   - Item Master (with Item_ID, Category, Price)
   - Store Master (with Store_ID, City, Region)
   - Competition Master (with Store_ID, Competitor)
   - Marketing Plan (with Campaign, Region, Date)
2. [ ] Ask: "Analyze master data and show correlations"
3. [ ] Wait for response

**Expected Output Includes:**
```markdown
📊 MASTER DATA JOINS PERFORMED:
| Join | Masters Connected | Join Key | Purpose |
|------|-------------------|----------|---------|
| 1    | Store ↔ Competition | Store_ID | Competitive impact |
| 2    | Item ↔ Marketing | Product_ID | Campaign effectiveness |
```

**Pass Criteria:**
- [ ] Master joins table present
- [ ] Join keys documented (Store_ID, Item_ID, Region, etc.)
- [ ] Correlation insights from multiple masters
- [ ] Clean formatting (tables + paragraphs)

---

### 🔗 Test 5: Hybrid - Catalogue + File Browser
**Purpose:** Verify hybrid correlation (masters + uploaded files)

**Steps:**
1. [ ] Load 2 master files in Data Catalogue
2. [ ] Upload 2 additional files in File Browser
3. [ ] Ask: "Correlate uploaded files with master data"
4. [ ] Wait for response

**Expected:**
- [ ] References to both masters AND uploaded files
- [ ] Cross-source correlation
- [ ] Insights showing: "Based on Item Master and uploaded sales data..."
- [ ] Both data sources used in analysis

**Pass Criteria:** Response uses both master catalogues and uploaded files

---

### 🌤️ Test 6: Weather-Only Restriction
**Purpose:** Verify database restriction for general queries

**Steps:**
1. [ ] Clear all uploaded files and masters
2. [ ] Ask: "What's the weather in Delhi store?"
3. [ ] Wait for response

**Expected:**
- [ ] Weather data provided (temperature, forecast, conditions)
- [ ] **NO** sales data mentioned
- [ ] **NO** inventory data mentioned
- [ ] **NO** other business metrics

**Negative Test:**
- [ ] Ask: "What are the sales for Delhi store?" (without files)
- [ ] **Expected:** "I can only provide weather information" or similar restriction message

**Pass Criteria:** Only weather data provided for general queries

---

### ⏱️ Test 7: Rate Limiting
**Purpose:** Verify rate limiting prevents errors

**Steps:**
1. [ ] Send 5 requests quickly (upload file, ask question, repeat)
2. [ ] Observe delays between responses
3. [ ] Check for any error messages

**Expected Behavior:**
- [ ] Minimum 4.5 seconds between requests
- [ ] No "rate limit exceeded" errors
- [ ] Loading indicators show processing
- [ ] All requests succeed

**Pass Criteria:** No rate limit errors, consistent 4.5s+ delays

---

### 📐 Test 8: Formatting Consistency
**Purpose:** Verify formatting rules applied consistently

**Test Cases:**

**A) Numerical Data:**
- [ ] Upload file with numbers (sales, revenue, quantities)
- [ ] **Expected:** Tables with columns and rows
- [ ] **Verify:** Pipe characters |, separator lines ---

**B) Text Insights:**
- [ ] Upload file with qualitative data (descriptions, observations)
- [ ] **Expected:** Flowing paragraphs
- [ ] **Verify:** No excessive bullets (•), no special markdown (* # >)

**C) Mixed Data:**
- [ ] Upload file with both numbers and text
- [ ] **Expected:** Numbers in tables, text in paragraphs
- [ ] **Verify:** Clear separation between sections

**Pass Criteria:** Consistent formatting across all response types

---

### 🚫 Test 9: File Upload Limits
**Purpose:** Verify 5-file maximum enforced

**Steps:**
1. [ ] Attempt to upload 6 files
2. [ ] Observe behavior

**Expected:**
- [ ] Only first 5 files processed, OR
- [ ] Error message: "Maximum 5 files allowed", OR
- [ ] Frontend prevents 6th file upload

**Pass Criteria:** System enforces 5-file limit

---

### 🔐 Test 10: Authentication
**Purpose:** Verify endpoints require login

**Steps:**
1. [ ] Open incognito/private browser window
2. [ ] Try to access: `http://127.0.0.1:8000/ask`
3. [ ] Observe behavior

**Expected:**
- [ ] Redirect to login page, OR
- [ ] Error: "Unauthorized" / "Login required"

**Pass Criteria:** Endpoints protected by authentication

---

## Post-Testing Actions

### If All Tests Pass ✅
- [ ] Mark as "Production Ready"
- [ ] Deploy to production environment
- [ ] Monitor Gemini API usage (stay under 1500 req/day)
- [ ] Collect user feedback on formatting

### If Any Test Fails ❌
- [ ] Document failure details
- [ ] Check code at relevant line numbers (see QA report)
- [ ] Fix issue and re-test
- [ ] Update QA report with findings

---

## Quick Reference

**Server:** `http://127.0.0.1:8000`  
**AI Chat:** `http://127.0.0.1:8000/ai-chat/`  
**Endpoint:** POST `/ask`  
**Status:** Running on port 8000

**Code Locations:**
- Greeting: `app.py` lines 427-442
- File Browser: `app.py` lines 444-606
- Data Catalogue: `app.py` lines 608-896
- Weather Only: `app.py` lines 1028-1053
- Rate Limiting: `gemini_agent.py` lines 33-271

**Key Metrics:**
- Rate Limit: 15 req/min (using 13 req/min = 4.5s delay)
- File Limit: 5 files max, 20KB each
- Master Limit: 30KB per catalogue
- Retries: 3 attempts with exponential backoff (2s, 4s, 8s)

---

## Notes

- **Authentication Required:** Tests must be run as logged-in user
- **Gemini API Key:** Must be configured in environment
- **Rate Limiting:** Tests will be slow (4.5s+ between requests)
- **Formatting:** Look for tables (|) and clean paragraphs (no excessive •)

---

**Status:** ⏳ Awaiting Manual Testing  
**Next Step:** Perform manual tests above and mark completion

---

**Tester Signature:** _________________  
**Date Completed:** _________________  
**Overall Result:** [ ] PASS  [ ] FAIL
