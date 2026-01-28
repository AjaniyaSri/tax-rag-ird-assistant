from __future__ import annotations
import os
from typing import List, Dict, Any, Tuple

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

try:
    from langchain_community.chat_models import ChatOllama
except Exception:
    ChatOllama = None

from app.rag.prompt import SYSTEM_PROMPT, build_user_prompt
from app.rag.retriever import is_low_confidence


FALLBACK = "This information is not available in the provided IRD documents."
DISCLAIMER = "This response is based solely on IRD-published documents and is not professional tax advice."


def get_llm():
    """
    Provider priority:
    1) OPENAI_API_KEY -> OpenAI chat model
    2) OLLAMA_MODEL + ChatOllama available -> Ollama local
    """
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
            temperature=0.1,
        )

    if os.getenv("OLLAMA_MODEL") and ChatOllama is not None:
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL"),
            temperature=0.1,
        )

    raise RuntimeError(
        "No LLM configured. Set OPENAI_API_KEY for OpenAI OR set OLLAMA_MODEL for local Ollama."
    )


def make_context_blocks(retrieved: List[Tuple[str, Dict[str, Any], float]]) -> List[Dict[str, Any]]:
    blocks = []
    for text, meta, score in retrieved:
        blocks.append(
            {
                "text": text,
                "document": meta.get("document", "Unknown"),
                "page": int(meta.get("page", -1)),
                "section": meta.get("section", "N/A"),
                "score": score,
            }
        )
    return blocks


def answer_question(question: str, retrieved: List[Tuple[str, Dict[str, Any], float]]) -> Dict[str, Any]:
    """
    Returns dict: answer, citations(list), disclaimer
    """
    scores = [s for _, _, s in retrieved]
    if is_low_confidence(scores):
        return {"answer": FALLBACK, "citations": [], "disclaimer": DISCLAIMER}

    context_blocks = make_context_blocks(retrieved)

    llm = get_llm()
    user_prompt = build_user_prompt(question, context_blocks)

    resp = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt),
        ]
    )

    answer_text = (resp.content or "").strip()
    if not answer_text:
        answer_text = FALLBACK

    # If model violates rules, enforce fallback
    if FALLBACK.lower() in answer_text.lower():
        return {"answer": FALLBACK, "citations": [], "disclaimer": DISCLAIMER}

    # Build citations from retrieved blocks (top unique doc+page+section)
    citations = []
    seen = set()
    for b in context_blocks:
        key = (b["document"], b["page"], b["section"])
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            {
                "document": b["document"],
                "page": b["page"],
                "section": b["section"] or "N/A",
                "snippet": (b["text"][:220] + "...") if len(b["text"]) > 220 else b["text"],
            }
        )
        if len(citations) >= 5:
            break

    return {"answer": answer_text, "citations": citations, "disclaimer": DISCLAIMER}
