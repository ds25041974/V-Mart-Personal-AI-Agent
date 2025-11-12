"""
SQLite Database Manager for Authentication
Simple database operations for user authentication
"""

import os
import sqlite3
from typing import Any, Dict, List, Optional


class AuthDatabaseManager:
    """Manages SQLite database for authentication"""

    def __init__(self, db_path: str = None):
        """Initialize database manager"""
        if db_path is None:
            # Default to project root/data/users.db
            project_root = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            data_dir = os.path.join(project_root, "data")
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, "users.db")

        self.db_path = db_path
        self._ensure_database()

    def _ensure_database(self):
        """Ensure database file exists"""
        if not os.path.exists(self.db_path):
            # Create database file
            conn = sqlite3.connect(self.db_path)
            conn.close()
            print(f"✅ Created authentication database at: {self.db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn

    def execute_query(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Execute a query that modifies data (INSERT, UPDATE, DELETE)

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Number of rows affected
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()

    def fetch_one(
        self, query: str, params: Optional[tuple] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Execute query and return first row as dictionary

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            First row as dict or None
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        finally:
            conn.close()

    def fetch_all(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute query and return all rows as list of dictionaries

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            List of rows as dicts
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def init_tables(self, create_queries: List[str]):
        """
        Initialize database tables

        Args:
            create_queries: List of CREATE TABLE statements
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            for query in create_queries:
                cursor.execute(query)
            conn.commit()
            print(
                f"✅ Initialized {len(create_queries)} tables in authentication database"
            )
        finally:
            conn.close()
