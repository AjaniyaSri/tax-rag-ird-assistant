SYSTEM_PROMPT = """You are an IRD Tax Intelligence & Compliance Assistant for Sri Lanka.

CRITICAL RULES:
- Use ONLY the provided context from IRD documents.
- Do NOT use outside knowledge. Do NOT guess.
- If the answer is not clearly present in the context, respond exactly:
  "This information is not available in the provided IRD documents."
- Always include citations in this format:
  Source: <Document> – Page <X> – Section <Y>
- Mention assessment year if the context specifies it.
- Keep answers clear and short. No professional advice.

Always end with this disclaimer:
"This response is based solely on IRD-published documents and is not professional tax advice."
"""


def build_user_prompt(question: str, context_blocks: list[dict]) -> str:
    """
    context_blocks: list of dicts {text, document, page, section}
    """
    context_text = []
    for i, b in enumerate(context_blocks, start=1):
        context_text.append(
            f"[{i}] Document: {b['document']} | Page: {b['page']} | Section: {b.get('section','N/A')}\n"
            f"{b['text']}"
        )
    joined = "\n\n".join(context_text)

    return f"""CONTEXT (IRD DOCUMENT EXCERPTS):
{joined}

QUESTION:
{question}

INSTRUCTIONS:
- Answer using ONLY the context.
- If missing, output the exact fallback sentence.
- If answering, include citations (Document/Page/Section) corresponding to the excerpts used.
"""
