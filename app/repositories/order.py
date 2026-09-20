from app.database.connection import get_connection


class OrderRepository:
    """Repository for accessing order data."""

    def get_order(self, order_id: str) -> dict | None:
        """Return complete order information."""

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, customer_id, product, status
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "customer_id": row[1],
            "product": row[2],
            "status": row[3],
        }

    def cancel_order(self,order_id:str) -> dict | None:
        """cancel an orderand return the update order."""

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE orders
            SET status = 'cancelled'
            WHERE id = ?
            """,
            (order_id,),
        )

        connection.commit()

        cursor.execute(
            """
            SELECT id, customer_id, product, status
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        )

        row = cursor.fetchone()

        connection.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "customer_id": row[1],
            "product": row[2],
            "status": row[3],
        }