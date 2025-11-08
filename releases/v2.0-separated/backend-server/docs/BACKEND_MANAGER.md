# Backend Manager Documentation

## Overview

The V-Mart AI Agent Backend Manager is a comprehensive enterprise-grade system for connecting to multiple data sources, executing queries, and providing AI-powered insights and recommendations.

## Architecture

### Core Components

1. **Database Connection Manager** (`db_manager.py`)
   - Abstract base class for all database connections
   - Connection pooling with automatic management
   - Unified interface for different database types

2. **Database Connectors**
   - **ClickHouse** (`clickhouse_connector.py`) - High-performance analytics database
   - **PostgreSQL** (`postgres_connector.py`) - Advanced relational database
   - **Oracle** (`oracle_connector.py`) - Enterprise database system
   - **SQL Server** (`sqlserver_connector.py`) - Microsoft SQL Server

3. **Data Source Connectors**
   - **Tableau** (`tableau_connector.py`) - Business intelligence and analytics
   - **Google Drive** (`gdrive_connector.py`) - Cloud file storage
   - **File System** (`filesystem_connector.py`) - Local and network drives

4. **AI Insights Engine** (`ai_insights.py`)
   - Powered by Google Gemini AI
   - Data analysis and pattern recognition
   - Actionable recommendations
   - Question answering

5. **RBAC System** (`rbac.py`)
   - Role-based access control
   - User and permission management
   - 4 default roles: admin, analyst, viewer, developer

6. **Configuration Manager** (`config_manager.py`)
   - Secure credential storage with encryption
   - Configuration management
   - API key management

## Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Database drivers (optional, based on your needs)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Database-Specific Drivers

For **SQL Server** on macOS/Linux, install ODBC Driver:
```bash
# macOS
brew install unixodbc
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql18 mssql-tools18

# Ubuntu/Debian
sudo apt-get install unixodbc unixodbc-dev
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install msodbcsql18 mssql-tools18
```

## Configuration

### Environment Variables

Create a `.env` file:

```env
# Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# Flask Secret
SECRET_KEY=your_secret_key
```

### Database Connections

Database credentials are stored securely in `~/.vmart/credentials.enc`.

## API Reference

### Database Management

#### List Connections
```http
GET /backend/connections
```

Response:
```json
{
  "connections": ["db1", "db2", "db3"]
}
```

#### Create Connection
```http
POST /backend/connections
Content-Type: application/json

{
  "name": "my_postgres",
  "type": "postgresql",
  "params": {
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "user": "admin",
    "password": "secret"
  }
}
```

#### Execute Query
```http
POST /backend/query
Content-Type: application/json

{
  "connection": "my_postgres",
  "query": "SELECT * FROM users LIMIT 10"
}
```

Response:
```json
{
  "result": [
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Jane", "email": "jane@example.com"}
  ]
}
```

#### Get Schema
```http
GET /backend/schema/my_postgres
```

Response:
```json
{
  "schema": {
    "tables": [
      {
        "name": "users",
        "columns": [
          {"name": "id", "type": "integer"},
          {"name": "name", "type": "varchar"},
          {"name": "email", "type": "varchar"}
        ]
      }
    ]
  }
}
```

### AI Analytics

#### Analyze Data
```http
POST /backend/ai/analyze
Content-Type: application/json

{
  "data": [
    {"date": "2025-01-01", "sales": 1000},
    {"date": "2025-01-02", "sales": 1200}
  ],
  "context": {
    "source": "sales_database",
    "table": "daily_sales"
  }
}
```

Response:
```json
{
  "summary": "Sales data showing upward trend",
  "insights": [
    {
      "type": "trend",
      "description": "20% increase in sales",
      "importance": "high"
    }
  ],
  "recommendations": [
    {
      "action": "Increase inventory",
      "rationale": "Sales trending up",
      "priority": "high"
    }
  ]
}
```

#### Get Recommendations
```http
POST /backend/ai/recommend
Content-Type: application/json

{
  "data": {"revenue": 100000, "costs": 80000},
  "goal": "Improve profit margins"
}
```

### User Management

#### List Users
```http
GET /backend/users
```

#### Create User
```http
POST /backend/users
Content-Type: application/json

{
  "username": "analyst1",
  "email": "analyst1@company.com",
  "roles": ["analyst"]
}
```

#### Update User Roles
```http
PUT /backend/users/analyst1/roles
Content-Type: application/json

{
  "roles": ["analyst", "developer"]
}
```

#### Delete User
```http
DELETE /backend/users/analyst1
```

### Role Management

#### List Roles
```http
GET /backend/roles
```

Response:
```json
{
  "roles": [
    {
      "name": "admin",
      "description": "System administrator with full access",
      "permissions": ["db:admin", "user:write", "system:admin"]
    },
    {
      "name": "analyst",
      "description": "Data analyst with read access and AI capabilities",
      "permissions": ["db:query", "ai:analyze", "ai:recommend"]
    }
  ]
}
```

#### Create Custom Role
```http
POST /backend/roles
Content-Type: application/json

{
  "name": "custom_role",
  "description": "Custom role for specific needs",
  "permissions": ["db:query", "file:read"]
}
```

### Configuration

#### Get Configuration
```http
GET /backend/config
```

#### Update Configuration
```http
PUT /backend/config
Content-Type: application/json

{
  "key": "database.max_connections",
  "value": 30
}
```

## Python SDK Usage

### Database Connections

```python
from backend.db_manager import db_manager
from backend.clickhouse_connector import ClickHouseConnection

# Register ClickHouse connector
db_manager.register_database_type("clickhouse", ClickHouseConnection)

# Create connection
connection_params = {
    "host": "localhost",
    "port": 9000,
    "user": "default",
    "password": "",
    "database": "default"
}

db_manager.create_connection("my_clickhouse", "clickhouse", connection_params)

# Execute query
results = db_manager.execute_query("my_clickhouse", "SELECT * FROM events LIMIT 5")
print(results)

# Get schema
schema = db_manager.get_schema("my_clickhouse")
print(schema)
```

### AI Insights

```python
from backend.ai_insights import AIInsightsEngine
import os

# Initialize AI engine
ai_engine = AIInsightsEngine(api_key=os.getenv("GEMINI_API_KEY"))

# Analyze data
data = [
    {"month": "Jan", "revenue": 50000},
    {"month": "Feb", "revenue": 55000},
    {"month": "Mar", "revenue": 60000}
]

context = {
    "source": "finance_db",
    "table": "monthly_revenue"
}

insights = ai_engine.analyze_data(data, context)
print(insights)

# Get recommendations
recommendations = ai_engine.generate_recommendations(
    data,
    goal="Increase revenue by 20%",
    context=context
)
print(recommendations)

# Answer questions
answer = ai_engine.answer_question(
    "What is the revenue trend?",
    data,
    context
)
print(answer)
```

### RBAC

```python
from backend.rbac import rbac_manager, Permission

# Create user
user = rbac_manager.create_user(
    "analyst1",
    "analyst1@company.com",
    ["analyst"]
)

# Check permissions
can_query = rbac_manager.check_permission("analyst1", Permission.DB_QUERY)
can_write = rbac_manager.check_permission("analyst1", Permission.DB_WRITE)

print(f"Can query: {can_query}")  # True
print(f"Can write: {can_write}")  # False

# Create custom role
custom_role = rbac_manager.create_role(
    "report_viewer",
    "Can view reports only",
    ["db:query", "datasource:read"]
)

# Assign role to user
rbac_manager.update_user_roles("analyst1", ["analyst", "report_viewer"])
```

### Configuration Management

```python
from backend.config_manager import config_manager

# Store database credentials
config_manager.add_database_connection(
    "prod_db",
    "postgresql",
    {
        "host": "prod.example.com",
        "port": 5432,
        "database": "production",
        "user": "app_user",
        "password": "secure_password"
    }
)

# Store API key
config_manager.add_api_key(
    "tableau",
    "your_tableau_token",
    {"server_url": "https://tableau.company.com"}
)

# Get configuration
max_conn = config_manager.get_config("database.max_connections")
print(f"Max connections: {max_conn}")

# Update configuration
config_manager.set_config("database.query_timeout", 600)

# Export configuration
config_manager.export_config("backup_config.json", include_credentials=False)
```

## Permissions Reference

### Database Permissions
- `db:connect` - Connect to databases
- `db:query` - Execute SELECT queries
- `db:write` - Execute INSERT/UPDATE/DELETE
- `db:admin` - Full database administration

### Data Source Permissions
- `datasource:read` - Read from data sources (Tableau, Drive)
- `datasource:write` - Write to data sources
- `datasource:admin` - Manage data sources

### File System Permissions
- `file:read` - Read files
- `file:write` - Write files
- `file:delete` - Delete files

### AI Permissions
- `ai:query` - Basic AI queries
- `ai:analyze` - Data analysis
- `ai:recommend` - Get recommendations

### User Management Permissions
- `user:read` - View users
- `user:write` - Create/update users
- `user:delete` - Delete users

### Role Management Permissions
- `role:read` - View roles
- `role:write` - Create/update roles
- `role:delete` - Delete roles

### System Permissions
- `system:config` - Manage configuration
- `system:admin` - System administration

## Default Roles

### Admin
Full system access including:
- All database operations
- User and role management
- System configuration
- All AI capabilities

### Analyst
Data analysis focused:
- Database queries (read-only)
- Data source reading
- AI analysis and recommendations
- File reading

### Viewer
Read-only access:
- Database queries
- Data source reading
- File reading
- Basic AI queries

### Developer
Development focused:
- Database read/write
- Data source read/write
- File read/write
- AI analysis

## Security Best Practices

1. **Credential Storage**
   - All credentials encrypted using Fernet (symmetric encryption)
   - Key stored separately in `~/.vmart/.key`
   - File permissions set to 600 (owner read/write only)

2. **API Key Management**
   - Store API keys in environment variables
   - Never commit `.env` files to version control
   - Use `config_manager` for secure storage

3. **Database Connections**
   - Use read-only accounts for analysts
   - Implement connection pooling to prevent resource exhaustion
   - Set query timeouts to prevent long-running queries

4. **Role Assignment**
   - Follow principle of least privilege
   - Create custom roles for specific use cases
   - Regularly audit user permissions

## Troubleshooting

### Database Connection Issues

**ClickHouse:**
```python
# Test connection
from backend.clickhouse_connector import ClickHouseConnection

conn = ClickHouseConnection("localhost", 9000, "default", "", "default")
if conn.test_connection():
    print("Connected successfully")
```

**PostgreSQL:**
```python
# Check if psycopg2 is installed
try:
    import psycopg2
    print(f"psycopg2 version: {psycopg2.__version__}")
except ImportError:
    print("psycopg2 not installed. Run: pip install psycopg2-binary")
```

**SQL Server:**
```bash
# Check ODBC drivers
odbcinst -q -d

# Should show "ODBC Driver 17 for SQL Server" or similar
```

### Permission Denied Errors

Check user permissions:
```python
from backend.rbac import rbac_manager

user = rbac_manager.get_user("username")
if user:
    permissions = user.get_all_permissions()
    print(f"User permissions: {[p.value for p in permissions]}")
```

### AI Engine Not Responding

Verify API key:
```python
import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("GEMINI_API_KEY not set!")
else:
    genai.configure(api_key=api_key)
    models = genai.list_models()
    print(f"Available models: {[m.name for m in models]}")
```

## Examples

### Complete Workflow Example

```python
from backend.db_manager import db_manager
from backend.postgres_connector import PostgreSQLConnection
from backend.ai_insights import AIInsightsEngine
from backend.rbac import rbac_manager, Permission
import os

# 1. Register database connector
db_manager.register_database_type("postgresql", PostgreSQLConnection)

# 2. Create connection
db_manager.create_connection(
    "analytics_db",
    "postgresql",
    {
        "host": "localhost",
        "port": 5432,
        "database": "analytics",
        "user": "analyst",
        "password": "password"
    }
)

# 3. Create analyst user
user = rbac_manager.create_user(
    "john_analyst",
    "john@company.com",
    ["analyst"]
)

# 4. Check permissions
if rbac_manager.check_permission("john_analyst", Permission.DB_QUERY):
    # 5. Execute query
    results = db_manager.execute_query(
        "analytics_db",
        "SELECT product, SUM(sales) as total_sales FROM sales GROUP BY product"
    )
    
    # 6. Analyze with AI
    ai_engine = AIInsightsEngine(api_key=os.getenv("GEMINI_API_KEY"))
    insights = ai_engine.analyze_data(
        results,
        context={"source": "analytics_db", "query": "product sales"}
    )
    
    print("Sales Analysis:")
    print(f"Summary: {insights.get('summary')}")
    
    for insight in insights.get('insights', []):
        print(f"- {insight['description']} (importance: {insight['importance']})")
    
    # 7. Get recommendations
    recommendations = ai_engine.generate_recommendations(
        results,
        goal="Optimize product mix",
        context={"source": "sales_data"}
    )
    
    print("\nRecommendations:")
    for rec in recommendations:
        print(f"- {rec['action']} ({rec['priority']} priority)")
        print(f"  Rationale: {rec['rationale']}")
```

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation
- Consult permission reference
- Verify environment variables

## License

Copyright © 2025 V-Mart Personal AI Agent
