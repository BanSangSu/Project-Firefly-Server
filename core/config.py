from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

import os


# On your server (e.g., Render), you should create an environment variable
# named 'APP_ENV' with the value 'production'.
APP_ENV = os.getenv('APP_ENV', 'local')

# Determine the .env file path based on the environment
if APP_ENV == 'production':
    # This block runs on the server (e.g., Render).
    # It uses the absolute path where secrets are mounted.
    ENV_PATH = Path("/etc/secrets/.env")
else:
    # This block runs on your local development machine.
    # It finds the .env file located in the same directory as your settings file.
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
