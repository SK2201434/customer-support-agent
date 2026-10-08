import uuid

from app.database.connection import get_connection


class CustomerRepository:
    """Repository for accessing customer data."""

    def create_customer(
        self,
        customer_id: str,
        name: str,
        email: str,
        plan: str,
    ) -> dict:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO customers (
                id,
                name,
                email,
                plan
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                customer_id,
                name,
                email,
                plan,
            ),
        )

        connection.commit()
        connection.close()

        return {
            "id": customer_id,
            "name": name,
            "email": email,
            "plan": plan,
        }

    def get_customer(
        self,
        customer_id: str,
    ) -> dict | None:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, email, plan
            FROM customers
            WHERE id = ?
            """,
            (customer_id,),
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "plan": row[3],
        }