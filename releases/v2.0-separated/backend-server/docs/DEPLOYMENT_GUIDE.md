# V-Mart AI Agent - Deployment Guide

## Overview

This guide covers deploying the V-Mart AI Agent in a **separated architecture** where:
- **Backend Server** runs on a central server (LAN/WAN accessible)
- **Chatbot Agents** run on individual user systems
- Communication happens over HTTP/HTTPS via REST API

## Quick Start

### Option 1: All-in-One (Development)

Run both backend and chatbot on the same machine:

```bash
# Terminal 1: Start backend server
python3 backend_server.py

# Terminal 2: Start chatbot agent  
export BACKEND_URL="http://localhost:5000"
export BACKEND_API_KEY="admin_key_default"
python3 src/web/app.py
```

### Option 2: Separated (Production)

**On Central Server**:
```bash
./deploy_backend.sh
```

**On User Systems**:
```bash
export BACKEND_URL="https://backend.vmart.co.in:5000"
export BACKEND_API_KEY="your-api-key-here"
./deploy_chatbot.sh
```

---

## Backend Server Deployment

### 1. System Requirements

**Hardware**:
- CPU: 4+ cores recommended
- RAM: 8GB+ recommended
- Disk: 20GB+ for logs and cache
- Network: Static IP or domain name

**Software**:
- Python 3.8+
- pip
- (Optional) SSL certificates for HTTPS
- (Optional) systemd for service management

### 2. Installation

```bash
# Clone repository
git clone https://github.com/yourusername/V-Mart-Personal-AI-Agent.git
cd V-Mart-Personal-AI-Agent

# Install backend dependencies
pip install -r backend_requirements.txt

# Create required directories
mkdir -p logs ~/.vmart
chmod 700 ~/.vmart
```

### 3. Configuration

**Environment Variables** (`.env` or system):
```bash
# Required
export GEMINI_API_KEY="your-gemini-api-key"

# Optional
export BACKEND_HOST="0.0.0.0"      # Listen on all interfaces
export BACKEND_PORT="5000"          # Port to use
export BACKEND_SSL="false"          # Enable SSL
```

**Config File** (`config/backend_config.yaml`):
```yaml
server:
  host: "0.0.0.0"
  port: 5000
  
security:
  rate_limit:
    requests_per_hour: 100
    
logging:
  level: "INFO"
  file:
    path: "logs/backend.log"
```

### 4. Generate API Keys

Create API keys for chatbot agents:

```bash
# Generate admin key
python3 backend_server.py generate-key \
  --name "Admin User" \
  --permissions "all"

# Generate read-only key
python3 backend_server.py generate-key \
  --name "Chatbot Agent 1" \
  --permissions "db_read,ai_insights"

# List all keys
python3 backend_server.py list-keys
```

**Save the generated API keys securely!** They won't be shown again.

### 5. Start Backend Server

**Development Mode**:
```bash
python3 backend_server.py
```

**Production Mode (Gunicorn)**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend_server:app
```

**Production with SSL**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 \
  --certfile=/path/to/cert.pem \
  --keyfile=/path/to/key.pem \
  backend_server:app
```

**Systemd Service** (recommended for production):

Create `/etc/systemd/system/vmart-backend.service`:
```ini
[Unit]
Description=V-Mart Backend Server
After=network.target

[Service]
Type=simple
User=vmart
WorkingDirectory=/opt/vmart-backend
Environment="GEMINI_API_KEY=your-key-here"
ExecStart=/usr/bin/python3 backend_server.py --host 0.0.0.0 --port 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable vmart-backend
sudo systemctl start vmart-backend
sudo systemctl status vmart-backend
```

### 6. Verify Backend

```bash
# Health check
curl http://localhost:5000/health

# Expected output:
# {"status":"ok","uptime_seconds":123,...}

# Check stats (requires API key)
curl -H "Authorization: Bearer admin_key_default" \
  http://localhost:5000/api/stats
```

---

## Chatbot Agent Deployment

### 1. System Requirements

**Hardware**:
- CPU: 2+ cores
- RAM: 4GB+
- Disk: 5GB+
- Network: Internet connection (for backend, Gemini, OAuth)

**Software**:
- Python 3.8+
- pip
- Web browser (for UI)

### 2. Installation

```bash
# Clone repository (or copy chatbot folder)
git clone https://github.com/yourusername/V-Mart-Personal-AI-Agent.git
cd V-Mart-Personal-AI-Agent

# Install chatbot dependencies
pip install -r chatbot_requirements.txt
```

### 3. Configuration

**Environment Variables** (`.env`):
```bash
# Backend connection (REQUIRED)
export BACKEND_URL="https://backend.vmart.co.in:5000"
export BACKEND_API_KEY="your-api-key-from-admin"

# Google OAuth (for login)
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"

# Gemini AI (for chatbot)
export GEMINI_API_KEY="your-gemini-key"
```

**LAN Configuration** (if backend on local network):
```bash
export BACKEND_URL="http://192.168.1.100:5000"
export BACKEND_API_KEY="admin_key_default"
```

**Config File** (`config/chatbot_config.yaml`):
```yaml
chatbot:
  port: 8000

backend:
  url: "${BACKEND_URL}"
  api_key: "${BACKEND_API_KEY}"
  timeout: 30
  cache:
    enabled: true
    ttl: 300
```

### 4. Start Chatbot Agent

**Manual**:
```bash
python3 src/web/app.py
```

**Using Deployment Script**:
```bash
./deploy_chatbot.sh
```

**Access UI**:
Open browser: `http://localhost:8000`

### 5. Verify Chatbot

1. Open `http://localhost:8000`
2. Login with Google or use demo mode
3. Check backend connection status in UI
4. Try a query that uses backend data

---

## Network Configuration

### LAN Deployment

**Backend Server** (central server on local network):
```
IP: 192.168.1.100
Port: 5000
URL: http://192.168.1.100:5000
```

**Chatbot Agents** (user machines):
```bash
export BACKEND_URL="http://192.168.1.100:5000"
```

**Firewall Rules**:
```bash
# On backend server, allow port 5000
sudo ufw allow 5000/tcp
```

**Advantages**:
- ✅ Fast, low latency
- ✅ No internet required
- ✅ Secure (local network only)
- ✅ Ideal for offices/enterprises

### WAN Deployment

**Backend Server** (public or VPN-accessible):
```
Domain: backend.vmart.co.in
Port: 5000 (HTTPS: 443)
URL: https://backend.vmart.co.in
```

**DNS Configuration**:
```
A Record: backend.vmart.co.in → your-server-ip
```

**SSL Certificate** (required for HTTPS):
```bash
# Using Let's Encrypt
sudo certbot certonly --standalone -d backend.vmart.co.in

# Certificate paths:
# cert: /etc/letsencrypt/live/backend.vmart.co.in/fullchain.pem
# key:  /etc/letsencrypt/live/backend.vmart.co.in/privkey.pem
```

**Chatbot Agents**:
```bash
export BACKEND_URL="https://backend.vmart.co.in"
```

**Firewall Rules**:
```bash
# On backend server
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 5000/tcp # If using custom port
```

**Advantages**:
- ✅ Remote access from anywhere
- ✅ Distributed teams
- ✅ Cloud deployment
- ⚠️ Requires internet
- ⚠️ SSL/TLS required

### Hybrid Deployment

Use both LAN (office) and WAN (remote workers):

**Backend Server**:
- Listen on `0.0.0.0:5000` (all interfaces)
- Configure firewall for both local and public access

**LAN Agents**:
```bash
export BACKEND_URL="http://192.168.1.100:5000"
```

**WAN Agents**:
```bash
export BACKEND_URL="https://backend.vmart.co.in:5000"
```

---

## Security

### API Key Management

**Generate Keys**:
```bash
python3 backend_server.py generate-key \
  --name "User Name" \
  --permissions "db_read,ai_insights"
```

**Available Permissions**:
- `all` - Full admin access
- `db_read` - Read database data
- `db_write` - Modify database data
- `db_admin` - Manage connections
- `ai_insights` - Use AI features
- `user_admin` - Manage users

**Rotate Keys**:
```bash
# Generate new key
python3 backend_server.py generate-key --name "User" --permissions "db_read"

# Update chatbot .env
export BACKEND_API_KEY="new-key-here"

# Delete old key from ~/.vmart/api_keys.json
```

### SSL/TLS Setup

**Self-Signed Certificate** (development/testing):
```bash
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes
```

**Let's Encrypt** (production):
```bash
sudo certbot certonly --standalone \
  -d backend.vmart.co.in \
  --agree-tos \
  --email admin@vmart.co.in
```

**Configure Backend**:
```bash
python3 backend_server.py \
  --host 0.0.0.0 \
  --port 5000 \
  --ssl \
  --cert /etc/letsencrypt/live/backend.vmart.co.in/fullchain.pem \
  --key /etc/letsencrypt/live/backend.vmart.co.in/privkey.pem
```

### Firewall Configuration

**Backend Server**:
```bash
# UFW (Ubuntu/Debian)
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 5000/tcp  # Backend port
sudo ufw allow 443/tcp   # HTTPS (if using)

# firewalld (RHEL/CentOS)
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

**IP Whitelisting** (optional):

Edit `config/backend_config.yaml`:
```yaml
security:
  ip_whitelist:
    - "192.168.1.0/24"   # LAN
    - "203.0.113.10"     # Specific IP
```

---

## Database Connection Setup

### Add Database Connection

**Via API** (from chatbot or curl):
```bash
curl -X POST http://backend.vmart.co.in:5000/api/connections \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "postgres_prod",
    "type": "postgres",
    "params": {
      "host": "db.example.com",
      "port": 5432,
      "database": "production",
      "username": "dbuser",
      "password": "dbpass"
    }
  }'
```

**Via Python**:
```python
from backend_client import BackendClient

client = BackendClient(
    base_url="https://backend.vmart.co.in:5000",
    api_key="your-api-key"
)

client.create_connection(
    name="postgres_prod",
    db_type="postgres",
    params={
        "host": "db.example.com",
        "port": 5432,
        "database": "production",
        "username": "dbuser",
        "password": "dbpass"
    }
)
```

### Supported Database Types

- `clickhouse` - ClickHouse
- `postgres` - PostgreSQL
- `oracle` - Oracle Database
- `sqlserver` - Microsoft SQL Server
- `tableau` - Tableau Server
- `gdrive` - Google Drive
- `filesystem` - Local/Network File System

---

## Monitoring

### Health Checks

**Backend**:
```bash
# Simple health check
curl http://backend.vmart.co.in:5000/health

# Detailed stats (requires API key)
curl -H "Authorization: Bearer your-api-key" \
  http://backend.vmart.co.in:5000/api/stats
```

**Chatbot**:
```python
from backend_client import BackendClient

client = BackendClient(...)
if client.health_check():
    print("✅ Backend connected")
else:
    print("❌ Backend offline")
```

### Logs

**Backend Logs**:
```bash
# Live tail
tail -f logs/backend.log

# Filter errors
grep ERROR logs/backend.log

# Last 100 lines
tail -100 logs/backend.log
```

**Chatbot Logs**:
```bash
tail -f logs/chatbot.log
```

### Metrics

Backend server exposes metrics at `/api/stats`:
- Uptime
- Total requests
- Error rate
- Active connections
- Request rate per API key

---

## Troubleshooting

### Backend Won't Start

**Check port availability**:
```bash
lsof -i :5000
# If port is in use, kill process or use different port
```

**Check Python version**:
```bash
python3 --version  # Should be 3.8+
```

**Check dependencies**:
```bash
pip install -r backend_requirements.txt
```

### Chatbot Can't Connect to Backend

**Test network connectivity**:
```bash
curl http://backend.vmart.co.in:5000/health
```

**Check API key**:
```bash
curl -H "Authorization: Bearer your-api-key" \
  http://backend.vmart.co.in:5000/api/stats
```

**Check firewall**:
```bash
# On backend server
sudo ufw status
```

### Database Connection Fails

**Test from backend server**:
```python
from backend.db_manager import db_manager

conn = db_manager.get_connection("postgres_prod")
result = conn.execute_query("SELECT 1")
print(result)
```

**Check credentials**:
```bash
# Stored in ~/.vmart/credentials.enc
ls -la ~/.vmart/
```

---

## Scaling

### Multiple Backend Servers

Use a load balancer (nginx, HAProxy):

```nginx
upstream backend_cluster {
    server 192.168.1.100:5000;
    server 192.168.1.101:5000;
    server 192.168.1.102:5000;
}

server {
    listen 80;
    server_name backend.vmart.co.in;
    
    location / {
        proxy_pass http://backend_cluster;
    }
}
```

### Multiple Chatbot Agents

Each user system can run its own chatbot agent.
All connect to the same backend server.

---

## Backup & Recovery

### Backup

**Backend Configuration**:
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz \
  ~/.vmart/ \
  config/ \
  logs/
```

**Database Credentials**:
```bash
# Encrypted in ~/.vmart/credentials.enc
cp ~/.vmart/credentials.enc ~/backup/
cp ~/.vmart/.key ~/backup/
```

### Restore

```bash
tar -xzf backup-20250109.tar.gz -C /
```

---

## Next Steps

1. ✅ Deploy backend server
2. ✅ Generate API keys
3. ✅ Deploy chatbot agents
4. ✅ Configure database connections
5. ✅ Test end-to-end
6. ✅ Set up monitoring
7. ✅ Configure backups

**Need Help?**
- See: `docs/ARCHITECTURE_SEPARATION.md`
- See: `docs/BACKEND_MANAGER.md`
- Issues: https://github.com/yourusername/V-Mart-Personal-AI-Agent/issues

---

**Developed by**: DSR  
**Version**: 2.0  
**Last Updated**: November 9, 2025
