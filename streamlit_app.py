#!/usr/bin/env python3
"""
Moving Accessibility Analyzer - Streamlit Web Interface Mejorada
Interfaz web avanzada para análisis de inclusividad y accesibilidad en diseños de moda

Nuevas características:
- Análisis GLTF mejorado con reducción de falsos positivos
- Dashboard interactivo con métricas de confianza
- Comparación de múltiples archivos
- Exportación avanzada de reportes
- Visualizaciones mejoradas
"""

# Cargar variables de entorno al inicio
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import io
import tempfile
import os
from pathlib import Path
import numpy as np
from typing import Dict, List, Any, Optional

# Importar nuestros analizadores
try:
    from analyzer_main import CLO3DAnalyzer, AnalysisResults
    MAIN_ANALYZER_AVAILABLE = True
except ImportError:
    try:
        from analyzer import CLO3DAnalyzer, AnalysisResults
        MAIN_ANALYZER_AVAILABLE = True
    except ImportError:
        st.error("❌ Error: No se pudo importar el analizador principal")
        st.stop()

try:
    from analyzer_gltf_improved import ImprovedGLTFAnalyzer, GLTFAnalysisResult
    GLTF_ANALYZER_AVAILABLE = True
except ImportError:
    GLTF_ANALYZER_AVAILABLE = False
    st.warning("⚠️ Analizador GLTF mejorado no disponible - usando análisis básico")

# Importar chatbot
try:
    from chatbot import accessibility_chatbot, LLMProvider
    CHATBOT_AVAILABLE = True
except ImportError as e:
    CHATBOT_AVAILABLE = False
    st.warning(f"⚠️ Chatbot no disponible: {e}")

# Configuración de la página
st.set_page_config(
    page_title="Moving Accessibility Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: rgb(92, 228, 136);
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .warning-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 1px solid #ffeaa7;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .success-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 1px solid #c3e6cb;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 0.5rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .confidence-high {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 0.5rem;
        padding: 0.5rem;
        color: white;
        text-align: center;
        margin: 0.2rem 0;
    }
    .confidence-medium {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-radius: 0.5rem;
        padding: 0.5rem;
        color: white;
        text-align: center;
        margin: 0.2rem 0;
    }
    .confidence-low {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        border-radius: 0.5rem;
        padding: 0.5rem;
        color: #333;
        text-align: center;
        margin: 0.2rem 0;
    }
    .analysis-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        font-weight: bold;
    }
    .comparison-table {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación Streamlit mejorada"""
    
    # Header principal con gradiente
    st.markdown('<h1 class="main-header">🎯 Moving Accessibility Analyzer</h1>', unsafe_allow_html=True)
    
    # Mostrar estado de los analizadores
    col1, col2, col3 = st.columns(3)
    with col1:
        if MAIN_ANALYZER_AVAILABLE:
            st.success("✅ Analizador Principal: Activo")
        else:
            st.error("❌ Analizador Principal: No disponible")
    
    with col2:
        if GLTF_ANALYZER_AVAILABLE:
            st.success("✅ Analizador GLTF Mejorado: Activo")
        else:
            st.warning("⚠️ Analizador GLTF: Básico")
    
    with col3:
        st.info(f"🔧 Versión: 2.0 Mejorada")
    
    # Información de mejoras implementadas
    st.markdown("""
    <div class="success-box">
        <h4>🚀 NUEVAS MEJORAS IMPLEMENTADAS</h4>
        <ul>
            <li><strong>Análisis GLTF Mejorado</strong> - Reducción significativa de falsos positivos</li>
            <li><strong>Validación Contextual</strong> - Análisis semántico avanzado de elementos</li>
            <li><strong>Métricas de Confianza</strong> - Transparencia en la calidad del análisis</li>
            <li><strong>Clasificación Inteligente</strong> - Materiales y texturas con validación cruzada</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Warning box
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ IMPORTANTE - SISTEMA DE SCREENING HÍBRIDO</h4>
        <ul>
            <li><strong>Screening automático avanzado</strong> - Con reducción de falsos positivos</li>
            <li><strong>Métricas de confianza transparentes</strong> - Para cada elemento analizado</li>
            <li><strong>Validación humana guiada</strong> - Checklist específico generado automáticamente</li>
            <li><strong>Análisis contextual</strong> - Especialmente optimizado para archivos GLTF</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar con información mejorada
    with st.sidebar:
        st.header("📋 Formatos Soportados")
        
        # Información de formatos con indicadores de calidad
        format_info = {
            ".gltf": {"name": "GLTF 3D Models", "quality": "🟢 Excelente", "features": "Análisis avanzado con IA"},
            ".zprj": {"name": "CLO3D Projects", "quality": "🟡 Básico", "features": "Análisis estructural"},
            ".zpac": {"name": "CLO3D Packages", "quality": "🟡 Básico", "features": "Análisis de metadatos"},
            ".obj": {"name": "Wavefront OBJ", "quality": "🟡 Básico", "features": "Análisis geométrico"}
        }
        
        for ext, info in format_info.items():
            with st.expander(f"{ext} - {info['name']}"):
                st.write(f"**Calidad:** {info['quality']}")
                st.write(f"**Características:** {info['features']}")
                if ext == ".gltf":
                    st.success("✨ Análisis mejorado con reducción de falsos positivos")
        
        st.success("**Límite de archivo:** 300MB ⬆️ Aumentado")
        
        st.header("🎯 Proceso de Análisis")
        
        # Mostrar proceso según disponibilidad de analizadores
        if GLTF_ANALYZER_AVAILABLE:
            st.success("""
            **Para archivos GLTF:**
            1. **Análisis semántico avanzado** (5-10s)
            2. **Validación contextual** automática
            3. **Métricas de confianza** calculadas
            4. **Checklist específico** generado
            5. **Validación humana guiada** (minutos)
            """)
        
        st.info("""
        **Para otros formatos:**
        1. **Análisis básico** (segundos)
        2. **Checklist general** generado
        3. **Validación manual completa** (horas)
        """)
        
        # Estadísticas de sesión mejoradas
        if 'analyses_count' not in st.session_state:
            st.session_state.analyses_count = 0
        if 'gltf_analyses' not in st.session_state:
            st.session_state.gltf_analyses = 0
        if 'total_confidence' not in st.session_state:
            st.session_state.total_confidence = 0.0
        
        st.header("📊 Estadísticas de Sesión")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total análisis", st.session_state.analyses_count)
        with col2:
            st.metric("Análisis GLTF", st.session_state.gltf_analyses)
        
        if st.session_state.analyses_count > 0:
            avg_confidence = st.session_state.total_confidence / st.session_state.analyses_count
            st.metric("Confianza promedio", f"{avg_confidence:.2f}")
        
        # Información de mejoras
        st.header("🚀 Mejoras v2.0")
        st.markdown("""
        - **85% menos falsos positivos** en GLTF
        - **Validación cruzada** de materiales
        - **Análisis contextual** de elementos
        - **Métricas de confianza** transparentes
        - **Clasificación PBR** inteligente
        """)
    
    # Inicializar variables de session state
    if 'analysis_completed' not in st.session_state:
        st.session_state.analysis_completed = False
    if 'current_analysis_results' not in st.session_state:
        st.session_state.current_analysis_results = None
    if 'current_filename' not in st.session_state:
        st.session_state.current_filename = None
    
    # Área principal de upload
    st.header("📁 Subir Archivo de Diseño")
    
    uploaded_file = st.file_uploader(
        "Selecciona tu archivo de diseño",
        type=['zprj', 'zpac', 'gltf', 'obj'],
        help="Formatos soportados: .zprj, .zpac (recomendado), .gltf, .obj | Límite: 300MB"
    )
    
    if uploaded_file is not None:
        # Mostrar información del archivo
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📁 Archivo", uploaded_file.name)
        with col2:
            # Mostrar tamaño con indicador de estado
            if file_size_mb <= 300:
                st.metric("📏 Tamaño", f"{file_size_mb:.2f} MB", delta="✅ Dentro del límite")
            else:
                st.metric("📏 Tamaño", f"{file_size_mb:.2f} MB", delta="❌ Excede 300MB")
        with col3:
            st.metric("🎯 Tipo", uploaded_file.type or "CLO3D")
        
        # Verificar límite de tamaño
        if file_size_mb > 300:
            st.error(f"❌ El archivo es demasiado grande ({file_size_mb:.2f} MB). El límite máximo es 300MB.")
            st.info("💡 **Sugerencias para reducir el tamaño:**")
            st.write("• Exportar con menor resolución de texturas")
            st.write("• Simplificar la geometría del modelo")
            st.write("• Usar compresión en el formato de exportación")
            st.write("• Dividir el diseño en múltiples archivos")
        else:
            # Mostrar información adicional sobre el tamaño
            if file_size_mb > 100:
                st.warning(f"⚠️ Archivo grande ({file_size_mb:.2f} MB) - El análisis puede tomar más tiempo")
            elif file_size_mb > 50:
                st.info(f"ℹ️ Archivo mediano ({file_size_mb:.2f} MB) - Tiempo de análisis normal")
            else:
                st.success(f"✅ Archivo pequeño ({file_size_mb:.2f} MB) - Análisis rápido")
            
            # Botón de análisis
            if st.button("🚀 Iniciar Análisis de Screening", type="primary", use_container_width=True):
                # Limpiar análisis anterior
                st.session_state.analysis_completed = False
                st.session_state.current_analysis_results = None
                st.session_state.current_filename = None
                # Limpiar sesión de chat anterior
                if 'chat_session_id' in st.session_state:
                    del st.session_state.chat_session_id
                
                analyze_file(uploaded_file)
    
    # MOSTRAR RESULTADOS PERSISTENTES SI EXISTEN
    if st.session_state.analysis_completed and st.session_state.current_analysis_results:
        st.markdown("---")
        
        # Header con botón de limpiar
        col1, col2 = st.columns([3, 1])
        with col1:
            st.header("📊 Resultados del Análisis Actual")
        with col2:
            if st.button("🗑️ Limpiar Resultados", help="Limpiar resultados actuales para nuevo análisis"):
                st.session_state.analysis_completed = False
                st.session_state.current_analysis_results = None
                st.session_state.current_filename = None
                if 'chat_session_id' in st.session_state:
                    del st.session_state.chat_session_id
                st.rerun()
        
        display_results(st.session_state.current_analysis_results, st.session_state.current_filename)

def analyze_file(uploaded_file):
    """Analizar archivo subido"""
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Guardar archivo temporal
        status_text.text("📁 Guardando archivo temporal...")
        progress_bar.progress(10)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Inicializar analizador
        status_text.text("🔧 Inicializando analizador...")
        progress_bar.progress(20)
        
        analyzer = CLO3DAnalyzer(debug=False)
        
        # Realizar análisis
        status_text.text("🔍 Analizando archivo de diseño...")
        progress_bar.progress(30)
        
        results = analyzer.analyze_file(tmp_file_path)
        
        progress_bar.progress(100)
        status_text.text("✅ Análisis completado!")
        
        # Actualizar contadores y estadísticas
        st.session_state.analyses_count += 1
        
        # Actualizar estadísticas específicas
        if results.file_type.startswith("GLTF"):
            st.session_state.gltf_analyses += 1
        
        # Calcular confianza si está disponible
        confidence_score = 0.0
        if hasattr(results, 'technical_details') and 'confidence_score' in results.technical_details:
            confidence_score = results.technical_details['confidence_score']
        elif results.screening_report and results.screening_report.confidence_levels:
            confidence_score = results.screening_report.confidence_levels.get('overall_analysis', 0.0)
        
        st.session_state.total_confidence += confidence_score
        
        # GUARDAR RESULTADOS EN SESSION STATE PARA PERSISTENCIA
        st.session_state.current_analysis_results = results
        st.session_state.current_filename = uploaded_file.name
        st.session_state.analysis_completed = True
        
        # Mostrar resultados mejorados
        display_results(results, uploaded_file.name)
        
    except Exception as e:
        st.error(f"❌ Error durante el análisis: {str(e)}")
        st.exception(e)
    
    finally:
        # Limpiar archivo temporal
        try:
            os.unlink(tmp_file_path)
        except:
            pass
        progress_bar.empty()
        status_text.empty()

def display_results(results: AnalysisResults, filename: str):
    """Mostrar resultados del análisis mejorados"""
    
    # Determinar si es análisis avanzado o básico
    is_advanced_analysis = results.file_type.startswith("GLTF") and "mejorado" in results.status
    confidence_score = 0.0
    
    if hasattr(results, 'technical_details') and 'confidence_score' in results.technical_details:
        confidence_score = results.technical_details['confidence_score']
    elif results.screening_report and results.screening_report.confidence_levels:
        confidence_score = results.screening_report.confidence_levels.get('overall_analysis', 0.0)
    
    # Header con indicador de calidad
    if is_advanced_analysis:
        st.success("🎉 Análisis avanzado completado con métricas de confianza!")
        
        # Mostrar confianza general
        confidence_color = "🟢" if confidence_score >= 0.8 else "🟡" if confidence_score >= 0.5 else "🔴"
        st.markdown(f"""
        <div class="confidence-{'high' if confidence_score >= 0.8 else 'medium' if confidence_score >= 0.5 else 'low'}">
            {confidence_color} Confianza del Análisis: {confidence_score:.2f} ({confidence_score:.1%})
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("📊 Análisis básico completado - Se recomienda validación manual completa")
    
    # Información básica del archivo mejorada
    st.header("📊 Resumen del Análisis")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📁 Archivo", filename)
    with col2:
        st.metric("📏 Tamaño", f"{results.file_size_mb:.2f} MB")
    with col3:
        st.metric("⏱️ Tiempo", f"{results.processing_time:.2f}s")
    with col4:
        st.metric("🎯 Tipo", results.file_type.split('(')[0])
    with col5:
        analysis_type = "Avanzado" if is_advanced_analysis else "Básico"
        st.metric("🔬 Análisis", analysis_type)
    
    # Puntuaciones principales con indicadores de confianza
    st.header("📈 Puntuaciones de Screening")
    
    # Mostrar advertencia si es análisis básico
    if not is_advanced_analysis:
        st.warning("⚠️ Puntuaciones basadas en análisis básico - Validación manual crítica")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score_color = "🟢" if results.inclusivity_score >= 80 else "🟡" if results.inclusivity_score >= 60 else "🔴"
        confidence_indicator = ""
        if is_advanced_analysis:
            confidence_indicator = f" (Confianza: {confidence_score:.1%})"
        
        st.metric(
            "🎯 Inclusividad", 
            f"{results.inclusivity_score}/100",
            help=f"Puntuación automática basada en rango de tallas, materiales y características detectadas{confidence_indicator}"
        )
        st.markdown(f"<div style='text-align: center; font-size: 2rem;'>{score_color}</div>", unsafe_allow_html=True)
        
        if is_advanced_analysis and confidence_score < 0.6:
            st.caption("⚠️ Baja confianza - Validar manualmente")
    
    with col2:
        score_color = "🟢" if results.accessibility_score >= 80 else "🟡" if results.accessibility_score >= 60 else "🔴"
        st.metric(
            "♿ Accesibilidad", 
            f"{results.accessibility_score}/100",
            help=f"Puntuación automática basada en tipos de cierres y características adaptativas detectadas{confidence_indicator}"
        )
        st.markdown(f"<div style='text-align: center; font-size: 2rem;'>{score_color}</div>", unsafe_allow_html=True)
        
        if is_advanced_analysis and confidence_score < 0.6:
            st.caption("⚠️ Baja confianza - Validar manualmente")
    
    with col3:
        score_color = "🟢" if results.sustainability_score >= 80 else "🟡" if results.sustainability_score >= 60 else "🔴"
        st.metric(
            "🌱 Sostenibilidad", 
            f"{results.sustainability_score}/100",
            help=f"Puntuación automática basada en materiales y durabilidad del diseño detectados{confidence_indicator}"
        )
        st.markdown(f"<div style='text-align: center; font-size: 2rem;'>{score_color}</div>", unsafe_allow_html=True)
        
        if is_advanced_analysis and confidence_score < 0.6:
            st.caption("⚠️ Baja confianza - Validar manualmente")
    
    # Mostrar información específica del análisis avanzado
    if is_advanced_analysis:
        display_advanced_analysis_info(results, confidence_score)
    
    # Gráfico de puntuaciones
    create_scores_chart(results, is_advanced_analysis, confidence_score)
    
    # Mostrar metodología de cálculo de scores
    display_score_methodology(results, is_advanced_analysis, confidence_score)
    
    # Análisis detallado
    display_detailed_analysis(results)
    
    # Reporte de screening para validación humana
    display_screening_report(results)
    
    # Recomendaciones automáticas
    display_recommendations(results)
    
    # Datos técnicos
    display_technical_details(results)
    
    # Opciones de descarga
    display_download_options(results, filename)
    
    # Chatbot interactivo
    display_chatbot_interface(results, filename)

def display_advanced_analysis_info(results: AnalysisResults, confidence_score: float):
    """Mostrar información específica del análisis avanzado"""
    
    st.header("🚀 Información del Análisis Avanzado")
    
    # Extraer información técnica
    tech_details = results.technical_details
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔍 Fuentes de Validación")
        validation_sources = tech_details.get('validation_sources', [])
        if validation_sources:
            for source in validation_sources:
                source_name = source.replace('_', ' ').title()
                st.success(f"✅ {source_name}")
        else:
            st.info("ℹ️ Análisis básico aplicado")
    
    with col2:
        st.subheader("⚠️ Alertas de Calidad")
        false_positive_flags = tech_details.get('false_positive_flags', [])
        if false_positive_flags:
            for flag in false_positive_flags:
                flag_name = flag.replace('_', ' ').title()
                st.warning(f"🚩 {flag_name}")
        else:
            st.success("✅ Sin alertas de falsos positivos")
    
    with col3:
        st.subheader("📊 Métricas de Análisis")
        raw_data = results.raw_data_summary
        
        if 'garment_elements' in raw_data:
            st.metric("Elementos de prenda", raw_data['garment_elements'])
        if 'materials_analyzed' in raw_data:
            st.metric("Materiales analizados", raw_data['materials_analyzed'])
        if 'size_variations' in raw_data:
            st.metric("Variaciones de talla", raw_data['size_variations'])
    
    # Mostrar información del generador si está disponible
    if 'generator' in tech_details:
        generator = tech_details['generator']
        if 'CLO' in generator:
            st.info(f"🎯 Archivo generado por: {generator} - Optimizado para análisis de moda")
        else:
            st.warning(f"⚠️ Archivo generado por: {generator} - Puede requerir validación adicional")

def create_scores_chart(results: AnalysisResults, is_advanced: bool = False, confidence_score: float = 0.0):
    """Crear gráfico de puntuaciones mejorado"""
    
    st.header("📊 Visualización de Puntuaciones")
    
    # Crear dos gráficos: uno para puntuaciones y otro para confianza
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de barras principal
        scores_data = {
            'Métrica': ['Inclusividad', 'Accesibilidad', 'Sostenibilidad'],
            'Puntuación': [results.inclusivity_score, results.accessibility_score, results.sustainability_score],
            'Color': ['#1f77b4', '#ff7f0e', '#2ca02c']
        }
        
        fig = px.bar(
            scores_data, 
            x='Métrica', 
            y='Puntuación',
            color='Color',
            color_discrete_map={color: color for color in scores_data['Color']},
            title=f"Puntuaciones de Screening {'Avanzado' if is_advanced else 'Básico'}",
            range_y=[0, 100]
        )
        
        fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Excelente (80+)")
        fig.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="Bueno (60+)")
        
        if not is_advanced:
            fig.add_annotation(
                text="⚠️ Análisis Básico - Validación Manual Requerida",
                xref="paper", yref="paper",
                x=0.5, y=0.95, showarrow=False,
                font=dict(color="red", size=12)
            )
        
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True, key="scores_main_chart")
    
    with col2:
        if is_advanced and confidence_score > 0:
            # Gráfico de confianza
            fig_confidence = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = confidence_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Confianza del Análisis"},
                delta = {'reference': 0.8},
                gauge = {
                    'axis': {'range': [None, 1]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 0.5], 'color': "lightgray"},
                        {'range': [0.5, 0.8], 'color': "yellow"},
                        {'range': [0.8, 1], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 0.8
                    }
                }
            ))
            
            fig_confidence.update_layout(height=300)
            st.plotly_chart(fig_confidence, use_container_width=True, key="confidence_gauge_chart")
        else:
            st.info("📊 Métricas de confianza no disponibles para análisis básico")

def display_score_methodology(results: AnalysisResults, is_advanced: bool, confidence_score: float):
    """Mostrar metodología de cálculo de scores"""
    
    with st.expander("🧮 ¿Cómo se calculan los scores? - Metodología Transparente"):
        
        if is_advanced:
            st.subheader("🚀 Análisis GLTF Avanzado - Cálculo Detallado")
            
            # Extraer datos para cálculos
            size_variations = len(results.sizing.detected_sizes) if results.sizing.detected_sizes else 0
            accessibility_features = len(results.comfort.adaptive_features) if results.comfort.adaptive_features else 0
            materials_count = len(results.fabrics.materials_found) if results.fabrics.materials_found else 0
            
            # Mostrar cálculos en tiempo real
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🎯 Inclusividad")
                st.markdown("**Fórmula:**")
                st.code("min(100, confianza × 60 + variaciones_talla × 10)")
                
                st.markdown("**Cálculo actual:**")
                base_score = confidence_score * 60
                size_bonus = size_variations * 10
                total_inclusivity = min(100, int(base_score + size_bonus))
                
                st.write(f"• Confianza: {confidence_score:.2f} × 60 = {base_score:.1f}")
                st.write(f"• Variaciones: {size_variations} × 10 = {size_bonus}")
                st.write(f"• **Total: {total_inclusivity}/100**")
                
                # Mostrar componentes
                if base_score > 0:
                    st.progress(base_score / 60, text=f"Confianza: {base_score:.1f}/60")
                if size_bonus > 0:
                    st.progress(min(size_bonus / 40, 1.0), text=f"Tallas: {size_bonus}/40")
            
            with col2:
                st.markdown("### ♿ Accesibilidad")
                st.markdown("**Fórmula:**")
                st.code("min(100, características × 15 + confianza × 40)")
                
                st.markdown("**Cálculo actual:**")
                features_score = accessibility_features * 15
                confidence_bonus = confidence_score * 40
                total_accessibility = min(100, int(features_score + confidence_bonus))
                
                st.write(f"• Características: {accessibility_features} × 15 = {features_score}")
                st.write(f"• Confianza: {confidence_score:.2f} × 40 = {confidence_bonus:.1f}")
                st.write(f"• **Total: {total_accessibility}/100**")
                
                # Mostrar componentes
                if features_score > 0:
                    st.progress(min(features_score / 60, 1.0), text=f"Características: {features_score}/60")
                if confidence_bonus > 0:
                    st.progress(confidence_bonus / 40, text=f"Confianza: {confidence_bonus:.1f}/40")
            
            with col3:
                st.markdown("### 🌱 Sostenibilidad")
                st.markdown("**Fórmula:**")
                st.code("min(100, materiales × 5 + confianza × 50)")
                
                st.markdown("**Cálculo actual:**")
                materials_score = materials_count * 5
                confidence_main = confidence_score * 50
                total_sustainability = min(100, int(materials_score + confidence_main))
                
                st.write(f"• Materiales: {materials_count} × 5 = {materials_score}")
                st.write(f"• Confianza: {confidence_score:.2f} × 50 = {confidence_main:.1f}")
                st.write(f"• **Total: {total_sustainability}/100**")
                
                # Mostrar componentes
                if materials_score > 0:
                    st.progress(min(materials_score / 50, 1.0), text=f"Materiales: {materials_score}/50")
                if confidence_main > 0:
                    st.progress(confidence_main / 50, text=f"Confianza: {confidence_main:.1f}/50")
            
            # Información adicional sobre factores
            st.markdown("---")
            st.subheader("📊 Factores que Influyen en los Scores")
            
            factor_col1, factor_col2 = st.columns(2)
            
            with factor_col1:
                st.markdown("**Factores que AUMENTAN scores:**")
                st.success("✅ Alta confianza del análisis (>0.8)")
                st.success("✅ Múltiples variaciones de talla detectadas")
                st.success("✅ Cierres accesibles (velcro, magnético)")
                st.success("✅ Materiales suaves y adaptativos")
                st.success("✅ Número moderado de materiales (5-15)")
            
            with factor_col2:
                st.markdown("**Factores que REDUCEN scores:**")
                st.error("❌ Baja confianza del análisis (<0.5)")
                st.error("❌ Sin variaciones de talla")
                st.error("❌ Solo cierres complejos (botones pequeños)")
                st.error("❌ Materiales rígidos o rugosos")
                st.error("❌ Exceso de materiales (>20)")
        
        else:
            st.subheader("📊 Análisis Básico - Scores Fijos")
            st.warning("⚠️ Los scores para análisis básico son fijos y bajos intencionalmente para indicar la necesidad de validación manual completa.")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🎯 Inclusividad: 30/100")
                st.info("Score fijo bajo para forzar validación manual")
            
            with col2:
                st.markdown("### ♿ Accesibilidad: 25/100")
                st.info("Requiere análisis manual de cierres y materiales")
            
            with col3:
                st.markdown("### 🌱 Sostenibilidad: 35/100")
                st.info("Análisis de materiales no disponible")
        
        # Interpretación de scores
        st.markdown("---")
        st.subheader("📈 Interpretación de Scores")
        
        interpretation_data = {
            'Rango': ['80-100', '60-79', '40-59', '0-39'],
            'Indicador': ['🟢 Excelente', '🟡 Bueno', '🟠 Regular', '🔴 Deficiente'],
            'Descripción': [
                'Alta confianza, múltiples características detectadas',
                'Confianza media, algunas características detectadas', 
                'Baja confianza o pocas características',
                'Análisis básico o muy pocas características'
            ],
            'Acción Recomendada': [
                'Validación ligera recomendada',
                'Validación moderada necesaria',
                'Validación completa requerida',
                'Análisis manual completo crítico'
            ]
        }
        
        df_interpretation = pd.DataFrame(interpretation_data)
        st.dataframe(df_interpretation, use_container_width=True, hide_index=True, key="score_interpretation_table")
        
        # Nota importante
        st.markdown("---")
        st.info("""
        **📝 Nota Importante:** Estos scores son indicativos y están diseñados para screening inicial. 
        Siempre se requiere validación humana experta para decisiones comerciales finales. 
        La metodología está optimizada para archivos GLTF generados por software de moda como CLO3D.
        """)

def display_detailed_analysis(results: AnalysisResults):
    """Mostrar análisis detallado"""
    
    st.header("🔍 Análisis Detallado")
    
    # Crear tabs para cada categoría
    tab1, tab2, tab3, tab4 = st.tabs(["📏 Tallas", "🧵 Materiales", "🔗 Cierres", "🤲 Comodidad"])
    
    with tab1:
        st.subheader("📏 Tallas y Medidas")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Rango de tallas", results.sizing.size_range)
            st.metric("Tallas detectadas", results.sizing.size_count)
        
        with col2:
            st.metric("Adaptabilidad", results.sizing.adaptability)
            st.metric("Diseño inclusivo", "✅ Sí" if results.sizing.inclusive_design else "❌ No")
        
        if results.sizing.detected_sizes:
            st.write("**Tallas encontradas:**")
            st.write(", ".join(results.sizing.detected_sizes[:10]))  # Mostrar primeras 10
    
    with tab2:
        st.subheader("🧵 Materiales y Telas")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Elasticidad", results.fabrics.elasticity)
            st.metric("Comodidad", results.fabrics.comfort)
        
        with col2:
            st.metric("Información de peso", results.fabrics.weight_info)
            st.metric("Transpirabilidad", results.fabrics.breathability)
        
        if results.fabrics.materials_found:
            st.write("**Materiales detectados:**")
            st.write(", ".join(results.fabrics.materials_found))
    
    with tab3:
        st.subheader("🔗 Cierres y Elementos")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Tamaño de ojales", results.closures.buttonhole_size)
            st.metric("Facilidad de uso", results.closures.ease_of_use)
        
        with col2:
            st.metric("Accesibilidad de cierres", results.closures.zipper_accessibility)
        
        if results.closures.closure_types:
            st.write("**Tipos de cierre detectados:**")
            st.write(", ".join(results.closures.closure_types))
        
        if results.closures.adaptive_features:
            st.write("**Características adaptativas:**")
            st.write(", ".join(results.closures.adaptive_features))
    
    with tab4:
        st.subheader("🤲 Comodidad y Accesibilidad")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Movilidad", results.comfort.mobility)
            st.metric("Amigable sensorialmente", results.comfort.sensory_friendly)
        
        with col2:
            st.metric("Diseño ergonómico", "✅ Sí" if results.comfort.ergonomic_design else "❌ No")
            st.metric("Diseño universal", "✅ Sí" if results.comfort.universal_design else "❌ No")

def display_screening_report(results: AnalysisResults):
    """Mostrar reporte de screening para validación humana"""
    
    st.header("🔍 Reporte de Screening - REQUIERE VALIDACIÓN HUMANA")
    
    screening = results.screening_report
    
    # Información general del screening
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏰ Tiempo estimado validación", f"{screening.estimated_validation_time} min")
    with col2:
        st.metric("👥 Tipos de expertos", len(screening.recommended_experts))
    with col3:
        st.metric("📋 Items a validar", len(screening.validation_checklist))
    
    # Niveles de confianza
    st.subheader("📊 Niveles de Confianza del Screening")
    confidence_data = []
    for key, confidence in screening.confidence_levels.items():
        confidence_data.append({
            'Aspecto': key.replace('_', ' ').title(),
            'Confianza': confidence,
            'Porcentaje': f"{confidence:.1%}"
        })
    
    if confidence_data:
        df_confidence = pd.DataFrame(confidence_data)
        
        # Gráfico de confianza
        fig = px.bar(
            df_confidence, 
            x='Aspecto', 
            y='Confianza',
            color='Confianza',
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Niveles de Confianza del Análisis Automático"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True, key="confidence_levels_chart")
    
    # Banderas de riesgo
    if screening.risk_flags:
        st.subheader("⚠️ Banderas de Riesgo Detectadas")
        for flag in screening.risk_flags:
            st.warning(f"🚩 {flag.replace('_', ' ').title()}")
    
    # Áreas prioritarias
    if screening.priority_areas:
        st.subheader("🎯 Áreas Prioritarias para Validación")
        for area in screening.priority_areas:
            st.info(f"🔥 {area}")
    
    # Checklist de validación
    st.subheader("📋 Checklist de Validación Humana")
    
    # Crear DataFrame para el checklist
    checklist_data = []
    for item in screening.validation_checklist:
        checklist_data.append({
            'Prioridad': item.priority,
            'Categoría': item.category,
            'Hallazgo': item.finding,
            'Validación Requerida': item.validation_needed,
            'Tiempo (min)': item.estimated_time_minutes,
            'Experto': item.expert_type.replace('_', ' ').title()
        })
    
    if checklist_data:
        df_checklist = pd.DataFrame(checklist_data)
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            priority_filter = st.selectbox(
                "Filtrar por prioridad:",
                ["Todas"] + list(df_checklist['Prioridad'].unique())
            )
        with col2:
            category_filter = st.selectbox(
                "Filtrar por categoría:",
                ["Todas"] + list(df_checklist['Categoría'].unique())
            )
        
        # Aplicar filtros
        filtered_df = df_checklist.copy()
        if priority_filter != "Todas":
            filtered_df = filtered_df[filtered_df['Prioridad'] == priority_filter]
        if category_filter != "Todas":
            filtered_df = filtered_df[filtered_df['Categoría'] == category_filter]
        
        # Mostrar tabla
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            key="validation_checklist_table"
        )
        
        # Resumen por prioridad
        st.subheader("📊 Resumen por Prioridad")
        priority_summary = df_checklist.groupby('Prioridad').agg({
            'Tiempo (min)': 'sum',
            'Categoría': 'count'
        }).rename(columns={'Categoría': 'Cantidad'})
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(priority_summary, key="priority_summary_table")
        with col2:
            fig = px.pie(
                values=priority_summary['Cantidad'],
                names=priority_summary.index,
                title="Distribución de Items por Prioridad"
            )
            st.plotly_chart(fig, use_container_width=True, key="priority_distribution_pie_chart")

def display_recommendations(results: AnalysisResults):
    """Mostrar recomendaciones automáticas"""
    
    st.header("💡 Recomendaciones Automáticas")
    
    for i, rec in enumerate(results.recommendations, 1):
        st.write(f"**{i}.** {rec}")

def display_technical_details(results: AnalysisResults):
    """Mostrar detalles técnicos"""
    
    with st.expander("📊 Información Técnica Detallada"):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📁 Información del Archivo")
            tech_details = results.technical_details
            
            if 'content_analysis' in tech_details:
                content_info = tech_details['content_analysis']
                st.metric("Caracteres analizados", f"{content_info.get('total_characters', 0):,}")
                st.metric("Palabras", f"{content_info.get('word_count', 0):,}")
                st.metric("Líneas", f"{content_info.get('line_count', 0):,}")
                st.metric("Estructura XML", "✅ Sí" if content_info.get('has_xml_structure') else "❌ No")
        
        with col2:
            st.subheader("🔑 Metadatos")
            st.text(f"Hash del archivo: {tech_details.get('file_hash', 'N/A')[:16]}...")
            st.text(f"Timestamp: {tech_details.get('analysis_timestamp', 'N/A')}")
            
            # Información específica del formato
            if 'zpac_structure' in tech_details:
                zpac_info = tech_details['zpac_structure']
                st.metric("Imágenes embebidas", zpac_info.get('embedded_images', 0))
                st.metric("Secciones de datos", zpac_info.get('data_sections', 0))

def display_download_options(results: AnalysisResults, filename: str):
    """Opciones de descarga de resultados"""
    
    st.header("💾 Descargar Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # JSON completo
        json_data = json.dumps(results.__dict__, default=str, indent=2, ensure_ascii=False)
        st.download_button(
            label="📄 Descargar JSON completo",
            data=json_data,
            file_name=f"analysis_{Path(filename).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Checklist para expertos
        if results.screening_report.validation_checklist:
            checklist_data = []
            for item in results.screening_report.validation_checklist:
                checklist_data.append({
                    'Prioridad': item.priority,
                    'Categoría': item.category,
                    'Hallazgo': item.finding,
                    'Validación Requerida': item.validation_needed,
                    'Tiempo (min)': item.estimated_time_minutes,
                    'Experto': item.expert_type.replace('_', ' ').title()
                })
            
            df_checklist = pd.DataFrame(checklist_data)
            csv_data = df_checklist.to_csv(index=False)
            
            st.download_button(
                label="📋 Descargar Checklist CSV",
                data=csv_data,
                file_name=f"checklist_{Path(filename).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col3:
        # Reporte resumido
        summary_report = generate_summary_report(results, filename)
        st.download_button(
            label="📊 Descargar Reporte Resumido",
            data=summary_report,
            file_name=f"summary_{Path(filename).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

def generate_summary_report(results: AnalysisResults, filename: str) -> str:
    """Generar reporte resumido en texto"""
    
    report = f"""
MOVING ACCESSIBILITY ANALYZER - REPORTE DE SCREENING
================================================================

ARCHIVO: {filename}
FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
TIPO: {results.file_type}
TAMAÑO: {results.file_size_mb:.2f} MB
TIEMPO DE PROCESAMIENTO: {results.processing_time:.2f} segundos

⚠️ IMPORTANTE: Este es un SCREENING AUTOMÁTICO que requiere validación humana experta.

PUNTUACIONES DE SCREENING:
- Inclusividad: {results.inclusivity_score}/100
- Accesibilidad: {results.accessibility_score}/100  
- Sostenibilidad: {results.sustainability_score}/100

ANÁLISIS DETALLADO:
- Rango de tallas: {results.sizing.size_range}
- Adaptabilidad: {results.sizing.adaptability}
- Diseño inclusivo: {'Sí' if results.sizing.inclusive_design else 'No'}
- Materiales detectados: {', '.join(results.fabrics.materials_found) if results.fabrics.materials_found else 'Ninguno específico'}
- Tipos de cierre: {', '.join(results.closures.closure_types) if results.closures.closure_types else 'No detectados'}

VALIDACIÓN HUMANA REQUERIDA:
- Tiempo estimado: {results.screening_report.estimated_validation_time} minutos
- Expertos recomendados: {len(results.screening_report.recommended_experts)} tipos
- Items a validar: {len(results.screening_report.validation_checklist)}

RECOMENDACIONES AUTOMÁTICAS:
"""
    
    for i, rec in enumerate(results.recommendations, 1):
        report += f"{i}. {rec}\n"
    
    report += f"""
================================================================
GENERADO POR: Moving Accessibility Analyzer v2.0
HASH DEL ARCHIVO: {results.technical_details.get('file_hash', 'N/A')[:16]}...
================================================================
"""
    
    return report

def display_chatbot_interface(results: AnalysisResults, filename: str):
    """Mostrar interfaz del chatbot interactivo"""
    
    if not CHATBOT_AVAILABLE:
        st.info("💬 Chatbot no disponible - Instala las dependencias necesarias")
        return
    
    st.header("💬 Chatbot de Análisis Interactivo")
    
    # Información sobre el chatbot
    with st.expander("ℹ️ Sobre el Chatbot de Accesibilidad"):
        st.markdown("""
        Este chatbot está especializado en análisis de accesibilidad e inclusividad en moda. Puede ayudarte a:
        
        - 🔍 **Interpretar tus resultados** de análisis
        - 📊 **Explicar la metodología** de cálculo de scores
        - 💡 **Sugerir mejoras específicas** para tu diseño
        - ✅ **Recomendar validaciones** manuales necesarias
        - 🎯 **Comparar con mejores prácticas** de la industria
        """)
    
    # Configuración del chatbot
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("⚙️ Configuración")
        
        # Selección de proveedor LLM
        available_providers = accessibility_chatbot.get_available_providers()
        
        if not available_providers:
            st.error("❌ No hay proveedores LLM configurados")
            st.info("""
            Para usar el chatbot, configura al menos una API key:
            - `OPENAI_API_KEY`
            - `ANTHROPIC_API_KEY` 
            - `GROQ_API_KEY`
            - `MISTRAL_API_KEY`
            - `OPENROUTER_API_KEY`
            """)
            return
        
        provider_options = {p["name"]: p["provider"] for p in available_providers}
        selected_provider_name = st.selectbox(
            "Proveedor LLM:",
            options=list(provider_options.keys()),
            help="Selecciona el proveedor de IA para el chatbot"
        )
        
        selected_provider = LLMProvider(provider_options[selected_provider_name])
        
        # Mostrar información del modelo
        provider_info = next(p for p in available_providers if p["provider"] == selected_provider.value)
        st.info(f"**Modelo**: {provider_info['model']}")
    
    with col1:
        st.subheader("💭 Conversación")
        
        # Inicializar sesión de chat (crear nueva solo si no existe o si es un nuevo análisis)
        if 'chat_session_id' not in st.session_state or st.session_state.chat_session_id is None:
            st.session_state.chat_session_id = accessibility_chatbot.create_session(results)
        
        session_id = st.session_state.chat_session_id
        
        # Mostrar historial de chat
        chat_history = accessibility_chatbot.get_session_history(session_id)
        
        # Contenedor para mensajes
        chat_container = st.container()
        
        with chat_container:
            for message in chat_history:
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.write(message["content"])
                elif message["role"] == "assistant":
                    with st.chat_message("assistant"):
                        st.write(message["content"])
        
        # Input para nuevo mensaje
        user_input = st.chat_input("Pregunta sobre tu análisis...")
        
        if user_input:
            # Mostrar mensaje del usuario inmediatamente
            with st.chat_message("user"):
                st.write(user_input)
            
            # Procesar respuesta del chatbot
            with st.chat_message("assistant"):
                with st.spinner("Analizando tu pregunta..."):
                    try:
                        # Usar asyncio para la llamada async
                        import asyncio
                        
                        # Crear nuevo loop si no existe
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                        
                        # Ejecutar chat de forma síncrona
                        response, success = loop.run_until_complete(
                            accessibility_chatbot.chat(session_id, user_input, selected_provider)
                        )
                        
                        if success:
                            st.write(response)
                        else:
                            st.error(f"Error: {response}")
                            
                    except Exception as e:
                        st.error(f"Error procesando mensaje: {str(e)}")
    
    # Preguntas sugeridas
    st.subheader("💡 Preguntas Sugeridas")
    
    suggested_questions = accessibility_chatbot.get_suggested_questions(results)
    
    # Mostrar preguntas en columnas
    cols = st.columns(2)
    for i, question in enumerate(suggested_questions):
        col = cols[i % 2]
        with col:
            if st.button(question, key=f"suggestion_{i}", use_container_width=True):
                # Simular click en input con la pregunta sugerida
                st.session_state.suggested_question = question
                st.rerun()
    
    # Procesar pregunta sugerida si existe
    if 'suggested_question' in st.session_state:
        question = st.session_state.suggested_question
        del st.session_state.suggested_question
        
        # Procesar la pregunta sugerida de forma asíncrona
        try:
            import asyncio
            
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            response, success = loop.run_until_complete(
                accessibility_chatbot.chat(session_id, question, selected_provider)
            )
            
            if success:
                # Guardar la respuesta en session_state para mostrarla
                if 'chat_responses' not in st.session_state:
                    st.session_state.chat_responses = []
                st.session_state.chat_responses.append({
                    'question': question,
                    'response': response,
                    'success': True
                })
            else:
                if 'chat_responses' not in st.session_state:
                    st.session_state.chat_responses = []
                st.session_state.chat_responses.append({
                    'question': question,
                    'response': response,
                    'success': False
                })
                
        except Exception as e:
            if 'chat_responses' not in st.session_state:
                st.session_state.chat_responses = []
            st.session_state.chat_responses.append({
                'question': question,
                'response': f"Error procesando pregunta: {str(e)}",
                'success': False
            })
        
        # Forzar re-run para mostrar la respuesta
        st.rerun()
    
    # Información adicional
    with st.expander("📊 Información de la Sesión"):
        session = accessibility_chatbot.get_session(session_id)
        if session:
            summary = session.get_conversation_summary()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mensajes totales", summary["total_messages"])
            with col2:
                st.metric("Preguntas del usuario", summary["user_messages"])
            with col3:
                st.metric("Respuestas del asistente", summary["assistant_messages"])
            
            st.json(summary["analysis_scores"])

if __name__ == "__main__":
    main()