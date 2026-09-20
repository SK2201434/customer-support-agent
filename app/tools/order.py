from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from app.repositories.order import OrderRepository
from app.services.order import OrderService


repository = OrderRepository()
order_service = OrderService(repository)


@tool
def get_order_status(
    order_id: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """Get the status of a customer's order."""

    customer_id = state["user_id"]

    order = order_service.get_customer_order(
        order_id=order_id,
        customer_id=customer_id,
    )

    if order is None:
        return "Order not found or you are not authorized to access this order."

    return order["status"]

@tool
def cancel_order(
    order_id: str,
    state: Annotated[dict, InjectedState],
) -> str:
    """Cancel a customer's order if it is eligible for cancellation."""

    customer_id = state["user_id"]

    order = order_service.cancel_customer_order(
        order_id=order_id,
        customer_id=customer_id,
    )

    if order is None:
        return (
            "The order could not be cancelled. "
            "It may not exist, may not belong to you, "
            "or may not be eligible for cancellation."
        )

    return f"Order {order['id']} has been cancelled successfully."