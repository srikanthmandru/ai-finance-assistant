
import json
from pathlib import Path

from src.rag.chunking import prepare_chunks
from src.rag.embeddings import EmbeddingService
from src.rag.vector_store import FAISSVectorStore
import os


def load_documents(data_dir: str):
    docs = []
    for file in Path(data_dir).glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                docs.extend(data)
            # elif isinstance(data, dict) and "documents" in data:
            #     docs.extend(data["documents"])
    return docs


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

    embedding_model = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))

    vector_store = build_faiss_index(
        data_dir="src/data/knowledge_base",
        embedding_model=embedding_model,
    )

    print(f"FAISS index built successfully with {len(vector_store.documents)} chunks.")