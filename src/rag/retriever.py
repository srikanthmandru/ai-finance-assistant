
from typing import Dict, List, Optional

from src.rag.embeddings import EmbeddingService
from src.rag.vector_store import FAISSVectorStore


class FinanceRetriever:
    def __init__(self, embedding_service: EmbeddingService, vector_store: FAISSVectorStore):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 4, category: Optional[str] = None) -> List[Dict]:
        query_vector = self.embedding_service.embed_query(query)
        results = self.vector_store.search(query_vector, top_k=top_k)

        if category:
            results = [doc for doc in results if doc.get("category") == category]

        return results