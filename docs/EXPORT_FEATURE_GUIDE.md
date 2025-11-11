# Data Export Feature Guide

## Overview
The V-Mart Personal AI Agent now supports exporting analysis results with insights and recommendations in professional Excel and PDF formats.

## Features

✅ **Excel Export (.xlsx)**
- Formatted spreadsheets with color-coded sections
- Insights highlighted in light blue
- Recommendations highlighted in light orange
- Structured data tables
- Auto-sized columns for readability

✅ **PDF Export (.pdf)**
- Professional document layout
- Branded with V-Mart colors
- Organized sections with headers
- Preserved formatting from AI analysis
- Print-ready format

## Where to Find Export Buttons

### 1. Analysis Tab
After running data analysis:
1. Paste your data in the Analysis tab
2. Click "Analyze"
3. View the AI-generated insights and recommendations
4. **Export buttons appear** at the bottom:
   - 📊 **Export to Excel**
   - 📄 **Export to PDF**

### 2. Decision Support Tab
After analyzing a decision:
1. Enter decision title and context
2. Add options to consider
3. Click "Analyze Decision"
4. View the AI-generated decision analysis
5. **Export buttons appear** at the bottom:
   - 📊 **Export to Excel**
   - 📄 **Export to PDF**

## What Gets Exported

### Included in Every Export

**1. Metadata**
- Generation date and time
- User email
- Data source

**2. AI Analysis**
- Complete analysis from Gemini AI
- Cleaned HTML formatting
- Preserved structure

**3. Key Insights**
- Automatically extracted insights
- Numbered list format
- Highlighted for visibility

**4. Recommendations**
- Actionable recommendations from AI
- Numbered action items
- Highlighted for emphasis

**5. Data Tables** (if applicable)
- Structured tabular data
- Formatted headers
- Sortable columns (in Excel)

## Excel Export Features

### Sheet 1: Analysis Summary
```
┌─────────────────────────────────────┐
│  AI Analysis Report                 │  ← Title (Purple, Bold, 16pt)
├─────────────────────────────────────┤
│  Generated: 2025-11-10 16:45:23    │
│  User: user@vmart.co.in            │
│  Source: Data Analysis Tool         │
├─────────────────────────────────────┤
│  Analysis:                          │  ← Section Header (Purple bg)
│  [Full AI analysis text...]        │
├─────────────────────────────────────┤
│  Key Insights:                      │  ← Section Header
│  Insight 1: [AI insight...]        │  ← Light blue background
│  Insight 2: [AI insight...]        │
├─────────────────────────────────────┤
│  Recommendations:                   │  ← Section Header
│  Action 1: [Recommendation...]     │  ← Light orange background
│  Action 2: [Recommendation...]     │
└─────────────────────────────────────┘
```

### Sheet 2: Data (if applicable)
```
┌───────────┬────────────┬──────────┐
│ Column 1  │ Column 2   │ Column 3 │  ← Purple header
├───────────┼────────────┼──────────┤
│ Data 1    │ Data 2     │ Data 3   │
│ Data 4    │ Data 5     │ Data 6   │
└───────────┴────────────┴──────────┘
```

### Color Scheme
- **Headers**: Purple (#667eea) with white text
- **Insights**: Light blue background (#f0f4ff)
- **Recommendations**: Light orange background (#fff4e6)
- **Data Tables**: Beige rows with black borders

## PDF Export Features

### Layout
- **Page Size**: US Letter (8.5" × 11")
- **Margins**: 0.75" all sides
- **Font**: Helvetica (system font)
- **Colors**: V-Mart brand colors

### Sections

**1. Title Page**
```
╔════════════════════════════════╗
║   AI Analysis Report           ║  ← Purple, 18pt
║                                ║
║   Generated: [date/time]       ║
║   User: [email]                ║
║   Source: [tool name]          ║
╚════════════════════════════════╝
```

**2. Analysis Section**
- Bold heading (14pt)
- Justified text (10pt)
- Proper paragraph breaks
- Preserved formatting

**3. Key Insights Section**
- Bold heading
- Numbered insights (1, 2, 3...)
- Light blue background boxes
- Easy to scan

**4. Recommendations Section**
- Bold heading
- Numbered actions
- Light orange background boxes
- Actionable items highlighted

**5. Data Tables** (if applicable)
- Separate page
- Purple header row
- Beige alternating rows
- Grid borders
- Maximum 50 rows per PDF

## How to Use

### Step-by-Step: Export Analysis

1. **Run Analysis**
   ```
   Analysis Tab → Paste Data → Select Type → Click Analyze
   ```

2. **View Results**
   - AI analysis appears in result box
   - Export buttons appear automatically

3. **Choose Format**
   - Click **📊 Export to Excel** for spreadsheet
   - Click **📄 Export to PDF** for document

4. **Download**
   - File downloads automatically
   - Filename: `AI_Analysis_YYYYMMDD_HHMMSS.xlsx/pdf`

### Step-by-Step: Export Decision

1. **Analyze Decision**
   ```
   Decision Tab → Enter Title → Add Context → Add Options → Click Analyze
   ```

2. **View Analysis**
   - Decision analysis appears
   - Export buttons appear

3. **Export**
   - Choose Excel or PDF
   - File downloads immediately

## File Naming Convention

### Excel Files
```
AI_Analysis_20251110_164523.xlsx
└─┬─┘ └──┬───┘ └──┬───┘└──┬──┘
  │       │        │       └─ Timestamp (HH:MM:SS)
  │       │        └───────── Date (YYYYMMDD)
  │       └────────────────── Type
  └────────────────────────── Prefix
```

### PDF Files
```
AI_Analysis_20251110_164523.pdf
└─┬─┘ └──┬───┘ └──┬───┘└──┬──┘
  │       │        │       └─ Timestamp
  │       │        └───────── Date
  │       └────────────────── Type
  └────────────────────────── Prefix
```

## Technical Details

### Dependencies
- **Excel**: `xlsxwriter` library
- **PDF**: `reportlab` library
- Both installed automatically with requirements.txt

### Export Endpoint
```
POST /export/<format_type>

Parameters:
- format_type: 'excel' or 'pdf'

Body (JSON):
{
  "title": "Report Title",
  "analysis": "Full AI analysis...",
  "insights": ["Insight 1", "Insight 2"],
  "recommendations": ["Rec 1", "Rec 2"],
  "data_table": [{"col1": "val1"}, ...],  // Optional
  "source": "Tool name"
}

Response:
- Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (Excel)
- Content-Type: application/pdf (PDF)
- Content-Disposition: attachment
```

### Check Availability
```
GET /export/check

Response:
{
  "excel_available": true,
  "pdf_available": true,
  "message": "Export functionality is ready"
}
```

## Troubleshooting

### Export Buttons Not Showing
**Problem**: Export buttons don't appear after analysis
**Solution**: 
1. Refresh the page
2. Run analysis again
3. Check browser console for errors

### "Export functionality not available" Error
**Problem**: Libraries not installed
**Solution**:
```bash
cd "V-Mart Personal AI Agent"
source venv/bin/activate
pip install reportlab xlsxwriter
```

### Download Doesn't Start
**Problem**: Browser blocks download
**Solution**:
1. Check browser's download settings
2. Allow downloads from localhost:8000
3. Check browser's blocked downloads list

### Excel File Won't Open
**Problem**: File corrupted or incomplete
**Solution**:
1. Try exporting again
2. Ensure analysis completed successfully
3. Check if antivirus is blocking the file

### PDF Shows Garbled Text
**Problem**: Special characters not rendering
**Solution**:
- PDF uses Helvetica font (supports ASCII)
- Special Unicode characters may not display
- Stick to standard characters for best results

## Best Practices

### For Best Excel Exports

1. **Keep Analysis Structured**
   - Use clear headings
   - Organize insights in lists
   - Separate recommendations clearly

2. **Data Tables**
   - Use consistent column names
   - Keep column count reasonable (< 20 columns)
   - Use simple data types

3. **File Size**
   - Excel supports large datasets
   - No practical limit for AI analysis text

### For Best PDF Exports

1. **Formatting**
   - Use **bold** for emphasis
   - Keep paragraphs short
   - Use bullet points for lists

2. **Length**
   - PDFs work best with 1-5 pages
   - Very long analysis may need pagination
   - Data tables limited to 50 rows

3. **Readability**
   - Clear section headers
   - Proper punctuation
   - Logical organization

## Use Cases

### Business Reports
- Weekly sales analysis → Excel export
- Monthly performance review → PDF export
- Quarterly insights summary → Both formats

### Decision Making
- Investment decisions → PDF for sharing
- Resource allocation → Excel for calculations
- Strategy planning → Both for team review

### Data Analysis
- Sales trends → Excel with charts
- Customer insights → PDF presentation
- Inventory analysis → Excel for tracking

## Future Enhancements

🔄 **Planned Features**:
- [ ] Chart generation in Excel
- [ ] Custom branding/logos in PDF
- [ ] PowerPoint export option
- [ ] Email export directly from app
- [ ] Scheduled automatic exports
- [ ] Cloud storage integration
- [ ] Export templates

---

**Last Updated**: November 10, 2025  
**Feature Version**: 1.0  
**Supported Formats**: Excel (.xlsx), PDF (.pdf)  
**Developed by**: DSR | Inspired by: LA | Powered by: Gemini AI
