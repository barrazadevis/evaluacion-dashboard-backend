"""
Use Case: Obtener Detalle de Evaluaciones por Pregunta
"""
from typing import Optional

from app.application.dtos.detalle_dtos import (
    DetalleEvaluacionRequest,
    DetalleEvaluacionResponse,
    RespuestaPreguntaDTO,
)
from app.domain.repositories.i_repository import (
    IEvaluacionRepository,
    IPreguntaRepository,
)
from app.core.exceptions import ProfesorNotFoundError


class ObtenerDetalleEvaluacionUseCase:
    """
    Caso de uso: Obtener detalle de todas las respuestas por pregunta
    """

    def __init__(
        self,
        evaluacion_repository: IEvaluacionRepository,
        pregunta_repository: IPreguntaRepository,
    ):
        self._evaluacion_repo = evaluacion_repository
        self._pregunta_repo = pregunta_repository

    def execute(self, request: DetalleEvaluacionRequest) -> DetalleEvaluacionResponse:
        """
        Obtiene el detalle de todas las respuestas agrupadas por pregunta
        
        Args:
            request: Solicitud con documento del profesor y periodo opcional
            
        Returns:
            DetalleEvaluacionResponse con todas las respuestas
            
        Raises:
            ProfesorNotFoundError: Si no se encuentra el profesor
        """
        # Buscar evaluaciones del profesor
        evaluaciones = self._evaluacion_repo.find_by_profesor(request.documento)
        if not evaluaciones:
            raise ProfesorNotFoundError(request.documento)

        # Obtener información del profesor de la primera evaluación
        profesor_nombre = evaluaciones[0].profesor_nombre

        # Filtrar evaluaciones por período si se especifica
        if request.periodo:
            evaluaciones = [
                ev for ev in evaluaciones 
                if ev.periodo.valor == request.periodo
            ]

        if not evaluaciones:
            periodo_msg = f" en el período {request.periodo}" if request.periodo else ""
            raise ProfesorNotFoundError(
                f"No se encontraron evaluaciones para el profesor {request.documento}{periodo_msg}"
            )

        # Recolectar todas las respuestas de todas las evaluaciones
        respuestas: list[RespuestaPreguntaDTO] = []
        
        for evaluacion in evaluaciones:
            for pregunta, calificacion in evaluacion.respuestas.items():
                # La clave del diccionario es el objeto Pregunta, no el código
                respuestas.append(
                    RespuestaPreguntaDTO(
                        codigo_pregunta=pregunta.codigo,
                        texto_pregunta=pregunta.texto,
                        categoria=pregunta.categoria.value,
                        calificacion=calificacion.valor if calificacion else None,
                        tipo_formulario=evaluacion.tipo_formulario,
                    )
                )

        return DetalleEvaluacionResponse(
            documento=request.documento,
            nombre_completo=profesor_nombre,
            periodo=request.periodo,
            total_evaluaciones=len(evaluaciones),
            respuestas=respuestas,
        )
