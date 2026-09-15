from app.database.connection import get_connection


def create_tables() -> None:
    """Create the database tables if they do not exist."""

    connection = get_connection()
    cursor = connection.cursor()

    # Create the customers table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            plan TEXT NOT NULL
        )
        """
    )

    # Create the orders table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            product TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """
    )

    # Create the knowledge documents table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS knowledge_documents (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            product TEXT,
            version INTEGER NOT NULL DEFAULT 1,
            status TEXT NOT NULL DEFAULT 'active',
            locale TEXT NOT NULL DEFAULT 'en-IN',
            priority INTEGER NOT NULL DEFAULT 0,
            effective_from TEXT,
            effective_until TEXT
        )
        """
    )
    # Create the full-text search index

    cursor.execute(
    """
    CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_documents_fts
    USING fts5(
        title,
        content,
        category,
        product,
        content='knowledge_documents',
        content_rowid='rowid'
    )
    """
)

    # Commit changes and close the connection
    connection.commit()
    connection.close()