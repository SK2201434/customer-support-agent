from app.repositories.order import OrderRepository


def test_get_order():
    repository = OrderRepository()

    result = repository.get_order("1001")

    assert result == {
        "id": "1001",
        "customer_id": "customer_123",
        "product": "Laptop",
        "status": "Shipped",
    }


def test_get_unknown_order():
    repository = OrderRepository()

    result = repository.get_order("9999")

    assert result is None