# Data Reading Feature Documentation

## Overview

The V-Mart Personal AI Agent now includes comprehensive data reading functionality that can capture and analyze data from various applications running on your system, including:

- **Excel Files** - All sheets, columns, rows, filters, pivot tables, formulas
- **Google Sheets** - Spreadsheets, filters, hidden data, formulas
- **PowerPoint Presentations** - Slides, content, notes, charts, tables
- **Email (Gmail)** - Messages, subjects, bodies, attachments
- **Active Screen Detection** - Automatically detect and read from active applications

## Features

### 📊 Excel Data Reading

#### Capabilities
- ✅ Read all sheets (visible and hidden)
- ✅ Capture all columns and rows (including hidden)
- ✅ Extract filters and advanced filters
- ✅ Read pivot tables (including hidden ones)
- ✅ Capture formulas and calculated fields
- ✅ Get cell formatting and data validation
- ✅ Detect active Excel file automatically

#### API Usage

**Read Active Excel File:**
```bash
curl -X POST http://localhost:5000/data/read-excel \
  -H "Content-Type: application/json" \
  -d '{"include_hidden": true, "active_sheet_only": false}'
```

**Read Specific Excel File:**
```bash
curl -X POST http://localhost:5000/data/read-excel \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/your/file.xlsx",
    "include_hidden": true,
    "active_sheet_only": false
  }'
```

**Response Example:**
```json
{
  "metadata": {
    "filename": "sales_data.xlsx",
    "author": "John Doe",
    "sheet_count": 3,
    "sheet_names": ["Sales", "Hidden Analysis", "Summary"]
  },
  "sheets_data": {
    "Sales": {
      "sheet_name": "Sales",
      "visibility": "visible",
      "dimensions": {
        "max_row": 500,
        "max_column": 15
      },
      "columns": [...],
      "data": [...],
      "filters": {...},
      "formulas": [...]
    }
  }
}
```

### 📑 Google Sheets Data Reading

#### Capabilities
- ✅ Read all sheets (visible and hidden)
- ✅ Extract filters and filter views
- ✅ Capture hidden columns and rows
- ✅ Get cell data, formulas, and formatting
- ✅ Read metadata and properties
- ✅ Auto-detect active Google Sheets from browser

#### API Usage

**Read Active Google Sheet:**
```bash
curl -X POST http://localhost:5000/data/read-google-sheets \
  -H "Content-Type: application/json" \
  -d '{"include_hidden": true}'
```

**Read Specific Spreadsheet:**
```bash
curl -X POST http://localhost:5000/data/read-google-sheets \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
    "include_hidden": true
  }'
```

### 📽️ PowerPoint Data Reading

#### Capabilities
- ✅ Read all slides (visible and hidden)
- ✅ Extract slide content (text, tables, charts)
- ✅ Capture speaker notes
- ✅ Get slide layouts and masters
- ✅ Detect embedded objects
- ✅ Read metadata
- ✅ Auto-detect active PowerPoint file

#### API Usage

**Read Active PowerPoint:**
```bash
curl -X POST http://localhost:5000/data/read-powerpoint \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Read Specific File:**
```bash
curl -X POST http://localhost:5000/data/read-powerpoint \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/presentation.pptx"
  }'
```

### 📧 Email Data Reading

#### Capabilities
- ✅ Read email subject, body, and headers
- ✅ Get sender and recipients
- ✅ List attachments
- ✅ Read labels/folders
- ✅ Check read/unread status
- ✅ Search emails with queries

#### API Usage

**Read Recent Emails:**
```bash
curl -X POST http://localhost:5000/data/read-email \
  -H "Content-Type: application/json" \
  -d '{
    "max_results": 10,
    "query": ""
  }'
```

**Search Unread Emails:**
```bash
curl -X POST http://localhost:5000/data/read-email \
  -H "Content-Type: application/json" \
  -d '{
    "max_results": 10,
    "query": "is:unread"
  }'
```

**Search Emails with Attachments:**
```bash
curl -X POST http://localhost:5000/data/read-email \
  -H "Content-Type: application/json" \
  -d '{
    "max_results": 10,
    "query": "has:attachment"
  }'
```

### 🖥️ Active Screen Detection

#### Capabilities
- ✅ Detect currently active application
- ✅ Identify application type (Excel, Google Sheets, PowerPoint, Email)
- ✅ Read data from active window automatically
- ✅ Support for macOS, Windows, and Linux

#### API Usage

**Detect Active Application:**
```bash
curl -X GET http://localhost:5000/data/detect-application
```

**Read Data from Active Screen:**
```bash
curl -X POST http://localhost:5000/data/read-active-screen \
  -H "Content-Type: application/json" \
  -d '{"include_hidden": true}'
```

**Response Example:**
```json
{
  "source": "active_screen",
  "application_info": {
    "application": "Microsoft Excel",
    "window_title": "Budget 2024.xlsx",
    "app_type": "excel",
    "timestamp": "2025-11-09T10:30:00"
  },
  "data_type": "excel",
  "data": {...},
  "status": "success"
}
```

## Chatbot Commands

You can interact with the data reading feature through natural language in the chatbot:

### Examples

1. **"Read the data from my active Excel file"**
   - Detects and reads the currently open Excel file

2. **"Show me the hidden sheets in my spreadsheet"**
   - Extracts hidden sheets with their data

3. **"What filters are applied in this Excel file?"**
   - Lists all active filters

4. **"Read my recent emails"**
   - Fetches and summarizes recent emails

5. **"Show me the content of this PowerPoint presentation"**
   - Extracts text, tables, and charts from all slides

6. **"What's in the active Google Sheet?"**
   - Reads data from the currently open Google Sheets tab

## Python API Usage

### Excel Reader

```python
from connectors.excel_reader import ExcelReader

# Initialize
reader = ExcelReader()

# Read active Excel file
data = reader.get_active_sheet_data(include_hidden=True)

# Read specific file
reader.load_file('/path/to/file.xlsx')
all_data = reader.read_all_data(include_hidden=True)

# Get metadata
metadata = reader.get_file_metadata()

# Get sheets info
sheets = reader.get_all_sheets_info()
```

### Google Sheets Reader

```python
from connectors.google_sheets_reader import GoogleSheetsReader

# Initialize
reader = GoogleSheetsReader()

# Authenticate
reader.authenticate()

# Read active sheet
data = reader.read_all_data(include_hidden=True)

# Read specific spreadsheet
data = reader.read_all_data(
    spreadsheet_id='1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms',
    include_hidden=True
)
```

### PowerPoint Reader

```python
from connectors.powerpoint_reader import PowerPointReader

# Initialize
reader = PowerPointReader()

# Read active PowerPoint
data = reader.read_all_slides()

# Read specific file
reader.load_file('/path/to/presentation.pptx')
data = reader.read_all_slides()
```

### Email Reader

```python
from connectors.email_reader import EmailReader

# Initialize
reader = EmailReader()

# Authenticate
reader.authenticate()

# Get recent emails
emails = reader.get_recent_emails(max_results=10)

# Search emails
unread = reader.get_unread_emails(max_results=10)
starred = reader.get_starred_emails(max_results=10)
with_attachments = reader.get_emails_with_attachments(max_results=10)
```

### Unified Data Reader

```python
from connectors.data_reader import DataReaderConnector

# Initialize
connector = DataReaderConnector()

# Detect active application
app_info = connector.detect_active_application()

# Read from active screen
data = connector.read_active_screen_data(include_hidden=True)

# Get formatted summary for chatbot
summary = connector.format_for_chatbot(data)
```

## Configuration

### Google Sheets and Gmail Setup

1. **Get Google OAuth Credentials:**
   - Visit [Google Cloud Console](https://console.cloud.google.com)
   - Create a project
   - Enable Google Sheets API and Gmail API
   - Create OAuth 2.0 credentials
   - Download `credentials.json`

2. **Place credentials.json:**
   ```bash
   cp credentials.json "/path/to/V-Mart-Personal-AI-Agent/credentials.json"
   ```

3. **First-time authentication:**
   - Run the application
   - When accessing Google Sheets or Gmail for the first time
   - Browser will open for OAuth consent
   - Grant permissions
   - Tokens will be saved automatically

### Excel and PowerPoint Setup

No additional configuration required. The readers will:
- Auto-detect active Microsoft Office applications
- Read files using `openpyxl` and `python-pptx` libraries
- Work on macOS, Windows, and Linux

## Supported Platforms

| Platform | Screen Detection | Excel | Google Sheets | PowerPoint | Email |
|----------|-----------------|-------|---------------|------------|-------|
| **macOS** | ✅ AppleScript | ✅ | ✅ | ✅ | ✅ |
| **Windows** | ✅ PowerShell | ✅ | ✅ | ✅ | ✅ |
| **Linux** | ✅ xdotool | ✅ | ✅ | ✅ | ✅ |

## Troubleshooting

### Excel Not Detected

**Issue:** Active Excel file not found

**Solution:**
1. Ensure Excel is open with a file
2. Make Excel the active window (click on it)
3. For macOS: Grant accessibility permissions to Terminal/Python
4. For Windows: Run with administrator privileges if needed

### Google Sheets Authentication Failed

**Issue:** Unable to authenticate with Google Sheets API

**Solution:**
1. Verify `credentials.json` is in the correct location
2. Delete `token_sheets.pickle` and re-authenticate
3. Ensure Google Sheets API is enabled in Google Cloud Console
4. Check that OAuth redirect URIs are configured correctly

### PowerPoint Not Reading

**Issue:** Cannot read PowerPoint file

**Solution:**
1. Ensure PowerPoint file is saved (not just open)
2. Check file permissions
3. Verify `python-pptx` is installed: `pip install python-pptx`

### Email Not Loading

**Issue:** Gmail emails not loading

**Solution:**
1. Verify Gmail API is enabled
2. Delete `token_gmail.pickle` and re-authenticate
3. Check internet connection
4. Ensure correct scopes are granted

## Performance Considerations

- **Excel Large Files:** Reading is limited to first 100 rows by default for performance
- **Google Sheets:** API rate limits apply (100 requests per 100 seconds per user)
- **Email:** Fetching large attachments may be slow
- **PowerPoint:** Large presentations with many images may take longer

## Security Notes

- **Credentials:** Never commit `credentials.json` or token files to version control
- **API Keys:** Store in `.env` file, not in code
- **File Access:** Readers only access files user has permission to read
- **OAuth Tokens:** Stored locally, encrypted by Google's libraries
- **Data Privacy:** All data processing happens locally, not sent to external servers (except Google APIs for Sheets/Gmail)

## Future Enhancements

- [ ] Tableau dashboard reading (requires Tableau SDK)
- [ ] Outlook email support (requires win32com on Windows)
- [ ] PDF document reading
- [ ] CSV and text file parsing
- [ ] Database connection support
- [ ] Real-time screen capture and OCR
- [ ] Video file metadata extraction

## License

MIT License - See main project LICENSE file

## Support

For issues, questions, or feature requests:
- GitHub Issues: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/issues
- Documentation: https://github.com/ds25041974/V-Mart-Personal-AI-Agent/tree/main/docs

---

**Last Updated:** November 9, 2025  
**Version:** 1.0.0  
**Developed by:** DSR  
**Powered by:** Google Gemini AI
