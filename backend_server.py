#!/usr/bin/env python3
"""
V-Mart Backend Server - Standalone Central Data Management API

This is a standalone server that provides centralized database connectivity
and data management services. It can be accessed by chatbot agents over
LAN or WAN via REST API.

Features:
- Database connectors (ClickHouse, PostgreSQL, Oracle, SQL Server, Tableau, Google Drive, File System)
- AI insights engine
- RBAC with 23 granular permissions
- Encrypted credential storage
- API key authentication
- Rate limiting
- Health monitoring

Deployment:
  LAN:  python backend_server.py --host 192.168.1.100 --port 5000
  WAN:  python backend_server.py --host 0.0.0.0 --port 5000 --ssl

Usage:
  python backend_server.py [options]

Options:
  --host HOST        Host to bind (default: 0.0.0.0)
  --port PORT        Port to listen (default: 5000)
  --ssl              Enable HTTPS
  --cert PATH        SSL certificate path
  --key PATH         SSL key path
  --config PATH      Config file path
  --generate-key     Generate API key

Developed by: DSR
Version: 1.0.0
"""

import argparse
import json
import os
import secrets
import sys
import time
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from backend.ai_insights import AIInsightsEngine
from backend.config_manager import config_manager
from backend.db_manager import db_manager
from backend.rbac import Permission

# Flask app
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Configuration
CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "ssl_enabled": False,
    "ssl_cert": None,
    "ssl_key": None,
    "api_keys_file": os.path.expanduser("~/.vmart/api_keys.json"),
    "rate_limit": 100,  # requests per hour per key
    "log_file": "logs/backend.log",
}

# Runtime stats
STATS = {
    "start_time": datetime.now(),
    "total_requests": 0,
    "total_errors": 0,
    "active_connections": 0,
}

# Request tracking for rate limiting
REQUEST_TRACKING: Dict[str, list] = {}


# ============================================================================
# Security & Authentication
# ============================================================================


def load_api_keys() -> Dict[str, Dict[str, Any]]:
    """Load API keys from encrypted file"""
    keys_file = Path(CONFIG["api_keys_file"])
    if not keys_file.exists():
        # Create default admin key
        default_keys = {
            "admin_key_default": {
                "name": "Default Admin",
                "permissions": ["all"],
                "created": datetime.now().isoformat(),
                "last_used": None,
            }
        }
        keys_file.parent.mkdir(parents=True, exist_ok=True)
        keys_file.write_text(json.dumps(default_keys, indent=2))
        print(f"⚠️  Created default API key file: {keys_file}")
        print("🔑 Default API key: admin_key_default")
        return default_keys

    try:
        return json.loads(keys_file.read_text())
    except Exception as e:
        print(f"❌ Error loading API keys: {e}")
        return {}


def save_api_keys(keys: Dict[str, Dict[str, Any]]) -> None:
    """Save API keys to file"""
    keys_file = Path(CONFIG["api_keys_file"])
    keys_file.parent.mkdir(parents=True, exist_ok=True)
    keys_file.write_text(json.dumps(keys, indent=2))
    os.chmod(keys_file, 0o600)  # Secure permissions


def generate_api_key(name: str, permissions: list) -> str:
    """Generate a new API key"""
    api_key = f"vmart_{secrets.token_urlsafe(32)}"
    keys = load_api_keys()
    keys[api_key] = {
        "name": name,
        "permissions": permissions,
        "created": datetime.now().isoformat(),
        "last_used": None,
    }
    save_api_keys(keys)
    return api_key


def validate_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    """Validate API key and return key info"""
    keys = load_api_keys()
    if api_key in keys:
        # Update last used timestamp
        keys[api_key]["last_used"] = datetime.now().isoformat()
        save_api_keys(keys)
        return keys[api_key]
    return None


def check_rate_limit(api_key: str) -> bool:
    """Check if API key has exceeded rate limit"""
    now = time.time()
    hour_ago = now - 3600

    # Clean old requests
    if api_key in REQUEST_TRACKING:
        REQUEST_TRACKING[api_key] = [
            t for t in REQUEST_TRACKING[api_key] if t > hour_ago
        ]
    else:
        REQUEST_TRACKING[api_key] = []

    # Check limit
    if len(REQUEST_TRACKING[api_key]) >= CONFIG["rate_limit"]:
        return False

    # Add current request
    REQUEST_TRACKING[api_key].append(now)
    return True


def require_api_key(f):
    """Decorator to require API key authentication"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        api_key = auth_header[7:]  # Remove "Bearer "

        # Validate key
        key_info = validate_api_key(api_key)
        if not key_info:
            return jsonify({"error": "Invalid API key"}), 401

        # Check rate limit
        if not check_rate_limit(api_key):
            return (
                jsonify(
                    {
                        "error": "Rate limit exceeded",
                        "limit": CONFIG["rate_limit"],
                        "window": "1 hour",
                    }
                ),
                429,
            )

        # Add key info to request context
        request.api_key_info = key_info
        return f(*args, **kwargs)

    return decorated_function


def require_permission(permission: Permission):
    """Decorator to require specific permission"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            key_info = getattr(request, "api_key_info", None)
            if not key_info:
                return jsonify({"error": "Unauthorized"}), 401

            # Check if key has permission
            permissions = key_info.get("permissions", [])
            if "all" not in permissions and permission.value not in permissions:
                return (
                    jsonify(
                        {
                            "error": "Insufficient permissions",
                            "required": permission.value,
                        }
                    ),
                    403,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# ============================================================================
# Middleware & Error Handlers
# ============================================================================


@app.before_request
def log_request():
    """Log incoming requests"""
    STATS["total_requests"] += 1
    print(f"[{datetime.now()}] {request.method} {request.path}")


@app.after_request
def add_headers(response):
    """Add security headers"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handle HTTP exceptions"""
    STATS["total_errors"] += 1
    return jsonify({"error": e.description}), e.code


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all other exceptions"""
    STATS["total_errors"] += 1
    print(f"❌ Error: {e}")
    return jsonify({"error": "Internal server error", "details": str(e)}), 500


# ============================================================================
# Health & Monitoring Endpoints
# ============================================================================


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint (no auth required)"""
    uptime = (datetime.now() - STATS["start_time"]).total_seconds()
    return jsonify(
        {
            "status": "ok",
            "uptime_seconds": uptime,
            "total_requests": STATS["total_requests"],
            "total_errors": STATS["total_errors"],
            "active_connections": STATS["active_connections"],
            "version": "1.0.0",
        }
    )


@app.route("/api/stats", methods=["GET"])
@require_api_key
def get_stats():
    """Get server statistics"""
    uptime = (datetime.now() - STATS["start_time"]).total_seconds()
    return jsonify(
        {
            "uptime_seconds": uptime,
            "total_requests": STATS["total_requests"],
            "total_errors": STATS["total_errors"],
            "error_rate": (
                STATS["total_errors"] / STATS["total_requests"]
                if STATS["total_requests"] > 0
                else 0
            ),
            "active_connections": STATS["active_connections"],
            "request_tracking": {
                k: len(v) for k, v in REQUEST_TRACKING.items()
            },  # Don't expose actual timestamps
        }
    )


# ============================================================================
# Database Connection Management
# ============================================================================


@app.route("/api/connections", methods=["GET"])
@require_api_key
@require_permission(Permission.DB_READ)
def list_connections():
    """List all database connections"""
    connections = config_manager.list_database_connections()
    return jsonify({"connections": connections})


@app.route("/api/connections", methods=["POST"])
@require_api_key
@require_permission(Permission.DB_ADMIN)
def create_connection():
    """Create a new database connection"""
    data = request.get_json() or {}
    name = data.get("name")
    db_type = data.get("type")
    params = data.get("params", {})

    if not name or not db_type:
        return jsonify({"error": "Name and type are required"}), 400

    try:
        config_manager.add_database_connection(name, db_type, params)
        return jsonify({"status": "success", "connection": name}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/connections/<name>", methods=["DELETE"])
@require_api_key
@require_permission(Permission.DB_ADMIN)
def delete_connection(name):
    """Delete a database connection"""
    try:
        success = config_manager.delete_credentials(f"db_{name}")
        if success:
            return jsonify({"status": "success"})
        else:
            return jsonify({"error": "Connection not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ============================================================================
# Query Execution
# ============================================================================


@app.route("/api/query", methods=["POST"])
@require_api_key
@require_permission(Permission.DB_READ)
def execute_query():
    """Execute a database query"""
    data = request.get_json() or {}
    connection_name = data.get("connection")
    query = data.get("query")
    params = data.get("params")

    if not connection_name or not query:
        return jsonify({"error": "Connection and query are required"}), 400

    try:
        STATS["active_connections"] += 1
        connection = db_manager.get_connection(connection_name)
        result = connection.execute_query(query, params)
        STATS["active_connections"] -= 1
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        STATS["active_connections"] -= 1
        return jsonify({"error": str(e)}), 400


@app.route("/api/schema/<connection_name>", methods=["GET"])
@require_api_key
@require_permission(Permission.DB_READ)
def get_schema(connection_name):
    """Get schema information for a database"""
    try:
        connection = db_manager.get_connection(connection_name)
        schema = connection.get_schema()
        return jsonify({"status": "success", "schema": schema})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ============================================================================
# AI Insights
# ============================================================================

# Initialize AI Insights Engine
ai_insights = None


def get_ai_insights_engine():
    """Lazy load AI insights engine"""
    global ai_insights
    if ai_insights is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")
        ai_insights = AIInsightsEngine(api_key=api_key)
    return ai_insights


@app.route("/api/ai/analyze", methods=["POST"])
@require_api_key
@require_permission(Permission.AI_INSIGHTS)
def analyze_data():
    """Analyze data with AI insights"""
    data = request.get_json() or {}
    connection_name = data.get("connection")
    query = data.get("query")
    analysis_type = data.get("analysis_type", "general")

    if not connection_name or not query:
        return jsonify({"error": "Connection and query are required"}), 400

    try:
        # Get AI engine
        engine = get_ai_insights_engine()

        # Execute query
        connection = db_manager.get_connection(connection_name)
        result = connection.execute_query(query)

        # Analyze
        insights = engine.analyze_query_results(result, analysis_type)
        return jsonify({"status": "success", "insights": insights})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/ai/recommend", methods=["POST"])
@require_api_key
@require_permission(Permission.AI_INSIGHTS)
def get_recommendations():
    """Get recommendations based on data"""
    data = request.get_json() or {}
    connection_name = data.get("connection")
    context = data.get("context", "")

    if not connection_name:
        return jsonify({"error": "Connection is required"}), 400

    try:
        # Get AI engine
        engine = get_ai_insights_engine()

        # Get schema for context
        connection = db_manager.get_connection(connection_name)
        schema = connection.get_schema()

        # Generate recommendations
        recommendations = engine.generate_recommendations(schema, context)
        return jsonify({"status": "success", "recommendations": recommendations})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ============================================================================
# User & Role Management (RBAC)
# ============================================================================


@app.route("/api/users", methods=["GET"])
@require_api_key
@require_permission(Permission.USER_ADMIN)
def list_users():
    """List all users"""
    # This would list users from RBAC system
    # For now, return API key info
    keys = load_api_keys()
    users = [{"api_key": k[:20] + "...", **v} for k, v in keys.items()]
    return jsonify({"users": users})


@app.route("/api/users", methods=["POST"])
@require_api_key
@require_permission(Permission.USER_ADMIN)
def create_user():
    """Create a new user (API key)"""
    data = request.get_json() or {}
    name = data.get("name")
    permissions = data.get("permissions", [])

    if not name:
        return jsonify({"error": "Name is required"}), 400

    try:
        api_key = generate_api_key(name, permissions)
        return (
            jsonify(
                {
                    "status": "success",
                    "api_key": api_key,
                    "warning": "Save this key securely, it won't be shown again",
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/config", methods=["GET"])
@require_api_key
def get_config():
    """Get server configuration (sanitized)"""
    return jsonify(
        {
            "rate_limit": CONFIG["rate_limit"],
            "ssl_enabled": CONFIG["ssl_enabled"],
            "version": "1.0.0",
        }
    )


# ============================================================================
# CLI Commands
# ============================================================================


def cmd_generate_key(args):
    """Generate a new API key"""
    permissions = args.permissions.split(",") if args.permissions else ["db_read"]
    api_key = generate_api_key(args.name, permissions)

    print("=" * 60)
    print("✅ API Key Generated Successfully")
    print("=" * 60)
    print(f"Name:        {args.name}")
    print(f"Permissions: {', '.join(permissions)}")
    print(f"\nAPI Key:     {api_key}")
    print("\n⚠️  Save this key securely - it won't be shown again!")
    print("=" * 60)


def cmd_list_keys(args):
    """List all API keys"""
    keys = load_api_keys()

    print("=" * 80)
    print("API Keys")
    print("=" * 80)
    for key, info in keys.items():
        print(f"\nKey: {key[:20]}...")
        print(f"  Name:        {info.get('name')}")
        print(f"  Permissions: {', '.join(info.get('permissions', []))}")
        print(f"  Created:     {info.get('created')}")
        print(f"  Last Used:   {info.get('last_used', 'Never')}")
    print("=" * 80)


def cmd_run_server(args):
    """Run the backend server"""
    # Update config
    CONFIG["host"] = args.host
    CONFIG["port"] = args.port
    CONFIG["ssl_enabled"] = args.ssl

    if args.ssl:
        if not args.cert or not args.key:
            print("❌ SSL enabled but --cert and --key not provided")
            sys.exit(1)
        CONFIG["ssl_cert"] = args.cert
        CONFIG["ssl_key"] = args.key

    # Print banner
    print("=" * 80)
    print("🚀 V-Mart Backend Server")
    print("=" * 80)
    print(f"Host:     {CONFIG['host']}")
    print(f"Port:     {CONFIG['port']}")
    print(f"SSL:      {'Enabled' if CONFIG['ssl_enabled'] else 'Disabled'}")
    print(f"API Keys: {CONFIG['api_keys_file']}")
    print(f"Rate Limit: {CONFIG['rate_limit']} req/hour")
    print("=" * 80)
    print("\n📡 Server starting...\n")

    # Run Flask app
    if CONFIG["ssl_enabled"]:
        app.run(
            host=CONFIG["host"],
            port=CONFIG["port"],
            ssl_context=(CONFIG["ssl_cert"], CONFIG["ssl_key"]),
            debug=False,
        )
    else:
        app.run(host=CONFIG["host"], port=CONFIG["port"], debug=False)


# ============================================================================
# Main Entry Point
# ============================================================================


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="V-Mart Backend Server - Central Data Management API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run server on LAN
  python backend_server.py --host 192.168.1.100 --port 5000
  
  # Run server with SSL for WAN
  python backend_server.py --host 0.0.0.0 --port 5000 --ssl --cert cert.pem --key key.pem
  
  # Generate API key
  python backend_server.py generate-key --name "chatbot-user1" --permissions "db_read,ai_insights"
  
  # List API keys
  python backend_server.py list-keys
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Run server command (default)
    run_parser = subparsers.add_parser("run", help="Run the backend server")
    run_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)"
    )
    run_parser.add_argument(
        "--port", type=int, default=5000, help="Port to listen (default: 5000)"
    )
    run_parser.add_argument("--ssl", action="store_true", help="Enable HTTPS")
    run_parser.add_argument("--cert", help="SSL certificate path")
    run_parser.add_argument("--key", help="SSL key path")

    # Generate key command
    gen_parser = subparsers.add_parser("generate-key", help="Generate API key")
    gen_parser.add_argument("--name", required=True, help="Name for the API key")
    gen_parser.add_argument(
        "--permissions", help="Comma-separated permissions (default: db_read)"
    )

    # List keys command
    subparsers.add_parser("list-keys", help="List all API keys")

    args = parser.parse_args()

    # Default to run if no command specified
    if not args.command:
        args.command = "run"
        args.host = "0.0.0.0"
        args.port = 5000
        args.ssl = False
        args.cert = None
        args.key = None

    # Execute command
    if args.command == "run":
        cmd_run_server(args)
    elif args.command == "generate-key":
        cmd_generate_key(args)
    elif args.command == "list-keys":
        cmd_list_keys(args)


if __name__ == "__main__":
    main()
