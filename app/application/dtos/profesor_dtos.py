"""
DTOs (Data Transfer Objects)
Objetos para transferir datos entre capas
Aplicando DTO Pattern y separación de responsabilidades
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class PromedioProfesorRequest:
    """Request DTO para calcular promedio de profesor"""
    documento: str
    periodo: Optional[str] = None  # Opcional - si no se pasa, usa todos los períodos


@dataclass
class PromedioCategoriaDTO:
    """DTO para promedio de una categoría"""
    categoria: str
    categoria_corta: str
    promedio: float
    total_evaluaciones: int


@dataclass
class PromedioActorDTO:
    """DTO para promedio por tipo de actor evaluador"""
    actor: str
    promedio: float
    total_evaluaciones: int


@dataclass
class PromedioProfesorResponse:
    """Response DTO con todos los promedios del profesor"""
    documento: str
    nombre_completo: str
    periodo: Optional[str]
    promedio_general: float
    total_evaluaciones: int
    promedios_por_categoria: list[PromedioCategoriaDTO]
    promedios_por_actor: list[PromedioActorDTO]


@dataclass
class EstadisticasCategoriaRequest:
    """Request para estadísticas de categoría"""
    categoria: str
    periodo: Optional[str] = None


@dataclass
class EstadisticasCategoriaResponse:
    """Response con estadísticas de una categoría"""
    categoria: str
    periodo: Optional[str]
    promedio_general: float
    promedio_maximo: float
    promedio_minimo: float
    desviacion_estandar: float
    total_evaluaciones: int
    total_profesores: int


@dataclass
class ComparacionActoresRequest:
    """Request para comparar actores evaluadores"""
    documento: str
    periodo: Optional[str] = None


@dataclass
class ComparacionActoresResponse:
    """Response comparando autoevaluación vs otros actores"""
    documento: str
    nombre_completo: str
    periodo: Optional[str]
    promedio_autoevaluacion: float
    promedio_estudiantes: float
    brecha: float  # Diferencia entre auto y estudiantes
    total_evaluaciones: int
