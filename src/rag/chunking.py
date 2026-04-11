
from typing import Dict, List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def prepare_chunks(documents: List[Dict]) -> List[Dict]:
    prepared = []

    for doc in documents:
        chunks = chunk_text(doc["content"])
        for idx, chunk in enumerate(chunks):
            prepared.append(
                {
                    "id": f'{doc["title"]}_{idx}',
                    "title": doc["title"],
                    "source": doc["source"],
                    "category": doc.get("category", "general"),
                    "content": chunk,
                }
            )

    return prepared