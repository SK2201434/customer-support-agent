from app.database.connection import get_connection


def test_seeded_data():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, email, plan FROM customers"
    )

    customers = cursor.fetchall()

    cursor.execute(
        "SELECT id, customer_id, product, status FROM orders"
    )

    orders = cursor.fetchall()

    connection.close()

    assert len(customers) == 2
    assert len(orders) == 3

    assert ("customer_123", "Satish", "satish@example.com", "Premium") in customers

    assert ("1001", "customer_123", "Laptop", "Shipped") in orders
    assert ("1002", "customer_123", "Headphones", "Processing") in orders
    assert ("1003", "customer_456", "Keyboard", "Delivered") in orders