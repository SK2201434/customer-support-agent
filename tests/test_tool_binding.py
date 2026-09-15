from langchain_core.messages import HumanMessage

from app.llm.provider import get_llm
from app.tools.order import get_order_status


def test_llm_can_request_order_tool():
    llm = get_llm()

    llm_with_tools = llm.bind_tools(
        [get_order_status]
    )

    response = llm_with_tools.invoke(
        [
            HumanMessage(
                content="What is the status of my order 1001?"
            )
        ]
    )

    print("\nLLM response:")
    print(response)

    print("\nTool calls:")
    print(response.tool_calls)

    assert len(response.tool_calls) > 0