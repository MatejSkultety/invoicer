from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    DEBUG_MODE: bool = False
    GUEST_MODE: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    
    # Timezone
    TZ: str = "Europe/Bratislava"
    
    # Logging
    LOG_LEVEL: str = "INFO"

    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:80",
        "http://frontend:3000",
    ]

    # Security settings
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "0.0.0.0",
        "frontend",
        "backend",
    ]
    
    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
