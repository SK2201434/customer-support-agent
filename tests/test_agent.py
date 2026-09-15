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
        }
    )

    messages = result["messages"]

    assert len(messages) == 4

    # First message should be the user's question.
    assert isinstance(messages[0], HumanMessage)

    # Second message should contain the tool request.
    assert isinstance(messages[1], AIMessage)
    assert len(messages[1].tool_calls) == 1

    tool_call = messages[1].tool_calls[0]

    assert tool_call["name"] == "get_order_status"
    assert tool_call["args"]["order_id"] == "1001"

    # Third message should contain the tool result.
    assert isinstance(messages[2], ToolMessage)
    assert messages[2].content == "Shipped"

    # Fourth message should be the final customer-facing response.
    assert isinstance(messages[3], AIMessage)
    assert messages[3].tool_calls == []
    assert "shipped" in messages[3].content.lower()


def test_agent_without_tool():
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is 2 + 2?"
                )
            ]
        }
    )

    messages = result["messages"]

    assert len(messages) == 2

    # User message
    assert isinstance(messages[0], HumanMessage)

    # Final LLM response
    assert isinstance(messages[1], AIMessage)

    # No tool should have been requested.
    assert messages[1].tool_calls == []

    # The answer should contain 4.
    assert "4" in messages[1].content

def test_agent_prevents_unauthorized_order_access():
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the status of my order 1001?"
                )
            ],
            "user_id": "customer_456",
        }
    )

    messages = result["messages"]

    final_message = messages[-1]

    assert isinstance(final_message, AIMessage)

    assert "shipped" not in final_message.content.lower()