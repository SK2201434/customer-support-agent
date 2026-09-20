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

    def cancel_customer_order(self,order_id: str, customer_id: str,) -> dict | None:
        """Cancel an order if it belongs to the customer and is cancellable."""

        order = self.repository.get_order(order_id)

        if order is None:
            return None

        # Authorization check.
        if order["customer_id"] != customer_id:
            return None

        # Only orders that are still being processed can be cancelled.
        if order["status"] != "Processing":
            return None

        return self.repository.cancel_order(order_id)
