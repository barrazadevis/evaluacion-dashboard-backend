"""
Entity: Pregunta
Representa una pregunta del formulario de evaluación
"""
from dataclasses import dataclass
from app.domain.entities.categoria import Categoria


@dataclass
class Pregunta:
    """
    Entity que representa una pregunta de evaluación
    
    Identidad: codigo (P147, P148, etc.)
    """
    codigo: str
    categoria: Categoria
    texto: str
    
    def __eq__(self, other: object) -> bool:
        """Igualdad basada en el código (identidad)"""
        if not isinstance(other, Pregunta):
            return NotImplemented
        return self.codigo == other.codigo
    
    def __hash__(self) -> int:
        """Hash basado en el código para usar en sets/dicts"""
        return hash(self.codigo)
    
    def pertenece_a_categoria(self, categoria: Categoria) -> bool:
        """Verifica si la pregunta pertenece a una categoría"""
        return self.categoria == categoria
    
    def es_comentario(self) -> bool:
        """Verifica si es una pregunta de tipo comentario"""
        return self.categoria == Categoria.COMENTARIOS
    
    def __str__(self) -> str:
        return f"{self.codigo} - {self.categoria.descripcion_corta()}"
