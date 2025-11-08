"""
Backend Client SDK - HTTP Client for V-Mart Backend Server

This client library provides a simple interface for chatbot agents to
communicate with the backend server over LAN or WAN.

Features:
- Automatic API key injection
- Request retry with exponential backoff
- Response caching
- Graceful error handling
- Health check monitoring

Usage:
    from backend_client import BackendClient

    client = BackendClient(
        base_url="https://backend.vmart.co.in:5000",
        api_key=os.getenv("BACKEND_API_KEY")
    )

    # Query database
    result = client.execute_query(
        connection="postgres_prod",
        query="SELECT * FROM customers LIMIT 10"
    )

    # Get AI insights
    insights = client.analyze_data(
        connection="clickhouse_analytics",
        query="SELECT date, revenue FROM sales"
    )

Developed by: DSR
Version: 1.0.0
"""

import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests


class BackendConnectionError(Exception):
    """Backend server connection error"""

    pass


class BackendTimeoutError(Exception):
    """Backend server timeout error"""

    pass


class BackendAuthError(Exception):
    """Backend authentication error"""

    pass


class BackendClient:
    """HTTP client for V-Mart Backend Server"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        retry_attempts: int = 3,
        cache_ttl: int = 300,
        verify_ssl: bool = True,
    ):
        """
        Initialize Backend Client

        Args:
            base_url: Backend server URL (e.g., "https://backend.vmart.co.in:5000")
            api_key: API key for authentication
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts
            cache_ttl: Cache time-to-live in seconds
            verify_ssl: Verify SSL certificates (set False for self-signed)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.cache_ttl = cache_ttl
        self.verify_ssl = verify_ssl

        # Cache storage
        self._cache: Dict[str, Dict[str, Any]] = {}

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "V-Mart-Chatbot-Client/1.0",
            }
        )

    def _get_cache_key(self, endpoint: str, params: Optional[Dict] = None) -> str:
        """Generate cache key from endpoint and params"""
        if params:
            params_str = json.dumps(params, sort_keys=True)
            return f"{endpoint}:{params_str}"
        return endpoint

    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            expires_at = cached["expires_at"]
            if datetime.now() < expires_at:
                return cached["data"]
            else:
                # Remove expired entry
                del self._cache[cache_key]
        return None

    def _set_cache(self, cache_key: str, data: Any) -> None:
        """Set value in cache with TTL"""
        self._cache[cache_key] = {
            "data": data,
            "expires_at": datetime.now() + timedelta(seconds=self.cache_ttl),
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        use_cache: bool = True,
    ) -> Any:
        """
        Make HTTP request with retry logic

        Args:
            method: HTTP method (GET, POST, DELETE)
            endpoint: API endpoint (e.g., "/api/connections")
            data: Request payload
            use_cache: Whether to use cache for GET requests

        Returns:
            Response data

        Raises:
            BackendConnectionError: Connection failed
            BackendTimeoutError: Request timeout
            BackendAuthError: Authentication failed
        """
        url = urljoin(self.base_url, endpoint)

        # Check cache for GET requests
        if method == "GET" and use_cache:
            cache_key = self._get_cache_key(endpoint, data)
            cached_data = self._get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data

        # Retry logic with exponential backoff
        last_exception = None
        for attempt in range(self.retry_attempts):
            try:
                if method == "GET":
                    response = self.session.get(
                        url, params=data, timeout=self.timeout, verify=self.verify_ssl
                    )
                elif method == "POST":
                    response = self.session.post(
                        url, json=data, timeout=self.timeout, verify=self.verify_ssl
                    )
                elif method == "DELETE":
                    response = self.session.delete(
                        url, timeout=self.timeout, verify=self.verify_ssl
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                # Handle response
                if response.status_code == 401:
                    raise BackendAuthError("Invalid API key or unauthorized")
                elif response.status_code == 403:
                    raise BackendAuthError("Insufficient permissions")
                elif response.status_code == 429:
                    # Rate limit exceeded - wait and retry
                    if attempt < self.retry_attempts - 1:
                        wait_time = 2**attempt
                        time.sleep(wait_time)
                        continue
                    raise BackendConnectionError("Rate limit exceeded")
                elif response.status_code >= 400:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get("error", f"HTTP {response.status_code}")
                    raise BackendConnectionError(error_msg)

                # Parse response
                result = response.json() if response.text else {}

                # Cache GET requests
                if method == "GET" and use_cache:
                    cache_key = self._get_cache_key(endpoint, data)
                    self._set_cache(cache_key, result)

                return result

            except requests.exceptions.Timeout:
                last_exception = BackendTimeoutError(
                    f"Request timeout after {self.timeout}s"
                )
                if attempt < self.retry_attempts - 1:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue
            except requests.exceptions.ConnectionError as e:
                last_exception = BackendConnectionError(f"Connection failed: {str(e)}")
                if attempt < self.retry_attempts - 1:
                    wait_time = 2**attempt
                    time.sleep(wait_time)
                    continue
            except (BackendAuthError, BackendConnectionError):
                # Don't retry auth errors or other backend errors
                raise

        # All retries exhausted
        raise last_exception  # type: ignore

    # ========================================================================
    # Health & Status
    # ========================================================================

    def health_check(self) -> bool:
        """
        Check if backend server is healthy

        Returns:
            True if server is reachable and healthy
        """
        try:
            url = urljoin(self.base_url, "/health")
            response = requests.get(url, timeout=5, verify=self.verify_ssl)
            return response.status_code == 200
        except Exception:
            return False

    def get_stats(self) -> Dict[str, Any]:
        """
        Get backend server statistics

        Returns:
            Server statistics including uptime, requests, errors
        """
        return self._make_request("GET", "/api/stats")

    # ========================================================================
    # Connection Management
    # ========================================================================

    def list_connections(self) -> List[Dict[str, Any]]:
        """
        List all available database connections

        Returns:
            List of connection configurations
        """
        result = self._make_request("GET", "/api/connections")
        return result.get("connections", [])

    def create_connection(
        self, name: str, db_type: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new database connection

        Args:
            name: Connection name
            db_type: Database type (clickhouse, postgres, oracle, sqlserver, etc.)
            params: Connection parameters (host, port, database, credentials, etc.)

        Returns:
            Creation result
        """
        data = {"name": name, "type": db_type, "params": params}
        return self._make_request("POST", "/api/connections", data, use_cache=False)

    def delete_connection(self, name: str) -> Dict[str, Any]:
        """
        Delete a database connection

        Args:
            name: Connection name

        Returns:
            Deletion result
        """
        return self._make_request("DELETE", f"/api/connections/{name}", use_cache=False)

    # ========================================================================
    # Query Execution
    # ========================================================================

    def execute_query(
        self,
        connection: str,
        query: str,
        params: Optional[Any] = None,
        use_cache: bool = True,
    ) -> Any:
        """
        Execute a database query

        Args:
            connection: Connection name
            query: SQL query or command
            params: Query parameters
            use_cache: Whether to use cache (default True for SELECT queries)

        Returns:
            Query results
        """
        data = {"connection": connection, "query": query}
        if params is not None:
            data["params"] = params

        result = self._make_request("POST", "/api/query", data, use_cache=use_cache)
        return result.get("result")

    def get_schema(self, connection: str) -> Dict[str, Any]:
        """
        Get database schema information

        Args:
            connection: Connection name

        Returns:
            Schema information (tables, columns, types)
        """
        result = self._make_request("GET", f"/api/schema/{connection}")
        return result.get("schema", {})

    # ========================================================================
    # AI Insights
    # ========================================================================

    def analyze_data(
        self,
        connection: str,
        query: str,
        analysis_type: str = "general",
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """
        Analyze query results with AI insights

        Args:
            connection: Connection name
            query: SQL query to analyze
            analysis_type: Type of analysis (general, trend, anomaly, forecast)
            use_cache: Whether to use cache

        Returns:
            AI-generated insights
        """
        data = {
            "connection": connection,
            "query": query,
            "analysis_type": analysis_type,
        }
        result = self._make_request("POST", "/api/ai/analyze", data, use_cache)
        return result.get("insights", {})

    def get_recommendations(
        self, connection: str, context: str = "", use_cache: bool = True
    ) -> List[str]:
        """
        Get AI recommendations based on database schema

        Args:
            connection: Connection name
            context: Additional context for recommendations
            use_cache: Whether to use cache

        Returns:
            List of recommendations
        """
        data = {"connection": connection, "context": context}
        result = self._make_request("POST", "/api/ai/recommend", data, use_cache)
        return result.get("recommendations", [])

    # ========================================================================
    # User & Role Management
    # ========================================================================

    def list_users(self) -> List[Dict[str, Any]]:
        """
        List all users (API keys)

        Returns:
            List of users with permissions
        """
        result = self._make_request("GET", "/api/users")
        return result.get("users", [])

    def create_user(self, name: str, permissions: List[str]) -> Dict[str, Any]:
        """
        Create a new user (API key)

        Args:
            name: User name
            permissions: List of permissions

        Returns:
            User creation result including API key
        """
        data = {"name": name, "permissions": permissions}
        return self._make_request("POST", "/api/users", data, use_cache=False)

    # ========================================================================
    # Configuration
    # ========================================================================

    def get_config(self) -> Dict[str, Any]:
        """
        Get backend server configuration

        Returns:
            Server configuration (sanitized)
        """
        return self._make_request("GET", "/api/config")

    # ========================================================================
    # Cache Management
    # ========================================================================

    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """
        Get cache statistics

        Returns:
            Cache size and hit count
        """
        total_entries = len(self._cache)
        valid_entries = sum(
            1
            for cached in self._cache.values()
            if datetime.now() < cached["expires_at"]
        )
        return {"total_entries": total_entries, "valid_entries": valid_entries}

    # ========================================================================
    # Graceful Degradation
    # ========================================================================

    def is_connected(self) -> bool:
        """
        Check if backend is currently accessible

        Returns:
            True if backend is accessible
        """
        return self.health_check()

    def get_offline_message(self) -> str:
        """
        Get user-friendly offline message

        Returns:
            Message to display when backend is offline
        """
        return (
            "⚠️ Backend server is currently unavailable. "
            "Some features may be limited. "
            "Please try again later or contact your administrator."
        )


# ============================================================================
# Convenience Functions
# ============================================================================


def create_client(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs,
) -> BackendClient:
    """
    Create a backend client with environment variables

    Args:
        base_url: Backend URL (or use BACKEND_URL env var)
        api_key: API key (or use BACKEND_API_KEY env var)
        **kwargs: Additional client options

    Returns:
        Configured BackendClient instance
    """
    import os

    base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:5000")
    api_key = api_key or os.getenv("BACKEND_API_KEY", "admin_key_default")

    return BackendClient(base_url=base_url, api_key=api_key, **kwargs)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    import os

    # Example: Create client
    client = create_client(
        base_url=os.getenv("BACKEND_URL", "http://localhost:5000"),
        api_key=os.getenv("BACKEND_API_KEY", "admin_key_default"),
    )

    # Example: Health check
    if client.health_check():
        print("✅ Backend server is healthy")

        # Example: List connections
        connections = client.list_connections()
        print(f"📊 Available connections: {len(connections)}")

        # Example: Get stats
        stats = client.get_stats()
        print(f"📈 Server uptime: {stats.get('uptime_seconds', 0)}s")
    else:
        print("❌ Backend server is offline")
