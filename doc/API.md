Perfect — thanks for sharing `main.py`. Below is a **clean, professional, HR-ready `docs/API.md`** that exactly matches your FastAPI implementation.

You can **copy–paste this as `docs/API.md`** in your repo.

---

# API Documentation

**IRD Tax RAG Assistant – REST API**

This document describes the REST API endpoints exposed by the **IRD Tax RAG Assistant**, which enables ingestion of Sri Lanka IRD tax documents (PDFs), indexing into a vector database, and question answering with source citations.

---

## Base Information

* **Base URL (local):**

  ```
  http://127.0.0.1:8000
  ```

* **Interactive API Docs (Swagger UI):**

  ```
  http://127.0.0.1:8000/docs
  ```

* **API Version:** 1.0

* **Framework:** FastAPI

* **Response Format:** JSON

---

## Authentication

No authentication is required (local / demo setup).

---

## Health Check

### `GET /health`

Check whether the API service is running.

#### Request

```
GET /health
```

#### Response

```json
{
  "status": "ok"
}
```

---

## Document Ingestion

### `POST /documents/upload`

Upload a single IRD-related PDF document (e.g., Income Tax Act, tax guide).

#### Request

* **Content-Type:** `multipart/form-data`
* **Form field:** `file` (PDF only)

#### Example (cURL)

```bash
curl -X POST http://127.0.0.1:8000/documents/upload \
  -F "file=@Income_Tax_Act.pdf"
```

#### Response

```json
{
  "filename": "Income_Tax_Act.pdf",
  "saved_path": "data/raw_pdfs/Income_Tax_Act.pdf"
}
```

#### Error Responses

* **400 Bad Request** – Non-PDF file uploaded

```json
{
  "detail": "Only PDF files are allowed."
}
```

---

## Document Indexing

### `POST /documents/index`

Processes all uploaded PDFs:

* Loads PDF pages
* Splits text into chunks
* Generates embeddings
* Stores them in the vector database (ChromaDB)

#### Request

```
POST /documents/index
```

#### Response

```json
{
  "indexed_files": [
    "Income_Tax_Act.pdf",
    "Tax_Guide_2023.pdf"
  ],
  "total_chunks": 250
}
```

#### Error Responses

* **400 Bad Request** – No PDFs found

```json
{
  "detail": "No PDFs found in data/raw_pdfs."
}
```

---

## Tax Question Answering (RAG)

### `POST /query`

Answer a natural-language tax question using Retrieval-Augmented Generation (RAG).
Responses include **citations** referencing the source documents.

#### Request Body

```json
{
  "question": "What is the personal income tax rate in Sri Lanka?",
  "top_k": 5
}
```

| Field    | Type    | Description                                      |
| -------- | ------- | ------------------------------------------------ |
| question | string  | User tax-related question                        |
| top_k    | integer | (Optional) Number of document chunks to retrieve |

#### Example (cURL)

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{
        "question": "What income is exempt from tax?",
        "top_k": 5
      }'
```

#### Response

```json
{
  "answer": "Certain income types such as employment terminal benefits and specific allowances are exempt from income tax under Sri Lankan law.",
  "citations": [
    {
      "document": "Income_Tax_Act.pdf",
      "page": 42,
      "snippet": "Employment terminal benefits received by an individual are exempt..."
    }
  ],
  "disclaimer": "This response is generated for informational purposes only and does not constitute legal or tax advice."
}
```

---

## Citation Format

Each citation contains:

* **document** – Source PDF name
* **page** – Page number (if available)
* **snippet** – Relevant extracted text

This ensures **traceability and factual grounding**, a key requirement for compliance-focused AI systems.

---

## Error Handling

| Status Code | Description                   |
| ----------- | ----------------------------- |
| 400         | Invalid input or missing data |
| 500         | Internal server error         |

---

