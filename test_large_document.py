#!/usr/bin/env python3
"""
Test script for generating a large 5-page technical document using batch tools
"""

import json
import sys
import os
import asyncio

# Add the word_document_server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'word_document_server'))

from word_document_server.tools.batch_document_tools import (
    create_technical_report_template
)

async def test_large_technical_document():
    """Generate a comprehensive 5-page technical document"""
    print("🚀 Generating Large Technical Document (5+ pages)")
    print("=" * 60)

    # Comprehensive report data for a 5-page document
    large_report_data = {
        "title": "INFORME TÉCNICO INTEGRAL - EVALUACIÓN ESTRUCTURAL PRESA ROSARITO",
        "subtitle": "Análisis Completo de Patologías, Evaluación Hidráulica y Recomendaciones de Mantenimiento - 2024",
        "metadata": {
            "author": "Departamento de Ingeniería Hidráulica",
            "subject": "Evaluación Estructural Integral",
            "company": "Ministerio de Fomento - División de Infraestructuras Hidráulicas",
            "keywords": "presa, evaluación estructural, hidráulica, patologías hormigón"
        },
        "introduction": {
            "content": """La Presa Rosarito, construida en 1987 sobre el río Tiétar, constituye una infraestructura hidráulica crítica para el abastecimiento de agua potable y la generación hidroeléctrica de la región. Con una altura de coronación de 85 metros y una capacidad de embalse de 120 hm³, esta presa de hormigón en arco representa una de las obras de ingeniería más significativas de la cuenca hidrográfica del Tajo.

Tras 37 años de operación continua, la infraestructura presenta diversos indicadores que requieren una evaluación técnica exhaustiva. Las inspecciones rutinarias han identificado fisuraciones menores en el paramento de aguas arriba, eflorescencias salinas en las galerías de inspección, y variaciones en los registros piezométricos que justifican la realización del presente estudio integral.

El presente informe técnico tiene como objetivo principal realizar una evaluación completa del estado estructural, funcional y de seguridad de la Presa Rosarito, proporcionando un diagnóstico detallado de las patologías identificadas y estableciendo un plan de actuaciones prioritarias para garantizar la continuidad operativa de la infraestructura en condiciones óptimas de seguridad.

La evaluación se ha desarrollado siguiendo los criterios establecidos en la Guía Técnica de Seguridad de Presas y Embalses (Orden ARM/2656/2008), aplicando metodologías de análisis no destructivas y técnicas de monitorización continua que permiten caracterizar el comportamiento estructural sin comprometer la operatividad de la instalación.""",
            "key_data": {
                "presa": "Rosarito",
                "rio": "Tiétar",
                "año_construccion": "1987",
                "altura": "85 metros",
                "capacidad": "120 hm³",
                "tipo": "Hormigón en arco",
                "años_operacion": "37 años"
            }
        },
        "methodology": {
            "content": """La metodología empleada para la evaluación integral de la Presa Rosarito se ha estructurado en cinco fases complementarias que abarcan desde la recopilación documental hasta la caracterización experimental de materiales y sistemas estructurales.

**FASE 1: ANÁLISIS DOCUMENTAL Y HISTÓRICO**
Se ha realizado una revisión exhaustiva de la documentación técnica disponible, incluyendo el proyecto original de construcción, los informes de seguimiento anuales, los registros de mantenimiento y las modificaciones estructurales implementadas durante la vida útil de la infraestructura. Esta fase ha permitido establecer la línea base de comportamiento y identificar los antecedentes relevantes para la evaluación actual.

**FASE 2: INSPECCIÓN VISUAL DETALLADA**
La inspección visual se ha desarrollado mediante técnicas de acceso especializado que han permitido evaluar todas las superficies accesibles de la estructura. Se han empleado drones con cámaras de alta resolución para el análisis del paramento de aguas arriba, equipos de escalada industrial para la inspección de las juntas de contracción, y sistemas de iluminación LED de alta potencia para la evaluación de galerías internas.

**FASE 3: ENSAYOS NO DESTRUCTIVOS**
Los ensayos no destructivos han incluido esclerometría para la evaluación de la resistencia superficial del hormigón, ultrasonidos para la detección de fisuraciones internas y discontinuidades, georradar para la localización de armaduras y análisis termográfico para la identificación de zonas de infiltración o variaciones de densidad.

**FASE 4: MONITORIZACIÓN INSTRUMENTAL**
Se ha implementado un sistema de monitorización continua mediante la instalación de inclinómetros de precisión, piezómetros de cuerda vibrante, extensómetros de base fija y acelerómetros triaxiales. El sistema permite el registro automático de parámetros estructurales y su transmisión en tiempo real para el análisis de tendencias.

**FASE 5: MODELIZACIÓN NUMÉRICA**
La caracterización del comportamiento estructural se ha completado mediante modelos de elementos finitos tridimensionales que incorporan las propiedades reales de los materiales, las condiciones de contorno identificadas y las cargas operativas registradas. Los modelos han sido calibrados mediante los datos experimentales obtenidos en las fases anteriores.""",
            "techniques": [
                "Análisis documental histórico",
                "Inspección visual con drones",
                "Esclerometría y ultrasonidos",
                "Georradar y termografía",
                "Monitorización instrumental continua",
                "Modelización por elementos finitos"
            ]
        },
        "results": {
            "content": """Los resultados obtenidos durante la evaluación integral de la Presa Rosarito revelan un estado general satisfactorio de la infraestructura, si bien se han identificado diversas patologías que requieren actuaciones de mantenimiento preventivo y correctivo en el corto y medio plazo.

**EVALUACIÓN ESTRUCTURAL DEL HORMIGÓN**
Los ensayos esclerométricos realizados en 120 puntos distribuidos por toda la superficie de la presa han proporcionado valores de resistencia superficial comprendidos entre 35 y 42 MPa, con una media de 38.7 MPa que se sitúa dentro del rango esperado para hormigones de 37 años de antigüedad. Los ensayos de ultrasonidos han detectado 12 zonas con velocidades de propagación inferiores a 4.000 m/s, indicativas de microfisuraciones o variaciones locales de densidad.

**ANÁLISIS DE FISURACIONES Y JUNTAS**
La inspección detallada ha identificado un total de 18 fisuraciones en el paramento de aguas arriba, con longitudes comprendidas entre 0.8 y 3.2 metros y aberturas máximas de 0.3 mm. Estas fisuraciones se concentran principalmente en la zona central del arco, presentando orientación preferentemente vertical y asociadas a los procesos de retracción del hormigón. Las juntas de contracción muestran un comportamiento adecuado, con movimientos estacionales de ±2.1 mm coherentes con las variaciones térmicas registradas.

**SISTEMA DE DRENAJE E INFILTRACIONES**
El caudal de infiltración registrado durante el período de evaluación ha oscilado entre 8.5 L/min en época estival y 12.3 L/min en período invernal, valores que se mantienen dentro de los límites admisibles establecidos en el proyecto original (≤ 15 L/min). El análisis químico de las aguas de infiltración revela un pH ligeramente alcalino (8.2-8.6) y ausencia de elementos agresivos que puedan comprometer la durabilidad del hormigón.

**COMPORTAMIENTO ESTRUCTURAL Y DEFORMACIONES**
Los registros de deformación obtenidos mediante los extensómetros instalados muestran desplazamientos máximos de 4.8 mm en la coronación durante los ciclos de llenado y vaciado del embalse, valores inferiores a los límites de proyecto (≤ 8 mm). La frecuencia fundamental de vibración se sitúa en 3.84 Hz, coherente con las características dinámicas esperadas para una estructura de estas dimensiones.

**SISTEMA DE INSTRUMENTACIÓN EXISTENTE**
La evaluación del sistema de auscultación instalado originalmente ha revelado el funcionamiento correcto del 87% de los instrumentos, identificándose 3 piezómetros con lecturas anómalas y 2 medidores de junta con deriva instrumental que requieren recalibración o sustitución.""",
            "summary": "Estado general satisfactorio con patologías menores que requieren mantenimiento preventivo",
            "key_findings": [
                "Resistencia del hormigón: 38.7 MPa (satisfactorio)",
                "18 fisuraciones menores identificadas (máx. 0.3 mm)",
                "Infiltraciones dentro de límites: 8.5-12.3 L/min",
                "Deformaciones normales: máx. 4.8 mm",
                "87% instrumentación operativa"
            ]
        },
        "conclusions": {
            "content": """Tras la evaluación integral realizada sobre la Presa Rosarito, se concluye que la infraestructura presenta un estado de conservación general satisfactorio que garantiza su operación segura en las condiciones actuales de explotación. Los 37 años de servicio continuo han producido un envejecimiento natural de los materiales y sistemas que se sitúa dentro de los parámetros esperados para estructuras de hormigón de esta tipología y antigüedad.

**CAPACIDAD ESTRUCTURAL Y SEGURIDAD**
El análisis estructural confirma que la presa mantiene íntegramente su capacidad resistente, con márgenes de seguridad acordes con los criterios normativos vigentes. Las fisuraciones identificadas corresponden a procesos naturales de retracción del hormigón y no comprometen la estabilidad global de la estructura. Los sistemas de drenaje y aliviadero conservan su funcionalidad original.

**EVALUACIÓN DEL RIESGO**
La evaluación de riesgo realizada siguiendo la metodología de análisis probabilístico establece un nivel de riesgo BAJO para todos los modos de fallo analizados. La probabilidad de fallo estructural se sitúa por debajo de 10⁻⁶ por año, cumpliendo holgadamente los criterios internacionales de seguridad para presas de categoría A.

**PERSPECTIVA DE VIDA ÚTIL**
Considerando el estado actual de la estructura y la evolución previsible de las patologías identificadas, se estima una vida útil remanente de 25-30 años con mantenimiento adecuado. Esta proyección asume la implementación de las actuaciones correctivas propuestas y el mantenimiento de un programa de inspección y monitorización continua.

**CUMPLIMIENTO NORMATIVO**
La infraestructura cumple con todos los requisitos establecidos en la normativa vigente (Reglamento Técnico sobre Seguridad de Presas y Embalses, Real Decreto 9/2008), no existiendo deficiencias que comprometan la autorización de explotación actual.""",
            "recommendations": [
                "Implementar programa de sellado de fisuraciones menores",
                "Renovar instrumentación defectuosa identificada",
                "Desarrollar plan de mantenimiento preventivo quinquenal",
                "Actualizar sistema de monitorización con sensores IoT",
                "Programar inspecciones subacuáticas anuales"
            ]
        },
        "annexes": {
            "content": """**ANEXO I: DOCUMENTACIÓN FOTOGRÁFICA**
Se adjunta reportaje fotográfico completo con 180 imágenes de alta resolución que documentan el estado actual de todos los elementos estructurales evaluados, incluyendo vistas generales, detalles de fisuraciones, estado de juntas y sistemas auxiliares.

**ANEXO II: RESULTADOS DE ENSAYOS**
Fichas técnicas completas de todos los ensayos realizados, incluyendo esclerometría (120 puntos), ultrasonidos (45 perfiles), georradar (8 secciones) y análisis químicos de aguas de infiltración.

**ANEXO III: REGISTROS DE INSTRUMENTACIÓN**
Series históricas completas de todos los parámetros monitorizados durante el período de evaluación, con análisis estadístico de tendencias y correlaciones.

**ANEXO IV: MODELOS DE CÁLCULO**
Memoria completa de los modelos de elementos finitos desarrollados, incluyendo geometría, propiedades de materiales, condiciones de contorno y resultados de análisis estático y dinámico.

**ANEXO V: ESPECIFICACIONES TÉCNICAS**
Especificaciones técnicas detalladas para la ejecución de las actuaciones correctivas propuestas, incluyendo materiales, procedimientos de ejecución y criterios de control de calidad.""",
            "documents": [
                "Reportaje fotográfico (180 imágenes)",
                "Fichas de ensayos y resultados",
                "Series de instrumentación histórica",
                "Modelos de elementos finitos",
                "Especificaciones técnicas de reparación"
            ]
        }
    }

    print("📝 Creating comprehensive technical report...")
    result = await create_technical_report_template(
        filename="informe_tecnico_presa_rosarito_completo.docx",
        report_data=large_report_data,
        cleanup_hours=2
    )

    print(f"\n✅ RESULT:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get('success'):
        print(f"\n🎉 SUCCESS! Large technical document created:")
        print(f"📄 Document: {result.get('original_filename')}")
        print(f"📥 Download: {result.get('download_url')}")
        print(f"📊 Sections: {result.get('report_sections', 'N/A')}")
        print(f"📈 Tables: {result.get('report_tables', 'N/A')}")
        print(f"⏰ Expires: {result.get('expires_at')}")
        print(f"\n💡 This single call replaces 25+ individual MCP tool calls!")
        return True
    else:
        print(f"\n❌ FAILED: {result.get('message', 'Unknown error')}")
        return False

async def main():
    """Test large document generation"""
    print("🚀 Testing Ultra-Efficient Large Document Generation")
    print("=" * 60)

    success = await test_large_technical_document()

    if success:
        print("\n" + "=" * 60)
        print("🎉 LARGE DOCUMENT TEST: SUCCESS!")
        print("✅ Generated comprehensive 5+ page technical report")
        print("⚡ Single MCP call instead of 25+ individual calls")
        print("🔗 Download link ready for immediate access")
    else:
        print("\n" + "=" * 60)
        print("❌ LARGE DOCUMENT TEST: FAILED")

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)