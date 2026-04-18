from src.rag.retriever import FinanceRetriever


class MockEmbeddingService:
    def embed_query(self, query):
        return [0.1, 0.2, 0.3]


class MockVectorStore:
    def search(self, query_vector, top_k=4):
        return [
            {
                "title": "ETF Basics",
                "source": "Investopedia",
                "category": "etfs",
                "content": "ETF content",
                "score": 0.12,
            }
        ]


def test_retriever_returns_docs():
    retriever = FinanceRetriever(
        embedding_service=MockEmbeddingService(),
        vector_store=MockVectorStore(),
    )

    results = retriever.retrieve("What is an ETF?", top_k=2)

    assert len(results) == 1
    assert results[0]["title"] == "ETF Basics"