from langchain_openai import OpenAIEmbeddings

from src.rag.build_index import build_faiss_index
from src.rag.embeddings import EmbeddingService
from src.rag.retriever import FinanceRetriever

embedding_model = OpenAIEmbeddings()
vector_store = build_faiss_index("src/data/knowledge_base", embedding_model)

embedding_service = EmbeddingService(embedding_model)
retriever = FinanceRetriever(
    embedding_service=embedding_service,
    vector_store=vector_store,
)

docs = retriever.retrieve("What is diversification?", top_k=3)
print(docs)