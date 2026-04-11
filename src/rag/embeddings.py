
from typing import List


class EmbeddingService:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return self.embedding_model.embed_documents(texts)

    def embed_query(self, query: str) -> List[float]:
        return self.embedding_model.embed_query(query)