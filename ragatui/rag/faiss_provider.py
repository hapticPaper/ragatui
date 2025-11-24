"""FAISS RAG provider implementation."""

import os
import pickle
import json
from typing import Any, Optional
from .providers import RAGProvider

class FAISSRAGProvider(RAGProvider):
    """FAISS-based RAG provider."""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.index = None
        self.documents = []
        self.metadatas = []
        self.ids = []
        self.persist_directory = config.get("persist_directory", "./faiss_db")
        self.index_file = os.path.join(self.persist_directory, "index.faiss")
        self.meta_file = os.path.join(self.persist_directory, "metadata.pkl")

    def connect(self) -> bool:
        """Load FAISS index from disk if exists."""
        try:
            import faiss
            import numpy as np
        except ImportError:
            print("FAISS not installed. Install with 'pip install faiss-cpu numpy'")
            return False

        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)

        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            try:
                self.index = faiss.read_index(self.index_file)
                with open(self.meta_file, "rb") as f:
                    data = pickle.load(f)
                    self.documents = data["documents"]
                    self.metadatas = data["metadatas"]
                    self.ids = data["ids"]
            except Exception as e:
                print(f"Error loading FAISS index: {e}")
                return False
        
        return True

    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]]
    ) -> bool:
        """Add documents to FAISS index."""
        try:
            import faiss
            import numpy as np
            
            embeddings_np = np.array(embeddings).astype('float32')
            dimension = embeddings_np.shape[1]

            if self.index is None:
                self.index = faiss.IndexFlatL2(dimension)

            self.index.add(embeddings_np)
            self.documents.extend(documents)
            self.metadatas.extend(metadatas)
            self.ids.extend(ids)

            # Persist immediately (simple implementation)
            faiss.write_index(self.index, self.index_file)
            with open(self.meta_file, "wb") as f:
                pickle.dump({
                    "documents": self.documents,
                    "metadatas": self.metadatas,
                    "ids": self.ids
                }, f)
            
            return True
        except Exception as e:
            print(f"Error adding to FAISS: {e}")
            return False

    def query(
        self,
        query_embeddings: list[list[float]],
        n_results: int = 5
    ) -> dict[str, Any]:
        """Query FAISS index."""
        if self.index is None:
            return {"ids": [], "distances": [], "documents": [], "metadatas": []}

        try:
            import numpy as np
            
            query_np = np.array(query_embeddings).astype('float32')
            distances, indices = self.index.search(query_np, n_results)

            results = {
                "ids": [],
                "distances": [],
                "documents": [],
                "metadatas": []
            }

            for i in range(len(indices)):
                batch_ids = []
                batch_dists = []
                batch_docs = []
                batch_metas = []
                
                for j, idx in enumerate(indices[i]):
                    if idx != -1 and idx < len(self.ids):
                        batch_ids.append(self.ids[idx])
                        batch_dists.append(float(distances[i][j]))
                        batch_docs.append(self.documents[idx])
                        batch_metas.append(self.metadatas[idx])
                
                results["ids"].append(batch_ids)
                results["distances"].append(batch_dists)
                results["documents"].append(batch_docs)
                results["metadatas"].append(batch_metas)

            return results
        except Exception as e:
            print(f"Error querying FAISS: {e}")
            return {"ids": [], "distances": [], "documents": [], "metadatas": []}

    def disconnect(self):
        """No explicit disconnect needed for FAISS file-based."""
        pass
