"""Base RAG provider interface."""

from abc import ABC, abstractmethod
from typing import Any, Optional

class RAGProvider(ABC):
    """Abstract base class for RAG providers."""

    def __init__(self, config: dict[str, Any]):
        self.config = config

    @abstractmethod
    def connect(self) -> bool:
        """Connect to the database."""
        pass

    @abstractmethod
    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]]
    ) -> bool:
        """Add documents to the database."""
        pass

    @abstractmethod
    def query(
        self,
        query_embeddings: list[list[float]],
        n_results: int = 5
    ) -> dict[str, Any]:
        """Query the database."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the database."""
        pass
