# V-Mart AI Agent - Architecture Diagrams

## System Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         V-MART AI AGENT ECOSYSTEM                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│                        USER SYSTEMS (Multiple Locations)                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │   User 1        │  │   User 2        │  │   User 3        │             │
│  │   Computer      │  │   Laptop        │  │   Remote PC     │             │
│  │                 │  │                 │  │                 │             │
│  │  ┌───────────┐  │  │  ┌───────────┐  │  │  ┌───────────┐  │             │
│  │  │ Chatbot   │  │  │  │ Chatbot   │  │  │  │ Chatbot   │  │             │
│  │  │ Agent     │  │  │  │ Agent     │  │  │  │ Agent     │  │             │
│  │  │ :8000     │  │  │  │ :8000     │  │  │  │ :8000     │  │             │
│  │  └─────┬─────┘  │  │  └─────┬─────┘  │  │  └─────┬─────┘  │             │
│  └────────┼────────┘  └────────┼────────┘  └────────┼────────┘             │
│           │                    │                    │                       │
│           └────────────────────┼────────────────────┘                       │
│                                │                                            │
└────────────────────────────────┼────────────────────────────────────────────┘
                                 │
                                 │ REST API over LAN/WAN
                                 │ HTTPS with API Key Auth
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        CENTRAL SERVER (Single Location)                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                     Backend Server (:5000)                         │     │
│  ├────────────────────────────────────────────────────────────────────┤     │
│  │                                                                    │     │
│  │  ┌──────────────────────────────────────────────────────────┐     │     │
│  │  │              REST API Layer                              │     │     │
│  │  │  • /api/connections   • /api/query                       │     │     │
│  │  │  • /api/schema        • /api/ai/analyze                  │     │     │
│  │  │  • /api/users         • /api/stats                       │     │     │
│  │  └──────────────────────────────────────────────────────────┘     │     │
│  │                           │                                        │     │
│  │  ┌────────────────────────┴─────────────────────────────────┐     │     │
│  │  │           Security & Authentication Layer                │     │     │
│  │  │  • API Key Validation  • Rate Limiting (100/hr)          │     │     │
│  │  │  • RBAC Permissions   • Request Logging                  │     │     │
│  │  └──────────────────────────────────────────────────────────┘     │     │
│  │                           │                                        │     │
│  │  ┌────────────────────────┴─────────────────────────────────┐     │     │
│  │  │                Core Services Layer                       │     │     │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │     │     │
│  │  │  │ DB Manager   │  │ RBAC Manager │  │ Config Mgr   │   │     │     │
│  │  │  │ Connection   │  │ 23 Permissions│ │ Encrypted    │   │     │     │
│  │  │  │ Pooling      │  │ User Roles   │  │ Credentials  │   │     │     │
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘   │     │     │
│  │  │  ┌─────────────────────────────────────────────────┐    │     │     │
│  │  │  │         AI Insights Engine (Gemini)             │    │     │     │
│  │  │  │  • Data Analysis  • Recommendations             │    │     │     │
│  │  │  │  • Pattern Detection  • Forecasting             │    │     │     │
│  │  │  └─────────────────────────────────────────────────┘    │     │     │
│  │  └──────────────────────────────────────────────────────────┘     │     │
│  │                           │                                        │     │
│  │  ┌────────────────────────┴─────────────────────────────────┐     │     │
│  │  │              Database Connectors Layer                   │     │     │
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐              │     │     │
│  │  │  │ClickHouse │ │ PostgreSQL│ │  Oracle   │              │     │     │
│  │  │  │ Connector │ │ Connector │ │ Connector │              │     │     │
│  │  │  └───────────┘ └───────────┘ └───────────┘              │     │     │
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐              │     │     │
│  │  │  │SQL Server │ │  Tableau  │ │Google Drive│             │     │     │
│  │  │  │ Connector │ │ Connector │ │ Connector │              │     │     │
│  │  │  └───────────┘ └───────────┘ └───────────┘              │     │     │
│  │  │  ┌───────────┐                                           │     │     │
│  │  │  │File System│                                           │     │     │
│  │  │  │ Connector │                                           │     │     │
│  │  │  └───────────┘                                           │     │     │
│  │  └──────────────────────────────────────────────────────────┘     │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                 │                                           │
│                                 ▼                                           │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │                    External Data Sources                           │     │
│  │  • ClickHouse Clusters    • PostgreSQL Databases                   │     │
│  │  • Oracle Databases       • SQL Server Instances                   │     │
│  │  • Tableau Servers        • Google Drive APIs                      │     │
│  │  • Network File Systems   • Cloud Storage                          │     │
│  └────────────────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Communication Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Request/Response Flow                                │
└─────────────────────────────────────────────────────────────────────────────┘

1. USER QUERY
   ┌──────────┐
   │   User   │  "Show me top 10 customers"
   └────┬─────┘
        │
        ▼
   ┌──────────────────┐
   │  Chatbot Agent   │  Web UI (port 8000)
   │  (User System)   │  
   └────┬─────────────┘
        │
        │ ① Gemini AI processes natural language
        │ ② Determines backend query needed
        │
        ▼
   ┌──────────────────┐
   │ Backend Client   │  HTTP Client SDK
   │     SDK          │  • Adds API key
   └────┬─────────────┘  • Handles retry
        │               • Caches responses
        │
        │ HTTP POST /api/query
        │ Authorization: Bearer <API_KEY>
        │ Content-Type: application/json
        │ {
        │   "connection": "postgres_prod",
        │   "query": "SELECT * FROM customers ORDER BY revenue DESC LIMIT 10"
        │ }
        │
        ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║                           NETWORK BOUNDARY                                ║
║                      (LAN: 192.168.1.x / WAN: HTTPS)                     ║
╚═══════════════════════════════════════════════════════════════════════════╝
        │
        ▼
   ┌──────────────────┐
   │ Backend Server   │  Central Server (port 5000)
   │                  │  ③ Validates API key
   └────┬─────────────┘  ④ Checks permissions
        │               ⑤ Applies rate limit
        │
        ▼
   ┌──────────────────┐
   │  DB Manager      │  ⑥ Gets connection from pool
   └────┬─────────────┘
        │
        ▼
   ┌──────────────────┐
   │ Postgres         │  ⑦ Executes query
   │ Connector        │  
   └────┬─────────────┘
        │
        ▼
   ┌──────────────────┐
   │ PostgreSQL DB    │  ⑧ Returns results
   │   (External)     │  
   └────┬─────────────┘
        │
        │ Results: [{id: 1, name: "ABC Corp", revenue: 1000000}, ...]
        │
        ▼
   ┌──────────────────┐
   │ Backend Server   │  ⑨ Formats response
   └────┬─────────────┘  ⑩ Returns JSON
        │
        │ HTTP 200 OK
        │ Content-Type: application/json
        │ {
        │   "status": "success",
        │   "result": [...]
        │ }
        │
        ▼
╔═══════════════════════════════════════════════════════════════════════════╗
║                           NETWORK BOUNDARY                                ║
╚═══════════════════════════════════════════════════════════════════════════╝
        │
        ▼
   ┌──────────────────┐
   │ Backend Client   │  ⑪ Caches response (TTL: 300s)
   │     SDK          │  ⑫ Returns data
   └────┬─────────────┘
        │
        ▼
   ┌──────────────────┐
   │  Chatbot Agent   │  ⑬ Formats for display
   └────┬─────────────┘  ⑭ Shows in UI
        │
        ▼
   ┌──────────┐
   │   User   │  Sees results in web interface
   └──────────┘
```

## Deployment Scenarios

### Scenario 1: LAN Deployment (Office)

```
┌────────────────────────────────────────────────────────────┐
│              Office Network (192.168.1.0/24)               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Workstation 1│  │ Workstation 2│  │ Workstation 3│     │
│  │ Chatbot :8000│  │ Chatbot :8000│  │ Chatbot :8000│     │
│  │ .1.101       │  │ .1.102       │  │ .1.103       │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │             │
│         └─────────────────┼─────────────────┘             │
│                           │                               │
│                           │ HTTP (fast local network)     │
│                           │                               │
│                           ▼                               │
│                  ┌──────────────┐                         │
│                  │ Server       │                         │
│                  │ Backend :5000│                         │
│                  │ 192.168.1.100│                         │
│                  └──────┬───────┘                         │
│                         │                                 │
└─────────────────────────┼─────────────────────────────────┘
                          │
                          │ Private DB connections
                          ▼
               ┌────────────────────┐
               │  Database Servers  │
               │  (Internal)        │
               └────────────────────┘

Advantages:
✅ Fast (< 5ms latency)
✅ Secure (no internet exposure)
✅ No SSL required
✅ Simple setup
```

### Scenario 2: WAN Deployment (Remote)

```
┌────────────────────────────────────────────────────────────┐
│                      INTERNET                              │
└────────────────────────────────────────────────────────────┘
         │                     │                     │
         │ HTTPS               │ HTTPS               │ HTTPS
         ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Home Office  │      │ Remote Worker│      │ Mobile User  │
│ Chatbot :8000│      │ Chatbot :8000│      │ Chatbot :8000│
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             │
                             │ HTTPS (encrypted)
                             │ backend.vmart.co.in
                             ▼
                    ┌──────────────────┐
                    │  Cloud Server    │
                    │  Backend :443    │
                    │  SSL/TLS         │
                    │  Firewall        │
                    └────────┬─────────┘
                             │
                             │ Private VPN
                             ▼
                  ┌────────────────────┐
                  │ Database Servers   │
                  │ (Cloud/Private)    │
                  └────────────────────┘

Advantages:
✅ Remote access anywhere
✅ Distributed teams
✅ Cloud scalability
⚠️ Requires SSL certificate
⚠️ Internet dependency
```

### Scenario 3: Hybrid Deployment

```
┌──────────────────────────────────────────────────────────────┐
│                   HYBRID NETWORK                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  LAN Users (Office)                                          │
│  ┌──────────┐  ┌──────────┐                                 │
│  │ Desktop 1│  │ Desktop 2│                                 │
│  │ Chatbot  │  │ Chatbot  │                                 │
│  └────┬─────┘  └────┬─────┘                                 │
│       │             │                                        │
│       │ HTTP (LAN)  │                                        │
│       └─────────┬───┘                                        │
│                 │                                            │
│                 ▼                                            │
│        ┌──────────────────┐                                 │
│        │ Backend Server   │◄────────────────┐               │
│        │ 192.168.1.100    │                 │               │
│        │ Port: 5000 (LAN) │                 │               │
│        │ Port: 443 (WAN)  │                 │               │
│        └──────────────────┘                 │               │
│                                             │               │
└─────────────────────────────────────────────┼───────────────┘
                                              │
                                              │ HTTPS (WAN)
                                              │
                       ┌──────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ Remote 1 │ │ Remote 2 │ │ Remote 3 │
    │ Chatbot  │ │ Chatbot  │ │ Chatbot  │
    └──────────┘ └──────────┘ └──────────┘
    
    WAN Users (Remote)

Advantages:
✅ Best of both worlds
✅ Fast for office users
✅ Remote access for others
✅ Flexible scaling
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: Network Security                                  │
│  ┌───────────────────────────────────────────────────┐     │
│  │ • Firewall Rules (UFW/iptables)                   │     │
│  │ • IP Whitelisting (optional)                      │     │
│  │ • SSL/TLS 1.3 Encryption                          │     │
│  │ • VPN (for sensitive deployments)                 │     │
│  └───────────────────────────────────────────────────┘     │
│                           │                                 │
│                           ▼                                 │
│  Layer 2: API Authentication                                │
│  ┌───────────────────────────────────────────────────┐     │
│  │ • Bearer Token (API Keys)                         │     │
│  │ • Unique per user/agent                           │     │
│  │ • Stored securely (~/.vmart/api_keys.json)        │     │
│  │ • Can be rotated/revoked                          │     │
│  └───────────────────────────────────────────────────┘     │
│                           │                                 │
│                           ▼                                 │
│  Layer 3: Authorization (RBAC)                              │
│  ┌───────────────────────────────────────────────────┐     │
│  │ Permissions:                                      │     │
│  │ • db_read      - Read database data               │     │
│  │ • db_write     - Modify database data             │     │
│  │ • db_admin     - Manage connections               │     │
│  │ • ai_insights  - Use AI features                  │     │
│  │ • user_admin   - Manage users                     │     │
│  │ • all          - Full admin access                │     │
│  └───────────────────────────────────────────────────┘     │
│                           │                                 │
│                           ▼                                 │
│  Layer 4: Rate Limiting                                     │
│  ┌───────────────────────────────────────────────────┐     │
│  │ • 100 requests per hour (default)                 │     │
│  │ • Per API key tracking                            │     │
│  │ • Sliding window algorithm                        │     │
│  │ • HTTP 429 on limit exceeded                      │     │
│  └───────────────────────────────────────────────────┘     │
│                           │                                 │
│                           ▼                                 │
│  Layer 5: Data Security                                     │
│  ┌───────────────────────────────────────────────────┐     │
│  │ • Fernet Encryption (credentials)                 │     │
│  │ • Separate key storage (~/.vmart/.key)            │     │
│  │ • Permissions: 600 (owner only)                   │     │
│  │ • No credentials in logs                          │     │
│  └───────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

**Developed by**: DSR  
**Version**: 2.0  
**Last Updated**: November 9, 2025
