#!/usr/bin/env python3
"""
Moving Accessibility Analyzer - Analizador Principal
Análisis avanzado de archivos de diseño para inclusividad y accesibilidad
"""

import os
import sys
import json
import re
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
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
    priority: str
    finding: str
    validation_needed: str
    estimated_time_minutes: int
    expert_type: str

@dataclass
class ScreeningReport:
    """Reporte de screening para validación humana"""
    automated_findings: Dict[str, Any]
    confidence_levels: Dict[str, float]
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
    """Analizador principal de archivos de diseño"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.start_time = None
        self.file_hash = None
    
    def analyze_file(self, file_path: str) -> AnalysisResults:
        """Analizar archivo de diseño"""
        self.start_time = datetime.now()
        
        logger.info(f"🔍 Iniciando análisis: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        file_ext = Path(file_path).suffix.lower()
        
        self.file_hash = self._calculate_file_hash(file_path)
        
        # Análisis según tipo de archivo
        if file_ext == '.gltf':
            results = self._analyze_gltf(file_path, file_size_mb)
        else:
            results = self._analyze_other_format(file_path, file_size_mb, file_ext)
        
        # Calcular tiempo de procesamiento
        processing_time = (datetime.now() - self.start_time).total_seconds()
        results.processing_time = processing_time
        
        logger.info(f"✅ Análisis completado en {processing_time:.2f}s")
        return results
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calcular hash SHA-256 del archivo"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _analyze_gltf(self, file_path: str, file_size_mb: float) -> AnalysisResults:
        """Analizar archivo GLTF"""
        try:
            # Intentar usar analizador GLTF mejorado
            from analyzer_gltf_improved import ImprovedGLTFAnalyzer
            
            gltf_analyzer = ImprovedGLTFAnalyzer()
            gltf_result = gltf_analyzer.analyze_gltf_file(file_path)
            
            return self._convert_gltf_result(gltf_result, file_size_mb)
            
        except ImportError:
            logger.warning("Analizador GLTF mejorado no disponible")
            return self._analyze_gltf_basic(file_path, file_size_mb)
    
    def _convert_gltf_result(self, gltf_result, file_size_mb: float) -> AnalysisResults:
        """Convertir resultado GLTF al formato estándar"""
        
        # Métricas de tallas
        size_variations = gltf_result.size_variations
        sizing_metrics = SizingMetrics(
            size_range=f"{len(size_variations)} variaciones" if size_variations else "Modelo único",
            adaptability="Alta" if len(size_variations) >= 3 else "Media" if len(size_variations) >= 1 else "Limitada",
            inclusive_design=len(size_variations) >= 3,
            detected_sizes=[var.get('node_name', '') for var in size_variations],
            grading_system=any('scale' in str(var) for var in size_variations),
            size_count=len(size_variations)
        )
        
        # Métricas de materiales
        materials = gltf_result.fabric_properties.get('materials', {})
        fabric_metrics = FabricMetrics(
            elasticity="Propiedades GLTF analizadas",
            comfort="Basado en análisis PBR",
            materials_found=list(materials.keys())[:10],
            stretch_properties=any('stretch' in str(mat) for mat in materials.values()),
            weight_info="Propiedades virtuales",
            breathability="Análisis contextual",
            texture_quality="Texturas validadas"
        )
        
        # Métricas de cierres
        closure_elements = []
        for element in gltf_result.garment_elements:
            for category in element.get('detected_elements', []):
                if category['category'] == 'closures':
                    closure_elements.extend([elem['element'] for elem in category['elements']])
        
        closure_metrics = ClosureMetrics(
            buttonhole_size=f"{len([c for c in closure_elements if 'button' in c])} botones",
            zipper_accessibility=f"{len([c for c in closure_elements if 'zipper' in c])} cremalleras",
            closure_types=list(set(closure_elements)),
            adaptive_features=[],
            ease_of_use="Evaluado por tipos detectados"
        )
        
        # Métricas de comodidad
        comfort_metrics = ComfortMetrics(
            mobility="Basado en materiales",
            sensory_friendly="Evaluado por superficie",
            adaptive_features=[feat['element'] for feat in gltf_result.accessibility_features],
            ergonomic_design=len(gltf_result.accessibility_features) > 0,
            universal_design=gltf_result.confidence_score > 0.7
        )
        
        # Puntuaciones
        inclusivity_score = min(100, int(gltf_result.confidence_score * 60 + len(size_variations) * 10))
        accessibility_score = min(100, int(len(gltf_result.accessibility_features) * 15 + gltf_result.confidence_score * 40))
        sustainability_score = min(100, int(len(materials) * 5 + gltf_result.confidence_score * 50))
        
        # Recomendaciones
        recommendations = self._generate_recommendations(gltf_result)
        
        # Screening report
        screening_report = self._create_screening_report(gltf_result)
        
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
                'file_hash': self.file_hash
            },
            raw_data_summary={
                'garment_elements': len(gltf_result.garment_elements),
                'materials': len(materials),
                'size_variations': len(size_variations)
            },
            screening_report=screening_report
        )
    
    def _analyze_gltf_basic(self, file_path: str, file_size_mb: float) -> AnalysisResults:
        """Análisis básico de GLTF"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                gltf_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Archivo GLTF inválido: {e}")
        
        return self._create_basic_results("GLTF 3D Model (análisis básico)", file_size_mb)
    
    def _analyze_other_format(self, file_path: str, file_size_mb: float, file_ext: str) -> AnalysisResults:
        """Análisis de otros formatos"""
        format_names = {
            '.zprj': 'CLO3D Project',
            '.zpac': 'CLO3D Package',
            '.obj': 'Wavefront OBJ'
        }
        
        file_type = format_names.get(file_ext, f"Archivo {file_ext}")
        return self._create_basic_results(file_type, file_size_mb)
    
    def _create_basic_results(self, file_type: str, file_size_mb: float) -> AnalysisResults:
        """Crear resultados básicos"""
        
        sizing_metrics = SizingMetrics(
            size_range="Análisis básico",
            adaptability="No determinada",
            inclusive_design=False,
            detected_sizes=[],
            grading_system=False,
            size_count=0
        )
        
        fabric_metrics = FabricMetrics(
            elasticity="Requiere análisis específico",
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
            automated_findings={'analysis_type': 'basic'},
            confidence_levels={'overall_analysis': 0.3},
            validation_checklist=[
                HumanValidationItem(
                    category="análisis_manual",
                    priority="ALTA",
                    finding="Requiere análisis manual completo",
                    validation_needed="Análisis manual del archivo",
                    estimated_time_minutes=30,
                    expert_type="diseñador"
                )
            ],
            priority_areas=['análisis_manual'],
            estimated_validation_time=30,
            recommended_experts=['diseñador'],
            risk_flags=['basic_analysis_only']
        )
        
        return AnalysisResults(
            file_type=file_type,
            status="Análisis básico completado",
            file_size_mb=file_size_mb,
            processing_time=0.0,
            inclusivity_score=30,
            accessibility_score=25,
            sustainability_score=35,
            sizing=sizing_metrics,
            fabrics=fabric_metrics,
            closures=closure_metrics,
            comfort=comfort_metrics,
            recommendations=[
                "Implementar analizador específico para mejor análisis",
                "Realizar validación manual completa",
                "Considerar formato GLTF para análisis avanzado"
            ],
            technical_details={
                'analysis_type': 'basic',
                'file_hash': self.file_hash
            },
            raw_data_summary={'analysis_type': 'basic'},
            screening_report=screening_report
        )
    
    def _generate_recommendations(self, gltf_result) -> List[str]:
        """Generar recomendaciones"""
        recommendations = []
        
        if gltf_result.confidence_score < 0.5:
            recommendations.append("Validación manual recomendada por baja confianza")
        
        if len(gltf_result.size_variations) == 0:
            recommendations.append("Considerar variaciones de talla para inclusividad")
        
        if len(gltf_result.accessibility_features) < 3:
            recommendations.append("Evaluar más características de accesibilidad")
        
        return recommendations[:5]
    
    def _create_screening_report(self, gltf_result) -> ScreeningReport:
        """Crear reporte de screening"""
        
        validation_checklist = []
        
        # Validación de elementos con baja confianza
        for element in gltf_result.garment_elements:
            if element['confidence_score'] < 0.8:
                validation_checklist.append(HumanValidationItem(
                    category="elementos_prenda",
                    priority="MEDIA",
                    finding=f"Elemento {element['mesh_name']} con confianza {element['confidence_score']:.2f}",
                    validation_needed="Verificar elemento de prenda",
                    estimated_time_minutes=5,
                    expert_type="diseñador"
                ))
        
        total_time = sum(item.estimated_time_minutes for item in validation_checklist)
        
        return ScreeningReport(
            automated_findings={
                'garment_elements': len(gltf_result.garment_elements),
                'confidence_score': gltf_result.confidence_score
            },
            confidence_levels={
                'overall_analysis': gltf_result.confidence_score
            },
            validation_checklist=validation_checklist,
            priority_areas=['elementos_prenda'] if validation_checklist else [],
            estimated_validation_time=max(total_time, 10),
            recommended_experts=['diseñador'],
            risk_flags=gltf_result.false_positive_flags
        )

def main():
    """Función principal para testing"""
    if len(sys.argv) != 2:
        print("Uso: python analyzer_main.py <archivo>")
        sys.exit(1)
    
    analyzer = CLO3DAnalyzer(debug=True)
    result = analyzer.analyze_file(sys.argv[1])
    
    print(f"\n🎯 ANÁLISIS COMPLETADO")
    print(f"📁 Archivo: {sys.argv[1]}")
    print(f"📊 Tipo: {result.file_type}")
    print(f"🎯 Inclusividad: {result.inclusivity_score}/100")
    print(f"♿ Accesibilidad: {result.accessibility_score}/100")
    print(f"🌱 Sostenibilidad: {result.sustainability_score}/100")

if __name__ == "__main__":
    main()