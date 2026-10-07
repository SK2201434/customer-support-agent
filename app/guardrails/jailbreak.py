import re

from app.guardrails.result import (
    GuardrailDecision,
    GuardrailResult,
)


JAILBREAK_PATTERNS = [
    r"ignore (all|any|the) previous instructions",
    r"ignore (all|any|the) prior instructions",
    r"forget (all|any|the) previous instructions",
    r"forget (all|any|the) prior instructions",
    r"forget (all|any|the) your instructions",
    r"forget (all|any|the) your rules",
    r"disregard (all|any|the) previous instructions",
    r"disregard (all|any|the) prior instructions",
    r"override (all|any|the) previous instructions",
    r"override (all|any|the) prior instructions",
    r"ignore your instructions",
    r"ignore your rules",
    r"forget your instructions",
    r"forget your rules",
    r"disregard your instructions",
    r"disregard your rules",
    r"override your instructions",
    r"override your rules",
    r"you are now (an|a|in)",
    r"act as (an|a|if you are)",
    r"pretend (to be|you are)",
    r"reveal (your|the) (system prompt|hidden instructions)",
    r"show (me )?(your|the) (system prompt|hidden instructions)",
    r"print (your|the) (system prompt|hidden instructions)",
    r"what are your system instructions",
    r"what is your system prompt",
]

def detect_jailbreak(message: str) -> GuardrailResult | None:
    normalized_message = message.lower().strip()

    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, normalized_message):
            return GuardrailResult(
                decision=GuardrailDecision.BLOCK,
                reason="prompt_injection",
            )

    return None