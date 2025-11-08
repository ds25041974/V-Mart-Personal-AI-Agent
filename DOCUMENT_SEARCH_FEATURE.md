# 📚 Document Search Feature - V-Mart AI Agent

## ✅ What's New

Your chatbot can now **search and analyze documents** from your local system to answer questions about progress reports, spreadsheets, presentations, and more!

## 🎯 How It Works

### Automatic Document Detection

The chatbot automatically searches for documents when you use keywords like:

- **Document keywords**: `document`, `doc`, `file`, `sheet`, `slide`, `presentation`, `pdf`, `excel`, `word`, `ppt`
- **Location keywords**: `local`, `computer`, `system`, `folder`, `desktop`, `documents`, `downloads`
- **Progress keywords**: `progress`, `report`, `status`, `result`, `metric`, `data`, `analysis`

### Search Locations

The chatbot scans these folders on your Mac:
- 📁 `~/Documents`
- 🖥️ `~/Desktop`
- ⬇️ `~/Downloads`

### Supported File Types

✅ PDF files (`.pdf`)
✅ Word documents (`.doc`, `.docx`)
✅ Excel spreadsheets (`.xlsx`, `.xls`)
✅ PowerPoint presentations (`.ppt`, `.pptx`)
✅ Text files (`.txt`, `.md`, `.csv`, `.rtf`)

## 💬 Example Questions You Can Ask

### Basic Document Queries
```
"Show me my progress report"
"What documents do I have about sales?"
"Find my presentation files"
"What's in my spreadsheet about Q4 results?"
```

### Progress-Related Questions
```
"Summarize my progress reports"
"What are the key metrics in my data files?"
"Analyze the results from my documents"
"Show me status updates from my files"
```

### Location-Specific Queries
```
"What documents are on my desktop?"
"Find files in my downloads folder"
"Search my local computer for reports"
```

## 🔍 What the Chatbot Returns

When documents are found, you'll see:

1. **📚 Source Attribution**: "Sources: Found X documents in local system"
2. **📁 Document List**: Up to 8 most recent matching files with:
   - File name
   - Location (Documents/Desktop/Downloads)
   - File size in KB
   - Directory path
   - Content preview (for text files)

3. **🤖 AI Analysis**: The chatbot will analyze the documents and answer your question based on the available information

## ⚙️ Technical Details

### Search Configuration
- **Max depth**: 2 levels deep in folders
- **Max documents shown**: 8 most recent files
- **Content preview**: First 200 characters for text files
- **Sorting**: By modification date (newest first)

### Smart Features
- ✅ Skips hidden files and folders (starting with `.`)
- ✅ Extracts search terms from your question (words longer than 4 characters)
- ✅ Shows file metadata (size, location, path)
- ✅ Reads text file previews (.txt, .md, .csv)
- ✅ Performance optimized with depth limits

## 📧 Gmail and Google Drive Support

### Current Status
The chatbot will inform you that Gmail and Google Drive search requires OAuth authentication:

```
📧 Note: Gmail search requires Google OAuth authentication (currently in demo mode).
☁️ Note: Google Drive search requires OAuth authentication (currently in demo mode).
```

### To Enable Gmail/Drive (Optional)
If you want to search Gmail and Google Drive:
1. Set up Google OAuth credentials in `.env`
2. Configure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
3. Remove demo mode by using regular login

## 🚀 Try It Now!

1. **Open the chatbot**: http://localhost:8000
2. **Ask a question**: "Show me my progress reports"
3. **See the results**: The chatbot will find documents and provide analysis

## 📝 Example Interaction

**You**: "What documents do I have about progress?"

**Chatbot**:
```
📚 Sources: Found 5 documents in local system

📁 AVAILABLE DOCUMENTS:
============================================================

1. Q4_Progress_Report.pdf
   Location: Documents
   Size: 245.3 KB
   Path: /Users/yourname/Documents/Reports

2. Sales_Progress_2024.xlsx
   Location: Desktop
   Size: 89.7 KB
   Path: /Users/yourname/Desktop

3. Project_Status.docx
   Location: Documents
   Size: 52.1 KB
   Path: /Users/yourname/Documents/Work

============================================================

Based on the documents found, I can see you have:
- A Q4 Progress Report in PDF format
- A Sales Progress spreadsheet for 2024
- A Project Status document

Would you like me to help you analyze any specific document?
```

## 🔧 Files Modified

- `src/web/app.py` - Enhanced `/ask` endpoint with document search
- `src/web/app_backup.py` - Backup of previous version (for safety)

## 📊 Performance Notes

- Fast scanning (limited to 2-level depth)
- No impact on basic chat queries (only searches when keywords detected)
- Handles large directories efficiently
- Graceful error handling if folders don't exist

## 🎉 Summary

Your chatbot is now **document-aware** and can help you find, analyze, and summarize information from your local files! Ask questions naturally, and it will search your Documents, Desktop, and Downloads folders automatically.

---

**Server Status**: ✅ Running on http://localhost:8000
**Model**: gemini-2.0-flash (FREE tier)
**Authentication**: Demo mode active
