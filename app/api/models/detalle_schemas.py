"""
Pydantic schemas para detalle de evaluaciones
"""
from pydantic import BaseModel
from typing import Optional


class RespuestaPreguntaSchema(BaseModel):
    """Schema para una respuesta individual"""
    codigo_pregunta: str
    texto_pregunta: str
    categoria: str
    calificacion: Optional[float]
    tipo_formulario: str


class DetalleEvaluacionResponse(BaseModel):
    """Schema para respuesta de detalle de evaluaciones"""
    documento: str
    nombre_completo: str
    periodo: Optional[str]
    total_evaluaciones: int
    respuestas: list[RespuestaPreguntaSchema]
