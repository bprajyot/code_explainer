# ==========================================
# BACKEND - backend/app/config.py (ADD TIMEOUT CONFIGS)
# ==========================================
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "deepseek-coder"
    
    # Timeout Configuration (in seconds)
    OLLAMA_TIMEOUT_SHORT: float = 180.0
    OLLAMA_TIMEOUT_MEDIUM: float = 300.0
    OLLAMA_TIMEOUT_LONG: float = 600.0
    
    # Application Settings
    APP_NAME: str = "Python Code Explainer"
    DEBUG: bool = False
    OUTPUT_DIR: str = "output"
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()