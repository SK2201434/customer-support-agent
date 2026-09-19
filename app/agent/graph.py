from typing import Annotated

from langchain_core.messages import AnyMessage,SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from app.llm.provider import get_llm
from app.tools.order import get_order_status
from app.tools.customer import get_customer_info

SYSTEM_PROMPT = """
You are a customer support assistant.

Your job is to help customers with questions about their orders
and the company's products and services.

Be helpful, concise, and professional.

When you need information about an order, use the appropriate tool.
Do not guess order information.

After receiving a tool result, use that information to provide
a clear response to the customer.
"""


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_id: str


llm = get_llm()

llm_with_tools = llm.bind_tools(
    [get_order_status,get_customer_info,]
)


def llm_node(state: AgentState):
    messages =[
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]
    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }

def should_continue(state:AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

tool_node = ToolNode(
    [get_order_status,get_customer_info,]
)


builder = StateGraph(AgentState)

builder.add_node("llm", llm_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "llm")
builder.add_conditional_edges(
    "llm",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)
builder.add_edge("tools", "llm")

graph = builder.compile()