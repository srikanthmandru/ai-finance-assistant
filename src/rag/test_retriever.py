from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from src.rag.build_index import build_faiss_index
from src.rag.embeddings import EmbeddingService
from src.rag.retriever import FinanceRetriever

load_dotenv()

embedding_model = OpenAIEmbeddings()

vector_store = build_faiss_index(
    data_dir="src/data/knowledge_base",
    embedding_model=embedding_model,
)

embedding_service = EmbeddingService(embedding_model)

retriever = FinanceRetriever(
    embedding_service=embedding_service,
    vector_store=vector_store,
)

results = retriever.retrieve("What is diversification?", top_k=3)

for doc in results:
    print(doc["title"], "-", doc["source"])
    print(doc["content"])
    print("-" * 50)