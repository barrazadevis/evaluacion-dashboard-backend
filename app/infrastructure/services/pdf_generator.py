"""
PDF Generator Service
Genera PDFs con diseño profesional usando ReportLab
Compatible con Windows sin dependencias externas
"""
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from app.application.dtos.profesor_dtos import PromedioProfesorResponse
from app.application.dtos.mejora_dtos import PropuestaMejoraResponse


class PDFGenerator:
    """Genera PDFs con diseño profesional manteniendo el estilo del frontend"""
    
    # Colores institucionales
    PRIMARY_COLOR = colors.Color(0/255, 69/255, 137/255)  # rgb(0,69,137)
    SECONDARY_COLOR = colors.Color(255/255, 237/255, 0/255)  # #ffed00
    
    @staticmethod
    def generate_profesor_report(
        promedios: PromedioProfesorResponse,
        mejoras: PropuestaMejoraResponse
    ) -> BytesIO:
        """
        Genera un reporte completo en PDF de un profesor
        
        Args:
            promedios: Datos de promedios del profesor
            mejoras: Propuestas de mejora
            
        Returns:
            BytesIO con el contenido del PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para el título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=PDFGenerator.PRIMARY_COLOR,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.grey,
            spaceAfter=6,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=PDFGenerator.PRIMARY_COLOR,
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Construir contenido
        story = []
        
        # Header
        story.append(Paragraph("Reporte de Evaluación Docente", title_style))
        story.append(Paragraph("Análisis de resultados de evaluaciones por profesor", subtitle_style))
        story.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Información del Profesor
        story.append(Paragraph("Información del Docente", heading_style))
        info_data = [
            ["Nombre:", promedios.nombre_completo],
            ["Documento:", promedios.documento],
            ["Período:", promedios.periodo or "Todos los períodos"],
            ["Total Evaluaciones:", str(promedios.total_evaluaciones)]
        ]
        info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.Color(0.95, 0.95, 0.95)),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.8, 0.8))
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Estadísticas Generales
        story.append(Paragraph("Estadísticas Generales", heading_style))
        
        # Determinar estado
        if promedios.promedio_general >= 4.5:
            estado = "Excelente"
            color_estado = colors.Color(0.9, 0.9, 0.9)  # Gris claro
        elif promedios.promedio_general >= 4.0:
            estado = "Muy Bueno"
            color_estado = colors.Color(0.9, 0.9, 0.9)  # Gris claro
        elif promedios.promedio_general >= 3.5:
            estado = "Bueno"
            color_estado = colors.Color(0.9, 0.9, 0.9)  # Gris claro
        else:
            estado = "Necesita Mejorar"
            color_estado = colors.Color(0.9, 0.9, 0.9)  # Gris claro
        
        stats_data = [
            ["Promedio General", f"{promedios.promedio_general:.2f}", estado]
        ]
        stats_table = Table(stats_data, colWidths=[2.5*inch, 2*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), PDFGenerator.PRIMARY_COLOR),
            ('BACKGROUND', (1, 0), (1, 0), color_estado),
            ('BACKGROUND', (2, 0), (2, 0), color_estado),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.black),
            ('TEXTCOLOR', (2, 0), (2, 0), colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 18),
            ('RIGHTPADDING', (0, 0), (-1, -1), 18),
            ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.8, 0.8))
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Tabla de Categorías
        story.append(Paragraph("Resultados por Categoría", heading_style))
        
        # Estilo para texto de categorías
        cat_text_style = ParagraphStyle(
            'CatText',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica'
        )
        
        cat_data = [["Categoría", "Promedio", "Evaluaciones"]]
        for cat in promedios.promedios_por_categoria:
            # Usar Paragraph para que el texto se ajuste automáticamente
            cat_nombre = Paragraph(cat.categoria, cat_text_style)
            cat_data.append([cat_nombre, f"{cat.promedio:.2f}", str(cat.total_evaluaciones)])
        
        cat_table = Table(cat_data, colWidths=[4*inch, 1.25*inch, 1.25*inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PDFGenerator.PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.8, 0.8)),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
            ('WORDWRAP', (0, 0), (-1, -1), True)
        ]))
        story.append(cat_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Tabla de Evaluadores
        story.append(Paragraph("Resultados por Tipo de Evaluador", heading_style))
        
        actor_data = [["Tipo de Evaluador", "Promedio", "Evaluaciones"]]
        for actor in promedios.promedios_por_actor:
            # Usar Paragraph para que el texto se ajuste automáticamente
            actor_nombre = Paragraph(actor.actor, cat_text_style)
            actor_data.append([actor_nombre, f"{actor.promedio:.2f}", str(actor.total_evaluaciones)])
        
        actor_table = Table(actor_data, colWidths=[4*inch, 1.25*inch, 1.25*inch])
        actor_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), PDFGenerator.PRIMARY_COLOR),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.Color(0.8, 0.8, 0.8)),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
            ('WORDWRAP', (0, 0), (-1, -1), True)
        ]))
        story.append(actor_table)
        story.append(PageBreak())
        
        # Propuestas de Mejora
        story.append(Paragraph("Propuestas de Mejora", heading_style))
        
        if not mejoras.categorias_a_mejorar:
            success_style = ParagraphStyle(
                'Success',
                parent=styles['Normal'],
                fontSize=14,
                textColor=colors.green,
                alignment=TA_CENTER,
                spaceAfter=12,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph("✓ ¡Excelente desempeño!", success_style))
            story.append(Paragraph("Todas las categorías tienen calificaciones superiores a 4.0", subtitle_style))
        else:
            for cat_mejora in mejoras.categorias_a_mejorar:
                # Categoría con promedio
                cat_title = ParagraphStyle(
                    'CategoryTitle',
                    parent=styles['Normal'],
                    fontSize=13,
                    textColor=colors.Color(0.6, 0.3, 0),
                    spaceAfter=8,
                    fontName='Helvetica-Bold'
                )
                story.append(Paragraph(
                    f"{cat_mejora.categoria} - Promedio: {cat_mejora.promedio_categoria:.2f}",
                    cat_title
                ))
                
                # Recomendaciones
                for rec in cat_mejora.recomendaciones:
                    # Estilo para texto de recomendaciones
                    rec_text_style = ParagraphStyle(
                        'RecText',
                        parent=styles['Normal'],
                        fontSize=9,
                        leading=11
                    )
                    
                    rec_title_style = ParagraphStyle(
                        'RecTitle',
                        parent=styles['Normal'],
                        fontSize=9,
                        textColor=PDFGenerator.PRIMARY_COLOR,
                        fontName='Helvetica-Bold',
                        leading=11
                    )
                    
                    # Usar Paragraph para que el texto se ajuste
                    pregunta_text = Paragraph(f"<b>{rec.codigo_pregunta}:</b> {rec.texto_pregunta}", rec_text_style)
                    recomendacion_text = Paragraph(f"<b>💡 Recomendación:</b> {rec.recomendacion}", rec_title_style)
                    
                    rec_data = [
                        [f"Calificación: {rec.calificacion_promedio:.1f}"],
                        [pregunta_text],
                        [recomendacion_text]
                    ]
                    rec_table = Table(rec_data, colWidths=[6.5*inch])
                    rec_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, 0), colors.Color(0.85, 0.85, 0.95)),
                        ('BACKGROUND', (0, 2), (0, 2), colors.Color(0.93, 0.96, 1)),
                        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (0, 0), 10),
                        ('TOPPADDING', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                        ('LEFTPADDING', (0, 0), (-1, -1), 15),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                        ('BOX', (0, 0), (-1, -1), 1, colors.Color(0.7, 0.7, 0.7)),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP')
                    ]))
                    story.append(rec_table)
                    story.append(Spacer(1, 0.15*inch))
                
                story.append(Spacer(1, 0.2*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph("Dashboard de Evaluaciones Docentes - Universidad", footer_style))
        story.append(Paragraph("Este reporte es confidencial y de uso exclusivo institucional", footer_style))
        
        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
