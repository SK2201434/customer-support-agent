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

    def get_cancel_decision(
        self,
        order_id: str,
        customer_id: str,
    ) -> str:
        """Return the cancellation policy decision."""

        order = self.repository.get_order(order_id)

        if order is None:
            return "DENY"

        if order["customer_id"] != customer_id:
            return "DENY"

        if order["status"] != "Processing":
            return "DENY"

        return "APPROVAL_REQUIRED"
    

    def execute_cancel_order(
        self,
        order_id: str,
        customer_id: str,
    ) -> dict | None:
        """Execute an order cancellation after approval."""

        order = self.repository.get_order(order_id)

        if order is None:
            return None

        if order["customer_id"] != customer_id:
            return None

        if order["status"] != "Processing":
            return None

        return self.repository.cancel_order(order_id)