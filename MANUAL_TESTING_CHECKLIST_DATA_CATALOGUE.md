# Data Catalogue Configuration - Manual Testing Checklist

**Tester:** ________________  
**Date:** ________________  
**Browser:** ________________  
**Server Status:** ☐ Running on http://localhost:8000

---

## Pre-Test Setup

- [ ] Server is running (check: `lsof -ti:8000`)
- [ ] Browser cache cleared (Cmd+Shift+Delete)
- [ ] DevTools ready (F12 or Cmd+Option+I)
- [ ] Sample CSV files located in `test_data/` folder
- [ ] This checklist printed or visible on second screen

---

## Part 1: UI Validation (5 minutes)

### Tab Navigation
- [ ] Open http://localhost:8000
- [ ] Click "📚 Data Catalogue Configuration" tab
- [ ] Tab opens without errors
- [ ] 4 master data sections visible:
  - [ ] 📦 Item Master
  - [ ] 🏪 Store Master
  - [ ] 🎯 Competition Master
  - [ ] 📢 Marketing Plan

### Visual Inspection
- [ ] Each section has "Browse..." button
- [ ] Each section has "Remove" button
- [ ] Layout is clean and aligned
- [ ] No JavaScript errors in console (check DevTools Console tab)

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

---

## Part 2: File Upload Testing (10 minutes)

### Item Master Upload
- [ ] Click "Browse..." under Item Master
- [ ] Select `test_data/item_master_sample.csv`
- [ ] File name appears: "item_master_sample.csv"
- [ ] Last Updated timestamp shows
- [ ] Records count shows: "10"
- [ ] No errors in console

### Store Master Upload
- [ ] Click "Browse..." under Store Master
- [ ] Select `test_data/store_master_sample.csv`
- [ ] File info displays correctly
- [ ] Records count: "10"
- [ ] No errors in console

### Competition Master Upload
- [ ] Click "Browse..." under Competition Master
- [ ] Select `test_data/competition_master_sample.csv`
- [ ] File info displays correctly
- [ ] Records count: "10"
- [ ] No errors in console

### Marketing Plan Upload
- [ ] Click "Browse..." under Marketing Plan
- [ ] Select `test_data/marketing_plan_sample.csv`
- [ ] File info displays correctly
- [ ] Records count: "10"
- [ ] No errors in console

**Result:** ☐ PASS | ☐ FAIL  
**Upload Speed:** Item(___ms) Store(___ms) Comp(___ms) Mkt(___ms)  
**Notes:** _______________________________________________

---

## Part 3: File Validation Testing (5 minutes)

### Test Invalid File Upload
- [ ] Try uploading `store_master_sample.csv` to Item Master browser
- [ ] Validation error appears
- [ ] Error message is user-friendly
- [ ] Original Item Master data unchanged

### Test Correct File After Error
- [ ] Re-upload correct `item_master_sample.csv` to Item Master
- [ ] Upload succeeds
- [ ] Data displays correctly

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

---

## Part 4: IndexedDB Verification (5 minutes)

### Access IndexedDB
- [ ] Open DevTools (F12)
- [ ] Navigate to: Application → IndexedDB → VMartCatalogueDB
- [ ] Database "VMartCatalogueDB" exists
- [ ] Version is 1

### Check Object Stores
- [ ] Object store "itemMaster" exists
  - [ ] Contains 10 records
  - [ ] Sample record has: ItemCode, ItemName, Category fields
- [ ] Object store "storeMaster" exists
  - [ ] Contains 10 records
  - [ ] Sample record has: StoreCode, StoreName, City fields
- [ ] Object store "competitionMaster" exists
  - [ ] Contains 10 records
  - [ ] Sample record has: CompetitorID, CompetitorName fields
- [ ] Object store "marketingPlan" exists
  - [ ] Contains 10 records
  - [ ] Sample record has: CampaignID, CampaignName fields
- [ ] Object store "metadata" exists
  - [ ] Contains 4 entries (one per master)

**Result:** ☐ PASS | ☐ FAIL  
**Total Records:** itemMaster(___) storeMaster(___) competitionMaster(___) marketingPlan(___)  
**Notes:** _______________________________________________

---

## Part 5: Gemini Integration Testing (15 minutes)

### Test 1: Simple Item Query
- [ ] In chat, type: "Show me all items in the catalogue"
- [ ] Send message
- [ ] Response received (time: _____ seconds)
- [ ] Response includes "Data Catalogue Correlation Analysis" header
- [ ] Response lists items from Item Master
- [ ] Response shows exact item names and codes

**Result:** ☐ PASS | ☐ FAIL  
**Response Time:** _____ seconds  
**Notes:** _______________________________________________

### Test 2: Simple Store Query
- [ ] Type: "List all stores and their monthly revenue"
- [ ] Send message
- [ ] Response includes store data
- [ ] Revenue figures match CSV file
- [ ] All 10 stores mentioned

**Result:** ☐ PASS | ☐ FAIL  
**Response Time:** _____ seconds  
**Notes:** _______________________________________________

### Test 3: Cross-Master Correlation (Critical!)
- [ ] Type: "Which stores should focus on ethnic wear during the Winter Bonanza campaign?"
- [ ] Send message
- [ ] Response analyzes multiple data sources:
  - [ ] Item Master (ethnic wear items mentioned)
  - [ ] Store Master (specific stores recommended)
  - [ ] Marketing Plan (Winter Bonanza campaign referenced)
  - [ ] Competition Master (competition considered)
- [ ] Response provides actionable recommendations
- [ ] Response cites specific data points
- [ ] No generic/assumed information used

**Result:** ☐ PASS | ☐ FAIL  
**Response Time:** _____ seconds  
**Correlation Quality:** ☐ Excellent | ☐ Good | ☐ Fair | ☐ Poor  
**Notes:** _______________________________________________

### Test 4: Complex Multi-Master Analysis
- [ ] Type: "Analyze the relationship between store revenue, local competition, and marketing campaign effectiveness"
- [ ] Send message
- [ ] Response correlates all 3 data sources
- [ ] Specific examples from each master provided
- [ ] Insights are data-driven (not generic advice)
- [ ] Recommendations are actionable

**Result:** ☐ PASS | ☐ FAIL  
**Response Time:** _____ seconds  
**Notes:** _______________________________________________

### Backend Console Check
- [ ] Check server terminal/console
- [ ] "📚 DATA CATALOGUE CONTEXT DETECTED" message appears for queries
- [ ] Catalogue summary logged
- [ ] No Python errors or warnings

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

---

## Part 6: Remove Functionality Testing (5 minutes)

### Test Single Remove
- [ ] Click "Remove" button under Item Master
- [ ] File info disappears
- [ ] "No file selected" or empty state shown
- [ ] Check DevTools → IndexedDB
  - [ ] itemMaster object store is empty
  - [ ] metadata entry for itemMaster removed
- [ ] Other 3 masters still have data

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

### Test Remove All
- [ ] Click "Remove" on all 4 masters
- [ ] All file info cleared
- [ ] All object stores empty (check DevTools)
- [ ] Type in chat: "Show items from catalogue"
- [ ] Response indicates no catalogue data available

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

### Test Re-upload After Remove
- [ ] Re-upload all 4 CSV files
- [ ] All uploads succeed
- [ ] Data visible in IndexedDB
- [ ] Gemini correlation query works again

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

---

## Part 7: Edge Cases & Error Handling (10 minutes)

### Empty File Test
- [ ] Create `test_data/empty.csv` (0 bytes or header only)
- [ ] Try uploading to Item Master
- [ ] Error handled gracefully
- [ ] User-friendly error message shown
- [ ] No console errors crash

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

### Invalid CSV Format Test
- [ ] Create `test_data/malformed.csv` with broken structure
- [ ] Try uploading to Store Master
- [ ] Parsing error caught
- [ ] Error message displayed
- [ ] Existing data not corrupted

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

### Large File Test (Optional)
- [ ] Create CSV with 100+ records
- [ ] Upload to Competition Master
- [ ] Upload completes successfully
- [ ] Performance acceptable (<5 seconds)
- [ ] All records stored in IndexedDB

**Result:** ☐ PASS | ☐ FAIL  
**Upload Time:** _____ seconds for _____ records  
**Notes:** _______________________________________________

### Filename Edge Cases
- [ ] Try `item.csv` (very short name) → should accept if contains "item"
- [ ] Try `store_data.xlsx` → should accept Excel files
- [ ] Try `products.csv` to Item Master → should accept (synonym)
- [ ] Try `stores.csv` to Marketing Plan → should reject (wrong category)

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

---

## Part 8: Performance Testing (5 minutes)

### Upload Performance
- [ ] Time each master upload (already captured above)
- [ ] All uploads complete in <1 second each
- [ ] UI remains responsive during upload
- [ ] No freezing or lag

**Item Master:** _____ ms  
**Store Master:** _____ ms  
**Competition Master:** _____ ms  
**Marketing Plan:** _____ ms  

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

### Query Performance
- [ ] Gemini simple query: <3 seconds
- [ ] Gemini correlation query: <8 seconds
- [ ] Backend processing: <2 seconds (check console logs)

**Simple Query:** _____ seconds  
**Correlation Query:** _____ seconds  

**Result:** ☐ PASS | ☐ FAIL  
**Notes:** _______________________________________________

---

## Part 9: Browser Compatibility (10 minutes per browser)

### Chrome
- [ ] All tests pass
- [ ] IndexedDB works correctly
- [ ] No console warnings

**Result:** ☐ PASS | ☐ FAIL | ☐ NOT TESTED

### Safari
- [ ] All tests pass
- [ ] IndexedDB works correctly
- [ ] No console warnings

**Result:** ☐ PASS | ☐ FAIL | ☐ NOT TESTED

### Firefox
- [ ] All tests pass
- [ ] IndexedDB works correctly
- [ ] No console warnings

**Result:** ☐ PASS | ☐ FAIL | ☐ NOT TESTED

---

## Final Assessment

### Overall Test Results
**Total Tests Executed:** _____  
**Tests Passed:** _____  
**Tests Failed:** _____  
**Pass Rate:** _____% 

### Critical Issues Found
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Minor Issues Found
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Recommendations
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Final Verdict
☐ **APPROVED FOR PRODUCTION** - All critical tests passed  
☐ **CONDITIONAL APPROVAL** - Minor issues, can deploy with fixes  
☐ **REQUIRES FIXES** - Critical issues must be resolved  
☐ **BLOCKED** - Major functionality broken

---

## Sign-Off

**Tester Name:** ________________  
**Date/Time:** ________________  
**Total Test Duration:** _____ minutes  
**Signature:** ________________

**Reviewed By:** ________________  
**Date:** ________________  
**Signature:** ________________

---

## Appendix: Console Commands for Debugging

Open DevTools Console and try these:

```javascript
// Check database list
indexedDB.databases().then(console.log)

// Get all item master data
getMasterData('itemMaster').then(console.log)

// Get all store master data
getMasterData('storeMaster').then(console.log)

// Get metadata for item master
getMetadata('itemMaster').then(console.log)

// Get all catalogue data (what Gemini receives)
getAllCatalogueDataForGemini().then(d => console.log(JSON.stringify(d, null, 2)))

// Clear specific master (for re-testing)
clearMasterData('itemMaster')

// Test validation
validateMasterFileName('item_master_sample.csv', 'itemMaster')
validateMasterFileName('store_data.csv', 'storeMaster')
```

---

**END OF CHECKLIST**

Save this file and check off items as you complete testing.
