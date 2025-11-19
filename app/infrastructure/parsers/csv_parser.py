"""
CSV Parser - Infrastructure Layer
Convierte archivos CSV en entidades del dominio
Aplicando Single Responsibility y Factory Pattern
"""
import pandas as pd
from pathlib import Path
from typing import Optional
import logging

from app.domain.entities.pregunta import Pregunta
from app.domain.entities.evaluacion import Evaluacion
from app.domain.entities.categoria import Categoria
from app.domain.value_objects.calificacion import Calificacion
from app.domain.value_objects.periodo import Periodo
from app.core.exceptions import DataParsingError

logger = logging.getLogger(__name__)


class PreguntaCSVParser:
    """
    Parser para el archivo preguntas.csv
    Responsabilidad: Convertir CSV → List[Pregunta]
    """
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._df: Optional[pd.DataFrame] = None
    
    def load(self) -> None:
        """Carga el archivo CSV"""
        try:
            self._df = pd.read_csv(
                self.file_path,
                sep=';',
                encoding='latin-1',  # Cambio a latin-1 para caracteres especiales
                dtype=str
            )
            logger.info(f"Cargadas {len(self._df)} preguntas desde {self.file_path}")
        except Exception as e:
            raise DataParsingError(str(self.file_path), str(e))
    
    def parse(self) -> list[Pregunta]:
        """
        Convierte DataFrame a lista de entidades Pregunta
        Factory Method Pattern
        """
        if self._df is None:
            self.load()
        
        preguntas: list[Pregunta] = []
        
        for _, row in self._df.iterrows():
            try:
                pregunta = self._crear_pregunta(row)
                preguntas.append(pregunta)
            except Exception as e:
                logger.warning(f"Error parseando pregunta {row.get('IDPREGUNTA', 'UNKNOWN')}: {e}")
                continue
        
        logger.info(f"Parseadas {len(preguntas)} preguntas exitosamente")
        return preguntas
    
    def _crear_pregunta(self, row: pd.Series) -> Pregunta:
        """Factory method para crear una Pregunta desde una fila"""
        codigo = str(row['IDPREGUNTA']).strip()
        categoria_str = str(row['CATEGORIA']).strip()
        texto = str(row['PREGUNTA']).strip()
        
        # Mapear categoría usando el factory method del enum
        try:
            categoria = Categoria.from_string(categoria_str)
        except ValueError:
            # Si no se encuentra, asignar a COMENTARIOS como fallback
            logger.warning(f"Categoría no reconocida '{categoria_str}' para pregunta {codigo}")
            categoria = Categoria.COMENTARIOS
        
        return Pregunta(
            codigo=codigo,
            categoria=categoria,
            texto=texto
        )


class EvaluacionCSVParser:
    """
    Parser para el archivo Evaluacion.csv
    Responsabilidad: Convertir CSV → List[Evaluacion]
    Requiere catálogo de preguntas para mapear columnas
    """
    
    def __init__(self, file_path: Path, preguntas: list[Pregunta]):
        self.file_path = file_path
        self.preguntas = preguntas
        # Crear índice de preguntas por código para búsqueda rápida
        self._preguntas_dict = {p.codigo: p for p in preguntas}
        self._df: Optional[pd.DataFrame] = None
    
    def load(self) -> None:
        """Carga el archivo CSV"""
        try:
            self._df = pd.read_csv(
                self.file_path,
                sep=';',
                encoding='latin-1'  # Cambio a latin-1 para caracteres especiales
            )
            logger.info(f"Cargadas {len(self._df)} evaluaciones desde {self.file_path}")
        except Exception as e:
            raise DataParsingError(str(self.file_path), str(e))
    
    def parse(self) -> list[Evaluacion]:
        """Convierte DataFrame a lista de entidades Evaluacion"""
        if self._df is None:
            self.load()
        
        evaluaciones: list[Evaluacion] = []
        
        for _, row in self._df.iterrows():
            try:
                evaluacion = self._crear_evaluacion(row)
                evaluaciones.append(evaluacion)
            except Exception as e:
                logger.warning(f"Error parseando evaluación ID {row.get('PEGE_ID', 'UNKNOWN')}: {e}")
                continue
        
        logger.info(f"Parseadas {len(evaluaciones)} evaluaciones exitosamente")
        return evaluaciones
    
    def _crear_evaluacion(self, row: pd.Series) -> Evaluacion:
        """Factory method para crear una Evaluacion desde una fila"""
        # Datos básicos
        evaluacion_id = str(row['PEGE_ID'])
        documento = str(row['DOCUMENTO']).strip()
        nombre = str(row['NOMBRECOMPLETO']).strip()
        periodo = Periodo(str(row['PERIODO']).strip())
        tipo_formulario = str(row['FORMULARIO']).strip()
        
        # Crear evaluación
        evaluacion = Evaluacion(
            id=evaluacion_id,
            profesor_documento=documento,
            profesor_nombre=nombre,
            periodo=periodo,
            tipo_formulario=tipo_formulario
        )
        
        # Procesar respuestas (columnas P147, P148, etc.)
        for codigo_pregunta, pregunta in self._preguntas_dict.items():
            if codigo_pregunta in row.index:
                calificacion = self._parse_calificacion(row[codigo_pregunta])
                evaluacion.agregar_respuesta(pregunta, calificacion)
        
        return evaluacion
    
    def _parse_calificacion(self, valor: any) -> Optional[Calificacion]:
        """
        Convierte valor del CSV a Calificacion
        Maneja valores vacíos/None
        """
        if pd.isna(valor) or valor == '' or valor is None:
            return None
        
        try:
            valor_float = float(valor)
            return Calificacion(valor_float)
        except (ValueError, TypeError):
            return None


class EvaluacionDataLoader:
    """
    Facade que coordina la carga completa de datos
    Aplicando Facade Pattern para simplificar la interfaz
    Soporta carga de múltiples archivos de evaluaciones
    """
    
    def __init__(self, data_dir: Path, preguntas_path: Path):
        self.data_dir = data_dir
        self.preguntas_path = preguntas_path
    
    def _find_evaluacion_files(self) -> list[Path]:
        """
        Busca todos los archivos CSV de evaluaciones en el directorio
        Patrones soportados: Evaluacion*.csv, evaluacion*.csv
        """
        evaluacion_files = []
        
        # Buscar archivos que empiecen con "Evaluacion" o "evaluacion"
        for pattern in ['Evaluacion*.csv', 'evaluacion*.csv']:
            evaluacion_files.extend(self.data_dir.glob(pattern))
        
        # Ordenar por nombre para carga consistente
        evaluacion_files.sort()
        
        if not evaluacion_files:
            logger.warning(f"No se encontraron archivos de evaluación en {self.data_dir}")
        else:
            logger.info(f"Encontrados {len(evaluacion_files)} archivos de evaluación: {[f.name for f in evaluacion_files]}")
        
        return evaluacion_files
    
    def load_all(self) -> tuple[list[Evaluacion], list[Pregunta]]:
        """
        Carga todos los datos en el orden correcto
        Carga múltiples archivos de evaluaciones si existen
        Retorna: (evaluaciones, preguntas)
        """
        logger.info("Iniciando carga de datos...")
        
        # 1. Cargar preguntas primero (necesarias para las evaluaciones)
        pregunta_parser = PreguntaCSVParser(self.preguntas_path)
        preguntas = pregunta_parser.parse()
        
        # 2. Buscar todos los archivos de evaluaciones
        evaluacion_files = self._find_evaluacion_files()
        
        if not evaluacion_files:
            raise DataParsingError(
                str(self.data_dir),
                "No se encontraron archivos de evaluación (Evaluacion*.csv)"
            )
        
        # 3. Cargar y combinar todas las evaluaciones
        todas_evaluaciones: list[Evaluacion] = []
        
        for eval_file in evaluacion_files:
            logger.info(f"Cargando evaluaciones desde {eval_file.name}...")
            evaluacion_parser = EvaluacionCSVParser(eval_file, preguntas)
            evaluaciones = evaluacion_parser.parse()
            todas_evaluaciones.extend(evaluaciones)
            logger.info(f"  → {len(evaluaciones)} evaluaciones cargadas desde {eval_file.name}")
        
        logger.info(f"Carga completa: {len(todas_evaluaciones)} evaluaciones totales, {len(preguntas)} preguntas")
        logger.info(f"Archivos procesados: {len(evaluacion_files)}")
        
        return todas_evaluaciones, preguntas
