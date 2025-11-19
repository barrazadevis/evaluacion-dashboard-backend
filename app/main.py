"""
FastAPI Main Application
Punto de entrada de la aplicación
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import get_settings
from app.api.routes import profesores_router, estadisticas_router
from app.api.dependencies import initialize_repositories

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Obtener settings
settings = get_settings()

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para análisis de evaluaciones docentes con Clean Architecture",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Evento que se ejecuta al iniciar la aplicación
    Inicializa repositorios cargando datos CSV
    """
    logger.info("Iniciando aplicación...")
    logger.info(f"Versión: {settings.app_version}")
    
    try:
        # Inicializar repositorios (carga de datos)
        initialize_repositories()
        logger.info("Datos cargados exitosamente")
    except Exception as e:
        logger.error(f"Error al cargar datos: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Evento que se ejecuta al apagar la aplicación"""
    logger.info("Apagando aplicación...")


@app.get("/")
async def root() -> dict:
    """Endpoint raíz con información de la API"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check() -> dict:
    """Health check endpoint para monitoreo"""
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


# Registrar routers
app.include_router(profesores_router, prefix=settings.api_prefix)
app.include_router(estadisticas_router, prefix=settings.api_prefix)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
