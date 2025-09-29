# Documentación del Chatbot de Accesibilidad

## 🎯 Descripción General

El Chatbot de Accesibilidad es un asistente de IA especializado en análisis de accesibilidad e inclusividad en diseño de moda. Está integrado directamente en la interfaz web del Moving Accessibility Analyzer y proporciona interpretación inteligente de los resultados de análisis.

## 🚀 Características Principales

### Especialización en Moda Accesible
- **Conocimiento específico** de metodologías de scoring
- **Interpretación contextual** de resultados de análisis
- **Recomendaciones accionables** para mejoras
- **Validación de mejores prácticas** de la industria

### Soporte Multi-LLM
- **OpenAI GPT-4** - Mejor calidad general
- **Anthropic Claude** - Excelente para análisis detallado
- **Groq** - Muy rápido y gratuito
- **Mistral** - Buena relación calidad-precio
- **OpenRouter** - Acceso a múltiples modelos

### Integración Completa
- **Contexto automático** del análisis actual
- **Preguntas sugeridas** basadas en resultados
- **Historial de conversación** persistente
- **Interfaz intuitiva** en Streamlit

## 🔧 Configuración

### 1. Variables de Entorno

Copia `.env.example` a `.env` y configura al menos una API key:

```bash
cp .env.example .env
```

```env
# Configura al menos una de estas:
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GROQ_API_KEY=gsk_your-key-here
MISTRAL_API_KEY=your-key-here
OPENROUTER_API_KEY=sk-or-your-key-here
```

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 3. Verificación

El chatbot se inicializa automáticamente al cargar la aplicación. Si no hay API keys configuradas, mostrará un mensaje informativo.

## 📊 Arquitectura del Sistema

### Componentes Principales

```
chatbot/
├── accessibility_chatbot.py    # Chatbot principal
├── llm_client.py              # Cliente unificado LLM
├── system_prompts.py          # Prompts especializados
└── __init__.py

config/
├── llm_config.py              # Configuración LLM
└── __init__.py
```

### Flujo de Datos

1. **Análisis completado** → Resultados disponibles
2. **Usuario hace pregunta** → Contexto + pregunta
3. **Sistema genera prompt** → Prompt especializado + contexto
4. **LLM procesa** → Respuesta contextualizada
5. **Usuario recibe respuesta** → Interpretación específica

## 🎯 Capacidades del Chatbot

### Interpretación de Scores
```python
# Ejemplo de pregunta:
"¿Por qué mi score de inclusividad es 33/100?"

# Respuesta contextualizada:
"Tu score de inclusividad es 33/100 porque:
- Confianza del análisis: 0.55 × 60 = 33 puntos
- Variaciones de talla: 0 × 10 = 0 puntos
- Sin variaciones de talla detectadas en tu modelo GLTF..."
```

### Recomendaciones Específicas
- **Mejoras de inclusividad**: Variaciones de talla, escalado paramétrico
- **Optimización de accesibilidad**: Tipos de cierres, materiales suaves
- **Sostenibilidad**: Reducción de materiales, opciones eco-friendly

### Validación Manual
- **Identificación de limitaciones** del análisis automático
- **Checklist específico** para validación humana
- **Priorización de tareas** según impacto

## 🔍 System Prompts Especializados

### Prompt Base
```python
"""Eres un asistente experto en análisis de accesibilidad e inclusividad 
en diseño de moda, especializado en el Moving Accessibility Analyzer.

CONOCIMIENTO ESPECÍFICO:
- Metodología de scoring exacta
- Tipos de análisis (GLTF avanzado vs básico)
- Elementos de accesibilidad y sus puntuaciones
- Limitaciones y mejores prácticas"""
```

### Contexto Dinámico
- **Información del archivo** analizado
- **Scores específicos** obtenidos
- **Elementos detectados** (cierres, materiales, tallas)
- **Nivel de confianza** del análisis

## 💡 Preguntas Sugeridas

### Basadas en Scores Bajos
- "¿Cómo puedo mejorar la inclusividad de mi diseño?"
- "¿Qué tipos de cierres son más accesibles?"
- "¿Cómo puedo reducir el impacto ambiental?"

### Preguntas Generales
- "Explícame cómo se calcularon mis scores"
- "¿Qué significa mi puntuación de confianza?"
- "¿Qué validaciones manuales necesito hacer?"

## 🔧 API del Chatbot

### Crear Sesión
```python
session_id = accessibility_chatbot.create_session(analysis_results)
```

### Procesar Chat
```python
response, success = await accessibility_chatbot.chat(
    session_id, 
    user_message, 
    provider=LLMProvider.OPENAI
)
```

### Obtener Historial
```python
history = accessibility_chatbot.get_session_history(session_id)
```

## 🎨 Interfaz de Usuario

### Componentes Visuales
- **Chat container** con historial de mensajes
- **Input field** para nuevas preguntas
- **Selector de proveedor** LLM
- **Preguntas sugeridas** en botones
- **Información de sesión** expandible

### Experiencia de Usuario
1. **Análisis completado** → Chatbot aparece automáticamente
2. **Preguntas sugeridas** → Click para usar
3. **Chat libre** → Escribir preguntas personalizadas
4. **Respuestas contextualizadas** → Específicas al análisis
5. **Historial persistente** → Durante la sesión

## 🔒 Seguridad y Privacidad

### Manejo de API Keys
- **Variables de entorno** para configuración
- **No almacenamiento** en código
- **Validación automática** de disponibilidad

### Datos de Usuario
- **Sesiones temporales** (24 horas por defecto)
- **No persistencia** en base de datos
- **Contexto limitado** al análisis actual

## 📈 Métricas y Monitoreo

### Métricas Disponibles
- **Sesiones activas** por período
- **Preguntas por sesión** promedio
- **Proveedores más utilizados**
- **Tipos de preguntas** más comunes

### Logs del Sistema
```python
logger.info(f"Nueva sesión de chat creada: {session_id}")
logger.info(f"Chat procesado exitosamente en sesión {session_id}")
logger.error(f"Error en chat {session_id}: {error}")
```

## 🚀 Mejoras Futuras

### Funcionalidades Planificadas
- **Persistencia de sesiones** en base de datos
- **Análisis de sentimiento** de feedback
- **Recomendaciones personalizadas** por usuario
- **Integración con validación manual**

### Optimizaciones Técnicas
- **Cache de respuestas** comunes
- **Streaming de respuestas** para mejor UX
- **Análisis de costos** por proveedor
- **Rate limiting** inteligente

## 🎯 Casos de Uso

### Diseñador Novato
- **Educación** sobre accesibilidad
- **Interpretación** de scores técnicos
- **Guía paso a paso** para mejoras

### Diseñador Experto
- **Validación** de decisiones de diseño
- **Comparación** con mejores prácticas
- **Optimización** de procesos

### Marca/Empresa
- **Evaluación** de líneas de productos
- **Compliance** con estándares
- **Reporting** para stakeholders

El chatbot transforma el análisis técnico en conversaciones comprensibles y accionables, democratizando el acceso a expertise en accesibilidad e inclusividad en moda.