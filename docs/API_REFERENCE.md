# V-Mart AI Agent - API Reference

Complete documentation for the V-Mart Personal AI Agent REST API.

## Table of Contents

1. [Authentication](#authentication)
2. [Chat Endpoints](#chat-endpoints)
3. [Analysis Endpoints](#analysis-endpoints)
4. [File Management Endpoints](#file-management-endpoints)
5. [Scheduler Endpoints](#scheduler-endpoints)
6. [Utility Endpoints](#utility-endpoints)
7. [Error Handling](#error-handling)
8. [Rate Limits](#rate-limits)

---

## Base URL

```
http://localhost:5000
```

For production deployments, replace with your actual domain.

---

## Authentication

All API endpoints (except `/login`, `/authorize`, `/logout`) require authentication via session cookies.

### Login Flow

#### 1. Initiate Login

```http
GET /login
```

**Response**: Redirects to Google OAuth consent screen

---

#### 2. OAuth Callback

```http
GET /authorize?code={authorization_code}&state={state}
```

**Parameters**:
- `code` (string): Authorization code from Google
- `state` (string): CSRF protection token

**Response**: Redirects to `/` with session cookie set

**Error Responses**:
- `403 Forbidden`: Domain not in allowed list
- `401 Unauthorized`: Authentication failed

---

#### 3. Logout

```http
GET /logout
```

**Response**: Redirects to `/` with session cleared

---

## Chat Endpoints

### Ask Question

Send a question or prompt to the AI agent.

```http
POST /ask
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "What are the key sales trends for Q4?",
  "context": "Looking at retail data" // Optional
}
```

**Response**:
```json
{
  "response": "Based on the Q4 data analysis, here are the key trends:\n1. Electronics sales increased by 23%\n2. Fashion saw a 15% decline\n3. Home goods remained stable..."
}
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Not logged in
- `500 Internal Server Error`: Processing error

**Example**:
```javascript
fetch('/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "Summarize our inventory status",
    context: "Focus on high-value items"
  })
})
.then(res => res.json())
.then(data => console.log(data.response));
```

---

### Clear Conversation History

Clear the conversation history for the current session.

```http
POST /clear-history
```

**Response**:
```json
{
  "status": "success",
  "message": "Conversation history cleared"
}
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Not logged in

---

## Analysis Endpoints

### Analyze Data

Perform AI-powered data analysis.

```http
POST /analyze
Content-Type: application/json
```

**Request Body**:
```json
{
  "data": "Product,Sales,Profit\nLaptop,150000,45000\nMouse,5000,2000",
  "analysis_type": "financial" // Options: general, financial, sales, inventory
}
```

**Response**:
```json
{
  "analysis": {
    "insights": [
      "Laptops show high profitability with 30% margin",
      "Mice have a 40% margin but lower absolute profit"
    ],
    "recommendations": [
      "Increase laptop inventory for upcoming season",
      "Bundle accessories with high-margin items"
    ],
    "key_metrics": {
      "total_sales": "155000",
      "total_profit": "47000",
      "average_margin": "30.3%"
    }
  }
}
```

**Analysis Types**:

| Type | Description |
|------|-------------|
| `general` | Overall insights and patterns |
| `financial` | Profitability, trends, financial health |
| `sales` | Sales patterns, trends, forecasts |
| `inventory` | Stock levels, turnover analysis |

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Missing or invalid data
- `401 Unauthorized`: Not logged in
- `500 Internal Server Error`: Analysis error

---

### Reasoning Task

Get step-by-step reasoning for complex problems.

```http
POST /reasoning
Content-Type: application/json
```

**Request Body**:
```json
{
  "task": "How should we optimize our supply chain to reduce costs by 15%?"
}
```

**Response**:
```json
{
  "reasoning": {
    "steps": [
      "Analyze current supply chain costs",
      "Identify high-cost areas (transportation, warehousing, inventory)",
      "Evaluate vendor contracts and negotiate better rates",
      "Consider consolidation of shipments",
      "Implement just-in-time inventory practices"
    ],
    "conclusion": "By renegotiating vendor contracts (5% savings), consolidating shipments (7% savings), and optimizing inventory (3% savings), you can achieve a 15% cost reduction."
  }
}
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Missing task description
- `401 Unauthorized`: Not logged in

---

### Summarize Document

Create summaries of documents or text.

```http
POST /summarize
Content-Type: application/json
```

**Request Body**:
```json
{
  "text": "Long document text here...",
  "summary_type": "executive" // Options: brief, detailed, executive
}
```

**Response**:
```json
{
  "summary": "Executive Summary:\n\nKey Points:\n- Revenue increased 12% YoY\n- Customer acquisition cost decreased by 8%\n- New markets show promising growth\n\nRecommendations:\n- Continue expansion in tier-2 cities\n- Invest in digital marketing"
}
```

**Summary Types**:

| Type | Description |
|------|-------------|
| `brief` | 2-3 sentences |
| `detailed` | Comprehensive summary |
| `executive` | Executive summary with key points |

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Missing text
- `401 Unauthorized`: Not logged in

---

### Decision Support

Get AI-powered decision analysis with pros/cons.

```http
POST /decision-support
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Should we expand to Tier-3 cities?",
  "context": "We're considering opening 50 new stores in tier-3 cities over the next year. Current presence is primarily in tier-1 and tier-2 cities.",
  "options": [
    "Aggressive expansion (50 stores in 6 months)",
    "Conservative approach (20 stores in 12 months)",
    "Franchise model (40 stores with local partners)"
  ]
}
```

**Response**:
```json
{
  "analysis": {
    "option_1": {
      "name": "Aggressive expansion (50 stores in 6 months)",
      "pros": [
        "Quick market capture",
        "Economies of scale faster",
        "Brand presence establishment"
      ],
      "cons": [
        "High upfront capital requirement",
        "Operational challenges",
        "Risk of overextension"
      ],
      "risk_level": "High"
    },
    "option_2": {
      "name": "Conservative approach (20 stores in 12 months)",
      "pros": [
        "Lower financial risk",
        "Time to learn market dynamics",
        "Better quality control"
      ],
      "cons": [
        "Slower market penetration",
        "Competitors may capture market",
        "Delayed ROI"
      ],
      "risk_level": "Low"
    },
    "option_3": {
      "name": "Franchise model (40 stores with local partners)",
      "pros": [
        "Reduced capital requirement",
        "Local market expertise",
        "Shared risk with partners"
      ],
      "cons": [
        "Less control over operations",
        "Profit sharing",
        "Brand consistency challenges"
      ],
      "risk_level": "Medium"
    },
    "recommendation": "Consider Option 3 (Franchise model) as it balances growth speed with risk management. Start with pilot franchises in 5 cities, measure performance, then scale."
  }
}
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Missing required fields
- `401 Unauthorized`: Not logged in

---

## File Management Endpoints

### List Files

List files from local filesystem.

```http
GET /files/list?directory=/path/to/dir&extension=.pdf
```

**Query Parameters**:
- `directory` (string, optional): Directory path (default: current directory)
- `extension` (string, optional): Filter by file extension (e.g., `.pdf`, `.txt`)

**Response**:
```json
{
  "files": [
    {
      "name": "Q4_Report.pdf",
      "path": "/Users/john/Documents/Q4_Report.pdf",
      "size": 245678,
      "modified": "2024-01-15T10:30:00"
    },
    {
      "name": "Sales_Data.xlsx",
      "path": "/Users/john/Documents/Sales_Data.xlsx",
      "size": 89012,
      "modified": "2024-01-16T14:20:00"
    }
  ]
}
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Not logged in
- `404 Not Found`: Directory doesn't exist

---

### Search Files

Search for files by name.

```http
GET /files/search?directory=/path/to/dir&filename=sales
```

**Query Parameters**:
- `directory` (string, optional): Search directory
- `filename` (string, required): Filename to search for (partial match)

**Response**:
```json
{
  "files": [
    "/Users/john/Documents/sales_report.pdf",
    "/Users/john/Documents/Q4/sales_data.xlsx",
    "/Users/john/Downloads/sales_forecast.docx"
  ]
}
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Missing filename parameter
- `401 Unauthorized`: Not logged in

---

### Read File

Read the contents of a file.

```http
POST /files/read
Content-Type: application/json
```

**Request Body**:
```json
{
  "path": "/Users/john/Documents/report.txt"
}
```

**Response**:
```json
{
  "content": "Q4 Sales Report\n\nTotal Revenue: $2.5M\nProfit: $750K\n..."
}
```

**Status Codes**:
- `200 OK`: Success
- `400 Bad Request`: Missing path
- `401 Unauthorized`: Not logged in
- `404 Not Found`: File doesn't exist
- `500 Internal Server Error`: Unable to read file

**Supported File Types**:
- Text files (`.txt`, `.md`, `.csv`)
- Code files (`.py`, `.js`, `.java`, etc.)
- JSON files
- Log files

---

## Scheduler Endpoints

### List Scheduled Tasks

Get all scheduled tasks.

```http
GET /scheduler/tasks
```

**Response**:
```json
{
  "tasks": [
    {
      "name": "Daily Sales Report",
      "next_run": "2024-01-17T09:00:00",
      "type": "daily",
      "interval": "09:00"
    },
    {
      "name": "Weekly Inventory Check",
      "next_run": "2024-01-20T10:00:00",
      "type": "weekly",
      "interval": "Monday 10:00"
    },
    {
      "name": "Email Reminder",
      "next_run": "2024-01-16T16:45:00",
      "type": "interval",
      "interval": "3600 seconds"
    }
  ]
}
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Not logged in

---

## Utility Endpoints

### Health Check

Check if the service is running.

```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-16T15:30:00Z"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is down

---

### Home Page

Serve the main web interface.

```http
GET /
```

**Response**: HTML page (if authenticated) or redirect to `/login`

---

## Error Handling

### Error Response Format

All errors return JSON with the following structure:

```json
{
  "error": "Error message here",
  "details": "Additional context (optional)"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200` | Success |
| `400` | Bad Request - Invalid input |
| `401` | Unauthorized - Not logged in |
| `403` | Forbidden - Domain restriction |
| `404` | Not Found - Resource doesn't exist |
| `500` | Internal Server Error - Server-side error |
| `503` | Service Unavailable - Service is down |

### Example Error Responses

**401 Unauthorized**:
```json
{
  "error": "Please log in to access this resource"
}
```

**400 Bad Request**:
```json
{
  "error": "Missing required field: message"
}
```

**403 Forbidden**:
```json
{
  "error": "Your domain is not authorized to use this service",
  "details": "Only vmart.co.in, vmartretail.com, and limeroad.com are allowed"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Failed to process request",
  "details": "Gemini API temporarily unavailable"
}
```

---

## Rate Limits

### Current Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/ask` | 60 requests | 1 minute |
| `/analyze` | 30 requests | 1 minute |
| `/files/*` | 100 requests | 1 minute |
| All others | 120 requests | 1 minute |

*Note: Rate limits are managed by external services (Gemini API, Google APIs). No application-level rate limiting is currently implemented.*

### Gemini API Limits

Free tier limits:
- 60 requests per minute
- 1,500 requests per day

For higher limits, upgrade your Gemini API plan.

---

## Example Usage

### JavaScript (Fetch API)

```javascript
// Chat with the agent
async function askAgent(question) {
  const response = await fetch('/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: question })
  });
  const data = await response.json();
  return data.response;
}

// Analyze data
async function analyzeData(csvData, type) {
  const response = await fetch('/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      data: csvData,
      analysis_type: type
    })
  });
  return await response.json();
}

// Read a file
async function readFile(filePath) {
  const response = await fetch('/files/read', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: filePath })
  });
  const data = await response.json();
  return data.content;
}
```

### Python (Requests)

```python
import requests

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Login (manual - opens browser)
# User must complete OAuth flow in browser

# Ask question
def ask_question(message, context=""):
    response = session.post(
        f"{BASE_URL}/ask",
        json={"message": message, "context": context}
    )
    return response.json()["response"]

# Analyze data
def analyze_data(data, analysis_type="general"):
    response = session.post(
        f"{BASE_URL}/analyze",
        json={"data": data, "analysis_type": analysis_type}
    )
    return response.json()["analysis"]

# List files
def list_files(directory=".", extension=None):
    params = {"directory": directory}
    if extension:
        params["extension"] = extension
    response = session.get(f"{BASE_URL}/files/list", params=params)
    return response.json()["files"]

# Usage
answer = ask_question("What are the top 3 sales trends?")
print(answer)
```

### cURL

```bash
# Ask a question
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze our Q4 performance"}' \
  --cookie "session=your_session_cookie"

# Analyze data
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "data": "Product,Sales\nLaptop,50000\nMouse,2000",
    "analysis_type": "sales"
  }' \
  --cookie "session=your_session_cookie"

# List files
curl http://localhost:5000/files/list?directory=/Documents \
  --cookie "session=your_session_cookie"

# Health check
curl http://localhost:5000/health
```

---

## Webhooks (Future)

*Webhook support is planned for future releases to enable:*
- Real-time notifications
- Event-driven automation
- Integration with external systems

---

## Versioning

Current API version: **v1.0**

The API follows semantic versioning. Breaking changes will increment the major version.

---

## Support

For API support, contact:
- **Email**: api-support@vmartretail.com
- **Internal Slack**: #ai-agent-api

---

**API Version**: 1.0  
**Last Updated**: 2024  
**Maintained by**: V-Mart IT Department
