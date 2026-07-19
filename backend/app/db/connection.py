from psycopg_pool import ConnectionPool
from psycopg import Connection
from psycopg.rows import dict_row

from backend.app.core.config import DATABASE_URL

pool = ConnectionPool(
    conninfo = DATABASE_URL,
    min_size = 2,
    max_size = 10,
    open = False
)

def initialize_database():
    """
    Initialize the PostgreSQL database connection pool.
    Called once when the application starts.
    """
    pool.open()


def close_database():
    """
    Close all database connections.
    Called when the application shuts down.
    """
    pool.close()

def get_connection() -> Connection:
    """
    Returns a pooled database connection.
    
    Usage:
    
        with get_connection() as conn:
            ...
    """
    
    return pool.connection()

