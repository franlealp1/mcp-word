#!/usr/bin/env python3
"""
Test script for the ultra-efficient batch document tools
"""

import json
import sys
import os
import asyncio

# Add the word_document_server to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'word_document_server'))

from word_document_server.tools.batch_document_tools import (
    create_complete_document_with_sections,
    create_complete_document_with_download_link_and_sections,
    add_multiple_sections_batch,
    create_technical_report_template
)

async def test_technical_report():
    """Test the technical report template - this replaces 20+ individual calls"""
    print("🧪 Testing create_technical_report_template...")

    report_data = {
        "title": "INFORME TÉCNICO - PRESA ROSARITO",
        "subtitle": "Evaluación Técnica Integral",
        "metadata": {
            "author": "Equipo de Ingeniería",
            "subject": "Evaluación Técnica"
        },
        "introduction": {
            "content": "La Presa Rosarito es una infraestructura crítica que requiere evaluación técnica continua.",
            "key_data": {"presa": "Rosarito", "location": "España"}
        },
        "methodology": {
            "content": "Se utilizaron métodos de análisis estructural y evaluación hidráulica.",
            "techniques": ["Análisis estructural", "Evaluación hidráulica"]
        },
        "results": {
            "content": "Los resultados muestran condiciones operativas normales con algunas recomendaciones menores.",
            "summary": "Condiciones normales con recomendaciones"
        },
        "conclusions": {
            "content": "Se concluye que la presa mantiene condiciones operativas seguras.",
            "recommendations": ["Monitoreo continuo", "Mantenimiento preventivo"]
        }
    }

    result = await create_technical_report_template(
        filename="test_technical_report.docx",
        report_data=report_data,
        cleanup_hours=1
    )

    print(f"✅ Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result.get('success', False)

async def test_multi_section_document():
    """Test the multi-section document creator"""
    print("\n🧪 Testing create_complete_document_with_download_link_and_sections...")

    sections = [
        {
            "heading": "Introducción",
            "level": 1,
            "content": "Esta es la introducción del documento de prueba.",
            "style": "Normal"
        },
        {
            "heading": "Metodología",
            "level": 1,
            "content": "Descripción de la metodología utilizada en el estudio.",
            "style": "Normal"
        },
        {
            "heading": "Resultados Preliminares",
            "level": 2,
            "content": "Los resultados iniciales muestran tendencias positivas.",
            "style": "Normal"
        },
        {
            "heading": "Conclusiones",
            "level": 1,
            "content": "Las conclusiones finales del análisis realizado.",
            "style": "Normal"
        }
    ]

    result = await create_complete_document_with_download_link_and_sections(
        filename="test_multi_section.docx",
        title="Documento Multi-Sección de Prueba",
        sections=sections,
        metadata={"author": "Claude Code Test"},
        cleanup_hours=1
    )

    print(f"✅ Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result.get('success', False)

async def test_batch_sections():
    """Test adding multiple sections to existing document"""
    print("\n🧪 Testing add_multiple_sections_batch...")

    # First create a simple document using the create_complete_document_with_sections
    base_result = await create_complete_document_with_sections(
        filename="test_base.docx",
        title="Documento Base",
        sections=[{
            "heading": "Introducción",
            "level": 1,
            "content": "Este es el contenido inicial del documento.",
            "style": "Normal"
        }],
        cleanup_hours=1
    )

    if not base_result.get('success'):
        print(f"❌ Failed to create base document: {base_result}")
        return False

    # Now add multiple sections
    sections = [
        {
            "heading": "Sección Agregada 1",
            "level": 1,
            "content": "Contenido de la primera sección agregada.",
            "style": "Normal"
        },
        {
            "heading": "Subsección A",
            "level": 2,
            "content": "Contenido de una subsección.",
            "style": "Normal"
        },
        {
            "heading": "Sección Agregada 2",
            "level": 1,
            "content": "Contenido de la segunda sección agregada.",
            "style": "Normal"
        }
    ]

    result = await add_multiple_sections_batch(
        filename="test_base.docx",
        sections=sections
    )

    print(f"✅ Result: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result.get('success', False)

async def main():
    """Run all batch tool tests"""
    print("🚀 Testing Ultra-Efficient Batch Document Tools")
    print("=" * 50)

    tests = [
        ("Technical Report Template", test_technical_report),
        ("Multi-Section Document", test_multi_section_document),
        ("Batch Section Addition", test_batch_sections)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
            print(f"{'✅' if success else '❌'} {test_name}: {'PASSED' if success else 'FAILED'}")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status:<12} {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All batch tools are working correctly!")
        print("💡 These tools reduce 20+ API calls to just 1-3 calls")
        return True
    else:
        print("⚠️  Some tests failed - check implementation")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)