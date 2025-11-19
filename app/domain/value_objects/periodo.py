"""
Value Object: Periodo
Representa un período académico (ej: 2025-2)
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Periodo:
    """
    Value Object para período académico
    Formato esperado: YYYY-N (ej: 2025-2)
    """
    valor: str
    
    PATTERN = re.compile(r'^\d{4}-[12]$')
    
    def __post_init__(self) -> None:
        """Valida formato del período"""
        if not self.PATTERN.match(self.valor):
            raise ValueError(
                f"Formato de período inválido: {self.valor}. "
                "Esperado: YYYY-1 o YYYY-2"
            )
    
    @property
    def anio(self) -> int:
        """Extrae el año del período"""
        return int(self.valor.split('-')[0])
    
    @property
    def semestre(self) -> int:
        """Extrae el semestre (1 o 2)"""
        return int(self.valor.split('-')[1])
    
    def es_mismo_anio(self, otro: 'Periodo') -> bool:
        """Compara si dos períodos son del mismo año"""
        return self.anio == otro.anio
    
    def __str__(self) -> str:
        return self.valor
    
    def __lt__(self, otro: 'Periodo') -> bool:
        """Permite ordenar períodos cronológicamente"""
        if self.anio != otro.anio:
            return self.anio < otro.anio
        return self.semestre < otro.semestre
