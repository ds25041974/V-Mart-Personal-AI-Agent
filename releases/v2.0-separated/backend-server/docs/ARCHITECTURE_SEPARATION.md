# V-Mart AI Agent - Separated Architecture

## Overview

This document describes the separated architecture where the **Chatbot Agent** (user-facing) and **Backend Server** (central data management) run as independent systems, communicating over LAN/WAN.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER SYSTEMS (Multiple)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │      Chatbot Agent (app.py)                  │          │
│  │  ┌────────────────────────────────────────┐  │          │
│  │  │ - Gemini AI Chat Interface             │  │          │
│  │  │ - Google OAuth Authentication          │  │          │
│  │  │ - Local File Access                    │  │          │
│  │  │ - Task Scheduler                       │  │          │
│  │  │ - Session Management                   │  │          │
│  │  └────────────────────────────────────────┘  │          │
│  │                    ▲                          │          │
│  │                    │ Backend Client SDK       │          │
│  │                    ▼                          │          │
│  │  ┌────────────────────────────────────────┐  │          │
│  │  │  Backend Client (HTTP/REST)            │  │          │
│  │  │  - API Key Authentication              │  │          │
│  │  │  - Request/Response Handling           │  │          │
│  │  │  - Retry Logic & Caching               │  │          │
│  │  │  - Graceful Degradation                │  │          │
│  │  └────────────────────────────────────────┘  │          │
│  └──────────────────────────────────────────────┘          │
│                          │                                  │
│                          │ HTTPS over LAN/WAN              │
│                          ▼                                  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                CENTRAL BACKEND SERVER                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │   Backend Server (backend_server.py)         │          │
│  │                                               │          │
│  │  ┌────────────────────────────────────────┐  │          │
│  │  │  REST API Endpoints                    │  │          │
│  │  │  - /api/connections (CRUD)             │  │          │
│  │  │  - /api/query (Execute queries)        │  │          │
│  │  │  - /api/schema (Get schemas)           │  │          │
│  │  │  - /api/ai/analyze (AI insights)       │  │          │
│  │  │  - /api/users (User management)        │  │          │
│  │  │  - /api/roles (RBAC)                   │  │          │
│  │  └────────────────────────────────────────┘  │          │
│  │                                               │          │
│  │  ┌────────────────────────────────────────┐  │          │
│  │  │  Database Connectors                   │  │          │
│  │  │  - ClickHouse                          │  │          │
│  │  │  - PostgreSQL                          │  │          │
│  │  │  - Oracle DB                           │  │          │
│  │  │  - SQL Server                          │  │          │
│  │  │  - Tableau                             │  │          │
│  │  │  - Google Drive                        │  │          │
│  │  │  - File System                         │  │          │
│  │  └────────────────────────────────────────┘  │          │
│  │                                               │          │
│  │  ┌────────────────────────────────────────┐  │          │
│  │  │  Core Services                         │  │          │
│  │  │  - RBAC Manager (23 permissions)       │  │          │
│  │  │  - Config Manager (encrypted storage)  │  │          │
│  │  │  - AI Insights Engine (Gemini)         │  │          │
│  │  │  - Connection Pool Manager             │  │          │
│  │  └────────────────────────────────────────┘  │          │
│  │                                               │          │
│  │  ┌────────────────────────────────────────┐  │          │
│  │  │  Security Layer                        │  │          │
│  │  │  - API Key Validation                  │  │          │
│  │  │  - Rate Limiting                       │  │          │
│  │  │  - Request Logging                     │  │          │
│  │  │  - IP Whitelisting (optional)          │  │          │
│  │  └────────────────────────────────────────┘  │          │
│  └──────────────────────────────────────────────┘          │
│                          │                                  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────┐          │
│  │        External Data Sources                 │          │
│  │  - ClickHouse Clusters                       │          │
│  │  - PostgreSQL Databases                      │          │
│  │  - Oracle Databases                          │          │
│  │  - SQL Server Instances                      │          │
│  │  - Tableau Servers                           │          │
│  │  - Google Drive APIs                         │          │
│  │  - Network File Systems                      │          │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Chatbot Agent (User System)

**Purpose**: User-facing AI chatbot for individual systems

**Location**: Runs on each user's machine

**Port**: 8000 (local)

**Features**:
- Gemini AI conversational interface
- Google OAuth authentication
- Local file access
- Task scheduling
- Session management
- Backend data integration via REST API

**Dependencies**:
- Flask (web framework)
- Gemini AI SDK
- Google Auth libraries
- Backend client SDK (custom)

**Configuration**:
```yaml
# chatbot_config.yaml
chatbot:
  port: 8000
  session_timeout: 3600
  
backend:
  url: "https://backend.vmart.co.in:5000"  # Or LAN IP
  api_key: "${BACKEND_API_KEY}"
  timeout: 30
  retry_attempts: 3
  cache_ttl: 300
  
google_oauth:
  client_id: "${GOOGLE_CLIENT_ID}"
  client_secret: "${GOOGLE_CLIENT_SECRET}"
  
gemini:
  api_key: "${GEMINI_API_KEY}"
  model: "gemini-pro"
```

### 2. Backend Server (Central)

**Purpose**: Central data management and API connector hub

**Location**: Runs on central server (LAN/WAN accessible)

**Port**: 5000 (configurable)

**Features**:
- Database connector management (7 types)
- AI insights engine
- RBAC with 23 granular permissions
- Encrypted credential storage
- Connection pooling
- Query execution and schema inspection
- API key authentication
- Rate limiting and logging

**Dependencies**:
- Flask (API server)
- clickhouse-driver
- psycopg2-binary
- oracledb
- pyodbc
- cryptography
- All backend modules

**Configuration**:
```yaml
# backend_config.yaml
server:
  host: "0.0.0.0"  # Listen on all interfaces
  port: 5000
  ssl_cert: "/path/to/cert.pem"
  ssl_key: "/path/to/key.pem"
  
security:
  api_keys_file: "/secure/api_keys.enc"
  rate_limit: "100/hour"
  allowed_ips:  # Optional whitelist
    - "192.168.1.0/24"
    - "10.0.0.0/8"
  
database:
  max_connections: 20
  connection_timeout: 30
  query_timeout: 300
  
logging:
  level: "INFO"
  file: "/var/log/vmart/backend.log"
  max_size_mb: 100
```

### 3. Backend Client SDK

**Purpose**: HTTP client library for chatbot-to-backend communication

**Location**: Embedded in chatbot agent

**Features**:
- Automatic API key injection
- Request retry with exponential backoff
- Response caching
- Graceful error handling
- Timeout management
- Health check monitoring

**Example Usage**:
```python
from backend_client import BackendClient

# Initialize client
client = BackendClient(
    base_url="https://backend.vmart.co.in:5000",
    api_key=os.getenv("BACKEND_API_KEY"),
    timeout=30
)

# Query database
result = client.execute_query(
    connection="postgres_prod",
    query="SELECT * FROM customers LIMIT 10"
)

# Get AI insights
insights = client.analyze_data(
    connection="clickhouse_analytics",
    query="SELECT date, revenue FROM sales WHERE date > '2024-01-01'"
)

# Manage connections
connections = client.list_connections()
```

## Communication Flow

### 1. User Makes Request
```
User → Chatbot UI → Gemini Agent → Backend Client SDK
```

### 2. Backend Query
```
Backend Client SDK → HTTP/HTTPS → Backend Server → Database Connector → External DB
```

### 3. Response Flow
```
External DB → Database Connector → Backend Server → HTTP Response → Backend Client SDK
→ Chatbot UI → User
```

### 4. With Caching
```
Backend Client SDK (cache hit) → Cached Response → Chatbot UI → User
```

## Network Configuration

### LAN Setup

**Backend Server**:
- IP: `192.168.1.100:5000`
- Accessible within local network
- Fast, low-latency communication

**Chatbot Agents**:
- Configure backend URL: `http://192.168.1.100:5000`
- No internet required
- Ideal for office/enterprise environments

### WAN Setup

**Backend Server**:
- Domain: `backend.vmart.co.in`
- SSL/TLS required (HTTPS)
- Public or VPN-accessible
- Firewall rules for port 5000

**Chatbot Agents**:
- Configure backend URL: `https://backend.vmart.co.in:5000`
- Requires internet connectivity
- Ideal for remote/distributed teams

## Security

### Authentication

**API Key Authentication**:
```http
GET /api/connections HTTP/1.1
Host: backend.vmart.co.in:5000
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

**Key Generation**:
```bash
# Generate API key for chatbot agent
python backend_server.py generate-key --name "chatbot-user1" --permissions "db_read,ai_insights"
```

### Encryption

**In Transit**:
- TLS 1.3 for HTTPS
- Certificate-based authentication (optional)

**At Rest**:
- Fernet encryption for credentials
- Encrypted config files
- Secure key storage (~/.vmart/.key)

### Authorization

**RBAC Permissions**:
- Each API key has specific permissions
- Permission check before each operation
- Audit logging of all actions

## Deployment

### Backend Server Deployment

**Option 1: Docker**:
```bash
cd backend
docker build -t vmart-backend .
docker run -d -p 5000:5000 \
  -v /secure/config:/app/config \
  -v /secure/logs:/app/logs \
  --name vmart-backend \
  vmart-backend
```

**Option 2: Systemd Service**:
```bash
# Install backend
sudo cp backend_server.py /usr/local/bin/
sudo cp backend.service /etc/systemd/system/

# Start service
sudo systemctl enable backend
sudo systemctl start backend
```

**Option 3: Manual**:
```bash
cd backend
pip install -r backend_requirements.txt
python backend_server.py --config /etc/vmart/backend_config.yaml
```

### Chatbot Agent Deployment

**Individual Systems**:
```bash
# Install chatbot
cd chatbot
pip install -r chatbot_requirements.txt

# Configure backend connection
cat > config/backend.yaml << EOF
backend:
  url: "https://backend.vmart.co.in:5000"
  api_key: "${BACKEND_API_KEY}"
EOF

# Run chatbot
python src/web/app.py
```

**Multiple Users**:
- Each user gets their own API key
- Isolated sessions and permissions
- Shared backend data access

## Error Handling

### Backend Server Unreachable

```python
try:
    result = client.execute_query(...)
except BackendConnectionError:
    # Fallback to cached data
    result = client.get_from_cache(...)
    show_warning("Backend server temporarily unavailable")
except BackendTimeoutError:
    # Retry with backoff
    result = client.retry_request(...)
```

### Database Connection Failure

```python
# Backend handles gracefully
try:
    conn = db_manager.get_connection("postgres_prod")
    result = conn.execute_query(query)
except DatabaseConnectionError as e:
    return {
        "error": "Database unavailable",
        "details": str(e),
        "retry_after": 60
    }
```

## Monitoring

### Health Checks

**Backend Server**:
```bash
curl https://backend.vmart.co.in:5000/health
# {"status": "ok", "connections": 5, "uptime": 86400}
```

**Chatbot Agent**:
```python
# Check backend connectivity
is_connected = client.health_check()
if not is_connected:
    show_offline_mode()
```

### Metrics

**Backend Server**:
- Request count per endpoint
- Average response time
- Active connections
- Error rates
- Database query performance

**Chatbot Agent**:
- Backend latency
- Cache hit rate
- Failed requests
- User session duration

## Advantages of Separation

### ✅ Scalability
- Backend server handles multiple chatbot agents
- Horizontal scaling of backend with load balancer
- Independent scaling of components

### ✅ Security
- Centralized credential management
- No database credentials on user systems
- API key-based access control

### ✅ Maintenance
- Update backend without touching user systems
- Deploy new connectors centrally
- Easier troubleshooting

### ✅ Performance
- Backend connection pooling benefits all users
- Cached query results shared across agents
- Reduced database load

### ✅ Flexibility
- Mix LAN and WAN deployments
- Support remote workers
- Easy to add new data sources

## Migration Path

### Phase 1: Prepare (Current)
- ✅ Backend manager already built
- ✅ All connectors implemented
- ✅ Documentation complete

### Phase 2: Separate (Next)
- Create backend_server.py
- Create backend_client.py SDK
- Update app.py to use client
- Split requirements.txt

### Phase 3: Deploy
- Set up backend server
- Configure network/firewall
- Generate API keys
- Deploy chatbot agents

### Phase 4: Optimize
- Add caching layer
- Implement monitoring
- Performance tuning
- Security hardening

## File Structure

```
V-Mart Personal AI Agent/
├── chatbot/                    # User system deployment
│   ├── src/
│   │   ├── web/
│   │   │   └── app.py         # Chatbot agent (refactored)
│   │   ├── agent/
│   │   │   └── gemini_agent.py
│   │   └── backend_client.py  # Backend client SDK
│   ├── config/
│   │   └── chatbot_config.yaml
│   ├── requirements.txt       # Chatbot dependencies only
│   └── run_chatbot.sh
│
├── backend/                   # Central server deployment
│   ├── backend_server.py     # Standalone backend server
│   ├── src/
│   │   └── backend/          # All connector modules
│   │       ├── db_manager.py
│   │       ├── clickhouse_connector.py
│   │       ├── postgres_connector.py
│   │       ├── oracle_connector.py
│   │       ├── sqlserver_connector.py
│   │       ├── tableau_connector.py
│   │       ├── gdrive_connector.py
│   │       ├── filesystem_connector.py
│   │       ├── ai_insights.py
│   │       ├── rbac.py
│   │       └── config_manager.py
│   ├── config/
│   │   └── backend_config.yaml
│   ├── requirements.txt      # Backend dependencies only
│   └── run_backend.sh
│
└── docs/
    ├── BACKEND_MANAGER.md
    ├── ARCHITECTURE_SEPARATION.md
    └── DEPLOYMENT_GUIDE.md
```

## Next Steps

1. ✅ Architecture documented
2. ⏳ Create backend_server.py
3. ⏳ Create backend_client.py SDK
4. ⏳ Refactor app.py to use client
5. ⏳ Split requirements.txt
6. ⏳ Create deployment scripts
7. ⏳ Test LAN/WAN connectivity
8. ⏳ Security hardening
9. ⏳ Performance optimization
10. ⏳ Production deployment

---

**Developed by**: DSR  
**Version**: 2.0  
**Last Updated**: November 9, 2025
