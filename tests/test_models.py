from app.models.schemas import (
    CustomerSupportRequest,
    CustomerSupportResponse,
)


def test_customer_support_request():
    request = CustomerSupportRequest(
        message="Where is my order 1001?",
        user_id="customer_123",
        conversation_id="conversation_456",
    )

    assert request.message == "Where is my order 1001?"
    assert request.user_id == "customer_123"
    assert request.conversation_id == "conversation_456"


def test_customer_support_response():
    response = CustomerSupportResponse(
        message="Your order has been shipped.",
        conversation_id="conversation_456",
    )

    assert response.message == "Your order has been shipped."
    assert response.conversation_id == "conversation_456"