"""
SQL Server Database Connector
Handles connections and queries to Microsoft SQL Server databases
"""

import logging
from typing import Any, Dict, List, Optional

from backend.db_manager import DatabaseConnection

logger = logging.getLogger(__name__)


class SQLServerConnection(DatabaseConnection):
    """SQL Server database connection implementation"""

    def __init__(self, connection_id: str, config: Dict[str, Any]):
        super().__init__(connection_id, config)
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        """Establish SQL Server connection"""
        try:
            import pyodbc

            server = self.config.get("server", "localhost")
            port = self.config.get("port", 1433)
            database = self.config.get("database", "master")
            user = self.config.get("user")
            password = self.config.get("password")
            driver = self.config.get("driver", "{ODBC Driver 17 for SQL Server}")
            trusted_connection = self.config.get("trusted_connection", False)

            # Build connection string
            if trusted_connection:
                conn_str = (
                    f"DRIVER={driver};"
                    f"SERVER={server},{port};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                )
            else:
                conn_str = (
                    f"DRIVER={driver};"
                    f"SERVER={server},{port};"
                    f"DATABASE={database};"
                    f"UID={user};"
                    f"PWD={password};"
                )

            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()

            logger.info(f"Connected to SQL Server: {server}:{port}/{database}")
            self.connection = self.conn
            return True

        except Exception as e:
            logger.error(f"SQL Server connection error: {str(e)}")
            return False

    def disconnect(self) -> bool:
        """Close SQL Server connection"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None

            if self.conn:
                self.conn.close()
                self.conn = None
                self.connection = None
                logger.info(f"Disconnected from SQL Server: {self.connection_id}")
            return True
        except Exception as e:
            logger.error(f"SQL Server disconnect error: {str(e)}")
            return False

    def execute_query(self, query: str, params=None) -> List[Dict]:
        """Execute a SQL Server query and return results"""
        if not self.conn or not self.cursor:
            raise ConnectionError("Not connected to SQL Server")

        try:
            # Execute query
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Check if query returns data
            if self.cursor.description:
                # Get column names
                column_names = [column[0] for column in self.cursor.description]

                # Fetch all results
                rows = self.cursor.fetchall()

                # Convert to list of dictionaries
                data = []
                for row in rows:
                    row_dict = dict(zip(column_names, row))
                    data.append(row_dict)

                logger.info(
                    f"Query executed successfully: {len(data)} rows returned"
                )
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
            logger.error(f"SQL Server query error: {str(e)}")
            raise

    def get_schema(self, database: Optional[str] = None) -> Dict[str, Any]:
        """Get SQL Server database schema information"""
        db_name = database or self.config.get("database", "master")

        try:
            # Get all tables in database
            tables_query = f"""
                SELECT 
                    TABLE_SCHEMA,
                    TABLE_NAME,
                    TABLE_TYPE
                FROM [{db_name}].INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """

            results = self.execute_query(tables_query)

            # Get columns for each table
            schema = {"database": db_name, "schemas": {}}

            for row in results:
                schema_name = row["TABLE_SCHEMA"]
                table_name = row["TABLE_NAME"]

                if schema_name not in schema["schemas"]:
                    schema["schemas"][schema_name] = {}

                columns_query = f"""
                    SELECT 
                        COLUMN_NAME,
                        DATA_TYPE,
                        CHARACTER_MAXIMUM_LENGTH,
                        NUMERIC_PRECISION,
                        NUMERIC_SCALE,
                        IS_NULLABLE,
                        COLUMN_DEFAULT
                    FROM [{db_name}].INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
                    ORDER BY ORDINAL_POSITION
                """

                columns = self.execute_query(
                    columns_query, (schema_name, table_name)
                )

                # Get indexes
                indexes_query = f"""
                    SELECT 
                        i.name as INDEX_NAME,
                        i.type_desc as INDEX_TYPE,
                        i.is_unique as IS_UNIQUE,
                        i.is_primary_key as IS_PRIMARY_KEY,
                        COL_NAME(ic.object_id, ic.column_id) as COLUMN_NAME
                    FROM [{db_name}].sys.indexes i
                    INNER JOIN [{db_name}].sys.index_columns ic 
                        ON i.object_id = ic.object_id 
                        AND i.index_id = ic.index_id
                    INNER JOIN [{db_name}].sys.tables t 
                        ON i.object_id = t.object_id
                    INNER JOIN [{db_name}].sys.schemas s 
                        ON t.schema_id = s.schema_id
                    WHERE s.name = ? AND t.name = ?
                    ORDER BY i.name, ic.key_ordinal
                """

                indexes = self.execute_query(indexes_query, (schema_name, table_name))

                schema["schemas"][schema_name][table_name] = {
                    "columns": columns,
                    "indexes": indexes,
                }

            return schema

        except Exception as e:
            logger.error(f"Schema retrieval error: {str(e)}")
            raise

    def get_tables(self, database: Optional[str] = None) -> List[str]:
        """Get list of tables in SQL Server database"""
        db_name = database or self.config.get("database", "master")

        try:
            query = f"""
                SELECT TABLE_SCHEMA + '.' + TABLE_NAME as TABLE_NAME
                FROM [{db_name}].INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_SCHEMA, TABLE_NAME
            """

            results = self.execute_query(query)
            return [row["TABLE_NAME"] for row in results]

        except Exception as e:
            logger.error(f"Table listing error: {str(e)}")
            raise

    def get_table_info(
        self, table_name: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about a SQL Server table"""
        db_name = database or self.config.get("database", "master")

        # Parse schema and table
        if "." in table_name:
            schema_name, tbl_name = table_name.split(".", 1)
        else:
            schema_name = "dbo"
            tbl_name = table_name

        try:
            # Get columns
            columns_query = f"""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    CHARACTER_MAXIMUM_LENGTH,
                    NUMERIC_PRECISION,
                    NUMERIC_SCALE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    ORDINAL_POSITION
                FROM [{db_name}].INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """

            columns = self.execute_query(columns_query, (schema_name, tbl_name))

            # Get indexes
            indexes_query = f"""
                SELECT 
                    i.name as INDEX_NAME,
                    i.type_desc as INDEX_TYPE,
                    i.is_unique as IS_UNIQUE,
                    i.is_primary_key as IS_PRIMARY_KEY,
                    COL_NAME(ic.object_id, ic.column_id) as COLUMN_NAME,
                    ic.key_ordinal as KEY_ORDINAL
                FROM [{db_name}].sys.indexes i
                INNER JOIN [{db_name}].sys.index_columns ic 
                    ON i.object_id = ic.object_id 
                    AND i.index_id = ic.index_id
                INNER JOIN [{db_name}].sys.tables t 
                    ON i.object_id = t.object_id
                INNER JOIN [{db_name}].sys.schemas s 
                    ON t.schema_id = s.schema_id
                WHERE s.name = ? AND t.name = ?
                ORDER BY i.name, ic.key_ordinal
            """

            indexes = self.execute_query(indexes_query, (schema_name, tbl_name))

            # Get constraints
            constraints_query = f"""
                SELECT 
                    tc.CONSTRAINT_NAME,
                    tc.CONSTRAINT_TYPE,
                    kcu.COLUMN_NAME
                FROM [{db_name}].INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                LEFT JOIN [{db_name}].INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
                    ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
                    AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
                    AND tc.TABLE_NAME = kcu.TABLE_NAME
                WHERE tc.TABLE_SCHEMA = ? AND tc.TABLE_NAME = ?
            """

            constraints = self.execute_query(
                constraints_query, (schema_name, tbl_name)
            )

            # Get table stats
            stats_query = f"""
                SELECT 
                    p.rows as ROW_COUNT,
                    SUM(a.total_pages) * 8 as TOTAL_SIZE_KB,
                    SUM(a.used_pages) * 8 as USED_SIZE_KB
                FROM [{db_name}].sys.tables t
                INNER JOIN [{db_name}].sys.schemas s 
                    ON t.schema_id = s.schema_id
                INNER JOIN [{db_name}].sys.partitions p 
                    ON t.object_id = p.object_id
                INNER JOIN [{db_name}].sys.allocation_units a 
                    ON p.partition_id = a.container_id
                WHERE s.name = ? AND t.name = ? AND p.index_id IN (0,1)
                GROUP BY p.rows
            """

            stats = self.execute_query(stats_query, (schema_name, tbl_name))

            return {
                "table_name": tbl_name,
                "schema": schema_name,
                "database": db_name,
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
        """Test if SQL Server connection is alive"""
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
                SELECT name
                FROM sys.databases
                WHERE database_id > 4
                ORDER BY name
            """
            results = self.execute_query(query)
            return [row["name"] for row in results]
        except Exception as e:
            logger.error(f"Database listing error: {str(e)}")
            raise

    def get_schemas(self, database: Optional[str] = None) -> List[str]:
        """Get list of all schemas in database"""
        db_name = database or self.config.get("database", "master")

        try:
            query = f"""
                SELECT SCHEMA_NAME
                FROM [{db_name}].INFORMATION_SCHEMA.SCHEMATA
                WHERE SCHEMA_NAME NOT IN ('db_owner', 'db_accessadmin', 
                    'db_securityadmin', 'db_ddladmin', 'db_backupoperator',
                    'db_datareader', 'db_datawriter', 'db_denydatareader',
                    'db_denydatawriter', 'INFORMATION_SCHEMA', 'sys')
                ORDER BY SCHEMA_NAME
            """
            results = self.execute_query(query)
            return [row["SCHEMA_NAME"] for row in results]
        except Exception as e:
            logger.error(f"Schema listing error: {str(e)}")
            raise
