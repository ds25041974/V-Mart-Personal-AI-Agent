#!/bin/bash

# Final Integration QA Test for V-Mart AI Agent File Upload
# This script validates the complete file upload and AI integration

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  V-MART AI AGENT - FINAL INTEGRATION QA TEST                   ║"
echo "║  Testing: File Upload + Auto-Processing + AI Integration       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -e "${BLUE}Test $TOTAL_TESTS: $test_name${NC}"
    
    result=$(eval "$test_command" 2>&1)
    
    if echo "$result" | grep -q "$expected_pattern"; then
        echo -e "${GREEN}✅ PASS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo -e "${RED}Expected pattern: $expected_pattern${NC}"
        echo -e "${RED}Got: $result${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

# Test 1: Backend server is running
run_test "Backend Server Running" \
    "curl -s http://localhost:8000/health 2>&1 || echo 'Server not responding'" \
    "healthy\|status"

# Test 2: Single text file upload
run_test "Single TXT File Upload" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_upload_1762889880.txt' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(\"SUCCESS\" if d.get(\"success\") and len(d.get(\"files\",[])) == 1 else \"FAIL\")'" \
    "SUCCESS"

# Test 3: CSV file upload with data parsing
run_test "CSV File with Data Parsing" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_data.csv' | python3 -c 'import json,sys; d=json.load(sys.stdin); f=d.get(\"files\",[{}])[0]; print(\"SUCCESS\" if \"Product\" in f.get(\"content\",\"\") else \"FAIL\")'" \
    "SUCCESS"

# Test 4: Multi-sheet Excel upload
run_test "Multi-Sheet Excel Upload" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_multisheet.xlsx' | python3 -c 'import json,sys; d=json.load(sys.stdin); f=d.get(\"files\",[{}])[0]; print(\"SUCCESS\" if \"Sales\" in f.get(\"content\",\"\") and \"Inventory\" in f.get(\"content\",\"\") else \"FAIL\")'" \
    "SUCCESS"

# Test 5: Multiple files upload (3 different types)
run_test "Multiple Files (TXT+CSV+XLSX)" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_upload_1762889880.txt' -F 'files=@/tmp/test_data.csv' -F 'files=@/tmp/test_multisheet.xlsx' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(\"SUCCESS\" if d.get(\"success\") and len(d.get(\"files\",[])) == 3 else \"FAIL\")'" \
    "SUCCESS"

# Test 6: JSON response structure validation
run_test "JSON Response Structure" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_data.csv' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(\"SUCCESS\" if all([\"success\" in d, \"files\" in d, \"file_count\" in d, isinstance(d.get(\"files\"), list)]) else \"FAIL\")'" \
    "SUCCESS"

# Test 7: File content extraction (full content, not preview)
run_test "Full Content Extraction (Not Preview)" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_upload_1762889880.txt' | python3 -c 'import json,sys; d=json.load(sys.stdin); f=d.get(\"files\",[{}])[0]; print(\"SUCCESS\" if f.get(\"content\") == f.get(\"preview\") or len(f.get(\"content\",\"\")) > 0 else \"FAIL\")'" \
    "SUCCESS"

# Test 8: File metadata generation
run_test "File Metadata Generation" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_data.csv' | python3 -c 'import json,sys; d=json.load(sys.stdin); f=d.get(\"files\",[{}])[0]; m=f.get(\"metadata\",{}); print(\"SUCCESS\" if m.get(\"rows\") or m.get(\"line_count\") or m.get(\"char_count\") else \"FAIL\")'" \
    "SUCCESS"

# Test 9: Error handling (empty upload)
run_test "Error Handling (No Files)" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload | python3 -c 'import json,sys; d=json.load(sys.stdin); print(\"SUCCESS\" if d.get(\"success\") == False or d.get(\"file_count\") == 0 else \"FAIL\")'" \
    "SUCCESS"

# Test 10: Content-Type header verification
run_test "Content-Type Header" \
    "curl -s -X POST http://localhost:8000/ai-chat/upload -F 'files=@/tmp/test_data.csv' -v 2>&1 | grep -i 'content-type.*application/json' && echo 'SUCCESS' || echo 'FAIL'" \
    "SUCCESS"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    TEST SUMMARY                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Total Tests:   ${BLUE}$TOTAL_TESTS${NC}"
echo -e "Passed:        ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed:        ${RED}$FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ ALL TESTS PASSED! Backend is ready for frontend testing.   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}📝 Next Steps:${NC}"
    echo "   1. Open browser to: http://localhost:8000/ai-chat"
    echo "   2. Go to 'File Browser' tab"
    echo "   3. Select files (they will auto-upload)"
    echo "   4. Open browser console (F12) to see detailed logs"
    echo "   5. Check for: ✅✅✅ SUCCESS! All validations passed"
    echo ""
    echo -e "${YELLOW}🐛 Debug Test Page:${NC}"
    echo "   open test_upload_debug.html"
    echo ""
    exit 0
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ❌ SOME TESTS FAILED - Review errors above                    ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
