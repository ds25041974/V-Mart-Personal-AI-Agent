"""
Database Connection Manager
Manages connections to multiple database types with pooling and retry logic
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class DatabaseConnection(ABC):
    """Abstract base class for database connections"""

    def __init__(self, connection_id: str, config: Dict[str, Any]):
        self.connection_id = connection_id
        self.config = config
        self.connection = None
        self.last_used = None
        self.created_at = datetime.now()

    @abstractmethod
    def connect(self) -> bool:
        """Establish database connection"""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Close database connection"""
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute a query and return results"""
        pass

    @abstractmethod
    def get_schema(self, database: Optional[str] = None) -> Dict[str, Any]:
        """Get database schema information"""
        pass

    @abstractmethod
    def get_tables(self, database: Optional[str] = None) -> List[str]:
        """Get list of tables"""
        pass

    @abstractmethod
    def get_table_info(
        self, table_name: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about a table"""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """Test if connection is alive"""
        pass

    def is_connected(self) -> bool:
        """Check if connection is established"""
        return self.connection is not None

    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection metadata"""
        return {
            "connection_id": self.connection_id,
            "type": self.__class__.__name__,
            "is_connected": self.is_connected(),
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "config": {
                k: v
                for k, v in self.config.items()
                if k not in ["password", "api_key", "token"]
            },
        }


class ConnectionPool:
    """Manages a pool of database connections"""

    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: Dict[str, DatabaseConnection] = {}
        self.connection_usage: Dict[str, int] = {}

    def add_connection(
        self, connection_id: str, connection: DatabaseConnection
    ) -> bool:
        """Add a new connection to the pool"""
        if len(self.connections) >= self.max_connections:
            logger.warning(f"Connection pool is full (max: {self.max_connections})")
            # Remove least used connection
            self._remove_least_used_connection()

        self.connections[connection_id] = connection
        self.connection_usage[connection_id] = 0
        logger.info(f"Added connection: {connection_id}")
        return True

    def get_connection(self, connection_id: str) -> Optional[DatabaseConnection]:
        """Get a connection from the pool"""
        connection = self.connections.get(connection_id)
        if connection:
            self.connection_usage[connection_id] += 1
            connection.last_used = datetime.now()
        return connection

    def remove_connection(self, connection_id: str) -> bool:
        """Remove a connection from the pool"""
        if connection_id in self.connections:
            connection = self.connections[connection_id]
            if connection.is_connected():
                connection.disconnect()
            del self.connections[connection_id]
            del self.connection_usage[connection_id]
            logger.info(f"Removed connection: {connection_id}")
            return True
        return False

    def _remove_least_used_connection(self):
        """Remove the least used connection"""
        if not self.connection_usage:
            return

        least_used_id = min(self.connection_usage, key=self.connection_usage.get)
        self.remove_connection(least_used_id)

    def get_all_connections(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all connections"""
        return {
            conn_id: conn.get_connection_info()
            for conn_id, conn in self.connections.items()
        }

    def close_all(self):
        """Close all connections in the pool"""
        for connection_id in list(self.connections.keys()):
            self.remove_connection(connection_id)
        logger.info("Closed all connections")


class DatabaseManager:
    """Central database connection manager"""

    def __init__(self, max_connections: int = 20):
        self.pool = ConnectionPool(max_connections)
        self.registered_types: Dict[str, type] = {}

    def register_database_type(self, db_type: str, connection_class: type):
        """Register a new database type"""
        self.registered_types[db_type] = connection_class
        logger.info(f"Registered database type: {db_type}")

    def create_connection(
        self, connection_id: str, db_type: str, config: Dict[str, Any]
    ) -> bool:
        """Create a new database connection"""
        if db_type not in self.registered_types:
            logger.error(f"Unknown database type: {db_type}")
            return False

        try:
            connection_class = self.registered_types[db_type]
            connection = connection_class(connection_id, config)

            # Test connection
            if connection.connect():
                self.pool.add_connection(connection_id, connection)
                logger.info(f"Created connection: {connection_id} (type: {db_type})")
                return True
            else:
                logger.error(f"Failed to connect: {connection_id}")
                return False

        except Exception as e:
            logger.error(f"Error creating connection {connection_id}: {str(e)}")
            return False

    def get_connection(self, connection_id: str) -> Optional[DatabaseConnection]:
        """Get a connection from the pool"""
        return self.pool.get_connection(connection_id)

    def remove_connection(self, connection_id: str) -> bool:
        """Remove a connection"""
        return self.pool.remove_connection(connection_id)

    def execute_query(
        self, connection_id: str, query: str, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Execute a query on a specific connection"""
        connection = self.get_connection(connection_id)
        if not connection:
            return {"success": False, "error": f"Connection not found: {connection_id}"}

        try:
            # Reconnect if needed
            if not connection.is_connected():
                connection.connect()

            results = connection.execute_query(query, params)
            return {
                "success": True,
                "data": results,
                "row_count": len(results),
                "connection_id": connection_id,
            }
        except Exception as e:
            logger.error(f"Query execution error on {connection_id}: {str(e)}")
            return {"success": False, "error": str(e), "connection_id": connection_id}

    def fetch_one(
        self, connection_id: str, query: str, params: Optional[tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Execute query and return first row as dictionary

        Args:
            connection_id: Database connection ID
            query: SQL query
            params: Query parameters as tuple

        Returns:
            First row as dict or None if no results
        """
        result = self.execute_query(connection_id, query, params)
        if result.get("success") and result.get("data"):
            return result["data"][0] if len(result["data"]) > 0 else None
        return None

    def fetch_all(
        self, connection_id: str, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute query and return all rows as list of dictionaries

        Args:
            connection_id: Database connection ID
            query: SQL query
            params: Query parameters as tuple

        Returns:
            List of rows as dicts or empty list if no results
        """
        result = self.execute_query(connection_id, query, params)
        if result.get("success") and result.get("data"):
            return result["data"]
        return []

    def get_schema(
        self, connection_id: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get schema information from a connection"""
        connection = self.get_connection(connection_id)
        if not connection:
            return {"error": f"Connection not found: {connection_id}"}

        try:
            schema = connection.get_schema(database)
            return {"success": True, "schema": schema, "connection_id": connection_id}
        except Exception as e:
            logger.error(f"Schema retrieval error on {connection_id}: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_tables(
        self, connection_id: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of tables from a connection"""
        connection = self.get_connection(connection_id)
        if not connection:
            return {"error": f"Connection not found: {connection_id}"}

        try:
            tables = connection.get_tables(database)
            return {
                "success": True,
                "tables": tables,
                "table_count": len(tables),
                "connection_id": connection_id,
            }
        except Exception as e:
            logger.error(f"Table listing error on {connection_id}: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_table_info(
        self, connection_id: str, table_name: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed table information"""
        connection = self.get_connection(connection_id)
        if not connection:
            return {"error": f"Connection not found: {connection_id}"}

        try:
            table_info = connection.get_table_info(table_name, database)
            return {
                "success": True,
                "table_info": table_info,
                "connection_id": connection_id,
            }
        except Exception as e:
            logger.error(f"Table info error on {connection_id}: {str(e)}")
            return {"success": False, "error": str(e)}

    def test_connection(self, connection_id: str) -> bool:
        """Test a specific connection"""
        connection = self.get_connection(connection_id)
        if not connection:
            return False
        return connection.test_connection()

    def get_all_connections(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all connections"""
        return self.pool.get_all_connections()

    def close_all_connections(self):
        """Close all database connections"""
        self.pool.close_all()


# Global database manager instance
db_manager = DatabaseManager()
