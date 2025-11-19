"""Application configuration."""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Project info
    PROJECT_NAME: str = "HRM Platform API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "API for candidate and vacancy matching system"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Scoring weights
    SCORING_WEIGHT_TECHNOLOGIES: int = 40
    SCORING_WEIGHT_EXPERIENCE: int = 20
    SCORING_WEIGHT_SKILLS: int = 15
    SCORING_WEIGHT_STANDARDS: int = 10
    SCORING_WEIGHT_INDUSTRY: int = 5
    SCORING_WEIGHT_LANGUAGES: int = 5
    SCORING_WEIGHT_LOCATION: int = 3
    SCORING_WEIGHT_SALARY: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create settings instance
settings = Settings()
