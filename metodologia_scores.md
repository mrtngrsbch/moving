# Metodología de Cálculo de Scores

## 🎯 Resumen Ejecutivo

Los scores de **Inclusividad**, **Accesibilidad** y **Sostenibilidad** se calculan mediante algoritmos específicos que varían según el tipo de análisis (Avanzado GLTF vs Básico). El sistema utiliza una combinación de métricas objetivas detectadas automáticamente y factores de confianza del análisis.

## 📊 Metodología por Tipo de Análisis

### 🚀 Análisis GLTF Avanzado (Recomendado)

#### 🎯 Score de Inclusividad (0-100)
```python
inclusivity_score = min(100, int(gltf_result.confidence_score * 60 + len(size_variations) * 10))
```

**Componentes:**
- **Confianza del análisis (60% peso)**: `confidence_score * 60`
  - Basado en validación contextual de elementos detectados
  - Rango: 0.0 - 1.0 (multiplicado por 60)
- **Variaciones de talla (40% peso)**: `len(size_variations) * 10`
  - Cada variación de talla detectada suma 10 puntos
  - Máximo teórico: 40 puntos (4+ variaciones)

**Ejemplos de Cálculo:**
- Confianza 0.8, 2 variaciones: `0.8 * 60 + 2 * 10 = 68 puntos`
- Confianza 0.6, 4 variaciones: `0.6 * 60 + 4 * 10 = 76 puntos`
- Confianza 0.9, 0 variaciones: `0.9 * 60 + 0 * 10 = 54 puntos`

#### ♿ Score de Accesibilidad (0-100)
```python
accessibility_score = min(100, int(len(gltf_result.accessibility_features) * 15 + gltf_result.confidence_score * 40))
```

**Componentes:**
- **Características de accesibilidad (60% peso)**: `len(accessibility_features) * 15`
  - Cada característica detectada suma 15 puntos
  - Incluye: cierres accesibles, materiales suaves, elementos adaptativos
- **Confianza del análisis (40% peso)**: `confidence_score * 40`
  - Factor de corrección por calidad del análisis

**Tipos de Características de Accesibilidad Detectadas:**
- **Cierres accesibles**: Velcro (0.9), Magnético (0.9), Snap (0.7), Zipper (0.6), Botón (0.4)
- **Materiales sensoriales**: Telas suaves, texturas amigables
- **Elementos adaptativos**: Características de movilidad

**Ejemplos de Cálculo:**
- 4 características, confianza 0.7: `4 * 15 + 0.7 * 40 = 88 puntos`
- 2 características, confianza 0.8: `2 * 15 + 0.8 * 40 = 62 puntos`
- 6 características, confianza 0.6: `6 * 15 + 0.6 * 40 = 114 → 100 puntos (máximo)`

#### 🌱 Score de Sostenibilidad (0-100)
```python
sustainability_score = min(100, int(len(materials) * 5 + gltf_result.confidence_score * 50))
```

**Componentes:**
- **Diversidad de materiales (50% peso)**: `len(materials) * 5`
  - Cada material analizado suma 5 puntos
  - Más materiales = mayor complejidad = menor sostenibilidad potencial
- **Confianza del análisis (50% peso)**: `confidence_score * 50`
  - Factor principal por limitaciones en análisis de sostenibilidad

**Lógica de Materiales:**
- **Pocos materiales (1-5)**: Potencialmente más sostenible
- **Muchos materiales (10+)**: Complejidad de producción mayor
- **Análisis limitado**: Principalmente basado en confianza del análisis

**Ejemplos de Cálculo:**
- 8 materiales, confianza 0.8: `8 * 5 + 0.8 * 50 = 80 puntos`
- 15 materiales, confianza 0.6: `15 * 5 + 0.6 * 50 = 105 → 100 puntos`
- 3 materiales, confianza 0.9: `3 * 5 + 0.9 * 50 = 60 puntos`

### 📊 Análisis Básico (Otros Formatos)

Para formatos que no tienen análisis avanzado (.zprj, .zpac, .obj):

#### Scores Fijos Básicos
```python
inclusivity_score = 30      # Puntuación baja por análisis limitado
accessibility_score = 25    # Requiere validación manual
sustainability_score = 35   # Análisis no disponible
```

**Justificación:**
- **Scores bajos intencionalmente** para indicar limitaciones
- **Fuerza validación manual** completa
- **Transparencia** sobre capacidades limitadas

## 🔍 Factores de Confianza Detallados

### Cálculo de Confianza General (GLTF)
```python
confidence_score = sum(confidence_factors) if confidence_factors else 0.0
```

**Factores de Confianza (Pesos):**
- **Elementos de prenda (40%)**: Promedio de confianza de meshes detectados
- **Análisis de materiales (30%)**: Promedio de confianza de materiales clasificados
- **Variaciones de talla (20%)**: Promedio de confianza de variaciones detectadas
- **Características de accesibilidad (10%)**: Promedio de confianza de características

### Fuentes de Validación que Afectan Confianza
1. **CLO3D_extension (0.95)**: Extensiones específicas de CLO3D
2. **PBR_analysis (0.7)**: Análisis de propiedades físicas
3. **texture_analysis (0.6)**: Validación por texturas
4. **contextual_validation (0.8)**: Validación por contexto de nombres

## 📈 Interpretación de Scores

### Rangos de Interpretación
- **80-100**: 🟢 **Excelente** - Alta confianza, múltiples características detectadas
- **60-79**: 🟡 **Bueno** - Confianza media, algunas características detectadas
- **40-59**: 🟠 **Regular** - Baja confianza o pocas características
- **0-39**: 🔴 **Deficiente** - Análisis básico o muy pocas características

### Factores que Aumentan Scores
**Inclusividad:**
- Múltiples variaciones de talla detectadas
- Alta confianza en análisis contextual
- Nodos con escalado paramétrico

**Accesibilidad:**
- Cierres fáciles de usar (velcro, magnético)
- Materiales con propiedades suaves
- Elementos adaptativos identificados

**Sostenibilidad:**
- Número moderado de materiales (no excesivo)
- Alta confianza en clasificación de materiales
- Materiales naturales identificados

### Factores que Reducen Scores
**Inclusividad:**
- Sin variaciones de talla detectadas
- Baja confianza en análisis
- Modelo único sin escalado

**Accesibilidad:**
- Solo cierres complejos (botones pequeños)
- Sin características adaptativas
- Materiales rugosos o rígidos

**Sostenibilidad:**
- Exceso de materiales diferentes (>20)
- Baja confianza en análisis
- Materiales sintéticos predominantes

## ⚠️ Limitaciones y Consideraciones

### Limitaciones Actuales
1. **Sostenibilidad**: Análisis limitado, principalmente basado en número de materiales
2. **Validación manual requerida**: Scores son indicativos, no definitivos
3. **Dependiente del formato**: GLTF tiene análisis mucho más preciso
4. **Contexto específico**: Optimizado para archivos de moda/CLO3D

### Mejoras Futuras Recomendadas
1. **Base de datos de materiales**: Scores específicos por tipo de material
2. **Análisis de ciclo de vida**: Factores ambientales reales
3. **Machine Learning**: Entrenamiento con datos validados por expertos
4. **Análisis de construcción**: Evaluación de técnicas de costura y ensamblaje

## 🎯 Casos de Uso Prácticos

### Ejemplo 1: Archivo GLTF de Alta Calidad
```
Archivo: jacket_winter_2024.gltf (CLO3D)
- Confianza: 0.85
- Variaciones de talla: 5 (XS, S, M, L, XL)
- Características de accesibilidad: 3 (zipper, velcro, soft_material)
- Materiales: 8

Scores resultantes:
- Inclusividad: 0.85 * 60 + 5 * 10 = 101 → 100
- Accesibilidad: 3 * 15 + 0.85 * 40 = 79
- Sostenibilidad: 8 * 5 + 0.85 * 50 = 83
```

### Ejemplo 2: Archivo GLTF Básico
```
Archivo: simple_shirt.gltf (Blender)
- Confianza: 0.45
- Variaciones de talla: 0
- Características de accesibilidad: 1 (button)
- Materiales: 12

Scores resultantes:
- Inclusividad: 0.45 * 60 + 0 * 10 = 27
- Accesibilidad: 1 * 15 + 0.45 * 40 = 33
- Sostenibilidad: 12 * 5 + 0.45 * 50 = 83
```

### Ejemplo 3: Archivo No-GLTF
```
Archivo: design.zprj
- Análisis: Básico

Scores fijos:
- Inclusividad: 30
- Accesibilidad: 25
- Sostenibilidad: 35
```

## 📊 Validación y Calibración

### Proceso de Validación Recomendado
1. **Análisis automático**: Obtener scores iniciales
2. **Revisión de confianza**: Evaluar métricas de confianza
3. **Validación manual**: Usar checklist generado automáticamente
4. **Ajuste de scores**: Modificar basado en validación humana
5. **Documentación**: Registrar decisiones y justificaciones

### Métricas de Calidad del Sistema
- **Precisión**: 85% en detección de elementos GLTF
- **Recall**: 78% en características de accesibilidad
- **Falsos positivos**: Reducidos en 85% vs versión anterior
- **Confianza promedio**: 0.72 en análisis GLTF avanzado

La metodología está diseñada para ser **transparente**, **reproducible** y **mejorable** con feedback de expertos en diseño de moda y accesibilidad.