# File Upload and Export Feature

## Overview
The AI Chat interface now supports file attachments and response exports, enabling users to:
- Upload multiple files (images, PDFs, Excel, text, DOCX) for AI analysis
- Get context-aware responses based on uploaded file content
- Export AI insights and recommendations as PDF or DOCX

## Features

### 1. File Upload
**Location:** AI Chat interface (`http://localhost:8000/ai-chat/`)

**Supported File Types:**
- **Images:** JPG, JPEG, PNG, GIF
- **Documents:** PDF, DOCX, DOC, TXT
- **Spreadsheets:** XLSX, XLS, CSV

**How to Use:**
1. Click the **+** button next to the message input
2. Select one or multiple files
3. Files appear as chips showing icon, name, and size
4. Click × on any chip to remove a file
5. Type your question and click Send
6. AI will analyze file content and respond accordingly

**UI Components:**
- **+ Button:** Circular button with hover animation (rotates 45°)
- **File Chips:** Display attached files with icons:
  - 📄 PDF files
  - 📊 Excel/CSV files
  - 📝 Text/DOCX files
  - 🖼️ Image files
- **Remove Button:** × icon on each chip to remove files

### 2. File Processing
**Backend:** `/ai-chat/upload` endpoint

**Processing Workflow:**
1. Files uploaded via multipart/form-data
2. Each file processed based on type:
   - **PDF:** Text extracted using PyPDF2
   - **DOCX:** Paragraphs and tables extracted using python-docx
   - **Excel/CSV:** Data summary with pandas (rows, columns, preview)
   - **Text:** Direct UTF-8/latin-1 decoding
   - **Images:** Metadata extraction (OCR placeholder for future)
3. Extracted content sent to Gemini AI as context
4. AI response incorporates file insights

**File Size Limits:**
- Each file: First 2000 characters used for context
- Multiple files: All files processed and combined
- Large files: Automatically truncated with indicator

### 3. AI Integration
**Enhanced Prompt:**
```
**Attached Files:**

**File: sales_report.xlsx** (Type: xlsx)
Data Summary: 100 rows × 5 columns
Columns: Month, Sales, Revenue, Profit, Growth
[Data preview...]

**User Question:** What are the key trends in this sales data?
```

**AI Response:**
- Gemini reads file content
- Analyzes data/text/images
- Provides insights based on file context
- References specific data points from files

### 4. Export Functionality
**Location:** Export buttons appear after each AI response

**Export Formats:**
- **📄 PDF:** Formatted PDF with V-Mart branding
- **📝 DOCX:** Word document with styled content

**Export Features:**
- **Title:** "V-Mart AI Insights & Recommendations"
- **Metadata:** Generation timestamp, store ID (if applicable)
- **Content:** 
  - Formatted headings (bold, colored)
  - Paragraphs with proper spacing
  - Clean HTML-to-text conversion
- **Footer:** "Powered by V-Mart AI | Developed by DSR | Inspired by LA"

**Export Styling:**
- **PDF:**
  - Purple gradient colors (#667eea, #764ba2)
  - 11pt Helvetica font
  - Professional formatting
  - Page size: US Letter
  
- **DOCX:**
  - Colored headings (purple theme)
  - Centered title
  - 11pt body text
  - Proper spacing and margins

### 5. Technical Implementation

**New Files:**
1. **src/utils/file_processor.py** (309 lines)
   - `extract_pdf_text()`: PyPDF2 text extraction
   - `extract_docx_text()`: python-docx paragraph/table extraction
   - `extract_excel_data()`: pandas CSV/Excel parsing
   - `extract_text_file()`: UTF-8/latin-1 text decoding
   - `extract_image_text()`: Image metadata (OCR placeholder)
   - `process_uploaded_file()`: Main processor dispatcher

2. **src/utils/export_generator.py** (217 lines)
   - `generate_pdf()`: reportlab PDF generation
   - `generate_docx()`: python-docx DOCX generation
   - `clean_html_tags()`: HTML tag removal utility

**Modified Files:**
1. **src/web/templates/ai_chat.html**
   - Added file upload button and input
   - File chip display area
   - Export buttons CSS styling
   - JavaScript file handling functions:
     - `handleFileSelect()`: Process selected files
     - `displayAttachedFiles()`: Show file chips
     - `removeFile()`: Remove attached file
     - `uploadFiles()`: Upload to server
     - `exportToPDF()`: Download PDF export
     - `exportToDOCX()`: Download DOCX export
   - Updated `sendMessage()`: Include file uploads
   - Updated `addMessage()`: Add export buttons

2. **src/web/ai_chat_routes.py**
   - **POST /ai-chat/upload**: File upload handler
   - **POST /ai-chat/export-pdf**: PDF generation endpoint
   - **POST /ai-chat/export-docx**: DOCX generation endpoint
   - **Modified /ai-chat/ask-stream**: Accept file_context parameter

**Dependencies (Already Installed):**
```
PyPDF2==3.0.1          # PDF text extraction
python-docx            # DOCX read/write
openpyxl==3.1.5        # Excel file handling
pillow==12.0.0         # Image processing
reportlab==4.4.4       # PDF generation
pandas                 # CSV/Excel data analysis
```

### 6. Usage Examples

**Example 1: Upload Sales Data Excel**
1. Attach `monthly_sales.xlsx`
2. Ask: "What are the top performing months?"
3. AI analyzes Excel data and provides insights
4. Export analysis as PDF for reporting

**Example 2: Upload Product Images**
1. Attach multiple product images
2. Ask: "Analyze these product images"
3. AI provides visual analysis (via Gemini Vision)
4. Export recommendations as DOCX

**Example 3: Upload PDF Report**
1. Attach `competitor_analysis.pdf`
2. Ask: "Summarize key findings from this report"
3. AI extracts and summarizes PDF content
4. Export summary as PDF or DOCX

### 7. Error Handling
- **No files uploaded:** Graceful handling, continues without file context
- **Unsupported file type:** Error message in file chip
- **Processing failure:** Warning message, continues with other files
- **Export failure:** Alert message with error details
- **Missing dependencies:** Informative error messages

### 8. UI/UX Enhancements
- **Smooth animations:** Button hover effects, chip transitions
- **Progress indicators:** File upload progress, "Processing files..." message
- **Clear feedback:** Success messages, file count display
- **Accessibility:** Button titles, keyboard support
- **Mobile responsive:** File chips wrap, buttons scale

### 9. Security Considerations
- File validation on backend
- File size limits enforced
- Content truncation for large files
- Safe file type checking
- No file storage (processed in-memory)

### 10. Future Enhancements
- Image OCR text extraction (pytesseract integration)
- Google Sheets direct integration
- File preview modal
- Batch file operations
- Custom export templates
- Export format options (font, color themes)
- File upload progress bars
- Drag-and-drop file upload

## Testing Checklist
- [x] Upload single PDF file
- [x] Upload multiple files (mixed types)
- [x] Remove attached file before sending
- [x] Send message with files
- [x] Verify AI reads file content
- [x] Export response as PDF
- [x] Export response as DOCX
- [x] Test unsupported file type
- [x] Test large file handling
- [x] Test with no files attached

## Commit Information
**Commit Hash:** a05f973  
**Branch:** main  
**Date:** 2024  
**Message:** Add file upload and export functionality to AI Chat

**Files Changed:**
- 4 files changed
- 986 insertions(+)
- 6 deletions(-)
- 2 new files created

## Repository
**GitHub:** https://github.com/ds25041974/V-Mart-Personal-AI-Agent  
**Branch:** main  
**Status:** Successfully pushed

---

**Developed by:** DSR  
**Inspired by:** LA  
**Powered by:** Gemini AI  
**Date:** December 2024
