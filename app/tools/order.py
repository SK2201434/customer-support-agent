from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from langgraph.types import interrupt
from app.repositories.order import OrderRepository
from app.services.order import OrderService
from app.auth.authorization import is_allowed

repository = OrderRepository()
order_service = OrderService(repository)


@tool
def get_order_status(
    order_id: str | int,
    state: Annotated[dict, InjectedState],
) -> str:
    """Get the status of a customer's order."""
    user = state["user"]

    if not is_allowed(user, "view_own_order"):
        return "You are not authorized to access this order."


    customer_id = user.user_id

    order = order_service.get_customer_order(
        order_id=order_id,
        customer_id=customer_id,
    )

    if order is None:
        return "Order not found or you are not authorized to access this order."

    return order["status"]



@tool
def cancel_order(
    order_id: str | int,
    state: Annotated[dict, InjectedState],
) -> str:
    """Request cancellation of a customer's order."""
    order_id = str(order_id)
    user = state["user"]

    if not is_allowed(user, "cancel_own_order"):
        return "CANCELLATION_DENIED: You are not authorized to cancel this order."

    customer_id = user.user_id

    decision = order_service.get_cancel_decision(
        order_id=order_id,
        customer_id=customer_id,
    )

    if decision == "DENY":
        return (
            "CANCELLATION_DENIED: "
            "The order cannot be cancelled."
        )

    if decision == "APPROVAL_REQUIRED":
        approval = interrupt(
            {
                "type": "order_cancellation",
                "order_id": order_id,
                "message": (
                    f"Order {order_id} is eligible for cancellation. "
                    "Do you approve this cancellation?"
                ),
            }
        )

        if approval is True:
            order = order_service.execute_cancel_order(
                order_id=order_id,
                customer_id=customer_id,
            )

            if order is None:
                return (
                    "CANCELLATION_FAILED: "
                    "The order could not be cancelled."
                )

            return (
                f"Order {order['id']} has been cancelled successfully."
            )

        return (
            "CANCELLATION_DECLINED: "
            f"Order {order_id} was not cancelled."
        )

    return (
        "CANCELLATION_DENIED: "
        "The cancellation policy did not allow this action."
    )
