from app.config.settings import settings


print("Environment:", settings.app_env)
print("Ollama URL:", settings.ollama_base_url)
print("Model:", settings.ollama_model)
print("Temperature:", settings.llm_temperature)