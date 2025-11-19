# 📊 Dashboard de Evaluaciones Docentes - Backend

API RESTful desarrollada con **FastAPI** y **Clean Architecture** para el análisis de evaluaciones de profesores universitarios.

## 🚀 Características

- ✅ **Clean Architecture** - Separación de responsabilidades en capas (Domain, Application, Infrastructure, API)
- ✅ **Procesamiento Multi-periodo** - Carga automática de múltiples archivos CSV de evaluaciones
- ✅ **Análisis de Promedios** - Cálculo de estadísticas por profesor, categoría y tipo de evaluador
- ✅ **Propuestas de Mejora** - Sistema de recomendaciones basado en categorías con bajo rendimiento
- ✅ **Exportación a PDF** - Generación de reportes profesionales con ReportLab
- ✅ **Exportación Masiva** - Descarga de PDFs de todos los profesores en formato ZIP
- ✅ **In-Memory Repository** - Alto rendimiento con datos en memoria usando Pandas

## 🛠️ Tecnologías

- **Python 3.11+**
- **FastAPI 0.104.1** - Framework web moderno y de alto rendimiento
- **Pandas 2.1.4** - Procesamiento y análisis de datos
- **ReportLab 4.4.5** - Generación de PDFs
- **Pydantic 2.5.0** - Validación de datos
- **Uvicorn** - Servidor ASGI

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── api/                    # Capa de API (Controladores y Rutas)
│   │   ├── dependencies.py     # Inyección de dependencias
│   │   ├── models/             # Schemas Pydantic para request/response
│   │   └── routes/             # Endpoints REST
│   ├── application/            # Capa de Aplicación (Casos de Uso)
│   │   ├── dtos/               # Data Transfer Objects
│   │   └── use_cases/          # Lógica de negocio
│   ├── core/                   # Configuración y excepciones
│   ├── domain/                 # Capa de Dominio (Entidades y Value Objects)
│   │   ├── entities/           # Entidades del negocio
│   │   ├── repositories/       # Interfaces de repositorios
│   │   └── value_objects/      # Objetos de valor inmutables
│   ├── infrastructure/         # Capa de Infraestructura
│   │   ├── parsers/            # Lectores de CSV
│   │   ├── repositories/       # Implementaciones de repositorios
│   │   └── services/           # Servicios externos (PDF Generator)
│   └── main.py                 # Punto de entrada de la aplicación
├── data/                       # Archivos CSV de datos
│   ├── Evaluacion*.csv         # Archivos de evaluaciones (múltiples períodos)
│   └── preguntas.csv           # Catálogo de preguntas
├── requirements.txt            # Dependencias de Python
└── README.md
```

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/evaluacion-dashboard-backend.git
cd evaluacion-dashboard-backend
```

### 2. Crear entorno virtual

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar archivos de datos

Coloca tus archivos CSV en la carpeta `data/`:
- `data/Evaluacion*.csv` - Archivos de evaluaciones (ej: `Evaluacion_2024-1.csv`, `Evaluacion_2024-2.csv`)
- `data/preguntas.csv` - Catálogo de preguntas

**Formato esperado de los CSV:**
- Separador: `;` (punto y coma)
- Encoding: `latin-1`

## 🏃 Ejecución

### Desarrollo (con auto-reload)

```bash
uvicorn app.main:app --reload
```

### Producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: **http://localhost:8000**

## 📚 Documentación de la API

FastAPI genera documentación interactiva automáticamente:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Principales

### Profesores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/profesores/` | Lista todos los profesores evaluados |
| `GET` | `/api/v1/profesores/{documento}/promedios` | Obtiene promedios de un profesor |
| `GET` | `/api/v1/profesores/{documento}/detalle` | Obtiene detalle de evaluaciones |
| `GET` | `/api/v1/profesores/{documento}/mejoras` | Obtiene propuestas de mejora |
| `GET` | `/api/v1/profesores/{documento}/export-pdf` | Exporta reporte individual a PDF |
| `GET` | `/api/v1/profesores/export-all-pdfs` | Exporta reportes de todos los profesores (ZIP) |

### Estadísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/estadisticas/resumen` | Resumen general de evaluaciones |

### Parámetros de consulta

- `periodo` (opcional): Filtra por período específico (ej: `2025-2`)
  - Si no se especifica, se usan todos los períodos

**Ejemplo de uso:**

```bash
# Obtener promedios de un profesor en un período específico
curl http://localhost:8000/api/v1/profesores/123456789/promedios?periodo=2025-2

# Obtener propuestas de mejora (todos los períodos)
curl http://localhost:8000/api/v1/profesores/123456789/mejoras

# Descargar reporte PDF
curl http://localhost:8000/api/v1/profesores/123456789/export-pdf -o reporte.pdf

# Descargar todos los reportes en ZIP
curl http://localhost:8000/api/v1/profesores/export-all-pdfs -o reportes.zip
```

## 🎯 Casos de Uso

### 1. Calcular Promedio de Profesor
Analiza las evaluaciones de un profesor y calcula:
- Promedio general
- Promedios por categoría (Planeación, Conducción, Evaluación, etc.)
- Promedios por tipo de evaluador (Estudiantes, Pares, Autoevaluación)

### 2. Obtener Detalle de Evaluaciones
Lista todas las respuestas individuales por pregunta, útil para análisis detallado.

### 3. Generar Propuestas de Mejora
Identifica categorías con promedio < 4.0 y genera recomendaciones específicas basadas en:
- Preguntas con calificaciones más bajas
- Palabras clave en las preguntas
- Base de conocimiento de mejores prácticas pedagógicas

### 4. Exportar Reportes PDF
Genera documentos profesionales con:
- Información del profesor
- Estadísticas generales
- Tablas de resultados por categoría y evaluador
- Propuestas de mejora detalladas
- Colores institucionales

## 🏗️ Arquitectura

### Clean Architecture

El proyecto sigue los principios de Clean Architecture:

1. **Domain (Núcleo)**
   - Entidades: `Profesor`, `Evaluacion`, `Pregunta`, `Categoria`
   - Value Objects: `Calificacion`, `Periodo`
   - Interfaces de repositorios

2. **Application (Casos de Uso)**
   - Lógica de negocio independiente de frameworks
   - DTOs para transferencia de datos

3. **Infrastructure (Detalles técnicos)**
   - Parsers CSV con Pandas
   - Repositorios en memoria
   - Generador de PDFs

4. **API (Interfaz externa)**
   - Controllers con FastAPI
   - Schemas de validación con Pydantic

### Patrones de Diseño

- ✅ **Repository Pattern** - Abstracción de acceso a datos
- ✅ **Dependency Injection** - Desacoplamiento de dependencias
- ✅ **Factory Pattern** - Creación de entidades desde CSV
- ✅ **Facade Pattern** - Simplificación de carga de datos
- ✅ **DTO Pattern** - Transferencia de datos entre capas

## 🔍 Procesamiento de Datos

### Flujo de carga

1. **Startup**: Al iniciar el servidor, se ejecuta `initialize_repositories()`
2. **Lectura CSV**: 
   - Busca todos los archivos `Evaluacion*.csv` en `data/`
   - Lee `preguntas.csv`
3. **Parsing**: Convierte filas CSV a entidades del dominio usando Pandas
4. **Indexación**: Crea índices en memoria para búsquedas O(1):
   - Por documento de profesor
   - Por período
   - Por tipo de formulario
5. **Memoria**: Todos los datos quedan en RAM para acceso instantáneo

### Ventajas del enfoque In-Memory

- 🚀 **Velocidad**: Sin I/O de disco en cada consulta
- 💾 **Simplicidad**: No requiere base de datos
- 🔄 **Multi-periodo**: Carga automática de múltiples archivos

## 📦 Dependencias Principales

```txt
fastapi==0.104.1          # Framework web
uvicorn[standard]==0.24.0 # Servidor ASGI
pandas==2.1.4             # Análisis de datos
pydantic==2.5.0           # Validación de datos
reportlab==4.4.5          # Generación de PDFs
python-multipart==0.0.6   # Parsing de formularios
```

## 🎨 Colores Institucionales

Los reportes PDF utilizan los colores de la institución:

- **Azul Primario**: `rgb(0, 69, 137)`
- **Amarillo Secundario**: `#FFED00`
- **Blanco**: Para fondos y textos

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es privado y de uso exclusivo de la institución.

## 👨‍💻 Autor

Desarrollado para el análisis de evaluaciones docentes de la IUB.

---

⭐ **¿Te gustó el proyecto? Dale una estrella en GitHub!**
