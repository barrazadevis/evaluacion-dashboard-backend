"""
Pydantic Schemas para la API
Validación automática de requests/responses
"""
from pydantic import BaseModel, Field
from typing import Optional


class PromedioCategoriaSchema(BaseModel):
    """Schema para promedio de categoría"""
    categoria: str
    categoria_corta: str
    promedio: float = Field(ge=0, le=5, description="Promedio entre 0 y 5")
    total_evaluaciones: int = Field(ge=0)


class PromedioActorSchema(BaseModel):
    """Schema para promedio por actor"""
    actor: str
    promedio: float = Field(ge=0, le=5)
    total_evaluaciones: int = Field(ge=0)


class PromedioProfesorResponse(BaseModel):
    """Response schema para promedio de profesor"""
    documento: str
    nombre_completo: str
    periodo: Optional[str] = None
    promedio_general: float = Field(ge=0, le=5)
    total_evaluaciones: int = Field(ge=0)
    promedios_por_categoria: list[PromedioCategoriaSchema]
    promedios_por_actor: list[PromedioActorSchema]
    
    class Config:
        json_schema_extra = {
            "example": {
                "documento": "1140844852",
                "nombre_completo": "JAIME ENRIQUE MONCADA DIAZ",
                "periodo": "2025-2",
                "promedio_general": 4.28,
                "total_evaluaciones": 2,
                "promedios_por_categoria": [
                    {
                        "categoria": "ENSEÑANZA-APRENDIZAJE",
                        "categoria_corta": "Enseñanza-Aprendizaje",
                        "promedio": 4.30,
                        "total_evaluaciones": 1
                    }
                ],
                "promedios_por_actor": [
                    {
                        "actor": "AUTOEVALUACIÓN V2",
                        "promedio": 5.0,
                        "total_evaluaciones": 1
                    },
                    {
                        "actor": "ESTUDIANTE V3",
                        "promedio": 4.28,
                        "total_evaluaciones": 1
                    }
                ]
            }
        }


class ProfesorListItem(BaseModel):
    """Schema para item en lista de profesores"""
    documento: str
    nombre_completo: str
    total_evaluaciones: int


class PeriodoListItem(BaseModel):
    """Schema para período en lista"""
    periodo: str
    total_evaluaciones: int


class ErrorResponse(BaseModel):
    """Schema para respuestas de error"""
    error: str
    detail: str
    status_code: int
