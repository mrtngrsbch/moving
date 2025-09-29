# Configuración de Límites de Archivo

## 🎯 Límite Actual: 300MB

El Moving Accessibility Analyzer está configurado para aceptar archivos de hasta **300MB**, optimizado para manejar archivos grandes de diseño de moda.

## ⚙️ Configuración Técnica

### Archivo de Configuración
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 300  # Límite en MB
```

### Validación en la Interfaz
La aplicación incluye validación automática que:
- ✅ **Acepta archivos ≤ 300MB**
- ❌ **Rechaza archivos > 300MB** con mensaje de error
- ⚠️ **Advierte sobre archivos > 100MB** (análisis más lento)
- ℹ️ **Informa sobre archivos > 50MB** (tiempo normal)
- 🚀 **Optimiza archivos < 50MB** (análisis rápido)

## 📊 Tamaños Típicos por Formato

### Archivos GLTF
- **Simples**: 1-10 MB (modelos básicos)
- **Complejos**: 50-150 MB (con texturas HD)
- **Muy complejos**: 200-300 MB (múltiples variaciones)

### Archivos CLO3D
- **.zprj**: 10-100 MB (proyectos completos)
- **.zpac**: 50-200 MB (paquetes con assets)

### Archivos OBJ
- **Básicos**: 1-20 MB (solo geometría)
- **Con texturas**: 20-100 MB (materiales incluidos)

## 🚀 Optimización de Archivos

### Para Reducir Tamaño de Archivos GLTF:
```javascript
// Configuración de exportación recomendada
{
  "textureSize": 1024,        // En lugar de 4096
  "compressionLevel": "high", // Activar compresión
  "includeAnimations": false, // Si no son necesarias
  "optimizeMeshes": true      // Optimizar geometría
}
```

### Para Archivos CLO3D:
1. **Reducir resolución de texturas**
2. **Eliminar assets no utilizados**
3. **Exportar solo elementos necesarios**
4. **Usar compresión de archivos**

## 📈 Rendimiento por Tamaño

| Tamaño | Tiempo Estimado | Recomendación |
|--------|----------------|---------------|
| < 10 MB | 5-15 segundos | ✅ Óptimo |
| 10-50 MB | 15-45 segundos | ✅ Bueno |
| 50-100 MB | 45-90 segundos | ⚠️ Aceptable |
| 100-200 MB | 90-180 segundos | ⚠️ Lento |
| 200-300 MB | 180-300 segundos | ❌ Muy lento |

## 🔧 Modificar el Límite

### Para Aumentar el Límite:
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 500  # Nuevo límite en MB
```

### Para Disminuir el Límite:
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 100  # Límite más restrictivo
```

**Nota**: Después de cambiar la configuración, reiniciar el servidor:
```bash
streamlit run streamlit_app.py --server.port 8503
```

## ⚠️ Consideraciones de Memoria

### Recursos del Sistema
- **RAM requerida**: ~2-3x el tamaño del archivo
- **Archivo 300MB**: Requiere ~600-900MB RAM
- **Procesamiento**: CPU intensivo durante análisis

### Recomendaciones del Sistema
- **Mínimo**: 4GB RAM para archivos de 100MB
- **Recomendado**: 8GB RAM para archivos de 300MB
- **Óptimo**: 16GB RAM para uso intensivo

## 🚨 Manejo de Errores

### Errores Comunes
1. **"File too large"**: Archivo excede 300MB
2. **"Memory error"**: Insuficiente RAM del sistema
3. **"Timeout"**: Archivo muy complejo para procesar

### Soluciones
1. **Reducir tamaño del archivo**
2. **Aumentar memoria del sistema**
3. **Dividir archivo en partes más pequeñas**
4. **Usar formato más eficiente (GLTF recomendado)**

## 📊 Monitoreo de Uso

### Métricas Disponibles
- Tamaño promedio de archivos subidos
- Tiempo de procesamiento por tamaño
- Tasa de éxito por formato
- Uso de memoria durante análisis

### Logs de Sistema
```bash
# Ver logs de Streamlit
tail -f ~/.streamlit/logs/streamlit.log

# Monitorear uso de memoria
htop
```

## 🎯 Mejores Prácticas

### Para Usuarios
1. **Optimizar antes de subir**: Reducir tamaño cuando sea posible
2. **Usar GLTF**: Mejor análisis y eficiencia
3. **Dividir proyectos grandes**: Analizar por partes
4. **Verificar conectividad**: Archivos grandes requieren conexión estable

### Para Administradores
1. **Monitorear recursos**: CPU y memoria del servidor
2. **Configurar timeouts**: Evitar procesos colgados
3. **Implementar cache**: Reutilizar análisis previos
4. **Backup regular**: Proteger configuraciones

## 🔄 Actualizaciones Futuras

### Mejoras Planificadas
- **Análisis incremental**: Para archivos muy grandes
- **Compresión automática**: Reducir tamaño en tiempo real
- **Análisis distribuido**: Procesar en múltiples núcleos
- **Cache inteligente**: Evitar re-análisis de archivos similares

La configuración actual de 300MB está optimizada para el balance entre funcionalidad y rendimiento, permitiendo analizar archivos complejos de diseño de moda sin comprometer la experiencia del usuario.