from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.agent.graph import graph


def test_agent_order_status():
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the status of my order 1001?"
                )
            ],
            "user_id": "customer_123",
        },
        config={
        "configurable": {
            "thread_id": "test-agent-order-status"
        }
    },
    )

    messages = result["messages"]

    # First message should be the user's question.
    assert isinstance(messages[0], HumanMessage)

    # The agent should request the order status tool.
    tool_request = next(
        message
        for message in messages
        if isinstance(message, AIMessage) and message.tool_calls
    )

    assert len(tool_request.tool_calls) == 1

    tool_call = tool_request.tool_calls[0]

    assert tool_call["name"] == "get_order_status"
    assert str(tool_call["args"]["order_id"]) == "1001"

    # The tool should return the actual order status.
    tool_result = next(
        message
        for message in messages
        if isinstance(message, ToolMessage)
    )

    assert tool_result.content == "Shipped"

    # The final message should be the customer-facing response.
    final_message = messages[-1]

    assert isinstance(final_message, AIMessage)
    assert final_message.tool_calls == []
    assert "shipped" in final_message.content.lower()


def test_agent_without_tool():
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is 2 + 2?"
                )
            ]
        },
        config={
        "configurable": {
            "thread_id": "test-agent-order-status"
        }
    },
    )

    messages = result["messages"]

    # User message.
    assert isinstance(messages[0], HumanMessage)

    # Final LLM response.
    final_message = messages[-1]

    assert isinstance(final_message, AIMessage)

    # No tool should have been requested.
    assert final_message.tool_calls == []

    # The answer should contain 4.
    assert "4" in final_message.content


def test_agent_prevents_unauthorized_order_access():
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the status of my order 1001?"
                )
            ],
            "user_id": "customer_456",
        },
        config={
        "configurable": {
            "thread_id": "test-agent-order-status"
        }
    },
    )

    messages = result["messages"]

    # Final customer-facing response.
    final_message = messages[-1]

    assert isinstance(final_message, AIMessage)

    # Customer 456 must not receive customer 123's order status.
    assert "shipped" not in final_message.content.lower()
