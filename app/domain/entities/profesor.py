"""
Entity: Profesor
Representa un docente evaluado
"""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.entities.evaluacion import Evaluacion


@dataclass
class Profesor:
    """
    Entity que representa un profesor
    
    Identidad: documento
    Aggregate Root para las evaluaciones del profesor
    """
    documento: str
    nombre_completo: str
    evaluaciones: list['Evaluacion'] = field(default_factory=list)
    
    def __eq__(self, other: object) -> bool:
        """Igualdad basada en el documento (identidad)"""
        if not isinstance(other, Profesor):
            return NotImplemented
        return self.documento == other.documento
    
    def __hash__(self) -> int:
        """Hash basado en el documento"""
        return hash(self.documento)
    
    def agregar_evaluacion(self, evaluacion: 'Evaluacion') -> None:
        """Agrega una evaluación al profesor"""
        if evaluacion not in self.evaluaciones:
            self.evaluaciones.append(evaluacion)
    
    def total_evaluaciones(self) -> int:
        """Retorna el número total de evaluaciones"""
        return len(self.evaluaciones)
    
    def tiene_evaluaciones(self) -> bool:
        """Verifica si el profesor tiene evaluaciones"""
        return len(self.evaluaciones) > 0
    
    def __str__(self) -> str:
        return f"{self.nombre_completo} ({self.documento})"
