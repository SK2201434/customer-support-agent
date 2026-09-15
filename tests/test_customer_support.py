from app.models.schemas import CustomerSupportRequest
from app.services.customer_support import handle_customer_request


class FakeLLM:
    def invoke(self, messages):
        class FakeResponse:
            content = "Your request has been received."

        return FakeResponse()


def test_handle_customer_request():
    request = CustomerSupportRequest(
        message="I need help with my order.",
        user_id="customer_123",
        conversation_id="conversation_456",
    )

    response = handle_customer_request(
        request,
        llm=FakeLLM(),
    )

    assert response.message == "Your request has been received."
    assert response.conversation_id == "conversation_456"