"""
Pydantic schemas para propuestas de mejora
"""
from pydantic import BaseModel
from typing import Optional


class RecomendacionMejoraSchema(BaseModel):
    """Schema para una recomendación de mejora"""
    codigo_pregunta: str
    texto_pregunta: str
    calificacion_promedio: float
    recomendacion: str


class MejoraPorCategoriaSchema(BaseModel):
    """Schema para mejora por categoría"""
    categoria: str
    promedio_categoria: float
    recomendaciones: list[RecomendacionMejoraSchema]


class PropuestaMejoraResponse(BaseModel):
    """Schema para respuesta de propuesta de mejora"""
    documento: str
    nombre_completo: str
    periodo: Optional[str]
    categorias_a_mejorar: list[MejoraPorCategoriaSchema]
