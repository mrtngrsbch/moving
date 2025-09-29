#!/usr/bin/env python3
"""
LLM Client Unificado
Cliente que maneja múltiples proveedores de LLM de forma transparente
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
import httpx
import json
from dataclasses import asdict

from config.llm_config import LLMProvider, LLMConfig, llm_config_manager

logger = logging.getLogger(__name__)

class LLMClient:
    """Cliente unificado para múltiples proveedores de LLM"""
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.config = llm_config_manager.get_config(provider)
        
        if not self.config or not self.config.api_key:
            raise ValueError(f"No se encontró configuración válida para {provider.value}")
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        stream: bool = False
    ) -> Dict[str, Any]:
        """Realizar chat completion con el proveedor configurado"""
        
        try:
            if self.provider == LLMProvider.OPENAI:
                return await self._openai_completion(messages, stream)
            elif self.provider == LLMProvider.ANTHROPIC:
                return await self._anthropic_completion(messages, stream)
            elif self.provider == LLMProvider.GROQ:
                return await self._groq_completion(messages, stream)
            elif self.provider == LLMProvider.MISTRAL:
                return await self._mistral_completion(messages, stream)
            elif self.provider == LLMProvider.OPENROUTER:
                return await self._openrouter_completion(messages, stream)
            else:
                raise ValueError(f"Proveedor no soportado: {self.provider}")
                
        except Exception as e:
            logger.error(f"Error en chat completion con {self.provider.value}: {e}")
            raise
    
    async def _openai_completion(self, messages: List[Dict[str, str]], stream: bool) -> Dict[str, Any]:
        """Completion para OpenAI"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": stream
        }
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def _anthropic_completion(self, messages: List[Dict[str, str]], stream: bool) -> Dict[str, Any]:
        """Completion para Anthropic Claude"""
        headers = {
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Convertir formato de mensajes para Anthropic
        system_message = ""
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append(msg)
        
        payload = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": user_messages,
            "stream": stream
        }
        
        if system_message:
            payload["system"] = system_message
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def _groq_completion(self, messages: List[Dict[str, str]], stream: bool) -> Dict[str, Any]:
        """Completion para Groq"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": stream
        }
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                f"{self.config.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def _mistral_completion(self, messages: List[Dict[str, str]], stream: bool) -> Dict[str, Any]:
        """Completion para Mistral"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": stream
        }
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                f"{self.config.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def _openrouter_completion(self, messages: List[Dict[str, str]], stream: bool) -> Dict[str, Any]:
        """Completion para OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://moving-accessibility-analyzer.com",
            "X-Title": "Moving Accessibility Analyzer"
        }
        
        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": stream
        }
        
        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            response = await client.post(
                f"{self.config.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    def get_response_text(self, response: Dict[str, Any]) -> str:
        """Extraer texto de respuesta según el proveedor"""
        try:
            if self.provider == LLMProvider.ANTHROPIC:
                return response.get("content", [{}])[0].get("text", "")
            else:
                return response.get("choices", [{}])[0].get("message", {}).get("content", "")
        except (KeyError, IndexError) as e:
            logger.error(f"Error extrayendo respuesta de {self.provider.value}: {e}")
            return "Error procesando respuesta del LLM"

class LLMManager:
    """Gestor de múltiples clientes LLM"""
    
    def __init__(self):
        self.clients: Dict[LLMProvider, LLMClient] = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Inicializar clientes disponibles"""
        available_providers = llm_config_manager.get_available_providers()
        
        for provider in available_providers:
            try:
                self.clients[provider] = LLMClient(provider)
                logger.info(f"Cliente LLM inicializado: {provider.value}")
            except Exception as e:
                logger.warning(f"No se pudo inicializar {provider.value}: {e}")
    
    def get_available_providers(self) -> List[LLMProvider]:
        """Obtener proveedores disponibles"""
        return list(self.clients.keys())
    
    def get_client(self, provider: LLMProvider) -> Optional[LLMClient]:
        """Obtener cliente específico"""
        return self.clients.get(provider)
    
    def get_default_client(self) -> Optional[LLMClient]:
        """Obtener cliente por defecto (prioridad: OpenAI > Anthropic > Groq > otros)"""
        priority_order = [
            LLMProvider.OPENAI,
            LLMProvider.ANTHROPIC,
            LLMProvider.GROQ,
            LLMProvider.MISTRAL,
            LLMProvider.OPENROUTER
        ]
        
        for provider in priority_order:
            if provider in self.clients:
                return self.clients[provider]
        
        # Si no hay ninguno de la lista de prioridad, devolver el primero disponible
        if self.clients:
            return next(iter(self.clients.values()))
        
        return None
    
    async def test_connection(self, provider: LLMProvider) -> bool:
        """Probar conexión con un proveedor"""
        client = self.get_client(provider)
        if not client:
            return False
        
        try:
            test_messages = [
                {"role": "system", "content": "Responde solo con 'OK'"},
                {"role": "user", "content": "Test"}
            ]
            
            response = await client.chat_completion(test_messages)
            return bool(response)
        except Exception as e:
            logger.error(f"Test de conexión falló para {provider.value}: {e}")
            return False

# Instancia global del gestor
llm_manager = LLMManager()