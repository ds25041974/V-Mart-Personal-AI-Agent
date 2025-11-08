"""
Oracle Database Connector
Handles connections and queries to Oracle databases
"""

import logging
from typing import Any, Dict, List, Optional

from backend.db_manager import DatabaseConnection

logger = logging.getLogger(__name__)


class OracleConnection(DatabaseConnection):
    """Oracle database connection implementation"""

    def __init__(self, connection_id: str, config: Dict[str, Any]):
        super().__init__(connection_id, config)
        self.conn = None
        self.cursor = None

    def connect(self) -> bool:
        """Establish Oracle connection"""
        try:
            import oracledb

            host = self.config.get("host", "localhost")
            port = self.config.get("port", 1521)
            user = self.config.get("user", "system")
            password = self.config.get("password", "")
            service_name = self.config.get("service_name")
            sid = self.config.get("sid")

            # Create DSN
            if service_name:
                dsn = oracledb.makedsn(host, port, service_name=service_name)
            elif sid:
                dsn = oracledb.makedsn(host, port, sid=sid)
            else:
                raise ValueError("Either service_name or sid must be provided")

            self.conn = oracledb.connect(user=user, password=password, dsn=dsn)
            self.cursor = self.conn.cursor()

            logger.info(f"Connected to Oracle: {host}:{port}")
            self.connection = self.conn
            return True

        except Exception as e:
            logger.error(f"Oracle connection error: {str(e)}")
            return False

    def disconnect(self) -> bool:
        """Close Oracle connection"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None

            if self.conn:
                self.conn.close()
                self.conn = None
                self.connection = None
                logger.info(f"Disconnected from Oracle: {self.connection_id}")
            return True
        except Exception as e:
            logger.error(f"Oracle disconnect error: {str(e)}")
            return False

    def execute_query(self, query: str, params=None) -> List[Dict]:
        """Execute an Oracle query and return results"""
        if not self.conn or not self.cursor:
            raise ConnectionError("Not connected to Oracle")

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
            logger.error(f"Oracle query error: {str(e)}")
            raise

    def get_schema(self, database: Optional[str] = None) -> Dict[str, Any]:
        """Get Oracle database schema information"""
        schema_name = (database or self.config.get("user", "")).upper()

        try:
            # Get all tables in schema
            tables_query = """
                SELECT 
                    table_name,
                    tablespace_name,
                    num_rows
                FROM all_tables
                WHERE owner = :schema
                ORDER BY table_name
            """

            results = self.execute_query(tables_query, {"schema": schema_name})
            tables = [row["TABLE_NAME"] for row in results]

            # Get columns for each table
            schema = {"schema": schema_name, "tables": {}}

            for table_name in tables:
                columns_query = """
                    SELECT 
                        column_name,
                        data_type,
                        data_length,
                        data_precision,
                        data_scale,
                        nullable,
                        data_default
                    FROM all_tab_columns
                    WHERE owner = :schema AND table_name = :table
                    ORDER BY column_id
                """

                columns = self.execute_query(
                    columns_query, {"schema": schema_name, "table": table_name}
                )

                # Get indexes
                indexes_query = """
                    SELECT 
                        index_name,
                        index_type,
                        uniqueness
                    FROM all_indexes
                    WHERE owner = :schema AND table_name = :table
                """

                indexes = self.execute_query(
                    indexes_query, {"schema": schema_name, "table": table_name}
                )

                schema["tables"][table_name] = {
                    "columns": columns,
                    "indexes": indexes,
                }

            return schema

        except Exception as e:
            logger.error(f"Schema retrieval error: {str(e)}")
            raise

    def get_tables(self, database: Optional[str] = None) -> List[str]:
        """Get list of tables in Oracle database"""
        schema_name = (database or self.config.get("user", "")).upper()

        try:
            query = """
                SELECT table_name
                FROM all_tables
                WHERE owner = :schema
                ORDER BY table_name
            """

            results = self.execute_query(query, {"schema": schema_name})
            return [row["TABLE_NAME"] for row in results]

        except Exception as e:
            logger.error(f"Table listing error: {str(e)}")
            raise

    def get_table_info(
        self, table_name: str, database: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about an Oracle table"""
        schema_name = (database or self.config.get("user", "")).upper()
        table_name = table_name.upper()

        try:
            # Get columns
            columns_query = """
                SELECT 
                    column_name,
                    data_type,
                    data_length,
                    data_precision,
                    data_scale,
                    nullable,
                    data_default,
                    column_id
                FROM all_tab_columns
                WHERE owner = :schema AND table_name = :table
                ORDER BY column_id
            """

            columns = self.execute_query(
                columns_query, {"schema": schema_name, "table": table_name}
            )

            # Get indexes
            indexes_query = """
                SELECT 
                    i.index_name,
                    i.index_type,
                    i.uniqueness,
                    ic.column_name,
                    ic.column_position
                FROM all_indexes i
                LEFT JOIN all_ind_columns ic 
                    ON i.owner = ic.index_owner 
                    AND i.index_name = ic.index_name
                WHERE i.owner = :schema AND i.table_name = :table
                ORDER BY i.index_name, ic.column_position
            """

            indexes = self.execute_query(
                indexes_query, {"schema": schema_name, "table": table_name}
            )

            # Get constraints
            constraints_query = """
                SELECT 
                    c.constraint_name,
                    c.constraint_type,
                    cc.column_name,
                    cc.position
                FROM all_constraints c
                LEFT JOIN all_cons_columns cc 
                    ON c.owner = cc.owner 
                    AND c.constraint_name = cc.constraint_name
                WHERE c.owner = :schema AND c.table_name = :table
                ORDER BY c.constraint_name, cc.position
            """

            constraints = self.execute_query(
                constraints_query, {"schema": schema_name, "table": table_name}
            )

            # Get table stats
            stats_query = """
                SELECT 
                    num_rows,
                    blocks,
                    avg_row_len,
                    last_analyzed
                FROM all_tables
                WHERE owner = :schema AND table_name = :table
            """

            stats = self.execute_query(
                stats_query, {"schema": schema_name, "table": table_name}
            )

            return {
                "table_name": table_name,
                "schema": schema_name,
                "columns": columns,
                "column_count": len(columns),
                "indexes": indexes,
                "constraints": constraints,
                "stats": stats[0] if stats else {},
            }

        except Exception as e:
            logger.error(f"Table info error: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test if Oracle connection is alive"""
        try:
            if not self.conn or not self.cursor:
                return False
            self.cursor.execute("SELECT 1 FROM DUAL")
            return True
        except Exception:
            return False

    def get_schemas(self) -> List[str]:
        """Get list of all schemas"""
        try:
            query = """
                SELECT DISTINCT owner
                FROM all_tables
                WHERE owner NOT IN (
                    'SYS', 'SYSTEM', 'OUTLN', 'DBSNMP', 'APPQOSSYS',
                    'WMSYS', 'EXFSYS', 'CTXSYS', 'XDB', 'ANONYMOUS',
                    'ORDSYS', 'MDSYS', 'ORDDATA', 'OLAPSYS'
                )
                ORDER BY owner
            """
            results = self.execute_query(query)
            return [row["OWNER"] for row in results]
        except Exception as e:
            logger.error(f"Schema listing error: {str(e)}")
            raise
