from __future__ import annotations
from typing import List, Dict, Any, Tuple
from langchain_community.vectorstores import Chroma
from app.ingestion.indexer import build_or_load_chroma


def load_retriever(
    persist_dir: str,
    collection_name: str = "ird_tax",
) -> Chroma:
    return build_or_load_chroma(persist_dir, collection_name)


def retrieve(
    vectordb: Chroma,
    question: str,
    top_k: int = 6,
) -> List[Tuple[str, Dict[str, Any], float]]:
    """
    Returns list of (text, metadata, score).
    Score here is distance-like depending on backend;
    smaller is better in Chroma similarity_search_with_score.
    """
    results = vectordb.similarity_search_with_score(question, k=top_k)
    out = []
    for doc, score in results:
        out.append((doc.page_content, doc.metadata, float(score)))
    return out


def is_low_confidence(scores: List[float]) -> bool:
    """
    Basic heuristic. In Chroma, lower scores are usually more similar.
    If everything is very high, it likely didn't find relevant info.
    """
    if not scores:
        return True
    best = min(scores)
    # This threshold may vary; tune if needed.
    return best > 1.2
