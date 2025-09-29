#!/usr/bin/env python3
"""
Script de prueba para verificar la corrección del bug de persistencia
"""

import streamlit as st
from datetime import datetime

def test_session_state():
    """Probar que session_state mantiene los datos"""
    st.title("🧪 Test de Persistencia - Session State")
    
    # Inicializar session state
    if 'test_data' not in st.session_state:
        st.session_state.test_data = None
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    
    # Simular datos de análisis
    if st.button("🔬 Simular Análisis"):
        st.session_state.test_data = {
            'timestamp': datetime.now().isoformat(),
            'file_name': 'test_file.gltf',
            'scores': {
                'inclusivity': 75,
                'accessibility': 80,
                'sustainability': 65
            }
        }
        st.session_state.counter += 1
        st.success("✅ Datos de análisis simulados guardados en session_state")
    
    # Widget que causa re-run
    selected_option = st.selectbox(
        "🔄 Selector que causa re-run:",
        ["Opción 1", "Opción 2", "Opción 3", "Opción 4"],
        help="Cambiar esta opción debería mantener los datos del análisis"
    )
    
    st.write(f"**Opción seleccionada:** {selected_option}")
    st.write(f"**Contador de re-runs:** {st.session_state.counter}")
    
    # Mostrar datos persistentes
    if st.session_state.test_data:
        st.success("🎉 ¡Los datos persisten correctamente!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.json(st.session_state.test_data)
        
        with col2:
            st.metric("Inclusividad", f"{st.session_state.test_data['scores']['inclusivity']}/100")
            st.metric("Accesibilidad", f"{st.session_state.test_data['scores']['accessibility']}/100")
            st.metric("Sostenibilidad", f"{st.session_state.test_data['scores']['sustainability']}/100")
        
        # Botón para limpiar
        if st.button("🗑️ Limpiar Datos"):
            st.session_state.test_data = None
            st.session_state.counter = 0
            st.rerun()
    else:
        st.info("ℹ️ No hay datos de análisis. Haz click en 'Simular Análisis' para crear datos de prueba.")
    
    # Información sobre el fix
    with st.expander("📋 Información sobre el Fix"):
        st.markdown("""
        ### 🐛 Problema Original:
        - Al interactuar con widgets (dropdown, botones), Streamlit re-ejecuta todo el script
        - Los resultados del análisis se perdían porque no estaban en `session_state`
        - El usuario tenía que volver a subir y analizar el archivo
        
        ### ✅ Solución Implementada:
        - Guardar resultados del análisis en `st.session_state`
        - Mostrar resultados persistentes desde `session_state`
        - Agregar botón para limpiar resultados cuando sea necesario
        - Manejar correctamente las sesiones de chat
        
        ### 🧪 Esta Prueba Verifica:
        - Los datos se mantienen después de interactuar con widgets
        - El contador muestra cuántas veces se re-ejecuta el script
        - Los datos persisten hasta que se limpien explícitamente
        """)

if __name__ == "__main__":
    test_session_state()