from dataclasses import dataclass
from enum import Enum


class GuardrailDecision(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    OUT_OF_SCOPE = "out_of_scope"


@dataclass(frozen=True)
class GuardrailResult:
    decision: GuardrailDecision
    reason: str