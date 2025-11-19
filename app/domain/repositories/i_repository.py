"""
Repository Interface - Dependency Inversion Principle
El dominio define el contrato, la infraestructura lo implementa
"""
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.evaluacion import Evaluacion
from app.domain.entities.pregunta import Pregunta
from app.domain.entities.profesor import Profesor
from app.domain.entities.categoria import Categoria
from app.domain.value_objects.periodo import Periodo


class IEvaluacionRepository(ABC):
    """
    Interface del repositorio de evaluaciones
    
    Aplicando Dependency Inversion Principle:
    - El dominio (capa superior) define la interfaz
    - La infraestructura (capa inferior) la implementa
    - El dominio NO depende de la infraestructura
    """
    
    @abstractmethod
    def find_all(self) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones"""
        pass
    
    @abstractmethod
    def find_by_id(self, evaluacion_id: str) -> Optional[Evaluacion]:
        """Busca una evaluación por su ID"""
        pass
    
    @abstractmethod
    def find_by_profesor(self, documento: str) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones de un profesor"""
        pass
    
    @abstractmethod
    def find_by_periodo(self, periodo: Periodo) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones de un período"""
        pass
    
    @abstractmethod
    def find_by_profesor_and_periodo(
        self, 
        documento: str, 
        periodo: Periodo
    ) -> list[Evaluacion]:
        """Obtiene evaluaciones de un profesor en un período específico"""
        pass
    
    @abstractmethod
    def find_by_tipo_formulario(self, tipo: str) -> list[Evaluacion]:
        """Obtiene evaluaciones por tipo de formulario (actor)"""
        pass
    
    @abstractmethod
    def get_profesores(self) -> list[Profesor]:
        """Obtiene lista de todos los profesores evaluados"""
        pass
    
    @abstractmethod
    def get_periodos_disponibles(self) -> list[Periodo]:
        """Obtiene lista de períodos con evaluaciones"""
        pass
    
    @abstractmethod
    def get_tipos_formulario(self) -> list[str]:
        """Obtiene lista de tipos de formulario (actores)"""
        pass


class IPreguntaRepository(ABC):
    """Interface del repositorio de preguntas"""
    
    @abstractmethod
    def find_all(self) -> list[Pregunta]:
        """Obtiene todas las preguntas"""
        pass
    
    @abstractmethod
    def find_by_codigo(self, codigo: str) -> Optional[Pregunta]:
        """Busca una pregunta por su código"""
        pass
    
    @abstractmethod
    def find_by_categoria(self, categoria: Categoria) -> list[Pregunta]:
        """Obtiene preguntas de una categoría"""
        pass
    
    @abstractmethod
    def get_categorias(self) -> list[Categoria]:
        """Obtiene lista de categorías disponibles"""
        pass
