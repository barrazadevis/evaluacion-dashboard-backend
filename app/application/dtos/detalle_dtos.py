"""
DTOs para detalle de evaluaciones por pregunta
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class RespuestaPreguntaDTO:
    """Respuesta de una pregunta en una evaluación"""
    codigo_pregunta: str
    texto_pregunta: str
    categoria: str
    calificacion: Optional[float]
    tipo_formulario: str


@dataclass
class DetalleEvaluacionRequest:
    """Request para obtener detalle de evaluaciones"""
    documento: str
    periodo: Optional[str] = None


@dataclass
class DetalleEvaluacionResponse:
    """Response con detalle de evaluaciones por pregunta"""
    documento: str
    nombre_completo: str
    periodo: Optional[str]
    total_evaluaciones: int
    respuestas: list[RespuestaPreguntaDTO]
