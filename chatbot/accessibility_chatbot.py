#!/usr/bin/env python3
"""
Accessibility Chatbot
Chatbot especializado en análisis de accesibilidad e inclusividad en moda
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json

from chatbot.llm_client import LLMManager, LLMProvider
from chatbot.system_prompts import SystemPrompts
from analyzer_main import AnalysisResults

logger = logging.getLogger(__name__)

class ChatMessage:
    """Mensaje de chat"""
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.role = role  # 'user', 'assistant', 'system'
        self.content = content
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

class ChatSession:
    """Sesión de chat con contexto del análisis"""
    
    def __init__(self, analysis_results: AnalysisResults, session_id: str = None):
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.analysis_results = analysis_results
        self.messages: List[ChatMessage] = []
        self.created_at = datetime.now()
        
        # Inicializar con mensaje del sistema
        self._initialize_system_context()
    
    def _initialize_system_context(self):
        """Inicializar contexto del sistema"""
        base_prompt = SystemPrompts.get_base_system_prompt()
        context_prompt = SystemPrompts.get_analysis_context_prompt(self.analysis_results.__dict__)
        guidelines = SystemPrompts.get_conversation_guidelines()
        error_handling = SystemPrompts.get_error_handling_prompt()
        
        full_system_prompt = f"{base_prompt}\n\n{context_prompt}\n\n{guidelines}\n\n{error_handling}"
        
        self.messages.append(ChatMessage("system", full_system_prompt))
    
    def add_user_message(self, content: str):
        """Agregar mensaje del usuario"""
        self.messages.append(ChatMessage("user", content))
    
    def add_assistant_message(self, content: str):
        """Agregar mensaje del asistente"""
        self.messages.append(ChatMessage("assistant", content))
    
    def get_messages_for_llm(self) -> List[Dict[str, str]]:
        """Obtener mensajes en formato para LLM"""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Obtener resumen de la conversación"""
        user_messages = [msg for msg in self.messages if msg.role == "user"]
        assistant_messages = [msg for msg in self.messages if msg.role == "assistant"]
        
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "total_messages": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "analysis_file": getattr(self.analysis_results, 'file_type', 'Unknown'),
            "analysis_scores": {
                "inclusivity": getattr(self.analysis_results, 'inclusivity_score', 0),
                "accessibility": getattr(self.analysis_results, 'accessibility_score', 0),
                "sustainability": getattr(self.analysis_results, 'sustainability_score', 0)
            }
        }

class AccessibilityChatbot:
    """Chatbot especializado en accesibilidad e inclusividad"""
    
    def __init__(self):
        self.llm_manager = LLMManager()
        self.active_sessions: Dict[str, ChatSession] = {}
        self.default_provider = None
        self._initialize_default_provider()
    
    def _initialize_default_provider(self):
        """Inicializar proveedor por defecto"""
        available_providers = self.llm_manager.get_available_providers()
        if available_providers:
            self.default_provider = available_providers[0]
            logger.info(f"Proveedor por defecto: {self.default_provider.value}")
        else:
            logger.warning("No hay proveedores LLM disponibles")
    
    def create_session(self, analysis_results: AnalysisResults) -> str:
        """Crear nueva sesión de chat"""
        session = ChatSession(analysis_results)
        self.active_sessions[session.session_id] = session
        
        logger.info(f"Nueva sesión de chat creada: {session.session_id}")
        return session.session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Obtener sesión existente"""
        return self.active_sessions.get(session_id)
    
    async def chat(
        self, 
        session_id: str, 
        user_message: str, 
        provider: Optional[LLMProvider] = None
    ) -> Tuple[str, bool]:
        """
        Procesar mensaje de chat
        Returns: (respuesta, éxito)
        """
        session = self.get_session(session_id)
        if not session:
            return "Error: Sesión no encontrada", False
        
        # Usar proveedor especificado o por defecto
        selected_provider = provider or self.default_provider
        if not selected_provider:
            return "Error: No hay proveedores LLM disponibles", False
        
        client = self.llm_manager.get_client(selected_provider)
        if not client:
            return f"Error: Proveedor {selected_provider.value} no disponible", False
        
        try:
            # Agregar mensaje del usuario
            session.add_user_message(user_message)
            
            # Obtener respuesta del LLM
            messages = session.get_messages_for_llm()
            response = await client.chat_completion(messages)
            
            # Extraer texto de respuesta
            assistant_response = client.get_response_text(response)
            
            # Agregar respuesta del asistente
            session.add_assistant_message(assistant_response)
            
            logger.info(f"Chat procesado exitosamente en sesión {session_id}")
            return assistant_response, True
            
        except Exception as e:
            error_msg = f"Error procesando chat: {str(e)}"
            logger.error(f"Error en chat {session_id}: {e}")
            return error_msg, False
    
    def get_available_providers(self) -> List[Dict[str, Any]]:
        """Obtener información de proveedores disponibles"""
        providers_info = []
        
        # Importar el gestor de configuración
        from config.llm_config import llm_config_manager
        
        for provider in self.llm_manager.get_available_providers():
            config = llm_config_manager.get_config(provider)
            providers_info.append({
                "provider": provider.value,
                "name": provider.value.title(),
                "model": config.model,
                "available": True
            })
        
        return providers_info
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Obtener historial de mensajes de una sesión"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        # Filtrar mensajes del sistema para el historial público
        return [
            msg.to_dict() for msg in session.messages 
            if msg.role in ["user", "assistant"]
        ]
    
    def get_suggested_questions(self, analysis_results: AnalysisResults) -> List[str]:
        """Generar preguntas sugeridas basadas en el análisis"""
        suggestions = []
        
        # Preguntas basadas en scores
        if analysis_results.inclusivity_score < 60:
            suggestions.append("¿Cómo puedo mejorar la inclusividad de mi diseño?")
            suggestions.append("¿Qué variaciones de talla debería considerar?")
        
        if analysis_results.accessibility_score < 60:
            suggestions.append("¿Qué tipos de cierres son más accesibles?")
            suggestions.append("¿Cómo puedo hacer mi diseño más fácil de usar?")
        
        if analysis_results.sustainability_score < 60:
            suggestions.append("¿Cómo puedo reducir el impacto ambiental de mi diseño?")
            suggestions.append("¿Qué materiales son más sostenibles?")
        
        # Preguntas generales siempre disponibles
        suggestions.extend([
            "Explícame cómo se calcularon mis scores",
            "¿Qué significa mi puntuación de confianza?",
            "¿Qué validaciones manuales necesito hacer?",
            "Compara mi diseño con las mejores prácticas"
        ])
        
        return suggestions[:6]  # Limitar a 6 sugerencias
    
    async def test_providers(self) -> Dict[str, bool]:
        """Probar conexión con todos los proveedores"""
        results = {}
        
        for provider in LLMProvider:
            try:
                result = await self.llm_manager.test_connection(provider)
                results[provider.value] = result
            except Exception as e:
                logger.error(f"Error probando {provider.value}: {e}")
                results[provider.value] = False
        
        return results
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Limpiar sesiones antiguas"""
        current_time = datetime.now()
        sessions_to_remove = []
        
        for session_id, session in self.active_sessions.items():
            age_hours = (current_time - session.created_at).total_seconds() / 3600
            if age_hours > max_age_hours:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.active_sessions[session_id]
            logger.info(f"Sesión {session_id} eliminada por antigüedad")
        
        return len(sessions_to_remove)

# Instancia global del chatbot
accessibility_chatbot = AccessibilityChatbot()