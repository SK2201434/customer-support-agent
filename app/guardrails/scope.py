ORDER_KEYWORDS = {
    "order",
    "package",
    "shipment",
    "shipping",
    "delivery",
    "purchase",
    "tracking",
    "cancel",
}

ACCOUNT_KEYWORDS = {
    "account",
    "profile",
    "subscription",
    "plan",
    "membership",
}

PRODUCT_KEYWORDS = {
    "product",
    "products",
    "item",
}

SERVICE_KEYWORDS = {
    "service",
    "services",
    "support",
}


def is_request_in_scope(message: str) -> bool:
    normalized_message = message.lower()

    keyword_groups = (
        ORDER_KEYWORDS,
        ACCOUNT_KEYWORDS,
        PRODUCT_KEYWORDS,
        SERVICE_KEYWORDS,
    )

    return any(
        keyword in normalized_message
        for group in keyword_groups
        for keyword in group
    )