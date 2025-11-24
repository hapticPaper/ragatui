"""Configuration management for ragatui."""

import os
from typing import Any, Optional


class Config:
    """
    Configuration for ragatui.

    Configuration can be set via:
    1. Environment variables
    2. .env file
    3. Direct API calls

    Example .env file:
        RAGATUI_LLM_PROVIDER=local
        RAGATUI_LLM_ENDPOINT=http://localhost:11434
        RAGATUI_LLM_MODEL=llama2
    """

    def __init__(self):
        """Initialize configuration."""
        self._load_from_env()

    def _load_from_env(self):
        """Load configuration from environment variables."""
        # LLM Configuration
        self.llm_provider = os.getenv("RAGATUI_LLM_PROVIDER", "none")
        self.llm_endpoint = os.getenv("RAGATUI_LLM_ENDPOINT", "http://localhost:11434")
        self.llm_model = os.getenv("RAGATUI_LLM_MODEL", "llama2")
        self.llm_api_key = os.getenv("RAGATUI_LLM_API_KEY", "")

        # RAG Configuration
        self.rag_enabled = os.getenv("RAGATUI_RAG_ENABLED", "false").lower() == "true"
        self.rag_provider = os.getenv("RAGATUI_RAG_PROVIDER", "chromadb")
        self.rag_storage_type = os.getenv("RAGATUI_RAG_STORAGE_TYPE", "memory") # memory, sqlite, server
        self.rag_persist_directory = os.getenv("RAGATUI_RAG_PERSIST_DIRECTORY", "./chroma_db")

        # Embedding Configuration
        self.embedding_provider = os.getenv("RAGATUI_EMBEDDING_PROVIDER", "local")
        self.embedding_model = os.getenv("RAGATUI_EMBEDDING_MODEL", "embeddinggemma")
        self.embedding_api_key = os.getenv("RAGATUI_EMBEDDING_API_KEY", "")
        self.embedding_endpoint = os.getenv("RAGATUI_EMBEDDING_ENDPOINT", "http://localhost:11434")

    def get_llm_config(self) -> dict[str, Any]:
        """Get LLM configuration as a dictionary."""
        return {
            "provider": self.llm_provider,
            "endpoint": self.llm_endpoint,
            "model": self.llm_model,
            "api_key": self.llm_api_key,
        }

    def set_llm_provider(
        self,
        provider: str,
        endpoint: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Set LLM provider configuration.

        Args:
            provider: Provider type ('local', 'openai', 'anthropic', 'none')
            endpoint: API endpoint (for local providers)
            model: Model name
            api_key: API key (for cloud providers)
        """
        self.llm_provider = provider
        if endpoint:
            self.llm_endpoint = endpoint
        if model:
            self.llm_model = model
        if api_key:
            self.llm_api_key = api_key

    def get_embedding_config(self) -> dict[str, Any]:
        """Get embedding configuration as a dictionary."""
        return {
            "provider": self.embedding_provider,
            "model": self.embedding_model,
            "api_key": self.embedding_api_key,
        }

    def set_embedding_config(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        """Set embedding configuration."""
        if provider:
            self.embedding_provider = provider
        if model:
            self.embedding_model = model
        if api_key:
            self.embedding_api_key = api_key
        if endpoint:
            self.embedding_endpoint = endpoint

    def enable_rag(
        self,
        provider: str = "chromadb",
        storage_type: str = "memory",
        persist_directory: Optional[str] = None
    ):
        """
        Enable RAG functionality.

        Args:
            provider: RAG provider ('chromadb', 'pgvector')
            storage_type: Storage type ('memory', 'sqlite', 'server')
            persist_directory: Directory for persistent storage (if sqlite)
        """
        self.rag_enabled = True
        self.rag_provider = provider
        self.rag_storage_type = storage_type
        if persist_directory:
            self.rag_persist_directory = persist_directory

    def disable_rag(self):
        """Disable RAG functionality."""
        self.rag_enabled = False


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def configure_llm(
    provider: str = "local",
    endpoint: str = "http://localhost:11434",
    model: str = "llama2",
    api_key: str = "",
):
    """
    Configure LLM provider.

    This is a convenience function for setting up LLM configuration.

    Args:
        provider: Provider type ('local', 'openai', 'anthropic')
        endpoint: API endpoint (for local providers like Ollama)
        model: Model name
        api_key: API key (for cloud providers)

    Example with Ollama:
        >>> from ragatui import configure_llm
        >>> configure_llm(provider="local", endpoint="http://localhost:11434", model="llama2")

    Example with OpenAI:
        >>> configure_llm(provider="openai", model="gpt-4", api_key="sk-...")
    """
    config = get_config()
    config.set_llm_provider(provider, endpoint, model, api_key)


def configure_rag(enabled: bool = True, provider: str = "chromadb"):
    """
    Configure RAG functionality.

    Args:
        enabled: Whether to enable RAG
        provider: RAG provider ('chromadb', 'pgvector')

    Example:
        >>> from ragatui import configure_rag
        >>> configure_rag(enabled=True, provider="chromadb")
    """
    config = get_config()
    if enabled:
        config.enable_rag(provider)
    else:
        config.disable_rag()
