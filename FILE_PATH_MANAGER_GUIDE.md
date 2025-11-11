# File Browser & Path Manager Guide

## Overview

The V-Mart AI Agent now includes two powerful features for working with files and data:

1. **📁 Enhanced File Browser Tab** - Upload and analyze multiple file formats
2. **🗂️ Path Manager Tab** - Configure fixed paths for direct AI access to your data

## Features Implemented

### 📁 File Browser Tab

The enhanced File Tab allows you to:

#### Supported File Formats
- **Images**: JPG, JPEG, PNG, GIF, BMP
- **Spreadsheets**: XLSX, XLS, CSV
- **Documents**: DOC, DOCX
- **PDF Files**: PDF
- **Text Files**: TXT, MD, JSON

#### Functionality
1. **Browse & Select Multiple Files**
   - Click "📂 Browse Files" button
   - Select one or multiple files
   - View selected files with size information
   - Remove individual files before upload

2. **Upload & Analyze**
   - Click "⬆️ Upload & Analyze Files" to upload all selected files
   - View file content preview
   - Files are automatically processed and made available to AI

3. **AI Chat for Files**
   - Once files are uploaded, a chat interface appears
   - Ask questions about your uploaded files
   - AI (Gemini LLM) analyzes file content and provides insights
   - Example: "What are the key points in this document?"

4. **Server File Search**
   - Search for files on the server
   - Click on any file to view its content

### 🗂️ Path Manager Tab

The Path Manager allows you to configure fixed local paths for direct AI access:

#### Features

1. **Add New Paths**
   - **Path Name**: Give your path a descriptive name (e.g., "My Documents")
   - **Path Location**: 
     - Use the "📁 Browse" button to select a folder
     - Or manually enter path (e.g., `/Users/username/Documents` or `C:\Users\username\Documents`)
   - **Description**: Optional description for the path

2. **Path Validation**
   - Click "🔍 Validate Path" to check if the path is valid
   - System verifies the path exists and is accessible

3. **Configured Paths Management**
   - View all configured paths
   - Each path shows:
     - Name and location
     - Description
     - Date added
   - Actions:
     - **🔍 Scan**: Scan the path to index files
     - **🗑️ Remove**: Remove the path configuration

4. **Automatic Path Refresh**
   - Click "🔄 Refresh" to reload the path list

## Smart Data Reading Priority System

The AI uses an intelligent priority system to access your data:

### Priority 1: Path Manager
- If you've configured paths in Path Manager, AI **first checks** these paths
- When you ask a question, AI searches configured paths for relevant files
- This is the **fastest and most direct** way for AI to access your data

### Priority 2: File Browser
- If no relevant data in configured paths, AI checks **uploaded files** from File Tab
- Uses content from files you've recently uploaded

### Priority 3: APIs & External Sources
- If no local data available, AI falls back to:
  - Connected APIs
  - General knowledge from Gemini LLM
  - Store data, weather data, analytics data (if applicable)

## Usage Examples

### Example 1: Upload and Analyze Excel File

1. Go to **📁 Files** tab
2. Click **📂 Browse Files**
3. Select your Excel file (e.g., `sales_data.xlsx`)
4. Click **⬆️ Upload & Analyze Files**
5. In the AI chat, ask: "What are the total sales for last month?"
6. Gemini AI analyzes the Excel content and responds with insights

### Example 2: Configure Document Folder

1. Go to **🗂️ Path Manager** tab
2. Enter:
   - **Path Name**: "Work Documents"
   - **Path Location**: `/Users/yourname/Documents/Work` (or browse to select)
   - **Description**: "All my work-related documents"
3. Click **🔍 Validate Path** to verify
4. Click **➕ Add Path**
5. Click **🔍 Scan** to index the files
6. Now in **💬 Chat** tab, ask: "Find information about project timeline"
7. AI automatically searches your configured Work Documents folder

### Example 3: Smart Fallback

1. **Scenario**: You ask "What's in my sales report?"
2. **AI Response Flow**:
   - ✅ First: Checks Path Manager for "sales report" files
   - ✅ If not found: Checks uploaded files in File Browser
   - ✅ If still not found: Informs you no sales report data is available
   - ℹ️ Suggests: Upload the file or configure the path

## Integration with Gemini AI

### Tight Integration Features

1. **Direct File Content Access**
   - Gemini LLM reads actual file content
   - Not just file names - actual data inside files

2. **Context-Aware Responses**
   - AI understands which files are relevant to your question
   - Provides specific answers citing file content

3. **Multi-File Analysis**
   - Can analyze multiple files simultaneously
   - Compares data across different sources

4. **Curated & Precise Answers**
   - Responses are based on YOUR data
   - More accurate than general knowledge
   - Cites specific files used for the answer

## Technical Details

### Backend API Endpoints

#### File Browser APIs
- `POST /ai-chat/upload` - Upload multiple files
- `GET /files/search?q=query` - Search server files
- `POST /files/read` - Read file content

#### Path Manager APIs
- `GET /api/paths/` - Get all configured paths
- `POST /api/paths/add` - Add new path
- `POST /api/paths/validate` - Validate path
- `POST /api/paths/{id}/scan` - Scan path for files
- `DELETE /api/paths/{id}` - Remove path

### Data Flow

```
User Question → Chat Tab
    ↓
AI Priority System
    ↓
1. Check Path Manager (configured paths)
    ├─ Found → Use path files
    └─ Not found → Continue
    ↓
2. Check File Browser (uploaded files)
    ├─ Found → Use uploaded files
    └─ Not found → Continue
    ↓
3. Use APIs / General Knowledge
    └─ Gemini LLM response
```

### Security & Privacy

- **Local Files**: Path Manager accesses only paths YOU configure
- **Uploaded Files**: Stored temporarily, processed by Gemini AI
- **No Auto-Scanning**: System never scans your computer without permission
- **User Control**: You decide which files/folders AI can access

## Best Practices

### For File Browser
1. **Organize Files**: Upload related files together for better context
2. **File Sizes**: Keep files under 10MB for faster processing
3. **Clear Context**: After analyzing, you can clear and upload new files
4. **Ask Specific**: Be specific in questions (e.g., "What's in column B?" vs "Analyze")

### For Path Manager
1. **Descriptive Names**: Use clear names for paths (e.g., "Q4 Reports", not "Folder1")
2. **Relevant Paths**: Only add paths with files you want AI to access
3. **Regular Scans**: Rescan paths when you add new files to the folder
4. **Path Cleanup**: Remove paths you no longer need

### For AI Questions
1. **Be Specific**: "What are sales in Q3?" vs "Tell me about sales"
2. **Reference Files**: "In the uploaded Excel file, what..."
3. **Multi-Step**: Can ask follow-up questions about same files
4. **Clarify Source**: If needed, ask "Which file did you use for this answer?"

## Troubleshooting

### File Browser Issues

**Problem**: Files not uploading
- **Solution**: Check file format is supported
- **Solution**: Ensure file size is under limit
- **Solution**: Check browser console for errors

**Problem**: Can't see uploaded files
- **Solution**: Click "⬆️ Upload & Analyze Files" button
- **Solution**: Wait for upload to complete
- **Solution**: Refresh the page

### Path Manager Issues

**Problem**: Path validation fails
- **Solution**: Check path exists on your system
- **Solution**: Ensure you have read permissions
- **Solution**: Use absolute path (full path from root)

**Problem**: Scan finds no files
- **Solution**: Verify folder contains supported file types
- **Solution**: Check folder permissions
- **Solution**: Remove and re-add the path

**Problem**: AI doesn't use configured paths
- **Solution**: Ensure path is scanned after adding
- **Solution**: Ask questions related to files in that path
- **Solution**: Check path hasn't been removed

## Rate Limits (Gemini API)

When using AI with files:
- **Free Tier**: 60 requests/minute, 1,500/day
- **Rate Limit Hit**: Wait 60 seconds and retry
- **Automatic Retry**: System retries with exponential backoff

## Updates & Roadmap

### ✅ Completed (v2.0)
- Multi-format file browser
- Path Manager with validation
- Smart priority system
- Gemini AI integration
- File upload & preview
- Path scanning & indexing

### 🔜 Planned Features
- Image analysis (OCR for scanned documents)
- Excel formula analysis
- PDF text extraction with formatting
- Folder watching (auto-update when files change)
- Cloud storage integration (Google Drive, OneDrive)
- Batch file processing

## Support

For issues or questions:
1. Check this guide first
2. Review error messages in UI
3. Check browser console (F12)
4. Contact: Developed by DSR

---

**💡 Developed by DSR | ✨ Inspired by LA | 🤖 Powered by Gemini AI**
