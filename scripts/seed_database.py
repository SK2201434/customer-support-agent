from app.database.connection import get_connection
from app.database.schema import create_tables


CUSTOMERS = [
    ("customer_123", "Satish", "satish@example.com", "Premium"),
    ("customer_456", "Rahul", "rahul@example.com", "Basic"),
]


ORDERS = [
    ("1001", "customer_123", "Laptop", "Shipped"),
    ("1002", "customer_123", "Headphones", "Processing"),
    ("1003", "customer_456", "Keyboard", "Delivered"),
]


def seed_database() -> None:
    """Insert development data into the database."""

    create_tables()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.executemany(
        """
        INSERT OR IGNORE INTO customers (
            id,
            name,
            email,
            plan
        )
        VALUES (?, ?, ?, ?)
        """,
        CUSTOMERS,
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO orders (
            id,
            customer_id,
            product,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        ORDERS,
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    seed_database()

    print("Database seeded successfully.")