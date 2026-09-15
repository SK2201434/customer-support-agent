from app.repositories.order import OrderRepository
from app.services.order import OrderService


def test_customer_can_access_own_order():
    repository = OrderRepository()
    service = OrderService(repository)

    result = service.get_customer_order(
        order_id="1001",
        customer_id="customer_123",
    )

    assert result is not None
    assert result["id"] == "1001"
    assert result["customer_id"] == "customer_123"
    assert result["status"] == "Shipped"


def test_customer_cannot_access_another_customers_order():
    repository = OrderRepository()
    service = OrderService(repository)

    result = service.get_customer_order(
        order_id="1001",
        customer_id="customer_456",
    )

    assert result is None


def test_unknown_order():
    repository = OrderRepository()
    service = OrderService(repository)

    result = service.get_customer_order(
        order_id="9999",
        customer_id="customer_123",
    )

    assert result is None