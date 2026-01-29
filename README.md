Perfect 👍
Here’s a **complete, clean, professional README.md** you can directly paste into your GitHub repo.
It’s written in a **final-year / research / demo-ready style** — ideal for evaluators, recruiters, and GitHub visitors.

---

# Intelligent Sri Lanka IRD Tax Intelligence & Compliance Assistant

### *(Retrieval-Augmented Generation System)*

## Overview

The **Intelligent Sri Lanka IRD Tax Intelligence & Compliance Assistant** is a document-grounded **Question Answering (QA) system** built using **Retrieval-Augmented Generation (RAG)**.
It allows users to query Sri Lanka Inland Revenue Department (IRD) tax information and receive **accurate, citation-backed answers** derived strictly from **official IRD PDF documents**.

The system is explicitly designed to **prevent hallucinations**, ensure **full traceability**, and support **compliance-oriented use cases**, making it suitable for educational, research, and regulatory demonstrations.

---

## Key Features

* Upload official IRD tax documents (PDF)
* Automatic page-wise text extraction
* Overlapping chunking with metadata preservation
* Semantic search using vector embeddings
* Context-aware question answering (RAG)
* Citation support (document name, page number, section, snippet)
* Strict fallback when information is unavailable
* Web-based UI for document ingestion and querying
* Fully local inference using Ollama (no paid API keys)

---

## Technology Stack

### Backend

* Python 3.11+
* FastAPI
* Uvicorn
* PyMuPDF (PDF text extraction)
* ChromaDB (vector database)
* Sentence Transformers (embeddings)

### LLM & Retrieval

* Ollama (local LLM inference)
* phi-3 / tinyllama (lightweight models)
* Custom dependency-safe chunking pipeline

### Frontend

* Streamlit (web-based UI)

### Development Tools

* Git & GitHub
* Virtual Environment (venv)

---

## System Architecture (High-Level)

1. User uploads IRD PDF documents
2. PDFs are parsed page-by-page
3. Text is split into overlapping chunks
4. Chunks are embedded and stored in a vector database
5. User queries are embedded and matched semantically
6. Relevant chunks are retrieved
7. Retrieved context is passed to the LLM
8. Final answer is generated with citations

---

## Setup Instructions (Windows)

### 1. Clone the Repository

```bash
git clone https://github.com/AjaniyaSri/tax-rag-ird-assistant.git
cd tax-rag-ird-assistant
```

---

### 2. Create and Activate Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```powershell
pip install --upgrade pip
pip install fastapi uvicorn python-multipart pymupdf chromadb langchain langchain-community sentence-transformers streamlit requests
```

---

### 4. Install Ollama and Pull Model

Download Ollama from:
[https://ollama.com](https://ollama.com)

Pull a lightweight model:

```powershell
ollama pull phi3
setx OLLAMA_MODEL phi3
```

> Restart the terminal after setting the environment variable.

---

## Running the Application

### Backend (FastAPI)

From the project root:

```powershell
venv\Scripts\activate
uvicorn app.main:app --port 8000
```

Available endpoints:

* Health check: [http://localhost:8000/health](http://localhost:8000/health)
* API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Frontend (Streamlit UI)

In a separate terminal:

```powershell
venv\Scripts\activate
streamlit run UI/app.py
```

Open in browser:

```
http://localhost:8501
```

---

## Deployments

**Streamlit Cloud Deployment:**
[https://tax-ird-assistant.streamlit.app](https://tax-ird-assistant.streamlit.app)

---

## API Overview

### Upload PDF

**POST** `/documents/upload`

* Multipart form-data
* Field name: `file`

---

### Index Documents

**POST** `/documents/index`
Indexes all uploaded PDFs into the vector database.

---

### Query Documents

**POST** `/query`

Example request:

```json
{
  "question": "What is the corporate income tax rate?",
  "top_k": 6
}
```

Example response:

```json
{
  "answer": "The corporate income tax rate is ...",
  "citations": [
    {
      "document": "IRD_Guide.pdf",
      "page": 12,
      "section": "Tax Rates",
      "snippet": "..."
    }
  ],
  "disclaimer": "This response is based solely on IRD-published documents and is not professional tax advice."
}
```

---

## Assumptions

* The assistant answers **only from uploaded IRD PDF documents**
* No external or internet-based tax knowledge is used
* If the answer is not found, the system responds with:
  **“This information is not available in the provided IRD documents.”**
* Uploaded documents are assumed to be official and text-extractable PDFs

---

## Compliance & Safety

* No hallucinated answers
* Full source traceability through citations
* Local inference (data never leaves the machine)
* Suitable for compliance-sensitive environments

---

## Limitations

* OCR is not included for scanned PDFs
* Section detection is heuristic-based
* Coverage limited to uploaded documents

---

## Future Enhancements

* OCR support for scanned PDFs
* Advanced re-ranking for improved retrieval accuracy
* Authentication and role-based access
* Multi-language support (Sinhala / Tamil / English)
* Cloud-based scalable deployment options

---

## License

This project is intended for **educational, research, and demonstration purposes only**.

---

## Design Rationale

The design decisions, system architecture, and use of Retrieval-Augmented Generation (RAG) are documented in the following PDF:

📄 **Design Rationale – Intelligent Sri Lanka IRD Tax Intelligence & Compliance Assistant**
`doc/Intelligent_Sri_Lanka_IRD_Tax_Intelligence_Compliance_Assistant.pdf`


