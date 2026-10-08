from app.guardrails.jailbreak import detect_jailbreak
from app.guardrails.scope import is_request_in_scope
from app.guardrails.semantic import classify_request
from app.guardrails.result import (
    GuardrailDecision,
    GuardrailResult,
)


def check_guardrail(message: str) -> GuardrailResult:
    normalized_message = message.strip()

    # 1. Empty request
    if not normalized_message:
        return GuardrailResult(
            decision=GuardrailDecision.OUT_OF_SCOPE,
            reason="empty_request",
        )

    # 2. Deterministic jailbreak / prompt-injection detection
    jailbreak_result = detect_jailbreak(normalized_message)

    if jailbreak_result is not None:
        return jailbreak_result

    # 3. Fast deterministic customer-support scope check
    scope_result = is_request_in_scope(normalized_message)

    if scope_result.decision == GuardrailDecision.ALLOW:
        return scope_result

    # 4. Semantic fallback for requests that keyword matching
    #    could not confidently classify.
    return classify_request(normalized_message)