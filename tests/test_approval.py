from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command

from app.agent.graph import graph
from app.database.connection import get_connection
from app.repositories.order import OrderRepository


def reset_order_1002():
    connection = get_connection()

    connection.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        ("Processing", "1002"),
    )

    connection.commit()
    connection.close()


def test_order_cancellation_approval():
    reset_order_1002()

    config = {
        "configurable": {
            "thread_id": "test-order-cancellation-approval"
        }
    }

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="Please cancel my order 1002."
                )
            ],
            "user_id": "customer_123",
        },
        config=config,
    )

    # The agent should pause and request human approval.
    assert "__interrupt__" in result

    interrupt_data = result["__interrupt__"]

    assert len(interrupt_data) == 1

    approval_request = interrupt_data[0].value

    assert approval_request["type"] == "order_cancellation"
    assert approval_request["order_id"] == "1002"

    # Resume the graph with human approval.
    result = graph.invoke(
        Command(resume=True),
        config=config,
    )

    messages = result["messages"]

    # The final response should be an AI response.
    final_message = messages[-1]

    assert isinstance(final_message, AIMessage)

    # Verify the actual business outcome in the database.
    order = OrderRepository().get_order("1002")

    assert order is not None
    assert order["status"] == "cancelled"


def test_order_cancellation_declined():
    reset_order_1002()

    config = {
        "configurable": {
            "thread_id": "test-order-cancellation-declined"
        }
    }

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="Please cancel my order 1002."
                )
            ],
            "user_id": "customer_123",
        },
        config=config,
    )

    # The agent should pause and request human approval.
    assert "__interrupt__" in result

    # Resume the graph with the customer declining approval.
    result = graph.invoke(
        Command(resume=False),
        config=config,
    )

    messages = result["messages"]

    # The final response should be an AI response.
    final_message = messages[-1]

    assert isinstance(final_message, AIMessage)

    # Verify that the order was NOT cancelled.
    order = OrderRepository().get_order("1002")

    assert order is not None
    assert order["status"] == "Processing"