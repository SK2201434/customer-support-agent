from typing import Annotated

from langchain_core.messages import AnyMessage,SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from app.llm.provider import get_llm
from app.tools.order import get_order_status,get_order_status,cancel_order
from app.tools.customer import get_customer_info

SYSTEM_PROMPT = """

You are a customer support assistant.

Your job is to help customers with questions and requests about
their orders, account, and the company's products and services.

Be helpful, concise, and professional.

When you need information or need to perform an action, use the
appropriate tool.

Tool usage rules:

- Use get_order_status when the customer asks about the status of an order.
- Use get_customer_info when the customer asks about their account information.
- Use cancel_order when the customer explicitly asks to cancel an order.
- When the customer explicitly requests cancellation, call cancel_order
  instead of asking for confirmation yourself.
- Do not guess order or customer information.
- Do not make authorization or business-rule decisions yourself.
- Do not claim that an action was completed unless the corresponding
  tool reports that it was completed.
- If a tool reports that approval is required, do not treat the action
  as completed.
- After receiving a tool result, use that information to provide
  a clear response to the customer.

"""

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_id: str


llm = get_llm()

llm_with_tools = llm.bind_tools(
    [get_order_status,get_customer_info,cancel_order,]
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
    [get_order_status,get_customer_info,cancel_order,]
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
checkpointer = InMemorySaver()
graph = builder.compile(
    checkpointer=checkpointer,
)