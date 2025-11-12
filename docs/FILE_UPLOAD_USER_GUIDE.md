# File Upload Guide for AI Analysis

## Quick Start

### 1. Upload Your Files
- Click the 📎 **Attach Files** button in the chat interface
- Select one or more files:
  - **PDF** files (reports, documents)
  - **CSV** files (data exports)
  - **Excel** files (.xlsx, .xls) - all sheets will be read

### 2. Ask Questions
Once files are uploaded, ask the AI questions about the data:

```
✅ "Which store has the highest revenue?"
✅ "What are the top 3 products?"
✅ "Compare performance between Delhi and Mumbai"
✅ "Identify underperforming stores"
✅ "Give me recommendations based on this data"
```

### 3. AI Will Analyze
The AI will:
- Read data directly from your uploaded files
- Analyze ONLY the file data (no assumptions)
- Provide insights with exact numbers
- Quote specific values from your files
- Give actionable recommendations

## Supported File Types

### CSV Files ✅
**Format Requirements:**
- Headers in first row
- Data in subsequent rows
- No commas within values (or use quotes)

**Good Example:**
```csv
Store ID,Store Name,City,Revenue,Category
ST001,V-Mart Delhi,Delhi,4500000,Electronics
ST002,V-Mart Mumbai,Mumbai,5200000,Fashion
```

**Bad Example (will fail):**
```csv
Store ID,Store Name,City,Revenue,Category
ST001,V-Mart Delhi,Delhi,₹45,00,000,Electronics  ❌ Commas in revenue
```

**Fix Option 1:** Remove commas in numbers
```csv
Store ID,Store Name,City,Revenue,Category
ST001,V-Mart Delhi,Delhi,4500000,Electronics  ✅
```

**Fix Option 2:** Use quotes
```csv
Store ID,Store Name,City,Revenue,Category
ST001,V-Mart Delhi,Delhi,"₹45,00,000",Electronics  ✅
```

### Excel Files ✅
- Supports .xlsx and .xls formats
- **All sheets** are automatically read
- Handles multiple sheets in one file
- Preserves formulas (as values)

### PDF Files ✅
- Text-based PDFs (reports, documents)
- Scanned PDFs (if OCR is enabled)
- Tables will be extracted as text
- Multiple pages supported

## Example Workflows

### Workflow 1: Store Performance Analysis

**1. Upload:** `store_sales_report.csv`

**2. Ask:**
```
"Which are the top 5 performing stores this month?"
```

**3. AI Response:**
```
Based on the uploaded file store_sales_report.csv:

Top 5 Performing Stores:
1. V-Mart Mumbai West - ₹5,200,000 (Fashion category)
2. V-Mart Delhi Central - ₹4,500,000 (Electronics)
3. V-Mart Bangalore Tech - ₹3,800,000 (Electronics)
4. V-Mart Chennai Marina - ₹3,100,000 (Home & Living)
5. V-Mart Pune Deccan - ₹2,900,000 (Fashion)

**Insights:**
- Mumbai West leads with 33% higher revenue than average
- Electronics and Fashion are top categories
- South region (Chennai) underperforming
```

### Workflow 2: Multi-File Analysis

**1. Upload:**
- `q1_sales.csv`
- `q2_sales.csv`
- `product_catalog.pdf`

**2. Ask:**
```
"Compare Q1 vs Q2 sales and identify trending products"
```

**3. AI Response:**
AI will analyze all 3 files together and provide comparative insights.

### Workflow 3: Data Validation

**1. Upload:** `inventory_report.xlsx`

**2. Ask:**
```
"Find stores with inventory below 100 units for any product"
```

**3. AI Response:**
AI will scan all sheets and identify low-inventory items.

## Tips for Best Results

### ✅ DO:
- Upload clean, well-formatted files
- Use clear column headers
- Ask specific questions
- Reference specific metrics you want to analyze
- Upload multiple related files for comprehensive analysis

### ❌ DON'T:
- Use corrupted or password-protected files
- Mix unrelated data in the same question
- Expect AI to access data from previous sessions (re-upload files)
- Use commas within CSV values (unless quoted)

## File Size Limits

- **Maximum file size:** 10 MB per file
- **Maximum files:** 10 files at once
- **Content analyzed:** Up to 10,000 characters per file

For large files, consider:
- Splitting into smaller files
- Removing unnecessary columns
- Uploading only the most relevant data

## Troubleshooting

### "AI says it cannot access my file"
✅ **Solution:** Make sure file uploaded successfully (you'll see file name displayed)
✅ **Solution:** Re-upload the file if needed
✅ **Solution:** Check file is not corrupted

### "AI gives wrong numbers"
✅ **Solution:** Check your CSV doesn't have commas in numbers
✅ **Solution:** Verify file uploaded correctly (check file preview)
✅ **Solution:** Ask AI to "show me the exact data from the file"

### "Upload fails"
✅ **Solution:** Check file size (max 10 MB)
✅ **Solution:** Verify file format is supported (CSV, Excel, PDF)
✅ **Solution:** Try a different file format

## Privacy & Security

- ✅ Files are processed in memory (not saved to disk)
- ✅ File content is only accessible during your session
- ✅ Files are automatically cleared after analysis
- ✅ No file data is stored permanently

## Example Questions

### Revenue Analysis
```
"Which store has the highest revenue?"
"Compare revenue across all cities"
"Show me stores with revenue below 3 million"
```

### Product Analysis
```
"What are the top-selling products?"
"Which category performs best in each city?"
"Identify slow-moving products"
```

### Trend Analysis
```
"Compare this month vs last month sales"
"Show me growth trends by store"
"Which stores are declining?"
```

### Recommendations
```
"Give me 3 actionable insights from this data"
"What should I prioritize based on this report?"
"Recommend stores that need attention"
```

## Technical Details

### File Processing
1. **Upload** → File sent to `/ai-chat/upload`
2. **Extraction** → Text/data extracted using processors
3. **Storage** → Content stored in session (temporary)
4. **Analysis** → Content sent to Gemini AI with your question
5. **Response** → AI analyzes and streams back insights

### Data Format
Files are converted to structured text:
```
📊 COMPLETE DATA (All Rows):
Store ID,Store Name,City,Revenue,Category
ST001,V-Mart Delhi,Delhi,4500000,Electronics
ST002,V-Mart Mumbai,Mumbai,5200000,Fashion

📋 TABLE FORMAT (First 20 rows):
[Readable table view]

📈 NUMERIC STATISTICS:
[Min, max, mean, standard deviation]
```

---

## Need Help?

If you encounter any issues:
1. Check this guide's troubleshooting section
2. Verify your file format matches the requirements
3. Try uploading a different file format
4. Contact support if issue persists

**Status:** ✅ Fully Operational
**Last Updated:** November 12, 2025
**Version:** 2.0
