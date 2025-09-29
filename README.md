# Moving Accessibility Analyzer MVP

Un MVP para analizar la inclusividad y accesibilidad de diseños de moda, procesando archivos `.zprj`, `.zpac` y `.obj` para extraer métricas específicas sin depender de LLMs costosos.

## 🎯 Objetivo

Evaluar diseños de moda en términos de:
- **Inclusividad**: Rango de tallas, adaptabilidad, diseño universal
- **Accesibilidad**: Tamaño de ojales, tipos de cierres, facilidad de uso
- **Sostenibilidad**: Materiales, durabilidad, impacto ambiental

## 🔧 Arquitectura Técnica

### Estrategia de Procesamiento
- **Archivos .zprj**: Extracción de metadatos XML (sin procesar geometría 3D completa)
- **Archivos .zpac**: Análisis avanzado de paquetes con datos ricos (RECOMENDADO)
- **Archivos .obj**: Análisis básico de geometría para métricas de complejidad
- **Análisis estructurado**: Sin usar LLMs para datos binarios grandes
- **Métricas específicas**: Algoritmos dedicados para cada factor de inclusividad

### Tecnologías
- **Backend**: Node.js + Express
- **Procesamiento**: yauzl (ZIP), xml2js (metadatos), sharp (imágenes)
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Límites**: Archivos hasta 300MB (configurado en .streamlit/config.toml)

## 🚀 Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor
npm start

# Desarrollo con auto-reload
npm run dev
```

## 📊 Métricas Analizadas

### Inclusividad (0-100)
- Rango de tallas disponibles
- Adaptabilidad del diseño
- Características de diseño universal

### Accesibilidad (0-100)
- Tamaño y posición de ojales
- Tipos de cierres y su facilidad de uso
- Elementos adaptativos

### Propiedades de Tela
- Elasticidad y stretch
- Peso y drapeado
- Características sensoriales

## 🔍 Análisis de Archivos

### Archivos .zprj (Proyectos CLO3D)
1. **Extracción ZIP**: Descompresión del archivo proyecto
2. **Parsing XML**: Lectura de metadatos estructurados
3. **Análisis específico**: Extracción de datos de tallas, materiales, cierres
4. **Cálculo de métricas**: Algoritmos dedicados para cada factor

### Archivos .obj (Modelos 3D)
1. **Análisis geométrico**: Conteo de vértices, caras, normales
2. **Métricas de complejidad**: Evaluación del nivel de detalle
3. **Recomendaciones**: Sugerencias para análisis más completo

## 📈 Roadmap MVP

### Fase 1 (Actual)
- [x] Estructura básica del servidor
- [x] Interfaz de usuario responsive
- [x] Procesamiento de archivos .zprj y .obj
- [x] Extracción de metadatos XML
- [x] Métricas básicas de inclusividad

### Fase 2 (Próxima)
- [ ] Parser específico para metadatos CLO3D reales
- [ ] Algoritmos avanzados de análisis de tallas
- [ ] Base de datos de propiedades de telas
- [ ] Exportación de reportes PDF

### Fase 3 (Futuro)
- [ ] API REST para integraciones
- [ ] Dashboard de múltiples proyectos
- [ ] Comparativas y benchmarking
- [ ] Machine Learning para patrones

## 🧪 Testing

Para probar el MVP:

1. **Archivos de prueba**: Usa archivos .zprj, .zpac, .gltf o .obj de CLO3D
2. **Límite de tamaño**: Máximo 300MB por archivo (configurado automáticamente)
3. **Formatos soportados**: .gltf (avanzado), .zprj, .zpac, .obj (básicos)

## 📝 Estructura del Proyecto

```
moving-accessibility-analyzer/
├── analyzer.py         # Analizador principal (Python)
├── streamlit_app.py    # Interfaz web Streamlit
├── requirements.txt    # Dependencias Python
├── uploads/            # Archivos temporales
├── server.js           # Servidor Node.js (legacy)
└── README.md          # Documentación
```

## 🔬 Metodología de Análisis

### Sin LLMs para Archivos Binarios
- **Problema**: LLMs de texto no son eficientes para archivos de 200MB
- **Solución**: Extracción directa de metadatos estructurados
- **Ventaja**: Análisis rápido, preciso y económico

### Métricas Específicas
- **Tallas**: Análisis de rangos y medidas en metadatos
- **Cierres**: Detección de tipos y dimensiones
- **Telas**: Propiedades físicas y de comodidad
- **Accesibilidad**: Factores de usabilidad motriz y sensorial

## 🤝 Contribuir

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-metrica`
3. Commit cambios: `git commit -m 'Agregar nueva métrica'`
4. Push: `git push origin feature/nueva-metrica`
5. Crear Pull Request

## 📄 Licencia

MIT License - Ver archivo LICENSE para detalles