"""
ClickHouse Database Connector
Handles connections and queries to ClickHouse databases
"""

import logging
from typing import Any, Dict, List, Optional

from backend.db_manager import DatabaseConnection

logger = logging.getLogger(__name__)


class ClickHouseConnection(DatabaseConnection):
    """ClickHouse database connection implementation"""

    def __init__(self, connection_id: str, config: Dict[str, Any]):
        super().__init__(connection_id, config)
        self.client = None

    def connect(self) -> bool:
        """Establish ClickHouse connection"""
        try:
            from clickhouse_driver import Client

            host = self.config.get("host", "localhost")
            port = self.config.get("port", 9000)
            user = self.config.get("user", "default")
            password = self.config.get("password", "")
            database = self.config.get("database", "default")
            secure = self.config.get("secure", False)

            self.client = Client(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                secure=secure,
            )

            # Test connection
            self.client.execute("SELECT 1")
            logger.info(f"Connected to ClickHouse: {host}:{port}/{database}")
            self.connection = self.client
            return True

        except Exception as e:
            logger.error(f"ClickHouse connection error: {str(e)}")
            return False

    def disconnect(self) -> bool:
        """Close ClickHouse connection"""
        try:
            if self.client:
                self.client.disconnect()
                self.client = None
                self.connection = None
                logger.info(f"Disconnected from ClickHouse: {self.connection_id}")
            return True
        except Exception as e:
            logger.error(f"ClickHouse disconnect error: {str(e)}")
            return False

    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """Execute a ClickHouse query and return results"""
        if not self.client:
            raise ConnectionError("Not connected to ClickHouse")

        try:
            # Execute query with column names
            result = self.client.execute(query, params or {}, with_column_types=True)

            if not result:
                return []

            # Parse results
            rows, column_info = result
            column_names = [col[0] for col in column_info]

            # Convert to list of dictionaries
            data = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                data.append(row_dict)

            logger.info(f"Query executed successfully: {len(data)} rows returned")
            return data

        except Exception as e:
            logger.error(f"ClickHouse query error: {str(e)}")
            raise

    def get_schema(self, database: Optional[str] = None) -> Dict[str, Any]:
        """Get ClickHouse database schema information"""
        db = database or self.config.get("database", "default")

        try:
            # Get all tables in database
            tables_query = f"""
                SELECT 
                    name,
                    engine,
                    total_rows,
                    total_bytes
                FROM system.tables
                WHERE database = '{db}'
                ORDER BY name
            """

            tables = self.execute_query(tables_query)

            # Get columns for each table
            schema = {"database": db, "tables": {}}

            for table in tables:
                table_name = table["name"]
                columns_query = f"""
                    SELECT 
                        name,
                        type,
                        default_kind,
                        default_expression,
                        comment
                    FROM system.columns
                    WHERE database = '{db}' AND table = '{table_name}'
                    ORDER BY position
                """

                columns = self.execute_query(columns_query)

                schema["tables"][table_name] = {
                    "engine": table["engine"],
                    "total_rows": table["total_rows"],
                    "total_bytes": table["total_bytes"],
                    "columns": columns,
                }

            return schema

        except Exception as e:
            logger.error(f"Schema retrieval error: {str(e)}")
            raise

    def get_tables(self, database: Optional[str] = None) -> List[str]:
        """Get list of tables in ClickHouse database"""
        db = database or self.config.get("database", "default")

        try:
            query = f"""
                SELECT name
                FROM system.tables
                WHERE database = '{db}'
                ORDER BY name
            """

            results = self.execute_query(query)
            return [row["name"] for row in results]

        except Exception as e:
            logger.error(f"Table listing error: {str(e)}")
            raise

    def get_table_info(
        self, table_name: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about a ClickHouse table"""
        db = database or self.config.get("database", "default")

        try:
            # Get table metadata
            table_query = f"""
                SELECT 
                    name,
                    engine,
                    partition_key,
                    sorting_key,
                    primary_key,
                    sampling_key,
                    total_rows,
                    total_bytes
                FROM system.tables
                WHERE database = '{db}' AND name = '{table_name}'
            """

            table_info = self.execute_query(table_query)
            if not table_info:
                return {"error": f"Table not found: {table_name}"}

            table_data = table_info[0]

            # Get columns
            columns_query = f"""
                SELECT 
                    name,
                    type,
                    default_kind,
                    default_expression,
                    comment,
                    is_in_partition_key,
                    is_in_sorting_key,
                    is_in_primary_key
                FROM system.columns
                WHERE database = '{db}' AND table = '{table_name}'
                ORDER BY position
            """

            columns = self.execute_query(columns_query)

            # Get partitions
            partitions_query = f"""
                SELECT 
                    partition,
                    rows,
                    bytes_on_disk
                FROM system.parts
                WHERE database = '{db}' AND table = '{table_name}' AND active = 1
                ORDER BY partition
            """

            partitions = self.execute_query(partitions_query)

            return {
                "table_name": table_name,
                "database": db,
                "engine": table_data["engine"],
                "partition_key": table_data["partition_key"],
                "sorting_key": table_data["sorting_key"],
                "primary_key": table_data["primary_key"],
                "sampling_key": table_data["sampling_key"],
                "total_rows": table_data["total_rows"],
                "total_bytes": table_data["total_bytes"],
                "columns": columns,
                "partitions": partitions,
                "partition_count": len(partitions),
            }

        except Exception as e:
            logger.error(f"Table info error: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test if ClickHouse connection is alive"""
        try:
            if not self.client:
                return False
            self.client.execute("SELECT 1")
            return True
        except Exception:
            return False

    def get_databases(self) -> List[str]:
        """Get list of all databases"""
        try:
            query = "SELECT name FROM system.databases ORDER BY name"
            results = self.execute_query(query)
            return [row["name"] for row in results]
        except Exception as e:
            logger.error(f"Database listing error: {str(e)}")
            raise

    def execute_query_with_stats(
        self, query: str, params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Execute query and return results with execution statistics"""
        try:
            import time

            start_time = time.time()

            # Get query stats
            self.client.execute("SET send_progress_in_http_headers = 1")

            results = self.execute_query(query, params)

            execution_time = time.time() - start_time

            return {
                "success": True,
                "data": results,
                "row_count": len(results),
                "execution_time_seconds": round(execution_time, 3),
                "connection_id": self.connection_id,
            }

        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            return {"success": False, "error": str(e)}
