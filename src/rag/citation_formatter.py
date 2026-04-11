
from typing import Dict, List


def format_sources(docs: List[Dict]) -> str:
    if not docs:
        return "Sources: None"

    unique_sources = []
    seen = set()

    for doc in docs:
        key = (doc.get("title"), doc.get("source"))
        if key not in seen:
            seen.add(key)
            unique_sources.append(f'- {doc.get("title")} ({doc.get("source")})')

    return "Sources:\n" + "\n".join(unique_sources)