"""
Use Case: Obtener Propuesta de Mejora
Genera recomendaciones basadas en categorías con bajo rendimiento
"""
from typing import Optional
from statistics import mean

from app.application.dtos.mejora_dtos import (
    PropuestaMejoraRequest,
    PropuestaMejoraResponse,
    MejoraPorCategoria,
    RecomendacionMejora,
)
from app.domain.repositories.i_repository import (
    IEvaluacionRepository,
    IPreguntaRepository,
)
from app.core.exceptions import ProfesorNotFoundError


# Mapeo de preguntas a recomendaciones de mejora
RECOMENDACIONES = {
    "PLANEACIÓN DEL PROCESO ENSEÑANZA - APRENDIZAJE - EVALUACIÓN": {
        "default": "Revise y actualice la planificación de sus clases, asegurándose de incluir objetivos claros, metodologías apropiadas y criterios de evaluación alineados con las competencias del módulo.",
        "keywords": {
            "conocimientos actualizados": "Actualice sus conocimientos mediante capacitaciones, lectura de literatura reciente y participación en comunidades académicas de su disciplina.",
            "programa": "Socialice el programa del módulo desde el inicio del periodo, explicando objetivos, contenidos, metodología y criterios de evaluación.",
            "plan": "Desarrolle un plan de trabajo detallado que sea coherente con el programa y las necesidades de aprendizaje de los estudiantes.",
        }
    },
    "CONDUCCIÓN DEL PROCESO ENSEÑANZA-APRENDIZAJE": {
        "default": "Implemente metodologías activas que promuevan la participación estudiantil, el pensamiento crítico y la aplicación práctica del conocimiento.",
        "keywords": {
            "proyectos de aula": "Diseñe proyectos de aula que conecten la teoría con situaciones reales y promuevan la investigación y creatividad estudiantil.",
            "recursos": "Incorpore diversos recursos didácticos (TIC, materiales audiovisuales, laboratorios) para enriquecer el proceso de aprendizaje.",
            "metodología": "Diversifique las estrategias metodológicas para atender diferentes estilos de aprendizaje y mantener la motivación estudiantil.",
            "tecnología": "Integre herramientas tecnológicas (aula virtual, aplicaciones, simuladores) de manera efectiva en sus clases.",
        }
    },
    "EVALUACIÓN DEL APRENDIZAJE": {
        "default": "Diseñe evaluaciones variadas que midan de forma integral las competencias desarrolladas, proporcionando retroalimentación oportuna y constructiva.",
        "keywords": {
            "métodos": "Aplique diferentes métodos de evaluación (pruebas escritas, orales, prácticas, proyectos) según las competencias a valorar.",
            "retroalimentación": "Proporcione retroalimentación clara, específica y oportuna que oriente la mejora del aprendizaje estudiantil.",
            "coherente": "Asegúrese de que las evaluaciones estén alineadas con los objetivos de aprendizaje y las actividades realizadas en clase.",
            "criterios": "Defina y comunique claramente los criterios de evaluación antes de cada actividad evaluativa.",
        }
    },
    "COMPONENTE PERSONAL": {
        "default": "Fortalezca las relaciones interpersonales en el aula mediante el respeto, la empatía y la comunicación efectiva.",
        "keywords": {
            "respeto": "Mantenga una actitud de respeto y tolerancia hacia la diversidad de ideas, creencias y características de los estudiantes.",
            "disciplina": "Establezca normas claras de convivencia y mantenga un ambiente de aprendizaje ordenado y propicio.",
            "comunicación": "Desarrolle habilidades de escucha activa y comunicación asertiva para mejorar la interacción con estudiantes.",
            "puntualidad": "Demuestre responsabilidad y compromiso cumpliendo puntualmente con horarios y compromisos académicos.",
        }
    },
}


class ObtenerPropuestaMejoraUseCase:
    """
    Caso de uso: Obtener propuesta de mejora
    Genera recomendaciones para categorías con promedio < 4
    """

    def __init__(
        self,
        evaluacion_repository: IEvaluacionRepository,
        pregunta_repository: IPreguntaRepository,
    ):
        self._evaluacion_repo = evaluacion_repository
        self._pregunta_repo = pregunta_repository

    def execute(self, request: PropuestaMejoraRequest) -> PropuestaMejoraResponse:
        """
        Genera propuestas de mejora para el profesor
        
        Args:
            request: Solicitud con documento del profesor y periodo opcional
            
        Returns:
            PropuestaMejoraResponse con categorías a mejorar y recomendaciones
            
        Raises:
            ProfesorNotFoundError: Si no se encuentra el profesor
        """
        # Buscar evaluaciones del profesor
        evaluaciones = self._evaluacion_repo.find_by_profesor(request.documento)
        if not evaluaciones:
            raise ProfesorNotFoundError(request.documento)

        profesor_nombre = evaluaciones[0].profesor_nombre

        # Filtrar por período si se especifica
        if request.periodo:
            evaluaciones = [
                ev for ev in evaluaciones 
                if ev.periodo.valor == request.periodo
            ]

        if not evaluaciones:
            raise ProfesorNotFoundError(
                f"No se encontraron evaluaciones para el profesor {request.documento}"
            )

        # Calcular promedios por categoría
        categorias_promedios = self._calcular_promedios_por_categoria(evaluaciones)
        
        # Identificar categorías con promedio < 4
        categorias_a_mejorar = []
        
        for categoria, promedio in categorias_promedios.items():
            if promedio < 4.0:
                # Obtener preguntas de esta categoría con bajo rendimiento
                recomendaciones = self._generar_recomendaciones(
                    categoria, evaluaciones
                )
                
                if recomendaciones:
                    categorias_a_mejorar.append(
                        MejoraPorCategoria(
                            categoria=categoria.value,
                            promedio_categoria=promedio,
                            recomendaciones=recomendaciones,
                        )
                    )

        return PropuestaMejoraResponse(
            documento=request.documento,
            nombre_completo=profesor_nombre,
            periodo=request.periodo,
            categorias_a_mejorar=categorias_a_mejorar,
        )

    def _calcular_promedios_por_categoria(self, evaluaciones) -> dict:
        """Calcula el promedio de cada categoría"""
        from collections import defaultdict
        
        categoria_calificaciones = defaultdict(list)
        
        for evaluacion in evaluaciones:
            for pregunta, calificacion in evaluacion.respuestas.items():
                if calificacion and not pregunta.es_comentario():
                    categoria_calificaciones[pregunta.categoria].append(
                        calificacion.valor
                    )
        
        return {
            cat: mean(cals) 
            for cat, cals in categoria_calificaciones.items()
            if cals
        }

    def _generar_recomendaciones(
        self, categoria, evaluaciones
    ) -> list[RecomendacionMejora]:
        """Genera recomendaciones para una categoría"""
        from collections import defaultdict
        
        # Agrupar calificaciones por pregunta
        pregunta_calificaciones = defaultdict(list)
        
        for evaluacion in evaluaciones:
            for pregunta, calificacion in evaluacion.respuestas.items():
                if (pregunta.categoria == categoria and 
                    calificacion and 
                    not pregunta.es_comentario()):
                    pregunta_calificaciones[pregunta].append(calificacion.valor)
        
        # Generar recomendaciones para preguntas con promedio < 4
        recomendaciones = []
        categoria_nombre = categoria.value
        
        for pregunta, calificaciones in pregunta_calificaciones.items():
            promedio = mean(calificaciones)
            
            if promedio < 4.0:
                recomendacion_texto = self._obtener_recomendacion(
                    categoria_nombre, pregunta.texto
                )
                
                recomendaciones.append(
                    RecomendacionMejora(
                        codigo_pregunta=pregunta.codigo,
                        texto_pregunta=pregunta.texto,
                        calificacion_promedio=promedio,
                        recomendacion=recomendacion_texto,
                    )
                )
        
        # Ordenar por calificación (peor primero)
        recomendaciones.sort(key=lambda r: r.calificacion_promedio)
        
        return recomendaciones

    def _obtener_recomendacion(self, categoria: str, texto_pregunta: str) -> str:
        """Obtiene la recomendación apropiada según la categoría y pregunta"""
        if categoria not in RECOMENDACIONES:
            return "Se recomienda revisar y fortalecer las competencias relacionadas con este aspecto mediante capacitación y reflexión sobre su práctica docente."
        
        config = RECOMENDACIONES[categoria]
        texto_lower = texto_pregunta.lower()
        
        # Buscar coincidencias con palabras clave
        for keyword, recomendacion in config["keywords"].items():
            if keyword in texto_lower:
                return recomendacion
        
        # Si no hay coincidencia, usar recomendación por defecto
        return config["default"]
