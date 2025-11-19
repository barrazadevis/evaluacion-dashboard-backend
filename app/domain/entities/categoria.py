"""
Entity: Categoria
Representa una categoría de evaluación
"""
from enum import Enum


class Categoria(str, Enum):
    """
    Enum de categorías de evaluación
    Hereda de str para serialización JSON directa
    """
    PLANEACION = "PLANEACIÓN DEL PROCESO ENSEÑANZA - APRENDIZAJE - EVALUACIÓN"
    CONDUCCION = "CONDUCCIÓN DEL PROCESO ENSEÑANZA-APRENDIZAJE"
    EVALUACION_APRENDIZAJE = "EVALUACIÓN DEL APRENDIZAJE"
    COMPONENTE_PERSONAL = "COMPONENTE PERSONAL"
    COMPORTAMIENTO = "COMPORTAMIENTO"
    ENSENANZA_APRENDIZAJE = "ENSEÑANZA-APRENDIZAJE"
    EVALUACION = "EVALUACIÓN"
    POSGRADO = "POSGRADO"
    ESTRUCTURA_AULA_VIRTUAL = "ESTRUCTURA DE AULA VIRTUAL"
    COMENTARIOS = "COMENTARIOS"
    
    @classmethod
    def from_string(cls, valor: str) -> 'Categoria':
        """
        Factory method para crear Categoria desde string
        Maneja variaciones en el texto
        """
        valor_normalizado = valor.strip().upper()
        
        for categoria in cls:
            if categoria.value.upper() == valor_normalizado:
                return categoria
        
        raise ValueError(f"Categoría no reconocida: {valor}")
    
    @classmethod
    def categorias_principales(cls) -> list['Categoria']:
        """Retorna solo las categorías principales (excluye COMENTARIOS)"""
        return [c for c in cls if c != cls.COMENTARIOS]
    
    def descripcion_corta(self) -> str:
        """Versión corta del nombre para visualizaciones"""
        mapping = {
            self.PLANEACION: "Planeación",
            self.CONDUCCION: "Conducción",
            self.EVALUACION_APRENDIZAJE: "Eval. Aprendizaje",
            self.COMPONENTE_PERSONAL: "Personal",
            self.COMPORTAMIENTO: "Comportamiento",
            self.ENSENANZA_APRENDIZAJE: "Enseñanza-Aprendizaje",
            self.EVALUACION: "Evaluación",
            self.POSGRADO: "Posgrado",
            self.ESTRUCTURA_AULA_VIRTUAL: "Aula Virtual",
            self.COMENTARIOS: "Comentarios"
        }
        return mapping.get(self, self.value)
