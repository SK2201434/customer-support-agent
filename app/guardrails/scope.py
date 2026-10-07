from app.guardrails.result import (
    GuardrailDecision,
    GuardrailResult,
)


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


def is_request_in_scope(message: str) -> GuardrailResult:
    normalized_message = message.lower().strip()

    keyword_groups = (
        ORDER_KEYWORDS,
        ACCOUNT_KEYWORDS,
        PRODUCT_KEYWORDS,
        SERVICE_KEYWORDS,
    )

    for group in keyword_groups:
        for keyword in group:
            if keyword in normalized_message:
                return GuardrailResult(
                    decision=GuardrailDecision.ALLOW,
                    reason="customer_support_request",
                )

    return GuardrailResult(
        decision=GuardrailDecision.OUT_OF_SCOPE,
        reason="unrelated_request",
    )