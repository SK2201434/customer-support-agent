from app.guardrails.jailbreak import detect_jailbreak
from app.guardrails.scope import is_request_in_scope
from app.guardrails.result import (
    GuardrailDecision,
    GuardrailResult,
)


def check_guardrail(message: str) -> GuardrailResult:
    normalized_message = message.strip()

    if not normalized_message:
        return GuardrailResult(
            decision=GuardrailDecision.OUT_OF_SCOPE,
            reason="empty_request",
        )

    jailbreak_result = detect_jailbreak(normalized_message)

    if jailbreak_result is not None:
        return jailbreak_result

    return is_request_in_scope(normalized_message)