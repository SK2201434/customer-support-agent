from app.config.settings import settings


print("Environment:", settings.app_env)
print("Ollama URL:", settings.openrouter_base_url)
print("Model:", settings.openrouter_model)
print("Temperature:", settings.llm_temperature)