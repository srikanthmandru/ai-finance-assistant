# src/rag/vector_store.py
from typing import Dict, List

import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: List[Dict] = []

    def add_documents(self, docs: List[Dict], vectors: List[List[float]]) -> None:
        np_vectors = np.array(vectors, dtype="float32")
        self.index.add(np_vectors)
        self.documents.extend(docs)

    def search(self, query_vector: List[float], top_k: int = 4) -> List[Dict]:
        query = np.array([query_vector], dtype="float32")
        distances, indices = self.index.search(query, top_k)

        results = []
        for score, idx in zip(distances[0], indices[0]):
            if idx == -1 or idx >= len(self.documents):
                continue

            doc = self.documents[idx]
            results.append(
                {
                    **doc,
                    "score": float(score),
                }
            )

        return results