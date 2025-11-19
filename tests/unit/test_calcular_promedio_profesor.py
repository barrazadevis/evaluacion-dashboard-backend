"""
Test para CalcularPromedioProfesorUseCase
Aplicando principios de testing: AAA (Arrange, Act, Assert)
"""
import pytest
from unittest.mock import Mock

from app.application.use_cases.calcular_promedio_profesor import CalcularPromedioProfesorUseCase
from app.application.dtos.profesor_dtos import PromedioProfesorRequest
from app.domain.entities.evaluacion import Evaluacion
from app.domain.entities.pregunta import Pregunta
from app.domain.entities.categoria import Categoria
from app.domain.value_objects.calificacion import Calificacion
from app.domain.value_objects.periodo import Periodo
from app.core.exceptions import ProfesorNotFoundError


class TestCalcularPromedioProfesorUseCase:
    """Test suite para el use case de cálculo de promedios"""
    
    def test_calcula_promedio_con_una_evaluacion(self):
        """Test: Calcula correctamente el promedio con una sola evaluación"""
        # Arrange
        mock_repo = Mock()
        
        # Crear pregunta de prueba
        pregunta = Pregunta(
            codigo="P364",
            categoria=Categoria.ENSENANZA_APRENDIZAJE,
            texto="Pregunta de prueba"
        )
        
        # Crear evaluación de prueba
        evaluacion = Evaluacion(
            id="1",
            profesor_documento="123456",
            profesor_nombre="Juan Pérez",
            periodo=Periodo("2025-2"),
            tipo_formulario="ESTUDIANTE V3"
        )
        evaluacion.agregar_respuesta(pregunta, Calificacion(4.5))
        
        mock_repo.find_by_profesor.return_value = [evaluacion]
        
        use_case = CalcularPromedioProfesorUseCase(mock_repo)
        request = PromedioProfesorRequest(documento="123456")
        
        # Act
        result = use_case.execute(request)
        
        # Assert
        assert result.documento == "123456"
        assert result.nombre_completo == "Juan Pérez"
        assert result.promedio_general == 4.5
        assert result.total_evaluaciones == 1
        assert len(result.promedios_por_categoria) > 0
        assert len(result.promedios_por_actor) > 0
    
    def test_lanza_excepcion_cuando_profesor_no_existe(self):
        """Test: Lanza ProfesorNotFoundError cuando no hay evaluaciones"""
        # Arrange
        mock_repo = Mock()
        mock_repo.find_by_profesor.return_value = []
        
        use_case = CalcularPromedioProfesorUseCase(mock_repo)
        request = PromedioProfesorRequest(documento="999999")
        
        # Act & Assert
        with pytest.raises(ProfesorNotFoundError):
            use_case.execute(request)
    
    def test_filtra_por_periodo_correctamente(self):
        """Test: Filtra evaluaciones por período cuando se especifica"""
        # Arrange
        mock_repo = Mock()
        
        pregunta = Pregunta(
            codigo="P364",
            categoria=Categoria.ENSENANZA_APRENDIZAJE,
            texto="Pregunta de prueba"
        )
        
        # Evaluación período 2025-1
        eval1 = Evaluacion(
            id="1",
            profesor_documento="123456",
            profesor_nombre="Juan Pérez",
            periodo=Periodo("2025-1"),
            tipo_formulario="ESTUDIANTE V3"
        )
        eval1.agregar_respuesta(pregunta, Calificacion(3.0))
        
        # Evaluación período 2025-2
        eval2 = Evaluacion(
            id="2",
            profesor_documento="123456",
            profesor_nombre="Juan Pérez",
            periodo=Periodo("2025-2"),
            tipo_formulario="ESTUDIANTE V3"
        )
        eval2.agregar_respuesta(pregunta, Calificacion(5.0))
        
        mock_repo.find_by_profesor.return_value = [eval1, eval2]
        
        use_case = CalcularPromedioProfesorUseCase(mock_repo)
        request = PromedioProfesorRequest(documento="123456", periodo="2025-2")
        
        # Act
        result = use_case.execute(request)
        
        # Assert
        assert result.periodo == "2025-2"
        assert result.promedio_general == 5.0  # Solo la eval2
        assert result.total_evaluaciones == 1
    
    def test_agrupa_por_categoria_correctamente(self):
        """Test: Agrupa y calcula promedios por categoría"""
        # Arrange
        mock_repo = Mock()
        
        pregunta1 = Pregunta(
            codigo="P364",
            categoria=Categoria.ENSENANZA_APRENDIZAJE,
            texto="Pregunta 1"
        )
        pregunta2 = Pregunta(
            codigo="P376",
            categoria=Categoria.EVALUACION,
            texto="Pregunta 2"
        )
        
        evaluacion = Evaluacion(
            id="1",
            profesor_documento="123456",
            profesor_nombre="Juan Pérez",
            periodo=Periodo("2025-2"),
            tipo_formulario="ESTUDIANTE V3"
        )
        evaluacion.agregar_respuesta(pregunta1, Calificacion(4.0))
        evaluacion.agregar_respuesta(pregunta2, Calificacion(5.0))
        
        mock_repo.find_by_profesor.return_value = [evaluacion]
        
        use_case = CalcularPromedioProfesorUseCase(mock_repo)
        request = PromedioProfesorRequest(documento="123456")
        
        # Act
        result = use_case.execute(request)
        
        # Assert
        assert len(result.promedios_por_categoria) == 2
        categorias = [c.categoria_corta for c in result.promedios_por_categoria]
        assert "Enseñanza-Aprendizaje" in categorias
        assert "Evaluación" in categorias
