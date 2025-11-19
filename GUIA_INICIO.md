# Guía de Inicio Rápido - Backend

## 🚀 Instalación y Ejecución

### 1. Instalar Dependencias

```powershell
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Verificar Datos

Asegúrate de que los archivos CSV estén en `backend/data/`:
- `Evaluacion.csv`
- `preguntas.csv`

### 3. Ejecutar el Servidor

```powershell
# Desde el directorio backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en:
- **API**: http://localhost:8000
- **Documentación Interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación Alternativa (ReDoc)**: http://localhost:8000/redoc

---

## 📡 Endpoints Disponibles

### Información General

#### `GET /`
Información básica de la API

#### `GET /health`
Health check para monitoreo

### Profesores

#### `GET /api/v1/profesores/`
Lista todos los profesores evaluados

**Response Example:**
```json
[
  {
    "documento": "1140844852",
    "nombre_completo": "JAIME ENRIQUE MONCADA DIAZ",
    "total_evaluaciones": 2
  }
]
```

#### `GET /api/v1/profesores/{documento}/promedios`
Obtiene promedios de un profesor específico

**Parámetros:**
- `documento` (path): Documento del profesor
- `periodo` (query, opcional): Período específico (ej: "2025-2")

**Example Request:**
```
GET /api/v1/profesores/1140844852/promedios?periodo=2025-2
```

**Response Example:**
```json
{
  "documento": "1140844852",
  "nombre_completo": "JAIME ENRIQUE MONCADA DIAZ",
  "periodo": "2025-2",
  "promedio_general": 4.64,
  "total_evaluaciones": 2,
  "promedios_por_categoria": [
    {
      "categoria": "ENSEÑANZA-APRENDIZAJE",
      "categoria_corta": "Enseñanza-Aprendizaje",
      "promedio": 4.65,
      "total_evaluaciones": 1
    }
  ],
  "promedios_por_actor": [
    {
      "actor": "AUTOEVALUACIÓN V2",
      "promedio": 5.0,
      "total_evaluaciones": 1
    },
    {
      "actor": "ESTUDIANTE V3",
      "promedio": 4.28,
      "total_evaluaciones": 1
    }
  ]
}
```

### Estadísticas

#### `GET /api/v1/estadisticas/periodos`
Lista todos los períodos disponibles

**Response Example:**
```json
[
  {
    "periodo": "2025-2",
    "total_evaluaciones": 2
  }
]
```

#### `GET /api/v1/estadisticas/actores`
Lista todos los tipos de actores evaluadores

**Response Example:**
```json
[
  {
    "actor": "AUTOEVALUACIÓN V2",
    "total_evaluaciones": 1
  },
  {
    "actor": "ESTUDIANTE V3",
    "total_evaluaciones": 1
  }
]
```

---

## 🧪 Ejecutar Tests

```powershell
# Ejecutar todos los tests
pytest

# Con reporte de cobertura
pytest --cov=app --cov-report=html

# Ver reporte de cobertura en navegador
# Abrir: backend/htmlcov/index.html
```

---

## 🔍 Probar con cURL

### Listar profesores
```powershell
curl http://localhost:8000/api/v1/profesores/
```

### Obtener promedios de un profesor
```powershell
curl "http://localhost:8000/api/v1/profesores/1140844852/promedios?periodo=2025-2"
```

### Listar períodos
```powershell
curl http://localhost:8000/api/v1/estadisticas/periodos
```

---

## 🐛 Troubleshooting

### Error: "Module not found"
```powershell
# Asegúrate de estar en el entorno virtual
.\venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "File not found" al cargar datos
```powershell
# Verifica que los archivos CSV estén en backend/data/
ls data/
```

### Puerto 8000 ya en uso
```powershell
# Usar otro puerto
uvicorn app.main:app --reload --port 8001
```

---

## 📊 Arquitectura Implementada

```
✅ Domain Layer       - Entidades, Value Objects, Interfaces
✅ Application Layer  - Use Cases, DTOs
✅ Infrastructure     - Parsers CSV, Repositories Pandas
✅ API Layer          - FastAPI, Routes, Schemas
✅ Tests              - Unit tests con pytest
```

---

## 🎯 Próximos Pasos

1. ✅ **Backend funcionando** - API REST completa
2. ⏭️ **Frontend** - Crear dashboard con React
3. ⏭️ **Más Use Cases** - Estadísticas por categoría, comparación actores
4. ⏭️ **Visualizaciones** - Gráficos con Recharts
5. ⏭️ **Deploy** - Docker, CI/CD (opcional)

---

## 📝 Notas Importantes

- Los datos se cargan **una sola vez** al iniciar el servidor (patrón Singleton)
- Todas las operaciones son **en memoria** (muy rápido para este volumen de datos)
- La API sigue principios **REST** y **Clean Architecture**
- Validación automática con **Pydantic**
- Documentación automática con **OpenAPI/Swagger**
