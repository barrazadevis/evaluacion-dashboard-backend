"""
Use Case: Calcular Promedio de Profesor
Aplicando Single Responsibility y Dependency Inversion
"""
from statistics import mean
from collections import defaultdict
from typing import Optional

from app.domain.repositories.i_repository import IEvaluacionRepository
from app.domain.entities.categoria import Categoria
from app.domain.value_objects.periodo import Periodo
from app.core.exceptions import ProfesorNotFoundError
from app.application.dtos.profesor_dtos import (
    PromedioProfesorRequest,
    PromedioProfesorResponse,
    PromedioCategoriaDTO,
    PromedioActorDTO,
)


class CalcularPromedioProfesorUseCase:
    """
    Use Case para calcular promedios de un profesor
    
    Responsabilidad única: Calcular y agregar promedios de evaluaciones
    Depende de abstracción (IRepository), no de implementación concreta
    """
    
    def __init__(self, evaluacion_repository: IEvaluacionRepository):
        self._repository = evaluacion_repository
    
    def execute(self, request: PromedioProfesorRequest) -> PromedioProfesorResponse:
        """
        Ejecuta el caso de uso
        
        Args:
            request: DTO con documento y período opcional
            
        Returns:
            Response DTO con todos los promedios calculados
            
        Raises:
            ProfesorNotFoundError: Si el profesor no tiene evaluaciones
        """
        # 1. Obtener evaluaciones del profesor
        evaluaciones = self._repository.find_by_profesor(request.documento)
        
        if not evaluaciones:
            raise ProfesorNotFoundError(request.documento)
        
        # 2. Filtrar por período si se especificó
        if request.periodo:
            periodo_obj = Periodo(request.periodo)
            evaluaciones = [e for e in evaluaciones if e.periodo == periodo_obj]
            
            if not evaluaciones:
                raise ProfesorNotFoundError(
                    f"{request.documento} en período {request.periodo}"
                )
        
        # 3. Calcular promedio general
        promedio_general = self._calcular_promedio_general(evaluaciones)
        
        # 4. Calcular promedios por categoría
        promedios_categoria = self._calcular_por_categoria(evaluaciones)
        
        # 5. Calcular promedios por actor
        promedios_actor = self._calcular_por_actor(evaluaciones)
        
        # 6. Construir response
        return PromedioProfesorResponse(
            documento=request.documento,
            nombre_completo=evaluaciones[0].profesor_nombre,
            periodo=request.periodo,
            promedio_general=promedio_general,
            total_evaluaciones=len(evaluaciones),
            promedios_por_categoria=promedios_categoria,
            promedios_por_actor=promedios_actor,
        )
    
    def _calcular_promedio_general(self, evaluaciones: list) -> float:
        """Calcula el promedio general de todas las evaluaciones"""
        promedios = [e.calcular_promedio_general() for e in evaluaciones]
        return mean(promedios) if promedios else 0.0
    
    def _calcular_por_categoria(self, evaluaciones: list) -> list[PromedioCategoriaDTO]:
        """
        Calcula promedios por categoría
        Agrupa evaluaciones por categoría y calcula promedio
        """
        # Agrupar por categoría
        categoria_promedios: dict[Categoria, list[float]] = defaultdict(list)
        categoria_count: dict[Categoria, int] = defaultdict(int)
        
        for evaluacion in evaluaciones:
            for categoria in evaluacion.categorias_evaluadas():
                if categoria != Categoria.COMENTARIOS:
                    promedio = evaluacion.calcular_promedio_por_categoria(categoria)
                    if promedio > 0:
                        categoria_promedios[categoria].append(promedio)
                        categoria_count[categoria] += 1
        
        # Calcular promedios finales
        resultados = []
        for categoria, promedios in categoria_promedios.items():
            if promedios:
                resultados.append(
                    PromedioCategoriaDTO(
                        categoria=categoria.value,
                        categoria_corta=categoria.descripcion_corta(),
                        promedio=mean(promedios),
                        total_evaluaciones=categoria_count[categoria],
                    )
                )
        
        # Ordenar por nombre de categoría
        return sorted(resultados, key=lambda x: x.categoria)
    
    def _calcular_por_actor(self, evaluaciones: list) -> list[PromedioActorDTO]:
        """
        Calcula promedios por tipo de actor evaluador
        Agrupa por tipo_formulario
        """
        actor_promedios: dict[str, list[float]] = defaultdict(list)
        actor_count: dict[str, int] = defaultdict(int)
        
        for evaluacion in evaluaciones:
            promedio = evaluacion.calcular_promedio_general()
            if promedio > 0:
                actor_promedios[evaluacion.tipo_formulario].append(promedio)
                actor_count[evaluacion.tipo_formulario] += 1
        
        # Calcular promedios finales
        resultados = []
        for actor, promedios in actor_promedios.items():
            if promedios:
                resultados.append(
                    PromedioActorDTO(
                        actor=actor,
                        promedio=mean(promedios),
                        total_evaluaciones=actor_count[actor],
                    )
                )
        
        # Ordenar por tipo de actor
        return sorted(resultados, key=lambda x: x.actor)
