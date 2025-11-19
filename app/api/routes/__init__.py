"""Routes module"""
from .profesores import router as profesores_router
from .estadisticas import router as estadisticas_router

__all__ = ["profesores_router", "estadisticas_router"]
