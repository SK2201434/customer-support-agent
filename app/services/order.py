from app.repositories.order import OrderRepository


class OrderService:
    """Business logic for customer orders."""

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def get_customer_order(
        self,
        order_id: str,
        customer_id: str,
    ) -> dict | None:
        """Return an order only if it belongs to the customer."""

        order = self.repository.get_order(order_id)

        if order is None:
            return None

        if order["customer_id"] != customer_id:
            return None

        return order