"""
PostgreSQL Database Connector
Handles connections and queries to PostgreSQL databases
"""

import logging
from typing import Any, Dict, List, Optional

from backend.db_manager import DatabaseConnection

logger = logging.getLogger(__name__)


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL database connection implementation"""

    def __init__(self, connection_id: str, config: Dict[str, Any]):
        super().__init__(connection_id, config)
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        """Establish PostgreSQL connection"""
        try:
            import psycopg2

            host = self.config.get("host", "localhost")
            port = self.config.get("port", 5432)
            user = self.config.get("user", "postgres")
            password = self.config.get("password", "")
            database = self.config.get("database", "postgres")
            sslmode = self.config.get("sslmode", "prefer")

            self.conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                sslmode=sslmode,
            )

            self.cursor = self.conn.cursor()
            logger.info(f"Connected to PostgreSQL: {host}:{port}/{database}")
            self.connection = self.conn
            return True

        except Exception as e:
            logger.error(f"PostgreSQL connection error: {str(e)}")
            return False

    def disconnect(self) -> bool:
        """Close PostgreSQL connection"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None

            if self.conn:
                self.conn.close()
                self.conn = None
                self.connection = None
                logger.info(f"Disconnected from PostgreSQL: {self.connection_id}")
            return True
        except Exception as e:
            logger.error(f"PostgreSQL disconnect error: {str(e)}")
            return False

    def execute_query(self, query: str, params=None) -> List[Dict]:
        """Execute a PostgreSQL query and return results"""
        if not self.conn or not self.cursor:
            raise ConnectionError("Not connected to PostgreSQL")

        try:
            # Execute query
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Check if query returns data
            if self.cursor.description:
                # Get column names
                column_names = [desc[0] for desc in self.cursor.description]

                # Fetch all results
                rows = self.cursor.fetchall()

                # Convert to list of dictionaries
                data = []
                for row in rows:
                    row_dict = dict(zip(column_names, row))
                    data.append(row_dict)

                logger.info(f"Query executed successfully: {len(data)} rows returned")
                return data
            else:
                # Query doesn't return data (INSERT, UPDATE, DELETE)
                self.conn.commit()
                logger.info(
                    f"Query executed successfully: {self.cursor.rowcount} rows affected"
                )
                return [
                    {
                        "rows_affected": self.cursor.rowcount,
                        "status": "success",
                    }
                ]

        except Exception as e:
            self.conn.rollback()
            logger.error(f"PostgreSQL query error: {str(e)}")
            raise

    def get_schema(self, database: Optional[str] = None) -> Dict[str, Any]:
        """Get PostgreSQL database schema information"""
        schema_name = database or "public"

        try:
            # Get all tables in schema
            tables_query = """
                SELECT 
                    table_name,
                    table_type
                FROM information_schema.tables
                WHERE table_schema = %s
                ORDER BY table_name
            """

            results = self.execute_query(tables_query, (schema_name,))
            tables = [row["table_name"] for row in results]

            # Get columns for each table
            schema = {"schema": schema_name, "tables": {}}

            for table_name in tables:
                columns_query = """
                    SELECT 
                        column_name,
                        data_type,
                        character_maximum_length,
                        is_nullable,
                        column_default
                    FROM information_schema.columns
                    WHERE table_schema = %s AND table_name = %s
                    ORDER BY ordinal_position
                """

                columns = self.execute_query(columns_query, (schema_name, table_name))

                # Get indexes
                indexes_query = """
                    SELECT 
                        indexname,
                        indexdef
                    FROM pg_indexes
                    WHERE schemaname = %s AND tablename = %s
                """

                indexes = self.execute_query(indexes_query, (schema_name, table_name))

                schema["tables"][table_name] = {
                    "columns": columns,
                    "indexes": indexes,
                }

            return schema

        except Exception as e:
            logger.error(f"Schema retrieval error: {str(e)}")
            raise

    def get_tables(self, database: Optional[str] = None) -> List[str]:
        """Get list of tables in PostgreSQL database"""
        schema_name = database or "public"

        try:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """

            results = self.execute_query(query, (schema_name,))
            return [row["table_name"] for row in results]

        except Exception as e:
            logger.error(f"Table listing error: {str(e)}")
            raise

    def get_table_info(
        self, table_name: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about a PostgreSQL table"""
        schema_name = database or "public"

        try:
            # Get columns
            columns_query = """
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    numeric_precision,
                    numeric_scale,
                    is_nullable,
                    column_default,
                    is_identity,
                    is_generated
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s
                ORDER BY ordinal_position
            """

            columns = self.execute_query(columns_query, (schema_name, table_name))

            # Get indexes
            indexes_query = """
                SELECT 
                    i.indexname,
                    i.indexdef,
                    pg_size_pretty(pg_relation_size(s.indexrelid)) as size
                FROM pg_indexes i
                JOIN pg_stat_user_indexes s ON i.indexname = s.indexrelname
                WHERE i.schemaname = %s AND i.tablename = %s
            """

            indexes = self.execute_query(indexes_query, (schema_name, table_name))

            # Get constraints
            constraints_query = """
                SELECT 
                    tc.constraint_name,
                    tc.constraint_type,
                    kcu.column_name
                FROM information_schema.table_constraints tc
                LEFT JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                WHERE tc.table_schema = %s AND tc.table_name = %s
            """

            constraints = self.execute_query(
                constraints_query, (schema_name, table_name)
            )

            # Get table stats
            stats_query = """
                SELECT 
                    n_live_tup as row_count,
                    pg_size_pretty(pg_total_relation_size(%s::regclass)) as total_size,
                    pg_size_pretty(pg_relation_size(%s::regclass)) as table_size,
                    pg_size_pretty(pg_total_relation_size(%s::regclass) - pg_relation_size(%s::regclass)) as indexes_size
                FROM pg_stat_user_tables
                WHERE schemaname = %s AND relname = %s
            """

            stats_param = f"{schema_name}.{table_name}"
            stats = self.execute_query(
                stats_query,
                (
                    stats_param,
                    stats_param,
                    stats_param,
                    stats_param,
                    schema_name,
                    table_name,
                ),
            )

            return {
                "table_name": table_name,
                "schema": schema_name,
                "columns": columns,
                "column_count": len(columns),
                "indexes": indexes,
                "index_count": len(indexes),
                "constraints": constraints,
                "constraint_count": len(constraints),
                "stats": stats[0] if stats else {},
            }

        except Exception as e:
            logger.error(f"Table info error: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test if PostgreSQL connection is alive"""
        try:
            if not self.conn or not self.cursor:
                return False
            self.cursor.execute("SELECT 1")
            return True
        except Exception:
            return False

    def get_databases(self) -> List[str]:
        """Get list of all databases"""
        try:
            query = """
                SELECT datname 
                FROM pg_database 
                WHERE datistemplate = false
                ORDER BY datname
            """
            results = self.execute_query(query)
            return [row["datname"] for row in results]
        except Exception as e:
            logger.error(f"Database listing error: {str(e)}")
            raise

    def get_schemas(self) -> List[str]:
        """Get list of all schemas"""
        try:
            query = """
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
                ORDER BY schema_name
            """
            results = self.execute_query(query)
            return [row["schema_name"] for row in results]
        except Exception as e:
            logger.error(f"Schema listing error: {str(e)}")
            raise
