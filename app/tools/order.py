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