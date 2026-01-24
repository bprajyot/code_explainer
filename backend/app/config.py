# ==========================================
# BACKEND - backend/app/config.py
# ==========================================
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "deepseek-coder"
    
    # Application Settings
    APP_NAME: str = "Python Code Explainer"
    DEBUG: bool = False
    OUTPUT_DIR: str = "output"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()