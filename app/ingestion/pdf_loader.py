from __future__ import annotations
import fitz  # PyMuPDF
from dataclasses import dataclass
from typing import List


@dataclass
class PageText:
    document: str
    page: int
    text: str


def load_pdf_pages(pdf_path: str, document_name: str | None = None) -> List[PageText]:
    """
    Extracts text from each page while keeping the page number.
    """
    doc = fitz.open(pdf_path)
    name = document_name or pdf_path.split("/")[-1]

    pages: List[PageText] = []
    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text").strip()
        if text:
            pages.append(PageText(document=name, page=i + 1, text=text))

    doc.close()
    return pages
