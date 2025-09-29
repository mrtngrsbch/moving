#!/usr/bin/env python3
"""
Setup script para el Chatbot de Accesibilidad
Configuración automática y verificación de dependencias
"""

import os
import sys
import subprocess
import asyncio
from typing import Dict, List

def install_dependencies():
    """Instalar dependencias necesarias"""
    print("🔧 Instalando dependencias del chatbot...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_env_file():
    """Crear archivo .env si no existe"""
    if not os.path.exists('.env'):
        print("📝 Creando archivo .env...")
        
        try:
            with open('.env.example', 'r') as example:
                content = example.read()
            
            with open('.env', 'w') as env_file:
                env_file.write(content)
            
            print("✅ Archivo .env creado desde .env.example")
            print("⚠️  IMPORTANTE: Configura tus API keys en el archivo .env")
            return True
        except Exception as e:
            print(f"❌ Error creando .env: {e}")
            return False
    else:
        print("ℹ️  Archivo .env ya existe")
        return True

def check_api_keys() -> Dict[str, bool]:
    """Verificar API keys configuradas"""
    print("🔑 Verificando API keys...")
    
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'MISTRAL_API_KEY': os.getenv('MISTRAL_API_KEY'),
        'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY')
    }
    
    configured = {}
    for key, value in api_keys.items():
        is_configured = bool(value and value.strip() and not value.startswith('your-') and not value.startswith('sk-your-'))
        configured[key] = is_configured
        
        if is_configured:
            print(f"✅ {key}: Configurada")
        else:
            print(f"❌ {key}: No configurada")
    
    return configured

async def test_chatbot():
    """Probar funcionalidad del chatbot"""
    print("🧪 Probando funcionalidad del chatbot...")
    
    try:
        # Importar módulos del chatbot
        from chatbot import accessibility_chatbot, LLMProvider
        from analyzer_main import AnalysisResults, SizingMetrics, FabricMetrics, ClosureMetrics, ComfortMetrics, ScreeningReport
        
        print("✅ Módulos del chatbot importados correctamente")
        
        # Crear resultados de prueba
        test_results = AnalysisResults(
            file_type="Test GLTF",
            status="Test",
            file_size_mb=10.0,
            processing_time=1.0,
            inclusivity_score=75,
            accessibility_score=80,
            sustainability_score=65,
            sizing=SizingMetrics("Test", "High", True, ["S", "M", "L"], True, 3),
            fabrics=FabricMetrics("Test", "Good", ["cotton"], True, "200g/m²", "Good", "High"),
            closures=ClosureMetrics("Good", "Accessible", ["zipper"], ["adaptive"], "Easy"),
            comfort=ComfortMetrics("Good", "Friendly", ["soft"], True, True),
            recommendations=["Test recommendation"],
            technical_details={"test": True},
            raw_data_summary={"test": True},
            screening_report=ScreeningReport({}, {}, [], [], 30, [], [])
        )
        
        # Crear sesión de prueba
        session_id = accessibility_chatbot.create_session(test_results)
        print(f"✅ Sesión de prueba creada: {session_id}")
        
        # Verificar proveedores disponibles
        providers = accessibility_chatbot.get_available_providers()
        print(f"✅ Proveedores disponibles: {len(providers)}")
        
        for provider in providers:
            print(f"  - {provider['name']}: {provider['model']}")
        
        if providers:
            print("✅ Chatbot configurado correctamente")
            return True
        else:
            print("⚠️  Chatbot funcional pero sin proveedores LLM configurados")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error probando chatbot: {e}")
        return False

def print_configuration_guide():
    """Mostrar guía de configuración"""
    print("\n" + "="*60)
    print("📋 GUÍA DE CONFIGURACIÓN DEL CHATBOT")
    print("="*60)
    
    print("\n1. 🔑 CONFIGURAR API KEYS:")
    print("   Edita el archivo .env y agrega al menos una API key:")
    print()
    print("   # OpenAI (Recomendado)")
    print("   OPENAI_API_KEY=sk-tu-api-key-aqui")
    print()
    print("   # Anthropic Claude (Excelente calidad)")
    print("   ANTHROPIC_API_KEY=sk-ant-tu-api-key-aqui")
    print()
    print("   # Groq (Rápido y gratuito)")
    print("   GROQ_API_KEY=gsk_tu-api-key-aqui")
    print()
    
    print("2. 🚀 OBTENER API KEYS:")
    print("   • OpenAI: https://platform.openai.com/api-keys")
    print("   • Anthropic: https://console.anthropic.com/")
    print("   • Groq: https://console.groq.com/keys")
    print("   • Mistral: https://console.mistral.ai/")
    print("   • OpenRouter: https://openrouter.ai/keys")
    print()
    
    print("3. 🔄 REINICIAR APLICACIÓN:")
    print("   Después de configurar las API keys:")
    print("   streamlit run streamlit_app.py")
    print()
    
    print("4. 💬 USAR EL CHATBOT:")
    print("   • Sube un archivo y completa el análisis")
    print("   • El chatbot aparecerá al final de los resultados")
    print("   • Haz preguntas sobre tu análisis")
    print("   • Usa las preguntas sugeridas para empezar")

def main():
    """Función principal de setup"""
    print("🎯 Moving Accessibility Analyzer - Setup del Chatbot")
    print("="*60)
    
    # 1. Instalar dependencias
    if not install_dependencies():
        print("❌ Setup fallido: No se pudieron instalar las dependencias")
        return False
    
    # 2. Crear archivo .env
    if not create_env_file():
        print("❌ Setup fallido: No se pudo crear el archivo .env")
        return False
    
    # 3. Verificar API keys
    configured_keys = check_api_keys()
    has_any_key = any(configured_keys.values())
    
    # 4. Probar chatbot
    chatbot_works = asyncio.run(test_chatbot())
    
    # 5. Mostrar resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DEL SETUP")
    print("="*60)
    
    print(f"✅ Dependencias: Instaladas")
    print(f"✅ Archivo .env: {'Creado' if os.path.exists('.env') else 'Error'}")
    print(f"{'✅' if has_any_key else '❌'} API Keys: {sum(configured_keys.values())}/5 configuradas")
    print(f"{'✅' if chatbot_works else '⚠️ '} Chatbot: {'Funcional' if chatbot_works else 'Parcial'}")
    
    if has_any_key and chatbot_works:
        print("\n🎉 ¡Setup completado exitosamente!")
        print("   El chatbot está listo para usar.")
        print("   Ejecuta: streamlit run streamlit_app.py")
    else:
        print("\n⚠️  Setup parcialmente completado")
        print("   Configura las API keys para usar el chatbot.")
        print_configuration_guide()
    
    return has_any_key and chatbot_works

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)