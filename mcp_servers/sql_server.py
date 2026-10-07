import os
from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Create the MCP Server
mcp = FastMCP("CockroachDB Sales Server")

# Create a reusable database connection
engine = create_engine(os.getenv("DATABASE_URL"))


@mcp.tool()
def list_tables() -> str:
    """List all available tables in the CockroachDB database."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        )
        tables = [row[0] for row in result]
        return f"Available tables: {', '.join(tables)}"


@mcp.tool()
def get_schema(table_name: str) -> str:
    """Get the column names and types for a specific table."""
    with engine.connect() as conn:
        result = conn.execute(
            text(
                f"SELECT column_name, data_type FROM information_schema.columns "
                f"WHERE table_name = '{table_name}'"
            )
        )
        columns = [f"{row[0]} ({row[1]})" for row in result]
        return f"Schema for {table_name}: {', '.join(columns)}"


@mcp.tool()
def execute_query(sql_query: str) -> str:
    """Execute a SQL query against the CockroachDB database and return results.
    IMPORTANT: The database uses PostgreSQL/CockroachDB syntax.
    The 'transaction_date' column is stored as VARCHAR, so cast it with ::date for date comparisons.
    Never use MySQL functions like DATE_FORMAT(); use TO_CHAR() instead.
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        rows = result.fetchall()
        columns = list(result.keys())
        return f"Columns: {columns}\nResults ({len(rows)} rows): {rows[:20]}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
