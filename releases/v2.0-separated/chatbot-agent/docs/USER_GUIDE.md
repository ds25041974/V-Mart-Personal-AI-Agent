# 📖 V-Mart AI Agent - User Guide

**Developed by: DSR | Inspired by: LA | Powered by: Gemini AI**

Complete guide to using the V-Mart Personal AI Agent.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Interface Overview](#interface-overview)
- [Chat Features](#chat-features)
- [Document Search](#document-search)
- [Data Analysis](#data-analysis)
- [File Management](#file-management)
- [Decision Support](#decision-support)
- [Advanced Features](#advanced-features)
- [Tips & Best Practices](#tips--best-practices)

---

## 🚀 Getting Started

### Accessing the Application

1. **Start the server:**
   ```bash
   python main.py  # or python3 main.py on macOS/Linux
   ```

2. **Open in browser:**
   - Local: http://localhost:8000
   - Network: http://YOUR_IP:8000

3. **Login:**
   - **Quick Start:** Click "Demo Login" (no credentials needed)
   - **Full Access:** Click "Login with Google" (requires OAuth setup)

### Home Screen

After logging in, you'll see:
- **Header:** App name and credits
- **Welcome message:** Shows your name
- **Four main tabs:** Chat, Analysis, Files, Decision Support
- **Footer:** Development credits

---

## 🎨 Interface Overview

### Navigation Tabs

#### 💬 Chat Tab (Default)
- Real-time conversation with AI
- Document-aware responses
- Context retention
- Multi-turn conversations

#### 📊 Analysis Tab
- Data analysis tools
- Financial analysis
- Sales metrics
- Inventory insights

#### 📁 Files Tab
- Local file browser
- Document search
- File content preview
- Quick access to recent files

#### 🎯 Decision Support Tab
- Compare multiple options
- Pros/cons analysis
- Recommendation engine
- Strategic planning assistance

### Responsive Design

The interface adapts to your device:
- **Desktop (1024px+):** Full layout with sidebar
- **Tablet (768-1024px):** Optimized grid layout
- **Mobile (<768px):** Stacked, touch-friendly layout

---

## 💬 Chat Features

### Basic Chat

1. **Type your message** in the text box
2. **Press Enter** or click "Send"
3. **Wait for response** (usually 2-5 seconds)
4. **Continue conversation** - AI remembers context

### Example Conversations

**General Questions:**
```
You: What is V-Mart?
AI: V-Mart is a retail company...

You: Tell me about artificial intelligence
AI: Artificial Intelligence (AI) is...
```

**Follow-up Questions:**
```
You: What's the weather like?
AI: I don't have real-time weather data, but...

You: Can you write me a poem?
AI: Of course! Here's a poem for you...
```

### Chat Controls

- **Clear History:** Removes all messages (fresh start)
- **Scroll:** Auto-scrolls to latest message
- **Copy Text:** Select and copy AI responses

### Keyboard Shortcuts

- `Enter`: Send message
- `Shift + Enter`: New line in message
- `Ctrl/Cmd + A`: Select all text

---

## 📁 Document Search

**The AI can search and analyze your local documents!**

### Supported Document Types

✅ **Office Documents:**
- Microsoft Word (.doc, .docx)
- Excel spreadsheets (.xlsx, .xls)
- PowerPoint presentations (.ppt, .pptx)

✅ **PDF Files:**
- PDF documents (.pdf)

✅ **Text Files:**
- Plain text (.txt)
- Markdown (.md)
- CSV files (.csv)
- Rich text (.rtf)

### Searchable Locations

The AI automatically scans:
- 📂 **Documents folder** (`~/Documents`)
- 🖥️ **Desktop** (`~/Desktop`)
- ⬇️ **Downloads** (`~/Downloads`)

### How to Search Documents

#### Automatic Search (Recommended)

Just ask naturally! The AI detects document-related keywords:

```
You: Show me my progress reports
AI: [Searches Documents/Desktop/Downloads]
    📁 Found 5 documents...
    1. Q4_Progress_Report.pdf
    2. Annual_Progress_2024.docx
    ...

You: Find my sales spreadsheet
AI: [Searches for Excel files with "sales"]
    Found: Sales_Data_Q4.xlsx, Monthly_Sales.xlsx

You: What's in my presentation about marketing?
AI: [Searches for PowerPoint files]
    Found: Marketing_Strategy.pptx...
```

#### Trigger Keywords

These words activate document search:
- **Documents:** document, doc, file, pdf
- **Spreadsheets:** sheet, excel, spreadsheet, xlsx
- **Presentations:** slide, presentation, ppt, powerpoint
- **Locations:** desktop, downloads, documents, local, computer
- **Actions:** find, search, show, locate
- **Data:** progress, report, status, results, data, analysis

### Document Search Examples

**Example 1: Progress Reports**
```
You: Summarize my progress reports
AI: 📚 Sources: Found 3 documents in local system

    📁 AVAILABLE DOCUMENTS:
    1. Q4_Progress_Report.pdf
       Location: Documents
       Size: 245.3 KB
       
    2. Team_Progress_Nov.docx
       Location: Desktop
       Size: 89.2 KB
       
    Based on these documents, your Q4 progress shows...
```

**Example 2: Spreadsheet Analysis**
```
You: What data is in my sales spreadsheet?
AI: Found: Sales_Analysis_2024.xlsx
    
    This spreadsheet contains sales data with metrics 
    including revenue, units sold, and regional breakdown...
```

**Example 3: Find Recent Files**
```
You: Show me my recent documents
AI: Here are your 8 most recent documents:
    
    1. Meeting_Notes.docx (Modified: Nov 8, 2024)
    2. Budget_2024.xlsx (Modified: Nov 7, 2024)
    3. Proposal.pdf (Modified: Nov 6, 2024)
    ...
```

### Document Preview

For text files (.txt, .md, .csv), the AI shows content previews:

```
File: Project_Notes.txt
Preview: "Meeting with team on Nov 8. Discussed Q4 
goals and new product launch strategy. Action items: 
1. Review budget 2. Schedule follow-up..."
```

### Search Results

Each result shows:
- **File name**
- **Location** (Documents/Desktop/Downloads)
- **File size** in KB
- **Directory path**
- **Content preview** (for text files)
- **Last modified date** (sorted by newest first)

### Limitations

⚠️ **Current Limitations:**
- **Max depth:** 2 folder levels
- **Max results:** 8 most recent documents
- **Text preview:** Only for .txt, .md, .csv files
- **Binary files:** PDF/Office files show metadata only

📧 **Email & Cloud Storage:**
- Gmail search requires Google OAuth setup
- Google Drive requires OAuth setup
- See: `docs/GOOGLE_OAUTH_SETUP.md`

---

## 📊 Data Analysis

### Using the Analysis Tab

1. **Switch to Analysis tab**
2. **Select analysis type:**
   - General Analysis
   - Financial Analysis
   - Sales Analysis
   - Inventory Analysis

3. **Paste your data**
4. **Click "Analyze"**
5. **Review results**

### Analysis Types

#### General Analysis
- Pattern detection
- Trend identification
- Summary statistics
- Insights and recommendations

#### Financial Analysis
- Revenue trends
- Profit margins
- Cost analysis
- Financial health indicators

#### Sales Analysis
- Sales performance
- Top products/regions
- Growth rates
- Seasonal patterns

#### Inventory Analysis
- Stock levels
- Turnover rates
- Reorder points
- Inventory optimization

### Example: Sales Data

**Input:**
```csv
Month,Revenue,Units
Jan,50000,500
Feb,55000,550
Mar,60000,600
```

**Click Analyze** → AI provides:
- Revenue trend: +20% growth
- Average units per month: 550
- Recommendations for Q2
- Forecasts and insights

---

## 📂 File Management

### File Search

1. Go to **Files tab**
2. Enter search term in search box
3. Click **"Search"**
4. View results list

### Reading Files

1. Click on any file in the results
2. File content appears below
3. Supports text files, code files, markdown

### File Information

Results show:
- File path
- File size
- Last modified
- File type

---

## 🎯 Decision Support

### Making Better Decisions

1. **Go to Decision Support tab**
2. **Enter decision title:**
   ```
   Example: "Choose Marketing Platform"
   ```

3. **Add context:**
   ```
   We need a platform for social media management.
   Budget: $500/month
   Team size: 5 people
   ```

4. **List options:**
   - Option 1: Hootsuite
   - Option 2: Buffer
   - Option 3: Sprout Social
   
   Click "+ Add Option" for more

5. **Click "Analyze Decision"**

### Analysis Results

The AI provides:
- ✅ **Pros** for each option
- ❌ **Cons** for each option
- 💰 **Cost comparison**
- 🏆 **Recommendation**
- 📝 **Additional considerations**

### Example Decision

**Title:** "Hire Developer or Outsource?"

**Context:** "Need to build mobile app. Timeline: 3 months. Budget: $50k."

**Options:**
1. Hire full-time developer
2. Use freelance developers
3. Outsource to agency

**AI Analysis:**
```
Recommendation: Outsource to Agency

Reasoning:
- ✅ Fastest timeline (agencies have teams)
- ✅ Within budget
- ✅ No long-term commitment
- ⚠️ Less control over process
- 💡 Suggestion: Hire developer after app launch
```

---

## 🔧 Advanced Features

### Context Management

The AI remembers conversation history:
```
You: What's 2+2?
AI: 4

You: Multiply that by 3
AI: 12 (remembering previous answer)

You: What was my first question?
AI: You asked "What's 2+2?"
```

### Multi-turn Conversations

Build on previous responses:
```
You: Explain machine learning
AI: [Detailed explanation]

You: Give me an example
AI: [Provides example based on previous explanation]

You: How would I implement that?
AI: [Implementation steps]
```

### Clear History

Start fresh conversation:
1. Click **"Clear History"** button
2. All previous messages removed
3. AI forgets context
4. New conversation begins

---

## 💡 Tips & Best Practices

### Getting Better Responses

#### ✅ Do:
- **Be specific:** "Find my Q4 sales report" vs "find file"
- **Provide context:** "I need help with Python code for data analysis"
- **Ask follow-ups:** Build on previous answers
- **Use natural language:** Talk normally, no special commands

#### ❌ Don't:
- Avoid vague questions: "help me"
- Don't ask multiple unrelated questions at once
- Don't expect real-time data (weather, stocks, etc.)
- Don't share sensitive personal information

### Document Search Tips

1. **Use descriptive file names:**
   ```
   ✅ Q4_Sales_Report_2024.xlsx
   ❌ document1.xlsx
   ```

2. **Organize by folders:**
   ```
   Documents/
     Reports/
       Sales/
       Marketing/
     Projects/
   ```

3. **Keywords in questions:**
   ```
   ✅ "Find my presentation about marketing strategy"
   ✅ "Show me Excel files with budget data"
   ❌ "Where's that thing?"
   ```

4. **Be specific about location:**
   ```
   "Find reports on my desktop"
   "Search downloads for PDFs"
   ```

### Performance Tips

1. **Faster responses:**
   - Keep questions concise
   - Clear chat history when switching topics
   - Close unused browser tabs

2. **Better search results:**
   - Organize files in Documents/Desktop/Downloads
   - Use meaningful file names
   - Keep folder structure shallow (2 levels max)

3. **Network access:**
   - For mobile access, use http://YOUR_IP:8000
   - Ensure firewall allows port 8000
   - Same WiFi network required

---

## 🔐 Privacy & Security

### Data Handling

- ✅ **Local processing:** Files scanned locally
- ✅ **No uploads:** Documents stay on your computer
- ✅ **Metadata only:** Only file names/paths sent to AI
- ⚠️ **Content previews:** Text file previews included in prompts
- 🔒 **API calls:** Queries sent to Gemini AI for processing

### What's Shared

**Sent to AI:**
- Your questions/prompts
- File names and metadata
- Text file previews (first 200 chars)
- Conversation history

**NOT sent to AI:**
- Full document contents (PDF, Office files)
- Your files themselves
- File system structure
- Other private data

### Security Best Practices

1. **Don't share:**
   - Passwords
   - Credit card numbers
   - Social security numbers
   - Private API keys

2. **Do use:**
   - Demo mode for testing
   - OAuth for production
   - Strong passwords for Google account
   - HTTPS in production

---

## 📱 Mobile Usage

### Access from Phone/Tablet

1. **Find your computer's IP:**
   - See SETUP_GUIDE.md for instructions

2. **Open browser on mobile device**

3. **Navigate to:**
   ```
   http://YOUR_IP:8000
   Example: http://192.168.1.100:8000
   ```

4. **Use normally:**
   - Touch-optimized interface
   - All features available
   - Same functionality

### Mobile Tips

- Use **portrait mode** for chat
- Use **landscape mode** for analysis
- **Larger buttons** for touch
- **Swipe** to scroll through messages

---

## ❓ Common Questions

### Q: Can I use this offline?
**A:** No, internet required for AI API calls.

### Q: Does it read my document contents?
**A:** Only metadata for PDF/Office files. Text files show 200-char preview.

### Q: How do I access Gmail/Drive?
**A:** Set up Google OAuth (see GOOGLE_OAUTH_SETUP.md).

### Q: Can I change the port?
**A:** Yes, edit `PORT=8000` in `.env` file.

### Q: Is my data private?
**A:** Queries sent to Gemini AI. See Privacy section above.

### Q: Can I customize responses?
**A:** Not directly, but context and phrasing affect results.

### Q: Does it work on tablets?
**A:** Yes! Responsive design works on all devices.

### Q: How do I update the app?
**A:** Run `git pull` and restart the server.

---

## 🆘 Troubleshooting

### AI Not Finding Documents

1. Check file is in Documents/Desktop/Downloads
2. Use specific keywords in question
3. Verify file has supported extension
4. Try exact file name in question

### Search Too Slow

1. Reduce folder depth
2. Move files to top-level folders
3. Clear browser cache
4. Restart server

### Can't Access from Mobile

1. Verify same WiFi network
2. Check firewall settings
3. Use correct IP address
4. Try http://IP:8000 (not https)

### Server Not Starting

1. Check `.env` file exists
2. Verify API key is valid
3. Ensure port not in use
4. Check Python version (3.8+)

---

## 📚 Additional Resources

- **Setup Guide:** `docs/SETUP_GUIDE.md`
- **OAuth Setup:** `docs/GOOGLE_OAUTH_SETUP.md`
- **Document Search:** `DOCUMENT_SEARCH_FEATURE.md`
- **Quick Setup:** `QUICK_SETUP.md`

---

## 🎓 Learning Resources

### Getting Started
1. Start with simple questions
2. Try document search with your files
3. Experiment with analysis tools
4. Test decision support

### Advanced Usage
1. Set up Google OAuth
2. Configure custom folders
3. Integrate with workflows
4. Automate with scripts

---

**Ready to get started? Try asking: "Show me my documents" or "Help me analyze sales data"**

**Developed by: DSR | Inspired by: LA | Powered by: Gemini AI**
