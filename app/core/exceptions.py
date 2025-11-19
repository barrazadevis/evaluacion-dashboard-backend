"""
Custom exceptions para el dominio
Aplicando Fail-Fast y Error Handling explícito
"""


class DomainException(Exception):
    """Base exception para errores del dominio"""
    pass


class EvaluacionNotFoundError(DomainException):
    """Evaluación no encontrada"""
    def __init__(self, evaluacion_id: str):
        self.evaluacion_id = evaluacion_id
        super().__init__(f"Evaluación con ID {evaluacion_id} no encontrada")


class ProfesorNotFoundError(DomainException):
    """Profesor no encontrado"""
    def __init__(self, documento: str):
        self.documento = documento
        super().__init__(f"Profesor con documento {documento} no encontrado")


class InvalidCalificacionError(DomainException):
    """Calificación fuera del rango válido"""
    def __init__(self, valor: float):
        self.valor = valor
        super().__init__(f"Calificación {valor} fuera del rango válido (1-5)")


class DataParsingError(DomainException):
    """Error al parsear archivos de datos"""
    def __init__(self, file_path: str, details: str):
        self.file_path = file_path
        self.details = details
        super().__init__(f"Error parseando {file_path}: {details}")


class CategoriaNotFoundError(DomainException):
    """Categoría no encontrada"""
    def __init__(self, categoria: str):
        self.categoria = categoria
        super().__init__(f"Categoría '{categoria}' no encontrada")
