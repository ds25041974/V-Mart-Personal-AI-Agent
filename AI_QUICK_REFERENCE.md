# Enhanced AI Integration - Quick Reference
## V-Mart Personal AI Agent

---

## 🚀 Quick Start

### 1. Single File Analysis
```javascript
// Upload file via UI File Browser
// Ask: "Analyze this sales report"
```

### 2. Multi-File Cross-Reference
```javascript
// Upload multiple files: sales.xlsx, inventory.csv
// System automatically detects cross-references
// Ask: "Find stock-out risks using both files"
```

### 3. Store + Weather Analysis
```javascript
// Ask: "How will weather affect sales today at VM_DL_001?"
// System auto-loads: Store data + Weather + Competition
```

---

## 📊 Data Sources Priority

1. **Path Manager** (configured paths) → Highest priority
2. **File Browser** (uploaded files) → Second priority  
3. **APIs** (weather, geo, competition) → Third priority
4. **Retail Intelligence** (sales, inventory, etc.) → Integrated

---

## 💡 Sample Queries

### Sales Analysis
```
"Analyze sales performance for last month"
"Which products are top sellers?"
"Compare sales between Delhi and Mumbai stores"
```

### Inventory Management
```
"Find products at stock-out risk"
"Recommend reorder quantities for next week"
"Show overstocked items"
```

### Weather-Based Insights
```
"Will rain affect sales today?"
"Recommend products for sunny weather"
"Weather forecast impact for this weekend"
```

### Competition Analysis
```
"How many competitors near VM_DL_001?"
"Compare our pricing with DMart"
"Market share analysis for Mumbai"
```

### Multi-File Analysis
```
"Compare sales and inventory files"
"Find discrepancies between reports"
"Cross-reference product IDs across all files"
```

---

## 🔧 Response Format

### Standard Response Structure
```
🔍 Key Insights:
• Insight 1
• Insight 2
• Insight 3

[AI Analysis Paragraph]

💡 Recommendations:
• Recommendation 1
• Recommendation 2
• Recommendation 3

📚 Data Sources:
• Source 1
• Source 2
```

---

## 📁 Supported File Formats

✅ **Excel**: .xlsx, .xls  
✅ **CSV**: .csv  
✅ **PDF**: .pdf (with OCR)  
✅ **Word**: .doc, .docx  
✅ **Text**: .txt, .md  
✅ **Images**: .jpg, .png (OCR)  

---

## 🎯 Key Features

### Curated Responses
- Structured output with sections
- Extracted insights automatically
- Actionable recommendations
- Data citations for transparency

### Multi-File Cross-Reference
- Auto-detects common data (IDs, dates, amounts)
- Finds correlations between files
- Highlights discrepancies
- Generates insights from patterns

### INR Formatting
- `₹1,234.56` (under 1 lakh)
- `₹2.5 L` (lakhs)
- `₹15.8 Cr` (crores)

### Smart Detection
- Greetings → Quick response (no file analysis)
- Comparison keywords → Multi-source analysis
- Store mentions → Auto-load geo/weather
- File questions → Deep file reading

---

## 🛠️ Configuration

### Required
```bash
GEMINI_API_KEY=your_key_here
```

### Optional
```bash
OPENWEATHER_API_KEY=your_key_here  # For weather data
STORE_DATABASE_PATH=data/stores.db  # Store info
```

---

## ⚡ Performance

- Simple queries: **1-2s**
- Single file: **2-4s**
- Multi-file: **3-6s**
- Complex analytics: **4-8s**

---

## 🔍 Pattern Detection

The system auto-detects:
- Store IDs: `VM_XX_###`
- Product IDs: `PRD####`
- Dates: `DD/MM/YYYY`
- Amounts: `₹##,###.##`
- Percentages: `##%`
- Phone: `+91-##########`
- Email: `user@example.com`

---

## 📱 API Endpoints

### Chat
```bash
POST /ask
{
  "prompt": "your question",
  "store_id": "VM_DL_001",  # optional
  "city": "Delhi"           # optional
}
```

### Upload
```bash
POST /ai-chat/upload
Content-Type: multipart/form-data
files: [file1, file2, ...]
```

---

## 🎓 Tips

1. **Upload related files together** for better cross-reference analysis
2. **Mention file names** when asking specific questions
3. **Use "compare" keyword** for multi-source analysis
4. **Provide store_id** for location-aware insights
5. **Check citations** to verify data sources

---

## 🐛 Common Issues

**Files not analyzing?**
→ Check file format is supported

**Weather not loading?**
→ Verify OPENWEATHER_API_KEY is set

**Cross-references not found?**
→ Ensure files have common data (IDs, dates, etc.)

**Slow responses?**
→ Reduce file size or number of files

---

## 📚 Full Documentation

See **ENHANCED_AI_INTEGRATION.md** for complete details.

---

**Version**: 2.0.0  
**Status**: Production Ready ✅
