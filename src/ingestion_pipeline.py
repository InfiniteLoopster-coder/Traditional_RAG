from src.arxiv_fetcher import fetch_arxiv_papers
from src.config import ARXIV_MAX_DOCS, ARXIV_QUERY
from src.document_processor import split_documents
from src.vector_store import store_chunks


def run_arxiv_ingestion() -> dict:
    """
    End-to-end ingestion pipeline:
    1. Fetch latest arXiv papers
    2. Convert to LangChain Documents
    3. Split into chunks
    4. Store chunks into Chroma
    """

    documents = fetch_arxiv_papers(
        query=ARXIV_QUERY,
        max_docs=ARXIV_MAX_DOCS,
    )

    chunks = split_documents(documents)

    stored_count = store_chunks(chunks)

    return {
        "papers_fetched": len(documents),
        "chunks_created": len(chunks),
        "chunks_stored": stored_count,
    }


if __name__ == "__main__":
    result = run_arxiv_ingestion()
    print(result)