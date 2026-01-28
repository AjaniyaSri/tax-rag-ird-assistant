from __future__ import annotations
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models.schemas import UploadResponse, IndexResponse, QueryRequest, QueryResponse, Citation
from app.ingestion.pdf_loader import load_pdf_pages
from app.ingestion.chunker import chunk_pages
from app.ingestion.indexer import index_chunks
from app.rag.retriever import load_retriever, retrieve
from app.rag.qa import answer_question


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

RAW_PDF_DIR = os.path.join(PROJECT_ROOT, "data", "raw_pdfs")
PERSIST_DIR = os.path.join(PROJECT_ROOT, "vectordb")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "ird_tax")

os.makedirs(RAW_PDF_DIR, exist_ok=True)
os.makedirs(PERSIST_DIR, exist_ok=True)

app = FastAPI(title="IRD Tax RAG Assistant", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    save_path = os.path.join(RAW_PDF_DIR, file.filename)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return UploadResponse(filename=file.filename, saved_path=save_path)


@app.post("/documents/index", response_model=IndexResponse)
def index_documents():
    pdf_files = [f for f in os.listdir(RAW_PDF_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        raise HTTPException(status_code=400, detail="No PDFs found in data/raw_pdfs.")

    all_chunks = []
    for pdf in pdf_files:
        path = os.path.join(RAW_PDF_DIR, pdf)
        pages = load_pdf_pages(path, document_name=pdf)
        chunks = chunk_pages(pages)
        all_chunks.extend(chunks)

    total_chunks, docs = index_chunks(all_chunks, persist_dir=PERSIST_DIR, collection_name=COLLECTION_NAME)

    return IndexResponse(indexed_files=docs, total_chunks=total_chunks)


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    vectordb = load_retriever(PERSIST_DIR, collection_name=COLLECTION_NAME)
    retrieved = retrieve(vectordb, req.question, top_k=req.top_k)

    result = answer_question(req.question, retrieved)

    citations = [Citation(**c) for c in result.get("citations", [])]
    return QueryResponse(
        answer=result["answer"],
        citations=citations,
        disclaimer=result["disclaimer"],
    )
