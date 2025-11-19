"""
Routes para Profesores
Endpoints relacionados con consultas de profesores
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import Optional
import io
import zipfile
from datetime import datetime

from app.api.dependencies import (
    get_calcular_promedio_profesor_use_case,
    get_evaluacion_repository,
    get_detalle_evaluacion_use_case,
    get_propuesta_mejora_use_case,
)
from app.api.models.schemas import PromedioProfesorResponse, ProfesorListItem
from app.api.models.detalle_schemas import DetalleEvaluacionResponse
from app.api.models.mejora_schemas import PropuestaMejoraResponse
from app.application.dtos.profesor_dtos import PromedioProfesorRequest
from app.application.dtos.detalle_dtos import DetalleEvaluacionRequest
from app.application.dtos.mejora_dtos import PropuestaMejoraRequest
from app.core.exceptions import ProfesorNotFoundError
from app.infrastructure.services.pdf_generator import PDFGenerator


router = APIRouter(prefix="/profesores", tags=["profesores"])


@router.get("/", response_model=list[ProfesorListItem])
async def listar_profesores(
    repo = Depends(get_evaluacion_repository),
) -> list[ProfesorListItem]:
    """
    Lista todos los profesores evaluados
    
    Returns:
        Lista de profesores con su información básica
    """
    profesores = repo.get_profesores()
    
    return [
        ProfesorListItem(
            documento=p.documento,
            nombre_completo=p.nombre_completo,
            total_evaluaciones=p.total_evaluaciones(),
        )
        for p in profesores
    ]


@router.get("/{documento}/promedios", response_model=PromedioProfesorResponse)
async def obtener_promedios_profesor(
    documento: str,
    periodo: Optional[str] = Query(
        None, 
        description="Período específico (ej: 2025-2). Si no se especifica, usa todos."
    ),
    use_case = Depends(get_calcular_promedio_profesor_use_case),
) -> PromedioProfesorResponse:
    """
    Obtiene los promedios de un profesor
    
    Args:
        documento: Documento del profesor
        periodo: Período opcional para filtrar
        
    Returns:
        Promedios generales, por categoría y por actor
        
    Raises:
        404: Si el profesor no se encuentra o no tiene evaluaciones
    """
    try:
        request = PromedioProfesorRequest(
            documento=documento,
            periodo=periodo,
        )
        
        result = use_case.execute(request)
        
        # Convertir DTO a Schema (Pydantic)
        return PromedioProfesorResponse(
            documento=result.documento,
            nombre_completo=result.nombre_completo,
            periodo=result.periodo,
            promedio_general=result.promedio_general,
            total_evaluaciones=result.total_evaluaciones,
            promedios_por_categoria=[
                {
                    "categoria": cat.categoria,
                    "categoria_corta": cat.categoria_corta,
                    "promedio": cat.promedio,
                    "total_evaluaciones": cat.total_evaluaciones,
                }
                for cat in result.promedios_por_categoria
            ],
            promedios_por_actor=[
                {
                    "actor": act.actor,
                    "promedio": act.promedio,
                    "total_evaluaciones": act.total_evaluaciones,
                }
                for act in result.promedios_por_actor
            ],
        )
        
    except ProfesorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{documento}/detalle", response_model=DetalleEvaluacionResponse)
async def obtener_detalle_evaluaciones(
    documento: str,
    periodo: Optional[str] = Query(
        None, 
        description="Período específico (ej: 2025-2). Si no se especifica, usa todos."
    ),
    use_case = Depends(get_detalle_evaluacion_use_case),
) -> DetalleEvaluacionResponse:
    """
    Obtiene el detalle de todas las respuestas por pregunta de un profesor
    
    Args:
        documento: Documento del profesor
        periodo: Período opcional para filtrar
        
    Returns:
        Detalle de todas las respuestas agrupadas por pregunta
        
    Raises:
        404: Si el profesor no se encuentra o no tiene evaluaciones
    """
    try:
        request = DetalleEvaluacionRequest(
            documento=documento,
            periodo=periodo,
        )
        
        result = use_case.execute(request)
        
        # Convertir DTO a Schema (Pydantic)
        from app.api.models.detalle_schemas import RespuestaPreguntaSchema
        
        return DetalleEvaluacionResponse(
            documento=result.documento,
            nombre_completo=result.nombre_completo,
            periodo=result.periodo,
            total_evaluaciones=result.total_evaluaciones,
            respuestas=[
                RespuestaPreguntaSchema(
                    codigo_pregunta=resp.codigo_pregunta,
                    texto_pregunta=resp.texto_pregunta,
                    categoria=resp.categoria,
                    calificacion=resp.calificacion,
                    tipo_formulario=resp.tipo_formulario,
                )
                for resp in result.respuestas
            ],
        )
        
    except ProfesorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{documento}/mejoras", response_model=PropuestaMejoraResponse)
async def obtener_propuesta_mejora(
    documento: str,
    periodo: Optional[str] = Query(
        None, 
        description="Período específico (ej: 2025-2). Si no se especifica, usa todos."
    ),
    use_case = Depends(get_propuesta_mejora_use_case),
) -> PropuestaMejoraResponse:
    """
    Obtiene propuestas de mejora para categorías con promedio < 4
    
    Args:
        documento: Documento del profesor
        periodo: Período opcional para filtrar
        
    Returns:
        Propuestas de mejora con recomendaciones específicas
        
    Raises:
        404: Si el profesor no se encuentra o no tiene evaluaciones
    """
    try:
        request = PropuestaMejoraRequest(
            documento=documento,
            periodo=periodo,
        )
        
        result = use_case.execute(request)
        
        # Convertir DTO a Schema (Pydantic)
        from app.api.models.mejora_schemas import (
            RecomendacionMejoraSchema,
            MejoraPorCategoriaSchema,
        )
        
        return PropuestaMejoraResponse(
            documento=result.documento,
            nombre_completo=result.nombre_completo,
            periodo=result.periodo,
            categorias_a_mejorar=[
                MejoraPorCategoriaSchema(
                    categoria=cat.categoria,
                    promedio_categoria=cat.promedio_categoria,
                    recomendaciones=[
                        RecomendacionMejoraSchema(
                            codigo_pregunta=rec.codigo_pregunta,
                            texto_pregunta=rec.texto_pregunta,
                            calificacion_promedio=rec.calificacion_promedio,
                            recomendacion=rec.recomendacion,
                        )
                        for rec in cat.recomendaciones
                    ],
                )
                for cat in result.categorias_a_mejorar
            ],
        )
        
    except ProfesorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{documento}/export-pdf")
async def exportar_pdf(
    documento: str,
    periodo: Optional[str] = Query(
        None, 
        description="Período específico (ej: 2025-2). Si no se especifica, usa todos."
    ),
    promedio_use_case = Depends(get_calcular_promedio_profesor_use_case),
    mejora_use_case = Depends(get_propuesta_mejora_use_case),
) -> StreamingResponse:
    """
    Exporta el reporte completo del profesor a PDF
    
    Args:
        documento: Documento del profesor
        periodo: Período opcional para filtrar
        
    Returns:
        PDF con el reporte completo
        
    Raises:
        404: Si el profesor no se encuentra
    """
    try:
        # Obtener datos del profesor
        promedio_request = PromedioProfesorRequest(
            documento=documento,
            periodo=periodo,
        )
        promedios = promedio_use_case.execute(promedio_request)
        
        # Obtener propuestas de mejora
        mejora_request = PropuestaMejoraRequest(
            documento=documento,
            periodo=periodo,
        )
        mejoras = mejora_use_case.execute(mejora_request)
        
        # Generar PDF
        pdf_file = PDFGenerator.generate_profesor_report(promedios, mejoras)
        
        # Nombre del archivo
        filename = f"reporte_{documento}_{periodo or 'todos'}.pdf".replace(" ", "_")
        
        return StreamingResponse(
            pdf_file,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except ProfesorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {str(e)}")


@router.get("/export-all-pdfs")
async def exportar_todos_pdfs(
    periodo: Optional[str] = Query(
        None, 
        description="Período específico (ej: 2025-2). Si no se especifica, usa todos."
    ),
    repo = Depends(get_evaluacion_repository),
    promedio_use_case = Depends(get_calcular_promedio_profesor_use_case),
    mejora_use_case = Depends(get_propuesta_mejora_use_case),
) -> StreamingResponse:
    """
    Exporta reportes PDF de todos los profesores en un archivo ZIP
    
    Args:
        periodo: Período opcional para filtrar
        
    Returns:
        ZIP con PDFs de todos los profesores
    """
    try:
        # Obtener lista de profesores
        profesores = repo.get_profesores()
        
        if not profesores:
            raise HTTPException(status_code=404, detail="No hay profesores para exportar")
        
        # Crear archivo ZIP en memoria
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for profesor in profesores:
                try:
                    # Obtener datos del profesor
                    promedio_request = PromedioProfesorRequest(
                        documento=profesor.documento,
                        periodo=periodo,
                    )
                    promedios = promedio_use_case.execute(promedio_request)
                    
                    # Obtener propuestas de mejora
                    mejora_request = PropuestaMejoraRequest(
                        documento=profesor.documento,
                        periodo=periodo,
                    )
                    mejoras = mejora_use_case.execute(mejora_request)
                    
                    # Generar PDF
                    pdf_file = PDFGenerator.generate_profesor_report(promedios, mejoras)
                    pdf_content = pdf_file.getvalue()
                    
                    # Nombre del archivo dentro del ZIP
                    filename = f"{profesor.documento}_{profesor.nombre_completo.replace(' ', '_')}.pdf"
                    
                    # Agregar al ZIP
                    zip_file.writestr(filename, pdf_content)
                    
                except Exception as e:
                    # Log error pero continuar con otros profesores
                    print(f"Error generando PDF para {profesor.documento}: {str(e)}")
                    continue
        
        # Preparar respuesta
        zip_buffer.seek(0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reportes_profesores_{periodo or 'todos'}_{timestamp}.zip"
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDFs: {str(e)}")
