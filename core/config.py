from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# absolute path
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # To read variables from a .env file
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH), 
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # APPLICATION SETTINGS
    APP_TITLE: str = "AI Agent Server"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str
    DEBUG_MODE: bool
    
    # DATABASE URL
    DATABASE_URL: str

    # LLM API KEY
    OPENAI_API_KEY: str
    OPENAI_API_BASE: str

    LLM_MODEL_NAME: str

    # SECURITY SETTINGS
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # --- Google OAuth ---
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    # --- Apple OAuth ---
    APPLE_CLIENT_ID: str
    APPLE_KEY_ID: str
    APPLE_TEAM_ID: str
    APPLE_PRIVATE_KEY: str

settings = Settings()