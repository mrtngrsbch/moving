#!/usr/bin/env python3
"""
LLM Configuration Manager
Configuración centralizada para múltiples proveedores de LLM
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv no está instalado

class LLMProvider(Enum):
    """Proveedores de LLM soportados"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"
    MISTRAL = "mistral"
    OPENROUTER = "openrouter"

@dataclass
class LLMConfig:
    """Configuración para un proveedor de LLM"""
    provider: LLMProvider
    api_key: str
    base_url: Optional[str] = None
    model: str = ""
    max_tokens: int = 4000
    temperature: float = 0.7
    timeout: int = 30

class LLMConfigManager:
    """Gestor de configuraciones de LLM"""
    
    def __init__(self):
        self.configs = self._load_default_configs()
    
    def _load_default_configs(self) -> Dict[LLMProvider, LLMConfig]:
        """Cargar configuraciones por defecto"""
        return {
            LLMProvider.OPENAI: LLMConfig(
                provider=LLMProvider.OPENAI,
                api_key=os.getenv("OPENAI_API_KEY", ""),
                model="gpt-4o-mini",
                max_tokens=4000,
                temperature=0.7
            ),
            
            LLMProvider.ANTHROPIC: LLMConfig(
                provider=LLMProvider.ANTHROPIC,
                api_key=os.getenv("ANTHROPIC_API_KEY", ""),
                model="claude-3-haiku-20240307",
                max_tokens=4000,
                temperature=0.7
            ),
            
            LLMProvider.GROQ: LLMConfig(
                provider=LLMProvider.GROQ,
                api_key=os.getenv("GROQ_API_KEY", ""),
                base_url="https://api.groq.com/openai/v1",
                model="llama-3.1-8b-instant",
                max_tokens=4000,
                temperature=0.7
            ),
            
            LLMProvider.MISTRAL: LLMConfig(
                provider=LLMProvider.MISTRAL,
                api_key=os.getenv("MISTRAL_API_KEY", ""),
                base_url="https://api.mistral.ai/v1",
                model="mistral-small-latest",
                max_tokens=4000,
                temperature=0.7
            ),
            
            LLMProvider.OPENROUTER: LLMConfig(
                provider=LLMProvider.OPENROUTER,
                api_key=os.getenv("OPENROUTER_API_KEY", ""),
                base_url="https://openrouter.ai/api/v1",
                model="anthropic/claude-3-haiku",
                max_tokens=4000,
                temperature=0.7
            )
        }
    
    def get_config(self, provider: LLMProvider) -> LLMConfig:
        """Obtener configuración para un proveedor"""
        return self.configs.get(provider)
    
    def get_available_providers(self) -> list[LLMProvider]:
        """Obtener proveedores con API keys configuradas"""
        available = []
        for provider, config in self.configs.items():
            if config.api_key:
                available.append(provider)
        return available
    
    def update_config(self, provider: LLMProvider, **kwargs):
        """Actualizar configuración de un proveedor"""
        if provider in self.configs:
            config = self.configs[provider]
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
    
    def get_model_options(self, provider: LLMProvider) -> list[str]:
        """Obtener opciones de modelos por proveedor"""
        model_options = {
            LLMProvider.OPENAI: [
                "gpt-4o",
                "gpt-4o-mini", 
                "gpt-4-turbo",
                "gpt-3.5-turbo"
            ],
            LLMProvider.ANTHROPIC: [
                "claude-3-5-sonnet-20241022",
                "claude-3-haiku-20240307",
                "claude-3-sonnet-20240229"
            ],
            LLMProvider.GROQ: [
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ],
            LLMProvider.MISTRAL: [
                "mistral-large-latest",
                "mistral-small-latest",
                "codestral-latest"
            ],
            LLMProvider.OPENROUTER: [
                "anthropic/claude-3-haiku",
                "anthropic/claude-3-sonnet",
                "meta-llama/llama-3.1-8b-instruct",
                "mistralai/mistral-7b-instruct"
            ]
        }
        return model_options.get(provider, [])

# Instancia global del gestor
llm_config_manager = LLMConfigManager()