"""
Routes para estadísticas generales
"""
from fastapi import APIRouter, Depends

from app.api.dependencies import get_evaluacion_repository
from app.api.models.schemas import PeriodoListItem


router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])


@router.get("/periodos", response_model=list[PeriodoListItem])
async def listar_periodos(
    repo = Depends(get_evaluacion_repository),
) -> list[PeriodoListItem]:
    """
    Lista todos los períodos disponibles con evaluaciones
    
    Returns:
        Lista de períodos ordenados cronológicamente
    """
    periodos = repo.get_periodos_disponibles()
    
    result = []
    for periodo in periodos:
        evaluaciones = repo.find_by_periodo(periodo)
        result.append(
            PeriodoListItem(
                periodo=str(periodo),
                total_evaluaciones=len(evaluaciones),
            )
        )
    
    return result


@router.get("/actores")
async def listar_actores(
    repo = Depends(get_evaluacion_repository),
) -> list[dict]:
    """
    Lista todos los tipos de actores evaluadores
    
    Returns:
        Lista de actores (tipos de formulario)
    """
    actores = repo.get_tipos_formulario()
    
    result = []
    for actor in actores:
        evaluaciones = repo.find_by_tipo_formulario(actor)
        result.append({
            "actor": actor,
            "total_evaluaciones": len(evaluaciones),
        })
    
    return result
