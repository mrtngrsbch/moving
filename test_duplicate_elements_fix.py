#!/usr/bin/env python3
"""
Script de prueba para verificar que no hay elementos duplicados en Streamlit
"""

import re

def check_duplicate_elements():
    """Verificar elementos que pueden tener IDs duplicados"""
    
    print("🔍 Verificando elementos con keys únicos en streamlit_app.py")
    print("=" * 60)
    
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
    
    # Elementos que necesitan keys únicos
    elements_to_check = {
        'plotly_chart': r'st\.plotly_chart\([^)]*\)',
        'dataframe': r'st\.dataframe\([^)]*\)',
        'selectbox': r'st\.selectbox\([^)]*\)',
        'button': r'st\.button\([^)]*\)'
        # Nota: st.metric() no acepta 'key' en Streamlit 1.50.0
    }
    
    results = {}
    
    for element_type, pattern in elements_to_check.items():
        matches = re.findall(pattern, content)
        
        # Verificar cuáles tienen key
        with_key = []
        without_key = []
        
        for match in matches:
            if 'key=' in match:
                with_key.append(match)
            else:
                without_key.append(match)
        
        results[element_type] = {
            'total': len(matches),
            'with_key': len(with_key),
            'without_key': len(without_key),
            'without_key_examples': without_key[:3]  # Primeros 3 ejemplos
        }
    
    # Mostrar resultados
    for element_type, data in results.items():
        status = "✅" if data['without_key'] == 0 else "⚠️" if data['without_key'] < 3 else "❌"
        print(f"{status} {element_type.upper()}:")
        print(f"   Total: {data['total']}")
        print(f"   Con key: {data['with_key']}")
        print(f"   Sin key: {data['without_key']}")
        
        if data['without_key'] > 0:
            print("   Ejemplos sin key:")
            for example in data['without_key_examples']:
                print(f"     - {example[:80]}...")
        print()
    
    # Verificar keys únicos
    print("🔑 Verificando unicidad de keys...")
    key_pattern = r'key=["\']([^"\']+)["\']'
    keys = re.findall(key_pattern, content)
    
    unique_keys = set(keys)
    duplicate_keys = [key for key in keys if keys.count(key) > 1]
    
    if duplicate_keys:
        print(f"❌ Keys duplicados encontrados: {set(duplicate_keys)}")
    else:
        print("✅ Todos los keys son únicos")
    
    print(f"📊 Total de keys: {len(keys)}")
    print(f"📊 Keys únicos: {len(unique_keys)}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN")
    print("=" * 60)
    
    total_elements = sum(data['total'] for data in results.values())
    total_with_key = sum(data['with_key'] for data in results.values())
    total_without_key = sum(data['without_key'] for data in results.values())
    
    print(f"Total elementos verificados: {total_elements}")
    print(f"Con key único: {total_with_key}")
    print(f"Sin key: {total_without_key}")
    
    if total_without_key == 0 and not duplicate_keys:
        print("🎉 ¡Perfecto! No hay elementos duplicados.")
        return True
    else:
        print("⚠️ Hay elementos que podrían causar problemas.")
        return False

def check_specific_plotly_elements():
    """Verificar específicamente los elementos plotly_chart"""
    print("\n🎯 Verificación específica de plotly_chart")
    print("=" * 40)
    
    with open('streamlit_app.py', 'r') as f:
        content = f.read()
    
    # Buscar todos los plotly_chart
    plotly_pattern = r'st\.plotly_chart\([^)]*\)'
    matches = re.findall(plotly_pattern, content)
    
    print(f"Total plotly_chart encontrados: {len(matches)}")
    
    for i, match in enumerate(matches, 1):
        has_key = 'key=' in match
        status = "✅" if has_key else "❌"
        print(f"{status} #{i}: {match[:60]}...")
        
        if has_key:
            key_match = re.search(r'key=["\']([^"\']+)["\']', match)
            if key_match:
                print(f"     Key: {key_match.group(1)}")
    
    return all('key=' in match for match in matches)

if __name__ == "__main__":
    print("🧪 Test de Elementos Duplicados - Streamlit")
    print("=" * 60)
    
    general_ok = check_duplicate_elements()
    plotly_ok = check_specific_plotly_elements()
    
    if general_ok and plotly_ok:
        print("\n🎉 ¡Todos los tests pasaron! No debería haber errores de elementos duplicados.")
    else:
        print("\n⚠️ Algunos tests fallaron. Revisa los elementos sin keys únicos.")