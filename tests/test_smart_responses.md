# Smart Response System - Test Cases

## Test Scenarios

### ✅ Test 1: Simple Greeting
**Input:** "Hi"
**Expected:** Natural greeting response without file analysis
**File Browsed:** None
**Should Search Files:** No

### ✅ Test 2: Greeting with File Browsed
**Input:** "Hello"
**Expected:** Natural greeting, ignores browsed file
**File Browsed:** sales_report.pdf
**Should Search Files:** No

### ✅ Test 3: File Question with File Browsed
**Input:** "Summarize this file"
**Expected:** Analyzes and summarizes sales_report.pdf
**File Browsed:** sales_report.pdf
**Should Search Files:** No (uses browsed file)

### ✅ Test 4: General Question with File Browsed
**Input:** "What is machine learning?"
**Expected:** General ML explanation, ignores browsed file
**File Browsed:** sales_report.pdf
**Should Search Files:** No

### ✅ Test 5: File Content Question
**Input:** "What are the sales numbers in this document?"
**Expected:** Extracts sales data from browsed file
**File Browsed:** sales_report.pdf
**Should Search Files:** No (uses browsed file)

### ✅ Test 6: Comparison Request
**Input:** "Compare this with my local sales data"
**Expected:** Analyzes browsed file + searches local files
**File Browsed:** week_31_sales.pdf
**Should Search Files:** Yes (for comparison)

### ✅ Test 7: Explicit File Search
**Input:** "Find my progress report"
**Expected:** Searches local files (Documents, Desktop, Downloads)
**File Browsed:** None
**Should Search Files:** Yes

### ✅ Test 8: General Question (No File)
**Input:** "What is Python?"
**Expected:** General explanation of Python
**File Browsed:** None
**Should Search Files:** No

### ✅ Test 9: Thank You Response
**Input:** "Thanks"
**Expected:** Natural acknowledgment, no file processing
**File Browsed:** sales_report.pdf
**Should Search Files:** No

### ✅ Test 10: Data Analysis on Browsed File
**Input:** "Analyze the data and give recommendations"
**Expected:** Analyzes browsed file with insights
**File Browsed:** sales_report.pdf
**Should Search Files:** No (uses browsed file)

## Expected Behavior Matrix

| Scenario | Greeting? | File Browsed? | About File? | Action |
|----------|-----------|---------------|-------------|--------|
| "Hi" | ✅ | ❌ | ❌ | Natural greeting |
| "Hi" | ✅ | ✅ | ❌ | Natural greeting (ignore file) |
| "Summarize this" | ❌ | ✅ | ✅ | Analyze browsed file |
| "What is AI?" | ❌ | ✅ | ❌ | Normal response (ignore file) |
| "Find my report" | ❌ | ❌ | ❌ | Search local files |
| "Compare with local" | ❌ | ✅ | ✅ | Analyze browsed + search local |
| "Thanks" | ✅ | ✅ | ❌ | Natural response (ignore file) |

## Keywords Reference

### Greetings (Trigger: Natural Response)
- hi, hello, hey
- good morning, good afternoon, good evening
- how are you, what's up, whats up, sup
- greetings

### Simple Responses (Trigger: Natural Response)
- thanks, thank you
- ok, okay
- yes, no, sure
- got it, understood
- bye, goodbye

### File Question Keywords (Trigger: Analyze Browsed File)
- this file, the file
- document, pdf, content, data
- analyze, summary, summarize
- what does, explain
- show me, find, search, look for
- contains, about this, in this
- from this, based on, according to

### Comparison Keywords (Trigger: Multi-Source Analysis)
- compare, difference, diff
- versus, vs
- match, similar

### Local File Search (Trigger: Search Local Files)
**Must have action word + file reference:**
- find file, search file, open file
- my file, my report, my document
- get file, read file
- show my, find my

## Testing Procedure

1. **Start with no file browsed:**
   - Test greetings ("Hi", "Hello")
   - Test general questions ("What is Python?")
   - Test file search ("Find my report")

2. **Browse a test file (e.g., sales_report.pdf):**
   - Test greeting ("Hi") - should ignore file
   - Test file question ("Summarize this") - should analyze file
   - Test general question ("What is AI?") - should ignore file
   - Test data question ("What are the insights?") - should analyze file

3. **Test comparison:**
   - Browse a file
   - Ask "Compare this with local data" - should use both sources

4. **Test acknowledgments:**
   - Say "Thanks", "Ok", "Got it" - should respond naturally

## Success Criteria

✅ Greetings return natural responses without file analysis
✅ File-specific questions analyze the browsed file
✅ General questions ignore browsed files
✅ Explicit searches trigger local file search
✅ Comparisons use multiple sources
✅ No unnecessary API calls for simple interactions
✅ Fast response times for greetings and acknowledgments

---

**Test Date**: November 10, 2025
**Tested By**: QA Team
**Status**: Ready for Testing
