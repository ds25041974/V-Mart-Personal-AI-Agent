# Path Configuration Feature

## Overview

The Path Configuration feature allows you to configure local file system paths (folders or individual files) that the AI chatbot can automatically access and analyze. This eliminates the need to manually upload files each time you want to ask questions about your local data.

## Key Benefits

- **Direct File Access**: AI can read files directly from your local drives/folders
- **Automatic File Discovery**: Scan entire folders to find relevant files
- **Persistent Configuration**: Save path configurations for repeated use
- **Intelligent Search**: AI searches configured paths for relevant files based on your questions
- **Curated Insights**: Get detailed analysis, recommendations, and summarization from local data
- **No Manual Uploads**: Set it once, use it always

## Features

### 1. Path Management
- Add multiple folder or file paths
- Configure each path with a name and description
- View all configured paths in one place
- Delete paths when no longer needed

### 2. File Scanning
- Automatically scan folders to count files
- Identify file types (PDF, Excel, Word, images, etc.)
- Track total file count and storage size
- Update scan results as files change

### 3. Smart File Search
- AI automatically searches configured paths when you ask questions
- Finds files matching keywords in your question
- Reads file content using intelligent processors
- Supports: PDF, DOCX, XLSX, CSV, TXT, images

### 4. AI Integration
- Files from configured paths are automatically included in AI context
- AI provides insights based on latest file content
- No need to re-upload files when they change
- Combines uploaded files + path files + question context

## How to Use

### Opening Path Configuration

1. **Click Settings Button**: In the AI Chat interface, click the ⚙️ **Configure Paths** button in the top-right corner
2. **Modal Opens**: A configuration modal will appear

### Adding a Path

1. **Fill Form Fields**:
   - **Path Name**: Give it a meaningful name (e.g., "Sales Reports", "Inventory Data")
   - **Location**: Enter full path (e.g., `/Users/username/Documents/Reports`)
   - **Description**: Optional description of what this path contains

2. **Click Add Path**: The ➕ button will add the configuration

3. **View in List**: Your path appears in the configured paths list below

### Managing Paths

Each configured path shows:
- **Badge**: `folder` or `file` type indicator
- **Name**: Your custom name
- **Location**: Full file system path
- **File Count**: Number of files (after scanning)
- **Actions**:
  - 🔍 **Scan**: Count files and analyze types
  - 🗑️ **Delete**: Remove this path configuration

### Using Configured Paths in Chat

Once paths are configured, the AI automatically uses them:

1. **Ask Your Question**: Type normally in the chat
2. **Automatic Search**: AI searches configured paths for relevant files
3. **File Processing**: Relevant files are read and processed
4. **Enhanced Response**: AI includes insights from your local files

**Example**:
```
You: "What were last month's sales figures?"

AI searches configured paths → finds "Sales_Nov_2024.xlsx" → 
reads content → provides analysis with actual data
```

### Disabling Path Search

If you want to ask a question WITHOUT using configured paths:

- The feature is enabled by default
- Future versions may add a toggle switch in the UI

## Technical Details

### File Storage

Path configurations are saved in:
```
data/path_config.json
```

### Configuration Structure

Each path configuration contains:
```json
{
  "id": 0,
  "name": "Sales Reports",
  "location": "/Users/username/Documents/Reports",
  "description": "Monthly sales data and analytics",
  "type": "folder",
  "added_at": "2024-12-10T10:30:00",
  "file_count": 15,
  "last_scanned": "2024-12-10T10:35:00",
  "file_types": {
    ".xlsx": 10,
    ".pdf": 3,
    ".docx": 2
  },
  "total_size": 2456789
}
```

### Supported File Types

The AI can process files from configured paths:

| Type | Extensions | Capabilities |
|------|-----------|--------------|
| PDF | `.pdf` | Text extraction, table detection |
| Excel | `.xlsx`, `.xls` | Data reading, sheet extraction |
| Word | `.docx` | Text extraction, formatting |
| CSV | `.csv` | Data parsing, analysis |
| Text | `.txt`, `.md` | Direct reading |
| Images | `.jpg`, `.png` | OCR text extraction |

### API Endpoints

The feature uses these REST endpoints:

- `GET /ai-chat/paths` - List all configured paths
- `POST /ai-chat/paths` - Add new path
- `DELETE /ai-chat/paths/<id>` - Remove path
- `POST /ai-chat/paths/<id>/scan` - Scan path for files
- `GET /ai-chat/paths/<id>/files` - Get file list
- `GET /ai-chat/paths/search` - Search files across paths

### File Search Algorithm

When you ask a question:

1. **Keyword Extraction**: AI identifies key terms from your question
2. **Path Search**: Searches filenames in all configured paths
3. **Relevance Ranking**: Ranks files by relevance to question
4. **Content Extraction**: Reads top 5 most relevant files
5. **Context Building**: Combines file content with your question
6. **AI Response**: Generates answer using all available context

### Performance Considerations

- **File Limit**: Up to 5 files per question (most relevant)
- **Content Limit**: 2000 characters per file (prevents context overflow)
- **Scan Speed**: Folder scans are fast (metadata only)
- **Search Speed**: Filename search is instant

## Use Cases

### 1. Business Analytics
**Scenario**: Analyze sales reports without manual uploads

```
Configure Path: "/Users/john/Documents/Sales Reports"
Ask: "What's the trend in Q4 sales?"
Result: AI reads latest Excel files and provides trend analysis
```

### 2. Document Management
**Scenario**: Get insights from policy documents

```
Configure Path: "/Users/sarah/Company/Policies"
Ask: "What's our remote work policy?"
Result: AI searches PDFs and extracts relevant policy info
```

### 3. Data Analysis
**Scenario**: Analyze inventory data

```
Configure Path: "/Users/mike/Inventory/Data"
Ask: "Which products are low in stock?"
Result: AI reads CSV/Excel files and identifies low stock items
```

### 4. Research & Learning
**Scenario**: Study from local notes and papers

```
Configure Path: "/Users/emma/Research/AI Papers"
Ask: "Summarize recent findings on LLMs"
Result: AI reads PDF papers and provides summary
```

## Troubleshooting

### Path Not Found Error

**Problem**: "Path does not exist" error when adding

**Solutions**:
- Verify the full path is correct
- Check folder/file actually exists
- Use absolute path (starting with `/` on Mac/Linux, `C:\` on Windows)
- Avoid relative paths like `./folder` or `../documents`

### No Files Found

**Problem**: Scan shows 0 files

**Solutions**:
- Check folder isn't empty
- Verify you have read permissions
- Ensure files have supported extensions
- Refresh scan after adding new files

### AI Not Using Path Files

**Problem**: AI doesn't include file content in responses

**Solutions**:
- Verify paths are configured (click settings icon)
- Check files match your question keywords
- Try using specific filenames in your question
- Scan paths to ensure file count is updated

### Scan Taking Too Long

**Problem**: Folder scan seems stuck

**Solutions**:
- Large folders (1000+ files) take longer
- Network drives may be slow
- Close and retry
- Consider configuring specific subfolders instead

## Best Practices

### 1. Organize Paths by Topic
✅ **Good**:
- "Sales Q4 2024"
- "Inventory November"
- "Customer Feedback"

❌ **Avoid**:
- "Documents"
- "Files"
- "Data"

### 2. Use Descriptive Names
✅ **Good**: "Monthly Sales Reports - 2024"
❌ **Avoid**: "Folder1"

### 3. Keep Paths Focused
✅ **Good**: Configure specific project folders
❌ **Avoid**: Entire "Documents" or "Desktop" folder

### 4. Regular Scans
- Scan paths after adding new files
- Weekly scans for active folders
- Delete outdated path configurations

### 5. File Organization
- Use clear filenames
- Include dates in filenames (YYYY-MM-DD format)
- Group related files in subfolders
- Remove obsolete files regularly

## Security & Privacy

### Data Privacy
- **Local Only**: Files never leave your computer
- **No Upload**: Path files aren't uploaded to cloud
- **Secure Processing**: Files processed in memory only
- **No Storage**: File content not saved by application

### Permissions
- **Read-Only**: Application only reads files
- **No Modifications**: Files are never altered
- **User Control**: You control which paths are accessible

### Access Control
- Application uses your user permissions
- Cannot access files you don't have permission for
- Network drives require proper authentication
- External drives must be mounted

## Future Enhancements

Planned features for future releases:

- [ ] Toggle switch to enable/disable path search per question
- [ ] File preview in path configuration modal
- [ ] Recent files quick access
- [ ] File type filtering in UI
- [ ] Path templates for common scenarios
- [ ] Batch path import/export
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Automatic file change detection
- [ ] Advanced search with regex patterns
- [ ] File content indexing for faster search

## Support

For issues or questions:
- Check troubleshooting section above
- Review application logs in `logs/` folder
- Create GitHub issue with details
- Contact support with error messages

## Version History

### v1.0.0 (Current)
- Initial release
- Basic path configuration (add/remove)
- File scanning and counting
- Search integration with AI chat
- Support for common file types
- JSON-based persistence

---

**Last Updated**: December 10, 2024
**Feature Status**: ✅ Production Ready
