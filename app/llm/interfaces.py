from typing import Protocol


class LLM(Protocol):
    def invoke(self, messages):
        ...