# V-Mart Personal AI Agent - Dependencies & Libraries Documentation

## Overview

This document provides a comprehensive list of all Python libraries and dependencies used in the V-Mart Personal AI Agent project, their purposes, versions, and how they contribute to achieving the project objectives.

## Table of Contents

1. [Core Objective](#core-objective)
2. [Web Framework Dependencies](#web-framework-dependencies)
3. [AI & Machine Learning](#ai--machine-learning)
4. [Google Cloud Integration](#google-cloud-integration)
5. [Authentication & Security](#authentication--security)
6. [Data Processing](#data-processing)
7. [System Utilities](#system-utilities)
8. [Development & Type Safety](#development--type-safety)
9. [Dependency Tree](#dependency-tree)
10. [Installation](#installation)

---

## Core Objective

**Project Goal:** Build an intelligent AI agent that integrates with Google Workspace (Gmail, Drive), GitHub, and uses Gemini AI to provide intelligent assistance for:
- Document search and analysis
- Business decision making
- Financial analysis
- File management
- Automated workflows

---

## Web Framework Dependencies

### 1. Flask (3.0.0)
**Purpose:** Core web framework for building the web application

**Key Features:**
- Creates RESTful API endpoints
- Handles HTTP requests/responses
- Manages routing and URL mapping
- Serves the web interface

**How It Helps:**
- Provides the foundation for the 4-tab web interface (Chat, Analysis, Files, Decision)
- Enables real-time interaction with the AI agent
- Serves static files (CSS, JavaScript)
- Manages session handling

**Usage in Project:**
```python
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
```

**Dependencies:**
- Werkzeug (WSGI utility library)
- Jinja2 (template engine)
- Click (CLI framework)
- ItsDangerous (cryptographic signing)

---

### 2. Werkzeug (3.0.1)
**Purpose:** WSGI utility library that powers Flask

**Key Features:**
- Request/response handling
- URL routing
- Debug utilities
- Security features

**How It Helps:**
- Provides secure password hashing
- Handles multipart form data (file uploads)
- URL parsing and generation
- Development server with auto-reload

**Usage in Project:**
```python
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
```

---

## AI & Machine Learning

### 3. google-generativeai (0.3.1)
**Purpose:** Official Google Gemini AI SDK

**Key Features:**
- Access to Gemini Pro model
- Text generation
- Multi-turn conversations
- Content understanding

**How It Helps:**
- **Core AI Engine**: Powers all intelligent features
- **Natural Language Understanding**: Processes user queries
- **Content Generation**: Creates responses, summaries, recommendations
- **Decision Support**: Analyzes data and provides insights

**Usage in Project:**
```python
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompt)
```

**Capabilities Used:**
1. **Chat Tab**: Conversational AI
2. **Analysis Tab**: Financial and sales analysis
3. **Files Tab**: Document summarization
4. **Decision Tab**: AI-powered recommendations

---

## Google Cloud Integration

### 4. google-api-python-client (2.108.0)
**Purpose:** Official Google API client library

**Key Features:**
- Access to Gmail API
- Access to Google Drive API
- OAuth2 authentication
- Resource management

**How It Helps:**
- **Email Integration**: Search and read Gmail messages
- **File Access**: Search and retrieve Google Drive files
- **Document Search**: Find documents across Google Workspace
- **Attachment Handling**: Download and process email attachments

**Usage in Project:**
```python
from googleapiclient.discovery import build

# Gmail API
gmail_service = build('gmail', 'v1', credentials=creds)
messages = gmail_service.users().messages().list(userId='me').execute()

# Drive API
drive_service = build('drive', 'v3', credentials=creds)
files = drive_service.files().list(q="name contains 'invoice'").execute()
```

**APIs Integrated:**
- **Gmail API v1**: Email search, read, attachments
- **Drive API v3**: File search, download, metadata

---

### 5. google-auth-httplib2 (0.2.0)
**Purpose:** HTTP transport library for Google authentication

**Key Features:**
- HTTP/2 support
- Connection pooling
- Authentication transport

**How It Helps:**
- Enables authenticated HTTP requests to Google APIs
- Manages connection efficiency
- Handles authentication headers

---

### 6. google-auth-oauthlib (1.2.0)
**Purpose:** OAuth 2.0 authentication flow

**Key Features:**
- OAuth2 consent flow
- Token management
- Credential storage

**How It Helps:**
- **User Authentication**: Securely authenticate users with Google
- **Token Refresh**: Automatically refresh expired tokens
- **Scope Management**: Request specific permissions (Gmail, Drive)
- **Security**: Implements OAuth2 best practices

**Usage in Project:**
```python
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/drive.readonly']
)
credentials = flow.run_local_server(port=0)
```

---

## Authentication & Security

### 7. authlib (1.3.0)
**Purpose:** OAuth and authentication library

**Key Features:**
- OAuth 1.0/2.0 client and server
- OpenID Connect
- JWT handling
- Session management

**How It Helps:**
- **Multi-provider Auth**: Support for Google, GitHub OAuth
- **Token Management**: Secure token storage and refresh
- **Session Security**: Encrypted session handling
- **Standards Compliance**: Implements RFC specifications

**Usage in Project:**
```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET
)
```

---

### 8. requests (2.31.0)
**Purpose:** HTTP library for making API calls

**Key Features:**
- Simple HTTP requests
- Session management
- SSL verification
- Automatic content decoding

**How It Helps:**
- **External API Calls**: Communicate with third-party services
- **File Downloads**: Retrieve files from URLs
- **Webhook Integration**: Send/receive webhooks
- **Error Handling**: Robust request error management

**Usage in Project:**
```python
import requests

response = requests.get('https://api.github.com/repos/user/repo')
data = response.json()
```

---

## GitHub Integration

### 9. PyGithub (2.1.1)
**Purpose:** GitHub API v3 Python library

**Key Features:**
- Repository management
- Issue tracking
- Pull request handling
- User/organization access

**How It Helps:**
- **Repository Access**: Browse and manage GitHub repositories
- **Issue Management**: Create, read, update issues
- **File Operations**: Read files from repositories
- **Automation**: Automate GitHub workflows

**Usage in Project:**
```python
from github import Github

g = Github(GITHUB_TOKEN)
repo = g.get_repo("user/repository")
issues = repo.get_issues(state='open')
```

**Features Used:**
- Search repositories
- Read file contents
- Access commit history
- Manage issues and PRs

---

## Data Processing

### 10. pandas (2.1.4)
**Purpose:** Data manipulation and analysis library

**Key Features:**
- DataFrame operations
- Data cleaning
- Statistical analysis
- CSV/Excel handling

**How It Helps:**
- **Financial Analysis**: Process sales and revenue data
- **Data Aggregation**: Group and summarize information
- **Report Generation**: Create structured reports
- **Data Visualization**: Prepare data for charts

**Usage in Project:**
```python
import pandas as pd

# Financial analysis
df = pd.DataFrame(sales_data)
monthly_revenue = df.groupby('month')['revenue'].sum()
growth_rate = (monthly_revenue.pct_change() * 100).round(2)
```

**Use Cases:**
1. **Sales Analysis**: Revenue trends, growth rates
2. **Inventory Management**: Stock levels, reorder points
3. **Financial Reports**: P&L statements, cash flow
4. **Data Cleaning**: Handle missing values, duplicates

---

### 11. numpy (1.26.2)
**Purpose:** Numerical computing library

**Key Features:**
- Array operations
- Mathematical functions
- Linear algebra
- Statistical operations

**How It Helps:**
- **Calculations**: Fast numerical computations
- **Data Processing**: Array-based operations for pandas
- **Statistical Analysis**: Mean, median, standard deviation
- **Performance**: Optimized C-based operations

**Usage in Project:**
```python
import numpy as np

# Calculate metrics
revenue_array = np.array([100000, 120000, 115000, 130000])
avg_revenue = np.mean(revenue_array)
growth = np.diff(revenue_array) / revenue_array[:-1] * 100
```

---

## Scheduling & Automation

### 12. schedule (1.2.0)
**Purpose:** Job scheduling library

**Key Features:**
- Cron-like scheduling
- Periodic task execution
- Time-based triggers
- Simple API

**How It Helps:**
- **Automated Tasks**: Run background jobs periodically
- **Data Refresh**: Update caches and data at intervals
- **Monitoring**: Check system health regularly
- **Cleanup**: Remove old files/logs automatically

**Usage in Project:**
```python
import schedule
import time

def check_emails():
    # Check for new emails every 5 minutes
    pass

schedule.every(5).minutes.do(check_emails)

while True:
    schedule.run_pending()
    time.sleep(1)
```

**Scheduled Tasks:**
- Email synchronization
- Cache updates
- Log rotation
- Health checks

---

## System Utilities

### 13. python-dotenv (1.0.0)
**Purpose:** Environment variable management

**Key Features:**
- Load .env files
- Environment isolation
- Configuration management
- Secret handling

**How It Helps:**
- **Security**: Keep API keys out of code
- **Configuration**: Manage settings per environment
- **Portability**: Easy deployment across environments
- **Secret Management**: Secure credential storage

**Usage in Project:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
```

**Environment Variables:**
```env
GEMINI_API_KEY=your_gemini_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GITHUB_TOKEN=your_github_token
PORT=5000
DEBUG=False
```

---

## Development & Type Safety

### 14. typing-extensions (4.9.0)
**Purpose:** Backport of latest typing features

**Key Features:**
- Type hints
- Generic types
- Protocol support
- Runtime type checking

**How It Helps:**
- **Code Quality**: Catch errors before runtime
- **IDE Support**: Better autocomplete and hints
- **Documentation**: Self-documenting code
- **Maintainability**: Easier refactoring

**Usage in Project:**
```python
from typing import List, Dict, Optional, Union
from typing_extensions import TypedDict

class AnalysisResult(TypedDict):
    revenue: float
    growth_rate: float
    insights: List[str]

def analyze_data(data: List[Dict]) -> Optional[AnalysisResult]:
    # Type hints help catch errors
    pass
```

---

## Dependency Tree

### Primary Dependencies → Sub-dependencies

```
V-Mart Personal AI Agent
├── Flask (3.0.0)
│   ├── Werkzeug (3.0.1)
│   ├── Jinja2 (3.1.2)
│   ├── Click (8.1.7)
│   └── ItsDangerous (2.1.2)
│
├── google-generativeai (0.3.1)
│   ├── google-ai-generativelanguage
│   ├── google-api-core
│   ├── google-auth
│   ├── protobuf
│   └── pydantic
│
├── google-api-python-client (2.108.0)
│   ├── google-auth
│   ├── google-auth-httplib2
│   ├── google-api-core
│   ├── httplib2
│   └── uritemplate
│
├── google-auth-oauthlib (1.2.0)
│   ├── google-auth
│   ├── requests-oauthlib
│   └── click
│
├── PyGithub (2.1.1)
│   ├── pynacl
│   ├── requests
│   ├── pyjwt
│   └── urllib3
│
├── pandas (2.1.4)
│   ├── numpy
│   ├── python-dateutil
│   ├── pytz
│   └── tzdata
│
├── authlib (1.3.0)
│   └── cryptography
│
├── requests (2.31.0)
│   ├── charset-normalizer
│   ├── idna
│   ├── urllib3
│   └── certifi
│
├── schedule (1.2.0)
│   (no dependencies)
│
├── python-dotenv (1.0.0)
│   (no dependencies)
│
└── typing-extensions (4.9.0)
    (no dependencies)
```

---

## Installation

### Method 1: Using requirements.txt

```bash
pip install -r requirements.txt
```

### Method 2: Individual Installation

```bash
# Web Framework
pip install Flask==3.0.0 Werkzeug==3.0.1

# AI & Google APIs
pip install google-generativeai==0.3.1
pip install google-api-python-client==2.108.0
pip install google-auth-httplib2==0.2.0
pip install google-auth-oauthlib==1.2.0

# GitHub Integration
pip install PyGithub==2.1.1

# Authentication & HTTP
pip install authlib==1.3.0
pip install requests==2.31.0

# Data Processing
pip install pandas==2.1.4
pip install numpy==1.26.2

# Utilities
pip install schedule==1.2.0
pip install python-dotenv==1.0.0
pip install typing-extensions==4.9.0
```

### Method 3: Development Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

## Dependency Summary by Category

### Web & API (3 libraries)
- **Flask**: Web framework
- **Werkzeug**: WSGI utilities
- **requests**: HTTP client

### AI & Intelligence (1 library)
- **google-generativeai**: Gemini AI SDK

### Google Cloud (3 libraries)
- **google-api-python-client**: Gmail, Drive APIs
- **google-auth-httplib2**: HTTP transport
- **google-auth-oauthlib**: OAuth2 flow

### Authentication (1 library)
- **authlib**: OAuth and authentication

### GitHub (1 library)
- **PyGithub**: GitHub API client

### Data Processing (2 libraries)
- **pandas**: Data analysis
- **numpy**: Numerical computing

### Utilities (3 libraries)
- **schedule**: Task scheduling
- **python-dotenv**: Environment management
- **typing-extensions**: Type hints

**Total Primary Dependencies**: 14 libraries  
**Total with Sub-dependencies**: ~50+ libraries

---

## How Dependencies Work Together

### 1. User Authentication Flow
```
User → Flask (Web Interface)
     → authlib (OAuth initiation)
     → google-auth-oauthlib (Google consent)
     → google-api-python-client (Access Gmail/Drive)
```

### 2. AI Query Processing
```
User Query → Flask (Receives input)
          → google-generativeai (Gemini AI)
          → pandas/numpy (Data processing)
          → Flask (Returns response)
```

### 3. Document Search
```
Search Request → Flask (API endpoint)
             → google-api-python-client (Drive/Gmail search)
             → google-generativeai (Content analysis)
             → Flask (Formatted results)
```

### 4. GitHub Integration
```
GitHub Request → Flask (API)
             → PyGithub (GitHub API)
             → requests (HTTP calls)
             → Flask (Response)
```

### 5. Background Tasks
```
schedule → Check emails (every 5 min)
        → Update cache (every hour)
        → Cleanup logs (daily)
```

---

## Performance Considerations

### Library Sizes (Approximate)

| Library | Size | Load Time |
|---------|------|-----------|
| Flask | 2 MB | Fast |
| google-generativeai | 5 MB | Medium |
| pandas | 20 MB | Medium |
| numpy | 15 MB | Fast |
| PyGithub | 3 MB | Fast |
| Others | 10 MB | Fast |

**Total Installed Size**: ~100-150 MB

### Optimization Tips

1. **Lazy Loading**: Import heavy libraries only when needed
2. **Caching**: Cache API responses to reduce calls
3. **Async Operations**: Use background tasks for long operations
4. **Connection Pooling**: Reuse HTTP connections
5. **Data Pagination**: Load data in chunks

---

## Security Best Practices

### 1. API Keys & Secrets
- Store in `.env` file (never commit to Git)
- Use environment variables (`python-dotenv`)
- Rotate keys regularly

### 2. OAuth Tokens
- Secure token storage (`authlib`)
- Automatic token refresh
- Minimal scope requests

### 3. HTTP Security
- Use HTTPS for production
- Verify SSL certificates (`requests`)
- Sanitize user inputs (Werkzeug)

### 4. Data Protection
- Encrypt sensitive data
- Secure session cookies
- Input validation

---

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Solution: Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### 2. API Authentication Failures
```bash
# Check environment variables
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

#### 3. Version Conflicts
```bash
# Create fresh virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Google API Quota Exceeded
- Implement rate limiting
- Use caching
- Batch requests

---

## Future Dependencies (Roadmap)

### Planned Additions

1. **Database**: SQLAlchemy or MongoDB
   - Persistent data storage
   - User management

2. **Caching**: Redis
   - Fast data caching
   - Session storage

3. **Testing**: pytest, pytest-cov
   - Unit tests
   - Integration tests
   - Coverage reports

4. **Logging**: loguru
   - Advanced logging
   - Log rotation

5. **Monitoring**: Sentry
   - Error tracking
   - Performance monitoring

6. **Documentation**: Sphinx
   - API documentation
   - Auto-generated docs

---

## License Information

All dependencies are open-source with permissive licenses:

- **Apache 2.0**: Flask, google-* libraries, pandas
- **MIT**: requests, PyGithub, schedule, python-dotenv
- **BSD**: numpy, Werkzeug

See individual package licenses for details.

---

## Conclusion

The V-Mart Personal AI Agent leverages a carefully selected stack of 14 primary Python libraries (plus ~50 sub-dependencies) to deliver:

✅ **Intelligent AI Capabilities** (Gemini AI)  
✅ **Google Workspace Integration** (Gmail, Drive)  
✅ **GitHub Integration** (Repository management)  
✅ **Data Analysis** (pandas, numpy)  
✅ **Web Interface** (Flask)  
✅ **Security** (OAuth, authlib)  
✅ **Automation** (schedule)  
✅ **Reliability** (Type hints, error handling)

Each library is chosen for its:
- **Reliability**: Well-maintained and tested
- **Performance**: Optimized for production use
- **Community**: Strong community support
- **Documentation**: Comprehensive docs
- **Integration**: Works well with other libraries

This technology stack enables the AI agent to provide comprehensive, intelligent assistance while maintaining security, performance, and reliability.

---

**Document Version**: 1.0  
**Last Updated**: November 8, 2025  
**Project**: V-Mart Personal AI Agent  
**Repository**: https://github.com/ds25041974/V-Mart-Personal-AI-Agent
