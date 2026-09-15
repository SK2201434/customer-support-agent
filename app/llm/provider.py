from langchain_ollama import ChatOllama

from app.config.settings import settings


def get_llm() -> ChatOllama:
    """Create and return the configured chat model."""

    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=settings.llm_temperature,
    )