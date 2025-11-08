"""LLM provider abstraction for ragatui."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from enum import Enum
import os


class LLMProviderType(Enum):
    """Supported LLM provider types."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    CUSTOM = "custom"


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    This allows ragatui to work with different LLM backends,
    both hosted (OpenAI, Anthropic) and local.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific arguments
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    async def analyze_logs(
        self,
        logs: List[str],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze logs and extract key information.
        
        Args:
            logs: List of log messages
            context: Optional context about what to look for
            
        Returns:
            Dictionary with analysis results
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.model = self.config.get("model", "gpt-4")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate response using OpenAI API."""
        # TODO: Implement actual OpenAI API call
        # This is a placeholder for now
        return f"[OpenAI Response to: {prompt[:50]}...]"
    
    async def analyze_logs(
        self,
        logs: List[str],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze logs using OpenAI."""
        # TODO: Implement actual log analysis
        return {
            "summary": "Log analysis placeholder",
            "key_metrics": [],
            "issues": [],
            "insights": []
        }


class LocalLLMProvider(LLMProvider):
    """Local LLM provider (e.g., Ollama, llama.cpp)."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.model_path = self.config.get("model_path")
        self.endpoint = self.config.get("endpoint", "http://localhost:11434")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """Generate response using local LLM."""
        # TODO: Implement local LLM integration
        return f"[Local LLM Response to: {prompt[:50]}...]"
    
    async def analyze_logs(
        self,
        logs: List[str],
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze logs using local LLM."""
        # TODO: Implement actual log analysis
        return {
            "summary": "Log analysis placeholder (local)",
            "key_metrics": [],
            "issues": [],
            "insights": []
        }


def get_llm_provider(
    provider_type: LLMProviderType = LLMProviderType.OPENAI,
    config: Optional[Dict[str, Any]] = None
) -> LLMProvider:
    """
    Factory function to get an LLM provider.
    
    Args:
        provider_type: Type of LLM provider to use
        config: Provider-specific configuration
        
    Returns:
        LLM provider instance
    """
    if provider_type == LLMProviderType.OPENAI:
        return OpenAIProvider(config)
    elif provider_type == LLMProviderType.LOCAL:
        return LocalLLMProvider(config)
    else:
        raise ValueError(f"Unsupported provider type: {provider_type}")
