import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data")/"support.db"

def get_connection() -> sqlite3.Connection:
    """Create a connection to the support database."""
    
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    return connection