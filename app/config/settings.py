import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_env: str = os.getenv("APP_ENV", "development")

    openrouter_api_key: str = os.getenv(
        "OPENROUTER_API_KEY",
        "",
    )

    openrouter_base_url: str = os.getenv(
        "OPENROUTER_BASE_URL",
        "https://openrouter.ai/api/v1",
    )

    openrouter_model: str = os.getenv(
        "OPENROUTER_MODEL",
        "openai/gpt-chat-latest",
    )

    llm_temperature: float = float(
        os.getenv("LLM_TEMPERATURE", "0")
    )


settings = Settings()