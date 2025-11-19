"""
Pandas Repository Implementation
Implementa las interfaces del dominio usando Pandas DataFrames en memoria
Aplicando Repository Pattern y Dependency Inversion
"""
from typing import Optional
from collections import defaultdict

from app.domain.repositories.i_repository import IEvaluacionRepository, IPreguntaRepository
from app.domain.entities.evaluacion import Evaluacion
from app.domain.entities.pregunta import Pregunta
from app.domain.entities.profesor import Profesor
from app.domain.entities.categoria import Categoria
from app.domain.value_objects.periodo import Periodo
from app.core.exceptions import ProfesorNotFoundError


class PandasPreguntaRepository(IPreguntaRepository):
    """
    Implementación del repositorio de preguntas usando listas en memoria
    """
    
    def __init__(self, preguntas: list[Pregunta]):
        self._preguntas = preguntas
        # Índices para búsquedas eficientes (caching)
        self._by_codigo = {p.codigo: p for p in preguntas}
        self._by_categoria = self._build_categoria_index()
    
    def _build_categoria_index(self) -> dict[Categoria, list[Pregunta]]:
        """Construye índice por categoría"""
        index: dict[Categoria, list[Pregunta]] = defaultdict(list)
        for pregunta in self._preguntas:
            index[pregunta.categoria].append(pregunta)
        return dict(index)
    
    def find_all(self) -> list[Pregunta]:
        """Obtiene todas las preguntas"""
        return self._preguntas.copy()
    
    def find_by_codigo(self, codigo: str) -> Optional[Pregunta]:
        """Busca una pregunta por su código - O(1)"""
        return self._by_codigo.get(codigo)
    
    def find_by_categoria(self, categoria: Categoria) -> list[Pregunta]:
        """Obtiene preguntas de una categoría - O(1)"""
        return self._by_categoria.get(categoria, []).copy()
    
    def get_categorias(self) -> list[Categoria]:
        """Obtiene lista de categorías disponibles"""
        return list(self._by_categoria.keys())


class PandasEvaluacionRepository(IEvaluacionRepository):
    """
    Implementación del repositorio de evaluaciones usando listas en memoria
    Optimizado con índices para búsquedas eficientes
    """
    
    def __init__(self, evaluaciones: list[Evaluacion]):
        self._evaluaciones = evaluaciones
        # Construir índices para búsquedas O(1)
        self._by_id = {e.id: e for e in evaluaciones}
        self._by_profesor = self._build_profesor_index()
        self._by_periodo = self._build_periodo_index()
        self._by_tipo_formulario = self._build_tipo_formulario_index()
    
    def _build_profesor_index(self) -> dict[str, list[Evaluacion]]:
        """Índice por documento de profesor"""
        index: dict[str, list[Evaluacion]] = defaultdict(list)
        for evaluacion in self._evaluaciones:
            index[evaluacion.profesor_documento].append(evaluacion)
        return dict(index)
    
    def _build_periodo_index(self) -> dict[Periodo, list[Evaluacion]]:
        """Índice por período"""
        index: dict[Periodo, list[Evaluacion]] = defaultdict(list)
        for evaluacion in self._evaluaciones:
            index[evaluacion.periodo].append(evaluacion)
        return dict(index)
    
    def _build_tipo_formulario_index(self) -> dict[str, list[Evaluacion]]:
        """Índice por tipo de formulario"""
        index: dict[str, list[Evaluacion]] = defaultdict(list)
        for evaluacion in self._evaluaciones:
            index[evaluacion.tipo_formulario].append(evaluacion)
        return dict(index)
    
    def find_all(self) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones"""
        return self._evaluaciones.copy()
    
    def find_by_id(self, evaluacion_id: str) -> Optional[Evaluacion]:
        """Busca una evaluación por su ID - O(1)"""
        return self._by_id.get(evaluacion_id)
    
    def find_by_profesor(self, documento: str) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones de un profesor - O(1)"""
        return self._by_profesor.get(documento, []).copy()
    
    def find_by_periodo(self, periodo: Periodo) -> list[Evaluacion]:
        """Obtiene todas las evaluaciones de un período - O(1)"""
        return self._by_periodo.get(periodo, []).copy()
    
    def find_by_profesor_and_periodo(
        self, 
        documento: str, 
        periodo: Periodo
    ) -> list[Evaluacion]:
        """Obtiene evaluaciones de un profesor en un período - O(n) donde n = evals del profesor"""
        evaluaciones_profesor = self._by_profesor.get(documento, [])
        return [e for e in evaluaciones_profesor if e.periodo == periodo]
    
    def find_by_tipo_formulario(self, tipo: str) -> list[Evaluacion]:
        """Obtiene evaluaciones por tipo de formulario - O(1)"""
        return self._by_tipo_formulario.get(tipo, []).copy()
    
    def get_profesores(self) -> list[Profesor]:
        """
        Obtiene lista de todos los profesores evaluados
        Construye agregado Profesor con sus evaluaciones
        """
        profesores: dict[str, Profesor] = {}
        
        for evaluacion in self._evaluaciones:
            documento = evaluacion.profesor_documento
            
            if documento not in profesores:
                profesores[documento] = Profesor(
                    documento=documento,
                    nombre_completo=evaluacion.profesor_nombre,
                    evaluaciones=[]
                )
            
            profesores[documento].agregar_evaluacion(evaluacion)
        
        return list(profesores.values())
    
    def get_periodos_disponibles(self) -> list[Periodo]:
        """Obtiene lista de períodos con evaluaciones, ordenados"""
        periodos = list(self._by_periodo.keys())
        return sorted(periodos)
    
    def get_tipos_formulario(self) -> list[str]:
        """Obtiene lista de tipos de formulario (actores)"""
        return list(self._by_tipo_formulario.keys())
