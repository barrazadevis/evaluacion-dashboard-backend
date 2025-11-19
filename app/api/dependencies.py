"""
Dependency Injection Container
Configura las dependencias para FastAPI
Aplicando Dependency Injection y Singleton patterns
"""
from functools import lru_cache
from pathlib import Path

from app.core.config import get_settings
from app.infrastructure.parsers.csv_parser import EvaluacionDataLoader
from app.infrastructure.repositories.pandas_repository import (
    PandasEvaluacionRepository,
    PandasPreguntaRepository,
)
from app.domain.repositories.i_repository import IEvaluacionRepository, IPreguntaRepository
from app.application.use_cases import (
    CalcularPromedioProfesorUseCase,
    ObtenerDetalleEvaluacionUseCase,
    ObtenerPropuestaMejoraUseCase,
)


# Singleton para repositorios (cargados una sola vez)
_evaluacion_repo: IEvaluacionRepository | None = None
_pregunta_repo: IPreguntaRepository | None = None


def initialize_repositories() -> None:
    """
    Inicializa los repositorios cargando los datos CSV
    Se llama una sola vez al inicio de la aplicación
    Carga automáticamente todos los archivos Evaluacion*.csv
    """
    global _evaluacion_repo, _pregunta_repo
    
    if _evaluacion_repo is not None and _pregunta_repo is not None:
        return  # Ya inicializados
    
    settings = get_settings()
    
    # Cargar datos usando el data loader
    # Ahora pasa el directorio completo en lugar de un archivo específico
    loader = EvaluacionDataLoader(
        data_dir=settings.data_dir,
        preguntas_path=settings.preguntas_file,
    )
    
    evaluaciones, preguntas = loader.load_all()
    
    # Crear repositorios
    _evaluacion_repo = PandasEvaluacionRepository(evaluaciones)
    _pregunta_repo = PandasPreguntaRepository(preguntas)


def get_evaluacion_repository() -> IEvaluacionRepository:
    """
    Dependency provider para IEvaluacionRepository
    Usado por FastAPI con Depends()
    """
    if _evaluacion_repo is None:
        initialize_repositories()
    return _evaluacion_repo  # type: ignore


def get_pregunta_repository() -> IPreguntaRepository:
    """Dependency provider para IPreguntaRepository"""
    if _pregunta_repo is None:
        initialize_repositories()
    return _pregunta_repo  # type: ignore


# Use Cases factories
def get_calcular_promedio_profesor_use_case():
    """Factory para el use case de promedio de profesor"""
    evaluacion_repo = get_evaluacion_repository()
    return CalcularPromedioProfesorUseCase(evaluacion_repo)


def get_detalle_evaluacion_use_case():
    """Factory para ObtenerDetalleEvaluacionUseCase"""
    evaluacion_repo = get_evaluacion_repository()
    pregunta_repo = get_pregunta_repository()
    return ObtenerDetalleEvaluacionUseCase(evaluacion_repo, pregunta_repo)


def get_propuesta_mejora_use_case():
    """Factory para ObtenerPropuestaMejoraUseCase"""
    evaluacion_repo = get_evaluacion_repository()
    pregunta_repo = get_pregunta_repository()
    return ObtenerPropuestaMejoraUseCase(evaluacion_repo, pregunta_repo)
