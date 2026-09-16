"""
config.py — Application configuration.

Loads and validates environment variables (like the API key and the
active AI model) from the .env file. Using pydantic-settings means
the app fails early and clearly if a required secret is missing,
instead of crashing later, deep inside a request.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Holds all app configuration, loaded from environment variables."""
    anthropic_api_key: str = ""

    # The Gemini API key — read from .env, never hard-coded.
    # Get a free-tier key at https://aistudio.google.com/apikey
    gemini_api_key: str

    # Which Gemini model to call. Has a sensible default, but can be
    # overridden in .env without touching any code — e.g. to test a
    # newer model or roll back if one gets deprecated.
    gemini_model: str = "gemini-3.6-flash"

    # Tells pydantic-settings to read from the .env file.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# A single shared instance the rest of the app imports.
settings = Settings()
