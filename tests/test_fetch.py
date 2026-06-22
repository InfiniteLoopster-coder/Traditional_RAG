# tests/test_arxiv_fetcher.py

from src.arxiv_fetcher import fetch_arxiv_papers
from src.config import ARXIV_MAX_DOCS, ARXIV_QUERY


def main():
    documents = fetch_arxiv_papers(
        query=ARXIV_QUERY,
        max_docs=ARXIV_MAX_DOCS,
    )

    print(f"Fetched documents: {len(documents)}")

    for index, doc in enumerate(documents, start=1):
        print("\n" + "=" * 100)
        print(f"Document {index}")
        print("-" * 100)

        print("Title:", doc.metadata.get("title"))
        print("arXiv ID:", doc.metadata.get("arxiv_id"))
        print("Published:", doc.metadata.get("published"))
        print("PDF URL:", doc.metadata.get("pdf_url"))
        print("Categories:", doc.metadata.get("categories"))

        print("\nContent Preview:")
        print(doc.page_content[:800])


if __name__ == "__main__":
    main()