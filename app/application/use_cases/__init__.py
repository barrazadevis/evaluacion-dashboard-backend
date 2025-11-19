"""Use Cases module"""
from .calcular_promedio_profesor import CalcularPromedioProfesorUseCase
from .obtener_detalle_evaluacion import ObtenerDetalleEvaluacionUseCase
from .obtener_propuesta_mejora import ObtenerPropuestaMejoraUseCase

__all__ = [
    "CalcularPromedioProfesorUseCase",
    "ObtenerDetalleEvaluacionUseCase",
    "ObtenerPropuestaMejoraUseCase",
]
