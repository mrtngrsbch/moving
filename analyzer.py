#!/usr/bin/env python3
"""
Moving Accessibility Analyzer - Python Version
Análisis avanzado de archivos de diseño para inclusividad y accesibilidad

Características:
- Análisis profundo de archivos .zprj, .zpac, .gltf y .obj
- Detección inteligente de patrones de inclusividad
- Métricas específicas para accesibilidad
- Recomendaciones personalizadas
- Soporte para múltiples formatos y estructuras
"""

import os
import sys
import zipfile
import xml.etree.ElementTree as ET
import json
import re
import struct
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SizingMetrics:
    """Métricas de tallas y medidas"""
    size_range: str
    adaptability: str
    inclusive_design: bool
    detected_sizes: List[str]
    grading_system: bool
    size_count: int

@dataclass
class FabricMetrics:
    """Métricas de materiales y telas"""
    elasticity: str
    comfort: str
    materials_found: List[str]
    stretch_properties: bool
    weight_info: str
    breathability: str
    texture_quality: str

@dataclass
class ClosureMetrics:
    """Métricas de cierres y elementos de accesibilidad"""
    buttonhole_size: str
    zipper_accessibility: str
    closure_types: List[str]
    adaptive_features: List[str]
    ease_of_use: str

@dataclass
class ComfortMetrics:
    """Métricas de comodidad y accesibilidad"""
    mobility: str
    sensory_friendly: str
    adaptive_features: List[str]
    ergonomic_design: bool
    universal_design: bool

@dataclass
class HumanValidationItem:
    """Item específico que requiere validación humana"""
    category: str
    priority: str  # 'ALTA', 'MEDIA', 'BAJA'
    finding: str
    validation_needed: str
    estimated_time_minutes: int
    expert_type: str  # 'diseñador', 'accesibilidad', 'materiales', etc.

@dataclass
class ScreeningReport:
    """Reporte de screening para validación humana"""
    automated_findings: Dict[str, Any]
    confidence_levels: Dict[str, float]  # 0.0 - 1.0
    validation_checklist: List[HumanValidationItem]
    priority_areas: List[str]
    estimated_validation_time: int
    recommended_experts: List[str]
    risk_flags: List[str]

@dataclass
class AnalysisResults:
    """Resultados completos del análisis"""
    file_type: str
    status: str
    file_size_mb: float
    processing_time: float
    inclusivity_score: int
    accessibility_score: int
    sustainability_score: int
    sizing: SizingMetrics
    fabrics: FabricMetrics
    closures: ClosureMetrics
    comfort: ComfortMetrics
    recommendations: List[str]
    technical_details: Dict[str, Any]
    raw_data_summary: Dict[str, Any]
    screening_report: ScreeningReport

class CLO3DAnalyzer:
    """Analizador avanzado de archivos de diseño para inclusividad y accesibilidad"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.start_time = None
        self.file_hash = None
        
        # Patrones de búsqueda mejorados
        self.size_patterns = {
            'standard_sizes': r'\b(XXS|XS|S|M|L|XL|XXL|XXXL|XXXXL)\b',
            'numeric_sizes': r'\b(0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])\b',
            'measurements': r'\d+\.?\d*\s*(cm|mm|inch|in|")',
            'size_declarations': r'size[s]?\s*[:=]\s*[\w\d]+',
            'talla_declarations': r'talla[s]?\s*[:=]\s*[\w\d]+',
        }
        
        self.material_patterns = {
            'natural_fibers': {
                'cotton': r'\b(cotton|algodón|coton)\b',
                'wool': r'\b(wool|lana|laine)\b',
                'silk': r'\b(silk|seda|soie)\b',
                'linen': r'\b(linen|lino|lin)\b',
            },
            'synthetic_fibers': {
                'polyester': r'\b(polyester|poliéster)\b',
                'nylon': r'\b(nylon|nilón)\b',
                'acrylic': r'\b(acrylic|acrílico)\b',
            },
            'stretch_materials': {
                'elastane': r'\b(elastane|elastano|spandex|lycra)\b',
                'elastic': r'\b(elastic|elástico)\b',
                'stretch': r'\b(stretch|estirable)\b'
            }
        }
        
        self.closure_patterns = {
            'buttons': r'\b(button|botón|bouton|btn)\b',
            'zippers': r'\b(zipper|cremallera|fermeture|zip)\b',
            'velcro': r'\b(velcro|hook|loop|gancho)\b',
            'snaps': r'\b(snap|broche|pression)\b',
            'ties': r'\b(tie|lazo|cordón|lien)\b',
            'magnetic': r'\b(magnetic|magnético|magnétique)\b',
        }
    
    def analyze_file(self, file_path: str) -> AnalysisResults:
        """Analizar archivo de diseño con análisis completo y detallado"""
        self.start_time = datetime.now()
        
        logger.info(f"🔍 Iniciando análisis de archivo: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        # Información básica del archivo
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        file_ext = Path(file_path).suffix.lower()
        
        # Calcular hash del archivo para identificación única
        self.file_hash = self._calculate_file_hash(file_path)
        
        logger.info(f"📏 Tamaño del archivo: {file_size_mb:.2f} MB")
        logger.info(f"🔑 Hash del archivo: {self.file_hash[:16]}...")
        
        # Análisis según tipo de archivo
        if file_ext == '.zprj':
            results = self._analyze_zprj(file_path, file_size_mb)
        elif file_ext == '.zpac':
            results = self._analyze_zpac(file_path, file_size_mb)
        elif file_ext == '.gltf':
            results = self._analyze_gltf(file_path, file_size_mb)
        elif file_ext == '.obj':
            results = self._analyze_obj(file_path, file_size_mb)
        else:
            raise ValueError(f"Formato de archivo no soportado: {file_ext}. Formatos soportados: .zprj, .zpac, .gltf, .obj")
        
        # Calcular tiempo de procesamiento
        processing_time = (datetime.now() - self.start_time).total_seconds()
        results.processing_time = processing_time
        
        logger.info(f"✅ Análisis completado en {processing_time:.2f} segundos")
        
        return results
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calcular hash SHA-256 del archivo"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _analyze_gltf(self, file_path: str, file_size_mb: float) -> AnalysisResults:
        """Analizar archivo GLTF usando el analizador mejorado si está disponible"""
        logger.info("🎯 Analizando modelo GLTF")
        
        try:
            # Intentar usar el analizador GLTF mejorado
            from analyzer_gltf_improved import ImprovedGLTFAnalyzer
            
            gltf_analyzer = ImprovedGLTFAnalyzer()
            gltf_result = gltf_analyzer.analyze_gltf_file(file_path)
            
            # Convertir resultado GLTF a formato estándar
            return self._convert_gltf_result_to_standard(gltf_result, file_size_mb)
            
        except ImportError:
            logger.warning("Analizador GLTF mejorado no disponible, usando análisis básico")
            return self._analyze_gltf_basic(file_path, file_size_mb)
    
    def _convert_gltf_result_to_standard(self, gltf_result, file_size_mb: float) -> AnalysisResults:
        """Convertir resultado GLTF mejorado al formato estándar"""
        
        # Crear métricas de tallas
        size_variations = gltf_result.size_variations
        sizing_metrics = SizingMetrics(
            size_range=f"{len(size_variations)} variaciones detectadas" if size_variations else "Modelo único",
            adaptability="Alta" if len(size_variations) >= 3 else "Media" if len(size_variations) >= 1 else "Limitada",
            inclusive_design=len(size_variations) >= 3,
            detected_sizes=[var['node_name'] for var in size_variations],
            grading_system=any('scale' in str(var) for var in size_variations),
            size_count=len(size_variations)
        )
        
        # Crear métricas de materiales
        materials = gltf_result.fabric_properties.get('materials', {})
        fabric_metrics = FabricMetrics(
            elasticity="Propiedades detectadas" if materials else "Sin datos específicos",
            comfort="Análisis basado en propiedades PBR",
            materials_found=[name for name in materials.keys()][:10],
            stretch_properties=any('stretch' in str(mat) for mat in materials.values()),
            weight_info="Propiedades virtuales GLTF",
            breathability="Análisis basado en clasificación de materiales",
            texture_quality="Texturas analizadas contextualmente"
        )
        
        # Crear métricas de cierres
        closure_elements = []
        for element in gltf_result.garment_elements:
            for category in element.get('detected_elements', []):
                if category['category'] == 'closures':
                    closure_elements.extend([elem['element'] for elem in category['elements']])
        
        closure_metrics = ClosureMetrics(
            buttonhole_size=f"{len([c for c in closure_elements if 'button' in c])} botones detectados",
            zipper_accessibility=f"{len([c for c in closure_elements if 'zipper' in c])} cremalleras detectadas",
            closure_types=list(set(closure_elements)),
            adaptive_features=[],
            ease_of_use="Evaluado según tipos de cierre detectados"
        )
        
        # Crear métricas de comodidad
        comfort_metrics = ComfortMetrics(
            mobility="Basado en análisis de materiales",
            sensory_friendly="Evaluado por propiedades de superficie",
            adaptive_features=[feat['element'] for feat in gltf_result.accessibility_features],
            ergonomic_design=len(gltf_result.accessibility_features) > 0,
            universal_design=gltf_result.confidence_score > 0.7
        )
        
        # Calcular puntuaciones
        inclusivity_score = min(100, int(gltf_result.confidence_score * 60 + len(size_variations) * 10))
        accessibility_score = min(100, int(len(gltf_result.accessibility_features) * 15 + gltf_result.confidence_score * 40))
        sustainability_score = min(100, int(len(materials) * 5 + gltf_result.confidence_score * 50))
        
        # Generar recomendaciones
        recommendations = self._generate_gltf_recommendations(gltf_result)
        
        # Crear reporte de screening
        screening_report = self._create_gltf_screening_report(gltf_result)
        
        return AnalysisResults(
            file_type=f"GLTF 3D Model (v{gltf_result.gltf_version})",
            status="Análisis GLTF mejorado completado",
            file_size_mb=file_size_mb,
            processing_time=0.0,
            inclusivity_score=inclusivity_score,
            accessibility_score=accessibility_score,
            sustainability_score=sustainability_score,
            sizing=sizing_metrics,
            fabrics=fabric_metrics,
            closures=closure_metrics,
            comfort=comfort_metrics,
            recommendations=recommendations,
            technical_details={
                'gltf_version': gltf_result.gltf_version,
                'generator': gltf_result.generator,
                'confidence_score': gltf_result.confidence_score,
                'validation_sources': gltf_result.validation_sources,
                'false_positive_flags': gltf_result.false_positive_flags,
                'file_hash': self.file_hash,
                'analysis_timestamp': datetime.now().isoformat()
            },
            raw_data_summary={
                'garment_elements': len(gltf_result.garment_elements),
                'materials_analyzed': len(materials),
                'size_variations': len(size_variations),
                'accessibility_features': len(gltf_result.accessibility_features)
            },
            screening_report=screening_report
        )
    
    def _generate_gltf_recommendations(self, gltf_result) -> List[str]:
        """Generar recomendaciones basadas en análisis GLTF"""
        recommendations = []
        
        if gltf_result.confidence_score < 0.5:
            recommendations.append("Considerar validación manual adicional debido a baja confianza del análisis automático")
        
        if len(gltf_result.size_variations) == 0:
            recommendations.append("Considerar crear variaciones de talla para mejorar inclusividad")
        
        if len(gltf_result.accessibility_features) < 3:
            recommendations.append("Evaluar agregar más características de accesibilidad (cierres fáciles, materiales suaves)")
        
        if gltf_result.false_positive_flags:
            recommendations.append("Revisar manualmente las alertas de falsos positivos detectadas")
        
        materials_count = len(gltf_result.fabric_properties.get('materials', {}))
        if materials_count > 50:
            recommendations.append("Considerar simplificar la variedad de materiales para mejorar sostenibilidad")
        
        return recommendations[:6]
    
    def _create_gltf_screening_report(self, gltf_result) -> ScreeningReport:
        """Crear reporte de screening para análisis GLTF"""
        
        validation_checklist = []
        
        # Items de validación basados en elementos detectados
        for element in gltf_result.garment_elements:
            if element['confidence_score'] < 0.8:
                validation_checklist.append(HumanValidationItem(
                    category="elementos_prenda",
                    priority="MEDIA",
                    finding=f"Elemento {element['mesh_name']} detectado con confianza {element['confidence_score']:.2f}",
                    validation_needed="Verificar manualmente si es realmente un elemento de prenda",
                    estimated_time_minutes=5,
                    expert_type="diseñador"
                ))
        
        # Items de validación para materiales
        materials = gltf_result.fabric_properties.get('materials', {})
        for mat_name, mat_info in materials.items():
            if mat_info['confidence'] < 0.7:
                validation_checklist.append(HumanValidationItem(
                    category="materiales",
                    priority="BAJA",
                    finding=f"Material {mat_name} clasificado con confianza {mat_info['confidence']:.2f}",
                    validation_needed="Verificar propiedades del material y clasificación",
                    estimated_time_minutes=3,
                    expert_type="materiales"
                ))
        
        # Calcular tiempo total
        total_time = sum(item.estimated_time_minutes for item in validation_checklist)
        
        return ScreeningReport(
            automated_findings={
                'garment_elements': len(gltf_result.garment_elements),
                'materials': len(materials),
                'confidence_score': gltf_result.confidence_score
            },
            confidence_levels={
                'overall_analysis': gltf_result.confidence_score,
                'garment_detection': sum(elem['confidence_score'] for elem in gltf_result.garment_elements) / max(len(gltf_result.garment_elements), 1),
                'material_analysis': sum(mat['confidence'] for mat in materials.values()) / max(len(materials), 1)
            },
            validation_checklist=validation_checklist,
            priority_areas=['elementos_prenda', 'materiales'] if validation_checklist else [],
            estimated_validation_time=total_time,
            recommended_experts=['diseñador', 'materiales'],
            risk_flags=gltf_result.false_positive_flags
        )
    
    def _analyze_gltf_basic(self, file_path: str, file_size_mb: float) -> AnalysisResults:
        """Análisis básico de GLTF cuando el analizador mejorado no está disponible"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                gltf_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Archivo GLTF inválido: {e}")
        
        # Análisis básico
        asset_info = gltf_data.get('asset', {})
        meshes_count = len(gltf_data.get('meshes', []))
        materials_count = len(gltf_data.get('materials', []))
        
        # Crear métricas básicas
        sizing_metrics = SizingMetrics(
            size_range="Análisis básico - modelo único",
            adaptability="No determinada",
            inclusive_design=False,
            detected_sizes=[],
            grading_system=False,
            size_count=0
        )
        
        fabric_metrics = FabricMetrics(
            elasticity="Análisis básico - propiedades no determinadas",
            comfort="Requiere análisis avanzado",
            materials_found=[f"material_{i}" for i in range(min(materials_count, 5))],
            stretch_properties=False,
            weight_info="No disponible en análisis básico",
            breathability="No determinada",
            texture_quality="Análisis básico"
        )
        
        closure_metrics = ClosureMetrics(
            buttonhole_size="No detectado en análisis básico",
            zipper_accessibility="Requiere análisis avanzado",
            closure_types=[],
            adaptive_features=[],
            ease_of_use="No determinado"
        )
        
        comfort_metrics = ComfortMetrics(
            mobility="No determinada",
            sensory_friendly="Requiere análisis avanzado",
            adaptive_features=[],
            ergonomic_design=False,
            universal_design=False
        )
        
        # Puntuaciones básicas
        inclusivity_score = 40  # Puntuación baja por análisis básico
        accessibility_score = 30
        sustainability_score = 35
        
        # Recomendaciones básicas
        recommendations = [
            "Usar analizador GLTF mejorado para análisis más preciso",
            "Validación manual recomendada para análisis básico",
            "Considerar usar formato .zpac para mejor análisis"
        ]
        
        # Screening report básico
        screening_report = ScreeningReport(
            automated_findings={'analysis_type': 'basic', 'meshes': meshes_count, 'materials': materials_count},
            confidence_levels={'overall_analysis': 0.3},
            validation_checklist=[
                HumanValidationItem(
                    category="análisis_completo",
                    priority="ALTA",
                    finding="Análisis básico realizado - requiere validación completa",
                    validation_needed="Realizar análisis manual completo del archivo GLTF",
                    estimated_time_minutes=30,
                    expert_type="diseñador"
                )
            ],
            priority_areas=['análisis_completo'],
            estimated_validation_time=30,
            recommended_experts=['diseñador', 'accesibilidad'],
            risk_flags=['basic_analysis_only']
        )
        
        return AnalysisResults(
            file_type="GLTF 3D Model (análisis básico)",
            status="Análisis básico completado - se recomienda análisis avanzado",
            file_size_mb=file_size_mb,
            processing_time=0.0,
            inclusivity_score=inclusivity_score,
            accessibility_score=accessibility_score,
            sustainability_score=sustainability_score,
            sizing=sizing_metrics,
            fabrics=fabric_metrics,
            closures=closure_metrics,
            comfort=comfort_metrics,
            recommendations=recommendations,
            technical_details={
                'analysis_type': 'basic',
                'gltf_version': asset_info.get('version', 'unknown'),
                'generator': asset_info.get('generator', 'unknown'),
                'file_hash': self.file_hash,
                'analysis_timestamp': datetime.now().isoformat()
            },
            raw_data_summary={
                'meshes': meshes_count,
                'materials': materials_count,
                'analysis_type': 'basic'
            },
            screening_report=screening_report
        )
    
    def _analyze_zprj(self, file_path: str, file_size_mb: float) -> AnalysisResults:
        """Análisis básico de archivos .zprj"""
        # Implementación básica para compatibilidad
        return self._create_basic_results("CLO3D Project (.zprj)", file_size_mb)
    
    def _analyze_zpac(self, file_path: str, file_size_mb: float) -> AnalysisResults:
        """Análisis básico de archivos .zpac"""
        # Implementación básica para compatibilidad
        return self._create_basic_results("CLO3D Package (.zpac)", file_size_mb)
    
    def _analyze_obj(self, file_path: str, file_size_mb: float) -> AnalysisResults:
        """Análisis básico de archivos .obj"""
        # Implementación básica para compatibilidad
        return self._create_basic_results("Wavefront OBJ (.obj)", file_size_mb)
    
    def _create_basic_results(self, file_type: str, file_size_mb: float) -> AnalysisResults:
        """Crear resultados básicos para formatos no implementados completamente"""
        
        sizing_metrics = SizingMetrics(
            size_range="Análisis básico - requiere implementación específica",
            adaptability="No determinada",
            inclusive_design=False,
            detected_sizes=[],
            grading_system=False,
            size_count=0
        )
        
        fabric_metrics = FabricMetrics(
            elasticity="Requiere análisis específico del formato",
            comfort="No determinado",
            materials_found=[],
            stretch_properties=False,
            weight_info="No disponible",
            breathability="No determinada",
            texture_quality="Análisis básico"
        )
        
        closure_metrics = ClosureMetrics(
            buttonhole_size="No detectado",
            zipper_accessibility="Requiere análisis específico",
            closure_types=[],
            adaptive_features=[],
            ease_of_use="No determinado"
        )
        
        comfort_metrics = ComfortMetrics(
            mobility="No determinada",
            sensory_friendly="Requiere análisis específico",
            adaptive_features=[],
            ergonomic_design=False,
            universal_design=False
        )
        
        screening_report = ScreeningReport(
            automated_findings={'analysis_type': 'basic', 'file_type': file_type},
            confidence_levels={'overall_analysis': 0.2},
            validation_checklist=[
                HumanValidationItem(
                    category="análisis_manual",
                    priority="ALTA",
                    finding=f"Formato {file_type} requiere análisis manual completo",
                    validation_needed="Realizar análisis manual del archivo",
                    estimated_time_minutes=45,
                    expert_type="diseñador"
                )
            ],
            priority_areas=['análisis_manual'],
            estimated_validation_time=45,
            recommended_experts=['diseñador', 'accesibilidad', 'materiales'],
            risk_flags=['format_not_fully_supported']
        )
        
        return AnalysisResults(
            file_type=file_type,
            status="Análisis básico - requiere implementación específica del formato",
            file_size_mb=file_size_mb,
            processing_time=0.0,
            inclusivity_score=25,
            accessibility_score=20,
            sustainability_score=30,
            sizing=sizing_metrics,
            fabrics=fabric_metrics,
            closures=closure_metrics,
            comfort=comfort_metrics,
            recommendations=[
                "Implementar analizador específico para este formato",
                "Realizar análisis manual completo",
                "Considerar convertir a formato GLTF para mejor análisis"
            ],
            technical_details={
                'analysis_type': 'basic',
                'file_hash': self.file_hash,
                'analysis_timestamp': datetime.now().isoformat()
            },
            raw_data_summary={'analysis_type': 'basic'},
            screening_report=screening_report
        )

def main():
    """Función principal para testing"""
    import sys
    
    if len(sys.argv) != 2:
        print("Uso: python analyzer.py <archivo>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    analyzer = CLO3DAnalyzer(debug=True)
    
    try:
        result = analyzer.analyze_file(file_path)
        
        print(f"\n🎯 ANÁLISIS COMPLETADO")
        print(f"📁 Archivo: {file_path}")
        print(f"📊 Tipo: {result.file_type}")
        print(f"🎯 Inclusividad: {result.inclusivity_score}/100")
        print(f"♿ Accesibilidad: {result.accessibility_score}/100")
        print(f"🌱 Sostenibilidad: {result.sustainability_score}/100")
        
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()