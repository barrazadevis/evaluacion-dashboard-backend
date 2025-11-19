"""
Core configuration settings
Aplicando Dependency Inversion y Single Responsibility
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Evaluacion Dashboard API"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # API
    api_prefix: str = "/api/v1"
    allowed_origins: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Vite dev server (alternative)
        "http://localhost:3000",  # Alternative frontend port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ]
    
    # Data paths
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    data_dir: Path = base_dir / "data"
    preguntas_file: Path = data_dir / "preguntas.csv"
    # evaluaciones_file ya no es necesario - carga todos los Evaluacion*.csv automáticamente
    
    # Cache
    enable_cache: bool = True
    cache_ttl: int = 3600  # 1 hour in seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Singleton pattern para settings
    lru_cache asegura una sola instancia
    """
    return Settings()
