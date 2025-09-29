#!/usr/bin/env python3
"""
Moving Accessibility Analyzer - Versión Mejorada
Análisis con validación de contexto para reducir falsos positivos
"""

import re
from typing import List, Dict, Tuple

def analyze_closures_with_context(content: str) -> Dict[str, any]:
    """Análisis de cierres con validación de contexto semántico"""
    
    # Patrones mejorados que requieren contexto
    contextual_patterns = {
        'buttons': [
            r'button\s+(hole|fastener|closure|opening)',
            r'(sew|attach|add)\s+button',
            r'button\s+(size|diameter|placement)',
            r'buttonhole\s+(size|width|length)',
        ],
        'zippers': [
            r'zipper\s+(closure|fastener|opening|pull)',
            r'(install|attach|sew)\s+zipper',
            r'zipper\s+(length|size|type)',
            r'zip\s+(closure|fastener|opening)',
        ],
        'velcro': [
            r'velcro\s+(closure|fastener|strip)',
            r'hook\s+and\s+loop',
            r'(attach|sew)\s+velcro',
        ],
        'ties': [
            r'tie\s+(closure|fastener|string)',
            r'drawstring\s+(closure|opening)',
            r'(ribbon|cord|string)\s+tie',
        ]
    }
    
    detected_closures = {}
    confidence_scores = {}
    
    for closure_type, patterns in contextual_patterns.items():
        matches = []
        total_confidence = 0
        
        for pattern in patterns:
            pattern_matches = re.findall(pattern, content, re.IGNORECASE)
            if pattern_matches:
                matches.extend(pattern_matches)
                # Dar más confianza a patrones más específicos
                if 'size' in pattern or 'length' in pattern:
                    total_confidence += 0.8
                elif 'closure' in pattern or 'fastener' in pattern:
                    total_confidence += 0.9
                else:
                    total_confidence += 0.6
        
        if matches:
            detected_closures[closure_type] = {
                'count': len(matches),
                'matches': matches[:5],  # Primeros 5 matches
                'confidence': min(total_confidence, 1.0)
            }
            confidence_scores[closure_type] = min(total_confidence, 1.0)
    
    return {
        'detected_closures': detected_closures,
        'confidence_scores': confidence_scores,
        'total_types': len(detected_closures),
        'high_confidence_types': [k for k, v in confidence_scores.items() if v >= 0.8]
    }

def test_with_sample_content():
    """Probar con contenido de muestra"""
    
    # Contenido que DEBERÍA detectar cierres
    good_content = """
    This garment features a zipper closure at the front.
    Button fasteners are placed along the sleeve.
    The buttonhole size is 15mm for accessibility.
    Velcro strips provide easy closure for users with limited dexterity.
    """
    
    # Contenido que NO debería detectar cierres (falsos positivos)
    bad_content = """
    File compression using zip algorithm.
    Database tie between tables.
    Button element in the UI design.
    kbtiE'ahPiM:ɻŲ random binary data
    """
    
    print("🟢 CONTENIDO CON CIERRES REALES:")
    good_results = analyze_closures_with_context(good_content)
    for closure_type, data in good_results['detected_closures'].items():
        print(f"   {closure_type}: {data['count']} matches (confianza: {data['confidence']:.1%})")
    
    print("\n🔴 CONTENIDO SIN CIERRES (debería estar vacío):")
    bad_results = analyze_closures_with_context(bad_content)
    if bad_results['detected_closures']:
        for closure_type, data in bad_results['detected_closures'].items():
            print(f"   {closure_type}: {data['count']} matches (confianza: {data['confidence']:.1%})")
    else:
        print("   ✅ Ningún falso positivo detectado")

if __name__ == "__main__":
    test_with_sample_content()