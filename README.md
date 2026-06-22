# Traditional RAG: arXiv Research Assistant

This project implements the initial version of a **Traditional Retrieval-Augmented Generation (RAG)** pipeline for fetching the latest AI research papers from arXiv, processing them into LangChain `Document` objects, splitting them into chunks, and storing them in a Chroma vector database.

The long-term goal is to build an assistant that can answer user questions about recent AI research papers using a continuously updated knowledge base.

---

## Project Goal

AI research changes daily, and new papers are published on arXiv frequently. This project aims to build a system that:

1. Fetches the latest AI research papers from arXiv.
2. Converts paper metadata and summaries into LangChain documents.
3. Splits documents into retrieval-friendly chunks.
4. Embeds the chunks into vector representations.
5. Stores the chunks in Chroma vector database.
6. Retrieves relevant chunks when a user asks a question.
7. Uses an LLM to generate grounded answers from the retrieved context.
8. Later schedules daily ingestion using Apache Airflow.

---

## Current Status

The current implementation covers the first ingestion milestone.

### Completed

- Direct arXiv paper fetching using the `arxiv` Python package.
- Conversion of arXiv results into LangChain `Document` objects.
- Metadata extraction for each paper.
- Text splitting using LangChain text splitters.
- Chroma vector store initialization.
- Deterministic chunk ID generation.
- End-to-end ingestion pipeline structure.
- Basic test scripts for fetching, chunking, and ingestion.

### Pending

- Local embedding support using HuggingFace sentence-transformers.
- Manual vector retrieval test.
- RAG answer generation chain.
- FastAPI `/ask` endpoint.
- Airflow DAG for daily ingestion.
- Full PDF text extraction from arXiv papers.

---

## Architecture

```text
arXiv API
   |
   v
Direct arxiv.Client() Fetcher
   |
   v
LangChain Document Objects
   |
   v
RecursiveCharacterTextSplitter
   |
   v
Document Chunks
   |
   v
Embedding Model
   |
   v
Chroma Vector Database
   |
   v
Retriever
   |
   v
Prompt + LLM
   |
   v
Grounded Answer with Sources
```

---

## Tech Stack

- Python
- uv
- LangChain
- arXiv Python package
- ChromaDB
- OpenAI Embeddings
- python-dotenv
- FastAPI
- Apache Airflow planned for orchestration

---

## Project Structure

```text
Traditional_RAG/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── arxiv_fetcher.py
│   ├── document_processor.py
│   ├── vector_store.py
│   └── ingestion_pipeline.py
│
├── tests/
│   ├── __init__.py
│   ├── test_arxiv_fetcher.py
│   ├── test_document_processor.py
│   └── test_ingestion_pipeline.py
│
├── data/
│   └── chroma_db/
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Setup Instructions

This project uses **uv** for dependency management.

Do not use `pip install` directly for this project.

### 1. Clone the repository

```powershell
git clone <repository-url>
cd Traditional_RAG
```

### 2. Sync dependencies

```powershell
uv sync
```

### 3. Add required dependencies if not already added

```powershell
uv add langchain langchain-core langchain-text-splitters langchain-openai langchain-chroma chromadb arxiv pymupdf pypdf python-dotenv fastapi uvicorn
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
ARXIV_QUERY=cat:cs.AI OR cat:cs.CL OR cat:cs.LG
ARXIV_MAX_DOCS=5

CHROMA_DIR=data/chroma_db
CHROMA_COLLECTION=arxiv_ai_papers

OPENAI_API_KEY=your_openai_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
```

> Important: Do not commit `.env` to GitHub.

---

## Current Implementation Details

### 1. arXiv Fetcher

File:

```text
src/arxiv_fetcher.py
```

The project uses the `arxiv` package directly instead of LangChain `ArxivLoader`.

Reason:

- More control over metadata.
- Better compatibility with current `arxiv` package versions.
- Easier deduplication using `arxiv_id`.
- Better support for future PDF extraction.

Each fetched paper is converted into a LangChain `Document`.

Captured metadata includes:

```text
arxiv_id
title
authors
summary
published
updated
pdf_url
entry_id
categories
source
```

---

### 2. Document Processor

File:

```text
src/document_processor.py
```

Documents are split using `RecursiveCharacterTextSplitter`.

Current splitter configuration:

```python
chunk_size=1200
chunk_overlap=200
separators=["\n\n", "\n", ". ", " ", ""]
```

At the current stage, documents mainly contain paper metadata and summaries, so the number of chunks may be close to the number of papers.

When full PDF extraction is added, this step will produce many more chunks per paper.

---

### 3. Vector Store

File:

```text
src/vector_store.py
```

Chroma is used as the vector database.

The project generates deterministic chunk IDs using:

```text
arxiv_id + chunk_index + content_preview
```

This helps reduce duplicate chunk storage during repeated ingestion runs.

---

### 4. Ingestion Pipeline

File:

```text
src/ingestion_pipeline.py
```

The ingestion pipeline performs:

```text
Fetch arXiv papers
   ↓
Split documents into chunks
   ↓
Store chunks in Chroma
```

Run it using:

```powershell
uv run python -m src.ingestion_pipeline
```

---

## Running Tests

Use module mode when running test scripts.

### Test arXiv fetcher

```powershell
uv run python -m tests.test_arxiv_fetcher
```

### Test document processor

```powershell
uv run python -m tests.test_document_processor
```

### Test ingestion pipeline

```powershell
uv run python -m tests.test_ingestion_pipeline
```

---

## Important Windows Note

If the project is inside OneDrive, `.venv` files may get locked by OneDrive or Windows processes.

If you see errors like:

```text
Access is denied. (os error 5)
```

Recommended fix:

1. Close VS Code, Python processes, and terminals.
2. Move the virtual environment outside OneDrive.
3. Use uv environment variable:

```powershell
$env:UV_PROJECT_ENVIRONMENT = "C:\uv-envs\traditional-rag"
uv sync
```

To set it permanently:

```powershell
[Environment]::SetEnvironmentVariable(
  "UV_PROJECT_ENVIRONMENT",
  "C:\uv-envs\traditional-rag",
  "User"
)
```

---

## Known Issues

### 1. OpenAI quota error

You may see:

```text
openai.RateLimitError: Error code: 429
code: insufficient_quota
```

This means the OpenAI API key is valid, but the account/project does not have enough API quota or billing enabled.

Possible fixes:

- Add OpenAI API credits.
- Enable billing for the correct OpenAI project.
- Use local embeddings with HuggingFace sentence-transformers.

### 2. Do not use direct test file execution

Avoid:

```powershell
uv run python .\tests\test_arxiv_fetcher.py
```

Use:

```powershell
uv run python -m tests.test_arxiv_fetcher
```

This avoids Python import path issues with the `src` package.

---

## Next Development Milestones

### Milestone 1: Configurable Embedding Provider

Add support for:

```text
EMBEDDING_PROVIDER=local
EMBEDDING_PROVIDER=openai
```

Local embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This will allow development without OpenAI billing.

---

### Milestone 2: Manual Retrieval

Add a retrieval test:

```text
User query
   ↓
Similarity search in Chroma
   ↓
Top-k relevant chunks
   ↓
Print metadata and content preview
```

---

### Milestone 3: RAG Answer Chain

Add:

- Retriever
- Prompt template
- LLM call
- Source-aware answer response

Expected flow:

```text
Question
   ↓
Retrieve relevant chunks
   ↓
Format context
   ↓
Prompt LLM
   ↓
Generate answer with source titles
```

---

### Milestone 4: FastAPI Endpoint

Add API endpoint:

```text
POST /ask
```

Example request:

```json
{
  "question": "What are the latest papers about RAG and LLM agents?"
}
```

Expected response:

```json
{
  "question": "...",
  "answer": "...",
  "sources": [...]
}
```

---

### Milestone 5: Airflow Daily Ingestion

Add Airflow DAG:

```text
daily_arxiv_rag_ingestion
```

The DAG will run every day and ingest latest papers into Chroma.

---

### Milestone 6: Full PDF Extraction

Current ingestion uses paper summaries.

Future enhancement:

```text
Download PDF
   ↓
Extract full text using PyMuPDF
   ↓
Clean text
   ↓
Section-aware chunking
   ↓
Store chunks with paper metadata
```

---

## Git Workflow

Recommended branch:

```powershell
git checkout -b feature/traditional-rag-arxiv-ingestion
```

Check status:

```powershell
git status
```

Add files:

```powershell
git add .
```

Commit:

```powershell
git commit -m "feat: add arxiv ingestion pipeline with chroma setup"
```

Push branch:

```powershell
git push origin feature/traditional-rag-arxiv-ingestion
```

---

## PR Summary

This implementation adds the foundation for a Traditional RAG system that can ingest latest arXiv AI research papers and prepare them for vector-based retrieval.

The current version focuses on ingestion architecture. Query-time retrieval, RAG answer generation, API exposure, and Airflow scheduling will be added in upcoming milestones.

---

## License

This project is for learning and research implementation purposes.
