"""
Value Object: Calificacion
Inmutable, self-validating, siguiendo DDD principles
"""
from dataclasses import dataclass
from app.core.exceptions import InvalidCalificacionError


@dataclass(frozen=True)
class Calificacion:
    """
    Value Object que representa una calificación en escala 1-5
    
    Inmutable (frozen=True) - Una vez creado no puede modificarse
    Self-validating - Valida sus propias invariantes
    """
    valor: float
    
    MIN_VALOR: float = 1.0
    MAX_VALOR: float = 5.0
    
    def __post_init__(self) -> None:
        """Validación de invariantes del negocio"""
        if not self.MIN_VALOR <= self.valor <= self.MAX_VALOR:
            raise InvalidCalificacionError(self.valor)
    
    def es_aprobatoria(self) -> bool:
        """Calificación >= 3.0 se considera aprobatoria"""
        return self.valor >= 3.0
    
    def es_excelente(self) -> bool:
        """Calificación >= 4.5 se considera excelente"""
        return self.valor >= 4.5
    
    def nivel_desempeno(self) -> str:
        """Clasificación cualitativa del desempeño"""
        if self.valor >= 4.5:
            return "Excelente"
        elif self.valor >= 4.0:
            return "Sobresaliente"
        elif self.valor >= 3.5:
            return "Bueno"
        elif self.valor >= 3.0:
            return "Aceptable"
        else:
            return "Insuficiente"
    
    def __float__(self) -> float:
        """Permite usar Calificacion directamente en operaciones numéricas"""
        return self.valor
    
    def __str__(self) -> str:
        return f"{self.valor:.2f}"
