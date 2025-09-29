#!/usr/bin/env python3
"""
Moving Accessibility Analyzer - Versión Mejorada para GLTF
Análisis avanzado de archivos GLTF con reducción de falsos positivos

Mejoras implementadas:
- Análisis semántico contextual de la estructura JSON
- Validación cruzada de materiales y texturas
- Reducción de falsos positivos mediante patrones contextuales
- Métricas de confianza para cada análisis
- Clasificación avanzada de materiales basada en propiedades PBR
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class GLTFAnalysisResult:
    """Resultado del análisis GLTF mejorado"""
    file_path: str
    gltf_version: str
    generator: str
    confidence_score: float
    garment_elements: List[Dict[str, Any]]
    fabric_properties: Dict[str, Any]
    size_variations: List[Dict[str, Any]]
    accessibility_features: List[Dict[str, Any]]
    validation_sources: List[str]
    false_positive_flags: List[str]

class ImprovedGLTFAnalyzer:
    """Analizador GLTF mejorado con reducción de falsos positivos"""
    
    def __init__(self):
        # Patrones contextuales mejorados para reducir falsos positivos
        self.garment_context_patterns = {
            'closures': {
                'primary': ['zipper', 'button', 'snap', 'velcro', 'closure', 'fastener', 'cremallera', 'botón'],
                'context': ['front', 'back', 'side', 'pocket', 'cuff', 'collar', 'frontal', 'lateral'],
                'exclusions': ['texture', 'pattern', 'decoration', 'logo', 'textura', 'patrón', 'decoración']
            },
            'body_parts': {
                'primary': ['sleeve', 'collar', 'cuff', 'hem', 'waist', 'chest', 'back', 'front', 'manga', 'cuello'],
                'context': ['left', 'right', 'upper', 'lower', 'main', 'body', 'izquierda', 'derecha'],
                'exclusions': ['texture', 'shadow', 'light', 'camera', 'textura', 'sombra', 'luz']
            },
            'construction': {
                'primary': ['seam', 'stitch', 'binding', 'trim', 'lining', 'dart', 'pleat', 'costura', 'puntada'],
                'context': ['construction', 'sewing', 'assembly', 'join', 'construcción', 'cosido'],
                'exclusions': ['decoration', 'pattern', 'print', 'decoración', 'patrón', 'estampado']
            }
        }
        
        # Patrones de materiales con validación contextual
        self.fabric_indicators = {
            'natural_fibers': {
                'cotton': ['cotton', 'algodón', 'coton'],
                'wool': ['wool', 'lana', 'laine'],
                'silk': ['silk', 'seda', 'soie'],
                'linen': ['linen', 'lino', 'lin']
            },
            'synthetic_fibers': {
                'polyester': ['polyester', 'poliéster'],
                'nylon': ['nylon', 'nilón'],
                'acrylic': ['acrylic', 'acrílico']
            },
            'stretch_materials': {
                'elastane': ['elastane', 'elastano', 'spandex', 'lycra'],
                'elastic': ['elastic', 'elástico', 'stretch', 'estirable']
            }
        }
    
    def analyze_gltf_file(self, file_path: str) -> GLTFAnalysisResult:
        """Analizar archivo GLTF con análisis mejorado"""
        logger.info(f"🔍 Iniciando análisis GLTF mejorado: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                gltf_data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON GLTF: {e}")
            raise ValueError(f"Archivo GLTF inválido: {e}")
        
        # Información básica del archivo
        asset_info = gltf_data.get('asset', {})
        gltf_version = asset_info.get('version', 'Unknown')
        generator = asset_info.get('generator', 'Unknown')
        
        logger.info(f"📊 GLTF v{gltf_version} generado por: {generator}")
        
        # Análisis semántico avanzado
        garment_elements = self._analyze_garment_elements_contextual(gltf_data)
        fabric_properties = self._analyze_fabric_properties_advanced(gltf_data)
        size_variations = self._analyze_size_variations_validated(gltf_data)
        accessibility_features = self._analyze_accessibility_features(gltf_data, garment_elements)
        
        # Calcular confianza general
        confidence_score = self._calculate_overall_confidence(
            garment_elements, fabric_properties, size_variations, accessibility_features
        )
        
        # Recopilar fuentes de validación
        validation_sources = self._collect_validation_sources(fabric_properties, garment_elements)
        
        # Detectar posibles falsos positivos
        false_positive_flags = self._detect_false_positives(gltf_data, garment_elements, fabric_properties)
        
        logger.info(f"✅ Análisis completado - Confianza: {confidence_score:.2f}")
        
        return GLTFAnalysisResult(
            file_path=file_path,
            gltf_version=gltf_version,
            generator=generator,
            confidence_score=confidence_score,
            garment_elements=garment_elements,
            fabric_properties=fabric_properties,
            size_variations=size_variations,
            accessibility_features=accessibility_features,
            validation_sources=validation_sources,
            false_positive_flags=false_positive_flags
        )
    
    def _analyze_garment_elements_contextual(self, gltf_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Análisis contextual de elementos de prenda con validación"""
        garment_elements = []
        
        for i, mesh in enumerate(gltf_data.get('meshes', [])):
            mesh_name = mesh.get('name', '').lower()
            if not mesh_name:
                continue
            
            element_analysis = {
                'mesh_name': mesh.get('name'),
                'mesh_index': i,
                'detected_elements': [],
                'confidence_score': 0.0,
                'validation_context': {}
            }
            
            # Analizar cada categoría con validación contextual
            for category, patterns in self.garment_context_patterns.items():
                category_elements = []
                
                for keyword in patterns['primary']:
                    if keyword in mesh_name:
                        # Calcular confianza base
                        base_confidence = 0.8
                        
                        # Validar contexto positivo
                        context_boost = 0.0
                        context_matches = []
                        for context_word in patterns['context']:
                            if context_word in mesh_name:
                                context_boost += 0.1
                                context_matches.append(context_word)
                        
                        # Penalizar exclusiones
                        exclusion_penalty = 0.0
                        exclusion_matches = []
                        for exclusion in patterns['exclusions']:
                            if exclusion in mesh_name:
                                exclusion_penalty += 0.3
                                exclusion_matches.append(exclusion)
                        
                        # Calcular confianza final
                        final_confidence = min(1.0, max(0.0, base_confidence + context_boost - exclusion_penalty))
                        
                        if final_confidence > 0.5:  # Umbral de confianza
                            category_elements.append({
                                'element': keyword,
                                'confidence': final_confidence,
                                'context_matches': context_matches,
                                'exclusion_flags': exclusion_matches,
                                'validated': len(context_matches) > 0 and len(exclusion_matches) == 0
                            })
                
                if category_elements:
                    element_analysis['detected_elements'].append({
                        'category': category,
                        'elements': category_elements,
                        'category_confidence': max(elem['confidence'] for elem in category_elements)
                    })
            
            # Calcular confianza general del mesh
            if element_analysis['detected_elements']:
                element_analysis['confidence_score'] = max(
                    cat['category_confidence'] for cat in element_analysis['detected_elements']
                )
                garment_elements.append(element_analysis)
        
        logger.info(f"🔍 Elementos de prenda detectados: {len(garment_elements)}")
        return garment_elements
    
    def _analyze_fabric_properties_advanced(self, gltf_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análisis avanzado de propiedades de tela con validación cruzada"""
        fabric_analysis = {
            'materials': {},
            'confidence_distribution': {},
            'validation_methods': []
        }
        
        materials = gltf_data.get('materials', [])
        textures = gltf_data.get('textures', [])
        images = gltf_data.get('images', [])
        
        for i, material in enumerate(materials):
            mat_name = material.get('name', f'material_{i}')
            
            material_analysis = {
                'name': mat_name,
                'index': i,
                'properties': {},
                'confidence': 0.0,
                'validation_sources': []
            }
            
            # Análisis de extensiones CLO3D (máxima confianza)
            if 'extensions' in material:
                clo_ext = material['extensions'].get('CLO_material_properties', {})
                if clo_ext:
                    material_analysis['properties'].update({
                        'stretch_warp': clo_ext.get('Stretch-Warp', 0),
                        'stretch_weft': clo_ext.get('Stretch-Weft', 0),
                        'weight': clo_ext.get('Weight', 0),
                        'thickness': clo_ext.get('Thickness', 0),
                        'has_stretch': clo_ext.get('Stretch-Warp', 0) > 100000 or clo_ext.get('Stretch-Weft', 0) > 100000
                    })
                    material_analysis['confidence'] = 0.95
                    material_analysis['validation_sources'].append('CLO3D_extension')
                    fabric_analysis['validation_methods'].append('CLO3D_extension')
            
            # Análisis de propiedades PBR con clasificación inteligente
            pbr = material.get('pbrMetallicRoughness', {})
            if pbr:
                roughness = pbr.get('roughnessFactor', 0.5)
                metallic = pbr.get('metallicFactor', 0.0)
                
                fabric_classification = self._classify_fabric_from_pbr(roughness, metallic, mat_name.lower())
                
                material_analysis['properties'].update({
                    'roughness': roughness,
                    'metallic': metallic,
                    'fabric_type': fabric_classification['type'],
                    'pbr_confidence': fabric_classification['confidence']
                })
                
                if material_analysis['confidence'] < fabric_classification['confidence']:
                    material_analysis['confidence'] = fabric_classification['confidence']
                
                material_analysis['validation_sources'].append('PBR_analysis')
                fabric_analysis['validation_methods'].append('PBR_analysis')
            
            # Validación cruzada con texturas
            texture_validation = self._validate_material_with_textures(material, textures, images)
            if texture_validation['confidence'] > 0:
                material_analysis['properties'].update(texture_validation['properties'])
                material_analysis['confidence'] = max(material_analysis['confidence'], texture_validation['confidence'])
                material_analysis['validation_sources'].extend(texture_validation['sources'])
                fabric_analysis['validation_methods'].extend(texture_validation['sources'])
            
            # Solo incluir materiales con confianza mínima
            if material_analysis['confidence'] > 0.3:
                fabric_analysis['materials'][mat_name] = material_analysis
        
        # Calcular distribución de confianza
        confidences = [mat['confidence'] for mat in fabric_analysis['materials'].values()]
        if confidences:
            fabric_analysis['confidence_distribution'] = {
                'high_confidence': len([c for c in confidences if c > 0.8]),
                'medium_confidence': len([c for c in confidences if 0.6 <= c <= 0.8]),
                'low_confidence': len([c for c in confidences if c < 0.6]),
                'average': sum(confidences) / len(confidences)
            }
        
        logger.info(f"🧵 Materiales analizados: {len(fabric_analysis['materials'])}")
        return fabric_analysis
    
    def _classify_fabric_from_pbr(self, roughness: float, metallic: float, mat_name: str) -> Dict[str, Any]:
        """Clasificar tipo de tela basado en propiedades PBR y nombre"""
        classification = {
            'type': 'unknown',
            'confidence': 0.0,
            'reasoning': []
        }
        
        # Verificar si es material metálico (hardware)
        if metallic > 0.7:
            classification.update({
                'type': 'metallic_hardware',
                'confidence': 0.9,
                'reasoning': ['High metallic factor indicates metal hardware']
            })
            return classification
        
        # Buscar indicadores en el nombre
        fabric_name_match = None
        for category, fabrics in self.fabric_indicators.items():
            for fabric_type, indicators in fabrics.items():
                if any(indicator in mat_name for indicator in indicators):
                    fabric_name_match = fabric_type
                    break
            if fabric_name_match:
                break
        
        # Clasificar basado en roughness para materiales no metálicos
        if metallic < 0.2:  # Definitivamente no metálico
            if roughness > 0.8:
                fabric_type = 'rough_fabric'
                confidence = 0.7
                reasoning = ['High roughness suggests rough woven fabric']
                
                if fabric_name_match in ['cotton', 'linen']:
                    fabric_type = fabric_name_match
                    confidence = 0.9
                    reasoning.append(f'Name validation supports {fabric_name_match}')
                    
            elif roughness < 0.3:
                fabric_type = 'smooth_fabric'
                confidence = 0.6
                reasoning = ['Low roughness suggests smooth fabric']
                
                if fabric_name_match in ['silk']:
                    fabric_type = fabric_name_match
                    confidence = 0.9
                    reasoning.append(f'Name validation supports {fabric_name_match}')
                    
            else:
                fabric_type = 'standard_fabric'
                confidence = 0.5
                reasoning = ['Medium roughness suggests standard fabric']
            
            classification.update({
                'type': fabric_type,
                'confidence': confidence,
                'reasoning': reasoning
            })
        
        return classification
    
    def _validate_material_with_textures(self, material: Dict[str, Any], textures: List[Dict[str, Any]], images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validar material mediante análisis de texturas asociadas"""
        validation = {
            'confidence': 0.0,
            'properties': {},
            'sources': []
        }
        
        # Buscar texturas asociadas
        texture_refs = []
        
        pbr = material.get('pbrMetallicRoughness', {})
        if 'baseColorTexture' in pbr:
            texture_refs.append(('diffuse', pbr['baseColorTexture'].get('index')))
        if 'metallicRoughnessTexture' in pbr:
            texture_refs.append(('metallic_roughness', pbr['metallicRoughnessTexture'].get('index')))
        
        if 'normalTexture' in material:
            texture_refs.append(('normal', material['normalTexture'].get('index')))
        
        # Analizar nombres de texturas
        fabric_indicators_found = []
        
        for tex_type, tex_index in texture_refs:
            if tex_index is not None and tex_index < len(textures):
                texture = textures[tex_index]
                source_index = texture.get('source')
                
                if source_index is not None and source_index < len(images):
                    image = images[source_index]
                    image_name = (image.get('name', '') or image.get('uri', '')).lower()
                    
                    # Buscar indicadores de tela
                    for category, fabrics in self.fabric_indicators.items():
                        for fabric_type, indicators in fabrics.items():
                            if any(indicator in image_name for indicator in indicators):
                                confidence = 0.7 if tex_type == 'diffuse' else 0.5
                                fabric_indicators_found.append({
                                    'type': fabric_type,
                                    'texture_type': tex_type,
                                    'confidence': confidence,
                                    'image_name': image_name
                                })
        
        if fabric_indicators_found:
            max_confidence = max(indicator['confidence'] for indicator in fabric_indicators_found)
            validation['confidence'] = max_confidence
            validation['properties']['texture_indicators'] = fabric_indicators_found
            validation['sources'].append('texture_analysis')
        
        return validation
    
    def _analyze_size_variations_validated(self, gltf_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Análisis de variaciones de talla con validación geométrica"""
        size_variations = []
        
        # Patrones de talla mejorados
        size_patterns = {
            'explicit_sizes': r'\b(xs|s|m|l|xl|xxl|xxxl|small|medium|large|chico|mediano|grande)\b',
            'numeric_sizes': r'\b(size[_\s]*\d+|talla[_\s]*\d+|\d+[_\s]*size)\b',
            'scale_variants': r'\b(scale[_\s]*[\d.]+|variant[_\s]*\d+|escala[_\s]*[\d.]+)\b'
        }
        
        for i, node in enumerate(gltf_data.get('nodes', [])):
            node_name = node.get('name', '').lower()
            if not node_name:
                continue
            
            size_analysis = {
                'node_name': node.get('name'),
                'node_index': i,
                'size_indicators': [],
                'confidence': 0.0,
                'geometric_validation': {}
            }
            
            # Buscar patrones de talla
            for pattern_type, pattern in size_patterns.items():
                matches = re.findall(pattern, node_name)
                if matches:
                    confidence = 0.8 if pattern_type == 'explicit_sizes' else 0.6
                    size_analysis['size_indicators'].extend([{
                        'type': pattern_type,
                        'value': match,
                        'confidence': confidence
                    } for match in matches])
            
            # Validación geométrica
            if 'scale' in node:
                scale = node['scale']
                if isinstance(scale, list) and len(scale) == 3:
                    scale_variance = max(scale) - min(scale)
                    size_analysis['geometric_validation'] = {
                        'has_scale': True,
                        'uniform_scale': scale_variance < 0.1,
                        'scale_factor': sum(scale) / 3,
                        'scale_variance': scale_variance
                    }
            
            # Calcular confianza final
            if size_analysis['size_indicators']:
                max_indicator_confidence = max(ind['confidence'] for ind in size_analysis['size_indicators'])
                geometric_boost = 0.2 if size_analysis['geometric_validation'].get('has_scale') else 0.0
                size_analysis['confidence'] = min(1.0, max_indicator_confidence + geometric_boost)
            
            if size_analysis['confidence'] > 0.5:
                size_variations.append(size_analysis)
        
        logger.info(f"📏 Variaciones de talla detectadas: {len(size_variations)}")
        return size_variations
    
    def _analyze_accessibility_features(self, gltf_data: Dict[str, Any], garment_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analizar características de accesibilidad"""
        accessibility_features = []
        
        # Evaluar cierres para accesibilidad
        for element in garment_elements:
            for category_info in element.get('detected_elements', []):
                if category_info['category'] == 'closures':
                    for closure_element in category_info['elements']:
                        accessibility_score = self._evaluate_closure_accessibility(closure_element['element'])
                        if accessibility_score > 0:
                            accessibility_features.append({
                                'type': 'closure_accessibility',
                                'element': closure_element['element'],
                                'mesh_name': element['mesh_name'],
                                'accessibility_score': accessibility_score,
                                'confidence': closure_element['confidence'],
                                'validated': closure_element.get('validated', False)
                            })
        
        logger.info(f"♿ Características de accesibilidad: {len(accessibility_features)}")
        return accessibility_features
    
    def _evaluate_closure_accessibility(self, closure_type: str) -> float:
        """Evaluar accesibilidad de diferentes tipos de cierre"""
        accessibility_scores = {
            'velcro': 0.9,      # Muy accesible
            'magnetic': 0.9,    # Muy accesible
            'snap': 0.7,        # Moderadamente accesible
            'zipper': 0.6,      # Depende del tipo
            'cremallera': 0.6,  # Depende del tipo
            'button': 0.4,      # Menos accesible
            'botón': 0.4,       # Menos accesible
            'tie': 0.3,         # Requiere destreza
            'toggle': 0.5       # Moderado
        }
        
        return accessibility_scores.get(closure_type, 0.0)
    
    def _calculate_overall_confidence(self, garment_elements: List[Dict[str, Any]], 
                                    fabric_properties: Dict[str, Any], 
                                    size_variations: List[Dict[str, Any]], 
                                    accessibility_features: List[Dict[str, Any]]) -> float:
        """Calcular confianza general del análisis"""
        confidence_factors = []
        
        # Confianza de elementos de prenda (40% peso)
        if garment_elements:
            avg_garment_confidence = sum(elem['confidence_score'] for elem in garment_elements) / len(garment_elements)
            confidence_factors.append(avg_garment_confidence * 0.4)
        
        # Confianza de materiales (30% peso)
        materials = fabric_properties.get('materials', {})
        if materials:
            avg_material_confidence = sum(mat['confidence'] for mat in materials.values()) / len(materials)
            confidence_factors.append(avg_material_confidence * 0.3)
        
        # Confianza de variaciones de talla (20% peso)
        if size_variations:
            avg_size_confidence = sum(var['confidence'] for var in size_variations) / len(size_variations)
            confidence_factors.append(avg_size_confidence * 0.2)
        
        # Confianza de accesibilidad (10% peso)
        if accessibility_features:
            avg_accessibility_confidence = sum(feat['confidence'] for feat in accessibility_features) / len(accessibility_features)
            confidence_factors.append(avg_accessibility_confidence * 0.1)
        
        return sum(confidence_factors) if confidence_factors else 0.0
    
    def _collect_validation_sources(self, fabric_properties: Dict[str, Any], garment_elements: List[Dict[str, Any]]) -> List[str]:
        """Recopilar fuentes de validación utilizadas"""
        sources = set()
        
        # Fuentes de materiales
        for material in fabric_properties.get('materials', {}).values():
            sources.update(material.get('validation_sources', []))
        
        # Fuentes de elementos de prenda
        for element in garment_elements:
            for category_info in element.get('detected_elements', []):
                for elem in category_info['elements']:
                    if elem.get('validated'):
                        sources.add('contextual_validation')
        
        return list(sources)
    
    def _detect_false_positives(self, gltf_data: Dict[str, Any], garment_elements: List[Dict[str, Any]], fabric_properties: Dict[str, Any]) -> List[str]:
        """Detectar posibles falsos positivos"""
        flags = []
        
        # Verificar si el archivo parece ser de moda/textil
        generator = gltf_data.get('asset', {}).get('generator', '').lower()
        if not any(fashion_indicator in generator for fashion_indicator in ['clo', 'fashion', 'textile', 'garment']):
            flags.append('generator_not_fashion_specific')
        
        # Verificar coherencia de elementos detectados
        total_elements = sum(len(elem.get('detected_elements', [])) for elem in garment_elements)
        if total_elements > len(gltf_data.get('meshes', [])) * 0.8:
            flags.append('too_many_garment_elements_detected')
        
        # Verificar coherencia de materiales
        materials_count = len(fabric_properties.get('materials', {}))
        gltf_materials_count = len(gltf_data.get('materials', []))
        if materials_count > gltf_materials_count:
            flags.append('material_count_inconsistency')
        
        return flags

def main():
    """Función principal para testing"""
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python analyzer_gltf_improved.py <archivo.gltf>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    analyzer = ImprovedGLTFAnalyzer()
    
    try:
        result = analyzer.analyze_gltf_file(file_path)
        
        print(f"\n🎯 ANÁLISIS GLTF MEJORADO")
        print(f"📁 Archivo: {result.file_path}")
        print(f"📊 GLTF v{result.gltf_version} - {result.generator}")
        print(f"🎯 Confianza general: {result.confidence_score:.2f}")
        
        print(f"\n🔍 ELEMENTOS DE PRENDA ({len(result.garment_elements)}):")
        for element in result.garment_elements:
            print(f"  • {element['mesh_name']} (confianza: {element['confidence_score']:.2f})")
            for category in element['detected_elements']:
                print(f"    - {category['category']}: {len(category['elements'])} elementos")
        
        print(f"\n🧵 PROPIEDADES DE TELA ({len(result.fabric_properties.get('materials', {}))}):")
        for mat_name, mat_info in result.fabric_properties.get('materials', {}).items():
            print(f"  • {mat_name} (confianza: {mat_info['confidence']:.2f})")
            if 'fabric_type' in mat_info['properties']:
                print(f"    - Tipo: {mat_info['properties']['fabric_type']}")
        
        print(f"\n📏 VARIACIONES DE TALLA ({len(result.size_variations)}):")
        for variation in result.size_variations:
            print(f"  • {variation['node_name']} (confianza: {variation['confidence']:.2f})")
        
        print(f"\n♿ ACCESIBILIDAD ({len(result.accessibility_features)}):")
        for feature in result.accessibility_features:
            print(f"  • {feature['element']} - Score: {feature['accessibility_score']:.1f}")
        
        print(f"\n✅ FUENTES DE VALIDACIÓN:")
        for source in result.validation_sources:
            print(f"  • {source}")
        
        if result.false_positive_flags:
            print(f"\n⚠️ ALERTAS DE FALSOS POSITIVOS:")
            for flag in result.false_positive_flags:
                print(f"  • {flag}")
        
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()