from langchain_openai import ChatOpenAI

from app.config.settings import settings


def get_llm() -> ChatOpenAI:
    """Create and return the configured cloud chat model."""

    if not settings.openrouter_api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not configured."
        )

    return ChatOpenAI(
        model=settings.openrouter_model,
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        temperature=settings.llm_temperature,
    )