"""RAG database integration for storing and retrieving execution history."""

from typing import Any, Optional


class RAGDatabase:
    """
    RAG database for storing execution history and context.

    This allows the LLM to compare current execution with past runs,
    providing better insights and analysis.
    """

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize RAG database.

        Args:
            connection_string: Database connection string (optional)
        """
        self.connection_string = connection_string
        self.connected = False

    async def connect(self) -> bool:
        """
        Connect to the RAG database.

        Returns:
            True if connection successful
        """
        if self.connected:
            return True

        from ragatui.config import get_config
        config = get_config()

        if not config.rag_enabled:
            return False

        try:
            if config.rag_provider == "faiss":
                from ragatui.rag.faiss_provider import FAISSRAGProvider
                self.provider = FAISSRAGProvider({
                    "persist_directory": config.rag_persist_directory
                })
            elif config.rag_provider == "chromadb":
                # Keep existing ChromaDB logic or move to provider
                # For now, let's focus on FAISS as requested
                print("ChromaDB support is being deprecated in favor of FAISS.")
                return False
            else:
                print(f"Unknown RAG provider: {config.rag_provider}")
                return False

            if self.provider.connect():
                self.connected = True
                return True
            return False

        except Exception as e:
            print(f"Failed to connect to RAG provider: {e}")
            return False

    async def store_execution(
        self,
        execution_id: str,
        metadata: dict[str, Any],
        logs: list[str],
        metrics: dict[str, Any]
    ) -> bool:
        """
        Store execution data in the RAG database.

        Args:
            execution_id: Unique execution identifier
            metadata: Execution metadata
            logs: Log messages
            metrics: Collected metrics

        Returns:
            True if stored successfully
        """
        if not self.connected:
            if not await self.connect():
                return False

        try:
            # Prepare text for embedding
            summary_text = f"Execution: {metadata.get('title', 'Untitled')}\n"
            summary_text += f"Date: {metadata.get('timestamp', '')}\n"
            summary_text += f"Metrics: {metrics}\n"
            summary_text += "Logs:\n" + "\n".join(logs[:50])
            
            # Generate embedding
            from ragatui.llm.providers import get_llm_provider, LLMProviderType
            from ragatui.config import get_config
            
            config = get_config()
            provider_type = LLMProviderType(config.embedding_provider)
            provider = get_llm_provider(
                provider_type, 
                config={
                    "embedding_model": config.embedding_model, 
                    "api_key": config.embedding_api_key,
                    "endpoint": config.embedding_endpoint
                }
            )
            
            embedding = await provider.get_embedding(summary_text)
            
            # Store via provider
            return self.provider.add(
                ids=[execution_id],
                documents=[summary_text],
                embeddings=[embedding],
                metadatas=[{
                    "execution_id": execution_id,
                    **{k: str(v) for k, v in metadata.items()},
                    **{k: str(v) for k, v in metrics.items()}
                }]
            )
        except Exception as e:
            print(f"Failed to store execution in RAG: {e}")
            return False

    async def query_similar_executions(
        self,
        current_metrics: dict[str, Any],
        limit: int = 5
    ) -> list[dict[str, Any]]:
        """
        Query for similar past executions.

        Args:
            current_metrics: Current execution metrics
            limit: Maximum number of results

        Returns:
            List of similar execution records
        """
        if not self.connected:
            if not await self.connect():
                return []

        try:
            # Create query text
            query_text = f"Metrics: {current_metrics}"
            
            # Generate embedding
            from ragatui.llm.providers import get_llm_provider, LLMProviderType
            from ragatui.config import get_config
            
            config = get_config()
            provider_type = LLMProviderType(config.embedding_provider)
            provider = get_llm_provider(
                provider_type, 
                config={
                    "embedding_model": config.embedding_model, 
                    "api_key": config.embedding_api_key,
                    "endpoint": config.embedding_endpoint
                }
            )
            
            embedding = await provider.get_embedding(query_text)
            
            # Query via provider
            results = self.provider.query(
                query_embeddings=[embedding],
                n_results=limit
            )
            
            # Format results
            formatted_results = []
            if results['ids']:
                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        "id": results['ids'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "document": results['documents'][0][i],
                        "distance": results['distances'][0][i] if 'distances' in results else None
                    })
            
            return formatted_results
        except Exception as e:
            print(f"Failed to query RAG: {e}")
            return []

    async def get_execution_history(
        self,
        function_name: str,
        limit: int = 10
    ) -> list[dict[str, Any]]:
        """
        Get execution history for a specific function.

        Args:
            function_name: Name of the function
            limit: Maximum number of results

        Returns:
            List of execution records
        """
        # TODO: Implement history retrieval
        return []

    async def add_context(
        self,
        context_type: str,
        content: str,
        metadata: Optional[dict[str, Any]] = None
    ) -> bool:
        """
        Add context to the RAG database.

        This could be documentation, best practices, common issues, etc.

        Args:
            context_type: Type of context (e.g., "documentation", "best_practice")
            content: The context content
            metadata: Optional metadata

        Returns:
            True if added successfully
        """
        # TODO: Implement context addition
        return True

    async def search_context(
        self,
        query: str,
        context_type: Optional[str] = None,
        limit: int = 5
    ) -> list[dict[str, Any]]:
        """
        Search for relevant context.

        Args:
            query: Search query
            context_type: Optional filter by context type
            limit: Maximum number of results

        Returns:
            List of relevant context items
        """
        # TODO: Implement context search
        return []

    async def disconnect(self) -> None:
        """Disconnect from the RAG database."""
        self.connected = False
