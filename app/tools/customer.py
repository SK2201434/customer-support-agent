from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from app.repositories.customer import CustomerRepository
from app.services.customer import CustomerService


repository = CustomerRepository()
customer_service = CustomerService(repository)


@tool
def get_customer_info(
    state: Annotated[dict, InjectedState],
) -> str:
    """Get information about the currently authenticated customer."""

    customer_id = state["user_id"]

    customer = customer_service.get_customer(customer_id)

    if customer is None:
        return "Customer not found or you are not authorized to access this information."

    return (
        f"Name: {customer['name']}\n"
        f"Email: {customer['email']}\n"
        f"Plan: {customer['plan']}"
    )