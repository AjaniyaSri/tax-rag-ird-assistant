from __future__ import annotations
from typing import List, Dict, Any
from app.ingestion.pdf_loader import PageText


def guess_section(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return "N/A"
    for ln in lines[:3]:
        if len(ln) <= 80 and any(ch.isalpha() for ch in ln):
            return ln[:80]
    return "N/A"


def simple_split(text: str, chunk_size: int = 1200, overlap: int = 150) -> List[str]:
    """
    Simple character-based chunking with overlap.
    No external dependencies.
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)

    return chunks


def chunk_pages(
    pages: List[PageText],
    chunk_size: int = 1200,
    chunk_overlap: int = 150
) -> List[Dict[str, Any]]:
    chunks: List[Dict[str, Any]] = []

    for p in pages:
        section = guess_section(p.text)
        pieces = simple_split(p.text, chunk_size=chunk_size, overlap=chunk_overlap)

        for idx, piece in enumerate(pieces):
            chunks.append(
                {
                    "text": piece,
                    "metadata": {
                        "document": p.document,
                        "page": p.page,
                        "section": section,
                        "chunk_index": idx,
                    },
                }
            )

    return chunks
