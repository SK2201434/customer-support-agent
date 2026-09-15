from langchain_core.messages import HumanMessage, SystemMessage

from app.llm.provider import get_llm
from app.models.schemas import (
    CustomerSupportRequest,
    CustomerSupportResponse,
)


SYSTEM_PROMPT = """
You are a customer support assistant.

Your job is to help customers with questions about the company's
products and services.

Be helpful, concise, and professional.

Do not invent information.
If you do not know something, say that you do not have enough
information to answer accurately.
"""


def handle_customer_request(
    request: CustomerSupportRequest,
    llm=None,
) -> CustomerSupportResponse:
    """Handle a customer support request using the LLM."""

    if llm is None:
        llm = get_llm()

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=request.message),
    ]

    response = llm.invoke(messages)

    return CustomerSupportResponse(
        message=response.content,
        conversation_id=request.conversation_id,
    )