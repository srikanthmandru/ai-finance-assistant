
import json
from pathlib import Path

from src.rag.chunking import prepare_chunks
from src.rag.embeddings import EmbeddingService
from src.rag.vector_store import FAISSVectorStore


def load_documents(data_dir: str):
    documents = []
    for file_path in Path(data_dir).glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            documents.append(json.load(f))
    return documents


def build_faiss_index(data_dir: str, embedding_model):
    raw_docs = load_documents(data_dir)
    chunked_docs = prepare_chunks(raw_docs)

    embedding_service = EmbeddingService(embedding_model)
    texts = [doc["content"] for doc in chunked_docs]
    vectors = embedding_service.embed_texts(texts)

    dimension = len(vectors[0])
    vector_store = FAISSVectorStore(dimension=dimension)
    vector_store.add_documents(chunked_docs, vectors)

    return vector_store

if __name__ == "__main__":
    from dotenv import load_dotenv
    from langchain_openai import OpenAIEmbeddings

    load_dotenv()

    embedding_model = OpenAIEmbeddings()

    vector_store = build_faiss_index(
        data_dir="src/data/knowledge_base",
        embedding_model=embedding_model,
    )

    print(f"FAISS index built successfully with {len(vector_store.documents)} chunks.")