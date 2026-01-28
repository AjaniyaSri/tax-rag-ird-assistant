from __future__ import annotations
import os
from typing import List, Tuple
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings():
    """
    Uses OpenAI embeddings if OPENAI_API_KEY exists, otherwise local HF embeddings.
    """
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    # Local embeddings (no API key needed)
    return HuggingFaceEmbeddings(model_name=os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))


def build_or_load_chroma(persist_dir: str, collection_name: str = "ird_tax") -> Chroma:
    embeddings = get_embeddings()
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )


def index_chunks(
    chunks: List[dict],
    persist_dir: str,
    collection_name: str = "ird_tax",
) -> Tuple[int, List[str]]:
    """
    Index chunks into ChromaDB.
    Returns total_chunks, documents_indexed list.
    """
    vectordb = build_or_load_chroma(persist_dir, collection_name)

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    vectordb.add_texts(texts=texts, metadatas=metadatas)
    vectordb.persist()

    docs = sorted(list({m["document"] for m in metadatas}))
    return len(texts), docs
