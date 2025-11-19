"""
DTOs para propuestas de mejora
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class RecomendacionMejora:
    """Recomendación de mejora para una pregunta específica"""
    codigo_pregunta: str
    texto_pregunta: str
    calificacion_promedio: float
    recomendacion: str


@dataclass
class MejoraPorCategoria:
    """Propuesta de mejora para una categoría"""
    categoria: str
    promedio_categoria: float
    recomendaciones: list[RecomendacionMejora]


@dataclass
class PropuestaMejoraRequest:
    """Request para obtener propuesta de mejora"""
    documento: str
    periodo: Optional[str] = None


@dataclass
class PropuestaMejoraResponse:
    """Response con propuestas de mejora"""
    documento: str
    nombre_completo: str
    periodo: Optional[str]
    categorias_a_mejorar: list[MejoraPorCategoria]
