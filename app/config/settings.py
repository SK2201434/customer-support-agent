import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    app_env: str = os.getenv("APP_ENV", "development")

    ollama_base_url: str = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    )

    ollama_model: str = os.getenv(
        "OLLAMA_MODEL",
        "qwen3:8b",
    )

    llm_temperature: float = float(
        os.getenv("LLM_TEMPERATURE", "0")
    )


settings = Settings()