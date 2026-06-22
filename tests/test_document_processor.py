from src.arxiv_fetcher import fetch_arxiv_papers
from src.config import ARXIV_MAX_DOCS, ARXIV_QUERY
from src.document_processor import split_documents


def main():
    documents = fetch_arxiv_papers(
        query=ARXIV_QUERY,
        max_docs=ARXIV_MAX_DOCS,
    )

    chunks = split_documents(documents)

    print(f"Original documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks[:5], start=1):
        print("\n" + "=" * 100)
        print(f"Chunk {index}")
        print("-" * 100)
        print("Metadata:", chunk.metadata)
        print("\nContent Preview:")
        print(chunk.page_content[:700])


if __name__ == "__main__":
    main()