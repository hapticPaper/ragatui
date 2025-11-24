"""LLM provider abstraction for ragatui."""

import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


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

    def __init__(self, config: Optional[dict[str, Any]] = None):
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
        logs: list[str],
        context: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Analyze logs and extract key information.

        Args:
            logs: List of log messages
            context: Optional context about what to look for

        Returns:
            Dictionary with analysis results
        """
        pass

    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""

    def __init__(self, config: Optional[dict[str, Any]] = None):
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
        logs: list[str],
        context: Optional[str] = None
    ) -> dict[str, Any]:
        """Analyze logs using OpenAI."""
        # TODO: Implement actual log analysis
        return {
            "summary": "Log analysis placeholder",
            "key_metrics": [],
            "issues": [],
            "insights": []
        }

    async def get_embedding(self, text: str) -> list[float]:
        """Generate embedding using OpenAI."""
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError("openai package is required for OpenAIProvider. Install with 'pip install ragatui[llm]'")

        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.embeddings.create(
            input=text,
            model=self.config.get("embedding_model", "text-embedding-ada-002")
        )
        return response.data[0].embedding


class LocalLLMProvider(LLMProvider):
    """Local LLM provider (e.g., Ollama, llama.cpp)."""

    def __init__(self, config: Optional[dict[str, Any]] = None):
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
        logs: list[str],
        context: Optional[str] = None
    ) -> dict[str, Any]:
        """Analyze logs using local LLM."""
        # TODO: Implement actual log analysis
        return {
            "summary": "Log analysis placeholder (local)",
            "key_metrics": [],
            "issues": [],
            "insights": []
        }

    async def get_embedding(self, text: str) -> list[float]:
        """Generate embedding using local LLM (Ollama or OpenAI-compatible)."""
        import json
        import urllib.request
        
        # Try OpenAI-compatible endpoint first if port is not 11434 or explicitly configured
        is_ollama_default = "11434" in self.endpoint
        
        # Strategy 1: OpenAI-compatible /v1/embeddings (e.g. LM Studio, Ollama v1)
        if not is_ollama_default or "/v1" in self.endpoint:
            try:
                # Construct URL
                base_url = self.endpoint.rstrip("/")
                if not base_url.endswith("/v1"):
                    url = f"{base_url}/v1/embeddings"
                else:
                    url = f"{base_url}/embeddings"
                
                payload = {
                    "model": self.config.get("embedding_model", "embeddinggemma"),
                    "input": text
                }
                
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    url, 
                    data=data, 
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))
                    # OpenAI format: {"data": [{"embedding": [...]}]}
                    if "data" in result and len(result["data"]) > 0:
                        return result["data"][0]["embedding"]
            except Exception as e:
                # If this wasn't the intended target or failed, fall through to Ollama native
                if not is_ollama_default:
                    print(f"Error getting embedding from OpenAI-compatible endpoint: {e}")
                    # Don't raise yet, try Ollama native if applicable
        
        # Strategy 2: Ollama Native API /api/embeddings
        url = f"{self.endpoint}/api/embeddings"
        # If endpoint already has path, strip it? Assuming endpoint is base URL
        if "/api/" in self.endpoint:
             url = self.endpoint # Assume user provided full path or close to it
        elif self.endpoint.endswith("/v1"):
             # If user provided /v1, we probably shouldn't try /api/embeddings unless we strip /v1
             url = self.endpoint.replace("/v1", "") + "/api/embeddings"

        payload = {
            "model": self.config.get("embedding_model", "embeddinggemma"),
            "prompt": text
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url, 
                data=data, 
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["embedding"]
        except Exception as e:
            print(f"Error getting embedding from Local LLM: {e}")
            raise e


def get_llm_provider(
    provider_type: LLMProviderType = LLMProviderType.OPENAI,
    config: Optional[dict[str, Any]] = None
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
