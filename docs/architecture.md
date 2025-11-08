# V-Mart Personal AI Agent - Technical Architecture

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Security Architecture](#security-architecture)
6. [Deployment Architecture](#deployment-architecture)
7. [Scalability Considerations](#scalability-considerations)

---

## System Overview

The V-Mart Personal AI Agent is a multi-layered web application that integrates Google's Gemini LLM with various data sources to provide intelligent assistance to V-Mart employees. The system follows a modular architecture with clear separation of concerns.

### Key Design Principles

- **Modularity**: Each component is independent and replaceable
- **Security First**: OAuth authentication with domain restrictions
- **Extensibility**: Easy to add new connectors and features
- **Resilience**: Auto-restart capabilities and error handling
- **Multi-Platform**: Works on Windows, macOS, and Linux

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript (jQuery) | User interface |
| **Backend** | Python 3.8+, Flask 3.0 | Web framework |
| **AI Engine** | Google Gemini Pro, Gemini Pro Vision | Language model |
| **Authentication** | Google OAuth 2.0, Authlib | User authentication |
| **Data Sources** | Google APIs, GitHub API, Local filesystem | Data integration |
| **Task Management** | Schedule library, Threading | Automation |
| **Configuration** | Python-dotenv, Environment variables | Settings management |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   Chat   │  │ Analysis │  │  Files   │  │ Decision │       │
│  │   Tab    │  │   Tab    │  │   Tab    │  │   Tab    │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                     ▲                                             │
│                     │ AJAX Requests (JSON)                       │
│                     ▼                                             │
├─────────────────────────────────────────────────────────────────┤
│                     Flask Web Application                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Routes: /ask, /analyze, /reasoning, /summarize,          │ │
│  │          /decision-support, /files/*, /scheduler/*         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                     ▲                                             │
│                     │                                             │
├─────────────────────┼─────────────────────────────────────────────┤
│                     │      Application Layer                      │
│  ┌──────────────────┼────────────────────────────────────────┐  │
│  │                  ▼                                         │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │         Gemini Agent (AI Core)                      │  │  │
│  │  │  • get_response() - Context-aware chat             │  │  │
│  │  │  • analyze_data() - Data analysis                  │  │  │
│  │  │  • reasoning_task() - Step-by-step thinking        │  │  │
│  │  │  • summarize_document() - Summarization            │  │  │
│  │  │  • extract_insights() - Pattern recognition        │  │  │
│  │  │  • decision_support() - Pros/cons analysis         │  │  │
│  │  │  • Conversation history management                 │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                             │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │         Task Scheduler                              │  │  │
│  │  │  • Daily/Weekly/Interval tasks                      │  │  │
│  │  │  • Threading-based execution                        │  │  │
│  │  │  • Task queue management                            │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                             │  │
│  │  ┌─────────────────────────────────────────────────────┐  │  │
│  │  │         Auto Emailer                                │  │  │
│  │  │  • Template management                              │  │  │
│  │  │  • Bulk sending with personalization               │  │  │
│  │  │  • Scheduled email campaigns                        │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                     ▲                                             │
│                     │                                             │
├─────────────────────┼─────────────────────────────────────────────┤
│                     │      Connector Layer                        │
│  ┌──────────────────┴────────────────────────────────────────┐  │
│  │                                                             │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │  Drive   │  │  Gmail   │  │  Sheets  │  │   Docs   │  │  │
│  │  │Connector │  │Connector │  │Connector │  │Connector │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  │                                                             │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                │  │
│  │  │  Slides  │  │  GitHub  │  │  Local   │                │  │
│  │  │Connector │  │Connector │  │  Files   │                │  │
│  │  └──────────┘  └──────────┘  └──────────┘                │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                     ▲                                             │
├─────────────────────┼─────────────────────────────────────────────┤
│                     │      Authentication Layer                   │
│  ┌──────────────────┴────────────────────────────────────────┐  │
│  │            Google OAuth 2.0 with Domain Restriction        │  │
│  │  • Authlib OAuth client                                    │  │
│  │  • Session management                                      │  │
│  │  • Domain validation (vmart.co.in, vmartretail.com,       │  │
│  │    limeroad.com)                                           │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                     ▲                                             │
└─────────────────────┼─────────────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────────┐
        │     External Services           │
        │  • Google Cloud APIs            │
        │  • Gemini API                   │
        │  • GitHub API                   │
        │  • Local filesystem             │
        └─────────────────────────────────┘
```

---

## Core Components

### 1. Web Interface (Flask)
**Location**: `src/web/app.py`, `src/web/templates/`, `src/web/static/`

A web-based user interface for interacting with the agent. It handles user authentication, chat functionality, and provides a responsive multi-tab interface.

**Key Features**:
- Real-time chat with AJAX
- File browser and search
- Data analysis interface
- Decision support tools
- Task scheduler management

### 2. AI Agent (Gemini LLM)
**Location**: `src/agent/gemini_agent.py`

The core of the agent, powered by Google's Gemini LLM. It processes user prompts, analyzes data, and generates intelligent responses with context awareness.

**Capabilities**:
- Context-aware conversations
- Data analysis (financial, sales, inventory)
- Step-by-step reasoning
- Document summarization
- Decision support with pros/cons analysis
- Multi-modal support (text and vision)

### 3. Authentication (Google OAuth)
**Location**: `src/auth/google_auth.py`

Securely authenticates users via their Google accounts, with domain restrictions to ensure only V-Mart employees have access.

**Allowed Domains**:
- www.vmart.co.in
- www.vmartretail.com
- www.limeroad.com

### 4. Connectors
**Location**: `src/connectors/`

A modular system for connecting to various data sources:

- **Google Drive** (`google_drive.py`): Read documents, sheets, and slides
- **Gmail** (`gmail_connector.py`): Read and send emails, handle attachments
- **Google Sheets** (`google_sheets_connector.py`): Read/write spreadsheet data
- **Google Docs** (`google_docs_connector.py`): Read and create documents
- **Google Slides** (`google_slides_connector.py`): Read presentations
- **GitHub** (`github_connector.py`): Interact with repositories, create issues
- **Local Files** (`local_files.py`): Access local filesystem

### 5. Task Automation
**Location**: `src/scheduler/`

- **Task Scheduler** (`task_scheduler.py`): Schedule daily, weekly, and interval tasks
- **Auto Emailer** (`auto_emailer.py`): Template-based bulk email automation

---

## System Design

The system is designed to be a multi-platform, personal agent that can be deployed on a laptop.

### Frontend
The frontend is a modern HTML5, CSS3, and JavaScript interface served by a Flask backend with:
- Responsive design
- Gradient animations
- Multi-tab navigation
- Real-time updates via AJAX

### Backend
The backend is a Flask application that orchestrates the different components:
- Handles web requests
- Manages user sessions
- Communicates with the AI agent and connectors
- Provides REST API endpoints

### Offline/Online Capability
The agent is designed to function with or without an internet connection:
- **Online**: Connects to Google APIs, Gemini API, GitHub
- **Offline**: Works with local data and cached responses (planned)

### Auto-start and Resilience
The agent runs as a background service that starts automatically:
- **Linux**: systemd service with auto-restart
- **macOS**: LaunchAgent with KeepAlive
- **Windows**: Task Scheduler with restart policy

---

## Data Flow

### Basic Chat Flow

1. User logs in via the web interface using their Google account
2. User sends a prompt through the chat interface
3. Flask backend receives the prompt via `/ask` endpoint
4. Backend calls `GeminiAgent.get_response()` with conversation context
5. Gemini Agent processes the prompt and generates response
6. If needed, agent uses connectors to fetch data from external sources
7. Agent sends the processed response back to Flask backend
8. Backend returns JSON response to web interface
9. Interface displays the response to the user

### Data Analysis Flow

1. User uploads or pastes data in Analysis tab
2. User selects analysis type (general/financial/sales/inventory)
3. Frontend sends POST request to `/analyze` endpoint
4. Backend calls `GeminiAgent.analyze_data(data, type)`
5. Gemini processes data with analysis-specific prompting
6. Returns structured JSON with insights, metrics, recommendations
7. Frontend displays formatted analysis results

### File Reading Flow

1. User browses files in Files tab
2. User clicks on a file to read
3. Frontend sends POST to `/files/read` with file path
4. Backend uses appropriate connector (LocalFiles, GoogleDrive, etc.)
5. Connector reads and returns file contents
6. Frontend displays contents in modal or text area

---

## Security Architecture

### Authentication & Authorization
- OAuth 2.0 flow with Google
- Domain restriction enforcement
- Session-based authentication
- Secure cookie flags (HttpOnly, Secure, SameSite)

### API Security
- API keys stored in environment variables
- Never exposed in code or logs
- Separate credentials per service
- Token refresh handling

### Data Security
- User data not persisted (in-memory only)
- File access respects user permissions
- HTTPS required for production
- No data logging or tracking

---

## Deployment Architecture

### Single-User Deployment (Laptop)

```
User's Laptop (Windows/macOS/Linux)
├── Python Application (Flask + Gemini)
│   └── Port: 5000 (configurable)
├── Web Browser → http://localhost:5000
└── Auto-Start Service
    ├── Windows: Task Scheduler
    ├── macOS: LaunchAgent
    └── Linux: systemd

External Services (HTTPS)
├── Google Cloud APIs
├── Gemini API
└── GitHub API
```

### Future: Multi-User Server Deployment

```
Load Balancer (nginx) → HTTPS
├── App Server 1 (Gunicorn)
├── App Server 2 (Gunicorn)
└── Session Store (Redis)
    └── External Services
```

---

## Scalability Considerations

### Current Limitations
- Single process (not horizontally scalable)
- In-memory sessions (lost on restart)
- No database (conversation history not persisted)
- Synchronous operations

### Scaling Strategy

**Phase 1: Optimize Current**
- Response caching
- Connection pooling
- Async/await for I/O
- Request queueing

**Phase 2: Horizontal Scaling**
- Redis for sessions
- PostgreSQL for persistence
- Message queue (Celery)
- Gunicorn with multiple workers

**Phase 3: Microservices**
- Separate AI engine service
- Connector microservices
- API gateway
- Service mesh

---

## Technology Decisions & Rationale

### Why Flask?
- Simple to set up and deploy
- Lightweight for single-user scenarios
- Extensive Python ecosystem
- Easy to extend with new features

### Why Gemini?
- State-of-the-art reasoning capabilities
- Multi-modal support (text and vision)
- Native Google Workspace understanding
- Cost-effective pricing

### Why OAuth?
- Industry-standard authentication
- Single sign-on experience
- Granular permission scopes
- User trust in Google authentication

### Why Local Deployment?
- Data privacy (stays on user's machine)
- Full control over environment
- Can work offline
- No server hosting costs

---

## Future Enhancements

### Planned Features
- [ ] Offline mode with local LLM fallback
- [ ] Vector database for RAG (Retrieval Augmented Generation)
- [ ] Voice interface (speech-to-text/text-to-speech)
- [ ] Mobile app (React Native)
- [ ] Tableau/Power BI connectors
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Custom model fine-tuning

### Technical Debt
- [ ] Add comprehensive unit tests
- [ ] Implement structured logging
- [ ] Add monitoring and alerting
- [ ] Create admin panel
- [ ] Document API with OpenAPI
- [ ] Add rate limiting
- [ ] Implement caching layer
- [ ] Add database for persistence

---

**Architecture Version**: 1.0  
**Last Updated**: 2024  
**Author**: V-Mart AI Development Team

