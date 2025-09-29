#!/usr/bin/env python3
"""
Script de prueba para verificar la integración del chatbot
"""

from dotenv import load_dotenv
import os

def test_env_loading():
    """Probar carga de variables de entorno"""
    print("🔧 Probando carga de variables de entorno...")
    load_dotenv()
    
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
        'GROQ_API_KEY': os.getenv('GROQ_API_KEY'),
        'MISTRAL_API_KEY': os.getenv('MISTRAL_API_KEY'),
        'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY')
    }
    
    configured_count = 0
    for key, value in api_keys.items():
        is_configured = bool(value and value.strip() and not value.startswith('sk-your-') and not value.startswith('your-'))
        if is_configured:
            configured_count += 1
            print(f"✅ {key}: Configurada")
        else:
            print(f"❌ {key}: No configurada")
    
    print(f"📊 Total configuradas: {configured_count}/5")
    return configured_count > 0

def test_chatbot_import():
    """Probar importación del chatbot"""
    print("\n🤖 Probando importación del chatbot...")
    
    try:
        from chatbot import accessibility_chatbot, LLMProvider
        print("✅ Chatbot importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando chatbot: {e}")
        return False

def test_providers():
    """Probar proveedores disponibles"""
    print("\n🔌 Probando proveedores LLM...")
    
    try:
        from chatbot import accessibility_chatbot
        providers = accessibility_chatbot.get_available_providers()
        
        print(f"✅ Proveedores disponibles: {len(providers)}")
        for provider in providers:
            print(f"  - {provider['name']}: {provider['model']}")
        
        return len(providers) > 0
    except Exception as e:
        print(f"❌ Error probando proveedores: {e}")
        return False

def test_streamlit_import():
    """Probar importación de Streamlit app"""
    print("\n🌐 Probando importación de Streamlit...")
    
    try:
        import streamlit_app
        print("✅ Streamlit app importada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando Streamlit app: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🎯 Moving Accessibility Analyzer - Test de Integración del Chatbot")
    print("=" * 70)
    
    tests = [
        ("Variables de entorno", test_env_loading),
        ("Importación del chatbot", test_chatbot_import),
        ("Proveedores LLM", test_providers),
        ("Streamlit app", test_streamlit_import)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 70)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(tests)} pruebas pasaron")
    
    if passed == len(tests):
        print("🎉 ¡Todas las pruebas pasaron! El chatbot está listo para usar.")
        print("🚀 Ejecuta: streamlit run streamlit_app.py")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)