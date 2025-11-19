"""
Entity: Evaluacion
Representa una evaluación realizada por un actor a un profesor
"""
from dataclasses import dataclass, field
from typing import Optional
from statistics import mean

from app.domain.value_objects.calificacion import Calificacion
from app.domain.value_objects.periodo import Periodo
from app.domain.entities.pregunta import Pregunta
from app.domain.entities.categoria import Categoria


@dataclass
class Evaluacion:
    """
    Entity que representa una evaluación
    
    Identidad: id (PEGE_ID)
    """
    id: str
    profesor_documento: str
    profesor_nombre: str
    periodo: Periodo
    tipo_formulario: str  # AUTOEVALUACIÓN V2, ESTUDIANTE V3, etc.
    respuestas: dict[Pregunta, Optional[Calificacion]] = field(default_factory=dict)
    
    def __eq__(self, other: object) -> bool:
        """Igualdad basada en el ID"""
        if not isinstance(other, Evaluacion):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash basado en el ID"""
        return hash(self.id)
    
    def agregar_respuesta(self, pregunta: Pregunta, calificacion: Optional[Calificacion]) -> None:
        """Agrega una respuesta a la evaluación"""
        self.respuestas[pregunta] = calificacion
    
    def calcular_promedio_general(self) -> float:
        """
        Calcula el promedio general de todas las respuestas válidas
        Ignora respuestas None y preguntas de comentarios
        """
        calificaciones = [
            float(cal) 
            for pregunta, cal in self.respuestas.items() 
            if cal is not None and not pregunta.es_comentario()
        ]
        
        if not calificaciones:
            return 0.0
        
        return mean(calificaciones)
    
    def calcular_promedio_por_categoria(self, categoria: Categoria) -> float:
        """Calcula el promedio de una categoría específica"""
        calificaciones = [
            float(cal)
            for pregunta, cal in self.respuestas.items()
            if cal is not None 
            and pregunta.pertenece_a_categoria(categoria)
        ]
        
        if not calificaciones:
            return 0.0
        
        return mean(calificaciones)
    
    def obtener_respuestas_por_categoria(self, categoria: Categoria) -> dict[Pregunta, Calificacion]:
        """Retorna todas las respuestas de una categoría específica"""
        return {
            pregunta: cal
            for pregunta, cal in self.respuestas.items()
            if cal is not None and pregunta.pertenece_a_categoria(categoria)
        }
    
    def categorias_evaluadas(self) -> set[Categoria]:
        """Retorna el conjunto de categorías que tienen respuestas"""
        return {
            pregunta.categoria
            for pregunta in self.respuestas.keys()
            if not pregunta.es_comentario()
        }
    
    def es_autoevaluacion(self) -> bool:
        """Verifica si es una autoevaluación"""
        return "AUTOEVALUACIÓN" in self.tipo_formulario.upper()
    
    def es_evaluacion_estudiante(self) -> bool:
        """Verifica si es evaluación de estudiante"""
        return "ESTUDIANTE" in self.tipo_formulario.upper()
    
    def total_respuestas_validas(self) -> int:
        """Cuenta respuestas válidas (no None, no comentarios)"""
        return sum(
            1 for pregunta, cal in self.respuestas.items()
            if cal is not None and not pregunta.es_comentario()
        )
    
    def __str__(self) -> str:
        return f"Evaluación {self.id} - {self.tipo_formulario} - {self.periodo}"
