# Smart Response System

## Overview
The V-Mart AI Agent now features an intelligent context-aware response system that only analyzes files and sources when relevant to your question.

## How It Works

### 1. **Simple Greetings** → Natural Conversation
When you say simple greetings or acknowledgments, the AI responds naturally without analyzing files.

**Examples:**
- "Hi" → Just greets you back
- "Hello" → Friendly greeting response
- "Thank you" → Acknowledges appreciation
- "Good morning" → Responds appropriately
- "How are you?" → Natural conversation

**Detected Greetings:**
- hi, hello, hey
- good morning, good afternoon, good evening
- how are you, what's up
- thanks, thank you
- ok, okay, yes, no, sure
- bye, goodbye

### 2. **File Questions** → Analyzes Browsed File
When you upload a file AND ask about it, the AI analyzes that specific file.

**Examples:**
- "Summarize this file" ✅ Analyzes browsed file
- "What does this document contain?" ✅ Analyzes browsed file
- "Show me the data in this PDF" ✅ Analyzes browsed file
- "Explain the content" ✅ Analyzes browsed file

**File Question Keywords:**
- this file, the file, document, pdf
- analyze, summary, summarize
- what does, explain, show me
- find, search, look for, contains
- about this, in this, from this

### 3. **General Questions** → Normal AI Response
Even if you have a file browsed, if you ask something unrelated, the AI responds normally WITHOUT forcing file context.

**Examples with file browsed:**
- "What is machine learning?" → Normal explanation (ignores file)
- "How do I cook pasta?" → Normal answer (ignores file)
- "What's the weather like?" → General response (ignores file)

### 4. **Comparison Requests** → Multi-Source Analysis
When you want to compare files, the AI analyzes both browsed and local files.

**Examples:**
- "Compare this with my local report" ✅ Compares browsed + local
- "Difference between this and system file" ✅ Compares both
- "Match this versus my data" ✅ Compares both

**Comparison Keywords:**
- compare, difference, diff
- versus, vs, match, similar

### 5. **Explicit File Search** → Searches Local/Cloud
When you explicitly ask to find or search files, the AI searches your sources.

**Examples:**
- "Find my sales report" ✅ Searches local files
- "Search for Q3 data file" ✅ Searches local files
- "Open my progress document" ✅ Searches local files
- "Get my email from John" ✅ Searches email (with OAuth)

**Search Triggers:**
Must have action words (find, search, open, get, read) + file keywords

### 6. **Connector Sources** → Shows Availability
When you mention specific sources, the AI explains their availability.

**Examples:**
- "Check my Gmail" → Shows OAuth requirement
- "Search Google Drive" → Shows OAuth requirement
- "Capture my screen" → Shows pending implementation

## Priority System

The AI follows this priority when responding:

```
1. Is it a simple greeting?
   ↓ YES → Respond naturally, ignore files
   ↓ NO
   
2. Is a file browsed?
   ↓ YES → Is the question about the file?
      ↓ YES → Analyze browsed file
      ↓ NO → Respond normally, ignore file
   ↓ NO
   
3. Is user explicitly asking for files?
   ↓ YES → Search local/cloud sources
   ↓ NO → Normal AI response
```

## Examples by Scenario

### Scenario 1: Just Chatting (No Files)
```
User: "Hi"
AI: "Hello! How can I help you today?"

User: "What is Python?"
AI: "Python is a high-level programming language..."
```

### Scenario 2: File Browsed + Relevant Question
```
User: [Browses "Sales_Report.pdf"]
User: "Summarize this file"
AI: [Analyzes Sales_Report.pdf and provides summary]

User: "What are the key insights?"
AI: [Provides insights from Sales_Report.pdf]
```

### Scenario 3: File Browsed + Unrelated Question
```
User: [Browses "Sales_Report.pdf"]
User: "What is artificial intelligence?"
AI: "Artificial intelligence is..." [Ignores the PDF]

User: "Hi"
AI: "Hello! How can I help?" [Ignores the PDF]
```

### Scenario 4: Comparison Request
```
User: [Browses "Week_31_Sales.pdf"]
User: "Compare this with my local week 30 sales data"
AI: [Analyzes browsed PDF + searches local files + compares both]
```

### Scenario 5: Explicit File Search
```
User: "Find my progress report from last month"
AI: [Searches ~/Documents, ~/Desktop, ~/Downloads for matching files]

User: "Search my email for invoice from vendor"
AI: [Requires Gmail OAuth, shows authentication link]
```

## Benefits

✅ **Natural Conversations**: Greetings don't trigger unnecessary file analysis
✅ **Context-Aware**: Only analyzes files when relevant to your question
✅ **Smart Detection**: Understands intent behind your queries
✅ **No Forced Context**: Doesn't force file context on unrelated questions
✅ **Efficient**: Reduces unnecessary API calls and processing time
✅ **Better UX**: Faster responses for simple queries

## Technical Implementation

### Detection Logic

```python
# 1. Greeting Detection
greetings = ["hi", "hello", "hey", "good morning", ...]
is_simple_greeting = prompt_lower in greetings

# 2. File Question Detection
file_keywords = ["this file", "document", "analyze", "summary", ...]
asking_about_file = any(keyword in prompt_lower for keyword in file_keywords)

# 3. Explicit Search Detection
should_search = (
    "find file" in prompt_lower or
    "search file" in prompt_lower or
    ("document" in prompt_lower and "show" in prompt_lower)
)
```

### Response Flow

```python
if is_simple_greeting:
    return natural_response()
    
elif browsed_file and asking_about_file:
    return analyze_browsed_file()
    
elif browsed_file and not asking_about_file:
    return normal_response()  # Ignore file
    
elif should_search_files:
    return search_and_analyze()
    
else:
    return normal_response()
```

## Configuration

All detection keywords are configurable in `src/web/app.py`:

```python
# Greeting detection
greetings = ["hi", "hello", "hey", ...]

# File question detection
file_question_keywords = ["this file", "document", ...]

# Search triggers
keywords_local = ["local file", "my file", ...]
```

## Future Enhancements

🔄 **Learning System**: AI learns your patterns over time
🎯 **Intent Classification**: More sophisticated NLP-based intent detection
🔍 **Smart Suggestions**: Suggests relevant files based on conversation
📊 **Context History**: Remembers which files you frequently use

---

**Last Updated**: November 10, 2025
**V-Mart AI Agent Version**: 1.0
**Developed by**: DSR | Inspired by: LA | Powered by: Gemini AI
